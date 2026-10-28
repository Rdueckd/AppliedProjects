import numpy as np

def discretewalk(dim, nsteps):
    dirs = np.zeros((nsteps+1,dim))
    L = np.random.randint(dim, size=nsteps)
    S = np.random.default_rng().choice([-1,1], size=nsteps)
    for k in range(1,nsteps+1):
        xk = L[k-1]
        dirs[k][xk] = S[k-1]
    walk = np.cumsum(dirs,axis=0)
    dists = np.sqrt(np.sum(np.reshape(walk.flatten()*walk.flatten(), (nsteps+1,dim)),axis=1))
    return dirs, walk, dists


def continuous2dwalk(nsteps,dx):
    L = np.random.random_sample(nsteps)*2*np.pi
    dirs = np.zeros((2,nsteps))
    dirs[0] = np.cos(L)
    dirs[1] = np.sin(L)
    dirs = np.transpose(dirs)
    walk = np.cumsum(dx*np.insert(dirs,0,0,axis=0),axis=0) # insert a point for zero
    dists = np.linalg.norm(walk, axis=1)
    return dirs, walk, dists
