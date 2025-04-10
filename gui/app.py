import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
from algorithms.search import bfs, dfs, ucs, ids, greedy, astar, ida_star, simple_hill_climbing, steepest_ascent_hill_climbing, stochastic_hill_climbing, simulated_annealing, beam_search, and_or_search

INITIAL_STATE = ((1, 2, 3),  
                 (4, 5, 6),  
                 (0, 7, 8))

GOAL_STATE = ((1, 2, 3), (4, 5, 6), (7, 8, 0))

class PuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title('8-Puzzle Solver')
        self.root.geometry('1000x750')
        self.root.configure(bg='#f0f0f0')

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()

        self.algorithm_var = tk.StringVar(value='BFS')
        self.tiles = []
        self.move_count = 0
        self.start_time = 0
        self.time_results = {}
        self.is_solving = False
        self.pause_event = threading.Event()
        self.pause_event.set()
        self.steps = []
        self.current_step_index = 0
        self.speed = tk.DoubleVar(value=0.5)

        self.algorithms = {
            "BFS": bfs,
            "DFS": dfs,
            "UCS": ucs,
            "IDS": ids,
            "Greedy": greedy,
            "A*": astar, 
            "IDA*": ida_star,
            "Simple Hill Climbing": simple_hill_climbing,
            "Steepest Ascent Hill Climbing": steepest_ascent_hill_climbing,
            "Stochastic Hill Climbing": stochastic_hill_climbing,
            "Simulated Annealing": simulated_annealing,
            "Beam Search": beam_search,
            "And-Or Search": and_or_search
        }

        self.create_widgets() 
        self.reset_board()   


    def configure_styles(self):
        self.style.configure('TFrame', background='#F5F7FA')
        self.style.configure('Header.TLabel', background='#3498DB', foreground='white', font=('Helvetica', 20, 'bold'), padding=15)
        self.style.configure('Title.TLabel', font=('Helvetica', 14, 'bold'), background='#F5F7FA', foreground='#2C3E50')
        self.style.configure('Board.TFrame', background='#FFFFFF', relief='solid', borderwidth=2)
        self.style.configure('Tile.TLabel', font=('Helvetica', 24, 'bold'), background='#3498DB', foreground='white', width=3, padding=15, relief='raised', borderwidth=2)
        self.style.configure('Empty.TLabel', background='#ECF0F1', relief='sunken', width=4, padding=20)
        self.style.configure('TRadiobutton', font=('Helvetica', 11), background='#F5F7FA', foreground='#2C3E50')
        self.style.configure('TButton', font=('Helvetica', 12, 'bold'), padding=8)
        self.style.map('TButton', foreground=[('active', 'white'), ('!active', 'white')], background=[('active', '#2980B9'), ('!active', '#3498DB')])
        self.style.configure('Time.TLabel', font=('Helvetica', 13, 'bold'), foreground='#2980B9', background='#F5F7FA')

    def create_widgets(self):
        header = ttk.Frame(self.root)
        header.pack(fill=tk.X)
        ttk.Label(header, text='8-Puzzle Solver', style='Header.TLabel').pack(fill=tk.X)

        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        main_container.columnconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)
        main_container.columnconfigure(2, weight=1)

        left_panel = ttk.Frame(main_container)
        left_panel.grid(row=0, column=0, sticky='nsew', padx=10)

        ttk.Label(left_panel, text='Chọn thuật toán:', style='Title.TLabel').pack(anchor=tk.W, padx=10, pady=(5, 10))
        for algo in self.algorithms:
            ttk.Radiobutton(left_panel, text=algo, variable=self.algorithm_var, value=algo).pack(anchor=tk.W, padx=10, pady=3)

        ttk.Label(left_panel, text='Time elapsed:', style='Time.TLabel').pack(anchor=tk.W, padx=10, pady=(15, 0))
        self.time_display = ttk.Label(left_panel, text='0.0000 seconds', style='Time.TLabel')
        self.time_display.pack(anchor=tk.W, padx=10, pady=(0, 15))

        ttk.Button(left_panel, text='Solve Puzzle', command=self.start_solving, style='TButton').pack(fill=tk.X, padx=10, pady=4)
        self.pause_button = ttk.Button(left_panel, text='Pause', command=self.toggle_pause, style='TButton')
        self.pause_button.pack(fill=tk.X, padx=10, pady=4)
        ttk.Button(left_panel, text='Reset Board', command=self.reset_board, style='TButton').pack(fill=tk.X, padx=10, pady=4)
        ttk.Button(left_panel, text='Export Solution', command=self.export_steps, style='TButton').pack(fill=tk.X, padx=10, pady=4)

        middle_panel = ttk.Frame(main_container)
        middle_panel.grid(row=0, column=1, sticky='nsew', padx=10)

        board_frame = ttk.Frame(middle_panel)
        board_frame.pack()

        state_label_frame = ttk.Frame(board_frame)
        state_label_frame.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        ttk.Label(state_label_frame, text='Initial State', style='Title.TLabel').grid(row=0, column=0, padx=15)
        ttk.Label(state_label_frame, text='Goal State', style='Title.TLabel').grid(row=0, column=1, padx=15)

        self.initial_frame = ttk.Frame(board_frame)
        self.initial_frame.grid(row=1, column=0, padx=15)
        self.goal_frame = ttk.Frame(board_frame)
        self.goal_frame.grid(row=1, column=1, padx=15)

        current_frame = ttk.Frame(board_frame)
        current_frame.grid(row=2, column=0, columnspan=2, pady=(30, 0))
        ttk.Label(current_frame, text='Current State', style='Title.TLabel').pack(pady=5)
        self.step_label = ttk.Label(current_frame, text='Step 0 of 0', style='Title.TLabel')
        self.step_label.pack()
        self.board_container = ttk.Frame(current_frame)
        self.board_container.pack()

        # Tạo 9 ô chỉ một lần
        for i in range(3):
            row = []
            for j in range(3):
                label = ttk.Label(self.board_container, style='Tile.TLabel', anchor='center')
                label.grid(row=i, column=j, padx=2, pady=2)
                row.append(label)
            self.tiles.append(row)

        right_panel = ttk.Frame(main_container)
        right_panel.grid(row=0, column=2, sticky='nsew', padx=10)

        ttk.Label(right_panel, text='Các bước đi:', style='Title.TLabel').pack(anchor=tk.W, padx=10, pady=(0, 5))

        self.steps_frame = ttk.Frame(right_panel)
        self.steps_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        self.steps_scroll = ttk.Scrollbar(self.steps_frame)
        self.steps_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.steps_display = tk.Text(self.steps_frame, height=15, width=30, font=('Consolas', 11), wrap=tk.WORD, yscrollcommand=self.steps_scroll.set, bg='#FFFFFF', fg='#2C3E50')
        self.steps_display.pack(fill=tk.BOTH, expand=True)
        self.steps_scroll.config(command=self.steps_display.yview)

        nav_buttons = [
            ('← Bước trước', self.previous_step),
            ('→ Bước sau', self.next_step),
            ('⏹ Dừng', self.stop_solving),
            ('▶ Tiếp tục', self.resume_solving)
        ]
        for text, command in nav_buttons:
            ttk.Button(right_panel, text=text, command=command, style='TButton').pack(fill=tk.X, padx=10, pady=3)

    def update_board(self, state):
        for i in range(3):
            for j in range(3):
                value = state[i][j]
                label = self.tiles[i][j]
                if value == 0:
                    label.config(text='', style='Empty.TLabel')
                else:
                    label.config(text=str(value), style='Tile.TLabel')
        self.step_label.config(text=f"Step {self.current_step_index + 1} of {len(self.steps)}")

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def draw_static_board(self, frame, state):
        board_frame = ttk.Frame(frame, style='Board.TFrame')
        board_frame.pack(padx=5, pady=5)
        for r, row in enumerate(state):
            for c, value in enumerate(row):
                style = 'Empty.TLabel' if value == 0 else 'Tile.TLabel'
                text = '' if value == 0 else str(value)
                tile = ttk.Label(board_frame, text=text, style=style)
                tile.grid(row=r, column=c, padx=2, pady=2, sticky='nsew')
        for i in range(3):
            board_frame.grid_columnconfigure(i, weight=1)
            board_frame.grid_rowconfigure(i, weight=1)

    def start_solving(self):
        if self.is_solving:
            return
        self.is_solving = True
        self.pause_event.set()
        threading.Thread(target=self.solve, daemon=True).start()

    def toggle_pause(self):
        if self.pause_event.is_set():
            self.pause_event.clear()
            self.pause_button.config(text='Resume')
        else:
            self.pause_event.set()
            self.pause_button.config(text='Pause')

    def solve(self):
        algorithm = self.algorithm_var.get()
        self.start_time = time.time()
        algorithm_function = self.algorithms.get(algorithm)

        if not algorithm_function:
            messagebox.showerror('Error', f'Algorithm "{algorithm}" not found')
            self.is_solving = False
            return

        result = algorithm_function(INITIAL_STATE, GOAL_STATE)
        elapsed_time = time.time() - self.start_time

        if result is None:
            messagebox.showinfo('Info', 'No solution found')
            self.is_solving = False
        else:
            self.steps = result
            self.current_step_index = 0
            self.steps_display.delete('1.0', tk.END)
            self.time_display.config(text=f'{elapsed_time:.4f} seconds')
            self.time_results[algorithm] = elapsed_time
            self.resume_solving()  # <-- GỌI TỰ ĐỘNG CHẠY TIẾP


    def stop_solving(self):
        self.is_solving = False
        self.pause_event.set()
        self.pause_button.config(text='Pause')

    def resume_solving(self):
        if not self.steps:
            return
        self.is_solving = True
        self.pause_event.set()
        self.root.after(0, self.play_from_current)

    def play_from_current(self):
        if self.current_step_index < len(self.steps):
            self.pause_event.wait()
            if not self.is_solving:
                return
            step = self.steps[self.current_step_index]
            self.update_board(step)
            self.steps_display.insert(tk.END, f'Step {self.current_step_index + 1}: {step}\n')
            self.steps_display.see(tk.END)
            self.current_step_index += 1
            self.root.after(int(self.speed.get() * 1000), self.play_from_current)

    def next_step(self):
        if self.current_step_index < len(self.steps):
            step = self.steps[self.current_step_index]
            self.update_board(step)
            self.steps_display.insert(tk.END, f'Step {self.current_step_index + 1}: {step}\n')
            self.steps_display.see(tk.END)
            self.current_step_index += 1

    def previous_step(self):
        if self.current_step_index > 1:
            self.current_step_index -= 2
            self.steps_display.delete('1.0', tk.END)
            step = self.steps[self.current_step_index]
            self.update_board(step)
            self.steps_display.insert(tk.END, f'Step {self.current_step_index + 1}: {step}\n')
            self.current_step_index += 1

    def reset_board(self):
        self.is_solving = False
        self.pause_event.set()
        self.pause_button.config(text='Pause')
        self.steps = []
        self.current_step_index = 0

        self.clear_frame(self.initial_frame)
        self.clear_frame(self.goal_frame)
        self.draw_static_board(self.initial_frame, INITIAL_STATE)
        self.draw_static_board(self.goal_frame, GOAL_STATE)
        self.update_board(INITIAL_STATE)

        self.steps_display.delete('1.0', tk.END)
        self.time_display.config(text='0.0000 seconds')
        self.step_label.config(text='Step 0 of 0')

    def export_steps(self):
        steps_text = self.steps_display.get("1.0", tk.END).strip()
        if not steps_text:
            messagebox.showinfo('Info', 'No steps to export!')
            return
        with open("steps_output.txt", "w", encoding="utf-8") as file:
            file.write(steps_text)
        messagebox.showinfo('Success', 'Steps exported to steps_output.txt')

def main():
    root = tk.Tk()
    app = PuzzleApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
