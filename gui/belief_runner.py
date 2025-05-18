class BeliefRunner:
    def __init__(self, algorithm_func):
        self.algorithm_func = algorithm_func

    def run(self, belief_states, goal_states):
        if not belief_states or not goal_states:
            return None, [], 0  # Trả về giá trị mặc định nếu danh sách rỗng

        all_paths = []
        successful_states = []

        # Chạy thuật toán cho từng trạng thái ban đầu với các trạng thái mục tiêu
        for init_state in belief_states:
            # Thử với từng goal_state
            for goal_state in goal_states:
                path = self.algorithm_func(init_state, goal_state)
                if path is not None:
                    all_paths.append(path)
                    successful_states.append(init_state)
                    break  # Thoát khi tìm thấy một đường đi thành công
            if not all_paths or len(all_paths[-1]) == 0:
                all_paths.append([init_state])  # Giữ trạng thái ban đầu nếu không tìm thấy đường đi

        if not all_paths:
            return None, [], 0  # Không có đường đi nào thành công

        # Đồng bộ chiều dài các path
        max_len = max(len(p) for p in all_paths)
        for i in range(len(all_paths)):
            if len(all_paths[i]) < max_len:
                all_paths[i].extend([all_paths[i][-1]] * (max_len - len(all_paths[i])))

        # Gom từng bước theo thời gian
        combined = list(zip(*all_paths))  # list of (s1, s2, s3) tại mỗi bước
        belief_steps = max_len  # Số bước tối đa

        # Lấy trạng thái cuối cùng làm final_belief
        final_belief = [path[-1] for path in all_paths]

        return final_belief, combined, belief_steps