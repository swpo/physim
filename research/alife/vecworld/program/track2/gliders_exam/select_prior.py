"""select_prior -- read results/scan.json, score each candidate, pick 4 hidden parameters, write prior.json.

Per candidate and edge:
  viable    finite; at least 2 tracked bodies at every recorded tick; mean count in [4, 12]; median speed of
            continuing bodies (mean over the 3 members) >= 0.5 px/tick; max A_sum < 10 (31-tick window
            after burn-in; the chosen box is re-checked at its corners over 100 ticks by viab_joint.py)
  headroom  the theta-plug-in deficit at level 1, mean over h = 2, 4, 8 (OES units, scan.py), and at
            level 2 h = 8
  stat_z    shift of the level-1/2 summary statistics against the null setting, in units of the SD of a
            3-trajectory mean of the same statistic over the same window in the default world (closure runs)
Selection rule (declared before looking at the pilot): candidates grouped into families
{lR}, {dm, dm_g}, {ls, ls_g}, {lh}, {lA, n}, {gw}; within a family the member with the largest headroom
(min over the two edges) among those viable at both edges; then the 4 families with the largest such
headroom. Prior = the scanned box (uniform). A candidate with a non-viable edge is not eligible (its box would
need a narrower rescan).
"""
import json
import os
import sys

import numpy as np

import gworld as GW

sys.path.insert(0, GW.ACT)
from viability import traj_stats  # noqa: E402

STATS = ["objects_mean", "speed_median", "mass_median", "rg_median", "fusions_per100", "fissions_per100"]
FAMILY = {"lR": "radius", "dm": "growth_mu", "ls": "growth_sigma", "lh": "growth_height", "lA": "alpha",
          "n": "alpha", "gw": "wind_gain"}


def family(k):
    return FAMILY.get(k, FAMILY.get(k.split("_")[0]))


def native_sd(T=30, J=3):
    """SD of 3-trajectory means of each statistic over ticks 0..T after burn-in (closure runs)."""
    vals = []
    for tg in "AB":
        c = np.load(f"/home/user/evalwork/vecworld/vw1/fresh/closure/results/sim_{tg}.npz")
        Y, TAB = c["Y"].astype(float), c["TAB"].astype(float)
        for j in range(len(Y)):
            tb = TAB[j, :T + 1, :GW.K * 5].reshape(T + 1, GW.K, 5)
            vals.append(traj_stats(Y[j, :T + 1, GW.NC:], tb, TAB[j, :T + 1, GW.K * 5:]))
    return {k: float(np.std([v[k] for v in vals], ddof=1) / np.sqrt(J)) for k in STATS}


def main():
    sc = json.load(open(os.path.join(GW.RES, "scan.json")))
    S = sc["settings"]
    nsd = native_sd()
    null = S["null"]

    def mstat(r, k):
        v = [s.get(k, np.nan) for s in r["stats"]]
        return float(np.nanmean(v))
    rows = {}
    for name, r in S.items():
        d = r["deficit"]
        sp = mstat(r, "speed_median")
        viable = bool(r["finite"] and r["count_min"] >= 2 and 4 <= r["count_mean"] <= 12 and sp >= 0.5
                      and r["A_sum_max_end"] < 10)
        z = {k: (mstat(r, k) - mstat(null, k)) / nsd[k] if nsd[k] > 0 else None for k in STATS}
        rows[name] = {"viable": viable, "count_min": r["count_min"], "count_max": r["count_max"],
                      "count_mean": r["count_mean"], "speed_median": sp,
                      "L1_h1": d["L1h1"]["mean"], "L1_h2": d["L1h2"]["mean"], "L1_h4": d["L1h4"]["mean"],
                      "L1_h8": d["L1h8"]["mean"], "L1_h8_se": d["L1h8"]["se"], "L2_h8": d["L2h8"]["mean"],
                      "L2_h8_se": d["L2h8"]["se"],
                      "headroom_L1": float(np.mean([d[f"L1h{h}"]["mean"] for h in (2, 4, 8)])),
                      "headroom_L1_class_a": float(np.mean([d[f"L1h{h}"]["class_a"] for h in (2, 4, 8)])),
                      "headroom_L1_class_d": float(np.mean([d[f"L1h{h}"]["class_d"] for h in (2, 4, 8)])),
                      "stat_z": z, "stat_dist": float(np.sqrt(np.nansum([v ** 2 for v in z.values() if v is not None])))}
    cands = {}
    for name in S:
        if name == "null":
            continue
        par = name.rsplit("@", 1)[0]
        cands.setdefault(par, {})[name.rsplit("@", 1)[1]] = rows[name]
    table = {}
    for par, e in cands.items():
        if len(e) < 2:
            continue
        table[par] = {"family": family(par), "box": sc["prior_boxes"][par],
                      "viable_both": e["lo"]["viable"] and e["hi"]["viable"],
                      "headroom_min_edge": min(e["lo"]["headroom_L1"], e["hi"]["headroom_L1"]),
                      "headroom_mean_edges": (e["lo"]["headroom_L1"] + e["hi"]["headroom_L1"]) / 2,
                      "L2_h8_mean_edges": (e["lo"]["L2_h8"] + e["hi"]["L2_h8"]) / 2,
                      "stat_dist_mean_edges": (e["lo"]["stat_dist"] + e["hi"]["stat_dist"]) / 2}
    best = {}
    for par, t in table.items():
        if not t["viable_both"]:
            continue
        f = t["family"]
        if f not in best or t["headroom_min_edge"] > table[best[f]]["headroom_min_edge"]:
            best[f] = par
    chosen = sorted(best.values(), key=lambda p: -table[p]["headroom_min_edge"])[:4]
    prior = {"names": chosen, "lo": [table[p]["box"][0] for p in chosen], "hi": [table[p]["box"][1] for p in chosen],
             "rule": __doc__.split("Selection rule")[1].strip(), "source": "results/scan.json"}
    out = {"null_noise_floor": {k: rows["null"][k] for k in ("L1_h1", "L1_h2", "L1_h4", "L1_h8", "L1_h8_se", "L2_h8")},
           "native_sd_3traj_31ticks": nsd, "rows": rows, "table": table, "best_per_family": best, "prior": prior}
    json.dump(out, open(os.path.join(GW.RES, "select.json"), "w"), indent=1)
    json.dump(prior, open(os.path.join(GW.RES, "prior.json"), "w"), indent=1)
    for p, t in sorted(table.items(), key=lambda kv: -kv[1]["headroom_min_edge"]):
        print(f"{p:6s} {t['family']:14s} viable {t['viable_both']!s:5s} headroom min {t['headroom_min_edge']:+.3f} "
              f"mean {t['headroom_mean_edges']:+.3f} L2h8 {t['L2_h8_mean_edges']:+.3f} statdist {t['stat_dist_mean_edges']:.1f}")
    print("chosen", prior)


if __name__ == "__main__":
    main()
