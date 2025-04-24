# belief_runner.py

def test_beliefs(belief_states, goal_state, algorithm):
    """
    belief_states: list of possible initial states
    goal_state: the final desired state
    algorithm: search function taking (initial_state, goal_state)
    """
    for belief in belief_states:
        result = algorithm(belief, goal_state)
        if result:
            print(f"[✓] Found solution from belief: {belief}")
            return result
    print("[x] No solution found from any belief state.")
    return None

GOAL_STATE = ((1, 2, 3),
              (4, 5, 6),
              (7, 8, 0))
