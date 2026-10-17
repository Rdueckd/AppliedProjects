import numpy as np
import matplotlib.pyplot as plt
from ContDiff_v1 import sawtooth
from ContDiff_v1 import derive
import imageio.v2 as imageio
from PIL import Image

m = 20
t = m
x = np.linspace(0,2,2**m)
delta = 40

for k in range(1,int(delta*0.6)):
    lam = k/delta
    y = sawtooth(lam,m,t)

    plt.style.use("dark_background")
    plt.figure(figsize=(8, 6))
    plt.title(f"Iteration {t}, #points=2^{m}, $\lambda$ = {lam}")
    plt.xlim(0,2)
    plt.plot(x, y, color="orange", linewidth=1)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.savefig(f"Plot/JointDerivativeGif/figure{k}.png", dpi=100)
    plt.close()

    yprime = derive(y)

    plt.style.use("dark_background")
    plt.figure(figsize=(8, 6))
    plt.title("Derivative")
    plt.plot(x, yprime, color="orange", linewidth=1)
    plt.xlabel("x")
    plt.ylabel("y'")
    plt.grid(True)
    plt.savefig(f"Plot/JointDerivativeGif/figure{k}Derivative.png", dpi=100)
    plt.close()

    img1 = Image.open(f"Plot/JointDerivativeGif/figure{k}.png")
    img2 = Image.open(f"Plot/JointDerivativeGif/figure{k}Derivative.png")

    width, height = img1.size
    img2 = img2.resize((width, height))

    combined = Image.new("RGB", (2 * width, height))

    combined.paste(img1, (0, 0))           # top-left
    combined.paste(img2, (width, 0))       # top-right

    combined.save(f"Plot/JointDerivativeGif/combinedderivative{k}.png")


frames = [ imageio.imread(f"Plot/JointDerivativeGif/combinedderivative{k}.png") for k in range(1,int(delta*0.6)) ]

imageio.mimsave("Plot/JointDerivativeGif/Derivative.gif", frames, duration=800, loop=0)
