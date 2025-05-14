import numpy as np
import matplotlib.pyplot as plt
import os

# Создаем папку images, если ее нет
if not os.path.exists('images'):
    os.makedirs('images')

# Определение функций для построения графиков
# x2 = 0.1 - sin(x1 - 1)
def func1_for_x2(x1_val):
  return 0.1 - np.sin(x1_val - 1)

# x1 = 0.8 + sin(x2 + 1)  => x2 = arcsin(x1 - 0.8) - 1
def func2_for_x2(x1_val):
  # Проверяем область допустимых значений для arcsin: -1 <= x1 - 0.8 <= 1
  # то есть x1 должно быть в [ -0.2, 1.8 ]
  with np.errstate(invalid='ignore'): # Игнорировать предупреждения для значений вне области arcsin
      val_for_asin = x1_val - 0.8
      # Оставляем только значения, для которых arcsin определен
      valid_indices = (val_for_asin >= -1) & (val_for_asin <= 1)
      result = np.full_like(x1_val, np.nan) # Заполняем nan
      result[valid_indices] = np.arcsin(val_for_asin[valid_indices]) - 1
  return result

# Диапазон значений для x1
x1_plot_range = np.linspace(-0.5, 2.5, 400)

# Вычисление значений x2
x2_from_f1 = func1_for_x2(x1_plot_range)
x2_from_f2 = func2_for_x2(x1_plot_range) # func2_for_x2 сама обработает допустимый диапазон

# Построение графика
plt.figure(figsize=(10, 7))
plt.plot(x1_plot_range, x2_from_f1, label=r'$x_2 = 0.1 - \sin(x_1 - 1)$', linewidth=2)
plt.plot(x1_plot_range, x2_from_f2, label=r'$x_2 = \arcsin(x_1 - 0.8) - 1$', linewidth=2)

# Приблизительная точка пересечения (из предыдущего анализа)
approx_x1_root = 1.43
approx_x2_root = -0.31
plt.plot(approx_x1_root, approx_x2_root, 'ro', markersize=8, label=f'Приблизительный корень\n$x_1 \\approx {approx_x1_root:.2f}, x_2 \\approx {approx_x2_root:.2f}$')

plt.xlabel('$x_1$', fontsize=14)
plt.ylabel('$x_2$', fontsize=14)
plt.title('Графическая локализация корня системы НЛУ', fontsize=16)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(fontsize=12)
plt.axhline(0, color='black', lw=0.5)
plt.axvline(0, color='black', lw=0.5)
plt.ylim(-2, 1.5) # Адаптируем пределы для лучшей видимости
plt.xlim(-0.5, 2.5)

plt.savefig('images/lab4_localization.png')
print("График сохранен в images/lab4_localization.png")
# plt.show() # Раскомментировать для отображения графика