import math
import numpy as np
import matplotlib.pyplot as plt

m = 5          # последняя цифра года
N = 6          # число каналов обслуживания
Nn = 6         # номер по списку

lambda_ = 10 * m / (N * Nn)
mu = 5 * m / (N * Nn)
a = lambda_ / mu  # нагрузка

den = sum([a**k / math.factorial(k) for k in range(0, N + 1)])
P0 = 1.0 / den
Pk = [(a**k / math.factorial(k)) * P0 for k in range(0, N + 1)]

P_reject = Pk[-1]                                 # вероятность отказа
M_zan = sum([k * Pk[k] for k in range(0, N + 1)]) # среднее число занятых каналов
M_sv = N - M_zan
Q_rel = 1.0 - P_reject
A_abs = lambda_ * Q_rel
Kz = M_zan / N

Pk_sum = sum(Pk)
Pk.append(Pk_sum)
labels = [str(k) for k in range(0, N + 1)] + ["ΣP(k)"]

print("Задание 1 — СМО с отказами:".format(N, N))
print("λ = {:.6f}, μ = {:.6f}, a = {:.3f}".format(lambda_, mu, a))
print(f"Вероятность отказа Pотк = {P_reject:.6f}")
print(f"Среднее число занятых каналов Mзан = {M_zan:.6f}")
print(f"Среднее число свободных каналов Mсв = {M_sv:.6f}")
print(f"Относительная пропускная способность Q = {Q_rel:.6f}")
print(f"Абсолютная пропускная способность A = {A_abs:.6f}")
print(f"Коэффициент занятости Kз = {Kz:.6f}")
print(f"ΣP(k) = {Pk_sum:.6f}")

plt.figure(figsize=(9, 5))
bars = plt.bar(labels, Pk, color="#3b82f6")
bars[-1].set_color("#f97316")
plt.title(f"Распределение вероятностей состояний Pk\nСМО с отказами", fontsize=12)
plt.xlabel("Число занятых каналов (k)", fontsize=10)
plt.ylabel("Вероятность состояния P(k)", fontsize=10)
plt.grid(axis='y', linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig("result1.png", dpi=200)
plt.close()
