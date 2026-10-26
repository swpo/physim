# runle with the world's own step DT: counts A/B cells every 10 t
import sys, numpy as np
sys.path.insert(0,'/home/user/physim/research/alife')
from labkit.world import load_world
from scipy import ndimage
W=load_world(sys.argv[1]); seed=int(sys.argv[2]); T=float(sys.argv[3]); out=sys.argv[4]
dt=W.P["DT"]; s=W.init(seed,W.META["size"]); rows=[]; n=int(round(T/dt)); every=int(round(10/dt))
def cnt(X):
    lab,k=ndimage.label(X>0.35)
    if not k: return 0
    a=ndimage.sum(np.ones_like(X),lab,np.arange(1,k+1)); return int((a>=20).sum())
for i in range(n+1):
    if i%every==0: rows.append([i*dt,cnt(s["A"][0]),cnt(s["B"][0]),float(s["A"].sum()),float(s["B"].sum()),float(s["F"].mean())])
    if i<n: s=W.step(s)
np.savetxt(out+".txt",np.array(rows),fmt="%g",header="t nA nB massA massB Fmean"); print(rows[-1])
