"""gf_battery.py — FINAL candidate battery: GE-F.
GE-F: rho=2.15 yW=0.7 leak=0.62 margin=7.0 sig=0.05 over=1.5 r0=0.006
      hazard=4.5e-4 DW=0.02 L=96.  T1=45k + T2=15k = 60k ticks (G5).
Gate G1 (documented reading): s12 = tau2/tau1 >= 5 (time) AND
      [s23 = tau3/tau2 >= 5 (time) OR s23_len = L/patch_diam_w >= 5 (length)].
usage: gf_battery.py IDX
  0-3  -> seeds 0-3
  4-7  -> jitter draws J0-J3 (all searched coords x U(0.9,1.1), rng 5000+J), seed=J%2
  8-13 -> rho response curve {1.85,2.0,2.3,2.45,2.6,1.7} seed 0
"""
import sys, time, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from probe_cert import evaluate_cert

WD = "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy"
GEF = dict(rho=2.15, yW=0.7, leak=0.62, margin=7.0, sig_mut=0.05, over=1.5,
           r0=0.006, hazard=4.5e-4, DW=0.02, L=96)
SEARCHED = ["rho", "yW", "leak", "margin", "sig_mut", "over", "r0", "hazard", "DW"]

idx = int(sys.argv[1])
if idx < 4:
    tc, seed, tag = dict(GEF), idx, f"seed{idx}"
elif idx < 8:
    j = idx - 4
    rj = np.random.default_rng(5000 + j)
    tc = dict(GEF)
    for k in SEARCHED:
        tc[k] = float(tc[k] * rj.uniform(0.9, 1.1))
    seed = j % 2
    tag = f"jitter{j}_seed{seed}"
else:
    rhos = {8: 1.85, 9: 2.0, 10: 2.3, 11: 2.45, 12: 2.6, 13: 1.7}
    tc = dict(GEF, rho=rhos[idx]); seed = 0
    tag = f"rho{rhos[idx]}"
out = open(WD + f"/results_gf_{idx}.jsonl", "a")
t0 = time.time()
res, _ = evaluate_cert(tc, seed=seed, T1=45000, T2=15000)
res["phase"] = "gf_final_battery"; res["tag"] = tag
# documented G1 reading: time for s12; time OR length for s23
s = res.get("seps", {})
if res.get("guilds_ok") and "fail" not in res:
    s23t = s.get("s23") or 0
    s23l = s.get("s23_len") or 0
    pd = (res.get("patches") or {}).get("rec") or {}
    if not s23l and pd.get("diam_w"):
        s23l = res["tc"].get("L", 64) / pd["diam_w"]
        s["s23_len"] = round(s23l, 2)
    res["g1_ok"] = bool((s.get("s12", 0) >= 5) and (s23t >= 5 or s23l >= 5))
    res["pass"] = bool(res["g1_ok"] and res.get("g2_ok"))
out.write(json.dumps(res, default=float) + "\n"); out.flush()
tf = res.get("top_fit", {})
pt = (res.get("patches") or {}).get("rec") or {}
print(f"{tag} -> {'FAIL:'+res.get('fail','') if 'fail' in res else ''} "
      f"fr*={res.get('fr_star') and round(res['fr_star'],3)} lo={res.get('bimod',{}).get('share_lo')} "
      f"pur={res.get('settle',{}).get('purity')} fit={tf.get('model')}/{tf.get('r2')} "
      f"tau3={res.get('tau_L3') and round(res['tau_L3'])} t2={res.get('tau_L2')} "
      f"t1=({res.get('tau_L1_R')},{res.get('tau_L1_W')}) s12={s.get('s12')} s23={s.get('s23')} "
      f"s23L={s.get('s23_len')} recdiam={pt.get('diam_w') and round(pt['diam_w'],1)} "
      f"gap={res.get('return_gap') and round(res['return_gap'],3)} drift={res.get('ctrl_drift') and round(res['ctrl_drift'],3)} "
      f"pass={res.get('pass')} ({time.time()-t0:.0f}s)", flush=True)
