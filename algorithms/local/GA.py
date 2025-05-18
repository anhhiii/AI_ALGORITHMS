from algorithms.utils import get_neighbors, mismatch_heuristic
import random

POPULATION_SIZE = 30
GENOME_LENGTH = 30
GENERATIONS = 200
MUTATION_RATE = 0.2

def genetic_algorithm(initial_state, goal_state):
    def flatten(state):
        return [num for row in state for num in row]

    def hamming_distance(state):
        flat_s = flatten(state)
        flat_g = flatten(goal_state)
        return sum(1 for a, b in zip(flat_s, flat_g) if a != b and a != 0)

    def generate_candidate():
        path = [initial_state]
        current = initial_state
        visited = {current}

        for _ in range(GENOME_LENGTH):
            neighbors = [n for n in get_neighbors(current) if n not in visited]
            if not neighbors:
                break
            current = random.choice(neighbors)
            visited.add(current)
            path.append(current)
        return path

    def evaluate(candidate):
        return -hamming_distance(candidate[-1])

    def crossover(p1, p2):
        if len(p1) < 3 or len(p2) < 3:
            return p1[:]
        split = random.randint(1, min(len(p1), len(p2)) - 2)
        return p1[:split] + p2[split:]

    def mutate(candidate):
        idx = random.randint(1, len(candidate) - 1)
        base = candidate[idx - 1]
        visited = set(candidate[:idx])
        neighbors = [n for n in get_neighbors(base) if n not in visited]
        if not neighbors:
            return candidate
        new_state = random.choice(neighbors)
        return candidate[:idx] + [new_state]

    population = [generate_candidate() for _ in range(POPULATION_SIZE)]

    for _ in range(GENERATIONS):
        population.sort(key=evaluate, reverse=True)
        next_gen = population[:2]
        while len(next_gen) < POPULATION_SIZE:
            p1, p2 = random.sample(population[:5], 2)
            child = crossover(p1, p2)
            if random.random() < MUTATION_RATE:
                child = mutate(child)
            next_gen.append(child)
        population = next_gen

    best = max(population, key=evaluate)
    if best[-1] == goal_state:
        return best
    return None