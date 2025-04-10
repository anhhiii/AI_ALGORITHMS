from collections import deque
import heapq
import random
import math
from heapq import heappush, heappop

def get_neighbors(state):
    neighbors = []
    rows, cols = len(state), len(state[0])
    empty_row, empty_col = [(r, c) for r in range(rows) for c in range(cols) if state[r][c] == 0][0]

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Lên, Xuống, Trái, Phải
    for dr, dc in directions:
        new_row, new_col = empty_row + dr, empty_col + dc
        if 0 <= new_row < rows and 0 <= new_col < cols:
            new_state = [list(row) for row in state]
            new_state[empty_row][empty_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[empty_row][empty_col]
            neighbors.append(tuple(tuple(row) for row in new_state))

    return neighbors

def bfs(initial_state, goal_state):
    queue = deque([(initial_state, [])])
    visited = set()

    while queue:
        state, path = queue.popleft()
        if state == goal_state:
            return path + [state]
        visited.add(state)

        for neighbor in get_neighbors(state):
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))

    return None

def dfs(state, goal_state, visited=None, path=None, depth=0, max_depth=50):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    if state == goal_state:
        return path + [state]

    if depth >= max_depth:
        return None

    visited.add(state)

    for neighbor in get_neighbors(state):
        if neighbor not in visited:
            result = dfs(neighbor, goal_state, visited, path + [neighbor], depth + 1, max_depth)
            if result is not None:
                return result

    return None

def ucs(initial_state, goal_state):
    queue = [(0, initial_state, [])]
    visited = set()

    while queue:
        cost, state, path = heapq.heappop(queue)
        if state == goal_state:
            return path + [state]
        visited.add(state)

        for neighbor in get_neighbors(state):
            if neighbor not in visited:
                heapq.heappush(queue, (cost + 1, neighbor, path + [neighbor]))

    return None

def ids(initial_state, goal_state, max_depth=20):
    def dfs(state, path, depth, visited):
        if state == goal_state:
            return path + [state]
        if depth == 0:
            return None

        visited.add(state)

        for neighbor in get_neighbors(state):
            if neighbor not in visited:
                result = dfs(neighbor, path + [neighbor], depth - 1, visited)
                if result:
                    return result

        visited.remove(state)
        return None

    for depth in range(max_depth):
        visited = set()
        result = dfs(initial_state, [], depth, visited)
        if result:
            return result
    return None

def greedy(initial_state, goal_state):
    def heuristic(state):
        distance = 0
        for r in range(3):
            for c in range(3):
                value = state[r][c]
                if value != 0:
                    gr, gc = divmod(value - 1, 3)
                    distance += abs(r - gr) + abs(c - gc)
        return distance

    queue = [(heuristic(initial_state), initial_state, [])]
    visited = set()

    while queue:
        _, state, path = heapq.heappop(queue)
        if state == goal_state:
            return path + [state]

        visited.add(state)

        for neighbor in get_neighbors(state):
            if neighbor not in visited:
                heapq.heappush(queue, (heuristic(neighbor), neighbor, path + [neighbor]))

    return None

def astar(initial_state, goal_state):
    def heuristic(state):
        distance = 0
        for r in range(3):
            for c in range(3):
                value = state[r][c]
                if value != 0:
                    gr, gc = divmod(value - 1, 3)
                    distance += abs(r - gr) + abs(c - gc)
        return distance

    queue = [(heuristic(initial_state), 0, initial_state, [])]
    visited = set()

    while queue:
        _, cost, state, path = heapq.heappop(queue)
        if state == goal_state:
            return path + [state]

        visited.add(state)

        for neighbor in get_neighbors(state):
            if neighbor not in visited:
                total_cost = cost + 1
                heapq.heappush(queue, (total_cost + heuristic(neighbor), total_cost, neighbor, path + [neighbor]))

    return None

def ida_star(initial_state, goal_state):
    def heuristic(state):
        distance = 0
        for r in range(3):
            for c in range(3):
                value = state[r][c]
                if value != 0:
                    gr, gc = divmod(value - 1, 3)
                    distance += abs(r - gr) + abs(c - gc)
        return distance

    def search(path, g, bound):
        state = path[-1]
        f = g + heuristic(state)
        if f > bound:
            return f
        if state == goal_state:
            return path
        min_bound = float('inf')

        for neighbor in get_neighbors(state):
            if neighbor not in path:
                result = search(path + [neighbor], g + 1, bound)
                if isinstance(result, list):
                    return result
                min_bound = min(min_bound, result)

        return min_bound

    bound = heuristic(initial_state)
    path = [initial_state]
    while True:
        result = search(path, 0, bound)
        if isinstance(result, list):
            return result
        if result == float('inf'):
            return None
        bound = result

def heuristic(state, goal_state):
    return sum(1 for r in range(3) for c in range(3) if state[r][c] != goal_state[r][c] and state[r][c] != 0)

def simple_hill_climbing(initial_state, goal_state):
    current_state = initial_state
    path = [current_state]

    while True:
        neighbors = get_neighbors(current_state)
        best_neighbor = None
        best_heuristic = heuristic(current_state, goal_state)

        for neighbor in neighbors:
            h = heuristic(neighbor, goal_state)
            if h < best_heuristic:
                best_neighbor = neighbor
                best_heuristic = h

        if best_neighbor is None:
            return path if current_state == goal_state else None

        current_state = best_neighbor
        path.append(current_state)

def steepest_ascent_hill_climbing(initial_state, goal_state):
    current_state = initial_state
    path = [current_state]

    while True:
        neighbors = get_neighbors(current_state)
        best_neighbor = min(neighbors, key=lambda s: heuristic(s, goal_state), default=None)

        if best_neighbor is None or heuristic(best_neighbor, goal_state) >= heuristic(current_state, goal_state):
            return path if current_state == goal_state else None

        current_state = best_neighbor
        path.append(current_state)

def stochastic_hill_climbing(initial_state, goal_state):
    current_state = initial_state
    path = [current_state]

    while True:
        neighbors = get_neighbors(current_state)
        if not neighbors:
            return path if current_state == goal_state else None

        better_neighbors = [n for n in neighbors if heuristic(n, goal_state) < heuristic(current_state, goal_state)]
        if not better_neighbors:
            return path if current_state == goal_state else None

        current_state = random.choice(better_neighbors)
        path.append(current_state)

def simulated_annealing(initial_state, goal_state, initial_temp=1000, cooling_rate=0.99, min_temp=0.1):
    current_state = initial_state
    current_cost = heuristic(current_state, goal_state)
    temp = initial_temp
    path = [current_state]

    while temp > min_temp:
        neighbors = get_neighbors(current_state)
        if not neighbors:
            break

        next_state = random.choice(neighbors)
        next_cost = heuristic(next_state, goal_state)
        delta = next_cost - current_cost

        if delta < 0 or random.random() < math.exp(-delta / temp):
            current_state = next_state
            current_cost = next_cost
            path.append(current_state)

        temp *= cooling_rate

        if current_state == goal_state:
            return path

    return None

def beam_search(initial_state, goal_state, beam_width=2):
    visited = set()
    queue = [(heuristic(initial_state, goal_state), [initial_state])]

    while queue:
        queue = sorted(queue, key=lambda x: x[0])[:beam_width]
        next_level = []

        for _, path in queue:
            current = path[-1]
            if current == goal_state:
                return path
            if current in visited:
                continue
            visited.add(current)
            for neighbor in get_neighbors(current):
                if neighbor not in visited:
                    h = heuristic(neighbor, goal_state)
                    next_level.append((h, path + [neighbor]))

        queue = next_level

def and_or_search(initial_state, goal_state):
    """
    Perform an AND-OR search to solve the problem.
    """
    class Problem:
        def __init__(self, initial, goal):
            self.initial = initial
            self.goal = goal

        def goal_test(self, state):
            return state == self.goal

        def actions(self, state):
            return get_neighbors(state)

        def result(self, state, action):
            return [action]  # Return the resulting state as a list for AND-OR search

    problem = Problem(initial_state, goal_state)
    return or_search(initial_state, problem, path=[])

def or_search(state, problem, path):
    if problem.goal_test(state):
        return [state]

    if state in path:
        return None

    for action in problem.actions(state):
        result_states = problem.result(state, action)
        plan = and_search(result_states, problem, path + [state])
        if plan:
            return [state] + plan  # Trả về đường đi từ state đến goal

    return None

def and_search(states, problem, path):
    plans = []
    for s in states:
        plan = or_search(s, problem, path)
        if not plan:
            return None
        plans += plan  # Nối tất cả đường đi lại
    return plans
