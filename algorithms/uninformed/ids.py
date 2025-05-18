from algorithms.utils import get_neighbors

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