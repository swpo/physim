# quick runner: prints stats every 'every' steps, saves snapshot strip
import sys, json, numpy as np
sys.path.insert(0,'/home/user/physim/research/alife')
from labkit.world import load_world
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy import ndimage
w=load_world(sys.argv[1]); seed=int(sys.argv[2]); T=int(sys.argv[3]); out=sys.argv[4]; every=int(sys.argv[5]) if len(sys.argv)>5 else 2000
s=w.init(seed,w.META["size"]); rows=[]; snaps=[]
for t in range(T+1):
    if t%every==0:
        lab,n=ndimage.label(s["phi"]>0.5, structure=None)
        H,W=s["phi"].shape; iy=s["py"].astype(int)%H; ix=s["px"].astype(int)%W
        cl=lab[iy,ix]; pk=s["kind"]==1
        npc=len(set(cl[pk & (cl>0)])) ; prc=len(set(cl[(~pk)&(cl>0)]))
        st=w.stats(s); rows.append([t,n,prc,npc,st["N"]-st["npred"],st["npred"],st["eaten"]])
        print(*rows[-1], flush=True)
    if t%(T//5)==0:
        f=w.fields(s); snaps.append((t,f))
    if t<T: s=w.step(s)
np.savetxt(out+".txt",np.array(rows),fmt="%g")
fig,ax=plt.subplots(1,len(snaps),figsize=(3*len(snaps),3))
for a,(t,f) in zip(ax,snaps):
    img=np.stack([np.clip(f[2]/0.5,0,1),np.clip(f[1]/0.5,0,1),np.clip(f[4],0,1)],-1); a.imshow(img); a.set_title(f"t={t}"); a.axis('off')
plt.tight_layout(); plt.savefig(out+".png",dpi=60)
