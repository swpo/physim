"""g4d.py — GE4 battery (interior candidate, jitter-robust).
GE4: rho=2.3 yW=0.7 leak=0.55 margin=7.0 sig=0.05 over=1.5 r0=0.006
     hazard=5e-4 DW=0.02 L=96.  T1=40k + T2=20k = 60k (G5 budget).
usage: g4d.py IDX  0-3 seeds | 4-7 jitter J0-J3 (seed=J%2) | 8-11 rho curve
"""
import sys, time, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from probe_cert import evaluate_cert

WD = "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy"
GE4 = dict(rho=2.3, yW=0.7, leak=0.55, margin=7.0, sig_mut=0.05, over=1.5,
           r0=0.006, hazard=5e-4, DW=0.02, L=96)
SEARCHED = ["rho", "yW", "leak", "margin", "sig_mut", "over", "r0", "hazard", "DW"]

idx = int(sys.argv[1])
if idx < 4:
    tc, seed, tag = dict(GE4), idx, f"seed{idx}"
elif idx < 8:
    j = idx - 4
    rj = np.random.default_rng(3000 + j)
    tc = dict(GE4)
    for k in SEARCHED:
        tc[k] = float(tc[k] * rj.uniform(0.9, 1.1))
    seed = j % 2
    tag = f"jitter{j}_seed{seed}"
else:
    rhos = {8: 1.9, 9: 2.1, 10: 2.6, 11: 2.9}
    tc = dict(GE4, rho=rhos[idx]); seed = 0
    tag = f"rho{rhos[idx]}"
out = open(WD + f"/results_g4d_{idx}.jsonl", "a")
t0 = time.time()
res, _ = evaluate_cert(tc, seed=seed, T1=40000, T2=20000)
res["phase"] = "g4d_GE4"; res["tag"] = tag
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
