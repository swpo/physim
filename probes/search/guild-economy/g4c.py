"""g4c.py — refined candidates battery (GE-3 family), seeds 0-3.
usage: g4c.py IDX  (IDX 0-7: cand = IDX//4, seed = IDX%4)
"""
import sys, time, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from probe_cert import evaluate_cert

WD = "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy"
cands = [
    ("GE1b", dict(rho=2.1, yW=0.7, leak=0.65, margin=7.0, sig_mut=0.05, over=1.5,
                  r0=0.006, hazard=4e-4, DW=0.02, L=96)),
    ("GE3",  dict(rho=2.1, yW=0.75, leak=0.60, margin=7.0, sig_mut=0.05, over=1.5,
                  r0=0.006, hazard=4e-4, DW=0.02, L=96)),
]
idx = int(sys.argv[1])
tag, tc = cands[idx // 4]
seed = idx % 4
out = open(WD + f"/results_g4c_{idx}.jsonl", "a")
t0 = time.time()
res, _ = evaluate_cert(tc, seed=seed, T1=48000, T2=12000)
res["phase"] = "g4c_refined"; res["tag"] = f"{tag}_seed{seed}"
out.write(json.dumps(res, default=float) + "\n"); out.flush()
s = res.get("seps", {}); tf = res.get("top_fit", {})
pt = (res.get("patches") or {}).get("rec") or {}
print(f"{tag} seed{seed} -> {'FAIL:'+res.get('fail','') if 'fail' in res else ''} "
      f"fr*={res.get('fr_star') and round(res['fr_star'],3)} lo={res.get('bimod',{}).get('share_lo')} "
      f"pur={res.get('settle',{}).get('purity')} fit={tf.get('model')}/{tf.get('r2')} "
      f"tau3={res.get('tau_L3') and round(res['tau_L3'])} t2={res.get('tau_L2')} "
      f"t1=({res.get('tau_L1_R')},{res.get('tau_L1_W')}) s12={s.get('s12')} s23={s.get('s23')} "
      f"rec_diam={pt.get('diam_w') and round(pt['diam_w'],1)} rec_n={pt.get('n')} "
      f"gap={res.get('return_gap') and round(res['return_gap'],3)} drift={res.get('ctrl_drift') and round(res['ctrl_drift'],3)} "
      f"pass={res.get('pass')} ({time.time()-t0:.0f}s)", flush=True)
