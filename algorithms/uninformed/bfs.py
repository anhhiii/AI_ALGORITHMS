from collections import deque
from algorithms.utils import get_neighbors

def bfs(initial_state, goal_state):
    """
    Breadth-First Search algorithm for solving 8-puzzle
    """
    # Khởi tạo queue và visited set
    queue = deque([(initial_state, [initial_state])])
    visited = set()
    
    while queue:
        # Lấy trạng thái đầu tiên từ queue
        current_state, path = queue.popleft()
        
        # Kiểm tra nếu đã đến goal state
        if current_state == goal_state:
            return path
            
        # Nếu trạng thái hiện tại chưa được thăm
        if current_state not in visited:
            visited.add(current_state)
            
            # Lấy các trạng thái kề
            for next_state in get_neighbors(current_state):
                if next_state not in visited:
                    new_path = path + [next_state]
                    queue.append((next_state, new_path))
    
    # Không tìm thấy đường đi
    return None