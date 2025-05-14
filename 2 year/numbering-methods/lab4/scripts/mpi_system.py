import math
import numpy as np

# Итерационные функции системы
def phi1(x1_k, x2_k):
  return 0.8 + math.sin(x2_k + 1)

def phi2(x1_k, x2_k):
  return 0.1 - math.sin(x1_k - 1)

# Функция для вычисления нормы разности векторов (максимум модуля разностей компонент)
def norm_inf_diff(v_curr, v_prev):
  return np.linalg.norm(v_curr - v_prev, np.inf)

def simple_iteration_system(phi1_func, phi2_func, x0_tuple, tolerance, max_iterations=100, print_every_n=10, print_first_n=5):
  x_k = np.array(x0_tuple, dtype=float) # Начальное приближение
  print(f"--- Метод Простой Итерации (Система) ---")
  print(f"k=0: x1 = {x_k[0]:.8f}, x2 = {x_k[1]:.8f}")

  for k_iter in range(max_iterations):
    x_k_plus_1 = np.array([0.0, 0.0])
    x_k_plus_1[0] = phi1_func(x_k[0], x_k[1])
    x_k_plus_1[1] = phi2_func(x_k_plus_1[0] if False else x_k[0], x_k[1]) # Для МПИ используем старое x1

    current_error = norm_inf_diff(x_k_plus_1, x_k)

    if k_iter < print_first_n or (k_iter + 1) % print_every_n == 0 or current_error < tolerance * 10:
      print(f"k={k_iter+1}: x1 = {x_k_plus_1[0]:.8f}, x2 = {x_k_plus_1[1]:.8f}, ||x^(k+1)-x^(k)||inf = {current_error:.2e}")

    if current_error < tolerance:
      print(f"Сходимость достигнута на итерации k={k_iter+1}.")
      return x_k_plus_1, k_iter + 1

    x_k = x_k_plus_1

  print(f"Метод простой итерации не сошелся за {max_iterations} итераций.")
  return None, max_iterations

if __name__ == "__main__":
  # Параметры для МПИ
  initial_approx_mpi = (1.4, -0.3)
  epsilon_tolerance_mpi = 1e-6
  max_iter_mpi = 70 # Увеличим немного, если нужно, но для примера хватит

  root_mpi, iterations_mpi = simple_iteration_system(phi1, phi2, initial_approx_mpi, epsilon_tolerance_mpi, max_iterations=max_iter_mpi)

  if root_mpi is not None:
    print(f"\nКорень (МПИ): x1 = {root_mpi[0]:.7f}, x2 = {root_mpi[1]:.7f}")
    print(f"Число итераций: {iterations_mpi}")
  else:
    print("\nРешение МПИ не найдено.")