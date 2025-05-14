import math
import numpy as np

# Итерационные функции системы (те же, что и для МПИ)
def phi1(x1_k, x2_k):
  return 0.8 + math.sin(x2_k + 1)

def phi2(x1_k_plus_1, x2_k): # x1 уже обновлен
  return 0.1 - math.sin(x1_k_plus_1 - 1)

# Функция для вычисления нормы разности векторов (максимум модуля разностей компонент)
def norm_inf_diff(v_curr, v_prev):
  return np.linalg.norm(v_curr - v_prev, np.inf)

def seidel_system_method(phi1_func, phi2_func, x0_tuple, tolerance, max_iterations=100, print_every_n=5, print_first_n=5):
  x_k = np.array(x0_tuple, dtype=float) # Начальное приближение
  print(f"--- Метод Зейделя (Система) ---")
  print(f"k=0: x1 = {x_k[0]:.8f}, x2 = {x_k[1]:.8f}")

  for k_iter in range(max_iterations):
    x_k_prev_iteration = np.copy(x_k) # Сохраняем значения x^(k) для вычисления ошибки

    # Вычисляем x1^(k+1) используя x2^(k)
    x_k[0] = phi1_func(x_k_prev_iteration[0], x_k_prev_iteration[1])
    # Вычисляем x2^(k+1) используя x1^(k+1) (уже обновленное значение x_k[0])
    x_k[1] = phi2_func(x_k[0], x_k_prev_iteration[1])

    current_error = norm_inf_diff(x_k, x_k_prev_iteration)

    if k_iter < print_first_n or (k_iter + 1) % print_every_n == 0 or current_error < tolerance * 10:
      print(f"k={k_iter+1}: x1 = {x_k[0]:.8f}, x2 = {x_k[1]:.8f}, ||x^(k+1)-x^(k)||inf = {current_error:.2e}")

    if current_error < tolerance:
      print(f"Сходимость достигнута на итерации k={k_iter+1}.")
      return x_k, k_iter + 1

    # x_k уже обновлен для следующей итерации

  print(f"Метод Зейделя не сошелся за {max_iterations} итераций.")
  return None, max_iterations

if __name__ == "__main__":
  # Параметры для метода Зейделя
  initial_approx_seidel = (1.4, -0.3)
  epsilon_tolerance_seidel = 1e-6
  max_iter_seidel = 40 # Обычно Зейдель сходится быстрее

  root_seidel, iterations_seidel = seidel_system_method(phi1, phi2, initial_approx_seidel, epsilon_tolerance_seidel, max_iterations=max_iter_seidel)

  if root_seidel is not None:
    print(f"\nКорень (Зейдель): x1 = {root_seidel[0]:.7f}, x2 = {root_seidel[1]:.7f}")
    print(f"Число итераций: {iterations_seidel}")
  else:
    print("\nРешение методом Зейделя не найдено.")