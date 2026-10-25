import numpy as np, sys
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
runs=sys.argv[2:]; out=sys.argv[1]
fig,ax=plt.subplots(len(runs)*3,8,figsize=(16,6.2*len(runs)))
for r,run in enumerate(runs):
    d=np.load(run+'/frames.npz'); R=d['render']; f=d['render_f']; idx=np.linspace(0,len(f)-1,8).astype(int)
    for c,(cm,vm) in enumerate((('magma',2.0),('viridis',1.0),('inferno',None))):
        for j,i in enumerate(idx):
            a=ax[3*r+c,j]; a.imshow(R[i,c],cmap=cm,vmin=0,vmax=vm if vm else max(1e-3,np.percentile(R[:,c],99.9))); a.axis('off')
            a.set_title(f'{run.split("/")[-2][:14]} c{c} f{f[i]} max {R[i,c].max():.2f}',fontsize=6)
plt.savefig(out,dpi=70,bbox_inches='tight')
