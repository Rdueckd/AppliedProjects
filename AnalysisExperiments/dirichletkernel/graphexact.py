import matplotlib.pyplot as plt
from dirichletkernel import dirchkern

for N in [5,10,20]:
    y = dirchkern(-1,1,N,1 << 15)
