from algorithms.utils import get_neighbors, manhattan_heuristic

def ida_star(initial_state, goal_state):
    def search(path, g, bound):
        state = path[-1]
        f = g + manhattan_heuristic(state, goal_state)
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

    bound = manhattan_heuristic(initial_state, goal_state)
    path = [initial_state]
    while True:
        result = search(path, 0, bound)
        if isinstance(result, list):
            return result
        if result == float('inf'):
            return None
        bound = result