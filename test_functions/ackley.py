import numpy as np

def ackley(x):
    a = 20
    b = 0.2
    c = 2 * np.pi
    d = len(x)
    sum1 = -a * np.exp(-b * np.sqrt(np.sum(x**2) / d))
    sum2 = -np.exp(np.sum(np.cos(c * x)) / d)
    return a + np.exp(1) + sum1 + sum2
