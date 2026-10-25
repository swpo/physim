import numpy as np, sys
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sp=sys.argv[1]; seeds=sys.argv[2:]
fig,ax=plt.subplots(figsize=(6,3.5))
for s in seeds:
    for arm,ls in (('up','-'),('twin','--')):
        d=np.load(f'{sp}/{arm}/seed{s}/frames.npz'); R=d['render']; f=d['render_f']
        k1=R[:,0].reshape(len(f),-1).sum(1); k2=R[:,1].reshape(len(f),-1).sum(1); sh=k2/np.maximum(k1+k2,1e-9)
        ax.plot(f*250,sh,ls,label=f'{arm} s{s}')
        i=np.searchsorted(f,[40,80,120,160]); print(arm,s,'K2 share at t=10k,20k,30k,40k:',[round(float(sh[min(j,len(sh)-1)]),3) for j in i],'final total K',round(float((k1+k2)[-1]),1))
ax.set_xlabel('time'); ax.set_ylabel('K2 biomass share'); ax.legend(fontsize=7); plt.tight_layout(); plt.savefig(f'{sp}/k2_share.png',dpi=100)
