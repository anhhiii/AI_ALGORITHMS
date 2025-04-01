import tkinter as tk
from tkinter import messagebox
import time
import threading
from algorithms.search import bfs, dfs, ucs, ids, greedy, astar, ida_star, simple_hill_climbing, steepest_ascent_hill_climbing

INITIAL_STATE = ((2, 6, 5), (0, 8, 7), (4, 3, 1))
GOAL_STATE = ((1, 2, 3), (4, 5, 6), (7, 8, 0))

class PuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title('8-Puzzle Solver')
        self.algorithm_var = tk.StringVar(value='BFS')
        self.tiles = []
        self.move_count = 0
        self.start_time = 0
        self.time_results = {}
        self.is_solving = False
        self.pause_event = threading.Event()  # Biến kiểm soát tạm dừng
        self.pause_event.set()  # Ban đầu để trạng thái chạy bình thường

        self.algorithms = {
            "BFS": bfs,
            "DFS": dfs,
            "UCS": ucs,
            "IDS": ids,
            "Greedy": greedy,
            "A*": astar, 
            "IDA*": ida_star,
            "Simple Hill Climbing": simple_hill_climbing,
            "Steepest Ascent Hill Climbing": steepest_ascent_hill_climbing
        }
        
        self.create_widgets()
        self.reset_board()
    
    def start_solving(self):
        self.is_solving = True
        self.pause_event.set()  # Bật trạng thái chạy
        solving_thread = threading.Thread(target=self.solve)  # Chạy giải thuật trên luồng riêng
        solving_thread.start()

    def toggle_pause(self):
        if self.pause_event.is_set():
            self.pause_event.clear()  # Tạm dừng thuật toán
            self.pause_button.config(text='Tiếp Tục')
        else:
            self.pause_event.set()  # Tiếp tục thuật toán
            self.pause_button.config(text='Dừng')

    def create_widgets(self):
        tk.Label(self.root, text='8-Puzzle Solver', bg='red', fg='white', font=('Arial', 16, 'bold')).pack(fill=tk.X)

        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=5, padx=5)

        # Left frame (boards and steps)
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, padx=10)

        state_frame = tk.Frame(left_frame)
        state_frame.pack()
        
        start_frame = tk.LabelFrame(state_frame, text='Trạng Thái Bắt Đầu', font=('Arial', 10, 'bold'))
        start_frame.pack(side=tk.LEFT, padx=5)
        self.draw_static_board(start_frame, INITIAL_STATE, small=True)
        
        goal_frame = tk.LabelFrame(state_frame, text='Trạng Thái Kết Thúc', font=('Arial', 10, 'bold'))
        goal_frame.pack(side=tk.LEFT, padx=5)
        self.draw_static_board(goal_frame, GOAL_STATE, small=True)

        self.result_frame = tk.LabelFrame(left_frame, text='Kết Quả', font=('Arial', 12, 'bold'))
        self.result_frame.pack(pady=5)
        self.draw_board(INITIAL_STATE)

        # Khung hiển thị các bước đi
        self.steps_frame = tk.LabelFrame(left_frame, text='Các Bước Đi', font=('Arial', 12, 'bold'))
        self.steps_frame.pack(pady=5, fill=tk.BOTH, expand=True)

        # Thêm Scrollbar để cuộn khi danh sách dài
        self.steps_scroll = tk.Scrollbar(self.steps_frame)
        self.steps_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Dùng Text widget thay vì Label để hỗ trợ cuộn
        self.steps_display = tk.Text(self.steps_frame, height=10, width=50, font=('Arial', 12), wrap=tk.WORD, yscrollcommand=self.steps_scroll.set)
        self.steps_display.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        # Liên kết thanh cuộn với Text widget
        self.steps_scroll.config(command=self.steps_display.yview)


        # Right frame (Algorithm, complexity, buttons)
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, padx=10)

        algo_frame = tk.LabelFrame(right_frame, text='Thuật toán', font=('Arial', 12, 'bold'))
        algo_frame.pack(pady=5)
         
        for algo in self.algorithms:
            tk.Radiobutton(algo_frame, text=algo, variable=self.algorithm_var, value=algo).pack(anchor=tk.W)


        self.time_frame = tk.LabelFrame(right_frame, text='Thời gian', font=('Arial', 12))
        self.time_frame.pack(pady=5)
        self.time_display = tk.Label(self.time_frame, text='', font=('Arial', 12))
        self.time_display.pack()

        # Button frame
        button_frame = tk.Frame(right_frame)
        button_frame.pack(pady=5)
        tk.Button(button_frame, text='Giải', bg='green', fg='white', command=self.start_solving).pack(side=tk.LEFT, padx=5)
        self.pause_button = tk.Button(button_frame, text='Dừng/Tiếp tục', bg='yellow', fg='black', command=self.toggle_pause)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text='Làm Mới', bg='orange', fg='white', command=self.reset_board).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text='Xuất File', bg='blue', fg='white', command=self.export_steps).pack(side=tk.LEFT, padx=5)


    def export_steps(self):
        steps_text = self.steps_display.get("1.0", tk.END).strip()
        if not steps_text:
            messagebox.showinfo('Thông báo', 'Không có bước nào để xuất!')
            return
        
        with open("steps_output.txt", "w", encoding="utf-8") as file:
            file.write(steps_text)
        
        messagebox.showinfo('Thành công', 'Các bước đã được xuất ra file steps_output.txt')

    def draw_static_board(self, frame, state, small=False):
        for r, row in enumerate(state):
            for c, value in enumerate(row):
                text = '' if value == 0 else str(value)
                tile = tk.Label(
                    frame, text=text,
                    width=2 if small else 4, height=1 if small else 2,
                    font=('Arial', 14 if small else 24, 'bold'),
                    bg='#FFDAB9' if value != 0 else '#D3D3D3',
                    relief=tk.RAISED, bd=5
                )
                tile.grid(row=r, column=c, padx=1, pady=1)

    def draw_board(self, state):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        for r, row in enumerate(state):
            for c, value in enumerate(row):
                text = '' if value == 0 else str(value)
                tile = tk.Label(
                    self.result_frame, text=text,
                    width=4, height=2,
                    font=('Arial', 24, 'bold'),
                    bg='#FFB347' if value != 0 else '#D3D3D3',
                    relief=tk.RAISED, bd=5
                )
                tile.grid(row=r, column=c, padx=2, pady=2)

    def start_solving(self):
        self.is_solving = True
        self.solve()

    def toggle_pause(self):
        self.is_solving = not self.is_solving
        self.pause_button.config(text='Tiếp Tục' if not self.is_solving else 'Dừng')

    
    def solve(self):
        algorithm = self.algorithm_var.get()
        self.start_time = time.time()
        algorithm_function = self.algorithms.get(algorithm, None)  # Lấy hàm tương ứng

        if algorithm_function:
            result = algorithm_function(INITIAL_STATE, GOAL_STATE)
        else:
            messagebox.showerror('Lỗi', f'Không tìm thấy thuật toán "{algorithm}"')
            return

        elapsed_time = time.time() - self.start_time

        if result is None:
            messagebox.showinfo('Thông báo', 'Không tìm thấy lời giải')
        else:
            self.steps_display.delete('1.0', tk.END)
            for i, step in enumerate(result, start=1):
                self.pause_event.wait()  # Đợi nếu đang tạm dừng

                if not self.is_solving:  # Nếu bị dừng hẳn, thoát khỏi vòng lặp
                    return  

                self.draw_board(step)
                self.steps_display.insert(tk.END, f'Bước {i}: {step}\n')
                self.steps_display.see(tk.END)
                self.root.update()
                time.sleep(0.3)

            self.time_display.config(text=f'{elapsed_time:.4f} giây')
            self.time_results[algorithm] = elapsed_time



    def reset_board(self):
        self.is_solving = False
        self.draw_board(INITIAL_STATE)
        self.steps_display.delete('1.0', tk.END)  # Xóa toàn bộ nội dung của Text widget
        self.time_display.config(text='')


# Chạy ứng dụng
def main():
    root = tk.Tk()
    app = PuzzleApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
