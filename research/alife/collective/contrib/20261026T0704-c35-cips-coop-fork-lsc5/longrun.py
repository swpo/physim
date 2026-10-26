import sys, os, json, importlib.util, time
import numpy as np
from scipy import ndimage
tag=sys.argv[1]; P=json.loads(sys.argv[2]); T=float(sys.argv[3]); N=int(sys.argv[4]); every=float(sys.argv[5])
os.environ["WORLD_P"]=json.dumps(P)
spec=importlib.util.spec_from_file_location("w","world.py"); w=importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s=w.init(P.get("seed",0),(N,N)); os.makedirs(f"long/{tag}",exist_ok=True)
nxt=0; log=[]
ck=f"long/{tag}/ckpt.npz"
if os.path.exists(ck):
    z=np.load(ck); s["e"],s["p"],s["F"]=z["e"],z["p"],z["F"]; s["t"]=float(z["t"]); nxt=float(z["nxt"]); log=json.load(open(f"long/{tag}/log.json"))
lastck=s["t"]
while s["t"]<T-1e-9:
    if s["t"]>=nxt-1e-9:
        e=s["e"]; lab,n=ndimage.label(e>0.5)
        log.append((round(s["t"]),n)); np.save(f"long/{tag}/e_{round(s['t']):06d}.npy",e.astype(np.float16))
        json.dump(log,open(f"long/{tag}/log.json","w")); nxt+=every
    w.step(s)
    if s["t"]-lastck>=1000:
        np.savez(ck+".tmp.npz",e=s["e"],p=s["p"],F=s["F"],t=s["t"],nxt=nxt); os.replace(ck+".tmp.npz",ck); lastck=s["t"]
print("done")
