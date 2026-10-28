import fire as fire
import numpy as np
import matplotlib.pyplot as plt
from randomwalk import discretewalk, continuous2dwalk


# discretedir = Path("plots/discrete/distance")

def distdiscrete2d(nsteps):
    x = np.linspace(0,nsteps, nsteps+1, dtype=int)
    p,w,d = discretewalk(2,nsteps=nsteps)
    plt.plot(x,d, marker='o',linestyle='dashed')
    plt.grid(True)
    plt.title(f"Distance From Origin, 2-D Discrete {nsteps} Steps")
    plt.savefig(f"plots/discrete/2d/distance/2ddiscrete{nsteps}.png")

def discrete2d(nsteps):
    p, w, d = discretewalk(2, nsteps=nsteps)
    w = np.asarray(w)
    fig, ax = plt.subplots()

    for k in range(nsteps):
        ax.annotate("", xy=w[k + 1], xytext=w[k],
                    arrowprops=dict(arrowstyle="->", color="black", lw=1,
                                    shrinkA=4, shrinkB=4))

    ax.plot(w[:, 0], w[:, 1], 'o', ms=5, zorder=3)
    for k in range(nsteps + 1):
        ax.annotate(str(k), xy=w[k])

    ax.grid(True)
    ax.set_aspect('equal')
    ax.set_title(f"2-D Discrete Random Walk With {nsteps} Steps")
    fig.savefig(f"plots/discrete/2d/walks/2ddiscrete{nsteps}.png", bbox_inches='tight')
    plt.close(fig)

def discrete3d(nsteps):
    p, w, d = discretewalk(3, nsteps=nsteps)
    w = np.asarray(w)
    x, y, z = w.T
    dx, dy, dz = np.diff(w, axis=0).T

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.quiver(x[:-1], y[:-1], z[:-1], dx, dy, dz,
                arrow_length_ratio=0.2, color='gray', lw=1)
    ax.scatter(x, y, z, s=20, depthshade=False, zorder=3)

    for k, (xi, yi, zi) in enumerate(w):
        ax.text(xi, yi, zi, f" {k}", fontsize=8)

    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z')
    ax.set_aspect('equal')
    ax.set_title(f"3-D Discrete Random Walk With {nsteps} Steps")
    fig.savefig(f"plots/discrete/3d/walks/3ddiscrete{nsteps}.png", bbox_inches='tight')
    plt.close(fig)

def continuous2dplot(nsteps,dx):
    p, w, d = continuous2dwalk(nsteps,dx)
    w = np.asarray(w)
    fig, ax = plt.subplots()

    ax.plot(w[:, 0], w[:, 1], 'o-', markersize=2)

    ax.grid(True)
    ax.set_title(f"2-D Random Walk, steps={nsteps}, dx={dx}")
    fig.savefig(f"plots/continuous/2d/2dcont{nsteps}-{dx}.png", bbox_inches='tight')
    plt.close(fig)

if __name__ == "__main__":
    fire.Fire()
