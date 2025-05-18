import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import random
from algorithms.puzzle_solver import *
from gui.runner_dispatcher import get_runner
from algorithms.search_in_complex_envi.partially import partially_observable_search

# Các hằng số
GOAL_STATE = ((1, 2, 3), (4, 5, 6), (7, 8, 0))
INITIAL_STATE = ((1, 2, 3), (4, 5, 6), (0, 7, 8))
BELIEF_STATES = [
    ((1, 2, 3), (4, 5, 6), (0, 7, 8)),  # State 1
    ((1, 2, 3), (5, 6, 7), (4, 0, 8)),  # State 2
    ((1, 2, 3), (5, 6, 8), (0, 4, 7))   # State 3
]
BELIEF_GOAL_STATES = [
    ((1, 2, 3), (4, 5, 6), (7, 8, 0)),  # Goal 1
    ((1, 2, 3), (5, 6, 7), (8, 0, 4)),  # Goal 2
    ((1, 2, 3), (5, 6, 8), (0, 4, 7))   # Goal 3
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
        self.algorithm_var.trace_add('write', self.on_algorithm_change)
        
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
        self.current_initial_state = INITIAL_STATE
        self.root.state('zoomed')

        self.algorithms = {
            "BFS": bfs,
            "DFS": dfs,
            "UCS": ucs,
            "IDS": ids,
            "Greedy": greedy,
            "A*": astar, 
            "IDA*": ida_star,
            "Simple Hill Climbing": simple_hill_climbing,
            "Steepest Ascent Hill Climbing": steepest_ascent,
            "Stochastic Hill Climbing": stochastic_hill,
            "Simulated Annealing": simulated_annealing,
            "Beam Search": beam_search,
            "Genetic Algorithm": genetic_algorithm,
            "And-Or Search": and_or_search,
            "Partially Observable Search": partially_observable_search,
            "Backtracking": Backtracking,
            "AC3": AC3,
            "Forward Checking": ForwardChecking,
            "Q-Learning": q_learning_step
        }

        self.partial_observation = ((1, 2, 3), (-1, -1, -1), (-1, -1, -1))
        self.selected_initial_states = BELIEF_STATES
        self.selected_goal_states = BELIEF_GOAL_STATES
        self.belief_current_states = list(BELIEF_STATES)

        self.create_widgets()
        self.on_mode_change()
        self.on_algorithm_change()

    def configure_styles(self):
        self.style.configure('TFrame', background='#F5F7FA')
        self.style.configure('Header.TLabel', background='#F5F7FA', foreground='#3498DB', font=('Helvetica', 24, 'bold'), padding=20)
        self.style.configure('Title.TLabel', font=('Helvetica', 14, 'bold'), background='#F5F7FA', foreground='#2C3E50')
        self.style.configure('Board.TFrame', background='#FFFFFF', relief='solid', borderwidth=2)
        self.style.configure('Tile.TLabel', font=('Helvetica', 24, 'bold'), background='#4A90E2', foreground='white', anchor='center', width=4, padding=15, relief='raised', borderwidth=1)
        self.style.configure('Empty.TLabel', background='#DDE6ED', relief='sunken', width=4, padding=15, borderwidth=1)
        self.style.configure('TRadiobutton', font=('Helvetica', 11), background='#F5F7FA', foreground='#2C3E50')
        self.style.configure('TButton', font=('Helvetica', 12, 'bold'), padding=8)
        self.style.map('TButton', foreground=[('active', 'white'), ('!active', 'white')], background=[('active', '#2980B9'), ('!active', '#3498DB')])
        self.style.configure('Time.TLabel', font=('Helvetica', 13, 'bold'), foreground='#2980B9', background='#F5F7FA')
        self.style.configure('TScale', troughcolor='#cce5ff', background='#3498DB')

    def create_widgets(self):
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1, uniform="group1")
        main_container.grid_columnconfigure(1, weight=2, uniform="group1")
        main_container.grid_columnconfigure(2, weight=1, uniform="group1")

        panel_width = 320
        # Left Panel
        left_panel = ttk.Frame(main_container, width=panel_width)
        left_panel.grid(row=0, column=0, sticky='nsew')
        left_panel.grid_propagate(False)

        # --- Thuật toán với scroll ---
        algo_group = ttk.LabelFrame(left_panel, text='Chọn thuật toán:', padding=5)
        algo_group.pack(fill='x', padx=10, pady=(10, 5))
        algo_canvas = tk.Canvas(algo_group, height=220, borderwidth=0, highlightthickness=0)
        algo_scrollbar = ttk.Scrollbar(algo_group, orient="vertical", command=algo_canvas.yview)
        algo_inner_frame = ttk.Frame(algo_canvas)
        algo_inner_frame.bind(
            "<Configure>", lambda e: algo_canvas.configure(scrollregion=algo_canvas.bbox("all"))
        )
        algo_canvas.create_window((0, 0), window=algo_inner_frame, anchor="nw")
        algo_canvas.configure(yscrollcommand=algo_scrollbar.set)
        # Gắn scroll bằng chuột
        def _on_mousewheel(event):
            algo_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        algo_canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows
        algo_canvas.bind_all("<Button-4>", lambda e: algo_canvas.yview_scroll(-1, "units"))  # Linux scroll up
        algo_canvas.bind_all("<Button-5>", lambda e: algo_canvas.yview_scroll(1, "units"))   # Linux scroll down

        algo_canvas.pack(side="left", fill="both", expand=True)
        algo_scrollbar.pack(side="right", fill="y")
        print("Registered algorithms:", list(self.algorithms.keys()))  # Debug
        for algo in self.algorithms:
            ttk.Radiobutton(algo_inner_frame, text=algo, variable=self.algorithm_var, value=algo).pack(anchor=tk.W, pady=2, padx=5)
        # --- Các nút điều khiển ---
        ttk.Label(left_panel, text='Chế độ chạy:', style='Title.TLabel').pack(anchor=tk.W, padx=10, pady=(10, 0))
        ttk.Radiobutton(left_panel, text='Bình thường', variable=self.mode_var, value='Normal').pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(left_panel, text='Niềm tin', variable=self.mode_var, value='Belief').pack(anchor=tk.W, padx=20)

        ttk.Label(left_panel, text="Speed (s/step):", font=("Arial", 15, "bold")).pack(pady=(20, 5))
        self.speed_value_label = ttk.Label(left_panel, text=f"{self.speed.get():.2f} s/step")
        self.speed_value_label.pack(pady=(0, 5))
        self.speed_scale = ttk.Scale(
            left_panel,
            from_=0.01, to=1.0, orient=tk.HORIZONTAL,
            variable=self.speed,
            length=panel_width - 40,
            style="TScale",
            command=lambda val: self.speed_value_label.config(text=f"{float(val):.2f} s/step")
        )
        self.speed_scale.pack(pady=(0, 10))
        
        # Frame chứa nút nhập và lưu
        self.init_buttons_frame = ttk.Frame(left_panel)
        self.init_buttons_frame.pack(fill='x', padx=10, pady=(10, 0))

        self.init_edit_btn = ttk.Button(self.init_buttons_frame, text="Nhập init state", command=self.show_init_entry)
        self.init_edit_btn.pack(fill='x', pady=(0, 4))

        self.init_save_btn = ttk.Button(self.init_buttons_frame, text="Lưu init state", command=self.save_init_entry)
        self.init_save_btn.pack(fill='x')

        # Các nút chỉ hiển thị khi ở chế độ bình thường
        if self.mode_var.get() == 'Belief':
            self.init_buttons_frame.pack_forget()

        for text, cmd in [
            ('Solve Puzzle', self.start_solving),
            ('Tạo trạng thái ngẫu nhiên', self.set_random_state),
            ('Reset Board', self.reset_board),
            ('Export Solution', self.export_steps)
        ]:
            ttk.Button(left_panel, text=text, command=cmd).pack(fill=tk.X, padx=10, pady=4)

        # Right Panel
        right_panel = ttk.Frame(main_container, width=panel_width)
        right_panel.grid(row=0, column=2, sticky='nsew')
        right_panel.grid_propagate(False)
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
        # Initial State nhập tay
        self.initial_frame = ttk.Frame(self.normal_board_frame)
        self.initial_frame.grid(row=1, column=0, padx=15)
        self.init_entry_mode = False
        self.init_entries = []  # Lưu các Entry khi nhập
        self.init_save_btn = ttk.Button(self.normal_board_frame, text="Lưu", command=self.save_init_entry)
        # Goal State giữ nguyên
        self.goal_frame = ttk.Frame(self.normal_board_frame)
        self.goal_frame.grid(row=1, column=1, padx=15)
        current_frame = ttk.Frame(self.normal_board_frame)
        current_frame.grid(row=2, column=0, columnspan=2, pady=(30, 0))
        ttk.Label(current_frame, text='Current State', style='Title.TLabel').pack(pady=5)
        self.step_label = ttk.Label(current_frame, text='Step 0 of 0', style='Title.TLabel')
        self.step_label.pack()
        self.board_container = ttk.Frame(current_frame)
        self.board_container.pack()
        # Frame cho chế độ niềm tin hoặc Partially Observable
        self.belief_board_frame = ttk.Frame(middle_panel)

        # --- Partial Observation group ---
        self.partial_obs_group = ttk.LabelFrame(self.belief_board_frame, text='Partial Observation', padding=10)
        self.partial_obs_frame = ttk.Frame(self.partial_obs_group)
        self.partial_obs_frame.pack()

        # --- Initial States group ---
        init_group = ttk.LabelFrame(self.belief_board_frame, text='Initial States', padding=10)
        self.partial_obs_group.pack(pady=5, fill='x')
        init_group.pack(pady=5, fill='x')
        self.belief_init_frames = []
        init_container = ttk.Frame(init_group)
        init_container.pack()
        for i in range(3):
            frame = ttk.Frame(init_container)
            frame.grid(row=0, column=i, padx=10)
            ttk.Label(frame, text=f'State {i+1}', style='Title.TLabel').pack(pady=2)
            board_frame = ttk.Frame(frame)
            board_frame.pack()
            self.belief_init_frames.append(board_frame)

        # --- Goal States group ---
        goal_group = ttk.LabelFrame(self.belief_board_frame, text='Goal States', padding=10)
        goal_group.pack(pady=5, fill='x')
        self.belief_goal_frames = []
        goal_container = ttk.Frame(goal_group)
        goal_container.pack()
        for i in range(3):
            frame = ttk.Frame(goal_container)
            frame.grid(row=0, column=i, padx=10)
            ttk.Label(frame, text=f'Goal {i+1}', style='Title.TLabel').pack(pady=2)
            board_frame = ttk.Frame(frame)
            board_frame.pack()
            self.belief_goal_frames.append(board_frame)

        # --- Current States group ---
        current_group = ttk.LabelFrame(self.belief_board_frame, text='Current States', padding=10)
        current_group.pack(pady=5, fill='x')
        self.belief_current_frames = []
        current_container = ttk.Frame(current_group)
        current_container.pack()
        for i in range(3):
            frame = ttk.Frame(current_container)
            frame.grid(row=0, column=i, padx=10)
            ttk.Label(frame, text=f'Current {i+1}', style='Title.TLabel').pack(pady=2)
            board_frame = ttk.Frame(frame)
            board_frame.pack()
            self.belief_current_frames.append(board_frame)

        self.belief_board_frame.pack_forget()

    def update_board(self, state):
        self.clear_frame(self.board_container)
        self.draw_static_board(self.board_container, state, size=90)
        step_text = f"Step {self.current_step_index + 1} of {len(self.steps)}"
        self.step_label.config(text=step_text)
        if self.mode_var.get() == 'Belief':
            size = 35 if self.algorithm_var.get() == "Partially Observable Search" else 45
            for i in range(3):
                self.clear_frame(self.belief_current_frames[i])
                if isinstance(state, list) and i < len(state) and state[i] is not None:
                    self.belief_current_states[i] = state[i]
                self.draw_static_board(self.belief_current_frames[i], self.belief_current_states[i], size=size)

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def draw_static_board(self, frame, state, size=90):
        for widget in frame.winfo_children():
            widget.destroy()
        board_frame = ttk.Frame(frame, style='Board.TFrame')
        board_frame.pack(padx=5, pady=5, expand=True, fill='both')
        for r, row in enumerate(state):
            for c, value in enumerate(row):
                style = {
                    'bg': '#4A90E2', 'fg': 'white', 'relief': 'raised', 'bd': 2} if value != 0 and value != -1 else \
                    {'bg': '#DDE6ED', 'fg': '#4A90E2', 'relief': 'sunken', 'bd': 2} if value == 0 else \
                    {'bg': '#A9A9A9', 'fg': 'black', 'relief': 'flat', 'bd': 1}
                text = '' if value == 0 else '?' if value == -1 else str(value)
                tile = tk.Label(
                    board_frame, text=text,
                    font=('Helvetica', 14, 'bold') if size < 60 else ('Helvetica', 18, 'bold') if size < 80 else ('Helvetica', 24, 'bold'),
                    width=3, height=1,
                    **style
                )
                tile.grid(row=r, column=c, sticky='nsew', padx=2, pady=2)
            board_frame.grid_rowconfigure(r, weight=1, minsize=size)
        for c in range(3):
            board_frame.grid_columnconfigure(c, weight=1, minsize=size)

    def start_solving(self):
        if self.is_solving:
            return

        self.steps = []
        self.current_step_index = 0
        self.steps_display.delete('1.0', tk.END)
        self.time_display.config(text='0.0000 seconds')
        self.step_label.config(text='Step 0 of 0')
        self.is_solving = True
        self.pause_event.set()

        if self.mode_var.get() == 'Belief':
            self.belief_current_states = list(self.selected_initial_states)
            size = 35 if self.algorithm_var.get() == "Partially Observable Search" else 50
            for i in range(3):
                self.clear_frame(self.belief_current_frames[i])
                self.draw_static_board(self.belief_current_frames[i], self.belief_current_states[i], size=size)
        else:
            self.puzzle_state = self.current_initial_state
            self.update_board(self.current_initial_state)

        threading.Thread(target=self.solve, daemon=True).start()

    def solve(self):
        algorithm = self.algorithm_var.get()
        print(f"Selected algorithm: {algorithm}")
        algorithm_function = self.algorithms.get(algorithm)

        self.steps = []
        self.current_step_index = 0
        self.steps_display.delete('1.0', tk.END)
        self.time_display.config(text='0.0000 seconds')
        self.step_label.config(text='Step 0 of 0')
        self.is_solving = True
        self.pause_event.set()
        self.start_time = time.time()

        # Trường hợp thuật toán không tồn tại
        if algorithm_function is None:
            messagebox.showerror('Error', f'Algorithm "{algorithm}" not found')
            self.is_solving = False
            return

        # Trường hợp Backtracking chế độ bình thường
        if algorithm == "Backtracking" and self.mode_var.get() == "Normal":
            def update_gui(state, step_index, detail):
                self.puzzle_state = state
                self.update_board(state)
                self.step_label.config(text=f"Step {step_index}")
                self.steps_display.insert(tk.END, f"Step {step_index}: {state}\n")
                self.steps_display.insert(tk.END, f"→ {detail}\n")
                self.steps_display.see(tk.END)


            runner = Backtracking(update_callback=update_gui, delay=self.speed.get())
            success_steps = runner.run(self.current_initial_state, GOAL_STATE)


            elapsed_time = time.time() - self.start_time
            self.time_display.config(text=f'{elapsed_time:.4f} seconds')

            if not success_steps or success_steps[-1] != GOAL_STATE:
                messagebox.showinfo("Kết quả", "Không tìm được trạng thái goal.")
                self.is_solving = False
                self.reset_board()
                return

            self.steps = success_steps
            self.current_step_index = 0
            self.root.after(0, self.resume_solving)
            return

        # Trường hợp AC3 chế độ bình thường
        if algorithm == "AC3" and self.mode_var.get() == "Normal":
            def update_gui(info, step_index, detail):
                # info là tuple (label, nội dung)
                label, content = info
                self.steps_display.insert(tk.END, f"Step {step_index}: {label}\n")
                self.steps_display.insert(tk.END, f"→ {content}\n")
                self.steps_display.insert(tk.END, f"→ {detail}\n")
                self.steps_display.see(tk.END)

            runner = AC3(update_callback=update_gui, get_delay=self.speed.get)
            result = runner.run(self.current_initial_state, GOAL_STATE)

            elapsed_time = time.time() - self.start_time
            self.time_display.config(text=f'{elapsed_time:.4f} seconds')

            if result is None:
                messagebox.showinfo("Kết quả", "AC3 không tìm được lời giải.")
                self.is_solving = False
                self.reset_board()
                return

            self.steps_display.insert(tk.END, f"Kết quả AC3: {result}\n")
            self.steps_display.see(tk.END)
            self.is_solving = False
            return

        if algorithm == "Forward Checking" and self.mode_var.get() == "Normal":
            def update_gui(info, step_index, detail):
                label, content = info
                self.steps_display.insert(tk.END, f"Step {step_index}: {label}\n")
                self.steps_display.insert(tk.END, f"→ {content}\n")
                self.steps_display.insert(tk.END, f"→ {detail}\n")
                self.steps_display.see(tk.END)

            runner = ForwardChecking(update_callback=update_gui, get_delay=self.speed.get)
            result = runner.run(self.current_initial_state, GOAL_STATE)

            elapsed_time = time.time() - self.start_time
            self.time_display.config(text=f'{elapsed_time:.4f} seconds')

            if result is None:
                messagebox.showinfo("Kết quả", "Forward Checking không tìm được lời giải.")
                self.is_solving = False
                self.reset_board()
                return

            self.steps_display.insert(tk.END, f"Kết quả Forward Checking: {result}\n")
            self.steps_display.see(tk.END)
            self.is_solving = False
            return

        # Các thuật toán còn lại
        runner = get_runner(self.mode_var.get(), algorithm_function, algorithm_name=algorithm)

        try:
            if self.mode_var.get() == 'Belief':
                # Với chế độ Belief
                if algorithm == "Partially Observable Search":
                    result = algorithm_function(self.selected_initial_states, self.selected_goal_states)
                    if result is None:
                        raise ValueError("Partially Observable Search failed to find solution")
                    final_belief, path, belief_steps = result
                    self.steps = [(self.selected_initial_states, None)]
                    if final_belief:
                        self.steps.append((final_belief, None))
                    if path:
                        for state in path:
                            self.steps.append((state, None))
                else:
                    result = runner.run(self.selected_initial_states, self.selected_goal_states)
                    if result is None:
                        raise ValueError("Không tìm thấy lời giải")
                    final_belief, path, _ = result
                    self.steps = [(self.selected_initial_states, None)]
                    if path:
                        for state in path:
                            self.steps.append((state, None))

                elapsed_time = time.time() - self.start_time
                self.time_display.config(text=f'{elapsed_time:.4f} seconds')
                self.current_step_index = 0
                self.root.after(0, self.resume_solving)

            else:
                # Với chế độ Normal
                result = runner.run(self.current_initial_state, GOAL_STATE)
                print(f"Runner result: {result}")
                elapsed_time = time.time() - self.start_time
                self.time_display.config(text=f'{elapsed_time:.4f} seconds')

                if not result or len(result) == 0:
                    raise ValueError("Không có kết quả trả về")

                self.steps = result if isinstance(result, list) else [result]
                self.current_step_index = 0
                final_board_state = self.steps[-1]
                if final_board_state != GOAL_STATE:
                    messagebox.showinfo('Info', 'Không tìm thấy lời giải trong chế độ Normal')
                    self.is_solving = False
                    self.reset_board()
                    return

                self.root.after(0, self.resume_solving)

        except Exception as e:
            elapsed_time = time.time() - self.start_time
            self.time_display.config(text=f'{elapsed_time:.4f} seconds')
            if self.mode_var.get() == 'Belief':
                messagebox.showinfo('Info', f'Không tìm thấy lời giải: {str(e)}')
            else:
                messagebox.showinfo('Info', f'Không tìm thấy lời giải trong chế độ Normal: {str(e)}')
            self.is_solving = False
            self.reset_board()


    def play_from_current(self):
        if self.current_step_index < len(self.steps):
            self.pause_event.wait()
            if not self.is_solving:
                return

            current = self.steps[self.current_step_index]

            if self.mode_var.get() == 'Belief':
                # Expect current to be (belief_states, action)
                belief_states, action = current

                if isinstance(belief_states, tuple):
                    belief_states = list(belief_states)

                # Đảm bảo luôn có 3 trạng thái để hiển thị
                while len(belief_states) < 3:
                    belief_states.append(self.selected_initial_states[len(belief_states)])

                self.belief_current_states = list(belief_states)

                for i in range(3):
                    self.clear_frame(self.belief_current_frames[i])
                    self.draw_static_board(self.belief_current_frames[i], self.belief_current_states[i], size=35)

                self.steps_display.insert(tk.END, f"Step {self.current_step_index + 1}:\n")
                for i in range(3):
                    self.steps_display.insert(tk.END, f"Curr {i+1}: {self.belief_current_states[i]}\n")
            else:
                # Normal mode: current là tuple đơn
                state = current[0] if isinstance(current, tuple) and len(current) == 2 else current
                self.update_board(state)
                self.steps_display.insert(tk.END, f"Step {self.current_step_index + 1}: {state}\n")

            self.steps_display.see(tk.END)
            self.current_step_index += 1
            self.root.after(int(self.speed.get() * 1000), self.play_from_current)


    def next_step(self):
        if self.current_step_index < len(self.steps):
            step = self.steps[self.current_step_index]
            state = step[0] if isinstance(step, tuple) else step
            self.update_board(state)
            self.steps_display.insert(tk.END, f'Step {self.current_step_index + 1}: {state}\n')
            self.steps_display.see(tk.END)
            self.current_step_index += 1

    def previous_step(self):
        if self.current_step_index > 1:
            self.current_step_index -= 2
            self.steps_display.delete('1.0', tk.END)
            step = self.steps[self.current_step_index]
            state = step[0] if isinstance(step, tuple) else step
            self.update_board(state)
            self.steps_display.insert(tk.END, f'Step {self.current_step_index + 1}: {state}\n')
            self.current_step_index += 1

    def reset_board(self):
        self.is_solving = False
        self.pause_event.set()
        self.steps = []
        self.current_step_index = 0
        self.move_count = 0
        self.puzzle_state = self.current_initial_state
        self.clear_frame(self.initial_frame)
        self.clear_frame(self.goal_frame)
        self.draw_static_board(self.initial_frame, self.current_initial_state)
        self.draw_static_board(self.goal_frame, GOAL_STATE)
        self.update_board(self.current_initial_state)
        self.steps_display.delete('1.0', tk.END)
        self.time_display.config(text='0.0000 seconds')
        self.step_label.config(text='Step 0 of 0')
        if self.mode_var.get() == 'Belief':
            self.belief_current_states = list(self.selected_initial_states)
            size = 35 if self.algorithm_var.get() == "Partially Observable Search" else 50
            for i in range(3):
                self.clear_frame(self.belief_current_frames[i])
                self.draw_static_board(self.belief_current_frames[i], self.belief_current_states[i], size=size)

    def export_steps(self):
        steps_text = self.steps_display.get("1.0", tk.END).strip()
        if not steps_text:
            messagebox.showinfo('Info', 'No steps to export!')
            return
        with open("steps_output.txt", "w", encoding="utf-8") as file:
            file.write(steps_text)
        messagebox.showinfo('Success', 'Steps exported to steps_output.txt')

    def get_puzzle_state(self):
        return self.puzzle_state

    def is_valid(self, state):
        flat = [num for row in state for num in row]
        return sorted(flat) == list(range(9))

    def is_solvable(self, state):
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

    def set_random_state(self):
        self.current_initial_state = self.generate_solvable_state()
        self.puzzle_state = self.current_initial_state
        self.init_entry_mode = False
        self.update_puzzle_display()
        self.move_count = 0
        messagebox.showinfo("Thông báo", f"Đã tạo trạng thái ngẫu nhiên mới: {self.current_initial_state}")

    def generate_solvable_state(self):
        numbers = list(range(9))
        random.shuffle(numbers)
        state = tuple(tuple(numbers[i:i+3]) for i in range(0, 9, 3))
        if self.is_solvable(state):
            return state
        else:
            return self.generate_solvable_state()

    def update_puzzle_display(self):
        self.clear_frame(self.initial_frame)
        self.clear_frame(self.goal_frame)
        if self.init_entry_mode:
            self.show_init_entry()
        else:
            if self.algorithm_var.get() == "Partially Observable Search":
                states_size = 35
                self.clear_frame(self.partial_obs_frame)
                self.draw_static_board(self.partial_obs_frame, self.partial_observation, size=states_size)
                for idx, state in enumerate(self.selected_initial_states):
                    self.clear_frame(self.belief_init_frames[idx])
                    self.draw_static_board(self.belief_init_frames[idx], state, size=states_size)
                for idx, state in enumerate(self.selected_goal_states):
                    self.clear_frame(self.belief_goal_frames[idx])
                    self.draw_static_board(self.belief_goal_frames[idx], state, size=states_size)
            else:
                self.draw_static_board(self.initial_frame, self.puzzle_state, size=90)

            if self.algorithm_var.get() == "Partially Observable Search":
                states_size = 35
                self.clear_frame(self.partial_obs_frame)
                self.draw_static_board(self.partial_obs_frame, self.partial_observation, size=states_size)
                for idx, state in enumerate(self.selected_goal_states):
                    self.clear_frame(self.belief_goal_frames[idx])
                    self.draw_static_board(self.belief_goal_frames[idx], state, size=states_size)
            else:
                self.draw_static_board(self.goal_frame, GOAL_STATE, size=90)

            self.update_board(self.puzzle_state)

    def on_mode_change(self, *args):
        if self.mode_var.get() == 'Belief':
            self.normal_board_frame.pack_forget()
            self.belief_board_frame.pack(fill=tk.BOTH, expand=True)
            self.init_buttons_frame.pack_forget()
            self.on_algorithm_change()
            self.belief_current_states = list(self.selected_initial_states)
            states_size = 35 if self.algorithm_var.get() == "Partially Observable Search" else 50
            for i in range(3):
                self.clear_frame(self.belief_init_frames[i])
                self.draw_static_board(self.belief_init_frames[i], self.selected_initial_states[i], size=states_size)
                self.clear_frame(self.belief_goal_frames[i])
                self.draw_static_board(self.belief_goal_frames[i], self.selected_goal_states[i], size=states_size)
                self.clear_frame(self.belief_current_frames[i])
                self.draw_static_board(self.belief_current_frames[i], self.belief_current_states[i], size=states_size)
        else:
            self.belief_board_frame.pack_forget()
            self.normal_board_frame.pack(fill=tk.BOTH, expand=True)
            self.init_buttons_frame.pack(fill='x', padx=10, pady=(10, 4))
            self.update_puzzle_display()

    def on_algorithm_change(self, *args):
        if self.mode_var.get() == 'Belief' and self.algorithm_var.get() == "Partially Observable Search":
            self.partial_obs_group.pack(pady=5, fill='x')
            states_size = 35
            self.clear_frame(self.partial_obs_frame)
            self.draw_static_board(self.partial_obs_frame, self.partial_observation, size=states_size)
            for i in range(3):
                self.clear_frame(self.belief_init_frames[i])
                self.draw_static_board(self.belief_init_frames[i], self.selected_initial_states[i], size=states_size)
                self.clear_frame(self.belief_goal_frames[i])
                self.draw_static_board(self.belief_goal_frames[i], self.selected_goal_states[i], size=states_size)
                self.clear_frame(self.belief_current_frames[i])
                self.draw_static_board(self.belief_current_frames[i], self.belief_current_states[i], size=states_size)
        else:
            self.partial_obs_group.pack_forget()
            states_size = 50
            if self.mode_var.get() == 'Belief':
                for i in range(3):
                    self.clear_frame(self.belief_init_frames[i])
                    self.draw_static_board(self.belief_init_frames[i], self.selected_initial_states[i], size=states_size)
                    self.clear_frame(self.belief_goal_frames[i])
                    self.draw_static_board(self.belief_goal_frames[i], self.selected_goal_states[i], size=states_size)
                    self.clear_frame(self.belief_current_frames[i])
                    self.draw_static_board(self.belief_current_frames[i], self.belief_current_states[i], size=states_size)
        self.update_puzzle_display()

    def stop_solving(self):
        self.is_solving = False
        self.pause_event.set()

    def resume_solving(self):
        if not self.steps or self.current_step_index >= len(self.steps):
            return
        self.is_solving = True
        self.pause_event.set()
        self.root.after(0, self.play_from_current)


    def show_init_entry(self):
        self.init_entry_mode = True
        self.clear_frame(self.initial_frame)
        self.init_entries = []
        for i in range(3):
            row = []
            for j in range(3):
                e = tk.Entry(self.initial_frame, width=3, font=('Helvetica', 18), justify='center')
                e.grid(row=i, column=j, padx=2, pady=2)
                initial_val = self.current_initial_state[i][j] if hasattr(self, 'current_initial_state') and i < len(self.current_initial_state) and j < len(self.current_initial_state[i]) else -1
                e.insert(0, '' if initial_val == -1 else str(initial_val))
                row.append(e)
            self.init_entries.append(row)

    def save_init_entry(self):
        try:
            values = []
            for i in range(3):
                row = []
                for j in range(3):
                    val = self.init_entries[i][j].get().strip()
                    row.append(int(val) if val and val != '-1' else -1)
                values.append(tuple(row))
            self.current_initial_state = tuple(values)
            self.puzzle_state = self.current_initial_state
            self.init_entry_mode = False
            self.init_save_btn.grid_remove()
            self.update_puzzle_display()
        except Exception:
            messagebox.showerror('Lỗi', 'Vui lòng nhập số từ 0 đến 8 hoặc -1 cho ô không biết!')

def main():
    root = tk.Tk()
    app = PuzzleApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()