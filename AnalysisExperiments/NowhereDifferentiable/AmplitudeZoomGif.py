import numpy as np
import matplotlib.pyplot as plt
from ContDiff_v1 import sawtooth
import imageio.v2 as imageio


m = 20
x = np.linspace(0,2,2**m)
for p in range(1,24,1):
    y = sawtooth(p/40,m,m)

    plt.style.use("dark_background")
    plt.figure(figsize=(8, 6))
    plt.xlim(0.5,1)
    plt.ylim(0.6,2)
    plt.plot(x, y, color="orange", linewidth=1)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(f"Iterations=m={m},#points=2^{m}, $\lambda = {p/40}$", color="white")
    plt.grid(True)
    plt.savefig(f"Plot/AmplitudeZoom/figure{p}.png", dpi=100)
    plt.close()



frames = [ imageio.imread(f"Plot/AmplitudeZoom/figure{p}.png") for p in range(2,21,1) ]

imageio.mimsave("Plot/AmplitudeZoom/amplitudezoom.gif", frames, duration=200, loop=0)
