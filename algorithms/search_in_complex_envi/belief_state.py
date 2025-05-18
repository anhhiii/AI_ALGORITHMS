from algorithms.utils import move

# def belief_state_search(beliefs, goal, search_fn):
#     for belief in beliefs:
#         result = search_fn(belief, goal)
#         if result:
#             return result
#     return None

def belief_bfs_wrapper(search_fn, init_beliefs, goal_states):
    # Mỗi belief là một trạng thái cụ thể
    from collections import deque
    queue = deque()
    visited = set()
    queue.append((tuple(init_beliefs), []))

    while queue:
        current_belief, path = queue.popleft()

        # Nếu tất cả trạng thái đều đạt goal
        if all(state in goal_states for state in current_belief):
            return path

        for action in ['up', 'down', 'left', 'right']:
            next_belief = []
            for state in current_belief:
                next_state = move(state, action)
                if next_state:
                    next_belief.append(next_state)

            belief_tuple = tuple(next_belief)
            if belief_tuple not in visited:
                visited.add(belief_tuple)
                queue.append((belief_tuple, path + [action]))
    return None
