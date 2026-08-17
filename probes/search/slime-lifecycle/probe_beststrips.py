
import sys, json, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/slime-lifecycle")
from slime import run
from hier_metrics import save_strip

p = json.load(open("best_c30.json"))
# lifecycle period ~2320; snapshot one cycle + next famine
snap = (2300, 2500, 2700, 2900, 3300, 3900, 4400, 4700, 4900, 5200)
o = run(params=p, T=5400, seed=0, rec=10, snap_times=snap)
sn = o["snaps"]
ts = sorted(sn)
for f, cm, vmx in (("V", "magma", None), ("S", "inferno", None), ("R", "viridis", 1.0), ("A", "cividis", None)):
    save_strip([sn[t][f] for t in ts], "strips/best_c30_%s.png" % f,
               titles=["%s t=%d" % (f, t) for t in ts], cmap=cm, vmax=vmx)
print("saved best_c30 strips")
