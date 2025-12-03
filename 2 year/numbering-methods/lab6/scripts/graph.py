# scripts/graph.py
import matplotlib.pyplot as plt
import numpy as np

# Данные варианта 7 (обновленные)
x_data = np.array([0.324, 0.645, 0.966, 1.287, 1.609, 1.930, 2.251, 2.572, 2.893])
y_data = np.array([-2.052, -1.756, -1.076, -0.284, 0.982, 2.209, 4.013, 5.796, 8.011])

# Построение графика исходных точек
plt.figure(figsize=(8, 6))
plt.plot(x_data, y_data, 'o', label='Исходные данные')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Исходные данные варианта 7')
plt.legend()
plt.grid(True)
plt.savefig('images/initial_data.png')
print("График исходных данных сохранен в images/initial_data.png")

# Коэффициенты из вывода mnk.py (обновленные)
coeffs_func1 = [1.2522786165289508, -0.10646674693457064, -2.169752391221911]
coeffs_func2 = [6.4533751329020115, 10.383276070196334, -11.489449462155681]

# Определяем функции
def func1(x, a, b, c):
    return a * x**2 + b * x + c

def func2(x, a, b, c):
    return a * x + b * np.exp(-x) + c

# Создаем точки для построения гладких кривых аппроксимации
x_fit = np.linspace(min(x_data) - 0.1, max(x_data) + 0.1, 200)

y_fit1_values = func1(x_fit, coeffs_func1[0], coeffs_func1[1], coeffs_func1[2])
y_fit2_values = func2(x_fit, coeffs_func2[0], coeffs_func2[1], coeffs_func2[2])

# Построение совмещенного графика
plt.figure(figsize=(10, 7))
plt.plot(x_data, y_data, 'o', label='Исходные данные', markersize=7) # Уменьшил маркеры для 9 точек
plt.plot(x_fit, y_fit1_values, label=f'$y = {coeffs_func1[0]:.3f}x^2 + {coeffs_func1[1]:.3f}x {coeffs_func1[2]:.3f}$')
plt.plot(x_fit, y_fit2_values, label=f'$y = {coeffs_func2[0]:.3f}x + {coeffs_func2[1]:.3f}e^{{-x}} {coeffs_func2[2]:.3f}$')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Аппроксимация функций методом наименьших квадратов (Вариант 7, 9 точек)')
plt.legend()
plt.grid(True)
# plt.ylim(min(y_data) - 1, max(y_data) + 1) # Можно настроить пределы y для лучшей визуализации
plt.savefig('images/approximation_plot.png')
print("График аппроксимаций сохранен в images/approximation_plot.png")
plt.show() # Раскомментировать для отображения