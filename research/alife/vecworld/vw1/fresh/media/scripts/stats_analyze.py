"""Legibility statistics of level 1 from the fresh VW-1 'both' trajectories (stats_run.py output), with the VW-0
estimator integrate/analyze.objects_stats (read only, unchanged) plus bootstrap SEs over trajectories.

usage: python -B stats_analyze.py NPZ NBOOT   -> results/legibility.json

Definitions (as VW-0 objects_stats): body length = 2.4 x median radius of gyration over present slot-ticks;
speed = |v| on continuing slot-ticks (present, no tracker event that tick), px per tick; track = one tracker
uid; path = summed per-tick displacement on event-free ticks, in body lengths, median over tracks living
>= 50 ticks; events per 100 ticks = tracker counters summed over all objects of a trajectory.
Added (checker, reports/check.md / review/gap_events.py): share of present slot-ticks whose slot has a tracker
event at t+1; median path over ALL tracks; ticks to cross one body length = body length / median speed.
"""
import json
import sys

sys.path.insert(0, "/home/user/evalwork/vecworld/vw1/port")
import _paths  # noqa: F401,E402
import numpy as np  # noqa: E402

import analyze as AN  # noqa: E402   (VW-0 estimators, read only)
assert AN.__file__.startswith(_paths.INT_DIR), AN.__file__

f, NBOOT = sys.argv[1], int(sys.argv[2])
z = np.load(f)
L1, tab, glob, mass = z["L1"].astype(float), z["tab"].astype(float), z["glob"].astype(float), z["mass"]
J, T1 = L1.shape[:2]
K, NF, NC = 12, 12, 192
D = {"Yo": [L1[j, :, NC:] for j in range(J)], "Yc": [L1[j, :, :NC] for j in range(J)],
     "tab": [tab[j] for j in range(J)], "glob": [glob[j] for j in range(J)], "mass": [mass[j] for j in range(J)]}


def extras(D, ticks=None):
    """Checker's definition (review/gap_events.py): slot-ticks (t, s) with s present at t or t+1; an
    'event' slot has a tracker event code at t+1 or changes presence. ticks: restrict t (None: all)."""
    ev_next, n = 0, 0
    for Yo, tb in zip(D["Yo"], D["tab"]):
        pres = Yo.reshape(len(Yo), K, NF)[:, :, 0] > 0.5
        a, b = pres[:-1], pres[1:]
        live = a | b
        evt = live & ((tb[1:, :, 3] != 0) | (a != b))
        if ticks is not None:
            live, evt = live[list(ticks)], evt[list(ticks)]
        ev_next += evt.sum()
        n += live.sum()
    return float(ev_next / n)


def headline(D):
    s = AN.objects_stats(D, K, 20)
    return s, {"objects_median": s["objects_per_tick"]["median"],
               "objects_mean": float(np.mean(np.concatenate([(Y.reshape(len(Y), K, NF)[:, :, 0] > 0.5).sum(1) for Y in D["Yo"]]))),
               "speed_px_per_tick_median": s["speed_px_per_tick"]["median"],
               "body_length_px": s["body_length_px(2.4 rg)"],
               "ticks_to_cross_body_length": s["body_length_px(2.4 rg)"] / s["speed_px_per_tick"]["median"],
               "path_body_lengths_median_tracks_ge_50": s["path_body_lengths_tracks_ge_50"]["median"],
               "frac_tracks_ge_50_with_path_ge_3": s["path_body_lengths_tracks_ge_50"]["frac_ge_3"],
               "fusions_per_100_ticks": s["events_per_100_ticks"]["fusions"],
               "fissions_per_100_ticks": s["events_per_100_ticks"]["fissions"],
               "track_life_median_ticks": s["track_life_ticks"]["median"],
               "frac_tracks_ge_50": s["track_life_ticks"]["frac_ge_50"],
               "encounters_per_100_ticks": s["encounters_per_100_ticks"],
               "encounters_fused_within_5_ticks": s["encounters_fused_within_5_ticks"],
               "mass_median": s["mass_median"],
               "frac_slot_ticks_event_at_t+1": extras(D),
               "frac_slot_ticks_event_at_t+1_at_ticks_60_140_220": extras(D, (60, 140, 220))}


stats, H = headline(D)
# median path over all tracks (not only >= 50 ticks), same path definition as objects_stats
rg_med = stats["rg_median_px"]
paths, lives = [], []
for Yo, tb in zip(D["Yo"], D["tab"]):
    S = Yo.reshape(len(Yo), K, NF)
    pres, ev, uid = S[:, :, 0] > 0.5, tb[:, :, 3], tb[:, :, 4]
    tr = {}
    for t in range(len(Yo)):
        for s in np.flatnonzero(pres[t]):
            k = int(uid[t, s])
            d = tr.setdefault(k, [t, t, 0.0])
            d[1] = t
            if ev[t, s] == 0 and t > d[0]:
                d[2] += float(np.hypot(S[t, s, 10], S[t, s, 11]))
    for a, b, p in tr.values():
        lives.append(b - a + 1)
        paths.append(p / (2.4 * rg_med))
H["path_body_lengths_median_all_tracks"] = float(np.median(paths))
H["frac_tracks_censored_by_window"] = None     # filled below
# tracks cut by the 300-tick window (alive at t = 0 or t = T): life is a lower bound for those
cens = 0
for Yo, tb in zip(D["Yo"], D["tab"]):
    S = Yo.reshape(len(Yo), K, NF)
    pres, uid = S[:, :, 0] > 0.5, tb[:, :, 4]
    allu = {int(u) for t in range(len(Yo)) for u in uid[t][pres[t]]}
    edge = {int(u) for u in uid[0][pres[0]]} | {int(u) for u in uid[-1][pres[-1]]}
    cens += len(allu & edge)
H["frac_tracks_censored_by_window"] = cens / stats["n_tracks"]

rng = np.random.default_rng(0)
boot = {k: [] for k in H if isinstance(H[k], float)}
for b in range(NBOOT):
    idx = rng.integers(0, J, J)
    Db = {k: [D[k][i] for i in idx] for k in ("Yo", "tab", "glob")}
    _, hb = headline(Db)
    for k in boot:
        if k in hb and hb[k] is not None:
            boot[k].append(hb[k])
SE = {k: float(np.std(v, ddof=1)) for k, v in boot.items() if len(v) > 1}
# per-trajectory event counts and mass drift
ev = np.array([g[-1, 1:] - g[0, 1:] for g in D["glob"]])            # (J, 4): births, deaths, fusions, fissions
drift = np.abs(mass - mass[:, :1]).max(1) / mass[:, 0]               # (J, 2) relative, per channel
out = {"source": f, "sizes": {"trajectories": J, "ticks_per_trajectory": T1 - 1, "slots": K, "stride_steps": 20,
                              "burn_in_ticks": int(z["burn_ticks"]), "designer_ensemble_seed": int(z["seed"]),
                              "world": "MapWorld(specs['both'], world_seed=0), no input",
                              "sim_wall_s": float(z["wall_s"]), "sim_cpu_s": float(z["cpu_s"])},
       "headline": H, "bootstrap_se_over_trajectories": SE, "n_boot": NBOOT,
       "events_total": dict(zip(["births", "deaths", "fusions", "fissions"], ev.sum(0).tolist())),
       "events_per_trajectory_per_300_ticks_mean_se": {k: [float(ev[:, i].mean()), float(ev[:, i].std(ddof=1) / np.sqrt(J))]
                                                      for i, k in enumerate(["births", "deaths", "fusions", "fissions"])},
       "trajectories_with_fusion_and_fission": int(((ev[:, 2] > 0) & (ev[:, 3] > 0)).sum()),
       "fusion_to_fission_ratio": float(ev[:, 2].sum() / max(ev[:, 3].sum(), 1)),
       "mass": {"max_rel_drift_per_channel_over_run": float(drift.max()), "median_rel_drift": float(np.median(drift)),
                "initial_mass_per_channel_mean": mass[:, 0].mean(0).tolist()},
       "objects_stats_vw0_estimator": stats, "coarse_stats_vw0_estimator": AN.coarse_stats(D)}
json.dump(out, open("/home/user/evalwork/vecworld/vw1/fresh/media/results/legibility.json", "w"), indent=1)
print(json.dumps({"headline": H, "se": SE, "mass": out["mass"], "events_total": out["events_total"]}, indent=1))
