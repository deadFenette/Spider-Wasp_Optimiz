import numpy as np


def bukin_function_n6(x):
    """
    Bukin Function N. 6
    Global minimum: f(x*) = 0 at x* = (-10, 1)
    """
    x1, x2 = x
    term1 = 100 * np.sqrt(np.abs(x2 - 0.01 * x1 ** 2))
    term2 = 0.01 * np.abs(x1 + 10)
    return term1 + term2
