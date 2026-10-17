import numpy as np
import matplotlib.pyplot as plt
from ContDiff_v1 import sawtooth
from ContDiff_v1 import derive
import imageio.v2 as imageio
from PIL import Image

m = 20
t = m
x = np.linspace(0,2,2**m)
for lam in [0.25,0.375]:
    y = sawtooth(lam,m,t)

    plt.style.use("dark_background")
    plt.figure(figsize=(8, 6))
    plt.title(f"Iteration {t}, #points=2^{m}, $\lambda$ = {lam}")
    plt.xlim(0,2)
    plt.plot(x, y, color="orange", linewidth=1)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.savefig(f"Plot/JointDerivatives/figure{int(lam*8)}.png", dpi=100)
    plt.close()

    yprime = derive(y)

    plt.style.use("dark_background")
    plt.figure(figsize=(8, 6))
    plt.title(f"Derivative")
    plt.plot(x, yprime, color="orange", linewidth=1)
    plt.xlabel("x")
    plt.ylabel("y'")
    plt.grid(True)
    plt.savefig(f"Plot/JointDerivatives/figure{int(lam*8)}Derivative.png", dpi=100)
    plt.close()


img1 = Image.open("Plot/JointDerivatives/figure2.png")
img2 = Image.open("Plot/JointDerivatives/figure3.png")
img4 = Image.open("Plot/JointDerivatives/figure2Derivative.png")
img10 = Image.open("Plot/JointDerivatives/figure3Derivative.png")

width, height = img1.size
img2 = img2.resize((width, height))
img4 = img4.resize((width, height))
img10 = img10.resize((width, height))

combined = Image.new("RGB", (2 * width, 2 * height))

# Paste images into the canvas
combined.paste(img1, (0, 0))           # top-left
combined.paste(img4, (width, 0))       # top-right
combined.paste(img2, (0, height))      # bottom-left
combined.paste(img10, (width, height))  # bottom-right

combined.save("Plot/JointDerivatives/combinedderivative.png")
