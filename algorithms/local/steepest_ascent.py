from algorithms.utils import get_neighbors, mismatch_heuristic

def steepest_ascent(initial_state, goal_state):
    current_state = initial_state
    path = [current_state]

    while True:
        neighbors = get_neighbors(current_state)
        best_neighbor = min(neighbors, key=lambda s: mismatch_heuristic(s, goal_state), default=None)

        if best_neighbor is None or mismatch_heuristic(best_neighbor, goal_state) >= mismatch_heuristic(current_state, goal_state):
            return path if current_state == goal_state else None

        current_state = best_neighbor
        path.append(current_state)