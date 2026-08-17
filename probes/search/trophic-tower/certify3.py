
import sys, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
from trophic_core import *
from hier_metrics import macro_period_quality
WD = "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower"
TCSTAR = json.load(open(WD + "/tcstar.json"))

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
        c = int(len(rec["meanP"]) * 0.35)
        pq = macro_period_quality(rec["meanP"][c:], dt=0.5)
        m["acfT3"] = pq["period"]; m["acfq3"] = pq["q"]; m["acfn3"] = pq["n_cycles"]
    except Exception as e:
        m = dict(status="error", error=str(e)); rec = None
    results.append(dict(stage="cert3", tag=tag, tc=dict(tc), seed=seed, L=L,
                        nticks=nticks, **jsonable(m)))
    tf = m.get("top_fit", {})
    both = m.get("G1") and m.get("G2")
    print(f"[{tag}] sd={seed} L={L}: {m.get('status')} top={tf.get('model')}/{tf.get('r2')} "
          f"T3={m.get('T3') and round(m['T3'],1)} T2={m.get('T2') and round(m['T2'],1)} "
          f"t1={m.get('tau1') and round(m['tau1'],2)} s12={m.get('sep12') and round(m['sep12'],1)} "
          f"s23={m.get('sep23') and round(m['sep23'],1)} lam={m.get('ell2_spec') and round(m['ell2_spec'],1)} "
          f"ell1={m.get('ell1') and round(m['ell1'],1)} des={m.get('desync') and round(m['desync'],2)} "
          f"pp={m.get('patch_powerlaw')} G1={m.get('G1')} G2={m.get('G2')} {'BOTH' if both else ''}", flush=True)
    json.dump(results, open(WD + "/results_cert3.json", "w"), indent=1)
    return m

print("=== extra jitter (6 more draws) ===")
jrng = np.random.default_rng(31337)
jok = 0
for j in range(6):
    tc = {k: float(v * (1 + 0.1 * (2 * jrng.random() - 1))) for k, v in TCSTAR.items()}
    m = probe(tc, 40 + j, f"jitB{j}")
    if m.get("G1") and m.get("G2"): jok += 1
print(f"extra JITTER: {jok}/6 BOTH")

print("=== L=96 at TC* (2 seeds) ===")
for sd in (0, 1):
    probe(TCSTAR, sd, "L96", L=96)
print("DONE cert3")
