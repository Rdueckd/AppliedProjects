import numpy as np
import matplotlib.pyplot as plt
from ContDiff_v1 import sawtooth
import imageio.v2 as imageio

m = 22
x = np.linspace(0,2,2**m)
y = sawtooth(0.75,m,m)
n=25
for z in range(0,n):
    plt.style.use("dark_background")
    plt.figure(figsize=(8, 6))
    plt.xlim(0.5*z/n,2-z/n)
    plt.ylim(z/n,2.75)
    plt.plot(x, y, color="orange", linewidth=1)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(f"Iterations=m={m}, #points=2^{m}, $\lambda$ = 0.75,zoom={round(2/(2-z/n-0.5*z/n), 2)}", color="white")
    plt.grid(True)
    plt.savefig(f"Plot/Zoom/figure{z}.png", dpi=100)
    plt.close()



frames = [ imageio.imread(f"Plot/Zoom/figure{z}.png") for z in range(0,n) ]

imageio.mimsave("Plot/Zoom/zoom.gif", frames, duration=200, loop=0)
