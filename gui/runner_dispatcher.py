from .normal_runner import NormalRunner
from .belief_runner import BeliefRunner

def get_runner(mode, algorithm_fn, algorithm_name=None):
    if mode == "Belief":
        return BeliefRunner(algorithm_fn)
    return NormalRunner(algorithm_fn, algorithm_name)
