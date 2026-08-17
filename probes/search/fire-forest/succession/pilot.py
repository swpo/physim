
import sys, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest/succession")
from sf_core import run
from sf_measure import measure4
SD = "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest/succession"

# W = mu/gT: senescence balance. Test forest persistence + decay across gT at mu=3e-5
mu = 3e-5
for gT in (1e-4, 1.6e-4, 2.4e-4, 3.6e-4):
    out = run(L=64, T_ticks=100000, seed=0, init="mixed", patch_frac=0.85,
              Tinit_patch=0.85, gT=gT, mu=mu, kapT=1.5, Tm=0.45, rhoT=0.02)
    res = measure4(out, drop=10000)
    mT = out["meanT"]
    print("gT=%.1e R=%.3f W=%.2f | T 0.85-> %.3f (mid %.3f) fracF=%.3f | L4relax tau=%s r2=%.3f | L3 %s r2=%.3f | rt=%.0fs" % (
        gT, gT/2e-3, mu/gT, res["T_end"], mT[len(mT)//2], res["fracF_end"],
        "%.0f" % res["L4_relax"]["tau"] if res["L4_relax"]["tau"] else "-",
        res["L4_relax"]["r2"], res["L3_model"], res["L3_r2"], out["runtime"]), flush=True)
    np.save(SD + "/logs/pilot_gT%.0e_meanT.npy" % gT, mT)
print("done")
