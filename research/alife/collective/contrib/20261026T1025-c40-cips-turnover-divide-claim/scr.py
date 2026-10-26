import sys, os, json, importlib.util, time
import numpy as np
from scipy import ndimage
tag=sys.argv[1]; P=json.loads(sys.argv[2]); T=float(sys.argv[3]); N=int(sys.argv[4]) if len(sys.argv)>4 else 128
os.environ["WORLD_P"]=json.dumps(P)
spec=importlib.util.spec_from_file_location("w",os.environ.get("WORLD","world.py")); w=importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s=w.init(P.get("seed",0),(N,N))
snaps=[]; log=[]; t0=time.time(); nxt=0; k=0
while s["t"]<T-1e-9:
    if s["t"]>=nxt-1e-9:
        e=s["e"]; lab,n=ndimage.label(e>0.5,structure=np.ones((3,3)))
        areas=np.bincount(lab.ravel())[1:]
        log.append((round(s["t"]),n,float(areas.mean()) if n else 0,float(areas.max()) if n else 0,float(e.mean()),float(s["F"].mean())))
        if k%5==0: snaps.append((round(s["t"]),e.copy()))
        k+=1; nxt+=T/80
    w.step(s)
    if not np.isfinite(s["e"]).all(): print("NAN"); break
os.makedirs("scr",exist_ok=True)
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig,ax=plt.subplots(2,(len(snaps)+1)//2,figsize=(1.1*len(snaps),4.8)); ax=ax.ravel()
for a,(tt,im) in zip(ax,snaps): a.imshow(im,vmin=0,vmax=1,cmap="magma",interpolation="nearest"); a.set_xticks([]);a.set_yticks([]); a.set_title(f"t={tt}",fontsize=7)
fig.suptitle(tag+" "+json.dumps(P),fontsize=7); fig.savefig(f"scr/{tag}.png",dpi=80)
json.dump(log,open(f"scr/{tag}.json","w")); np.save(f"scr/{tag}_final.npy",np.stack([s["e"],s["p"],s["F"]]))
print(tag, "wall %.0fs"%(time.time()-t0))
for r in log[::8]+[log[-1]]: print(r)
