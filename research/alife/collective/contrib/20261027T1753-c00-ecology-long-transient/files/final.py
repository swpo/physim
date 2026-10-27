"""c00 long-transient test of c52: final figures and table across all runs.
Reads <pack>/long.json (analyze.py), polar.json (polar.py), recur.json (recur.py).
usage: final.py <outdir> <pack> [...]
writes regime.png (per run vs time: persistent splits per pair, recurrence Rmin, comet polar order P; colour = box),
counts.png (labkit prey/predator counts vs time, one panel per box), endstates.png (every run at t=12000 and t=48000),
table.json and a printed per-box summary."""
import sys, os, json
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

out = sys.argv[1]
packs = [p.rstrip("/") for p in sys.argv[2:]]
R = []
for p in packs:
    d = json.load(open(f"{p}/long.json")); d["polar"] = json.load(open(f"{p}/polar.json")); d["recur"] = json.load(open(f"{p}/recur.json"))
    R.append(d)
R.sort(key=lambda d: (d["size"][0], d["seed"]))
sizes = sorted({d["size"][0] for d in R})
col = {L: plt.cm.viridis(i / max(1, len(sizes) - 1)) for i, L in enumerate(sizes)}

# ---------------- regime.png
fig, ax = plt.subplots(1, 3, figsize=(14, 3.8))
for d in R:
    L = d["size"][0]; c = col[L]
    # persistent splits (prey + predator) per pair per 1000 t, per 6000-t window (eligible time)
    wp, wq = d["prey"]["windows"], d["predator"]["windows"]
    tm, y = [], []
    for a, b in zip(wp, wq):
        if a["t0"] < 6000 or not a["eligible_t"]:
            continue
        pairs = max(1.0, b["mean_count"])
        tm.append(a["t0"] + 0.5 * a["eligible_t"]); y.append(1000 * (a["persistent_splits"] + b["persistent_splits"]) / a["eligible_t"] / pairs)
    ax[0].plot(tm, y, "o-", color=c, ms=3, lw=0.8, alpha=0.85)
    w = d["recur"]["Rmin_median_by_window"]
    ax[1].plot([int(k) + 3000 for k in w], list(w.values()), "o-", color=c, ms=3, lw=0.8, alpha=0.85)
    pw = d["polar"]["P_mean_by_6000t"]
    ks = [k for k, v in pw.items() if v is not None]
    ax[2].plot([int(k.split("-")[0]) + 3000 for k in ks], [pw[k] for k in ks], "o-", color=c, ms=3, lw=0.8, alpha=0.85)
for L in sizes:
    ax[0].plot([], [], color=col[L], label=f"{L}^2 (n={sum(d['size'][0] == L for d in R)})")
ax[0].legend(fontsize=7)
ax[0].set_title("persistent splits (prey + predator) per predator body per 1000 t", fontsize=8)
ax[1].axhline(0.2, color="k", lw=0.6, ls="--")
ax[1].set_title("recurrence Rmin (window median): < 0.2 = regular (locked / periodic)", fontsize=8)
ax[2].set_title("comet polar order P (window mean); random ~ 0.89/sqrt(N)", fontsize=8)
for a in ax:
    a.set_xlabel("time"); a.axvline(12000, color="0.6", lw=0.6, ls=":"); a.set_ylim(bottom=0); a.set_xlim(0, 48500)
plt.tight_layout(); plt.savefig(f"{out}/regime.png", dpi=90); plt.close()

# ---------------- counts.png
fig, ax = plt.subplots(len(sizes), 1, figsize=(10, 1.9 * len(sizes)), squeeze=False, sharex=True)
for i, L in enumerate(sizes):
    a = ax[i, 0]; rs = [d for d in R if d["size"][0] == L]
    for j, d in enumerate(rs):
        t = np.arange(len(d["prey"]["n"])) * 100.0
        a.plot(t, d["prey"]["n"], color=plt.cm.Greens(0.45 + 0.5 * j / max(1, len(rs))), lw=0.7)
        a.plot(t, d["predator"]["n"], color=plt.cm.Reds(0.45 + 0.5 * j / max(1, len(rs))), lw=0.7)
        tr = d["recur"]["t_regular"]
        if tr is not None:
            a.axvline(tr, color="b", ls=":", lw=0.8)
    a.set_ylabel(f"{L}^2", fontsize=8); a.set_ylim(bottom=0)
    a.text(0.995, 0.05, f"seeds {[d['seed'] for d in rs]}", transform=a.transAxes, ha="right", fontsize=6)
ax[-1, 0].set_xlabel("time  (prey green, predators red, one shade per seed; blue dotted = start of regular dynamics)")
fig.suptitle("labkit per-species body counts, c52 world to t=48000", fontsize=8)
plt.tight_layout(); plt.savefig(f"{out}/counts.png", dpi=90); plt.close()

# ---------------- endstates.png
times = [12000, 48000]
nc = 4
nr = int(np.ceil(len(R) / nc))
fig, ax = plt.subplots(nr, nc * 2, figsize=(1.7 * nc * 2, 1.9 * nr), squeeze=False)
for i in range(nr * nc):
    for c2 in range(2):
        A = ax[i // nc, (i % nc) * 2 + c2]; A.set_xticks([]); A.set_yticks([])
        if i >= len(R):
            A.axis("off"); continue
        d = R[i]; z = np.load(f"{d['pack']}/frames.npz"); Rr = z["render"]; rf = z["render_f"] * 100.0
        k = int(np.argmin(np.abs(rf - times[c2]))); F = Rr[k].astype(np.float32)
        A.imshow(np.stack([F[1] / 1.5, F[0], 0.35 * F[2]], -1).clip(0, 1), interpolation="nearest")
        A.set_title(f"{d['size'][0]}^2 s{d['seed']} t={rf[k]:.0f}", fontsize=6)
fig.suptitle("every run at t=12000 (left of each pair) and t=48000 (right); prey green, predator red", fontsize=7)
plt.tight_layout(); plt.savefig(f"{out}/endstates.png", dpi=90); plt.close()

# ---------------- table
tab = []
for d in R:
    p, q = d["prey"], d["predator"]
    late = lambda x: sum(w["persistent_splits"] for w in x["windows"] if w["t0"] >= 36000)
    row = {"run": os.path.basename(d["pack"]), "size": d["size"][0], "seed": d["seed"],
           "prey_final": p["final"], "pred_final": q["final"], "prey_extinct_t": p["extinct_at_t"], "pred_extinct_t": q["extinct_at_t"],
           "prey_ps_by_window": [w["persistent_splits"] for w in p["windows"]],
           "pred_ps_by_window": [w["persistent_splits"] for w in q["windows"]],
           "prey_ps_after_36000": late(p), "pred_ps_after_36000": late(q),
           "prey_last_ps_t": p["last_persistent_split_t"], "pred_last_ps_t": q["last_persistent_split_t"],
           "prey_max_gen": p["max_generation"], "pred_max_gen": q["max_generation"],
           "prey_mean_12000_48000": p["mean_count_12000_48000"], "pred_mean_12000_48000": q["mean_count_12000_48000"],
           "prey_slope_per_10000t": p["count_slope_per_10000t_after_12000"], "pred_slope_per_10000t": q["count_slope_per_10000t_after_12000"],
           "t_regular": d["recur"]["t_regular"], "Rmin_by_window": list(d["recur"]["Rmin_median_by_window"].values()),
           "t_last_count_change": d["polar"]["t_last_count_change"], "count_changes_last_10000t": d["polar"]["count_changes_last_10000t"],
           "P_by_window": list(d["polar"]["P_mean_by_6000t"].values()), "P_random_typ": d["polar"]["P_random_typ"],
           "hosted_frac_median": d["polar"]["hosted_frac_median"], "wall_s": d["wall_s"]}
    lp = [x for x in (p["last_persistent_split_t"], q["last_persistent_split_t"]) if x is not None]
    row["t_last_division"] = max(lp) if lp else None          # last persistent split of either kind
    # the dividing regime has ended if neither kind has a persistent split in the last 12000 eligible t (34000-46000)
    row["division_ended"] = row["t_last_division"] is None or row["t_last_division"] < 34000
    # expected persistent splits (both kinds) in 12000 t at the churning rate of this run's own first 3 windows after
    # predator formation (6000-24000), for the chance level of a 12000-t gap
    early = sum(w["persistent_splits"] for x in (p, q) for w in x["windows"] if 6000 <= w["t0"] < 24000)
    row["expected_splits_per_12000t_early_rate"] = round(early * 12000 / 18000, 2)
    row["coexist_48000"] = p["final"] > 0 and q["final"] > 0
    row["both_divide_36000_48000"] = row["prey_ps_after_36000"] > 0 and row["pred_ps_after_36000"] > 0
    row["irregular_at_end"] = d["recur"]["t_regular"] is None
    tab.append(row)
json.dump(tab, open(f"{out}/table.json", "w"), indent=1)
for L in sizes:
    rs = [r for r in tab if r["size"] == L]
    print(f"{L}^2: n={len(rs)} coexist {sum(r['coexist_48000'] for r in rs)}/{len(rs)}; both divide in 36000-48000 "
          f"{sum(r['both_divide_36000_48000'] for r in rs)}/{len(rs)}; division ended {sum(r['division_ended'] for r in rs)}/{len(rs)} "
          f"(t_last_division {[r['t_last_division'] for r in rs]}); irregular at end {sum(r['irregular_at_end'] for r in rs)}/{len(rs)}; "
          f"t_regular {[r['t_regular'] for r in rs]}; extinctions {[(r['prey_extinct_t'], r['pred_extinct_t']) for r in rs]}")
    for r in rs:
        print(f"   s{r['seed']}: final {r['prey_final']}/{r['pred_final']} mean {r['prey_mean_12000_48000']}/{r['pred_mean_12000_48000']} "
              f"slope {r['prey_slope_per_10000t']}/{r['pred_slope_per_10000t']} ps prey {r['prey_ps_by_window']} pred {r['pred_ps_by_window']} "
              f"gen {r['prey_max_gen']}/{r['pred_max_gen']} Rmin {r['Rmin_by_window']} P {r['P_by_window']}")

# ---------------- lifetime.png: end of the dividing regime vs box size
fig, ax = plt.subplots(figsize=(5.2, 3.6))
for r in tab:
    L = r["size"]; jit = (r["seed"] % 10 - 4.5) * 0.6
    if not r["division_ended"]:
        ax.plot(L + jit, 48000, "^", color="tab:green", ms=7)
    elif r["t_last_division"] is None:
        ax.plot(L + jit, 2000, "x", color="tab:red", ms=7)
    else:
        ax.plot(L + jit, r["t_last_division"], "o", color="tab:red", ms=6)
    if r["t_regular"] is not None:
        ax.plot(L + jit, r["t_regular"], "s", mfc="none", color="tab:blue", ms=7)
ax.plot([], [], "^", color="tab:green", label="still dividing at t=48000 (censored)")
ax.plot([], [], "o", color="tab:red", label="last persistent split (division ended)")
ax.plot([], [], "x", color="tab:red", label="no persistent split ever (plotted at t=2000)")
ax.plot([], [], "s", mfc="none", color="tab:blue", label="start of regular (locked/periodic) dynamics")
ax.axhline(12000, color="0.6", ls=":", lw=0.8); ax.text(sizes[0] - 8, 12500, "claim's run end", fontsize=6, color="0.4")
ax.set_xticks(sizes); ax.set_xlabel("box side L (grid points; ~12 prey-predator pairs per 64^2)")
ax.set_ylabel("time"); ax.set_ylim(0, 52000); ax.legend(fontsize=6, loc="center right")
ax.set_title("c52 ecology: lifetime of the dividing regime vs box size", fontsize=8)
plt.tight_layout(); plt.savefig(f"{out}/lifetime.png", dpi=100); plt.close()
