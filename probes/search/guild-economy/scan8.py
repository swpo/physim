import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from probe_cert import evaluate_cert

WD = "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy"
shard, nsh = int(sys.argv[1]), int(sys.argv[2])
out = open(WD + f"/results_scan8_shard{shard}.jsonl", "a")

grid = []
for DW in (0.02, 0.06):
    for rho, leak in [(1.8, 0.55), (2.1, 0.65), (2.4, 0.75), (2.7, 0.85)]:
        for hz in (5e-4, 7e-4):
            grid.append(dict(rho=rho, yW=0.7, leak=leak, margin=7.0,
                             sig_mut=0.05, over=1.5, r0=0.006, hazard=hz, DW=DW))
mine = grid[shard::nsh]
print(f"shard {shard}/{nsh}: {len(mine)}", flush=True)
for i, tc in enumerate(mine):
    t0 = time.time()
    try:
        res, _ = evaluate_cert(tc, seed=0)
    except Exception as e:
        res = {"tc": tc, "fail": f"error:{e}"}
    res["phase"] = "scan8_DW_leak"
    out.write(json.dumps(res, default=float) + "\n"); out.flush()
    s = res.get("seps", {})
    tf = res.get("top_fit", {})
    pt = res.get("patches", {})
    dw_r = pt.get("rec", {}) or {}
    print(f"[{i+1}/{len(mine)}] DW={tc['DW']} rho={tc['rho']} lk={tc['leak']} hz={tc['hazard']} -> "
          f"{'FAIL:'+res.get('fail','') if 'fail' in res else ''} "
          f"lo={res.get('bimod',{}).get('share_lo')} fit={tf.get('model')}/{tf.get('r2')} "
          f"tau3={res.get('tau_L3') and round(res['tau_L3'])} t2={res.get('tau_L2')} "
          f"s12={s.get('s12')} s23={s.get('s23')} rec_diam={dw_r.get('diam_w') and round(dw_r['diam_w'],1)} "
          f"gap={res.get('return_gap') and round(res['return_gap'],3)} drift={res.get('ctrl_drift') and round(res['ctrl_drift'],3)} "
          f"pass={res.get('pass')} ({time.time()-t0:.0f}s)", flush=True)
print("done", flush=True)
