import math

def f(x):
  return 3 - 0.5 * x - math.exp(-0.5 * x**2)

def f_prime(x):
  return -0.5 + x * math.exp(-0.5 * x**2)

def newtons_method(f, f_prime, x0, epsilon, max_iter=100):
  x_prev = x0
  print(f"k=0: x = {x_prev:.8f}")
  results = [(0, x_prev, float('nan'))]
  for k in range(max_iter):
    fx = f(x_prev)
    fpx = f_prime(x_prev)
    if abs(fpx) < 1e-12: # Проверка деления на ноль
      print("Производная близка к нулю!")
      return None, k, results
    x_curr = x_prev - fx / fpx
    error = abs(x_curr - x_prev)
    print(f"k={k+1}: x = {x_curr:.8f}, |x_k - x_(k-1)| = {error:.2e}, f(x) = {f(x_curr):.2e}")
    results.append((k + 1, x_curr, error))
    if error < epsilon:
      return x_curr, k + 1, results
    x_prev = x_curr
  print("Метод Ньютона не сошелся")
  return None, max_iter, results

x0_newton = 6.0
epsilon_req = 1e-6 # Требуемая точность

print("\n--- Метод Ньютона ---")
root_newton, iterations_newton, results_newton = newtons_method(f, f_prime, x0_newton, epsilon_req)

if root_newton is not None:
  print(f"\nКорень (Ньютон): {root_newton:.7f}")
  print(f"Число итераций: {iterations_newton}")
else:
  print("\nРешение не найдено.")