import numpy as np
from scipy import ndimage
H=W=192
yy,xx=np.mgrid[:H,:W]
for sd in (0,1):
    c=np.load(f'pre{sd}_ckpt.npz'); A=c['A']
    lab,k=ndimage.label(ndimage.gaussian_filter(A[0],1)>0.3)
    cands=[]
    for i in range(1,k+1):
        m=lab==i; area=m.sum(); ys,xs=np.nonzero(m)
        if ys.min()<25 or ys.max()>H-26 or xs.min()<25 or xs.max()>W-26: continue
        cands.append((i,area,int(max(np.ptp(ys),np.ptp(xs))),ys.mean(),xs.mean()))
    cands.sort(key=lambda r:r[2])
    cog=[r for r in cands if r[2]<12]; worm=[r for r in cands if r[2]>30]
    print(sd,'cogs',len(cog),'worms',len(worm))
    for name,r,rad in (('cog',cog[len(cog)//2],18),('worm',worm[-1],int(worm[-1][2]*0.6+10))):
        d=np.hypot(yy-r[3],xx-r[4]); mask=d<rad
        np.savez_compressed(f'cut_{name}{sd}.npz',A=c['A'],F=c['F'],W=c['W'],t=c['t'],mask=mask,label=(lab==r[0]),cy=r[3],cx=r[4],rad=rad)
        print(name,'ext',r[2],'center',round(r[3]),round(r[4]),'rad',rad)
