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
    # plt.plot(r[0][:-1], p[0], '-o', label='0')
    # plt.plot(r[20][:-1], p[20], '-o', label='20')
    # plt.plot(r[40][:-1], p[40], '-o', label='40')
    # plt.plot(r[-1][:-1], p[-1], '-o', label='-1')
    plt.plot(range(params.N + 1), r[0], 'o', label='0')
    plt.plot(range(params.N + 1), r[1 * r.shape[0] // 4], 'o', label='1 / 4')
    plt.plot(range(params.N + 1), r[3 * r.shape[0] // 4], 'o', label='3 / 4')
    plt.plot(range(params.N + 1), r[-1], 'o', label='-1')
    plt.legend()
    plt.grid(True)
    plt.show()


def update_u(u: NDArray, r: NDArray, p: NDArray, params: InitParams):
    res = np.zeros(params.N + 1)
    res[0] = 0
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
