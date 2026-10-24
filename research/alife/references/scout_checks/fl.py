import numpy as np, sys
from rt import rt
seed=int(sys.argv[1]) if len(sys.argv)>1 else 0
rng=np.random.default_rng(seed)
X=128;k=10;dt=0.2;s=0.65;theta=2.0
R=rng.uniform(2,25); r=rng.uniform(.2,1,k); m=rng.uniform(.05,.5,k); sg=rng.uniform(.001,.18,k)
h=rng.uniform(.01,1,k); a=rng.uniform(0,1,(k,3)); b=rng.uniform(.001,1,(k,3)); w=rng.uniform(.01,.5,(k,3))
yy,xx=np.mgrid[-X//2:X//2,-X//2:X//2]; dist=np.hypot(xx,yy)
fK=[]
for i in range(k):
    D=dist/((R+15)*r[i])
    K=(1/(1+np.exp((D-1)*10)))*(b[i]*np.exp(-(D[...,None]-a[i])**2/w[i])).sum(-1)
    K/=K.sum(); fK.append(np.fft.fft2(np.fft.ifftshift(K)))
fK=np.array(fK)
def grad(f):  # sobel-equivalent (unnormalized, x8) periodic
    gx=(np.roll(f,-1,0)-np.roll(f,1,0)); gy=(np.roll(f,-1,1)-np.roll(f,1,1))
    sm=lambda g,ax: np.roll(g,1,ax)+2*g+np.roll(g,-1,ax)
    return np.stack([sm(gx,1),sm(gy,0)],-1)
A=np.zeros((X,X)); A[44:84,44:84]=rng.random((40,40))
M0=A.sum()
for t in range(300):
    fA=np.fft.fft2(A)
    U=np.real(np.fft.ifft2(fK*fA[None]))
    G=2*np.exp(-((U-m[:,None,None])/sg[:,None,None])**2/2)-1
    U=(h[:,None,None]*G).sum(0)
    alpha=np.clip((A/theta)**2,0,1)[...,None]
    F=(1-alpha)*grad(U)-alpha*grad(A)
    A=rt(A,F,dt,s,5)
# localization: fraction of mass within bounding box of top cells
occ=(A>0.01).mean(); print('seed',seed,'R',round(R,1),'mass err',abs(A.sum()-M0)/M0,'occupied frac',round(occ,3),'max',round(A.max(),2))
