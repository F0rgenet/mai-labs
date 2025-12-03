# scripts/mnk.py
import numpy as np

# Данные варианта 7 (обновленные)
x_data = np.array([0.324, 0.645, 0.966, 1.287, 1.609, 1.930, 2.251, 2.572, 2.893])
y_data = np.array([-2.052, -1.756, -1.076, -0.284, 0.982, 2.209, 4.013, 5.796, 8.011])
n = len(x_data)

print(f"Исходные данные:")
print(f"x: {x_data}")
print(f"y: {y_data}")

# --- Функция 1: y = ax^2 + bx + c ---
print("\n--- Функция 1: y = ax^2 + bx + c ---")

sum_x = np.sum(x_data)
sum_x2 = np.sum(x_data**2)
sum_x3 = np.sum(x_data**3)
sum_x4 = np.sum(x_data**4)

sum_y = np.sum(y_data)
sum_yx = np.sum(y_data * x_data)
sum_yx2 = np.sum(y_data * x_data**2)

# Матрица коэффициентов A1 и вектор свободных членов B1
A1_matrix = np.array([
    [sum_x4, sum_x3, sum_x2],
    [sum_x3, sum_x2, sum_x],
    [sum_x2, sum_x, n]
])
B1_vector = np.array([sum_yx2, sum_yx, sum_y])

print("Матрица A1:")
print(A1_matrix)
print("Вектор B1:")
print(B1_vector)

try:
    coeffs1 = np.linalg.solve(A1_matrix, B1_vector)
    a1, b1, c1 = coeffs1
    print(f"Коэффициенты: a1 = {a1:.4f}, b1 = {b1:.4f}, c1 = {c1:.4f}")

    y_fit1 = a1 * x_data**2 + b1 * x_data + c1
    residuals1 = y_data - y_fit1
    S1 = np.sum(residuals1**2)
    delta1 = np.sqrt(S1)
    print(f"Сумма квадратов остатков S1 = {S1:.6f}")
    print(f"Невязка delta1 = {delta1:.6f}")
    
    print(f"coeffs_func1 = [{a1}, {b1}, {c1}]")


except np.linalg.LinAlgError:
    print("Ошибка: Матрица A1 вырождена, система не имеет единственного решения.")


# --- Функция 2: y = ax + be^(-x) + c ---
print("\n--- Функция 2: y = ax + be^(-x) + c ---")

phi1_vals = x_data
phi2_vals = np.exp(-x_data)
phi3_vals = np.ones(n)

sum_phi1_phi1 = np.sum(phi1_vals * phi1_vals)
sum_phi1_phi2 = np.sum(phi1_vals * phi2_vals)
sum_phi1_phi3 = np.sum(phi1_vals * phi3_vals)

sum_phi2_phi2 = np.sum(phi2_vals * phi2_vals)
sum_phi2_phi3 = np.sum(phi2_vals * phi3_vals)

sum_phi3_phi3 = n # sum(phi3_vals * phi3_vals) which is sum(1*1) = n

sum_y_phi1 = np.sum(y_data * phi1_vals)
sum_y_phi2 = np.sum(y_data * phi2_vals)
sum_y_phi3 = np.sum(y_data * phi3_vals)

A2_matrix = np.array([
    [sum_phi1_phi1, sum_phi1_phi2, sum_phi1_phi3],
    [sum_phi1_phi2, sum_phi2_phi2, sum_phi2_phi3],
    [sum_phi1_phi3, sum_phi2_phi3, sum_phi3_phi3]
])
B2_vector = np.array([sum_y_phi1, sum_y_phi2, sum_y_phi3])

print("Матрица A2:")
print(A2_matrix)
print("Вектор B2:")
print(B2_vector)

try:
    coeffs2 = np.linalg.solve(A2_matrix, B2_vector)
    a2, b2, c2 = coeffs2
    print(f"Коэффициенты: a2 = {a2:.4f}, b2 = {b2:.4f}, c2 = {c2:.4f}")

    y_fit2 = a2 * x_data + b2 * np.exp(-x_data) + c2
    residuals2 = y_data - y_fit2
    S2 = np.sum(residuals2**2)
    delta2 = np.sqrt(S2)
    print(f"Сумма квадратов остатков S2 = {S2:.6f}")
    print(f"Невязка delta2 = {delta2:.6f}")

    print(f"coeffs_func2 = [{a2}, {b2}, {c2}]")

except np.linalg.LinAlgError:
    print("Ошибка: Матрица A2 вырождена, система не имеет единственного решения.")