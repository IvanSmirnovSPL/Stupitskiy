from support import InitParams
import numpy as np
from numpy.typing import NDArray
from matplotlib import pyplot as plt


def calc_init_r(params: InitParams):
    r = np.zeros(params.N + 1)
    r[0] = params.a
    for i in range(1, params.N + 1):
        r[i] = np.sqrt(r[i - 1] ** 2 + (1 - params.a ** 2) / params.N)
    return r


def calculate(params: InitParams):
    u = np.zeros((params.time_iter, params.N + 1))
    r = np.zeros((params.time_iter, params.N + 1))
    rho = np.zeros((params.time_iter, params.N))
    p = np.zeros((params.time_iter, params.N))

    u[0] = np.ones_like(u[0]) * params.U
    r[0] = calc_init_r(params)
    rho[0] = np.ones_like(rho[0])
    p[0] = np.ones_like(p[0]) / params.gamma

    for n in range(1, params.time_iter):
        u[n] = update_u(u=u[n - 1], r=r[n - 1], p=p[n - 1], params=params)
        r[n] = update_r(r=r[n - 1], u=u[n - 1], params=params)
        rho[n] = update_rho(r=r[n], params=params)
        p[n] = update_p(rho=rho[n], params=params)

    #times = [0, 4e-4, 8e-4, 1.2e-3, 1.6e-3, 2e-3, 2.4e-3, 2.8e-3]
    times = [0, 0.04, 0.08, 0.12, 0.16, 0.2]
    nums = [int(_t / params.dt) for _t in times]

    fig = plt.figure(figsize=(30, 15))
    ax = fig.subplots(1, 3)

    for idx, _n in enumerate(nums):
        ax[1].plot(r[_n], u[_n], '-', label=f'{"%.1e" % times[idx]}')
        ax[1].legend()
        ax[1].grid(True)
        ax[1].set_title('u')

        ax[2].plot(r[_n][:-1], p[_n], '-', label=f'{"%.1e" % times[idx]}')
        ax[2].legend()
        ax[2].grid(True)
        ax[2].set_title('p')

        ax[0].plot(r[_n][:-1], rho[_n], '-', label=f'{"%.1e" % times[idx]}')
        ax[0].legend()
        ax[0].grid(True)
        ax[0].set_title(r'$\rho$')

    fig.suptitle(f'$a_0 = {params.a}, U_0 = {params.U}$')
    plt.savefig(str(params.path / f'a_{params.a}, U_{params.U}.png'))




def update_u(u: NDArray, r: NDArray, p: NDArray, params: InitParams):
    res = np.zeros(params.N + 1)
    res[0] = u[0] - (params.dt / params.m) * r[-1]**2 * p[0]
    for j in range(1, params.N):
        res[j] = u[j] - (params.dt / params.m) * r[j]**2 * (p[j] - p[j - 1])
    res[-1] = u[-1] + (params.dt / params.m) * r[-1]**2 * p[-1]
    return res


def update_r(r: NDArray, u: NDArray, params: InitParams):
    res = np.zeros(params.N + 1)
    for j in range(res.size):
        res[j] = r[j] + u[j] * params.dt
    return res


def update_rho(r: NDArray, params: InitParams):
    res = np.zeros(params.N)
    for j in range(params.N):
        res[j] = 2 * params.m / (r[j + 1] ** 2 - r[j] ** 2)
    return res


def update_p(rho: NDArray, params: InitParams):
    res = np.zeros(params.N)
    for j in range(params.N):
        res[j] = (1 / params.gamma) * (rho[j]) ** params.gamma
    return res
