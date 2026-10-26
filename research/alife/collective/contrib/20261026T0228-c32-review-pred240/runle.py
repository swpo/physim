# quick runner: counts of A and B cells (core channel > 0.35, area >= 20) every 10 t, + 6 snapshots
import sys, json, numpy as np
sys.path.insert(0,'/home/user/physim/research/alife')
from labkit.world import load_world
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy import ndimage
W=load_world(sys.argv[1]); seed=int(sys.argv[2]); T=float(sys.argv[3]); out=sys.argv[4]
s=W.init(seed,W.META["size"]); rows=[]; snaps=[]; n=int(round(T/0.1))
def cnt(X):
    lab,k=ndimage.label(X>0.35); 
    if not k: return 0
    a=ndimage.sum(np.ones_like(X),lab,np.arange(1,k+1)); return int((a>=20).sum())
for i in range(n+1):
    if i%100==0:
        rows.append([i*0.1,cnt(s["A"][0]),cnt(s["B"][0]),float(s["A"].sum()),float(s["B"].sum()),float(s["F"].mean())])
    if i%(n//5)==0: snaps.append((i*0.1,np.concatenate([s["A"][:1],s["B"][:1],s["F"][None]])))
    if i<n: s=W.step(s)
np.savetxt(out+".txt",np.array(rows),fmt="%g",header="t nA nB massA massB Fmean")
fig,ax=plt.subplots(1,len(snaps)+1,figsize=(3*(len(snaps)+1),3))
for a,(t,f) in zip(ax,snaps):
    a.imshow(np.stack([np.clip(f[0],0,1),np.clip(f[2],0,1)*0.5,np.clip(f[1],0,1)],-1)); a.set_title(f"t={t:.0f}"); a.axis('off')
r=np.array(rows); ax[-1].plot(r[:,0],r[:,1],'r',label='A cells'); ax[-1].plot(r[:,0],r[:,2],'b',label='B cells'); ax[-1].legend()
plt.tight_layout(); plt.savefig(out+".png",dpi=60); print(rows[-1])
