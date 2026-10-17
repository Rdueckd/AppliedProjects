import numpy as np
import matplotlib.pyplot as plt
from ContDiff_v1 import sawtooth
import imageio.v2 as imageio
from PIL import Image

lam = 0.5
m = 20
x = np.linspace(0,2,2**m)
for t in [1,2,4,10]:
    y = sawtooth(lam,m,t)

    # plt.style.use("dark_background")
    plt.figure(figsize=(8, 6))
    plt.title(f"Iteration {t}, #points=2^{m}, $\lambda$ = {lam}")
    plt.xlim(0,2)
    plt.plot(x, y, color="orange", linewidth=1)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.savefig(f"Plot/Joint/figure{t}.png", dpi=200)
    plt.close()


img1 = Image.open("Plot/Joint/figure1.png")
img2 = Image.open("Plot/Joint/figure2.png")
img4 = Image.open("Plot/Joint/figure4.png")
img10 = Image.open("Plot/Joint/figure10.png")

width, height = img1.size
img2 = img2.resize((width, height))
img4 = img4.resize((width, height))
img10 = img10.resize((width, height))

combined = Image.new("RGB", (2 * width, 2 * height))

# Paste images into the canvas
combined.paste(img1, (0, 0))           # top-left
combined.paste(img2, (width, 0))       # top-right
combined.paste(img4, (0, height))      # bottom-left
combined.paste(img10, (width, height))  # bottom-right

combined.save("Plot/Joint/combined.png")
