import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

lambdas = {
    '13': 2, '15': 4,
    '21': 3, '24': 5, '26': 1,
    '35': 6,
    '43': 2, '47': 4,
    '54': 3,
    '67': 5,
    '72': 2
}

def get_derivatives(P, t, lam):
    P1, P2, P3, P4, P5, P6, P7 = P
    
    # Система уравнений Колмогорова согласно графу
    dP1dt = -(lam['13'] + lam['15'])*P1 + lam['21']*P2
    dP2dt = -(lam['21'] + lam['24'] + lam['26'])*P2 + lam['72']*P7
    dP3dt = -lam['35']*P3 + lam['13']*P1 + lam['43']*P4
    dP4dt = -(lam['43'] + lam['47'])*P4 + lam['24']*P2 + lam['54']*P5
    dP5dt = -lam['54']*P5 + lam['15']*P1 + lam['35']*P3
    dP6dt = -lam['67']*P6 + lam['26']*P2
    dP7dt = -lam['72']*P7 + lam['47']*P4 + lam['67']*P6
    
    return [dP1dt, dP2dt, dP3dt, dP4dt, dP5dt, dP6dt, dP7dt]

P0 = [1, 0, 0, 0, 0, 0, 0]
time = np.linspace(0, 3, 1000)

# Решение исходной системы
sol_orig = odeint(get_derivatives, P0, time, args=(lambdas,))

plt.figure(figsize=(10, 6))
for i in range(7):
    plt.plot(time, sol_orig[:, i], label=f'P{i+1}')
plt.title('Вероятности состояний (Исходная система)')
plt.xlabel('Время, t')
plt.ylabel('Вероятность, P(t)')
plt.legend()
plt.grid(True)
plt.savefig('graph_1.png')
plt.close()

# Измененная система: увеличим lambda_13 в 5 раз
lambdas_mod = lambdas.copy()
lambdas_mod['13'] *= 5

sol_mod = odeint(get_derivatives, P0, time, args=(lambdas_mod,))

plt.figure(figsize=(10, 6))
for i in range(7):
    plt.plot(time, sol_mod[:, i], label=f'P{i+1}')
plt.title(f'Вероятности состояний (С модифицированной lambda_13 = {lambdas_mod["13"]})')
plt.xlabel('Время, t')
plt.ylabel('Вероятность, P(t)')
plt.legend()
plt.grid(True)
plt.savefig('graph_2.png')
plt.close()
