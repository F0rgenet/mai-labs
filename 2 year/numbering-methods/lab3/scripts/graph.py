import numpy as np
import matplotlib.pyplot as plt

def g(x): return 3 - 0.5 * x
def h(x): return np.exp(-0.5 * x**2)
def f(x): return g(x) - h(x)

x_vals = np.linspace(5.8, 6.2, 400)
g_vals, h_vals = g(x_vals), h(x_vals)

# Проверка знаков на концах интервала
for xi in (5.9, 6.1):
    print(f"f({xi}) = {f(xi):.4e}")

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(x_vals, g_vals, label=r'$g(x) = 3 - 0.5x$')
plt.plot(x_vals, h_vals, label=r'$h(x) = e^{-0.5x^2}$')

a, b = 5.9, 6.1
plt.axvline(a, color='gray', ls='--', lw=1)
plt.axvline(b, color='gray', ls='--', lw=1)

y_vals = [g(a), g(b), h(a), h(b)]
y_min, y_max = min(y_vals), max(y_vals)
y_pad = max((y_max - y_min) * 0.05, 0.01)
y_range = np.linspace(y_min - y_pad, y_max + y_pad, 2)

plt.fill_betweenx(y_range, a, b, color='lightgray', alpha=0.5,
                  label=f'Интервал локализации [{a}, {b}]')

plt.title(f'Локализация корня: $g(x)$ и $h(x)$ на отрезке [{a}, {b}]')
plt.xlabel('x'), plt.ylabel('y')
plt.legend(), plt.grid(True)

pad_y = max((np.max(h_vals) - np.min(g_vals)) * 0.2, 0.05)
plt.ylim(np.min(g_vals) - pad_y, np.max(h_vals) + pad_y)

