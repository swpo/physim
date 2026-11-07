"""probe_input -- does an aimed substrate input register at levels 1 and 2 within a few hundred nats?

    python probe_input.py [n_members] [amp_feed] [amp_starve] [ticks_on] [H] [tag]
        (defaults 12, 0.05, -0.03, 5, 30, ''; the second run used 16 0.03 -0.03 20 40 long)

States: members 0..n-1 of the pilot's designer ensemble (dt 0.5, sigma_a 0.01) at tick 150. For each member the
largest present cell (most likely to divide next) is the target; the program applies amp on every bump whose
centre lies within 8 px of the target's centroid, for ticks_on ticks (open loop, aimed once). Arms per member,
identical keys (paired twins): none (u = 0), feed (amp_feed), starve (amp_starve); plus R = 4 fresh-noise
replicates of `none` for the oracle spread. Recorded over H ticks: level 2 (N, mean size, rate) and the target
slot's mass, and divisions near it: new slots of mass >= 50 px (the level-2 division rule) whose centroid lies within
25 px of the target's centroid at the start.
Reports per arm: nats charged, divisions near the target within H ticks, target mass at the end of the input, the
paired level-2 differences against `none` at h = 5, 10, 20, 30 (and H), and the fresh-noise SD of level 2 at the
same h. Writes results/probe_input{tag}.json.
"""
import json
import os
import sys

import _paths
import jax
import numpy as np

import membrane_jax as MJ
import membrane_world as MW

NM = int(sys.argv[1]) if len(sys.argv) > 1 else 12
A_FEED = float(sys.argv[2]) if len(sys.argv) > 2 else 0.05
A_STARVE = float(sys.argv[3]) if len(sys.argv) > 3 else -0.03
T_ON = int(sys.argv[4]) if len(sys.argv) > 4 else 5
HZ = int(sys.argv[5]) if len(sys.argv) > 5 else 30
TAG = sys.argv[6] if len(sys.argv) > 6 else ""
T0, RREP = 150, 4
HS = tuple(sorted({h for h in (5, 10, 20, 30, HZ) if h <= HZ}))


def main():
    cfg = MJ.Config()
    specs, parts = MW.build(cfg)
    w = MW.MapWorld(specs["population"], world_seed=0)
    d = w.designer
    budget = MW.nats_budget(cfg)
    K = parts["tracker"].K
    ens = d.ensemble(NM, seed=0)
    ens, r0 = d.rollout(ens, T=T0, rec=("L1", "ev"))
    L1 = r0["L1"][:, -1, :K * 12].reshape(NM, K, 12)
    uid0 = r0["ev"][:, -1, :, 1]
    cen = MJ.bump_centres(cfg)
    H = cfg.H
    tgt, U = [], np.zeros((NM, T0 + HZ, cfg.m))
    for i in range(NM):
        pres = L1[i, :, 0] > 0.5
        k = int(np.argmax(np.where(pres, L1[i, :, 1], -1)))
        cx = (np.arctan2(L1[i, k, 4], L1[i, k, 3]) * H / (2 * np.pi)) % H
        cy = (np.arctan2(L1[i, k, 6], L1[i, k, 5]) * H / (2 * np.pi)) % H
        dd = np.hypot((cen[:, 0] - cy + H / 2) % H - H / 2, (cen[:, 1] - cx + H / 2) % H - H / 2)
        sel = np.flatnonzero(dd <= 8.0)
        tgt.append({"slot": k, "uid": int(uid0[i, k]), "mass_t0": float(L1[i, k, 1]), "bumps": sel.tolist(),
                    "cy": float(cy), "cx": float(cx)})
        U[i, T0:T0 + T_ON][:, sel] = 1.0
    out = {"n_members": NM, "t0_tick": T0, "ticks_on": T_ON, "H": HZ, "targets": tgt, "arms": {}}
    rec = ("L1", "L2", "ev")
    runs = {}
    for arm, amp in (("none", 0.0), ("feed", A_FEED), ("starve", A_STARVE)):
        e = ens.clone(rep=1)
        _, r = d.rollout(e, P=amp * U, T=HZ, rec=rec)
        runs[arm] = r
    rep = ens.clone(rep=RREP, fresh=True)
    _, rr = d.rollout(rep, T=HZ, rec=("L2",))
    L2rep = rr["L2"].reshape(NM, RREP, HZ + 1, 3)
    sd_oracle = {str(h): np.sqrt(L2rep[:, :, h].var(1, ddof=1).mean(0)).tolist() for h in HS}
    for arm, r in runs.items():
        Ltab = r["L1"][..., :K * 12].reshape(NM, HZ + 1, K, 12)
        res = {"nats_per_member": [float(sum(budget.cost(A * U[i, T0 + t]) for t in range(T_ON)))
                                   for i, A in [(i, {"none": 0.0, "feed": A_FEED, "starve": A_STARVE}[arm]) for i in range(NM)]]}
        divs, m_end, alive = [], [], []
        for i, tg in enumerate(tgt):
            k = tg["slot"]
            same = r["ev"][i, :, k, 1] == tg["uid"]
            pres = Ltab[i, :, k, 0] > 0.5
            ok = same & pres
            last = int(np.flatnonzero(~ok)[0]) if (~ok).any() else HZ + 1
            P = Ltab[i, :, :, 0] > 0.5
            newb = P[1:] & ~P[:-1] & (Ltab[i, 1:, :, 1] >= MW.M_DIV)
            ncx = (np.arctan2(Ltab[i, 1:, :, 4], Ltab[i, 1:, :, 3]) * H / (2 * np.pi)) % H
            ncy = (np.arctan2(Ltab[i, 1:, :, 6], Ltab[i, 1:, :, 5]) * H / (2 * np.pi)) % H
            dist = np.hypot((ncy - tg["cy"] + H / 2) % H - H / 2, (ncx - tg["cx"] + H / 2) % H - H / 2)
            divs.append(int((newb & (dist <= 25.0)).sum()))
            m_end.append(float(Ltab[i, T_ON, k, 1]) if ok[T_ON] else 0.0)
            alive.append(bool(ok[-1]))
        res.update({"target_divisions_within_H": divs, "target_divided_frac": float(np.mean(np.array(divs) > 0)),
                    "target_mass_at_end_of_input": m_end, "target_alive_at_H": alive})
        if arm != "none":
            dl = r["L2"] - runs["none"]["L2"]
            res["paired_L2_diff_mean"] = {str(h): dl[:, h].mean(0).tolist() for h in HS}
            res["paired_L2_diff_se"] = {str(h): (dl[:, h].std(0, ddof=1) / np.sqrt(NM)).tolist() for h in HS}
            res["paired_N_diff_over_oracle_sd"] = {str(h): float(dl[:, h, 0].mean() / sd_oracle[str(h)][0])
                                                   if sd_oracle[str(h)][0] > 0 else None for h in HS}
        out["arms"][arm] = res
    out["oracle_sd_L2"] = sd_oracle
    out["amps"] = {"feed": A_FEED, "starve": A_STARVE}
    json.dump(out, open(os.path.join(_paths.RESULTS, f"probe_input{TAG}.json"), "w"), indent=1)
    for arm, v in out["arms"].items():
        print(arm, {k: v[k] for k in ("target_divided_frac",)}, "nats", np.mean(v["nats_per_member"]),
              "mass_end", np.round(np.mean(v["target_mass_at_end_of_input"]), 1),
              v.get("paired_N_diff_over_oracle_sd"))
    print("oracle sd", sd_oracle)


if __name__ == "__main__":
    main()
