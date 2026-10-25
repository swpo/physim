import numpy as np
from scipy import ndimage
Fs=np.linspace(0.018,0.042,9); Ks=np.linspace(0.050,0.066,9)
FF,KK=np.meshgrid(Fs,Ks,indexing='ij'); FF=FF.ravel()[:,None,None]; KK=KK.ravel()[:,None,None]
n=FF.shape[0]; H=96; rng=np.random.default_rng(0)
u=np.ones((n,H,H)); v=np.zeros((n,H,H))
for k in range(30):
    y,x=rng.integers(0,H,2); u[:,y-2:y+3,x-2:x+3]=0.5; v[:,y-2:y+3,x-2:x+3]=0.25
def lap(a): return np.roll(a,1,1)+np.roll(a,-1,1)+np.roll(a,1,2)+np.roll(a,-1,2)-4*a
masks=[]
for t in range(12001):
    g=u*v*v; u+=0.2*lap(u)-g+FF*(1-u); v+=0.1*lap(v)+g-(FF+KK)*v
    if t>=6000 and t%500==0: masks.append(v>0.2)
M=np.array(masks)  # time, n
flip=(M[1:]!=M[:-1]).mean(axis=(0,2,3)); occ=M[-1].mean(axis=(1,2))
cnt=[ndimage.label(M[-1][i])[1] for i in range(n)]
for i in range(n):
    if occ[i]>0.01: print(f"F={FF[i,0,0]:.4f} K={KK[i,0,0]:.4f} occ={occ[i]:.2f} flip500={flip[i]:.3f} n={cnt[i]}")
