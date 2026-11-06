"""Checker: recompute the media key's headline numbers from its saved outputs with independent code
(not integrate/analyze.objects_stats). Reads results/stats_both_J24_T300.npz and hero_*_s0.npz.

usage: python -B recompute.py   -> check/recompute.json
"""
import json

import numpy as np

R = "/home/user/evalwork/vecworld/vw1/fresh/media/results"
K, NF, NC, T_ = 12, 12, 192, 300
z = np.load(f"{R}/stats_both_J24_T300.npz")
L1 = z["L1"].astype(float)
tab = z["tab"].astype(float)
glob = z["glob"].astype(float)
mass = z["mass"]
J, T1 = L1.shape[:2]
S = L1[:, :, NC:].reshape(J, T1, K, NF)
pres = S[..., 0] > 0.5
ev = tab[..., 3]
uid = tab[..., 4]


def mi(d, L=128):
    return (d + L / 2) % L - L / 2


def stats(idx):
    Sx, P, E, U, TB, GL = S[idx], pres[idx], ev[idx], uid[idx], tab[idx], glob[idx]
    n = P.sum(-1).ravel()
    rg = np.median(Sx[..., 7][P])
    bl = 2.4 * rg
    sp = np.hypot(Sx[..., 10], Sx[..., 11])
    spd = np.median(sp[P & (E == 0)])
    lives, paths = [], []
    for j in range(len(idx)):
        for u in np.unique(U[j][P[j]]):
            m = P[j] & (U[j] == u)                     # (T1, K)
            ts = np.flatnonzero(m.any(1))
            t0, t1 = ts[0], ts[-1]
            lives.append(t1 - t0 + 1)
            ok = m & (E[j] == 0)
            ok[t0] = False
            paths.append(sp[j][ok].sum() / bl)
    lives, paths = np.array(lives), np.array(paths)
    lg = lives >= 50
    evc = (GL[:, -1, 1:] - GL[:, 0, 1:]).sum(0)
    # encounters (same rule as the VW-0 estimator, written independently, vectorised over pairs)
    enc, fus = 0, 0
    for j in range(len(idx)):
        cy, cx, r = TB[j][..., 0], TB[j][..., 1], Sx[j][..., 7]
        dd = np.hypot(mi(cy[:, :, None] - cy[:, None, :]), mi(cx[:, :, None] - cx[:, None, :]))
        close = (dd < 1.6 * (r[:, :, None] + r[:, None, :]) + 2) & P[j][:, :, None] & P[j][:, None, :]
        same = (U[j][1:] == U[j][:-1])
        was = close[:-1] & same[:, :, None] & same[:, None, :]
        new = close[1:] & ~was
        fe = np.isin(E[j], (-1, 3))
        for t, a, b in zip(*np.nonzero(np.triu(new, 1))):
            t = t + 1
            enc += 1
            fus += bool(fe[t + 1:t + 6, a].any() or fe[t + 1:t + 6, b].any())
    # checker's event share (review/gap_events.py definition)
    a, b = P[:, :-1], P[:, 1:]
    live = a | b
    evt = live & ((E[:, 1:] != 0) | (a != b))
    tt = [60, 140, 220]
    return {"objects_median": float(np.median(n)), "objects_mean": float(n.mean()),
            "objects_p10": float(np.percentile(n, 10)), "objects_p90": float(np.percentile(n, 90)),
            "body_length_px": float(bl), "speed_median": float(spd), "ticks_to_cross": float(bl / spd),
            "n_tracks": int(len(lives)), "life_median": float(np.median(lives)), "frac_ge_50": float(lg.mean()),
            "path_median_ge_50": float(np.median(paths[lg])), "frac_path_ge_3_of_ge_50": float((paths[lg] >= 3).mean()),
            "path_median_all": float(np.median(paths)),
            "fusions_per_100": float(100 * evc[2] / (len(idx) * T_)), "fissions_per_100": float(100 * evc[3] / (len(idx) * T_)),
            "births": float(evc[0]), "deaths": float(evc[1]), "fusions": float(evc[2]), "fissions": float(evc[3]),
            "encounters_per_100": float(100 * enc / (len(idx) * T_)), "enc_fused_5": float(fus / max(enc, 1)),
            "mass_median": float(np.median(Sx[..., 1][P])),
            "event_share_all": float(evt.sum() / live.sum()),
            "event_share_60_140_220": float(evt[:, tt].sum() / live[:, tt].sum()),
            "event_share_60_140_220_counts": [int(evt[:, tt].sum()), int(live[:, tt].sum())]}


full = stats(np.arange(J))
rng = np.random.default_rng(123)
keys = ["body_length_px", "speed_median", "ticks_to_cross", "path_median_ge_50", "fusions_per_100", "event_share_all",
        "event_share_60_140_220", "objects_mean", "frac_ge_50", "enc_fused_5"]
B = [stats(rng.integers(0, J, J)) for _ in range(40)]
se = {k: float(np.std([b[k] for b in B], ddof=1)) for k in keys}
drift = np.abs(mass - mass[:, :1]).max(1) / mass[:, 0]
# censoring: tracks alive at the first or last recorded tick
cens = sum(len(set(uid[j, 0][pres[j, 0]]) | set(uid[j, -1][pres[j, -1]])) for j in range(J)) / full["n_tracks"]
out = {"stats_both_J24_T300": {"shape_L1": list(L1.shape), "seed": int(z["seed"]), "cpu_s": float(z["cpu_s"]),
                               "full": full, "bootstrap_se_40": se, "mass_max_rel_drift": float(drift.max()),
                               "frac_tracks_censored": float(cens)}}
# hero episodes: observation check, presence, events, maps
h = {v: np.load(f"{R}/hero_{v}_s0.npz") for v in ("objects", "coarse", "both")}
hero = {}
for v, hh in h.items():
    o, y, om = hh["obs64"], hh["L1"], hh["out_map"]
    hero[v] = {"obs_eq_quantised_permuted_L1": bool(np.array_equal(o, 1e-3 * np.round(y[:, om] / 1e-3))),
               "out_map_is_perm": bool(np.array_equal(np.sort(om), np.arange(len(om)))),
               "out_map_fixed_points": int((om == np.arange(len(om))).sum()),
               "in_map_fixed_points": int((hh["in_map"] == np.arange(len(hh["in_map"]))).sum())}
    if "tab" in hh.files:
        P = y[:, -K * NF:].reshape(len(y), K, NF)[:, :, 0] > 0.5
        g = hh["glob"]
        hero[v].update(objects_median=float(np.median(P.sum(1))), objects_min=int(P.sum(1).min()),
                       objects_max=int(P.sum(1).max()), slots_ever=int(P.any(0).sum()),
                       events=(g[-1, 1:] - g[0, 1:]).tolist())
hero["in_map_identical_objects_coarse_both"] = bool(np.array_equal(h["objects"]["in_map"], h["coarse"]["in_map"]) and
                                                    np.array_equal(h["objects"]["in_map"], h["both"]["in_map"]))
hero["level0_objects_vs_coarse_max_abs"] = float(np.abs(h["objects"]["x"] - h["coarse"]["x"]).max())
# the both-view designer level contains the objects-view level (same tracker on the same level 0)?
hero["both_L1_objects_part_eq_objects_L1"] = float(np.abs(h["both"]["L1"][:, NC:] - h["objects"]["L1"]).max())
out["hero"] = hero
json.dump(out, open("/home/user/evalwork/vecworld/vw1/fresh/media/check/recompute.json", "w"), indent=1)
print(json.dumps(out, indent=1))
