import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from hier_metrics import *
from guild_econ import *
import numpy as np

tc = dict(rho=2.0, yW=0.8, leak=0.5, margin=3.0, sig_mut=0.05)
t0 = time.time()
out = simulate(tc, T=30000, seed=0, snap_ticks=(2000, 8000, 20000, 29999),
               block_win=(15000, 30000), dwell_win=(15000, 30000), fork_probes=True)
rt = time.time() - t0
h = out["hist"]
print(f"runtime {rt:.1f}s for 30k ticks")
print("final Vtot=%.1f ncell=%d fr_e=%.3f purity=%.3f" % (
    h["Vtot"][-1], h["ncell"][-1], h["fr_e"][-1], h["purity"][-1]))
print("Rm=%.3f Wm=%.3f (theory R*=%.3f W*=%.3f)" % (
    h["Rm"][-1], h["Wm"][-1], 1/3, 1/6))
bm = bimodality(out["final"][4], out["final"][2])
print("bimod:", bm)
print("tau_R micro:", out.get("tau_R"), " tau_W micro:", out.get("tau_W"))
bt = block_tau(out["blocks"])
print("block tau (L2):", bt)
dw = out["dwells"]
print("dwells n=%d median=%s" % (len(dw), np.median(dw) if len(dw) else None))
# macro series shape
import numpy as np
fr = h["fr_e"]
print("fr_e trajectory: ", [round(float(x),3) for x in fr[::120]])
for t, s in out["snaps"].items():
    save_strip([s[0], s[1], s[2], s[3]],
               f"/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy/strips/sanity_t{t}.png",
               titles=[f"R t={t}", "W", "V", "alloc a"], cmap="viridis")
print("strips saved")
