import sys, os, json, numpy as np, importlib.util
sys.path.insert(0, '/home/user/physim/research/alife')
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy import ndimage
spec = importlib.util.spec_from_file_location("w", sys.argv[1]); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
seed=int(sys.argv[2]); T=int(sys.argv[3]); out=sys.argv[4]; nsnap=6
s=w.init(seed, w.META["size"]); rows=[]; snaps=[]
for t in range(T+1):
    if t%200==0:
        v=s["v"]; tot=v.sum(axis=(1,2)); cnt=[ndimage.label(v[i]>0.2)[1] for i in range(3)]
        rows.append([t,*tot,*cnt])
    if t % (T//(nsnap-1))==0: snaps.append((t,s["v"].copy()))
    if t<T: s=w.step(s)
rows=np.array(rows); np.savetxt(out+".txt", rows, fmt="%.4g")
fig,ax=plt.subplots(1,nsnap+1,figsize=(3*(nsnap+1),3))
for a,(t,v) in zip(ax,snaps):
    img=np.clip(np.moveaxis(v,0,-1)/0.5,0,1); a.imshow(img); a.set_title(f"t={t}"); a.axis('off')
for i,c in enumerate("rgb"): ax[-1].plot(rows[:,0],rows[:,4+i],c); 
ax[-1].set_title("spots per kind"); plt.tight_layout(); plt.savefig(out+".png",dpi=60)
print(rows[-1])
