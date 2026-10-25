import numpy as np, sys
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
out=sys.argv[1]; runs=sys.argv[2:]
fig,ax=plt.subplots(2*len(runs),8,figsize=(16,4.4*len(runs)))
for r,run in enumerate(runs):
    d=np.load(run+'/frames.npz'); R=d['render']; f=d['render_f']; idx=np.linspace(0,len(f)-1,8).astype(int)
    for j,i in enumerate(idx):
        ax[2*r,j].imshow(R[i,0],cmap='magma',vmin=0,vmax=3); ax[2*r,j].set_title(f'{run.split("/")[-2]} t={f[i]*4}',fontsize=7)
        rgb=np.zeros(R[i,1].shape+(3,)); rgb[...,0]=np.clip(np.log10(R[i,1]+1e-4)/2+1,0,1)*(R[i,1]>1e-3); rgb[...,1]=np.clip(np.log10(R[i,2]+1e-4)/2+1,0,1)*(R[i,2]>1e-3)
        ax[2*r+1,j].imshow(rgb); ax[2*r+1,j].set_title(f'K1 red {R[i,1].sum():.0f} K2 green {R[i,2].sum():.0f}',fontsize=6)
for a in ax.flat: a.axis('off')
plt.savefig(out,dpi=75,bbox_inches='tight')
