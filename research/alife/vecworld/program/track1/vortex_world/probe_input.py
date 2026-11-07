"""probe_input -- does an aimed stir show up at level 2 within budget? (designer twin runs, 64^2, eps 0.2)

    python probe_input.py [n_states] [R] [T]           (defaults 6 8 16)

Starts: level-0 states saved by pilot.py (sel arm, seed 0, branch points 4 .. 4 + n_states - 1).
Target: the heaviest kind-b vortex of the start's vortex list (level 1); its sign is read from level 0
(privileged; the vortex list carries |om| only). Aim: the stirring coefficient whose bump centre is
nearest to the vortex. Programs (ticks 0 and 1, open loop):
    none
    cut05   u_j = -sign * 0.05   (2 x 50 = 100 nats)
    feed05  u_j = +sign * 0.05   (100 nats)
    cut15   u_j = -sign * 0.15   (2 x 450 = 900 nats)
Every program runs R replicates with the same fresh keys (designer common random numbers, variance
reduction only). Effect at h ticks: mean over replicates and starts of y_prog - y_none for y = (N, s_b),
in units of the no-input replicate sd (pooled over starts) and of sqrt(Ve) from analyse.py (w = 2).
Writes results/probe_input.json.
"""
import json
import os
import sys

import _paths
import jax
import jax.numpy as jnp
import numpy as np

import vw
import vortex_jax as VJ
import vortex_world as VW

NS = int(sys.argv[1]) if len(sys.argv) > 1 else 6
R = int(sys.argv[2]) if len(sys.argv) > 2 else 8
T = int(sys.argv[3]) if len(sys.argv) > 3 else 16
H = 64
PROGS = {"none": 0.0, "cut05": -0.05, "feed05": 0.05, "cut15": -0.15}


def main():
    D = np.load(os.path.join(_paths.RESULTS, f"pilot_H{H}.npz"))
    cfg = VJ.Config(H=H, W=H, G=H // 16)
    specs, parts = VW.build(cfg)
    w = VW.MapWorld(specs["kinds"], world_seed=0, params={k: jnp.asarray(v, jnp.float64) for k, v in dict(VJ.THETA, eps=0.2).items()})
    d = w.designer
    K = parts["tracker"].K
    budget = VW.nats_budget(cfg)
    centres = VJ.bump_centres(cfg)
    pts = list(range(4, 4 + NS))
    x0 = {k: np.asarray(D[f"sel_x_{k}"][pts, 0], np.float64) for k in ("om", "Y", "a", "b", "t")}
    start = d.from_states(x0, keys=vw.member_keys(vw.make_key(91, 0), NS))
    L1 = start.level(1).reshape(NS, K, vw.objects.NF)
    aims, signs, info = [], [], []
    for i in range(NS):
        T1 = L1[i]
        cand = np.flatnonzero((T1[:, 0] > 0.5) & (T1[:, 2] > 0.5))
        if cand.size == 0:
            cand = np.flatnonzero(T1[:, 0] > 0.5)
        s = cand[np.argmax(T1[cand, 1])]
        cx = (np.arctan2(T1[s, 4], T1[s, 3]) * H / (2 * np.pi)) % H
        cy = (np.arctan2(T1[s, 6], T1[s, 5]) * H / (2 * np.pi)) % H
        dd = np.hypot((centres[:, 0] - cy + H / 2) % H - H / 2, (centres[:, 1] - cx + H / 2) % H - H / 2)
        j = int(np.argmin(dd))
        sg = float(np.sign(x0["om"][i][int(round(cy)) % H, int(round(cx)) % H]))
        aims.append(j)
        signs.append(sg)
        info.append({"t": float(x0["t"][i]), "target_mass": float(T1[s, 1]), "target_frac_b": float(T1[s, 2]),
                     "bump": j, "dist_px": float(dd[j]), "sign": sg, "N": int((T1[:, 0] > 0.5).sum())})
    keys = vw.member_keys(vw.make_key(91, 1), NS * R)
    res = {}
    for name, amp in PROGS.items():
        P = np.zeros((NS * R, T, cfg.m))
        for i in range(NS):
            P[i * R:(i + 1) * R, :2, aims[i]] = amp * signs[i]
        ens = d.from_states(jax.tree_util.tree_map(lambda a: np.repeat(a, R, 0), x0), keys=keys)
        _, r = d.rollout(ens, P=P, T=T, rec=("L2",))
        res[name] = r["L2"].reshape(NS, R, T + 1, 2)
        print(name, np.round(res[name][:, :, -1].mean((0, 1)), 3).tolist(), flush=True)
    an = json.load(open(os.path.join(_paths.RESULTS, f"analysis_H{H}.json")))
    hs = [h for h in (1, 2, 4, 8, 16) if h <= T]
    hz = an["horizons_ticks"]
    out = {"starts": info, "R": R, "T": T, "costs_nats": {n: float(budget.program_cost([(0, np.eye(cfg.m)[0] * a), (1, np.eye(cfg.m)[0] * a)]))
                                                         for n, a in PROGS.items()}, "effects": {}}
    sd0 = res["none"].std(1, ddof=1).mean(0)                               # (T+1, 2) oracle sd, pooled over starts
    for name in PROGS:
        if name == "none":
            continue
        diff = res[name] - res["none"]                                    # paired by key
        m = diff.mean((0, 1))
        se = diff.mean(1).std(0, ddof=1) / np.sqrt(NS)
        e = {}
        for h in hs:
            row = {}
            for c, nm in enumerate(("N", "s_b")):
                ve = an["closure"]["sel"][nm]["Ve"]["2"][hz.index(h)] if h in hz else None
                row[nm] = {"mean_diff": float(m[h, c]), "se_over_starts": float(se[h, c]),
                           "in_oracle_sd": float(m[h, c] / sd0[h, c]) if sd0[h, c] > 0 else None,
                           "in_sqrt_Ve": float(m[h, c] / np.sqrt(ve)) if ve else None}
            e[str(h)] = row
        out["effects"][name] = e
    json.dump(out, open(os.path.join(_paths.RESULTS, "probe_input.json"), "w"), indent=1)
    print(json.dumps(out["effects"], indent=1))


if __name__ == "__main__":
    main()
