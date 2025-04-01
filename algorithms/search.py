from collections import deque
import heapq


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

def heuristic_misplaced_tiles(state, goal_state):
    return sum(1 for r in range(3) for c in range(3) if state[r][c] != goal_state[r][c] and state[r][c] != 0)

def simple_hill_climbing(initial_state, goal_state):
    current_state = initial_state
    path = [current_state]

    while True:
        neighbors = get_neighbors(current_state)
        best_neighbor = None
        best_heuristic = heuristic_misplaced_tiles(current_state, goal_state)

        for neighbor in neighbors:
            h = heuristic_misplaced_tiles(neighbor, goal_state)
            if h < best_heuristic:
                best_neighbor = neighbor
                best_heuristic = h
        
        if best_neighbor is None:  # Không tìm thấy trạng thái tốt hơn
            return path if current_state == goal_state else None
        
        current_state = best_neighbor
        path.append(current_state)

def steepest_ascent_hill_climbing(initial_state, goal_state):
    """Thuật toán Leo đồi dốc."""
    current_state = initial_state
    path = [current_state]

    while True:
        neighbors = get_neighbors(current_state)
        best_neighbor = min(neighbors, key=lambda s: heuristic_misplaced_tiles(s, goal_state), default=None)

        if best_neighbor is None or heuristic_misplaced_tiles(best_neighbor, goal_state) >= heuristic_misplaced_tiles(current_state, goal_state):
            return path if current_state == goal_state else None  # Dừng khi không thể cải thiện

        current_state = best_neighbor
        path.append(current_state)