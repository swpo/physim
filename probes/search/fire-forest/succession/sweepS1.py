
import sys, json, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest/succession")
from sf_core import run
from sf_measure import measure4, gates4
SD = "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest/succession"

cands = []
# theory coords: R=gT/g, W=mu/gT, Tm, kapT, cT, patch geometry
for R in (0.04, 0.05, 0.065, 0.08):
    for kapT in (0.8, 1.5):
        cands.append(dict(gT=R * 2e-3, mu=1.5e-5, kapT=kapT, Tm=0.45,
                          rhoT=0.03, cT=0.5, patch_frac=0.30, Tinit_patch=0.62))
for Tm in (0.35, 0.55):
    for R in (0.05, 0.065):
        cands.append(dict(gT=R * 2e-3, mu=1.5e-5, kapT=1.5, Tm=Tm,
                          rhoT=0.03, cT=0.5, patch_frac=0.30, Tinit_patch=0.62))
for cT in (0.35, 0.65):
    cands.append(dict(gT=1e-4, mu=1.5e-5, kapT=1.5, Tm=0.45, rhoT=0.03,
                      cT=cT, patch_frac=0.30, Tinit_patch=0.62))
for pf, tip in ((0.45, 0.62), (0.30, 0.55), (0.45, 0.55)):
    cands.append(dict(gT=1e-4, mu=1.5e-5, kapT=1.5, Tm=0.45, rhoT=0.03,
                      cT=0.5, patch_frac=pf, Tinit_patch=tip))
# W variation at fixed R (mu is the senescence price)
for mu in (0.8e-5, 3e-5):
    cands.append(dict(gT=1e-4, mu=mu, kapT=1.5, Tm=0.45, rhoT=0.03, cT=0.5,
                      patch_frac=0.30, Tinit_patch=0.62))

results = []
for i, c in enumerate(cands):
    try:
        out = run(L=64, T_ticks=60000, seed=0, init="mixed", **c)
        res = measure4(out, drop=10000)
        gt = gates4(res)
        rec = dict(id=300 + i, stage="sweepS1", params=dict(L=64, T=60000,
                   init="mixed", **c), res=res, gates=gt)
    except Exception as e:
        rec = dict(id=300 + i, stage="sweepS1", params=c, error=repr(e),
                   gates=dict(G1=False, G2=False, G5=False))
    results.append(rec)
    r = rec.get("res", {})
    rel = r.get("L4_relax", {})
    print("%3d R=%.3f W=%.2f kT=%.1f Tm=%.2f cT=%.2f pf=%.2f tip=%.2f | "
          "T:%.2f->%.2f fF=%.2f | L4 tau=%s r2=%s | L3 %s r2=%s t3=%s | "
          "s43=%s span=%s nev=%s | G1=%d G2=%d" % (
        300 + i, c["gT"] / 2e-3, c["mu"] / c["gT"], c["kapT"], c["Tm"],
        c["cT"], c["patch_frac"], c["Tinit_patch"],
        r.get("T_start", 0), r.get("T_end", 0), r.get("fracF_end", 0),
        "%.0f" % rel["tau"] if rel.get("tau") else "-",
        "%.3f" % rel["r2"] if rel.get("r2") is not None else "-",
        r.get("L3_model", "ERR"), "%.3f" % r.get("L3_r2", 0),
        "%.0f" % r["tau3_used"] if r.get("tau3_used") else "-",
        "%.1f" % r["sep43"] if r.get("sep43") else "-",
        "%.0f" % r["span41"] if r.get("span41") else "-",
        r.get("n_events", "-"), rec["gates"]["G1"], rec["gates"]["G2"]),
        flush=True)
json.dump(results, open(SD + "/sweepS1_results.json", "w"), indent=1)
print("done", len(results))
