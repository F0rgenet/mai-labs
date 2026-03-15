import numpy as np
import matplotlib.pyplot as plt
import os

if not os.path.exists('images'):
    os.makedirs('images')

R_target = 0.6          # Загрузка системы (P)
b = 0.121               # Среднее время обслуживания (mu или t_obs)
C = np.array([4, 3, 2, 1]) 
M = 4  # Количество потоков


def get_metrics(rho_sys):
    lam = rho_sys / (4 * b)
    lams = np.array([lam] * M)
    rhos = lams * b
    R_k = np.cumsum(rhos)
    R_total = R_k[-1]
    b2 = 2 * (b**2)

    W0 = np.sum(lams * b2) / 2
    
    # FIFO
    W_fifo_val = W0 / (1 - R_total)
    W_fifo = np.array([W_fifo_val] * M)
    L_fifo = np.sum(lams * C * W_fifo)
    
    # Относительные приоритеты (PR)
    W_rel = []
    for k in range(M):
        R_prev = R_k[k-1] if k > 0 else 0
        R_curr = R_k[k]
        wk = W0 / ((1 - R_prev) * (1 - R_curr))
        W_rel.append(wk)
    W_rel = np.array(W_rel)
    L_rel = np.sum(lams * C * W_rel)
    
    # Абсолютные приоритеты (PA) - Preemptive Resume
    W_abs = []
    for k in range(M):
        R_prev = R_k[k-1] if k > 0 else 0
        R_curr = R_k[k]
        
        W0_k = np.sum(lams[:k+1] * b2) / 2 # b2 одинаков
        
        term1 = b
        term2 = W0_k / (1 - R_curr)
        T_k = (term1 + term2) / (1 - R_prev)
        
        W_abs.append(T_k - b)
    W_abs = np.array(W_abs)
    L_abs = np.sum(lams * C * W_abs)
    
    M_abs = 2
    W_mix = []
    for k in range(M_abs):
        W_mix.append(W_abs[k])

    R_abs_total = R_k[M_abs-1]
    for k in range(M_abs, M):
        R_prev = R_k[k-1]
        R_curr = R_k[k]
        wk = W0 / ((1 - R_abs_total) * (1 - R_prev) * (1 - R_curr))
        W_mix.append(wk)
    W_mix = np.array(W_mix)
    L_mix = np.sum(lams * C * W_mix)
    
    # Среднее время ожидания по системе
    W_avg_sys = lambda W: np.sum(lams * W) / np.sum(lams)
    
    return {
        'L': [L_fifo, L_rel, L_abs, L_mix],
        'W_avg': [W_avg_sys(W_fifo), W_avg_sys(W_rel), W_avg_sys(W_abs), W_avg_sys(W_mix)]
    }

loads = np.linspace(0.1, 0.9, 50)
res_L = []
res_W = []

for r in loads:
    m = get_metrics(r)
    res_L.append(m['L'])
    res_W.append(m['W_avg'])

res_L = np.array(res_L)
res_W = np.array(res_W)


plt.figure(figsize=(10, 6))
labels = ['FIFO (Без приоритетов)', 'Относительные приоритеты', 'Абсолютные приоритеты', 'Смешанные приоритеты']
styles = ['--', '-.', '-', ':']

for i in range(4):
    plt.plot(loads, res_L[:, i], label=labels[i], linestyle=styles[i])

plt.title('Зависимость суммарных потерь от загрузки системы')
plt.xlabel('Коэффициент загрузки системы, R')
plt.ylabel('Суммарные потери, L (у.е.)')
plt.legend()
plt.grid(True)
plt.savefig('images/graph_losses.png')
plt.close()

plt.figure(figsize=(10, 6))
for i in range(4):
    plt.plot(loads, res_W[:, i], label=labels[i], linestyle=styles[i])

plt.title('Зависимость среднего времени ожидания от загрузки')
plt.xlabel('Коэффициент загрузки системы, R')
plt.ylabel('Среднее время ожидания, W (сек)')
plt.legend()
plt.grid(True)
plt.savefig('images/graph_waits.png')
plt.close()

final_m = get_metrics(0.6)
print(f"Results for R=0.6:")
print(f"L_FIFO: {final_m['L'][0]:.4f}")
print(f"L_REL:  {final_m['L'][1]:.4f}")
print(f"L_ABS:  {final_m['L'][2]:.4f}")
print(f"L_MIX:  {final_m['L'][3]:.4f}")
