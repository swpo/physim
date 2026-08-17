"""sweep_main.py — main theory-coordinate sweep (shardable).
usage: sweep_main.py SHARD NSHARDS
"""
import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from probe import evaluate
import numpy as np

WD = "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy"
shard, nsh = int(sys.argv[1]), int(sys.argv[2])
out = open(WD + f"/results_scan2_shard{shard}.jsonl", "a")

grid = []
for margin in (6.0, 8.0):
    for rho in (1.8, 2.2, 2.6):
        for leak in (0.25, 0.4, 0.55):
            for hz in (4e-4, 7e-4):
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
    res["phase"] = "scan2_main"
    out.write(json.dumps(res, default=float) + "\n"); out.flush()
    s = res.get("seps", {})
    tf = res.get("top_fit", {})
    print(f"[{i+1}/{len(mine)}] m={tc['margin']} rho={tc['rho']} lk={tc['leak']} hz={tc['hazard']} -> "
          f"{'FAIL:'+res['fail'] if 'fail' in res else ''} "
          f"bimod={res.get('bimod',{}).get('bimod')} lo={res.get('bimod',{}).get('share_lo')} "
          f"fit={tf.get('model')}/{tf.get('r2')} tau3={res.get('tau_L3')} "
          f"t2={res.get('tau_L2')} t1=({res.get('tau_L1_R')},{res.get('tau_L1_W')}) "
          f"s12={s.get('s12')} s23={s.get('s23')} pass={res.get('pass')} ({time.time()-t0:.0f}s)", flush=True)
print("done", flush=True)
