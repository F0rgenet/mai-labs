import numpy as np
import matplotlib.pyplot as plt
import os

class LagrangePolynomial:
    def __init__(self, x_nodes, y_nodes):
        if len(x_nodes) != len(y_nodes):
            raise ValueError("Количество узлов x и y должно совпадать.")
        self.x_nodes = np.array(x_nodes)
        self.y_nodes = np.array(y_nodes)
        self.n = len(x_nodes) -1 # Степень многочлена

    def basis_polynomial(self, i, x):
        """Вычисляет i-й базисный полином l_i(x)"""
        term = 1.0
        for j in range(self.n + 1):
            if i == j:
                continue
            term *= (x - self.x_nodes[j]) / (self.x_nodes[i] - self.x_nodes[j])
        return term

    def __call__(self, x):
        """Вычисляет значение многочлена Лагранжа в точке x"""
        result = 0.0
        for i in range(self.n + 1):
            result += self.y_nodes[i] * self.basis_polynomial(i, x)
        return result

# Данные варианта 7
x_data = [0.235, 0.672, 1.385, 2.051, 2.908]
y_data = [1.082, 1.805, 4.280, 5.011, 7.082]

# 1. Построение интерполяционного многочлена Лагранжа
L4 = LagrangePolynomial(x_data, y_data)

# Вычисление L4(x1+x2)
x_eval_point = x_data[1] + x_data[2] # x1 + x2 = 0.672 + 1.385
L4_at_x1_plus_x2 = L4(x_eval_point)

print(f"Узлы x: {x_data}")
print(f"Узлы y: {y_data}")
print(f"Точка для вычисления x1+x2 = {x_data[1]} + {x_data[2]} = {x_eval_point:.4f}")
print(f"L4({x_eval_point:.4f}) = {L4_at_x1_plus_x2:.7f}")

# Построение графика многочлена Лагранжа
x_plot = np.linspace(min(x_data) - 0.1, max(x_data) + 0.1, 400)
y_plot_L4 = [L4(val) for val in x_plot]

plt.figure(figsize=(10, 6))
plt.plot(x_plot, y_plot_L4, label=f'$L_{L4.n}(x)$ - Многочлен Лагранжа', color='blue')
plt.scatter(x_data, y_data, color='red', zorder=5, label='Узлы интерполяции')
plt.scatter(x_eval_point, L4_at_x1_plus_x2, color='green', marker='X', s=100, zorder=6,
            label=f'$L_{L4.n}({x_eval_point:.3f}) \\approx {L4_at_x1_plus_x2:.3f}$')

plt.title(f'Интерполяционный многочлен Лагранжа $L_{L4.n}(x)$')
plt.xlabel('$x$')
plt.ylabel('$y$')
plt.legend()
plt.grid(True)
plt.axhline(0, color='black', lw=0.5)
plt.axvline(0, color='black', lw=0.5)
plt.savefig('images/lagrange_polynomial.png')
print("График многочлена Лагранжа сохранен в images/lagrange_polynomial.png")
# plt.show()