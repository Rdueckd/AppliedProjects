
import numpy as np
import matplotlib.pyplot as plt
from ContDiff_v1 import sawtooth, haardecomp, derive

m = 20
t = m
for k in range(1,9):
    lam = k/8
    y = sawtooth(lam, m, t)
    lambdas = haardecomp(derive(y))

    diag = np.diag(lambdas)
    k = np.arange(len(diag))

    xpct = lam**k # expected
    err = diag - xpct

    #plt.style.use("dark_background")
    plt.figure(figsize=(14, 7))
    plt.title(f"Haar Decomposition of $f'(x)$, #points=2^{m}, $\lambda$ = {lam}", fontsize=25)

    plt.scatter(k, diag, color="orange", s=35, label="Haar")
    plt.scatter(k, xpct, color="cyan", s=30, marker="x",
                label=r"$\lambda^k$")

    for i, e in enumerate(err):
        plt.annotate(
            f"{e:+.2e}",
            (k[i], diag[i]),
            xytext=(6, 12 if i % 2 == 0 else -14),
            textcoords="offset points",
            fontsize=12,
            color="black"
        )

    plt.xlim(0, 20)
    plt.xticks(np.arange(0, 21, 1))
    plt.xlabel("k", fontsize=20)
    plt.ylabel(r"$\lambda_{k,k}$", fontsize=20)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(f"Plot/HaarDecomp/figure{int(lam*8)}Haar.png", dpi=300)
    plt.close()
