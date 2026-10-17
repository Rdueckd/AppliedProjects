import numpy as np
import matplotlib.pyplot as plt
from ContDiff_v1 import sawtooth
from ContDiff_v1 import sawintegrate
import imageio.v2 as imageio
from PIL import Image

m = 20
t = m
x = np.linspace(0,2,2**m)
delta = 20
lam = 0.75

for k in range(1,delta+1):
    y = sawtooth(lam,m,k)

    plt.style.use("dark_background")
    plt.figure(figsize=(8, 6))
    plt.title(f"Iteration {k}, #points=2^{m}, $\lambda$ = {lam}")
    plt.xlim(0,2)
    plt.plot(x, y, color="orange", linewidth=1)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.savefig(f"Plot/JointIntegralGif/figure{k}.png", dpi=100)
    plt.close()

    yprime = sawintegrate(y)

    plt.style.use("dark_background")
    plt.figure(figsize=(8, 6))
    plt.title("Integral")
    plt.plot(x, yprime, color="orange", linewidth=1)
    plt.xlabel("x")
    plt.ylabel("y'")
    plt.grid(True)
    plt.savefig(f"Plot/JointIntegralGif/figure{k}Integral.png", dpi=100)
    plt.close()

    img1 = Image.open(f"Plot/JointIntegralGif/figure{k}.png")
    img2 = Image.open(f"Plot/JointIntegralGif/figure{k}Integral.png")

    width, height = img1.size
    img2 = img2.resize((width, height))

    combined = Image.new("RGB", (2 * width, height))

    combined.paste(img1, (0, 0))           # top-left
    combined.paste(img2, (width, 0))       # top-right

    combined.save(f"Plot/JointIntegralGif/combinedintegral{k}.png")


frames = [ imageio.imread(f"Plot/JointIntegralGif/combinedintegral{k}.png") for k in range(1,delta) ]

imageio.mimsave("Plot/JointIntegralGif/integral.gif", frames, duration=500, loop=0)
