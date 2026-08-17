
import sys, json, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest/succession")
from sf_core import run
from sf_measure import measure4, gates4
SD = "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest/succession"
base = dict(g=2e-3, Lam=9.0, theta=0.78, M=2.0, D=8.0, gsig=0.35, rho=0.03,
            mu=1.5e-5, kapT=1.5, Tm=0.45, rhoT=0.03, cT=0.5)

print("--- forest-branch collapse (low gT) ---", flush=True)
rows = []
for gT in (0.8e-5, 1.5e-5, 2.5e-5, 4e-5):
    o = run(L=64, T_ticks=60000, seed=0, init="forest", gT=gT, **base)
    r = dict(gT=gT, T_dn=float(o["meanT"][-100:].mean()),
             fF_dn=float(o["fracForest"][-100:].mean()))
    rows.append(r)
    print("gT=%.1e | forest-branch T=%.3f fF=%.2f" % (gT, r["T_dn"], r["fF_dn"]), flush=True)
json.dump(rows, open(SD + "/hysteresis_low.json", "w"), indent=1)

print("--- savanna->forest tipping refine ---", flush=True)
rows2 = []
for gT in (3.0e-4, 3.4e-4, 3.7e-4):
    o = run(L=64, T_ticks=60000, seed=0, init="savanna", gT=gT, **base)
    r = dict(gT=gT, T_up=float(o["meanT"][-100:].mean()),
             fF_up=float(o["fracForest"][-100:].mean()))
    rows2.append(r)
    print("gT=%.2e | savanna-branch T=%.3f fF=%.2f" % (gT, r["T_up"], r["fF_up"]), flush=True)
json.dump(rows2, open(SD + "/tipping_up.json", "w"), indent=1)

print("--- NEGATIVE CONTROL: flammable canopy veg_flam>0 ---", flush=True)
for vf in (0.4, 0.8):
    o_s = run(L=64, T_ticks=60000, seed=0, init="savanna", gT=1e-4, veg_flam=vf, **base)
    o_f = run(L=64, T_ticks=60000, seed=0, init="forest", gT=1e-4, veg_flam=vf, **base)
    res = measure4(o_f, drop=10000)
    print("veg_flam=%.1f | sav T=%.3f fF=%.2f | forest T=%.3f fF=%.2f | forest FRI n=%d | bistable=%s" % (
        vf, o_s["meanT"][-100:].mean(), o_s["fracForest"][-100:].mean(),
        o_f["meanT"][-100:].mean(), o_f["fracForest"][-100:].mean(),
        res["n_fri_forest"],
        o_s["fracForest"][-100:].mean() < 0.15 and o_f["fracForest"][-100:].mean() > 0.6), flush=True)

print("--- L3-clock integrity inside 4-layer world vs round-1 (no trees) ---", flush=True)
o_no = run(L=64, T_ticks=60000, seed=0, init="savanna", gT=0.0, rhoT=0.0, **{k: v for k, v in base.items() if k not in ("mu","kapT","Tm","rhoT","cT")}, mu=0.0, kapT=0.0, Tm=0.45, cT=0.5)
res_no = measure4(o_no, drop=10000)
print("no-trees: L3 %s r2=%.3f tau3=%s FRIg=%.0f" % (
    res_no["L3_model"], res_no["L3_r2"],
    "%.0f" % res_no["tau3_used"] if res_no["tau3_used"] else "-",
    res_no["fri_grass_med"] or -1), flush=True)
print("done")
