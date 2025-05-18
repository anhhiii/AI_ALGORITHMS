import time
from algorithms.utils import create_puzzle_csp

class ForwardChecking:
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

        assignment = self._forward_checking(csp)
        if assignment is None:
            self.step_details.append("Không tìm thấy lời giải")
            self.update_callback(self.steps[-1], len(self.steps), self.step_details[-1])
            return None

        self.steps.append(("Solution", str(assignment)))
        self.step_details.append("Tìm thấy lời giải")
        self.update_callback(self.steps[-1], len(self.steps), self.step_details[-1])
        time.sleep(self.get_delay())
        return assignment

    def _forward_checking(self, csp):
        return self.backtrack({}, csp)

    def backtrack(self, assignment, csp):
        if len(assignment) == len(csp.variables):
            return assignment
        var = self.select_unassigned_variable(assignment, csp)
        for value in csp.domains[var]:
            if not csp.domains[var]:
                return None
            if csp.is_consistent(var, value, assignment):
                assignment[var] = value
                removed = csp.forward_check(var, value)

                self.steps.append(("Assignment", str(assignment)))
                self.step_details.append(f"Gán {var} = {value}")
                self.update_callback(self.steps[-1], len(self.steps), self.step_details[-1])
                time.sleep(self.get_delay())

                result = self.backtrack(assignment, csp)
                if result:
                    return result

                del assignment[var]
                csp.restore_domains(removed)

                self.steps.append(("Assignment", str(assignment)))
                self.step_details.append(f"Quay lui: bỏ {var} = {value}")
                self.update_callback(self.steps[-1], len(self.steps), self.step_details[-1])
                time.sleep(self.get_delay())
        return None

    def select_unassigned_variable(self, assignment, csp):
        unassigned = [v for v in csp.variables if v not in assignment]
        return min(unassigned, key=lambda v: len(csp.domains[v]))
