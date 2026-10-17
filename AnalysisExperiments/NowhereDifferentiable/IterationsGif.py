import numpy as np
import matplotlib.pyplot as plt
from ContDiff_v1 import sawtooth
import imageio.v2 as imageio


m = 20
x = np.linspace(0,2,2**m)
for t in range(1,15):
    y = sawtooth(0.75,m,t)

    plt.style.use("dark_background")
    plt.figure(figsize=(8, 6))
    plt.xlim(0,2)
    plt.ylim(0,3)
    plt.plot(x, y, color="orange", linewidth=1)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(f"Iteration {t}, #points=2^{m}, $\lambda = 0.75$", color="white")
    plt.grid(True)
    plt.savefig(f"Plot/Iterations/figure{t}.png", dpi=100)
    plt.close()



frames = [ imageio.imread(f"Plot/Iterations/figure{t}.png") for t in range(1,15) ]

imageio.mimsave("Plot/Iterations/iterations.gif", frames, duration=200, loop=0)
