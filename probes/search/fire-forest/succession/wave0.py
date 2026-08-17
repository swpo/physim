
import sys, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest/succession")
from sf_core import run
from sf_measure import measure4
SD = "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest/succession"
base = dict(g=2e-3, gT=1e-4, mu=1.5e-5, kapT=1.5, Tm=0.45, rhoT=0.03)

# check 1: savanna with NO fire trap -> trees should invade (proves trap holds savanna)
kw = dict(base); kw["kapT"] = 0.0
out = run(L=64, T_ticks=50000, seed=0, init="savanna", **kw)
print("kapT=0 savanna: T %.3f -> %.3f fracF_end=%.3f  (expect invasion)" % (
    out["meanT"][0], out["meanT"][-40:].mean(), out["fracForest"][-40:].mean()), flush=True)

# check 2: long mixed run -> pinned mosaic or drift?
out = run(L=64, T_ticks=150000, seed=0, init="mixed", **base)
mT = out["meanT"]; fF = out["fracForest"]
n = len(mT)
for fr in (0.2, 0.4, 0.6, 0.8, 1.0):
    i = int(n * fr) - 1
    print("t=%6d meanT=%.3f fracF=%.3f" % (i * 5, mT[i], fF[i]), flush=True)
res = measure4(out, drop=10000)
print("L4 relax tau=%s r2=%.3f | L3 %s r2=%.3f tau3=%s | seps 43=%s span=%s rt=%.1f" % (
    "%.0f" % res["L4_relax"]["tau"] if res["L4_relax"]["tau"] else "-",
    res["L4_relax"]["r2"], res["L3_model"], res["L3_r2"],
    "%.0f" % res["tau3_used"] if res["tau3_used"] else "-",
    "%.1f" % res["sep43"] if res["sep43"] else "-",
    "%.0f" % res["span41"] if res["span41"] else "-", out["runtime"]))
np.save(SD + "/logs/wave0_mixed150k_meanT.npy", mT)
np.save(SD + "/logs/wave0_mixed150k_fracF.npy", fF)
print("done")
