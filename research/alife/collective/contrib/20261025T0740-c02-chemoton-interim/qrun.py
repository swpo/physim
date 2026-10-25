"""quick scratch runner: python qrun.py world.py out.png T key=val ... (overrides world P)"""
import sys, importlib.util, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
spec=importlib.util.spec_from_file_location('w',sys.argv[1]); W=importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
out=sys.argv[2]; T=float(sys.argv[3]); seed=0; size=tuple(W.META['size'])
for a in sys.argv[4:]:
    k,v=a.split('=')
    if k=='seed': seed=int(v)
    elif k=='size': size=(int(v),int(v))
    else: W.P[k]=float(v)
s=W.init(seed,size); n=int(T/W.P['dt']); nsn=8; ev=n//(nsn-1); snaps=[]
for i in range(n+1):
    if i%ev==0: snaps.append((i*W.P['dt'],W.fields(s).copy()))
    if i<n: s=W.step(s)
C=snaps[0][1].shape[0]
fig,ax=plt.subplots(C,len(snaps),figsize=(2.2*len(snaps),2.3*C))
vm=[max(1e-3,max(f[c].max() for _,f in snaps)) for c in range(C)]
for j,(t,f) in enumerate(snaps):
    for c in range(C):
        ax[c,j].imshow(f[c],cmap=['magma','viridis','inferno'][c%3],vmin=0,vmax=vm[c]); ax[c,j].axis('off')
        ax[c,j].set_title(f't={t:.0f} m={f[c].mean():.3f} M={f[c].max():.2f}',fontsize=6)
plt.suptitle(' '.join(sys.argv[3:]),fontsize=7); plt.savefig(out,dpi=70,bbox_inches='tight')
