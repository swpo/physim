import sys, os, json, importlib.util, time
import numpy as np
from scipy import ndimage
tag=sys.argv[1]; P=json.loads(sys.argv[2]); T=float(sys.argv[3]); N=int(sys.argv[4]) if len(sys.argv)>4 else 128
os.environ["WORLD_P"]=json.dumps(P)
spec=importlib.util.spec_from_file_location("w",os.environ.get("WORLD","world.py")); w=importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s=w.init(P.get("seed",0),(N,N)); dt=s["par"]["dt"]
snaps=[]; log=[]; t0=time.time(); nxt=0
while s["t"]<T-1e-9:
    if s["t"]>=nxt-1e-9:
        e=(s["e"] if "e" in s else s["e1"]+s["e2"]); lab,n=ndimage.label(e>0.5,structure=np.ones((3,3)))
        # periodic wrap ignored for count
        areas=np.bincount(lab.ravel())[1:]
        log.append((round(s["t"]),n,float(areas.mean()) if n else 0,float(areas.max()) if n else 0,float(e.mean()),float(s["F"].mean())))
        if len(log)%5==1: snaps.append(np.stack([s["e1"],s["e2"],0*e],-1).clip(0,1) if "e1" in s else e.copy())
        nxt+=T/40
    w.step(s)
os.makedirs("scr",exist_ok=True)
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig,ax=plt.subplots(1,len(snaps),figsize=(2.2*len(snaps),2.4))
for a,(i,im) in zip(ax,enumerate(snaps)): a.imshow(im,vmin=0,vmax=1,cmap="magma",interpolation="nearest"); a.set_xticks([]);a.set_yticks([]); a.set_title(f"t={i*T/8:.0f}",fontsize=7)
fig.suptitle(tag+" "+json.dumps(P),fontsize=7); fig.savefig(f"scr/{tag}.png",dpi=80); 
json.dump(log,open(f"scr/{tag}.json","w"))
print(tag, "wall %.0fs"%(time.time()-t0)); 
for r in log[::4]+[log[-1]]: print(r)
