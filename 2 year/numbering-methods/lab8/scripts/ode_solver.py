import numpy as np
import matplotlib.pyplot as plt
import os
import math


def f_ode(x, y):
    if abs(y) > 1e10:
        return -np.sign(y) * 1e12 if (1 - x**3) < 0 else np.sign(y) * 1e12
    try:
        term1 = 4 * y**2 * math.exp(4 * x) * (1 - x**3)
        term2 = 4 * x**3 * y
        return term1 - term2
    except OverflowError:
        if (1 - x**3) < 0:
            return -1e15
        else:
            return 1e15

C_exact = math.exp(-1) + math.exp(3)

def exact_solution(x):
    try:
        exp_x4 = math.exp(x**4)
        exp_4x = math.exp(4 * x)
        denominator = C_exact * exp_x4 - exp_4x
        if abs(denominator) < 1e-15:
            return float("inf") if denominator >= 0 else float("-inf")
        return 1.0 / denominator
    except OverflowError:
        if x > 1.5:
            return 0.0
        return float("nan")


def euler_method(f, x0, y0, h, x_end):
    x_points = [x0]
    y_points = [y0]
    xi = x0
    yi = y0

    n_steps = math.ceil((x_end - x0) / h - 1e-9)

    for i in range(n_steps):
        if xi + h > x_end + 1e-9 and abs(xi - x_end) > 1e-9:
            h_step = x_end - xi
        else:
            h_step = h

        yi += h_step * f(xi, yi)
        xi += h_step

        x_points.append(xi)
        y_points.append(yi)

        if xi >= x_end - 1e-9:
            break

    if abs(x_points[-1] - x_end) > 1e-9 and x_points[-1] < x_end:
        h_final_adjust = x_end - x_points[-1]
        y_points[-1] += h_final_adjust * f(x_points[-1], y_points[-1])
        x_points[-1] = x_end
    return np.array(x_points), np.array(y_points)


def runge_kutta_4(f, x0, y0, h, x_end):
    x_points = [x0]
    y_points = [y0]
    xi = x0
    yi = y0
    n_steps = math.ceil((x_end - x0) / h - 1e-9)
    for i in range(n_steps):
        if xi + h > x_end + 1e-9 and abs(xi - x_end) > 1e-9:
            h_step = x_end - xi
        else:
            h_step = h

        k1 = h_step * f(xi, yi)
        k2 = h_step * f(xi + 0.5 * h_step, yi + 0.5 * k1)
        k3 = h_step * f(xi + 0.5 * h_step, yi + 0.5 * k2)
        k4 = h_step * f(xi + h_step, yi + k3)
        yi += (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
        xi += h_step

        x_points.append(xi)
        y_points.append(yi)
        if xi >= x_end - 1e-9:
            break

    if abs(x_points[-1] - x_end) > 1e-9 and x_points[-1] < x_end:
        h_final_adjust = x_end - x_points[-1]

        xi_prev = x_points[-2]
        yi_prev = y_points[-2]

        k1 = h_final_adjust * f(xi_prev, yi_prev)
        k2 = h_final_adjust * f(xi_prev + 0.5 * h_final_adjust, yi_prev + 0.5 * k1)
        k3 = h_final_adjust * f(xi_prev + 0.5 * h_final_adjust, yi_prev + 0.5 * k2)
        k4 = h_final_adjust * f(xi_prev + h_final_adjust, yi_prev + k3)
        y_points[-1] = yi_prev + (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
        x_points[-1] = x_end
    return np.array(x_points), np.array(y_points)

x_start = 1.0
y_start = 1.0
x_finish = 2.8
epsilon_rk4_step_target = 1e-4
print("--- 1. Определение начального шага h0 для Рунге-Кутты ---")
h0_test_initial = 0.2
print(f"Первоначальный тестовый шаг h0_test_initial = {h0_test_initial}")
current_h_for_test = h0_test_initial
for test_iter in range(5):
    print(f"\nПопытка {test_iter+1} с h_test = {current_h_for_test:.5f}")
    x_check_point = x_start + 2 * current_h_for_test
    if x_check_point > x_finish + 1e-9:
        print(
            f"Точка проверки {x_check_point:.2f} выходит за x_finish={x_finish:.2f}. Уменьшаем шаг."
        )
        current_h_for_test /= 2
        if test_iter == 4:
            current_h_for_test = (x_finish - x_start) / 20
            print(f"Принудительно устанавливаем h_test = {current_h_for_test:.5f}")
        continue
    try:
        _, y_h0_arr = runge_kutta_4(
            f_ode, x_start, y_start, current_h_for_test, x_check_point
        )
        y_h0_at_checkpoint = y_h0_arr[-1]
        _, y_2h0_arr = runge_kutta_4(
            f_ode, x_start, y_start, 2 * current_h_for_test, x_check_point
        )
        y_2h0_at_checkpoint = y_2h0_arr[-1]
    except OverflowError:
        print(
            f"OverflowError при вычислении с h_test = {current_h_for_test:.5f}. Уменьшаем шаг."
        )
        current_h_for_test /= 2
        h_final_chosen = current_h_for_test
        continue
    error_h0_selection = abs(y_h0_at_checkpoint - y_2h0_at_checkpoint) / 15.0
    print(
        f"y(x0+2h_test) с шагом h_test={current_h_for_test:.5f}: {y_h0_at_checkpoint:.7f}"
    )
    print(
        f"y(x0+2h_test) с шагом 2h_test={2*current_h_for_test:.5f}: {y_2h0_at_checkpoint:.7f}"
    )
    print(f"Оценка погрешности |y_h - y_2h|/15 = {error_h0_selection:.2e}")
    if error_h0_selection < epsilon_rk4_step_target and error_h0_selection > 0:
        h_final_chosen = current_h_for_test
        print(
            f"Шаг h={h_final_chosen:.5f} обеспечивает требуемую точность ({error_h0_selection:.2e} < {epsilon_rk4_step_target:.1e})."
        )
        break
    else:
        if error_h0_selection == 0 and y_h0_at_checkpoint == y_2h0_at_checkpoint:
            print(
                "Нулевая погрешность, но значения могут быть неверными из-за большого шага. Уменьшаем шаг для проверки."
            )
            h_final_chosen = current_h_for_test / 2
        elif error_h0_selection == 0:
            h_final_chosen = current_h_for_test / 2
            print("Странная нулевая погрешность. Уменьшаем шаг.")
        else:
            h_final_chosen = (
                current_h_for_test
                * (epsilon_rk4_step_target / error_h0_selection) ** 0.25
                * 0.9
            )
            print(
                f"Погрешность велика или некорректна. Новый рекомендуемый шаг h_final ~ {h_final_chosen:.5f}"
            )
        current_h_for_test = h_final_chosen
        if current_h_for_test < 1e-5:
            print("Шаг стал слишком маленьким. Остановка подбора.")
            h_final_chosen = 1e-5
            break
else:
    print(
        "Не удалось подобрать шаг, удовлетворяющий точности за 5 итераций. Используется последний рассчитанный."
    )

N_steps_on_interval = math.ceil((x_finish - x_start) / h_final_chosen)
if N_steps_on_interval % 2 != 0:
    N_steps_on_interval += 1
if N_steps_on_interval == 0:
    N_steps_on_interval = 2
N_max_for_report = 60
if N_steps_on_interval > N_max_for_report:
    print(
        f"Расчетное число шагов {N_steps_on_interval} слишком велико, ограничиваем до {N_max_for_report}"
    )
    N_steps_on_interval = N_max_for_report
    if N_steps_on_interval % 2 != 0:
        N_steps_on_interval -= 1
h_for_report_calc = (x_finish - x_start) / N_steps_on_interval
print(
    f"\nОкончательно выбран шаг для расчетов h = {h_for_report_calc:.7f} (число шагов N = {N_steps_on_interval})"
)
print("\n--- 2. Решение методом Рунге-Кутты IV ---")
h_rk4 = h_for_report_calc
x_rk4_h, y_rk4_h = runge_kutta_4(f_ode, x_start, y_start, h_rk4, x_finish)
x_rk4_2h, y_rk4_2h = runge_kutta_4(f_ode, x_start, y_start, 2 * h_rk4, x_finish)
print(f"Решение с шагом h = {h_rk4:.5f} (N_h={len(x_rk4_h)-1} шагов):")
print("  x_i   | y_i(h)")
print("-------------------")
points_to_show = min(len(x_rk4_h), 11)
for i in np.linspace(0, len(x_rk4_h) - 1, points_to_show, dtype=int):
    print(f"{x_rk4_h[i]:7.4f} | {y_rk4_h[i]:.7f}")
print(f"\nРешение с шагом 2h = {2*h_rk4:.5f} (N_2h={len(x_rk4_2h)-1} шагов):")
print("  x_i   | y_i(2h)  | Погр. Рунге")
print("----------------------------------")
for i in range(len(x_rk4_2h)):
    error_runge_val = (
        abs(y_rk4_h[i * 2] - y_rk4_2h[i]) / 15.0
        if i * 2 < len(y_rk4_h)
        else float("nan")
    )
    if (
        i
        % (
            max(
                1,
                (len(x_rk4_2h) - 1)
                // (points_to_show - 1 if points_to_show > 1 else 1),
            )
        )
        == 0
        or i == len(x_rk4_2h) - 1
    ):
        print(f"{x_rk4_2h[i]:7.4f} | {y_rk4_2h[i]:.7f} | {error_runge_val:.2e}")
print("\n--- 3. Решение методом Эйлера ---")
h_euler = h_rk4
x_euler, y_euler = euler_method(f_ode, x_start, y_start, h_euler, x_finish)
print(f"Решение с шагом h = {h_euler:.5f} (N_h={len(x_euler)-1} шагов):")
print("  x_i   | y_i (Эйлер)")
print("-----------------------")
for i in np.linspace(0, len(x_euler) - 1, points_to_show, dtype=int):
    print(f"{x_euler[i]:7.4f} | {y_euler[i]:.7f}")
print("\n--- 4. Точное решение ---")
x_exact_nodes = x_rk4_h
y_exact_values = np.array([exact_solution(xi) for xi in x_exact_nodes])
print("  x_i   | y_i (Точное)")
print("----------------------")
for i in np.linspace(0, len(x_exact_nodes) - 1, points_to_show, dtype=int):
    print(f"{x_exact_nodes[i]:7.4f} | {y_exact_values[i]:.7f}")
print("\n--- 5. Сравнение и максимальные отклонения ---")
y_exact_for_rk4_h = np.array([exact_solution(xi) for xi in x_rk4_h])
deviation_rk4 = np.abs(y_rk4_h - y_exact_for_rk4_h)
max_dev_rk4 = np.max(deviation_rk4) if len(deviation_rk4) > 0 else float("nan")
print(f"Максимальное отклонение для Рунге-Кутты (h={h_rk4:.5f}): {max_dev_rk4:.2e}")
y_exact_for_euler = np.array([exact_solution(xi) for xi in x_euler])
deviation_euler = np.abs(y_euler - y_exact_for_euler)
max_dev_euler = np.max(deviation_euler) if len(deviation_euler) > 0 else float("nan")
print(f"Максимальное отклонение для Эйлера (h={h_euler:.5f}): {max_dev_euler:.2e}")
print("\n--- 6. Сводная таблица результатов (несколько точек) ---")
print("  x_i   |  y_Euler  |  y_RK4(h) | y_Точное | |y_RK4-y_T| | |y_Eul-y_T| |")
print("------------------------------------------------------------------------------")
indices_to_print_summary = np.linspace(
    0, len(x_rk4_h) - 1, min(len(x_rk4_h), points_to_show), dtype=int
)
for i in indices_to_print_summary:
    xi_val = x_rk4_h[i]

    euler_idx = np.argmin(np.abs(x_euler - xi_val))
    yi_euler_val = y_euler[euler_idx] if euler_idx < len(y_euler) else float("nan")
    dev_euler_i_val = (
        deviation_euler[euler_idx] if euler_idx < len(deviation_euler) else float("nan")
    )
    yi_rk4_val = y_rk4_h[i]
    yi_exact_val = y_exact_values[i]
    dev_rk4_i_val = deviation_rk4[i]
    print(
        f"{xi_val:7.4f} | {yi_euler_val:9.5f} | {yi_rk4_val:9.5f} | {yi_exact_val:9.5f} |  {dev_rk4_i_val:7.2e}   |  {dev_euler_i_val:7.2e}   |"
    )
if not os.path.exists("images"):
    os.makedirs("images")
plt.figure(figsize=(12, 7))
plt.plot(
    x_rk4_h,
    y_rk4_h,
    "bo-",
    label=f"Рунге-Кутта IV (h={h_rk4:.4f})",
    markersize=3,
    linewidth=1,
)
plt.plot(
    x_euler,
    y_euler,
    "g^--",
    label=f"Эйлер (h={h_euler:.4f})",
    markersize=3,
    linewidth=1,
)
plt.plot(
    x_exact_nodes, y_exact_values, "r-", label="Точное решение", linewidth=2, alpha=0.8
)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Сравнение численных методов решения ОДУ (Вариант 8)")
plt.legend()
plt.grid(True)
plt.ylim(
    min(
        0,
        np.min(y_exact_values) * 1.1
        if len(y_exact_values) > 0 and not np.isnan(np.min(y_exact_values))
        else -1,
    ),
    max(
        1.5,
        np.max(y_exact_values) * 1.1
        if len(y_exact_values) > 0 and not np.isnan(np.max(y_exact_values))
        else 2,
    ),
)
plt.savefig("images/ode_lab8_comparison_plot.png")
print("\nГрафик сравнения методов сохранен в images/ode_lab8_comparison_plot.png")
