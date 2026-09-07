"""Offline absolute per-contract scores for the two completed BLOB2v2r2 rollouts.
Read-only: uses archived payloads + frozen truth ensembles; no models, no world calls.
"""
import json, sys, hashlib
from pathlib import Path
import numpy as np
sys.path.insert(0, "environments/physim")
from physim import blobround5 as R5
from physim import blobcore as B

RUNS = {
 "E1_928": dict(path=Path.home()/"v3work/ops/recovery_20260905/eval_fable_r2/E1/traces.jsonl",
                trace="0bdd699154ee4e1d96aac4e0961bc11d", world="p4g2_044", seed=928, menu="E1",
                payload=lambda cid: f"app/probe/payload_{cid}.json"),
 "E2_942": dict(path=Path.home()/"v3work/ops/recovery_20260905/eval_fable_r2/E2/traces.jsonl",
                trace="ae982494a72144c186f58a687a99cd33", world="p6g8_033", seed=942, menu="E2",
                payload=lambda cid: f"app/models/sub_{cid}_i1.json"),
}
OUT = Path(__file__).parent

def load_trace(path, tid):
    with open(path) as f:
        for line in f:
            if tid in line:
                outer = json.loads(line)
                for t in outer.get("traces", [outer]):
                    if t.get("id") == tid:
                        return t
    raise SystemExit("trace not found")

def crps_stats(mu, sig, legs):
    """Per-leg member-averaged Gaussian CRPS of the agent, plus the truth
    ensemble's own irreducible CRPS (member-vs-ensemble, leave-one-out gaussian)."""
    agent, aleatoric, spread, mae = [], [], [], []
    multi = len(legs) > 1
    for j, (lbl, mem) in enumerate(legs):
        m = np.asarray(mem, float)
        mu_j = np.asarray(mu[j] if multi else mu, float)
        sig_j = np.asarray(sig[j] if multi else sig, float)
        agent.append(float(np.mean([B.gauss_crps(mu_j, sig_j, y).mean() for y in m])))
        mae.append(float(np.mean([np.abs(mu_j - y).mean() for y in m])))
        if len(m) >= 2:
            loo = []
            for k in range(len(m)):
                rest = np.delete(m, k, axis=0)
                loo.append(B.gauss_crps(rest.mean(0), rest.std(0) + 1e-9, m[k]).mean())
            aleatoric.append(float(np.mean(loo)))
            spread.append(float(m.std(0).mean()))
        else:
            aleatoric.append(None); spread.append(0.0)
    return agent, aleatoric, spread, mae

results = {}
for name, r in RUNS.items():
    tr = load_trace(r["path"], r["trace"])
    ws = tr["info"]["physim"]["workspace"]; det = tr["info"]["physim"]["detail"]
    shapes = R5.payload_shapes5(r["world"], r["seed"], r["menu"])
    legs_all = R5.truth_legs(r["world"], r["seed"], r["menu"])
    hist_dev = {d: R5._hist_dev(r["world"], r["seed"], d) for d in (0, 1)}
    hist_glob = R5._hist_glob(r["world"], r["seed"])
    rows = {}
    for cid in R5.MENUS5[r["menu"]]:
        js = ws[r["payload"](cid)]
        parsed, why = B._parse_payload(js, shapes[cid])
        assert parsed is not None, (name, cid, why)
        mu, sig = parsed
        legs = legs_all[cid]
        agent, alea, spread, mae = crps_stats(mu, sig, legs)
        stored = det.get(f"{cid.lower()}_crps")
        # Scale for a unit-free view: typical variability of that observable in
        # the pre-anchor base record (climatological sd), per contract.
        if cid == "L2":
            scale = float(np.sqrt(np.maximum(hist_glob[:, :, 1], 0)).mean())
        elif cid == "L3S":
            scale = float(hist_glob[:, :, 0].std(0).mean())
        elif cid == "L3E":
            scale = None  # counts; use truth spread instead
        else:
            dev = 0 if cid in ("L1",) else 1 if cid in ("L4", "L4D") else det["instances"]["L3F"].get("device", 0)
            scale = float(hist_dev[dev].std(0).mean())
        crps_mean = float(np.mean(agent))
        rows[cid] = dict(
            agent_crps=crps_mean, stored_crps=stored,
            reproduces_stored=(stored is not None and abs(crps_mean - stored) < 2e-6),
            per_leg_agent_crps=agent, truth_loo_crps=alea, truth_member_spread=spread, mae=mae,
            n_members=[len(m) for _, m in legs],
            climatological_sd_scale=scale,
            crps_over_clim_sd=(crps_mean / scale) if scale else None,
            crps_over_truth_loo=(crps_mean / float(np.mean([a for a in alea if a])) if any(alea) else None),
            reference_best=min(det["ladders"][cid].values()),
        )
    results[name] = dict(world=r["world"], seed=r["seed"], menu=r["menu"], trace=r["trace"], contracts=rows)
    print(name)
    for cid, v in rows.items():
        print(f"  {cid:4s} crps={v['agent_crps']:.6f} stored={v['stored_crps']} ok={v['reproduces_stored']} "
              f"crps/clim_sd={v['crps_over_clim_sd']} crps/truth_loo={v['crps_over_truth_loo']} members={v['n_members']}")
(OUT/"absolute_scores.json").write_text(json.dumps(results, indent=2, default=str))
print("written", OUT/"absolute_scores.json")
