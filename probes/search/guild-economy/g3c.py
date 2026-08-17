"""g3c.py — G3 response curve on GE1 config (rho sweep, seed 0).
GE1: yW=0.7 leak=0.65 margin=7.0 sig=0.05 over=1.5 r0=0.006 hazard=4.5e-4
     DW=0.02 L=96; T1=45k+T2=15k.
usage: g3c.py IDX -> rho {2.0, 2.2, 2.4, 2.5}
"""
import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from probe_cert import evaluate_cert

WD = "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy"
rhos = (2.0, 2.2, 2.4, 2.5)
rho = rhos[int(sys.argv[1])]
tc = dict(rho=rho, yW=0.7, leak=0.65, margin=7.0, sig_mut=0.05, over=1.5,
          r0=0.006, hazard=4.5e-4, DW=0.02, L=96)
out = open(WD + f"/results_g3c_{int(sys.argv[1])}.jsonl", "a")
t0 = time.time()
res, _ = evaluate_cert(tc, seed=0, T1=45000, T2=15000)
res["phase"] = "g3c_rho_curve_GE1"
out.write(json.dumps(res, default=float) + "\n"); out.flush()
s = res.get("seps", {}); tf = res.get("top_fit", {})
print(f"rho={rho} -> {'FAIL:'+res.get('fail','') if 'fail' in res else ''} "
      f"fr*={res.get('fr_star') and round(res['fr_star'],3)} lo={res.get('bimod',{}).get('share_lo')} "
      f"fit={tf.get('model')}/{tf.get('r2')} tau3={res.get('tau_L3') and round(res['tau_L3'])} "
      f"t2={res.get('tau_L2')} s12={s.get('s12')} s23={s.get('s23')} "
      f"gap={res.get('return_gap') and round(res['return_gap'],3)} drift={res.get('ctrl_drift') and round(res['ctrl_drift'],3)} "
      f"pass={res.get('pass')} ({time.time()-t0:.0f}s)", flush=True)
