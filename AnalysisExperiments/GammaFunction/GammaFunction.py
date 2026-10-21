
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma
from PIL import Image
import os

def f(t, r, lam):
    return (lam**r / gamma(r)) * t**(r-1) * np.exp(-lam*t)

lam = 0.5
m = 12
x = np.linspace(0, 40, 2**m)

r_values = [1, 2, 4, 10]
colors = ["#2563EB", "#0D9488", "#9333EA", "#EA580C"]

for r, color in zip(r_values, colors):
    y = f(x, r, lam)

    plt.figure(figsize=(8, 6))
    ax = plt.gca()

    ax.set_facecolor("#FAFAFA")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#AAAAAA")
    ax.spines["bottom"].set_color("#AAAAAA")

    plt.plot(x, y, color=color, linewidth=2.5)
    plt.fill_between(x, y, color=color, alpha=0.12)

    mode = max(0, (r - 1) / lam)
    peak = f(mode, r, lam)

    plt.scatter(mode, peak, color=color, s=55, zorder=5)
    plt.vlines(mode, 0, peak, colors=color,
               linestyles="--", alpha=0.5)

    plt.title(
        f"Gamma Distribution ($r={r}$, $\\lambda={lam}$)",
        fontsize=16, fontweight="bold", pad=18
    )
    plt.xlim(0, 40)
    plt.ylim(0, max(y) * 1.2)

    plt.xlabel("t", fontsize=13)
    plt.ylabel(r"$f_r(t)$", fontsize=13)

    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.25)
    plt.tight_layout()

    plt.savefig(f"Plot/figure{r}.png", dpi=200)
    plt.close()


img1 = Image.open("Plot/figure1.png")
img2 = Image.open("Plot/figure2.png")
img4 = Image.open("Plot/figure4.png")
img10 = Image.open("Plot/figure10.png")

width, height = img1.size
img2 = img2.resize((width, height))
img4 = img4.resize((width, height))
img10 = img10.resize((width, height))

combined = Image.new("RGB", (2 * width, 2 * height), "white")

combined.paste(img1, (0, 0))           # top left
combined.paste(img2, (width, 0))       # top right
combined.paste(img4, (0, height))      # bottom left
combined.paste(img10, (width, height))  # bottom right

combined.save("Plot/combined.png", dpi=(200, 200))
