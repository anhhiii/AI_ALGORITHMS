import random

def q_learning_train(env, episodes, alpha=0.2, gamma=0.95, epsilon=0.3):
    q_table = {}
    for episode in range(episodes):
        state = env.reset()
        done = False
        while not done:
            state_str = str(state)
            if state_str not in q_table:
                q_table[state_str] = {a: 0.0 for a in env.actions}
            if random.random() < epsilon:
                action = env.sample_action()
            else:
                action = max_q_action(q_table, state, env)
            next_state, reward, done = env.step(state, action)
            next_state_str = str(next_state)
            if next_state_str not in q_table:
                q_table[next_state_str] = {a: 0.0 for a in env.actions}
            old_q = q_table[state_str][action]
            future_q = max(q_table.get(next_state_str, {a: 0.0 for a in env.actions}).values())
            q_table[state_str][action] = old_q + alpha * (reward + gamma * future_q - old_q)
            state = next_state
        if episode % 1000 == 0:
            print(f"Episode {episode}: Q-table size = {len(q_table)}")
    return q_table
def q_learning_step(initial_state, goal_state, q_table, env):
    steps = [initial_state]
    state = initial_state
    visited = set()
    step_count = 0
    print(f"Starting with state: {state}, goal: {goal_state}")
    while state != goal_state and len(steps) < 100:
        state_str = str(state)
        print(f"Step {step_count}: State = {state}, in q_table = {state_str in q_table}")
        if state_str not in q_table:
            print(f"State {state} not in q_table, returning None")
            return None
        action = max_q_action(q_table, state, env)
        print(f"Chosen action: {action}")
        next_state, reward, done = env.step(state, action)
        print(f"Next state: {next_state}, Reward: {reward}, Done: {done}")
        if next_state is None:
            print("Next state is None, returning None")
            return None
        if next_state in visited:
            print(f"Next state {next_state} already visited, returning None")
            return None
        if done and next_state != goal_state:
            print("Done but not goal, returning None")
            return None
        visited.add(next_state)
        steps.append(next_state)
        state = next_state
        step_count += 1
    print(f"Finished with steps: {steps}")
    return steps if state == goal_state else None

def max_q_action(q_table, state, env):
    state_str = str(state)
    return max(env.actions, key=lambda a: q_table.get(state_str, {a: 0.0})[a])