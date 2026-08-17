
import sys, json, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest/succession")
from sf_core import run
SD = "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest/succession"

# hysteresis loop in gT (tree growth price): both branches followed
base = dict(g=2e-3, Lam=9.0, theta=0.78, M=2.0, D=8.0, gsig=0.35, rho=0.03,
            mu=1.5e-5, kapT=1.5, Tm=0.45, rhoT=0.03, cT=0.5)
gTs = [0.4e-4, 0.6e-4, 0.9e-4, 1.35e-4, 2.0e-4, 3.0e-4, 4.5e-4, 6.75e-4]
rows = []
for gT in gTs:
    o_s = run(L=64, T_ticks=60000, seed=0, init="savanna", gT=gT, **base)
    o_f = run(L=64, T_ticks=60000, seed=0, init="forest", gT=gT, **base)
    row = dict(gT=gT,
               T_up=float(o_s["meanT"][-100:].mean()),
               fF_up=float(o_s["fracForest"][-100:].mean()),
               T_dn=float(o_f["meanT"][-100:].mean()),
               fF_dn=float(o_f["fracForest"][-100:].mean()))
    rows.append(row)
    print("gT=%.2e | savanna-branch T=%.3f fF=%.2f | forest-branch T=%.3f fF=%.2f | gap=%.3f" % (
        gT, row["T_up"], row["fF_up"], row["T_dn"], row["fF_dn"],
        row["T_dn"] - row["T_up"]), flush=True)
json.dump(rows, open(SD + "/hysteresis.json", "w"), indent=1)
print("done")
