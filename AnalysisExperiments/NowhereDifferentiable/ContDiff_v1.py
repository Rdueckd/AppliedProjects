import numpy as np



def sawtooth(h, n, iterations):
    N = 1 << n
    y = 1 - np.abs(np.linspace(-1, 1, N))

    for k in range(1, iterations):
        m = N >> k
        y_k = h**k * (1 - np.abs(np.linspace(-1, 1, m)))
        y.reshape(-1, m)[:] += y_k

    y[-1] = 0
    return y

def derive(y):
    yprime = np.gradient(y, 2 / (len(y) - 1))

    return yprime

def sawintegrate(y):
    yint = np.cumsum(y)
    yint *= 2 / (len(yint) - 1)
    yint[0] = 0
    return yint


def haardecomp(y):
    m = len(y).bit_length()-1 # y must be length 2^n
    Hk = np.ones(len(y))
    Hk[1 << m-1:] -= 2
    lambdas = np.zeros((m,m))
    r = 1

    for n in range(0,m):
        yH = y.reshape(-1,1 << m-n) * Hk[::r]
        for k in range(0, n+1):
            lambdas[n,k] = np.sum(yH[k]) / (2**m-1)
        r = r << 1
    return lambdas
