
"""sweep.py — theory-coordinate sweep for slime lifecycle. Usage: sweep.py <chunk.json> <out.json>"""
import sys, json, time
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/slime-lifecycle")
from slime import run, DEFAULTS
from measure import candidate_metrics, gate_check

chunk_file, out_file = sys.argv[1], sys.argv[2]
cands = json.load(open(chunk_file))
results = []
for c in cands:
    pp = dict(c["params"])
    T = int(c.get("T", 40000))
    t0 = time.time()
    try:
        o = run(params=pp, T=T, seed=int(c.get("seed", 0)), rec=20)
        m = candidate_metrics(o, rec=20)
        g = gate_check(m)
    except Exception as e:
        m, g = {"ok": False, "why": "exception:%s" % e}, {}
    wall = time.time() - t0
    rec_out = dict(id=c["id"], theory=c.get("theory", {}), params=pp, T=T,
                   seed=c.get("seed", 0), wall_s=round(wall, 1), metrics=m, gates=g)
    results.append(rec_out)
    l3 = (m.get("l3") or {}).get("aggm", {}).get("fit", {})
    print("[%s] ok=%s why=%-8s nfam=%-3s top=%s r2=%s G1=%s G2=%s wall=%.0fs" % (
        c["id"], m.get("ok"), m.get("why", ""), m.get("n_famines"),
        l3.get("model"), l3.get("r2"), g.get("G1"), g.get("G2"), wall), flush=True)

def clean(x):
    if isinstance(x, dict): return {k: clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [clean(v) for v in x]
    if isinstance(x, (np.floating,)): return float(x)
    if isinstance(x, (np.integer,)): return int(x)
    if isinstance(x, np.bool_): return bool(x)
    return x

json.dump(clean(results), open(out_file, "w"), indent=1)
print("wrote", out_file)
