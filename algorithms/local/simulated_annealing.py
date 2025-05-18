from algorithms.utils import get_neighbors, mismatch_heuristic
import random, math

def simulated_annealing(initial_state, goal_state, initial_temp=1000, cooling_rate=0.99, min_temp=0.1):
    current_state = initial_state
    current_cost = mismatch_heuristic(current_state, goal_state)
    temp = initial_temp
    path = [current_state]

    while temp > min_temp:
        neighbors = get_neighbors(current_state)
        if not neighbors:
            break

        next_state = random.choice(neighbors)
        next_cost = mismatch_heuristic(next_state, goal_state)
        delta = next_cost - current_cost

        if delta < 0 or random.random() < math.exp(-delta / temp):
            current_state = next_state
            current_cost = next_cost
            path.append(current_state)

        temp *= cooling_rate

        if current_state == goal_state:
            return path

    return None