import numpy as np
from scipy import ndimage
H=W=192; yy,xx=np.mgrid[:H,:W]
c=np.load('pre0_ckpt.npz'); A=c['A']
lab,k=ndimage.label(ndimage.gaussian_filter(A[0],1)>0.3)
for name,lo,hi in (('cog',0,12),('rod',14,26),('worm',30,99)):
    best=None
    for i in range(1,k+1):
        m=lab==i; ys,xs=np.nonzero(m); ext=int(max(np.ptp(ys),np.ptp(xs)))
        if ys.min()<30 or ys.max()>H-31 or xs.min()<30 or xs.max()>W-31 or not(lo<=ext<hi): continue
        best=(i,ys.mean(),xs.mean(),ext); break
    if best is None: print('none',name); continue
    i,cy,cx,ext=best
    body=ndimage.binary_dilation(lab==i, iterations=12)   # core plus its shell
    Anew=np.where(body[None],A,0)
    Anew=np.roll(Anew,(int(H//2-cy),int(W//2-cx)),(1,2))
    np.savez_compressed(f'founder_{name}.npz',A=Anew,F=np.full((H,W),1.0),W=np.zeros((H,W)),t=0.0)
    print(name,'ext',ext,'matter',Anew.sum())
