
"""sweep3.py -- FINAL scoring pass: all candidates, metric-locked runner v3."""
import sys, json, time
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter")
from runner import eval_candidate

cands = []
cid = 0
def add(note="", **kw):
    global cid
    kw.setdefault("noise", 2e-3)
    kw.setdefault("sigma", 1.0)
    kw.setdefault("Dc", 10.0)
    cands.append((cid, kw, note))
    cid += 1

pair_for_L = {48: (4, 5), 64: (5, 6), 80: (6, 7), 96: (7, 8)}
for Dv in [10.0, 11.0, 12.0, 15.0]:
    for L in [48, 64, 80]:
        add(Dv=Dv, L=L, kappa=0.5, eps=2.4e-3, n_pair=pair_for_L[L], note="A:band x ladder")
for Dv in [11.0, 12.0]:
    for L in [64, 80]:
        for eps in [1.2e-3, 4.8e-3]:
            add(Dv=Dv, L=L, kappa=0.5, eps=eps, n_pair=pair_for_L[L], note="A2:eps")
add(Dv=11.0, L=64, kappa=0.5, eps=3.4e-3, n_pair=(5, 6), note="A3:flagship eps")
add(Dv=10.0, L=48, kappa=0.5, eps=3.4e-3, n_pair=(4, 5), note="A3:flagship eps")
for kap in [0.1, 0.2, 0.35, 0.65, 0.8, 0.9]:
    add(Dv=11.0, L=64, kappa=kap, eps=2.4e-3, n_pair=(5, 6), note="B:kappa")
for noise in [5e-4, 1e-3, 4e-3, 8e-3]:
    add(Dv=11.0, L=64, kappa=0.5, eps=2.4e-3, n_pair=(5, 6), noise=noise, note="C:noise")
add(Dv=25.0, L=96, kappa=0.5, eps=2.4e-3, n_pair=(7, 8), note="D:wide band")
add(Dv=25.0, L=96, kappa=0.5, eps=8.0e-3, n_pair=(7, 8), note="D:wide band")
add(Dv=25.0, L=64, kappa=0.5, eps=2.4e-3, n_pair=(5, 6), note="D:wide band")
add(Dv=9.0, L=64, kappa=0.5, eps=2.4e-3, n_pair=(5, 6), note="E:narrow band")
add(Dv=9.5, L=64, kappa=0.5, eps=2.4e-3, n_pair=(5, 6), note="E:narrow band")
for sg in [0.5, 0.75, 1.25, 1.5]:
    add(Dv=11.0, L=64, kappa=0.5, eps=2.4e-3, n_pair=(5, 6), sigma=sg, note="F:sigma")
for Dc in [1.0, 3.0]:
    add(Dv=11.0, L=64, kappa=0.5, eps=2.4e-3, n_pair=(5, 6), Dc=Dc, note="G:Dc")
# H: cert-grid refinement region (from v2 grid)
for eps in [2.8e-3, 3.2e-3]:
    for kap in [0.42, 0.5]:
        add(Dv=11.0, L=64, kappa=kap, eps=eps, n_pair=(5, 6), note="H:cert grid")
add(Dv=11.0, L=64, kappa=0.5, eps=2.8e-3, n_pair=(5, 6), noise=8e-3, note="H:cert grid")
add(Dv=10.5, L=64, kappa=0.5, eps=2.8e-3, n_pair=(5, 6), note="H:cert grid")

print("total candidates:", len(cands), flush=True)
results = []
t00 = time.time()
for cid_, kw, note in cands:
    try:
        r = eval_candidate(dict(kw))
        r["id"], r["note"] = cid_, note
    except Exception as e:
        r = {"id": cid_, "cand": dict(kw), "note": note, "status": "error: %r" % e}
    r.pop("_rec", None)
    results.append(r)
    with open("results_sweep3.json", "w") as f:
        json.dump({"metric_version": "v3-locked", "results": results}, f, indent=1)
    s = r.get("status", "?")
    msg = "id=%02d %s Dv=%.1f L=%d kap=%.2f eps=%.1e sg=%.2f -> %s" % (
        cid_, note, kw["Dv"], kw["L"], kw["kappa"], kw["eps"], kw["sigma"], s)
    if s == "ok":
        msg += (" | G1=%s G2=%s G5=%s r2=%.3f fl=%s per=%s tau=%s/%s sep=%.1f/%.1f rungs=%s"
                % (r["G1"], r["G2"], r["G5"], r["top_r2"], r["top_params"].get("n_flips"),
                   r["tau3_period"], r["tau1"], round(r["tau2"],1) if r["tau2"] else None,
                   r["sep12"], r["sep23"], r["rungs_visited"]))
    print(msg, flush=True)
print("sweep3 done in %.0fs" % (time.time() - t00), flush=True)
