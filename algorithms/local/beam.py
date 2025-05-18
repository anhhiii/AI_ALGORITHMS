from algorithms.utils import get_neighbors, mismatch_heuristic

def beam_search(initial_state, goal_state, beam_width=2):
    visited = set()
    queue = [(mismatch_heuristic(initial_state, goal_state), [initial_state])]

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
                    h = mismatch_heuristic(neighbor, goal_state)
                    next_level.append((h, path + [neighbor]))

        queue = next_level