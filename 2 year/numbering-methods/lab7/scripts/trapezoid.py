import numpy as np

def trapezoid_rule(func, a, b, n):
    """
    Вычисляет определенный интеграл функции func от a до b
    используя метод трапеций с n интервалами.
    """
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = func(x)
    
    integral = h * ( (y[0] + y[n]) / 2 + np.sum(y[1:n]) )
    return integral