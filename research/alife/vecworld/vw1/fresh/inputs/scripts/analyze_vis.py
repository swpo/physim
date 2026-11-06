"""Analysis of (a) blind input visibility and (d) late differences from results/vis/state_*.npz.

usage: python -B analyze_vis.py      -> results/visibility.json, results/vis_sd.npz, media/visibility.png

Estimators (integrate/analyze.inputs_rep_analysis and inputs_analysis, re-applied to the VW-1 records):
standardised units (per-coordinate SD over all no-input runs, all states and ticks; coordinates with
SD <= 1e-6 max dropped); oracle spread Vu(tau) = unbiased within-replicate variance over the R
fresh-noise no-input twins of the state, averaged over coordinates;
  mean-shift SNR(tau) = (|mean_r Delta_r|^2 - var_r(Delta_r)/R) / Vu    (Delta_r = with-input minus its
                         identical-noise twin; unbiased squared shift of the conditional mean)
  twin SNR(tau)       = mean_r |Delta_r|^2 / Vu    (one twin pair; ~2 once the pair is fully scrambled)
Reported per horizon: median over states (bootstrap SE over states), worst state, fraction >= 1."""
import glob
import json

import common as CM
import numpy as np

TAUS = [1, 2, 4, 8, 16, 32]
files = sorted(glob.glob(f"{CM.RES}/vis/state_*.npz"))
D = [np.load(f) for f in files]
names = [str(n) for n in D[0]["names"]]
CONDS = [str(c) for c in D[0]["conds"]]
R = sum(n.startswith("twin_") for n in names)
idx = {c: [names.index(f"{c}_{r}") for r in range(R)] for c in ["twin"] + CONDS}
Ys = [d["Y"].astype(float) for d in D]
S = len(Ys)
allt = np.concatenate([Y[idx["twin"]].reshape(-1, Y.shape[-1]) for Y in Ys])
sd = allt.std(0)
views = {"coarse": slice(0, CM.NC), "objects": slice(CM.NC, CM.NC + CM.K * CM.NF)}
eff = {}
for v, sl in views.items():
    s_ = sd[sl]
    eff[v] = s_ > 1e-6 * s_.max()
np.savez(f"{CM.RES}/vis_sd.npz", sd=sd, eff_coarse=eff["coarse"], eff_objects=eff["objects"])
rng = np.random.default_rng(0)


def boot_median_se(a, n=2000):
    a = np.asarray(a)
    b = rng.integers(0, len(a), (n, len(a)))
    return float(np.median(a[b], 1).std())


out = {"n_states": S, "R_noise_keys": R, "horizons": TAUS, "conditions": CONDS,
       "admissible_default": {c: bool(D[0]["adm"][i]) for i, c in enumerate(CONDS)},
       "null_check_max_abs_level0": float(max(float(d["null_x"]) for d in D)),
       "null_check_max_abs_level1": float(max(float(d["null_y"]) for d in D)),
       "n_eff_coords": {v: int(e.sum()) for v, e in eff.items()}}
curves = {}
for v, sl in views.items():
    e = eff[v]
    sdv = sd[sl][e]
    res = {}
    per = {c: {"snr_mean": [], "snr_twin": []} for c in CONDS}
    Vu_all = []
    for Y in Ys:
        Tw = Y[idx["twin"]][..., sl][..., e] / sdv                     # (R, 33, q)
        Vu = Tw.var(0, ddof=1).mean(1)                                  # (33,)
        Vu_all.append(Vu)
        for c in CONDS:
            Dl = Y[idx[c]][..., sl][..., e] / sdv - Tw
            m = Dl.mean(0)
            varm = Dl.var(0, ddof=1) / R
            with np.errstate(divide="ignore", invalid="ignore"):
                per[c]["snr_mean"].append(((m ** 2) - varm).mean(1) / Vu)
                per[c]["snr_twin"].append((Dl ** 2).mean(2).mean(0) / Vu)
    for c in CONDS:
        sm, st = np.array(per[c]["snr_mean"]), np.array(per[c]["snr_twin"])
        curves[(v, c)] = (sm, st)
        res[c] = {
            "mean_shift_snr_median": {t: float(np.median(sm[:, t])) for t in TAUS},
            "mean_shift_snr_median_se": {t: boot_median_se(sm[:, t]) for t in TAUS},
            "mean_shift_snr_worst_state": {t: float(sm[:, t].max()) for t in TAUS},
            "worst_state_index": {t: int(np.argmax(sm[:, t])) for t in TAUS},
            "n_states_mean_shift_snr_ge_1": {t: int((sm[:, t] >= 1).sum()) for t in TAUS},
            "twin_snr_median": {t: float(np.median(st[:, t])) for t in TAUS},
            "n_states_twin_snr_ge_1": {t: int((st[:, t] >= 1).sum()) for t in TAUS},
        }
        # (d) first tick at which the twin difference reaches the natural (oracle) spread
        cross = np.array([next((t for t in range(1, 33) if st[i, t] >= 1), 99) for i in range(S)])
        res[c]["first_tick_twin_snr_ge_1"] = {"median": float(np.median(cross)),
                                              "p25": float(np.percentile(cross, 25)),
                                              "p75": float(np.percentile(cross, 75)),
                                              "n_never_by_32": int((cross == 99).sum()),
                                              "n_crossed_by": {t: int((cross <= t).sum()) for t in TAUS},
                                              "median_label": (str(int(np.median(cross))) if np.median(cross) <= 32 else ">32"),
                                              "note": "99 = not reached by tick 32", "per_state": cross.tolist()}
    res["oracle_spread_Vu_median"] = {t: float(np.median(np.array(Vu_all)[:, t])) for t in TAUS}
    out[v] = res
# matter moved per program (summed over its input ticks), and random-site occupancy
mv = {}
for c in CONDS:
    a = np.array([d["moved"][idx[c]].sum(1) for d in D])               # (S, R)
    mv[c] = {"median": float(np.median(a)), "mean": float(a.mean()), "min": float(a.min()), "max": float(a.max()),
             "per_input_tick_median": float(np.median(np.concatenate([d["moved"][idx[c]][d["moved"][idx[c]] > 0]
                                                                      if (d["moved"][idx[c]] > 0).any() else [0.0]
                                                                      for d in D])))}
out["moved_matter_per_program"] = mv
rm = np.concatenate([d["rand_moved"] for d in D])
out["random_admissible_commands"] = {
    "n_samples": int(rm.size), "source": "Admissible.sample at each test state; numpy transcription of the JAX kick",
    "moved_mean": float(rm.mean()), "moved_median": float(np.median(rm)), "moved_p90": float(np.percentile(rm, 90)),
    "moved_se_mean": float(rm.std(ddof=1) / np.sqrt(rm.size)),
    "frac_sites_empty(A_sum<1e-3)": float(np.concatenate([d["rand_empty_frac"] for d in D]).mean()),
    "frac_source_sites_empty(A_sum<1e-3)": float(np.concatenate([d["rand_src_empty_frac"] for d in D]).mean()),
    "frac_sites_in_tracked_bodies": float(np.concatenate([d["rand_body_frac"] for d in D]).mean()),
    "frac_commands_moving_over_0.01": float((rm > 0.01).mean()),
}
st0 = np.load(f"{CM.RES}/states.npz")
Sx = st0["x"][:S].sum(1).reshape(S, -1)
out["matter_footprint"] = {"frac_cells_A_sum_gt_1e-3": float((Sx > 1e-3).mean()),
                           "frac_cells_A_sum_gt_1e-2": float((Sx > 1e-2).mean())}
emp_sites = np.concatenate([d["site_empty_x1"][:, 2] for d in D])
out["empty_x1_site_A_sum"] = {"median": float(np.median(emp_sites)), "max": float(emp_sites.max())}
json.dump(out, open(f"{CM.RES}/visibility.json", "w"), indent=1, default=float)

# ---------------------------------------------------------------- figure
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

plt.rcParams.update({"font.size": 9, "axes.edgecolor": "0.5", "axes.labelcolor": "0.9", "xtick.color": "0.8",
                     "ytick.color": "0.8", "text.color": "0.9"})
lab = {"rand_x1": "random, 1 tick", "rand_x8": "random, 8 ticks", "body_x1": "on bodies, 1 tick",
       "body_x8same": "on bodies, same input 8 ticks", "k32_x1": "on bodies, k=32, |a|=1 (probe)",
       "empty_x1": "empty cells, 1 tick"}
col = {"rand_x1": "#7fb3ff", "rand_x8": "#2f6fdf", "body_x1": "#ffb347", "body_x8same": "#ff7f0e",
       "k32_x1": "#e04040", "empty_x1": "#9be39b"}
fig, axs = plt.subplots(1, 3, figsize=(9.6, 3.6), dpi=100)
fig.patch.set_facecolor("black")
FLOOR = 1e-3
tt = np.arange(1, 33)
for ax, v in zip(axs[:2], ("objects", "coarse")):
    ax.set_facecolor("black")
    for c in ("rand_x1", "rand_x8", "body_x1", "body_x8same", "k32_x1"):
        sm = curves[(v, c)][0]
        med = np.array([np.median(sm[:, t]) for t in TAUS])
        wst = np.array([sm[:, t].max() for t in TAUS])
        ax.plot(TAUS, np.maximum(med, FLOOR), color=col[c], lw=1.6, marker="o", ms=4, label=lab[c])
        ax.plot(TAUS, np.maximum(wst, FLOOR), color=col[c], lw=0.0, marker="^", ms=4, mfc="none", mew=0.9)
    ax.axhline(1.0, color="0.6", lw=0.8, ls="--")
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_ylim(FLOOR * 0.8, 600)
    ax.set_xticks(TAUS)
    ax.set_xticklabels(TAUS)
    ax.set_xlabel("horizon (ticks)")
    ax.set_title(f"{v} view: shift of the mean", color="white", fontsize=9.5)
axs[0].set_ylabel("squared mean shift / oracle variance\n(dots: median of %d states, triangles: worst)" % S, fontsize=8)
fig.text(0.01, 0.012, "Shift of the mean: unbiased squared shift of the level-1 conditional mean (6 noise keys, each against "
         "its identical-noise twin) over the oracle variance; values <= 1e-3, including estimates below 0, sit on the floor.",
         color="0.65", fontsize=6.5)
axs[1].legend(fontsize=6.8, loc="upper right", frameon=False)
ax = axs[2]
ax.set_facecolor("black")
for c, v, ls in (("empty_x1", "objects", "-"), ("empty_x1", "coarse", "--"), ("body_x1", "objects", "-"), ("body_x1", "coarse", "--")):
    st = curves[(v, c)][1]
    med = np.median(st[:, 1:], 0)
    if c == "empty_x1":
        lo, hi = np.percentile(st[:, 1:], 25, 0), np.percentile(st[:, 1:], 75, 0)
        ax.fill_between(tt, np.clip(lo, 1e-13, None), np.clip(hi, 1e-13, None), color=col[c], alpha=0.18 if ls == "-" else 0.10, lw=0)
    ax.plot(tt, np.clip(med, 1e-13, None), color=col[c], lw=1.5, ls=ls, label=f"{lab[c]} ({v})")
ax.axhline(1.0, color="0.6", lw=0.8, ls="--")
ax.set_xscale("log", base=2)
ax.set_yscale("log")
ax.set_ylim(1e-13, 20)
ax.set_xticks(TAUS)
ax.set_xticklabels(TAUS)
ax.set_xlabel("ticks after the input")
ax.set_ylabel("one twin pair: |difference|^2 / oracle variance", fontsize=8)
ax.set_title("late differences (median, IQR band)", color="white", fontsize=9.5)
ax.legend(fontsize=6.8, loc="lower right", frameon=False)
for a in axs:
    for sp in a.spines.values():
        sp.set_color("0.4")
plt.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig(f"{CM.MEDIA}/visibility.png", dpi=100, facecolor="black")
print(json.dumps({v: {c: out[v][c]["mean_shift_snr_median"] for c in CONDS} for v in views}, indent=0))
print(json.dumps(out["random_admissible_commands"], indent=0), json.dumps(mv, indent=0))
