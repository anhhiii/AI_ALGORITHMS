from algorithms.uninformed.bfs import bfs
from algorithms.uninformed.dfs import dfs
from algorithms.uninformed.ucs import ucs
from algorithms.uninformed.ids import ids
from algorithms.informed.greedy import greedy
from algorithms.informed.a_star import astar
from algorithms.informed.ida_star import ida_star
from algorithms.local.simple_hill_climbing import simple_hill_climbing
from algorithms.local.steepest_ascent import steepest_ascent
from algorithms.local.stochastic_hill_climbing import stochastic_hill
from algorithms.local.GA import genetic_algorithm
from algorithms.local.simulated_annealing import simulated_annealing
from algorithms.local.beam import beam_search
from algorithms.search_in_complex_envi.andor import and_or_search
from algorithms.constraint_satisfaction_problem.backtracking import Backtracking
from algorithms.reinforcement_learning.Q_learning import q_learning_train, q_learning_step
from algorithms.constraint_satisfaction_problem.ac3 import AC3
from algorithms.constraint_satisfaction_problem.forward_checking import ForwardChecking
from algorithms.search_in_complex_envi.partially import partially_observable_search


def test_beliefs(belief_states, goal_state, algorithm):
    """
    Test algorithm on multiple belief states
    """
    for state in belief_states:
        result = algorithm(state, goal_state)
        if result:
            return result
    return None 