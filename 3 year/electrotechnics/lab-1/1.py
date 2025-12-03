import matplotlib.pyplot as plt

# Данные из эксперимента
M = [0.02 * 9.81 * 0.048, 0.04 * 9.81 * 0.048, 0.05 * 9.81 * 0.048]  # моменты
omega = [10, 15, 17]  # угловые скорости (градусы за 10 секунд)

# Построение графика
plt.figure(figsize=(8, 5))
plt.plot(M, omega, marker='o', linestyle='-', color='b')
plt.title('Зависимость скорости прецессии от момента внешнего усилия')
plt.xlabel('Момент внешнего усилия M, Н·м')
plt.ylabel('Скорость прецессии ω, град/с')
plt.grid(True)
plt.show()
