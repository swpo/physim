"""probe_S -- how far an aimed 300-nat input moves the substrate inside the target cell (public world, tiny size).

    python -B probe_S.py [size] [members] [nats]         (defaults 64, 8, 300)

Used to place the thresholds of the gated candidates (`dorm`: below the passive range, `store`: above it) where an
aimed input reaches them and passive evolution does not. For each member: formation (150 ticks), then three twins
with the same noise keys: none, feed, starve (screen.py's aimed programs: 10 ticks on the bumps within 8 px of the
largest cell). Reported per arm and tick: quantiles over members of the min / median / max of S over the pixels
of the target cell (phi > 0.5 within 12 px of its start centroid), and S quantiles over all in-cell pixels.
Writes results/probe_S.json.
"""
import json
import os
import sys

import numpy as np

import sublevel as SL
from sublevel import MJ, MW
import screen as SC

SIZE = int(sys.argv[1]) if len(sys.argv) > 1 else 64
M = int(sys.argv[2]) if len(sys.argv) > 2 else 8
NATS = float(sys.argv[3]) if len(sys.argv) > 3 else 300.0


def main():
    cfg = SL.small_cfg(SIZE)
    spec, parts = SL.build(cfg)
    w = MW.MapWorld(spec, world_seed=0)
    d = w.designer
    K = parts["tracker"].K
    ens = d.ensemble(M, seed=(77, 1))
    ens, rec0 = d.rollout(ens, None, T=SC.T0, rec=("L1",))
    P, tgt = SC.programs(cfg, rec0["L1"][:, -1], K, NATS, np.random.default_rng(1))
    yy, xx = np.mgrid[0:cfg.H, 0:cfg.W].astype(float)
    out = {"size": SIZE, "members": M, "nats": NATS, "amp": [t["amp"] for t in tgt], "arms": {}}
    for arm, ci in (("none", 0), ("feed", 2), ("starve", 3)):
        e = ens.clone(rep=1)
        Pd = np.concatenate([np.zeros((M, SC.T0, cfg.m)), P[:, ci]], 1)       # absolute agent time
        rows = {}
        for t in (0, 2, 5, 10, 15, 20, 32):
            if t > 0:
                e, _ = d.rollout(e, Pd, t_end=SC.T0 + t, rec=())
            x = {k: np.asarray(v) for k, v in e.x.items()}
            mn, md, mx, allin = [], [], [], []
            for i in range(M):
                dd = np.hypot((yy - tgt[i]["cy"] + cfg.H / 2) % cfg.H - cfg.H / 2, (xx - tgt[i]["cx"] + cfg.W / 2) % cfg.W - cfg.W / 2)
                m = (x["phi"][i] > 0.5) & (dd <= 12.0)
                if m.sum() == 0:
                    continue
                s = x["S"][i][m]
                mn.append(s.min()); md.append(np.median(s)); mx.append(s.max())
                allin.append(x["S"][i][x["phi"][i] > 0.5])
            allin = np.concatenate(allin)
            rows[str(t)] = {"target_min_S_q10_q50_q90": np.quantile(mn, [0.1, 0.5, 0.9]).round(4).tolist(),
                            "target_median_S_q10_q50_q90": np.quantile(md, [0.1, 0.5, 0.9]).round(4).tolist(),
                            "target_max_S_q10_q50_q90": np.quantile(mx, [0.1, 0.5, 0.9]).round(4).tolist(),
                            "all_cells_S_q01_q05_q50_q95_q99": np.quantile(allin, [0.01, 0.05, 0.5, 0.95, 0.99]).round(4).tolist()}
            print(arm, t, rows[str(t)], flush=True)
        out["arms"][arm] = rows
    json.dump(out, open(os.path.join(SL.HERE, "results", "probe_S.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
