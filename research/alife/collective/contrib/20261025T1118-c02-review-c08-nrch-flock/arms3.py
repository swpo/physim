import numpy as np, json, sys, glob
from scipy import ndimage
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
S='/tmp/claude-0/-home-user-physim/b139604c-6bf5-5119-8527-e3beb44741c5/scratchpad/rv6/'
arms=[('NRCH','plain','plain'),('NRCH+AMB+B+reaction','both','both')]
fig,ax=plt.subplots(1,3,figsize=(14,3.8))
for i,(name,a,b) in enumerate(arms):
  for j,p in enumerate((a,b)):
    f=glob.glob(S+p+'/**/frames.npz',recursive=True)
    if not f: continue
    z=np.load(f[0]); F=z['matter']
    R=z['render']; rf=z['render_f']
    pol=[]
    for fi,rr in zip(rf,R):
      phi=rr[0]; psi=rr[1]; lab,k=ndimage.label(phi>0); us=[]
      for q in range(1,k+1):
        m=lab==q
        if m.sum()<20: continue
        yy,xx=np.nonzero(m); w=psi[m]-psi[m].min()+1e-9
        v=np.array([(xx*w).sum()/w.sum()-xx.mean(),(yy*w).sum()/w.sum()-yy.mean()])
        if np.hypot(*v)>0.3: us.append(v/np.hypot(*v))
      pol.append(np.hypot(*np.mean(us,0)) if len(us)>1 else np.nan)
    pol=np.array(pol)
    n=[];cv=[];t=np.arange(len(F))*50
    for fr in F:
      lab,k=ndimage.label(fr>0); ar=np.bincount(lab.ravel())[1:]; ar=ar[ar>=20]
      n.append(len(ar)); cv.append(ar.std()/ar.mean() if len(ar)>1 else np.nan)
    n=np.array(n); cv=np.array(cv); late=slice(len(F)//2,None)
    print(name,p,'n late mean %.1f sd %.1f'%(n[late].mean(),n[late].std()),'CV late %.2f'%np.nanmean(cv[late]),'polar order late %.2f'%np.nanmean(pol[len(pol)//2:]))
    ax[2].plot(np.array(rf)*50,pol,c='C%d'%i,ls='-' if j==0 else '--')
    ax[0].plot(t,n,c='C%d'%i,ls='-' if j==0 else '--',label=name if j==0 else None)
    ax[1].plot(t,cv,c='C%d'%i,ls='-' if j==0 else '--')
ax[0].set_title('droplets (area>=20 px) vs time; solid seed0, dashed seed1'); ax[1].set_title('CV of droplet area'); ax[0].legend(fontsize=7); ax[2].set_title('polar order of droplet polarity (psi offset)')
for a_ in ax[:2]: a_.set_xlabel('t')
fig.tight_layout(); fig.savefig(S+'arms_seed3.png',dpi=80)
