import sys, importlib.util, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
spec=importlib.util.spec_from_file_location('w',sys.argv[1]); W=importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
out=sys.argv[2]; T=float(sys.argv[3]); seed=0; size=tuple(W.META['size'])
for a in sys.argv[4:]:
    k,v=a.split('=')
    if k=='seed': seed=int(v)
    elif k=='size': size=(int(v),int(v))
    else: W.P[k]=float(v)
s=W.init(seed,size); n=int(T/W.P['dt']); nsn=10; ev=n//(nsn-1); snaps=[]
for i in range(n+1):
    if i%ev==0: snaps.append((i*W.P['dt'],W.fields(s).copy()))
    if i<n: s=W.step(s)
fig,ax=plt.subplots(1,len(snaps),figsize=(2.4*len(snaps),2.6))
for j,(t,f) in enumerate(snaps):
    ax[j].imshow(f[2],cmap='Greens',vmin=0,vmax=0.8); ax[j].contour(f[0],levels=[1.2],colors='m',linewidths=0.6); ax[j].axis('off')
    ax[j].set_title(f't={t:.0f} Kmean={f[2].mean():.3f}',fontsize=6)
plt.suptitle('K (green) with bilayer contour (magenta): '+' '.join(sys.argv[3:]),fontsize=7); plt.savefig(out,dpi=90,bbox_inches='tight')
np.save(out.replace('.png','_final.npy'),np.stack([s['u'],s['P'],s['K']]))
