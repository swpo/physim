
import sys, json, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest/succession")
from sf_core import run
from sf_measure import measure4, gates4
SD = "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest/succession"

BASE = dict(g=2e-3, Lam=9.0, theta=0.78, M=2.0, D=8.0, gsig=0.35, rho=0.03,
            gT=1e-4, mu=1.5e-5, kapT=1.5, Tm=0.45, rhoT=0.03, cT=0.5,
            patch_frac=0.30, Tinit_patch=0.62)
JIT = ("g", "Lam", "theta", "M", "D", "gsig", "rho", "gT", "mu", "kapT",
       "Tm", "rhoT", "cT", "patch_frac", "Tinit_patch")

def one(kw, seed):
    out = run(L=64, T_ticks=60000, seed=seed, init="mixed", **kw)
    res = measure4(out, drop=10000)
    gt = gates4(res)
    ok = gt["G1"] and gt["G2"] and gt["G5"]
    return out, res, gt, ok

entry = dict(base=BASE, seeds=[], jitter=[])
for seed in range(4):
    out, res, gt, ok = one(BASE, seed)
    entry["seeds"].append(dict(seed=seed, ok=ok, gates=gt,
        L4_tau=res["L4_relax"]["tau"], L4_r2=res["L4_relax"]["r2"],
        L3_model=res["L3_model"], L3_r2=res["L3_r2"], tau3=res["tau3_used"],
        tau2=res["tau2"], tau1=res["tau1"], sep21=res["sep21"],
        sep32=res["sep32"], sep43=res["sep43"], span41=res["span41"],
        n_events=res["n_events"], fri_grass=res["fri_grass_med"],
        n_fri_forest=res["n_fri_forest"], fracF_end=res["fracF_end"],
        T_end=res["T_end"], runtime=res["runtime"]))
    print("S1 seed%d ok=%d | L4 tau=%.0f r2=%.3f | L3 %s r2=%.3f t3=%.0f | "
          "seps %.1f/%.1f/%.1f span=%.0f | FRIg=%.0f nFRIf=%d | rt=%.0fs" % (
        seed, ok, res["L4_relax"]["tau"] or -1, res["L4_relax"]["r2"],
        res["L3_model"], res["L3_r2"], res["tau3_used"] or -1,
        res["sep21"] or -1, res["sep32"] or -1, res["sep43"] or -1,
        res["span41"] or -1, res["fri_grass_med"] or -1,
        res["n_fri_forest"], res["runtime"]), flush=True)

rngj = np.random.default_rng(4242)
for j in range(3):
    kw = dict(BASE)
    for k in JIT:
        kw[k] = BASE[k] * float(rngj.uniform(0.9, 1.1))
    out, res, gt, ok = one(kw, 30 + j)
    entry["jitter"].append(dict(j=j, ok=ok, gates=gt,
        kw={k: round(v, 6) for k, v in kw.items()},
        L4_tau=res["L4_relax"]["tau"], L4_r2=res["L4_relax"]["r2"],
        L3_r2=res["L3_r2"], sep43=res["sep43"], span41=res["span41"],
        n_events=res["n_events"]))
    print("S1 jit%d ok=%d | L4 tau=%s r2=%.3f | seps43=%s span=%s" % (
        j, ok, "%.0f" % res["L4_relax"]["tau"] if res["L4_relax"]["tau"] else "-",
        res["L4_relax"]["r2"],
        "%.1f" % res["sep43"] if res["sep43"] else "-",
        "%.0f" % res["span41"] if res["span41"] else "-"), flush=True)

npass = sum(s["ok"] for s in entry["seeds"])
jpass = sum(s["ok"] for s in entry["jitter"])
entry["G4"] = bool(npass >= 3 and jpass >= 2)
print("== S1: seeds %d/4 jitter %d/3 -> G4=%s" % (npass, jpass, entry["G4"]))
json.dump(entry, open(SD + "/gateS1_results.json", "w"), indent=1)
print("done")
