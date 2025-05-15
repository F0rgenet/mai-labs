import numpy as np

def simpson_rule(func, a, b, n):
    """
    Вычисляет определенный интеграл функции func от a до b
    используя метод Симпсона с n интервалами (n должно быть четным).
    """
    if n % 2 != 0:
        raise ValueError("n должно быть четным для метода Симпсона.")
    
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = func(x)
    
    integral = y[0] + y[n] # f(x_0) + f(x_n)
    
    for i in range(1, n):
        if i % 2 == 1:  # Нечетные индексы (x_1, x_3, ..., x_{n-1})
            integral += 4 * y[i]
        else:  # Четные индексы (x_2, x_4, ..., x_{n-2})
            integral += 2 * y[i]
            
    integral *= h / 3
    return integral