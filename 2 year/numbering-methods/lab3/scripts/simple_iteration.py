# Код для метода простой итерации
import math

def phi1(x):
  # Итерационная функция x = 6 - 2*exp(-0.5*x^2)
  return 6 - 2 * math.exp(-0.5 * x**2)

def simple_iteration(phi, x0, epsilon, max_iter=100):
  # Выполняет метод простой итерации
  x_prev = x0
  print(f"k=0: x = {x_prev:.8f}")
  results = [(0, x_prev, float('nan'))]
  for k in range(max_iter):
    x_curr = phi(x_prev)
    error = abs(x_curr - x_prev)
    print(f"k={k+1}: x = {x_curr:.8f}, |x_k - x_(k-1)| = {error:.2e}")
    results.append((k + 1, x_curr, error))
    if error < epsilon:
      return x_curr, k + 1, results
    x_prev = x_curr
  print("Метод простой итерации не сошелся")
  return None, max_iter, results

# Параметры
x0_mpi = 6.0
epsilon_req = 1e-6 # Требуемая точность

print("--- Метод Простой Итерации (МПИ) ---")
root_mpi, iterations_mpi, results_mpi = simple_iteration(phi1, x0_mpi, epsilon_req)

if root_mpi is not None:
  print(f"\nКорень (МПИ): {root_mpi:.7f}")
  print(f"Число итераций: {iterations_mpi}")
else:
  print("\nРешение не найдено.")
