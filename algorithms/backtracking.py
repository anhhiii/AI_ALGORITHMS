# algorithms/backtracking.py

from copy import deepcopy

def get_neighbors(state):
    from_pos = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0][0]
    i, j = from_pos
    moves = []
    directions = [(-1,0), (1,0), (0,-1), (0,1)]  # up, down, left, right

    for di, dj in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < 3 and 0 <= nj < 3:
            new_state = [list(row) for row in state]
            new_state[i][j], new_state[ni][nj] = new_state[ni][nj], new_state[i][j]
            moves.append(tuple(tuple(row) for row in new_state))
    return moves

def backtracking(initial_state, goal_state, visited=None, path=None, depth_limit=50):
    if visited is None:
        visited = set()
    if path is None:
        path = [initial_state]

    if initial_state == goal_state:
        return path

    if len(path) > depth_limit:
        return None  # giới hạn độ sâu để tránh chạy vô hạn

    visited.add(initial_state)

    for neighbor in get_neighbors(initial_state):
        if neighbor not in visited:
            result = backtracking(neighbor, goal_state, visited.copy(), path + [neighbor], depth_limit)
            if result:
                return result

    return None  # không tìm được -> backtrack
