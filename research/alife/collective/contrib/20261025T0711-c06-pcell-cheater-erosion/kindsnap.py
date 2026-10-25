"""Particles coloured by kind over the wall contour, at chosen times. usage: kindsnap.py world seed out.png t1,t2,.. key=val.."""
import sys; sys.path.insert(0,'/home/user/physim/research/alife')
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from labkit.world import load_world
W=load_world(sys.argv[1]); seed=int(sys.argv[2]); out=sys.argv[3]; ts=[int(x) for x in sys.argv[4].split(',')]
for kv in sys.argv[5:]:
    k,v=kv.split('='); W.P[k]=float(v)
s=W.init(seed,(128,128)); fr=[]
for t in range(max(ts)+1):
    if t in ts: fr.append((t,s['phi'].copy(),s['px'].copy(),s['py'].copy(),(s['y'].copy() if W.P['ytrait'] else s['kind'].copy())))
    s=W.step(s)
f,ax=plt.subplots(1,len(fr),figsize=(4*len(fr),4.3))
for a,(t,phi,px,py,k) in zip(np.atleast_1d(ax),fr):
    a.imshow(phi,cmap='Greys',vmin=0,vmax=2.5,origin='upper'); a.contour(phi,[0.5],colors='k',linewidths=0.6)
    (a.scatter(px,py,s=0.15,c=k,cmap='viridis',vmin=0,vmax=1.4) if W.P['ytrait'] else a.scatter(px,py,s=0.15,c=np.where(k==1,'tab:red','tab:blue'))); a.set_title(f't={t}  N={len(px)}  mean {np.mean(k):.2f}',fontsize=9)
    a.set_xticks([]); a.set_yticks([])
plt.suptitle(' '.join(sys.argv[5:])+f'  seed {seed}  (blue kind 0, red kind 1)',fontsize=9); plt.tight_layout(); plt.savefig(out,dpi=80)
