
import sys, json, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest/succession")
from sf_core import run
SD = "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest/succession"

# bistability map: for each (gT, kapT), run savanna-init and forest-init.
# bistable <=> savanna stays low AND forest stays high.
rows = []
mu = 3e-5
for kapT in (0.8, 1.5, 2.5):
    for gT in (0.8e-4, 1.2e-4, 1.8e-4, 2.7e-4, 4e-4):
        ends = {}
        for init in ("savanna", "forest"):
            out = run(L=64, T_ticks=60000, seed=0, init=init, gT=gT, mu=mu,
                      kapT=kapT, Tm=0.45, rhoT=0.02, cT=0.5)
            ends[init] = dict(T_end=float(out["meanT"][-40:].mean()),
                              fracF=float(out["fracForest"][-40:].mean()),
                              rt=round(out["runtime"], 1))
        bist = ends["savanna"]["fracF"] < 0.15 and ends["forest"]["fracF"] > 0.6
        rows.append(dict(gT=gT, kapT=kapT, mu=mu, W=mu / gT, R=gT / 2e-3,
                         sav=ends["savanna"], forest=ends["forest"],
                         bistable=bool(bist)))
        print("kapT=%.1f gT=%.1e W=%.2f | sav T=%.3f fF=%.2f | for T=%.3f fF=%.2f | BISTABLE=%s"
              % (kapT, gT, mu / gT, ends["savanna"]["T_end"], ends["savanna"]["fracF"],
                 ends["forest"]["T_end"], ends["forest"]["fracF"], bist), flush=True)
json.dump(rows, open(SD + "/bistability_map.json", "w"), indent=1)
print("done")
