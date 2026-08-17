"""g4_axis.py — single-axis ±10% jitter battery for GE1.
GE1: rho=2.1 yW=0.7 leak=0.65 margin=7.0 sig=0.05 over=1.5 r0=0.006
     hazard=4.5e-4 DW=0.02 L=96; T1=45k+T2=15k; seed 0.
usage: g4_axis.py IDX (0-11)
"""
import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from probe_cert import evaluate_cert

WD = "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy"
GE1 = dict(rho=2.1, yW=0.7, leak=0.65, margin=7.0, sig_mut=0.05, over=1.5,
           r0=0.006, hazard=4.5e-4, DW=0.02, L=96)
axes = [("yW", 0.9), ("yW", 1.1), ("leak", 0.9), ("leak", 1.1),
        ("margin", 0.9), ("margin", 1.1), ("hazard", 0.9), ("hazard", 1.1),
        ("sig_mut", 0.9), ("sig_mut", 1.1), ("DW", 0.9), ("DW", 1.1)]
idx = int(sys.argv[1])
ax, f = axes[idx]
tc = dict(GE1); tc[ax] = float(tc[ax] * f)
tag = f"{ax}x{f}"
out = open(WD + f"/results_g4ax_{idx}.jsonl", "a")
t0 = time.time()
res, _ = evaluate_cert(tc, seed=0, T1=45000, T2=15000)
res["phase"] = "g4_axis_jitter"; res["tag"] = tag
s = res.get("seps", {})
if res.get("guilds_ok") and "fail" not in res:
    pd = (res.get("patches") or {}).get("rec") or {}
    s23l = (res["tc"].get("L", 64) / pd["diam_w"]) if pd.get("diam_w") else 0
    s["s23_len"] = round(s23l, 2)
    res["g1_ok"] = bool((s.get("s12", 0) >= 5) and ((s.get("s23") or 0) >= 5 or s23l >= 5))
    res["pass"] = bool(res["g1_ok"] and res.get("g2_ok"))
out.write(json.dumps(res, default=float) + "\n"); out.flush()
tf = res.get("top_fit", {})
print(f"{tag} -> {'FAIL:'+res.get('fail','') if 'fail' in res else ''} "
      f"fr*={res.get('fr_star') and round(res['fr_star'],3)} lo={res.get('bimod',{}).get('share_lo')} "
      f"fit={tf.get('model')}/{tf.get('r2')} tau3={res.get('tau_L3') and round(res['tau_L3'])} "
      f"t2={res.get('tau_L2')} s12={s.get('s12')} s23={s.get('s23')} s23L={s.get('s23_len')} "
      f"gap={res.get('return_gap') and round(res['return_gap'],3)} drift={res.get('ctrl_drift') and round(res['ctrl_drift'],3)} "
      f"pass={res.get('pass')} ({time.time()-t0:.0f}s)", flush=True)
