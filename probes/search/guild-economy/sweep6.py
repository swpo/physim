import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from probe_cert import evaluate_cert

WD = "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy"
shard, nsh = int(sys.argv[1]), int(sys.argv[2])
out = open(WD + f"/results_scan6_shard{shard}.jsonl", "a")

grid = []
for rho in (1.9, 2.1, 2.3):
    for leak in (0.60, 0.65):
        for hz in (5.5e-4, 6.5e-4):
            grid.append(dict(rho=rho, yW=0.7, leak=leak, margin=7.0,
                             sig_mut=0.05, over=1.5, r0=0.006, hazard=hz))
mine = grid[shard::nsh]
print(f"shard {shard}/{nsh}: {len(mine)}", flush=True)
for i, tc in enumerate(mine):
    t0 = time.time()
    try:
        res, _ = evaluate_cert(tc, seed=0, T1=40000, T2=20000)
    except Exception as e:
        res = {"tc": tc, "fail": f"error:{e}"}
    res["phase"] = "scan6_cert40k"
    out.write(json.dumps(res, default=float) + "\n"); out.flush()
    s = res.get("seps", {})
    tf = res.get("top_fit", {})
    print(f"[{i+1}/{len(mine)}] rho={tc['rho']} lk={tc['leak']} hz={tc['hazard']} -> "
          f"{'FAIL:'+res['fail'] if 'fail' in res else ''} "
          f"lo={res.get('bimod',{}).get('share_lo')} pur={res.get('settle',{}).get('purity')} "
          f"fit={tf.get('model')}/{tf.get('r2')} (full {res.get('top_fit_full',{}).get('model')}/{res.get('top_fit_full',{}).get('r2')}) "
          f"tau3={res.get('tau_L3') and round(res['tau_L3'])} t2={res.get('tau_L2')} t1=({res.get('tau_L1_R')},{res.get('tau_L1_W')}) "
          f"s12={s.get('s12')} s23={s.get('s23')} gap={res.get('return_gap') and round(res['return_gap'],3)} "
          f"drift={res.get('ctrl_drift') and round(res['ctrl_drift'],3)} pass={res.get('pass')} ({time.time()-t0:.0f}s)", flush=True)
print("done", flush=True)
