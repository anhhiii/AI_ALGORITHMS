from algorithms.reinforcement_learning.Q_learning import q_learning_train, q_learning_step
from algorithms.utils import QPuzzleEnv 
from algorithms.constraint_satisfaction_problem.backtracking import Backtracking
from algorithms.constraint_satisfaction_problem.ac3 import AC3
from algorithms.constraint_satisfaction_problem.forward_checking import ForwardChecking
from algorithms.search_in_complex_envi.partially import partially_observable_search
from algorithms.puzzle_solver import bfs

class NormalRunner:
    def __init__(self, algorithm_fn, algorithm_name):
        self.algorithm_fn = algorithm_fn
        self.algorithm_name = algorithm_name
        print(f"NormalRunner: algorithm_name = {algorithm_name}, function = {algorithm_fn}")

    def run(self, initial_state, goal_state):
        print(f"Chạy thuật toán: {self.algorithm_name}, function = {self.algorithm_fn}")
        if self.algorithm_fn == q_learning_step or self.algorithm_name == "Q-Learning":
            env = QPuzzleEnv(initial_state, goal_state)
            q_table = q_learning_train(env, episodes=20000, alpha=0.2, gamma=0.95, epsilon=0.3)
            print("Final q_table:", q_table)  # Debug toàn bộ q_table
            return q_learning_step(initial_state, goal_state, q_table, env)

        if self.algorithm_name == "Backtracking":
            runner = Backtracking()
            return runner.run(initial_state, goal_state)
        
        if self.algorithm_name == "AC3":
            runner = AC3(update_callback=self.update_callback, get_delay=self.get_delay)
            return runner.run(initial_state, goal_state)


        if self.algorithm_name == "Partially Observable Search":
            return partially_observable_search(initial_state, goal_state, search_fn=bfs)

        if self.algorithm_name == "AC3":
            return AC3(initial_state, goal_state)

        if self.algorithm_name == "Forward Checking":
            return ForwardChecking(initial_state, goal_state)

        return self.algorithm_fn(initial_state, goal_state)

