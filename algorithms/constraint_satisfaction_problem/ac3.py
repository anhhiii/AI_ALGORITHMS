import time
from algorithms.utils import create_puzzle_csp

class AC3:
    def __init__(self, update_callback=None, get_delay=None):
        self.update_callback = update_callback or (lambda *_: None)
        self.get_delay = get_delay or (lambda: 0.1)
        self.steps = []
        self.step_details = []

    def run(self, initial_state, goal_state):
        self.steps.clear()
        self.step_details.clear()

        csp = create_puzzle_csp(initial_state, goal_state)
        self.steps.append(("Initial CSP", str(csp.domains)))
        self.step_details.append("Khởi tạo CSP")
        self.update_callback(self.steps[-1], len(self.steps), self.step_details[-1])
        time.sleep(self.get_delay())

        success = self._ac3(csp)
        if not success:
            self.step_details.append("Không tìm thấy lời giải")
            self.update_callback(self.steps[-1], len(self.steps), self.step_details[-1])
            return None

        solution = csp.extract_solution()
        self.steps.append(("Solution", str(solution)))
        self.step_details.append("Tìm thấy lời giải")
        self.update_callback(self.steps[-1], len(self.steps), self.step_details[-1])
        time.sleep(self.get_delay())
        return solution

    def _ac3(self, csp):
        queue = list(csp.arcs)
        while queue:
            (xi, xj) = queue.pop(0)
            if self.revise(csp, xi, xj):
                self.steps.append(("Domains after revise", str(csp.domains)))
                self.step_details.append(f"Revise ({xi}, {xj}): Miền của {xi} thay đổi")
                self.update_callback(self.steps[-1], len(self.steps), self.step_details[-1])
                time.sleep(self.get_delay())

                if not csp.domains[xi]:
                    return False
                for xk in csp.neighbors[xi]:
                    if xk != xj:
                        queue.append((xk, xi))
        return True

    def revise(self, csp, xi, xj):
        revised = False
        for x_val in csp.domains[xi][:]:
            if not any(csp.constraints(xi, x_val, xj, y_val) for y_val in csp.domains[xj]):
                csp.domains[xi].remove(x_val)
                revised = True
        return revised
