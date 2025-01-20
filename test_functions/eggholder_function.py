import numpy as np

def eggholder_function(x):
    """
    Eggholder Function
    Global minimum: f(x*) = -959.6407 at x* = (512, 404.2319)
    """
    if len(x) != 2:
        raise ValueError("Eggholder Function is defined only for 2-dimensional input.")

    x1, x2 = x
    term1 = -(x2 + 47) * np.sin(np.sqrt(np.abs(x2 + x1/2 + 47)))
    term2 = -x1 * np.sin(np.sqrt(np.abs(x1 - (x2 + 47))))
    return term1 + term2
