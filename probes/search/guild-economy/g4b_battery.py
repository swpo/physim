"""g4b_battery.py — G4 battery for GE-2.
GE-2: rho=2.2 yW=0.7 leak=0.60 margin=7.0 sig=0.05 over=1.5 r0=0.006
      hazard=4.5e-4 DW=0.02 L=96.  T1=42k settle + T2=18k kick = 60k ticks.
usage: g4b_battery.py IDX  (0-3 seeds; 4-9 jitter draws J0-J5, seed=J%2)
"""
import sys, time, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from probe_cert import evaluate_cert

WD = "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy"
GE2 = dict(rho=2.2, yW=0.7, leak=0.60, margin=7.0, sig_mut=0.05, over=1.5,
           r0=0.006, hazard=4.5e-4, DW=0.02, L=96)
SEARCHED = ["rho", "yW", "leak", "margin", "sig_mut", "over", "r0", "hazard", "DW"]

idx = int(sys.argv[1])
if idx < 4:
    tc, seed, tag = dict(GE2), idx, f"seed{idx}"
else:
    j = idx - 4
    rj = np.random.default_rng(2000 + j)
    tc = dict(GE2)
    for k in SEARCHED:
        tc[k] = float(tc[k] * rj.uniform(0.9, 1.1))
    seed = j % 2
    tag = f"jitter{j}_seed{seed}"
out = open(WD + f"/results_g4b_{idx}.jsonl", "a")
t0 = time.time()
res, _ = evaluate_cert(tc, seed=seed, T1=42000, T2=18000)
res["phase"] = "g4b_battery_GE2"; res["tag"] = tag
out.write(json.dumps(res, default=float) + "\n"); out.flush()
s = res.get("seps", {}); tf = res.get("top_fit", {})
print(f"{tag} -> {'FAIL:'+res.get('fail','') if 'fail' in res else ''} "
      f"fr*={res.get('fr_star') and round(res['fr_star'],3)} lo={res.get('bimod',{}).get('share_lo')} "
      f"pur={res.get('settle',{}).get('purity')} fit={tf.get('model')}/{tf.get('r2')} "
      f"tau3={res.get('tau_L3') and round(res['tau_L3'])} t2={res.get('tau_L2')} "
      f"t1=({res.get('tau_L1_R')},{res.get('tau_L1_W')}) s12={s.get('s12')} s23={s.get('s23')} "
      f"gap={res.get('return_gap') and round(res['return_gap'],3)} drift={res.get('ctrl_drift') and round(res['ctrl_drift'],3)} "
      f"pass={res.get('pass')} ({time.time()-t0:.0f}s)", flush=True)
