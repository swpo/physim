"""sweep_region.py — focused sweep in the slow-market region (shardable).
usage: sweep_region.py SHARD NSHARDS
Theory-coordinate hypothesis being tested: HIGH LEAK weakens the waste price
signal -> slow market relaxation (tau3 up) at fixed turnover (tau2 fixed by
hazard) -> s23 >= 5. Sweep leak x rho x margin x hazard near that window.
"""
import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from probe import evaluate

WD = "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy"
shard, nsh = int(sys.argv[1]), int(sys.argv[2])
out = open(WD + f"/results_scan3_shard{shard}.jsonl", "a")

grid = []
for leak in (0.45, 0.55, 0.65):
    for rho in (1.8, 2.1, 2.4):
        for margin in (7.0, 8.5):
            for hz in (7e-4, 1e-3):
                grid.append(dict(rho=rho, yW=0.7, leak=leak, margin=margin,
                                 sig_mut=0.05, over=1.5, r0=0.006, hazard=hz))
mine = grid[shard::nsh]
print(f"shard {shard}/{nsh}: {len(mine)} candidates", flush=True)
for i, tc in enumerate(mine):
    t0 = time.time()
    try:
        res, _ = evaluate(tc, seed=0)
    except Exception as e:
        res = {"tc": tc, "fail": f"error:{e}"}
    res["phase"] = "scan3_region"
    out.write(json.dumps(res, default=float) + "\n"); out.flush()
    s = res.get("seps", {})
    tf = res.get("top_fit", {})
    print(f"[{i+1}/{len(mine)}] lk={tc['leak']} rho={tc['rho']} m={tc['margin']} hz={tc['hazard']} -> "
          f"{'FAIL:'+res['fail'] if 'fail' in res else ''} "
          f"lo={res.get('bimod',{}).get('share_lo')} pur={res.get('settle',{}).get('purity')} "
          f"fit={tf.get('model')}/{tf.get('r2')} tau3={res.get('tau_L3') and round(res['tau_L3'])} "
          f"t2={res.get('tau_L2')} s12={s.get('s12')} s23={s.get('s23')} s23L={s.get('s23_len')} "
          f"gap={res.get('return_gap') and round(res['return_gap'],3)} pass={res.get('pass')} ({time.time()-t0:.0f}s)", flush=True)
print("done", flush=True)
