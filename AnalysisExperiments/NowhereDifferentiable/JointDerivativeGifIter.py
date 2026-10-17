import numpy as np
import matplotlib.pyplot as plt
from ContDiff_v1 import sawtooth
from ContDiff_v1 import derive
import imageio.v2 as imageio
from PIL import Image

m = 20
# t = m
x = np.linspace(0,2,2**m)
lam = 0.5

for k in range(0,20):
    y = sawtooth(lam,m,k)

    plt.style.use("dark_background")
    plt.figure(figsize=(8, 6))
    plt.title(f"Iteration {k}, #points=2^{m}, $\lambda$ = {lam}")
    plt.xlim(0,2)
    plt.plot(x, y, color="orange", linewidth=1)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.savefig(f"Plot/JointDerivativeGifIter/figure{k}.png", dpi=100)
    plt.close()

    yprime = derive(y)

    plt.style.use("dark_background")
    plt.figure(figsize=(8, 6))
    plt.title("Derivative")
    plt.plot(x, yprime, color="orange", linewidth=1)
    plt.xlabel("x")
    plt.ylabel("y'")
    plt.grid(True)
    plt.savefig(f"Plot/JointDerivativeGifIter/figure{k}Derivative.png", dpi=100)
    plt.close()

    img1 = Image.open(f"Plot/JointDerivativeGifIter/figure{k}.png")
    img2 = Image.open(f"Plot/JointDerivativeGifIter/figure{k}Derivative.png")

    width, height = img1.size
    img2 = img2.resize((width, height))

    combined = Image.new("RGB", (2 * width, height))

    combined.paste(img1, (0, 0))           # top-left
    combined.paste(img2, (width, 0))       # top-right

    combined.save(f"Plot/JointDerivativeGifIter/combinedderivative{k}.png")


frames = [ imageio.imread(f"Plot/JointDerivativeGifIter/combinedderivative{k}.png") for k in range(1,20) ]

imageio.mimsave("Plot/JointDerivativeGifIter/DerivativeIter.gif", frames, duration=800, loop=0)
