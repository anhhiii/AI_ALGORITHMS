import random
def get_neighbors(state):
    """
    Lấy các trạng thái kề của trạng thái hiện tại
    """
    neighbors = []
    # Tìm vị trí của ô trống (0)
    empty_pos = None
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                empty_pos = (i, j)
                break
        if empty_pos:
            break
            
    # Các hướng di chuyển có thể (lên, xuống, trái, phải)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for di, dj in directions:
        new_i, new_j = empty_pos[0] + di, empty_pos[1] + dj
        
        # Kiểm tra vị trí mới có hợp lệ không
        if 0 <= new_i < 3 and 0 <= new_j < 3:
            # Tạo trạng thái mới bằng cách đổi chỗ ô trống với ô kề
            new_state = list(list(row) for row in state)
            new_state[empty_pos[0]][empty_pos[1]] = new_state[new_i][new_j]
            new_state[new_i][new_j] = 0
            neighbors.append(tuple(tuple(row) for row in new_state))
            
    return neighbors

def is_valid_state(state):
    """
    Kiểm tra trạng thái có hợp lệ không
    """
    if not isinstance(state, tuple) or len(state) != 3:
        return False
    for row in state:
        if not isinstance(row, tuple) or len(row) != 3:
            return False
    numbers = set()
    for row in state:
        for num in row:
            if not isinstance(num, int) or num < 0 or num > 8:
                return False
            numbers.add(num)
    return len(numbers) == 9

def is_solvable(state):
    """
    Kiểm tra trạng thái có thể giải được không
    """
    if not is_valid_state(state):
        return False
        
    # Chuyển đổi trạng thái thành mảng một chiều
    flat_state = [item for sublist in state for item in sublist]
    inversions = 0
    
    # Đếm số nghịch đảo
    for i in range(len(flat_state)):
        if flat_state[i] == 0:
            continue
        for j in range(i + 1, len(flat_state)):
            if flat_state[j] == 0:
                continue
            if flat_state[i] > flat_state[j]:
                inversions += 1
                
    # Trạng thái có thể giải được nếu số nghịch đảo là số chẵn
    return inversions % 2 == 0

def manhattan_heuristic(state, goal_state):
    distance = 0
    for r in range(3):
        for c in range(3):
            value = state[r][c]
            if value != 0:
                gr, gc = divmod(value - 1, 3)
                distance += abs(r - gr) + abs(c - gc)
    return distance


def mismatch_heuristic(state, goal_state):
    return sum(1 for r in range(3) for c in range(3) if state[r][c] != goal_state[r][c] and state[r][c] != 0)

def move(state, action):
    import copy
    # Tìm vị trí ô trống (0)
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                x, y = i, j
                break

    dx_dy = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
    }

    if action not in dx_dy:
        return None

    dx, dy = dx_dy[action]
    nx, ny = x + dx, y + dy

    # Kiểm tra biên
    if 0 <= nx < 3 and 0 <= ny < 3:
        new_state = [list(row) for row in state]  # Tạo bản sao dạng list
        new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]  # Đổi chỗ
        return tuple(tuple(row) for row in new_state)  # Trả về dạng tuple
    else:
        return None
    
class QPuzzleEnv:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.state = initial_state
        self.actions = ['up', 'down', 'left', 'right']

    def reset(self):
        self.state = self.initial_state
        return self.state

    def is_goal(self, state):
        return state == self.goal_state

    def get_possible_actions(self, state):
        return self.actions

    def sample_action(self):
        return random.choice(self.actions)

    def step(self, state, action):
        new_state = move(state, action)
        if new_state is None:
            return state, -10, False
        old_dist = manhattan_heuristic(state, self.goal_state)
        new_dist = manhattan_heuristic(new_state, self.goal_state)
        reward = 0
        if new_state == self.goal_state:
            reward = 100  # Thưởng lớn khi đạt mục tiêu
        elif new_dist < old_dist:
            reward = 10  # Thưởng khi tiến gần mục tiêu
        elif new_dist == old_dist:
            reward = -1  # Không đổi thì phạt nhẹ
        else:
            reward = -5  # Phạt nếu xa hơn
        done = new_state == self.goal_state
        return new_state, reward, done

    def solve_with_q(self, q_table):
        path = [self.initial_state]
        state = self.initial_state
        visited = set()
        for _ in range(100):
            state_str = str(state)
            if state_str not in q_table:
                break
            # Giả định q_table[state_str] là dict với key là action
            action = max(q_table[state_str].items(), key=lambda x: x[1])[0]  # Lấy action có giá trị cao nhất
            next_state, _, done = self.step(state, action)
            if next_state in visited:
                break
            visited.add(next_state)
            path.append(next_state)
            state = next_state
            if done:
                break
        return path

class CSP:
    def __init__(self, variables, domains, neighbors, constraints):
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.arcs = [(xi, xj) for xi in variables for xj in neighbors[xi] if xi != xj]

    def extract_solution(self):
        return {var: self.domains[var][0] if self.domains[var] else -1 for var in self.variables}
    
    def is_consistent(self, var, value, assignment):
        """
        Kiểm tra giá trị có hợp lệ với các biến đã gán hay không
        """
        for neighbor in self.neighbors[var]:
            if neighbor in assignment:
                if not self.constraints(var, value, neighbor, assignment[neighbor]):
                    return False
        return True

    def forward_check(self, var, value):
        """
        Cập nhật lại domain của các biến lân cận sau khi gán var = value
        """
        removed = []
        for neighbor in self.neighbors[var]:
            for v in self.domains[neighbor][:]:
                if not self.constraints(var, value, neighbor, v):
                    self.domains[neighbor].remove(v)
                    removed.append((neighbor, v))
        return removed

    def restore_domains(self, removed):
        """
        Khôi phục các giá trị domain đã bị loại bỏ
        """
        for var, value in removed:
            if value not in self.domains[var]:
                self.domains[var].append(value)


def create_puzzle_csp(initial_state, goal_state):
    variables = [(i, j) for i in range(3) for j in range(3)]
    domains = {v: list(range(9)) for v in variables}
    
    neighbors = {v: [] for v in variables}
    for i in range(3):
        for j in range(3):
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ni, nj = i + dx, j + dy
                if 0 <= ni < 3 and 0 <= nj < 3:
                    neighbors[(i, j)].append((ni, nj))

    # Sửa constraint để nhận 4 tham số
    def constraint(var1, val1, var2, val2):
        return val1 != val2

    return CSP(variables, domains, neighbors, constraint)



