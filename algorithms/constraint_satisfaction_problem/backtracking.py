import time
import random
from algorithms.utils import is_solvable

GOAL_STATE = ((1, 2, 3), (4, 5, 6), (7, 8, 0))

class Backtracking:
    def __init__(self, update_callback=None, delay=0.1):
        self.update_callback = update_callback or (lambda *_: None)
        self.steps = []
        self.step_details = []  # Lưu chi tiết hành động (điền số, quay lui)
        self.delay = delay

    def count_misplaced_tiles(self, state):
        """Đếm số ô sai vị trí so với Goal State."""
        count = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != GOAL_STATE[i][j] and state[i][j] != 0:
                    count += 1
        return count

    def get_allowed_numbers(self, r, c):
        """Trả về danh sách số cho phép dựa trên ràng buộc vị trí."""
        # Ràng buộc mẫu: ô (r, c) chỉ nhận số trong [r * 3 + c + 1, r * 3 + c + 3]
        start = r * 3 + c + 1
        end = min(start + 2, 9)  # Giới hạn tối đa là 8
        return [n for n in range(start, end + 1) if n <= 8]

    def run(self, initial_state=None, goal_state=GOAL_STATE):
        board = [[-1 for _ in range(3)] for _ in range(3)]
        used = [False] * 9
        self.steps.clear()
        self.step_details.clear()

        board[2][2] = 0
        used[0] = True
        self.steps.append(tuple(tuple(row) for row in board))
        self.step_details.append("Khởi tạo: ô (2,2) = 0")
        self.update_callback(self.steps[-1], len(self.steps), self.step_details[-1])
        time.sleep(self.delay)

        success = self._backtrack(board, used, 0, goal_state)
        if not success:
            self.step_details.append("Không tìm thấy lời giải")
            self.update_callback(self.steps[-1], len(self.steps), self.step_details[-1])
        return self.steps



    def _backtrack(self, board, used, idx, goal_state):
        if idx == 8:
            state = tuple(tuple(row) for row in board)
            if is_solvable(state):
                self.steps.append(state)
                self.step_details.append(f"Hoàn thành điền: {state}")
                self.update_callback(state, len(self.steps), self.step_details[-1])
                time.sleep(self.delay)
                if state == goal_state:
                    return True
                self.steps.pop()
                self.step_details.append(f"Quay lui: trạng thái {state} không phải Goal")
                self.update_callback(self.steps[-1], len(self.steps), self.step_details[-1])
                time.sleep(self.delay)
            return False

        r, c = divmod(idx, 3)
        if r == 2 and c == 2:
            return self._backtrack(board, used, idx + 1, goal_state)

        allowed_numbers = [n for n in self.get_allowed_numbers(r, c) if not used[n]]
        random.shuffle(allowed_numbers)
        for n in allowed_numbers:
            used[n] = True
            board[r][c] = n
            state = tuple(tuple(row) for row in board)
            self.steps.append(state)
            self.step_details.append(f"Điền ô ({r},{c}) = {n}")
            self.update_callback(state, len(self.steps), self.step_details[-1])
            time.sleep(self.delay)

            if board[r][c] == goal_state[r][c]:
                self.step_details.append(f"Tiếp tục: ô ({r},{c}) = {n} đúng vị trí")
                self.update_callback(self.steps[-1], len(self.steps), self.step_details[-1])
                time.sleep(self.delay)
                if self._backtrack(board, used, idx + 1, goal_state):
                    return True
            else:
                misplaced = self.count_misplaced_tiles(state)
                if misplaced > 6:
                    self.step_details.append(f"Quay lui sớm: {misplaced} ô sai tại {state}")
                    self.update_callback(self.steps[-1], len(self.steps), self.step_details[-1])
                    time.sleep(self.delay)
                else:
                    if self._backtrack(board, used, idx + 1, goal_state):
                        return True

            used[n] = False
            board[r][c] = -1
            self.steps.pop()
            self.step_details.append(f"Quay lui: bỏ {n} tại ô ({r},{c})")
            self.update_callback(self.steps[-1], len(self.steps), self.step_details[-1])
            time.sleep(self.delay)
        return False
