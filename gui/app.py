import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import random
from algorithms.search import bfs, dfs, ucs, ids, greedy, astar, ida_star, simple_hill_climbing, steepest_ascent_hill_climbing, stochastic_hill_climbing, simulated_annealing, beam_search, and_or_search, genetic_algorithm
from gui.belief_runner import test_beliefs, GOAL_STATE

# Thay đổi trạng thái đầu vào thành trạng thái có thể giải được
INITIAL_STATE = ((1, 2, 3),  
                 (4, 5, 6),  
                 (0, 7, 8))

# Các trạng thái niềm tin
BELIEF_STATES = [
    ((1, 2, 3), (4, 5, 6), (0, 7, 8)),
    ((1, 2, 3), (4, 5, 6), (7, 0, 8)),
    ((1, 2, 3), (4, 0, 6), (7, 5, 8)),
]

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
        self.mode_var = tk.StringVar(value='Normal')
        self.mode_var.trace_add('write', self.on_mode_change)
        
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
        self.puzzle_state = INITIAL_STATE
        self.current_initial_state = INITIAL_STATE  # Thêm biến để lưu trạng thái ban đầu hiện tại


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
            "And-Or Search": and_or_search,
            "Genetic Algorithm": genetic_algorithm
        }

        self.create_widgets() 
        self.reset_board()   


    def configure_styles(self):
        self.style.configure('TFrame', background='#F5F7FA')
        self.style.configure('Header.TLabel', background='#F5F7FA', foreground='#3498DB', font=('Helvetica', 24, 'bold'), padding=20)
        self.style.configure('Title.TLabel', font=('Helvetica', 14, 'bold'), background='#F5F7FA', foreground='#2C3E50')
        self.style.configure('Board.TFrame', background='#FFFFFF', relief='solid', borderwidth=2)
        self.style.configure('Tile.TLabel', font=('Helvetica', 24, 'bold'), background='#4A90E2', foreground='white', width=3, padding=15, relief='raised', borderwidth=1)
        self.style.configure('Empty.TLabel', background='#DDE6ED', relief='sunken', width=4, padding=20, borderwidth=1)
        self.style.configure('TRadiobutton', font=('Helvetica', 11), background='#F5F7FA', foreground='#2C3E50')
        self.style.configure('TButton', font=('Helvetica', 12, 'bold'), padding=8)
        self.style.map('TButton', foreground=[('active', 'white'), ('!active', 'white')], background=[('active', '#2980B9'), ('!active', '#3498DB')])
        self.style.configure('Time.TLabel', font=('Helvetica', 13, 'bold'), foreground='#2980B9', background='#F5F7FA')
        self.style.configure('TScale', troughcolor='#cce5ff', background='#3498DB')

    def create_widgets(self):
        # Tự động fit kích thước màn hình
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.9)
        window_height = int(screen_height * 0.9)
        self.root.geometry(f"{window_width}x{window_height}")

        header = ttk.Frame(self.root)
        header.pack(fill=tk.X, pady=(10, 0))
        ttk.Label(header, text='8-Puzzle Solver', style='Header.TLabel').pack(anchor='center')

        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        main_container.columnconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=3)
        main_container.columnconfigure(2, weight=1)

        panel_width = 250

        # Left Panel
        left_panel = ttk.Frame(main_container, width=panel_width)
        left_panel.grid(row=0, column=0, sticky='nsew')
        left_panel.grid_propagate(False)

        ttk.Label(left_panel, text='Chọn thuật toán:', style='Title.TLabel').pack(anchor=tk.W, padx=10, pady=(10, 5))

        # Scrollable Algorithm Selection
        algo_border = ttk.Frame(left_panel, height=200)
        algo_border.pack(padx=10, pady=(0, 10), fill="both")
        algo_border.pack_propagate(False)

        algo_canvas = tk.Canvas(algo_border, background="#FFFFFF", bd=0, highlightthickness=1, relief="solid")
        algo_scrollbar = ttk.Scrollbar(algo_border, orient="vertical", command=algo_canvas.yview)
        algo_scrollbar.pack(side="right", fill="y")
        algo_canvas.pack(side="left", fill="both", expand=True)
        algo_canvas.configure(yscrollcommand=algo_scrollbar.set)

        algo_inner_frame = ttk.Frame(algo_canvas)
        canvas_window = algo_canvas.create_window((0, 0), window=algo_inner_frame, anchor="nw")

        def on_configure(event):
            algo_canvas.configure(scrollregion=algo_canvas.bbox("all"))

        algo_inner_frame.bind("<Configure>", on_configure)
        algo_canvas.bind_all("<MouseWheel>", lambda e: algo_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        for algo in self.algorithms:
            ttk.Radiobutton(algo_inner_frame, text=algo, variable=self.algorithm_var, value=algo).pack(anchor=tk.W, pady=2, padx=5)

        # Mode selection
        ttk.Label(left_panel, text='Chế độ chạy:', style='Title.TLabel').pack(anchor=tk.W, padx=10, pady=(10, 0))
        ttk.Radiobutton(left_panel, text='Bình thường', variable=self.mode_var, value='Normal').pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(left_panel, text='Niềm tin', variable=self.mode_var, value='Belief').pack(anchor=tk.W, padx=20)


        # Control Buttons
        for text, cmd in [
            ('Solve Puzzle', self.start_solving),
            ('Tạo trạng thái ngẫu nhiên', self.set_random_state),
            ('Reset Board', self.reset_board),
            ('Export Solution', self.export_steps)
        ]:
            ttk.Button(left_panel, text=text, command=cmd).pack(fill=tk.X, padx=10, pady=4)

        # Speed control
        ttk.Label(left_panel, text="Speed (s/step):", font=("Arial", 15, "bold")).pack(pady=(20, 5))
        self.speed_value_label = ttk.Label(left_panel, text=f"{self.speed.get():.1f} s/step")
        self.speed_value_label.pack(pady=(0, 5))
        self.speed_scale = ttk.Scale(
            left_panel,
            from_=0.1, to=2.0, orient=tk.HORIZONTAL,
            variable=self.speed,
            length=panel_width - 40,
            style="TScale",
            command=lambda val: self.speed_value_label.config(text=f"{float(val):.1f} s/step")
        )
        self.speed_scale.pack(pady=(0, 10))

        # Right Panel
        right_panel = ttk.Frame(main_container, width=panel_width)
        right_panel.grid(row=0, column=2, sticky='nsew')
        right_panel.grid_propagate(False)
        # Time display
        ttk.Label(right_panel, text='Time elapsed:', style='Title.TLabel').pack(anchor=tk.W, padx=10, pady=(5, 0))
        self.time_display = ttk.Label(right_panel, text='0.0000 seconds', style='Time.TLabel')
        self.time_display.pack(anchor=tk.W, padx=10, pady=(0, 10))


        ttk.Label(right_panel, text='Các bước đi:', style='Title.TLabel').pack(anchor=tk.W, padx=10, pady=(0, 5))

        self.steps_frame = ttk.Frame(right_panel, height=200)
        self.steps_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.steps_frame.pack_propagate(False)

        self.steps_scroll = ttk.Scrollbar(self.steps_frame)
        self.steps_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.steps_display = tk.Text(
            self.steps_frame, height=10, width=30, font=('Consolas', 11),
            wrap=tk.WORD, yscrollcommand=self.steps_scroll.set,
            bg='#FFFFFF', fg='#2C3E50'
        )
        self.steps_display.pack(fill=tk.BOTH, expand=True)
        self.steps_scroll.config(command=self.steps_display.yview)

        for text, command in [
            ('← Bước trước', self.previous_step),
            ('→ Bước sau', self.next_step),
            ('⏹ Dừng', self.stop_solving),
            ('▶ Tiếp tục', self.resume_solving)
        ]:
            ttk.Button(right_panel, text=text, command=command, style='TButton').pack(fill=tk.X, padx=10, pady=3)

        # Middle Panel
        middle_panel = ttk.Frame(main_container)
        middle_panel.grid(row=0, column=1, sticky='nsew')

        # Frame cho chế độ bình thường
        self.normal_board_frame = ttk.Frame(middle_panel)
        self.normal_board_frame.pack(pady=10)

        state_label_frame = ttk.Frame(self.normal_board_frame)
        state_label_frame.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        ttk.Label(state_label_frame, text='Initial State', style='Title.TLabel').grid(row=0, column=0, padx=15)
        ttk.Label(state_label_frame, text='Goal State', style='Title.TLabel').grid(row=0, column=1, padx=15)

        self.initial_frame = ttk.Frame(self.normal_board_frame)
        self.initial_frame.grid(row=1, column=0, padx=15)
        self.goal_frame = ttk.Frame(self.normal_board_frame)
        self.goal_frame.grid(row=1, column=1, padx=15)

        current_frame = ttk.Frame(self.normal_board_frame)
        current_frame.grid(row=2, column=0, columnspan=2, pady=(30, 0))
        ttk.Label(current_frame, text='Current State', style='Title.TLabel').pack(pady=5)
        self.step_label = ttk.Label(current_frame, text='Step 0 of 0', style='Title.TLabel')
        self.step_label.pack()
        self.board_container = ttk.Frame(current_frame)
        self.board_container.pack()

        for i in range(3):
            row = []
            for j in range(3):
                label = ttk.Label(self.board_container, style='Tile.TLabel', anchor='center')
                label.grid(row=i, column=j, padx=2, pady=2)
                row.append(label)
            self.tiles.append(row)

        # Frame cho chế độ niềm tin
        self.belief_board_frame = ttk.Frame(middle_panel)
        
        # Container cho 3 trạng thái init
        init_states_frame = ttk.Frame(self.belief_board_frame)
        init_states_frame.pack(pady=10)
        ttk.Label(init_states_frame, text='Initial States', style='Title.TLabel').pack(pady=5)
        
        self.belief_init_frames = []
        init_container = ttk.Frame(init_states_frame)
        init_container.pack()
        for i in range(3):
            frame = ttk.Frame(init_container)
            frame.grid(row=0, column=i, padx=10)
            ttk.Label(frame, text=f'State {i+1}', style='Title.TLabel').pack(pady=2)
            board_frame = ttk.Frame(frame)
            board_frame.pack()
            self.belief_init_frames.append(board_frame)

        # Container cho goal state và current state
        bottom_states_frame = ttk.Frame(self.belief_board_frame)
        bottom_states_frame.pack(pady=10)
        
        # Goal state (bên trái)
        goal_frame = ttk.Frame(bottom_states_frame)
        goal_frame.grid(row=0, column=0, padx=20)
        ttk.Label(goal_frame, text='Goal State', style='Title.TLabel').pack(pady=5)
        self.belief_goal_frame = ttk.Frame(goal_frame)
        self.belief_goal_frame.pack()

        # Current state (bên phải)
        current_frame = ttk.Frame(bottom_states_frame)
        current_frame.grid(row=0, column=1, padx=20)
        ttk.Label(current_frame, text='Current State', style='Title.TLabel').pack(pady=5)
        self.belief_step_label = ttk.Label(current_frame, text='Step 0 of 0', style='Title.TLabel')
        self.belief_step_label.pack()
        self.belief_current_frame = ttk.Frame(current_frame)
        self.belief_current_frame.pack()

        # Ẩn frame belief mode ban đầu vì mode mặc định là Normal
        self.belief_board_frame.pack_forget()

    def update_board(self, state):
        for i in range(3):
            for j in range(3):
                value = state[i][j]
                label = self.tiles[i][j]
                if value == 0:
                    label.config(text='', style='Empty.TLabel')
                else:
                    label.config(text=str(value), style='Tile.TLabel')
        
        # Cập nhật cả hai step label
        step_text = f"Step {self.current_step_index + 1} of {len(self.steps)}"
        self.step_label.config(text=step_text)
        self.belief_step_label.config(text=step_text)
        
        # Cập nhật current state trong belief mode
        if self.mode_var.get() == 'Belief':
            self.clear_frame(self.belief_current_frame)
            self.draw_static_board(self.belief_current_frame, state)

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
            
        # Reset về trạng thái ban đầu hiện tại
        self.puzzle_state = self.current_initial_state
        self.update_puzzle_display()
        
        # Reset các biến liên quan đến việc giải
        self.steps = []
        self.current_step_index = 0
        self.steps_display.delete('1.0', tk.END)
        self.time_display.config(text='0.0000 seconds')
        self.step_label.config(text='Step 0 of 0')
        
        self.is_solving = True
        self.pause_event.set()
        threading.Thread(target=self.solve, daemon=True).start()

    def toggle_pause(self):
        if self.pause_event.is_set():
            self.pause_event.clear()
        else:
            self.pause_event.set()

    def is_valid(self, state):
        flat = [num for row in state for num in row]
        return sorted(flat) == list(range(9))
    
    def is_solvable(self, state):
        # Chuyển đổi trạng thái thành mảng một chiều
        flat_state = [item for sublist in state for item in sublist]
        inversions = 0
        for i in range(len(flat_state)):
            if flat_state[i] == 0:
                continue
            for j in range(i + 1, len(flat_state)):
                if flat_state[j] == 0:
                    continue
                if flat_state[i] > flat_state[j]:
                    inversions += 1
        return inversions % 2 == 0

    def get_inversion_count(self, state):
        flat = [num for row in state for num in row if num != 0]
        inversions = sum(1 for i in range(len(flat)) for j in range(i + 1, len(flat)) if flat[i] > flat[j])
        return inversions
    
    def check_state_solvability(self):
        state = self.get_puzzle_state()
        if not state:
            messagebox.showerror("Lỗi", "Không có trạng thái đầu vào.")
            return
        
        if not self.is_valid(state):
            messagebox.showerror("Lỗi", "Trạng thái đầu vào không hợp lệ.")
            return
        
        inversions = self.get_inversion_count(state)
        is_solvable = self.is_solvable(state)
        
        message = f"Trạng thái: {state}\n"
        message += f"Số nghịch đảo: {inversions}\n"
        message += f"Trạng thái {'có thể giải được' if is_solvable else 'không thể giải được'}"
        
        messagebox.showinfo("Kiểm tra tính giải được", message)

    def solve(self):
        algorithm = self.algorithm_var.get()
        algorithm_function = self.algorithms.get(algorithm)

        if not algorithm_function:
            messagebox.showerror('Error', f'Algorithm "{algorithm}" not found')
            self.is_solving = False
            return

        self.start_time = time.time()

        if self.mode_var.get() == 'Belief':
            result = test_beliefs(BELIEF_STATES, GOAL_STATE, algorithm_function)
        else:
            initial_state = self.get_puzzle_state()

            if not initial_state or not self.is_valid(initial_state):
                messagebox.showerror("Lỗi", "Trạng thái đầu vào không hợp lệ.")
                self.is_solving = False
                return

            if not self.is_solvable(initial_state):
                messagebox.showerror("Lỗi", "Trạng thái đầu vào không giải được. Số nghịch đảo phải là số chẵn.")
                self.is_solving = False
                return

            print(f"Đang giải trạng thái: {initial_state}")
            result = algorithm_function(initial_state, GOAL_STATE)

        elapsed_time = time.time() - self.start_time
        self.time_display.config(text=f'{elapsed_time:.4f} seconds')

        if result is None:
            messagebox.showinfo('Info', 'Không tìm thấy lời giải')
            self.is_solving = False
        else:
            self.steps = result
            self.current_step_index = 0
            self.steps_display.delete('1.0', tk.END)
            self.resume_solving()

        print("Chế độ:", self.mode_var.get())
        print("Trạng thái đầu vào:", self.get_puzzle_state())



    def get_puzzle_state(self):
        # Giả sử bạn lưu trạng thái của puzzle trong một thuộc tính `self.puzzle_state`
        return self.puzzle_state
    

    def stop_solving(self):
        self.is_solving = False
        self.pause_event.set()

    def resume_solving(self):
        if not self.steps:
            return
        self.is_solving = True
        self.pause_event.set()
        self.root.after(0, self.play_from_current)
    
    def get_speed_delay(self):
        return int(self.speed.get() * 1000)


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
        self.steps = []
        self.current_step_index = 0
        self.move_count = 0

        # Reset về trạng thái ban đầu hiện tại
        self.puzzle_state = self.current_initial_state
        
        # Cập nhật giao diện
        self.clear_frame(self.initial_frame)
        self.clear_frame(self.goal_frame)
        self.draw_static_board(self.initial_frame, self.current_initial_state)
        self.draw_static_board(self.goal_frame, GOAL_STATE)
        self.update_board(self.current_initial_state)

        # Reset các hiển thị
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

    def generate_solvable_state(self):
        # Tạo trạng thái ngẫu nhiên
        numbers = list(range(9))
        random.shuffle(numbers)
        state = tuple(tuple(numbers[i:i+3]) for i in range(0, 9, 3))
        # Kiểm tra tính giải được
        if self.is_solvable(state):
            return state
        else:
            # Nếu không giải được, thử lại
            return self.generate_solvable_state()

    def set_random_state(self):
        self.current_initial_state = self.generate_solvable_state()  # Lưu trạng thái ngẫu nhiên mới
        self.puzzle_state = self.current_initial_state  # Cập nhật trạng thái hiện tại
        self.update_puzzle_display()
        self.move_count = 0
        self.update_move_counter()
        messagebox.showinfo("Thông báo", f"Đã tạo trạng thái ngẫu nhiên mới: {self.current_initial_state}")

    def update_puzzle_display(self):
        self.clear_frame(self.initial_frame)
        self.clear_frame(self.goal_frame)
        self.draw_static_board(self.initial_frame, self.puzzle_state)
        self.draw_static_board(self.goal_frame, GOAL_STATE)
        self.update_board(self.puzzle_state)

    def update_move_counter(self):
        self.step_label.config(text=f'Step {self.move_count} of {len(self.steps)}')

    def on_mode_change(self, *args):
        if self.mode_var.get() == 'Belief':
            self.normal_board_frame.pack_forget()
            self.belief_board_frame.pack(pady=10)
            # Cập nhật hiển thị cho belief mode
            for i, state in enumerate(BELIEF_STATES):
                self.clear_frame(self.belief_init_frames[i])
                self.draw_static_board(self.belief_init_frames[i], state)
            self.clear_frame(self.belief_goal_frame)
            self.draw_static_board(self.belief_goal_frame, GOAL_STATE)
            self.clear_frame(self.belief_current_frame)
            self.draw_static_board(self.belief_current_frame, self.puzzle_state)
        else:
            self.belief_board_frame.pack_forget()
            self.normal_board_frame.pack(pady=10)


def main():
    root = tk.Tk()
    app = PuzzleApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
