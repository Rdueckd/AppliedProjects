
import numpy as np
import matplotlib.pyplot as plt
from ContDiff_v1 import sawtooth
import imageio.v2 as imageio
from pathlib import Path

m = 22
h = 0.5
n = 150

x = np.linspace(0, 2, 2**m)
y = sawtooth(h, m, m)

# Zoom target
x0 = 2/3

# Set False to display the original curve
remove_trend = True

if remove_trend:
    y = y - 1.6 * (x - x0)

y0 = np.interp(x0, x, y)

# Number of successive 4x zooms
levels = 5

# Initial window half-widths
initial_width = 1/3
initial_height = 1.0

outdir = Path("Plot/Zoom")
outdir.mkdir(parents=True, exist_ok=True)

plt.style.use("dark_background")

with imageio.get_writer(
    outdir / "zoom.gif",
    mode="I",
    duration=0.06,
    loop=0
) as writer:

    for z in range(n):
        t = z / (n - 1)
        level = levels * t

        # Horizontal and vertical scaling
        x_width = initial_width / (4**level)
        y_height = initial_height * h**(2*level)

        xmin = x0 - x_width
        xmax = x0 + x_width

        # Plot only the visible data
        i0 = np.searchsorted(x, xmin)
        i1 = np.searchsorted(x, xmax)

        fig, ax = plt.subplots(figsize=(8, 6))

        ax.plot(
            x[i0:i1],
            y[i0:i1],
            color="orange",
            linewidth=1
        )

        ax.set_xlim(xmin, xmax)
        ax.set_ylim(y0-y_height, y0+y_height)

        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(
            f"Blancmange Curve, h={h}\n"
            f"x₀=1/3, Zoom={4**level:.1f}x"
        )
        ax.grid(True, alpha=0.3)

        filename = outdir / f"figure{z:03d}.png"
        fig.savefig(filename, dpi=100)
        plt.close(fig)

        writer.append_data(imageio.imread(filename))


print("Working directory:", Path.cwd())
print("GIF location:", (outdir / "zoom.gif").resolve())
print("GIF exists:", (outdir / "zoom.gif").exists())
