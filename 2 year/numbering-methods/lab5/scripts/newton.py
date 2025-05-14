import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs('images', exist_ok=True)

def divided_differences(x, y):
    n = len(x)
    table = np.zeros((n, n))
    table[:, 0] = y
    for j in range(1, n):
        for i in range(n - j):
            table[i, j] = (table[i+1, j-1] - table[i, j-1]) / (x[i+j] - x[i])
    return table

class NewtonPolynomial:
    def __init__(self, x, y):
        self.x = np.array(x)
        self.coeffs = divided_differences(x, y)[0]

    def __call__(self, x_val):
        result, term = self.coeffs[0], 1
        for i in range(1, len(self.coeffs)):
            term *= (x_val - self.x[i-1])
            result += self.coeffs[i] * term
        return result

# Данные
x_data = [0.235, 0.672, 1.385, 2.051, 2.908]
y_data = [1.082, 1.805, 4.280, 5.011, 7.082]

# Проверка на равноотстоящие узлы
h = np.diff(x_data)
if np.allclose(h, h[0]):
    print("Узлы равноотстоящие")
else:
    print("Узлы НЕ равноотстоящие:", ["{:.3f}".format(step) for step in h])

# Таблица разделенных разностей
div_diff = divided_differences(x_data, y_data)
print("\nТаблица разделенных разностей:")
for j in range(len(x_data)):
    row = [f"{div_diff[i, j]:.4f}" for i in range(len(x_data)-j)]
    if row: print(f"Порядок {j}: " + ", ".join(row))

# Многочлен Ньютона
P = NewtonPolynomial(x_data, y_data)
x_val = x_data[1] + x_data[2]
y_val = P(x_val)
print(f"\nЗначение в x1+x2 = {x_val:.4f}: {y_val:.7f}")
print("Коэффициенты многочлена:", [f"{c:.7f}" for c in P.coeffs])

# График
x_plot = np.linspace(min(x_data)-0.1, max(x_data)+0.1, 400)
y_plot = [P(x) for x in x_plot]

plt.figure(figsize=(10, 6))
plt.plot(x_plot, y_plot, label='Многочлен Ньютона', color='purple')
plt.scatter(x_data, y_data, color='red', label='Узлы')
plt.scatter(x_val, y_val, color='lime', marker='P', s=100,
            label=f'$N(x={x_val:.3f}) \\approx {y_val:.3f}$')
plt.title('Интерполяция многочленом Ньютона')
plt.xlabel('$x$')
plt.ylabel('$y$')
plt.grid(True)
plt.legend()
plt.savefig('images/newton_polynomial.png')
print("График сохранён в images/newton_polynomial.png")
