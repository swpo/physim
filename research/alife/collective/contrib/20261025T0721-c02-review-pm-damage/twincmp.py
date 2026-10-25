import numpy as np, json, sys
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy import ndimage as ndi
rv=sys.argv[1]; s=sys.argv[2]
D=np.load(f'{rv}/dmg/seed{s}/frames.npz')['matter']; T=np.load(f'{rv}/twin/seed{s}/frames.npz')['matter']
m=json.load(open(f'{rv}/dmg/seed{s}/metrics.json'))['damage']; cy,cx=int(m['cy']),int(m['cx']); f0=m['frame']
fr=[f0-1,f0,f0+2,f0+5,f0+8,f0+12,f0+16,f0+22,f0+30,min(f0+40,D.shape[0]-1)]
H=D.shape[1]; h=24
def crop(A): return np.roll(np.roll(A,H//2-cy,0),H//2-cx,1)[H//2-h:H//2+h,H//2-h:H//2+h]
vmax=np.percentile(T,99.5)
fig,ax=plt.subplots(2,len(fr),figsize=(1.6*len(fr),3.6))
thr=0.35*vmax
for i,f in enumerate(fr):
    for j,(A,lab) in enumerate(((D,'damaged'),(T,'twin'))):
        c=crop(A[f]); ax[j,i].imshow(c,cmap='magma',vmin=0,vmax=vmax); ax[j,i].axis('off')
        L,n=ndi.label(ndi.binary_fill_holes(c>thr)); l=L[h,h] if L[h,h] else 0
        a=(L==l).sum() if l else 0
        ax[j,i].set_title(f'{lab[0]} t={f*50} A={a}',fontsize=6)
plt.suptitle(f'seed {s}: damaged run (top) vs undamaged same-seed twin (bottom), crop at target centre; A=area of component at crop centre',fontsize=7)
plt.savefig(f'{rv}/twin_cmp_seed{s}.png',dpi=110,bbox_inches='tight')
