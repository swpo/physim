"""physim.report — collect eval outputs + baselines into the difficulty report."""
from __future__ import annotations
import glob, json, os
import numpy as np

def collect_traces(outputs_glob="/Users/spoho/Documents/prime/test/physim/outputs/*/*"):
    rows = []
    for d in sorted(glob.glob(outputs_glob), key=os.path.getmtime):
        cfgp = os.path.join(d, "config.toml")
        model = harness = diff = None
        if os.path.exists(cfgp):
            txt = open(cfgp).read()
            for line in txt.splitlines():
                line = line.strip()
                if line.startswith("model ="): model = line.split("=",1)[1].strip().strip('"')
                if line.startswith("difficulty ="): diff = line.split("=",1)[1].strip().strip('"')
                if line.startswith("id =") and harness is None and "[env.agent" in txt[:txt.find(line)]:
                    pass
        tp = os.path.join(d, "traces.jsonl")
        if not os.path.exists(tp): continue
        for l in open(tp):
            try: rec = json.loads(l)
            except json.JSONDecodeError: continue
            for itr in rec.get("traces", []):
                rew = (itr.get("rewards") or {}).get("accuracy", {}).get("score")
                met = itr.get("metrics") or {}
                info = (itr.get("info") or {}).get("physim") or {}
                if rew is None: continue
                rows.append(dict(
                    run_dir=d.split("outputs/")[-1], model=model,
                    difficulty=info.get("difficulty") or diff,
                    seed=info.get("world_seed"),
                    reward=rew, coverage=met.get("coverage"),
                    turns=met.get("turns_used"), budget=met.get("budget_used_frac"),
                    S1=met.get("acc_S1"), S2=met.get("acc_S2"), S3=met.get("acc_S3"),
                    S4=met.get("acc_S4"),
                    replication=met.get("replication_ref"),
                ))
    return rows

def summarize(rows):
    from collections import defaultdict
    agg = defaultdict(list)
    for r in rows:
        agg[(r["model"], r["difficulty"])].append(r)
    out = []
    for (m, d), rs in sorted(agg.items()):
        out.append(dict(model=m, difficulty=d, n=len(rs),
            reward=float(np.mean([r["reward"] for r in rs])),
            reward_sd=float(np.std([r["reward"] for r in rs])),
            coverage=float(np.mean([r["coverage"] or 0 for r in rs])),
            S1=float(np.mean([r["S1"] or 0 for r in rs])),
            S2=float(np.mean([r["S2"] or 0 for r in rs])),
            S3=float(np.mean([r["S3"] or 0 for r in rs])),
            S4=float(np.mean([r["S4"] for r in rs if r["S4"] is not None])) if any(r["S4"] is not None for r in rs) else None,
            budget=float(np.mean([r["budget"] or 0 for r in rs])),
        ))
    return out
