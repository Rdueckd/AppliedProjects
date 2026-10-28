import matplotlib.pyplot as plt
from dirichletkernel import dirchkern
import plotstyle

for N in [5,10,20]:
    x, y = dirchkern(-1,1,N,1 << 15)
    def make():
        fig, ax = plotstyle.figure()
        ax.title(f"$D_n$ with N={N}")
        ax.plot(x, y)
        return fig

    plotstyle.render(make, f"plots/exact/{N}", formats=("png",))



# for N in [5,10,20]:
#     for name in []
