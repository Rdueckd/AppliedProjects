import numpy as np

def dirchkern(a,b, N, res):
    x = np.linspace(a, b, res)

    Dn = np.sin((N+1/2)*x)/(np.sin(x/2)*2*np.pi)

    Dn[0] = (2*N+1) / (2*np.pi)
    return x, Dn


def dirchkernsum(a,b,N,res):
    x = np.linspace(a,b,res)
    Dn = np.ones(res)/2

    for n in range(0,N):
        Dn += np.cos(n*x)

    return x, Dn / np.pi
