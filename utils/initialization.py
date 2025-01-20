import numpy as np


def initialize_positions(search_agents_no, dim, ub, lb):
    return np.random.uniform(lb, ub, (search_agents_no, dim))
