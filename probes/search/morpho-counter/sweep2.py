
"""sweep2.py -- full theory-coordinate sweep with runner v2 (measured tau1/tau2)."""
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
# A: band ratio x ladder
for Dv in [10.0, 11.0, 12.0, 15.0]:
    for L in [48, 64, 80]:
        add(Dv=Dv, L=L, kappa=0.5, eps=2.4e-3, n_pair=pair_for_L[L], note="A:band x ladder")
# A2: eps on 2x2 promising
for Dv in [11.0, 12.0]:
    for L in [64, 80]:
        for eps in [1.2e-3, 4.8e-3]:
            add(Dv=Dv, L=L, kappa=0.5, eps=eps, n_pair=pair_for_L[L], note="A2:eps")
# A3: F64 flagship eps
add(Dv=11.0, L=64, kappa=0.5, eps=3.4e-3, n_pair=(5, 6), note="A3:flagship eps")
add(Dv=10.0, L=48, kappa=0.5, eps=3.4e-3, n_pair=(4, 5), note="A3:flagship eps")
# B: kappa scan + extremes
for kap in [0.1, 0.2, 0.35, 0.65, 0.8, 0.9]:
    add(Dv=11.0, L=64, kappa=kap, eps=2.4e-3, n_pair=(5, 6), note="B:kappa")
# C: noise scan
for noise in [5e-4, 1e-3, 4e-3, 8e-3]:
    add(Dv=11.0, L=64, kappa=0.5, eps=2.4e-3, n_pair=(5, 6), noise=noise, note="C:noise")
# D: wide band (rung-skip expected)
add(Dv=25.0, L=96, kappa=0.5, eps=2.4e-3, n_pair=(7, 8), note="D:wide band")
add(Dv=25.0, L=96, kappa=0.5, eps=8.0e-3, n_pair=(7, 8), note="D:wide band")
add(Dv=25.0, L=64, kappa=0.5, eps=2.4e-3, n_pair=(5, 6), note="D:wide band")
# E: narrow band edge
add(Dv=9.0, L=64, kappa=0.5, eps=2.4e-3, n_pair=(5, 6), note="E:narrow band")
add(Dv=9.5, L=64, kappa=0.5, eps=2.4e-3, n_pair=(5, 6), note="E:narrow band")
# F: sigma (wavelength-control exponent)
for sg in [0.5, 0.75, 1.25, 1.5]:
    add(Dv=11.0, L=64, kappa=0.5, eps=2.4e-3, n_pair=(5, 6), sigma=sg, note="F:sigma")
# G: Dc (C spatial coupling)
for Dc in [1.0, 3.0]:
    add(Dv=11.0, L=64, kappa=0.5, eps=2.4e-3, n_pair=(5, 6), Dc=Dc, note="G:Dc")

print("total candidates:", len(cands), flush=True)
results = []
t00 = time.time()
for cid_, kw, note in cands:
    sigma, Dc = kw.pop("sigma"), kw.pop("Dc")
    note_s = note
    try:
        # sigma/Dc forwarded via cand dict -> eval_candidate passes to simulate?
        r = eval_candidate(dict(kw, sigma=sigma, Dc=Dc))
        r["id"], r["note"] = cid_, note_s
    except Exception as e:
        r = {"id": cid_, "cand": dict(kw, sigma=sigma, Dc=Dc), "note": note_s,
             "status": "error: %r" % e}
    r.pop("_rec", None)
    results.append(r)
    with open("results_sweep2.json", "w") as f:
        json.dump(results, f, indent=1)
    s = r.get("status", "?")
    msg = "id=%02d %s Dv=%.1f L=%d kap=%.2f eps=%.1e sg=%.2f Dc=%.0f -> %s" % (
        cid_, note_s, kw["Dv"], kw["L"], kw["kappa"], kw["eps"], sigma, Dc, s)
    if s == "ok":
        msg += (" | G1=%s G2=%s G5=%s r2=%.3f flips=%s per=%s tau=%s/%s rungs=%s sep=%.1f/%.1f"
                % (r["G1"], r["G2"], r["G5"], r["top_r2"], r["top_params"].get("n_flips"),
                   r["tau3_period"], r["tau1"], r["tau2"], r["rungs_visited"],
                   r["sep12"], r["sep23"]))
    print(msg, flush=True)
print("sweep2 done in %.0fs" % (time.time() - t00), flush=True)
