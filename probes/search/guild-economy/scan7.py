import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from probe_cert import evaluate_cert

WD = "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy"
shard = int(sys.argv[1])
out = open(WD + f"/results_scan7_shard{shard}.jsonl", "a")
cands = [
    dict(rho=1.8, yW=0.7, leak=0.55, margin=7.0, sig_mut=0.05, over=1.5, r0=0.006, hazard=7e-4),
    dict(rho=2.1, yW=0.7, leak=0.65, margin=7.0, sig_mut=0.05, over=1.5, r0=0.006, hazard=7e-4),
    dict(rho=1.9, yW=0.7, leak=0.60, margin=7.0, sig_mut=0.05, over=1.5, r0=0.006, hazard=6e-4),
    dict(rho=2.0, yW=0.7, leak=0.60, margin=7.0, sig_mut=0.05, over=1.5, r0=0.006, hazard=7e-4),
]
tc = cands[shard]
for seed in (0, 1):
    t0 = time.time()
    res, _ = evaluate_cert(tc, seed=seed)
    res["phase"] = "scan7_anchor_v2"
    out.write(json.dumps(res, default=float) + "\n"); out.flush()
    s = res.get("seps", {})
    tf = res.get("top_fit", {})
    print(f"seed={seed} rho={tc['rho']} lk={tc['leak']} hz={tc['hazard']} -> "
          f"{'FAIL:'+res['fail'] if 'fail' in res else ''} "
          f"lo={res.get('bimod',{}).get('share_lo')} pur={res.get('settle',{}).get('purity')} "
          f"fit={tf.get('model')}/{tf.get('r2')} tau3={res.get('tau_L3') and round(res['tau_L3'])} "
          f"t2={res.get('tau_L2')} t1=({res.get('tau_L1_R')},{res.get('tau_L1_W')}) "
          f"s12={s.get('s12')} s23={s.get('s23')} gap={res.get('return_gap') and round(res['return_gap'],3)} "
          f"drift={res.get('ctrl_drift') and round(res['ctrl_drift'],3)} pass={res.get('pass')} ({time.time()-t0:.0f}s)", flush=True)
print("done", flush=True)
