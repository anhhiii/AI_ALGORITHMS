from algorithms.puzzle_solver import bfs
from collections import deque

def move(state, action):
    """Di chuyển ô trống theo hành động và trả về trạng thái mới."""
    flat_state = [num for row in state for num in row]
    blank_idx = flat_state.index(0)
    blank_row, blank_col = divmod(blank_idx, 3)

    directions = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
    }

    if action not in directions:
        return None

    dr, dc = directions[action]
    new_row, new_col = blank_row + dr, blank_col + dc

    if 0 <= new_row < 3 and 0 <= new_col < 3:
        new_state = [list(row) for row in state]
        new_state[blank_row][blank_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[blank_row][blank_col]
        return tuple(tuple(row) for row in new_state)
    return None

def partially_observable_search(initial_belief, goal_states, search_fn=bfs):
    # Sử dụng trực tiếp initial_belief và goal_states được truyền vào
    initial_belief = list(initial_belief)
    goal_states = list(goal_states)

    print("Belief States:", initial_belief)
    print("Goal States:", goal_states)

    queue = deque()
    visited = set()
    queue.append((tuple(initial_belief), []))
    visited.add(tuple(initial_belief))

    belief_steps = 0
    while queue:
        current_belief, path = queue.popleft()
        belief_steps += 1

        if all(state in goal_states for state in current_belief):
            return current_belief, path, belief_steps

        for action in ['up', 'down', 'left', 'right']:
            next_belief = []
            for state in current_belief:
                next_state = move(state, action)
                if next_state:
                    next_belief.append(next_state)

            if len(next_belief) == len(current_belief):  # Đảm bảo tất cả trạng thái đều di chuyển được
                belief_tuple = tuple(next_belief)
                if belief_tuple not in visited:
                    visited.add(belief_tuple)
                    queue.append((belief_tuple, path + [action]))

    return None, [], belief_steps