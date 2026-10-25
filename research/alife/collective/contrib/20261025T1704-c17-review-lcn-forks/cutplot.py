import numpy as np, sys
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
rows=[(n,sd) for sd in map(int,sys.argv[1:]) for n in ('cog','worm')]
fig,ax=plt.subplots(len(rows),6,figsize=(19,3.2*len(rows)))
H=W=192; yy,xx=np.mgrid[:H,:W]
out=[]
for r,(n,sd) in enumerate(rows):
    c=np.load(f'cut_{n}{sd}.npz'); m=c['mask']; cy,cx,rad=float(c['cy']),float(c['cx']),float(c['rad'])
    d=np.hypot(yy-cy,xx-cx); ann=(d>=rad)&(d<rad+25)
    cu=np.load(f'cutrun_{n}{sd}_snaps.npz'); fe=np.load(f'fed{sd}_snaps.npz')
    Xc=cu['X'].astype(np.float32); Xf=fe['X'].astype(np.float32)[:len(Xc)]; t=cu['t']
    A0=c['A'][:, m].sum(); An0=c['A'][:, ann].sum()
    ic=Xc[:,:2][:,:,m].sum((1,2))/A0; iff=Xf[:,:2][:,:,m].sum((1,2))/A0
    nc=Xc[:,:2][:,:,ann].sum((1,2))/An0; nf=Xf[:,:2][:,:,ann].sum((1,2))/An0
    for j,(X,i,lab) in enumerate([(Xc,0,'cut'),(Xc,10,'cut'),(Xc,len(t)-1,'cut'),(Xf,10,'fed twin'),(Xf,len(t)-1,'fed twin')]):
        y0,y1=int(max(0,cy-rad-30)),int(min(H,cy+rad+30)); x0,x1=int(max(0,cx-rad-30)),int(min(W,cx+rad+30))
        im=np.stack([X[i,1],X[i,0],np.clip(X[i,2]/1.5,0,1)],-1).clip(0,1)[y0:y1,x0:x1]
        ax[r,j].imshow(im); ax[r,j].add_patch(plt.Circle((cx-x0,cy-y0),rad,fill=False,color='w',ls='--'))
        ax[r,j].set_title(f'{n} seed{sd} {lab} t={t[i]:.0f}',fontsize=8); ax[r,j].axis('off')
    a=ax[r,5]; a.plot(t,ic,'r',label='inside disk, cut'); a.plot(t,iff,'r--',label='inside disk, fed twin')
    a.plot(t,nc,'b',label='annulus (neighbours), cut'); a.plot(t,nf,'b--',label='annulus, fed twin'); a.set_ylim(0,1.6); a.legend(fontsize=6); a.set_xlabel('t')
    out.append(f"{n} seed{sd}: inside matter at end cut {ic[-1]:.2f} vs fed {iff[-1]:.2f}; neighbours cut {nc[-1]:.2f} vs fed {nf[-1]:.2f}; t(inside<0.1)={t[np.argmax(ic<0.1)] if (ic<0.1).any() else None}")
plt.tight_layout(); plt.savefig('localcut.png',dpi=65); print('\n'.join(out))
