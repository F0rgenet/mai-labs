import math
import numpy as np
import matplotlib.pyplot as plt

m = 5       # последняя цифра года
N = 4       # число каналов обслуживания
Nn = 6      # номер по списку

lambda_ = 15 * m / (N * Nn)
mu = 5 * m / (N * Nn)
a = lambda_ / mu  # интенсивность нагрузки (ρ)

if a >= N:
    print(f"Система неустойчива (a = {a:.2f} ≥ N = {N})\n")

sum_term = sum([a**k / math.factorial(k) for k in range(0, N)])
last_term = (a**N / math.factorial(N)) * (N / (N - a))
P0 = 1.0 / (sum_term + last_term)

# Вероятность ожидания (все каналы заняты)
P_wait = (a**N / math.factorial(N)) * (N / (N - a)) * P0
P_zan = P_wait

eps = 1e-9  # защита от деления на ноль
Lq = max(P_wait * (a / (N - a + eps)), 0)  # средняя длина очереди
L = Lq + a                                 # среднее число заявок в системе
M_zan = a                                  # среднее число занятых каналов
M_sv = N - M_zan                           # среднее число свободных каналов
Wq = max(Lq / lambda_, 0)                  # среднее время ожидания начала обслуживания
W = Wq + 1.0 / mu                          # среднее время пребывания заявки в системе
Tooj = lambda_ * Wq                        # суммарное время ожидания всех заявок в единицу времени
A = lambda_                                # абсолютная пропускная способность

print(f"Задание 2 — СМО с ожиданием\n")
print(f"λ (интенсивность поступления) = {lambda_:.6f}")
print(f"μ (интенсивность обслуживания) = {mu:.6f}")
print(f"ρ (нагрузка на систему) = {a:.6f}")
print(f"P0 (вероятность пустой системы) = {P0:.6f}")
print(f"Pоч (вероятность ожидания) = {P_wait:.6f}")
print(f"Pзан (все каналы заняты) = {P_zan:.6f}")
print(f"Mоч (средняя длина очереди) = {Lq:.6f}")
print(f"MТР (среднее число заявок в системе) = {L:.6f}")
print(f"Mзан (среднее число занятых каналов) = {M_zan:.6f}")
print(f"Mсв (среднее число свободных каналов) = {M_sv:.6f}")
print(f"Tож (среднее время ожидания) = {Wq:.6f}")
print(f"Тоож (время ожидания всех заявок за единицу времени) = {Tooj:.6f}")
print(f"Tтр (среднее время пребывания в системе) = {W:.6f}")
print(f"A (абсолютная пропускная способность) = {A:.6f}")

k_max = N + 30
Pk = []
for k in range(0, k_max + 1):
    if k < N:
        pk = (a**k / math.factorial(k)) * P0
    else:
        pk = (a**k / (math.factorial(N) * (N**(k - N)))) * P0
    Pk.append(pk)

Pk = np.array(Pk)
Pk = Pk / Pk.sum()

plt.figure(figsize=(10, 5))
ks = np.arange(0, k_max + 1)
plt.bar(ks, Pk, color="#10b981")
plt.title(f"Распределение вероятностей состояний Pk\nСМО с ожиданием (M/M/{N}/∞)", fontsize=12)
plt.xlabel("Число заявок в системе (k)", fontsize=10)
plt.ylabel("Вероятность состояния P(k)", fontsize=10)
plt.grid(axis='y', linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig("result2.png", dpi=200)
plt.close()
