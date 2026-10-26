import sys, numpy as np
sys.path.insert(0,'/home/user/physim/research/alife')
from labkit.world import load_world
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy import ndimage
W=load_world(sys.argv[1]); seed=int(sys.argv[2]); T=float(sys.argv[3]); out=sys.argv[4]
s=W.init(seed,W.META["size"]); rows=[]; snaps=[]; n=int(round(T/0.1)); K=s["X"].shape[0]
def cnt(X):
    lab,k=ndimage.label(X>0.35)
    if not k: return 0
    a=ndimage.sum(np.ones_like(X),lab,np.arange(1,k+1)); return int((a>=20).sum())
def kmap(s):
    c=s["X"][:,0]; m=c.max(0); return np.where(m>0.35, c.argmax(0), -1)
prev=None; turn=[]
for i in range(n+1):
    if i%100==0: rows.append([i*0.1]+[cnt(s["X"][k][0]) for k in range(K)]+[float(s["F"].mean())])
    if i%200==0:
        km=kmap(s)
        if prev is not None:
            occ=(km>=0)|(prev>=0); turn.append([i*0.1, float((km!=prev)[occ].mean()) if occ.any() else 0.0])
        prev=km
    if i%(n//5)==0: snaps.append((i*0.1,s["X"][:,0].copy()))
    if i<n: s=W.step(s)
np.savetxt(out+".txt",np.array(rows),fmt="%g")
np.savetxt(out+"_turnover.txt",np.array(turn),fmt="%g",header="t fraction of occupied pixels whose kind label changed in the last 20 t")
fig,ax=plt.subplots(1,len(snaps)+1,figsize=(3*(len(snaps)+1),3))
for a,(t,f) in zip(ax,snaps):
    a.imshow(np.clip(np.moveaxis(f[:3],0,-1),0,1)); a.set_title(f"t={t:.0f}"); a.axis('off')
r=np.array(rows)
for k,c in zip(range(K),'rgb'): ax[-1].plot(r[:,0],r[:,1+k],c)
plt.tight_layout(); plt.savefig(out+".png",dpi=60); print(rows[-1])
