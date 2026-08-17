
import sys, json, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest")
from ff_core import *
from hier_metrics import save_strip

# quick: L=64, T=20000, expected sawtooth regime
out = run(L=64, T=20000, g=1e-3, Lam=30, theta=0.5, M=3, D=4, seed=0,
          snap_times=(4000, 9000, 9050, 9100, 14000))
res = measure(out, drop=4000)
print("runtime", round(out["runtime"],2), "s   f=%.2e Tg=%.0f" % (out["f"], out["Tg"]))
for k in ("B_lo","B_hi","meanF_mean","top_model","top_r2","top_params",
          "n_events","size_max","size_med","tau1","tau2","tau3","sep21","sep32"):
    print(k, "=", res.get(k))
print("pl", res.get("pl"))
snaps = out["snaps"]
if snaps:
    ts = sorted(snaps)
    save_strip([snaps[t][0] for t in ts],
               "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest/strips/sanity_B.png",
               titles=["B t=%d" % t for t in ts], cmap="Greens", vmax=1.0)
    save_strip([snaps[t][1] for t in ts],
               "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest/strips/sanity_F.png",
               titles=["F t=%d" % t for t in ts], cmap="magma", vmax=1.0)
# dump macro series for a look
np.save("/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest/logs/sanity_meanB.npy", out["meanB"])
