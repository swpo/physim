"""g4e.py — GE1 extended battery: seeds 4-7 and jitters J4-J7.
GE1: rho=2.1 yW=0.7 leak=0.65 margin=7.0 sig=0.05 over=1.5 r0=0.006
     hazard=4.5e-4 DW=0.02 L=96, protocol T1=45k+T2=15k.
usage: g4e.py IDX   (0-3 -> seeds 4-7; 4-7 -> jitters J4-J7 seed=2+J%2)
"""
import sys, time, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from probe_cert import evaluate_cert

WD = "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy"
GE1 = dict(rho=2.1, yW=0.7, leak=0.65, margin=7.0, sig_mut=0.05, over=1.5,
           r0=0.006, hazard=4.5e-4, DW=0.02, L=96)
SEARCHED = ["rho", "yW", "leak", "margin", "sig_mut", "over", "r0", "hazard", "DW"]

idx = int(sys.argv[1])
if idx < 4:
    tc, seed, tag = dict(GE1), 4 + idx, f"seed{4+idx}"
else:
    j = idx  # J4-J7
    rj = np.random.default_rng(1000 + j)
    tc = dict(GE1)
    for k in SEARCHED:
        tc[k] = float(tc[k] * rj.uniform(0.9, 1.1))
    seed = 2 + (j % 2)
    tag = f"jitter{j}_seed{seed}"
out = open(WD + f"/results_g4e_{idx}.jsonl", "a")
t0 = time.time()
res, _ = evaluate_cert(tc, seed=seed, T1=45000, T2=15000)
res["phase"] = "g4e_GE1_extended"; res["tag"] = tag
out.write(json.dumps(res, default=float) + "\n"); out.flush()
s = res.get("seps", {}); tf = res.get("top_fit", {})
pt = (res.get("patches") or {}).get("rec") or {}
print(f"{tag} -> {'FAIL:'+res.get('fail','') if 'fail' in res else ''} "
      f"fr*={res.get('fr_star') and round(res['fr_star'],3)} lo={res.get('bimod',{}).get('share_lo')} "
      f"pur={res.get('settle',{}).get('purity')} fit={tf.get('model')}/{tf.get('r2')} "
      f"tau3={res.get('tau_L3') and round(res['tau_L3'])} t2={res.get('tau_L2')} "
      f"t1=({res.get('tau_L1_R')},{res.get('tau_L1_W')}) s12={s.get('s12')} s23={s.get('s23')} "
      f"recdiam={pt.get('diam_w') and round(pt['diam_w'],1)} "
      f"gap={res.get('return_gap') and round(res['return_gap'],3)} drift={res.get('ctrl_drift') and round(res['ctrl_drift'],3)} "
      f"pass={res.get('pass')} ({time.time()-t0:.0f}s)", flush=True)
