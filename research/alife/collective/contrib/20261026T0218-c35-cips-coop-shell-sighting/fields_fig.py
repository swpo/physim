import sys, os, json, importlib.util
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
out=sys.argv[1]; T=float(sys.argv[2]); N=int(sys.argv[3]); arms=json.loads(sys.argv[4])
fig,ax=plt.subplots(len(arms),4,figsize=(12,3*len(arms)))
for r,(name,P) in enumerate(arms.items()):
    os.environ["WORLD_P"]=json.dumps(P)
    spec=importlib.util.spec_from_file_location("w","world.py"); w=importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
    s=w.init(P.get("seed",0),(N,N))
    while s["t"]<T-1e-9: w.step(s)
    for c,(k,vm) in enumerate([("e",1),("F",1),("p",None)]):
        im=ax[r,c].imshow(s[k],cmap="magma",vmin=0,vmax=vm); plt.colorbar(im,ax=ax[r,c],fraction=0.046)
        ax[r,c].set_title(f"{name}: {k}, t={T:.0f}",fontsize=8); ax[r,c].set_xticks([]); ax[r,c].set_yticks([])
    m=N//2
    for k,col in [("e","C0"),("F","C1"),("p","C2")]: ax[r,3].plot(s[k][m,:],col,label=k)
    ax[r,3].legend(fontsize=7); ax[r,3].set_title("horizontal cut through centre",fontsize=8)
    np.save(f"{out}_{name}.npy",np.stack([s["e"],s["p"],s["F"]]))
fig.tight_layout(); fig.savefig(out+".png",dpi=70)
