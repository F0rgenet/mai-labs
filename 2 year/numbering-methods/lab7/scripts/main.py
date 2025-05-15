import numpy as np
from functions import f, I_exact # Импортируем f(x) и точное значение
from trapezoid import trapezoid_rule
from simpson import simpson_rule

# Параметры интегрирования
a = 1.0
b = 4.0

print(f"Лабораторная работа №7: Численное интегрирование")
print(f"Функция: f(x) = 1 / (x^2 * (x+1)^2)")
print(f"Отрезок интегрирования: [{a}, {b}]")
print(f"Точное значение интеграла: {I_exact:.7f}\n")

# --- Метод Трапеций ---
print("--- Метод Трапеций ---")
n1_trap = 20
n2_trap = 2 * n1_trap

I1_trap = trapezoid_rule(f, a, b, n1_trap)
I2_trap = trapezoid_rule(f, a, b, n2_trap)

# Правило Рунге для трапеций (p=2)
# Погрешность I_2n оценивается как (I_2n - I_n) / (2^p - 1)
runge_correction_trap = (I2_trap - I1_trap) / (2**2 - 1)
error_estimate_trap = abs(runge_correction_trap)
adjusted_I_trap = I2_trap + runge_correction_trap # Уточненное значение

print(f"Число интервалов n = {n1_trap}, Интеграл I_n = {I1_trap:.7f}")
print(f"Число интервалов 2n = {n2_trap}, Интеграл I_2n = {I2_trap:.7f}")
print(f"Оценка погрешности для I_2n (Рунге): {error_estimate_trap:.3e}")
# print(f"Уточненное значение (Рунге): {adjusted_I_trap:.7f}") # Можно добавить, если нужно
print(f"Абсолютная погрешность I_2n от точного: {abs(I2_trap - I_exact):.3e}\n")


# --- Метод Симпсона ---
print("--- Метод Симпсона ---")
n1_simp = 20 # n должно быть четным
n2_simp = 2 * n1_simp

I1_simp = simpson_rule(f, a, b, n1_simp)
I2_simp = simpson_rule(f, a, b, n2_simp)

# Правило Рунге для Симпсона (p=4)
runge_correction_simp = (I2_simp - I1_simp) / (2**4 - 1)
error_estimate_simp = abs(runge_correction_simp)
adjusted_I_simp = I2_simp + runge_correction_simp # Уточненное значение

print(f"Число интервалов n = {n1_simp}, Интеграл I_n = {I1_simp:.7f}")
print(f"Число интервалов 2n = {n2_simp}, Интеграл I_2n = {I2_simp:.7f}")
print(f"Оценка погрешности для I_2n (Рунге): {error_estimate_simp:.3e}")
# print(f"Уточненное значение (Рунге): {adjusted_I_simp:.7f}")
print(f"Абсолютная погрешность I_2n от точного: {abs(I2_simp - I_exact):.3e}\n")

# Данные для ручного расчета в отчет
print("--- Данные для ручных расчетов (в отчет) ---")
# Трапеции n=2
h_trap_manual = (b - a) / 2
x_trap_manual = np.linspace(a, b, 2 + 1)
y_trap_manual = f(x_trap_manual)
I_trap_manual_n2 = (h_trap_manual / 2) * (y_trap_manual[0] + 2 * y_trap_manual[1] + y_trap_manual[2])
print(f"Ручной расчет (Трапеции, n=2):")
print(f"  h = {h_trap_manual}")
print(f"  x_nodes = {x_trap_manual}")
print(f"  y_values = {y_trap_manual}")
print(f"  Integral = {I_trap_manual_n2:.7f}")

# Симпсон n=2
h_simp_manual = (b - a) / 2
x_simp_manual = np.linspace(a, b, 2 + 1)
y_simp_manual = f(x_simp_manual)
I_simp_manual_n2 = (h_simp_manual / 3) * (y_simp_manual[0] + 4 * y_simp_manual[1] + y_simp_manual[2])
print(f"Ручной расчет (Симпсон, n=2):")
print(f"  h = {h_simp_manual}")
print(f"  x_nodes = {x_simp_manual}")
print(f"  y_values = {y_simp_manual}")
print(f"  Integral = {I_simp_manual_n2:.7f}")