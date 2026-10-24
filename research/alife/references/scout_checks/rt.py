import numpy as np
def rt(A, F, dt=0.2, s=0.65, dd=5):
    # A: (X,Y) mass, F: (X,Y,2) flow; torus. returns new A (mass-conserving)
    X,Y=A.shape
    ma=dd-s
    D=np.clip(dt*F,-ma,ma)                       # displacement of each source cell
    out=np.zeros_like(A)
    for dx in range(-dd,dd+1):
        for dy in range(-dd,dd+1):
            # mass from source cell (i,j) to target (i+dx,j+dy): overlap of square [mu-s,mu+s] with cell
            ox=np.clip(0.5+s-np.abs(D[...,0]-dx),0,min(1,2*s))
            oy=np.clip(0.5+s-np.abs(D[...,1]-dy),0,min(1,2*s))
            out+=np.roll(A*ox*oy/(4*s*s),(dx,dy),axis=(0,1))
    return out
rng=np.random.default_rng(0)
A=rng.random((64,64)); F=rng.normal(0,8,(64,64,2))
B=rt(A,F); print(A.sum(),B.sum(), abs(A.sum()-B.sum())/A.sum())
