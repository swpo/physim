import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from probe_cert import evaluate_cert

WD = "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy"
shard = int(sys.argv[1])
out = open(WD + f"/results_scan9_shard{shard}.jsonl", "a")
cands = [
    dict(rho=2.1, yW=0.7, leak=0.65, margin=7.0, sig_mut=0.05, over=1.5, r0=0.006, hazard=5e-4, DW=0.02),
    dict(rho=2.7, yW=0.7, leak=0.85, margin=7.0, sig_mut=0.05, over=1.5, r0=0.006, hazard=5e-4, DW=0.02),
    dict(rho=2.1, yW=0.7, leak=0.65, margin=7.0, sig_mut=0.05, over=1.5, r0=0.006, hazard=4e-4, DW=0.02),
    dict(rho=2.4, yW=0.7, leak=0.75, margin=7.0, sig_mut=0.05, over=1.5, r0=0.006, hazard=5e-4, DW=0.02),
]
tc = cands[shard]
t0 = time.time()
res, _ = evaluate_cert(tc, seed=0, T1=45000, T2=15000)
res["phase"] = "scan9_T45k"
out.write(json.dumps(res, default=float) + "\n"); out.flush()
s = res.get("seps", {})
tf = res.get("top_fit", {})
print(f"rho={tc['rho']} lk={tc['leak']} hz={tc['hazard']} -> "
      f"{'FAIL:'+res.get('fail','') if 'fail' in res else ''} "
      f"lo={res.get('bimod',{}).get('share_lo')} pur={res.get('settle',{}).get('purity')} "
      f"fit={tf.get('model')}/{tf.get('r2')} tau3={res.get('tau_L3') and round(res['tau_L3'])} "
      f"t2={res.get('tau_L2')} t1=({res.get('tau_L1_R')},{res.get('tau_L1_W')}) "
      f"s12={s.get('s12')} s23={s.get('s23')} gap={res.get('return_gap') and round(res['return_gap'],3)} "
      f"drift={res.get('ctrl_drift') and round(res['ctrl_drift'],3)} pass={res.get('pass')} ({time.time()-t0:.0f}s)", flush=True)
print("done", flush=True)
