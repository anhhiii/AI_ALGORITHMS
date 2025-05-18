# andor.py
import random
from algorithms.utils import move

ACTIONS = ["up", "down", "left", "right"]

def and_or_search(initial_state, goal_state):
    class Problem:
        def __init__(self, initial, goal):
            self.initial = initial
            self.goal = goal

        def goal_test(self, state):
            return state == self.goal

        def actions(self, state):
            return ACTIONS

        def result(self, state, action):
            next_states = []
            correct = move(state, action)
            if correct and correct != state:
                next_states.append(correct)
            return next_states

    problem = Problem(initial_state, goal_state)
    memo = {}
    visited = set()  # Thêm tập visited để theo dõi trạng thái
    return or_search(initial_state, problem, path=[], memo=memo, visited=visited)

def or_search(state, problem, path, memo, visited):
    if problem.goal_test(state):
        return [state]

    state_str = str(state)  # Chuyển trạng thái thành chuỗi để lưu trong visited
    if state_str in visited:
        return None
    visited.add(state_str)

    if state in path:  # Giữ kiểm tra chu kỳ trong path
        return None

    if state in memo:
        return memo[state]

    for action in problem.actions(state):
        result_states = problem.result(state, action)
        plan = and_search(result_states, problem, path + [state], memo, visited)
        if plan:
            memo[state] = [state] + plan
            return memo[state]

    memo[state] = None
    return None

def and_search(states, problem, path, memo, visited):
    plans = []
    for s in states:
        if s in path:  # Ngăn đệ quy vô hạn
            continue
        plan = or_search(s, problem, path, memo, visited)
        if not plan:
            return None
        plans.extend(plan)
    return plans