
import sys, json, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest/succession")
from sf_core import run
from sf_measure import measure4
SD = "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest/succession"

# G3: tree growth price gT swept; mu, fire params ABSOLUTE-fixed.
# Response 1 (primary): forest-branch equilibrium cover T* (forest init).
# Response 2: savanna-branch T_end (bistability check / tipping edge).
# Response 3: mosaic relaxation tau4 (mixed init).
base = dict(g=2e-3, Lam=9.0, theta=0.78, M=2.0, D=8.0, gsig=0.35, rho=0.03,
            mu=1.5e-5, kapT=1.5, Tm=0.45, rhoT=0.03, cT=0.5)
gTs = [0.6e-4, 0.8e-4, 1.2e-4, 1.8e-4, 2.7e-4, 4.0e-4]
rows = []
for gT in gTs:
    row = dict(gT=gT, W=base["mu"] / gT, R=gT / 2e-3)
    Tstars = []
    for seed in (0, 1, 2):
        out = run(L=64, T_ticks=60000, seed=seed, init="forest", gT=gT, **base)
        Tstars.append(float(out["meanT"][-100:].mean()))
    row["Tstar_forest"] = Tstars
    row["Tstar_med"] = float(np.median(Tstars))
    out = run(L=64, T_ticks=60000, seed=0, init="savanna", gT=gT, **base)
    row["T_savanna_end"] = float(out["meanT"][-100:].mean())
    row["fracF_savanna"] = float(out["fracForest"][-100:].mean())
    out = run(L=64, T_ticks=60000, seed=0, init="mixed", gT=gT,
              patch_frac=0.30, Tinit_patch=0.62, **base)
    res = measure4(out, drop=10000)
    row["tau4_mixed"] = res["L4_relax"]["tau"]; row["tau4_r2"] = res["L4_relax"]["r2"]
    rows.append(row)
    print("gT=%.1e W=%.2f | T* forest=%.3f (%s) | savanna end=%.3f fF=%.2f | tau4=%s r2=%s" % (
        gT, row["W"], row["Tstar_med"],
        ",".join("%.3f" % v for v in Tstars), row["T_savanna_end"],
        row["fracF_savanna"],
        "%.0f" % row["tau4_mixed"] if row["tau4_mixed"] else "-",
        "%.3f" % row["tau4_r2"] if row["tau4_r2"] is not None else "-"), flush=True)
json.dump(rows, open(SD + "/g3_succession.json", "w"), indent=1)
Ts = [r["Tstar_med"] for r in rows]
mono = all(b > a for a, b in zip(Ts, Ts[1:]))
print("T* monotone increasing:", mono)
print("done")
