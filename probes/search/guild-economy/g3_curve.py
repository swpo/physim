"""g3_curve.py — G3 response curve: fr* (demand curve) and tau3 vs rho.
Fixed: yW=0.7 leak=0.65 margin=7 over=1.5 sig=0.05 r0=0.006 hz=5e-4 DW=0.02.
usage: g3_curve.py IDX  (IDX in 0..9 -> (rho, seed) pairs)
"""
import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from probe_cert import evaluate_cert

WD = "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy"
idx = int(sys.argv[1])
rhos = (1.5, 1.8, 2.1, 2.4, 2.7)
pairs = [(r, s) for s in (0, 1) for r in rhos]
rho, seed = pairs[idx]
tc = dict(rho=rho, yW=0.7, leak=0.65, margin=7.0, sig_mut=0.05, over=1.5,
          r0=0.006, hazard=5e-4, DW=0.02)
out = open(WD + f"/results_g3_{idx}.jsonl", "a")
t0 = time.time()
res, _ = evaluate_cert(tc, seed=seed, T1=45000, T2=15000)
res["phase"] = "g3_rho_curve"
out.write(json.dumps(res, default=float) + "\n"); out.flush()
s = res.get("seps", {}); tf = res.get("top_fit", {})
print(f"rho={rho} seed={seed} -> fr*={res.get('fr_star') and round(res['fr_star'],3)} "
      f"lo={res.get('bimod',{}).get('share_lo')} fit={tf.get('model')}/{tf.get('r2')} "
      f"tau3={res.get('tau_L3') and round(res['tau_L3'])} s12={s.get('s12')} s23={s.get('s23')} "
      f"gap={res.get('return_gap') and round(res['return_gap'],3)} pass={res.get('pass')} ({time.time()-t0:.0f}s)", flush=True)
