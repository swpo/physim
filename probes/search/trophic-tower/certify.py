
import sys, json, time
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
from trophic_core import *
from hier_metrics import macro_period_quality
WD = "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower"

TCSTAR = dict(sigma1=4.5, mu1=0.4, d1=0.4, sigma2=2.0, eta2=0.45, rho=0.03,
              DH=0.05, Delta=4.0, nu=0.02)

def jsonable(m):
    def cv(v):
        if isinstance(v, (np.floating, np.integer)): return float(v)
        if isinstance(v, dict): return {k: cv(x) for k, x in v.items()}
        if isinstance(v, (list, tuple)): return [cv(x) for x in v]
        return v
    return {k: cv(v) for k, v in m.items() if k not in ("finalR","finalH","finalP")}

results = []

def probe(tc, seed, tag, L=64, nticks=56000):
    try:
        rec, m = run_and_measure_teacup(tc, L=L, nticks=nticks, seed=seed)
        # ACF period of meanP for the response curve (consistent estimator)
        c = int(len(rec["meanP"]) * 0.35)
        pq = macro_period_quality(rec["meanP"][c:], dt=0.5)
        m["acfT3"] = pq["period"]; m["acfq3"] = pq["q"]; m["acfn3"] = pq["n_cycles"]
    except Exception as e:
        m = dict(status="error", error=str(e)); rec = None
    row = dict(stage="cert", tag=tag, tc=dict(tc), seed=seed, L=L, nticks=nticks, **jsonable(m))
    results.append(row)
    tf = m.get("top_fit", {})
    both = m.get("G1") and m.get("G2")
    print(f"[{tag}] sd={seed}: {m.get('status')} top={tf.get('model')}/{tf.get('r2')} "
          f"T3={m.get('T3') and round(m['T3'],1)} acfT3={m.get('acfT3') and round(m['acfT3'],1)} "
          f"q={m.get('acfq3') and round(m['acfq3'],2)} T2={m.get('T2') and round(m['T2'],1)} "
          f"t1={m.get('tau1') and round(m['tau1'],2)} s12={m.get('sep12') and round(m['sep12'],1)} "
          f"s23={m.get('sep23') and round(m['sep23'],1)} cv={m.get('spatial_cv') and round(m['spatial_cv'],2)} "
          f"np={m.get('npatch_med')} G1={m.get('G1')} G2={m.get('G2')} {'BOTH' if both else ''}", flush=True)
    json.dump(results, open(WD + "/results_cert.json", "w"), indent=1)
    return m

print("=== A) 4 seeds at TC* ===")
seed_ok = 0
for sd in range(4):
    m = probe(TCSTAR, sd, "seeds")
    if m.get("G1") and m.get("G2"): seed_ok += 1
print(f"SEEDS: {seed_ok}/4 BOTH")

print("=== B) +-10% jitter of ALL searched params (3 draws) ===")
jit_ok = 0
jrng = np.random.default_rng(777)
for j in range(3):
    tc = {k: float(v * (1 + 0.1 * (2 * jrng.random() - 1))) for k, v in TCSTAR.items()}
    m = probe(tc, 10 + j, f"jitter{j}")
    if m.get("G1") and m.get("G2"): jit_ok += 1
print(f"JITTER: {jit_ok}/3 BOTH")

print("=== C) response curve: rho (predator metabolic price) ===")
for rho in (0.022, 0.026, 0.030, 0.034, 0.038):
    for sd in (0, 1):
        tc = dict(TCSTAR); tc["rho"] = rho
        probe(tc, sd, f"rc_rho={rho}")

print("=== D) response curve: eta2 (predator efficiency) ===")
for e2 in (0.40, 0.43, 0.45, 0.47):
    tc = dict(TCSTAR); tc["eta2"] = e2
    probe(tc, 0, f"rc_eta2={e2}")
print("DONE cert")
