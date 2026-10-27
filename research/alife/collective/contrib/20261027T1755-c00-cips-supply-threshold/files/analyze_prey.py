"""World 2 (c52 prey only): kF ramps (0.1 -> 0) and constant fractions from a formed state at t=3000."""
import glob, json, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from loadlog import load, tracks, series

O = "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/paperexp/supply-ramp"
KF0 = 0.1
RAMPS = {"R100": 100, "R1000": 1000, "R4000": 4000}
CONSTS = ["1", "0.75", "0.625", "0.5", "0.25", "0.1"]


def arm(sd, name):
    p = f"{O}/prey/s{sd}/{name}/log.jsonl"
    if not os.path.exists(p):
        return None
    meta, recs, evs = load(p)
    return {"recs": recs, "evs": evs, "tr": tracks(recs)}


def summarize(sd):
    out = {"seed": sd, "ramps": {}, "const": {}}
    for name in RAMPS:
        a = arm(sd, name)
        if a is None:
            continue
        recs, evs = a["recs"], a["evs"]
        A0 = recs[0]["body_area"]
        d = [e for e in evs if e["ev"] == "death"]
        ext = next((r for r in recs if r["n"] == 0), None)
        half = next((r for r in recs if r["body_area"] < 0.5 * A0), None)
        n10 = next((r for r in recs if r["n"] <= 0.1 * recs[0]["n"]), None)
        out["ramps"][name] = {"n_start": recs[0]["n"], "area_start": A0, "n_end": recs[-1]["n"],
                              "deaths": len(d), "splits_children": sum(e["ev"] == "split_child" for e in evs),
                              "births": sum(e["ev"] == "birth" for e in evs), "merge_children": sum(e["ev"] == "merge_child" for e in evs),
                              "death_kF_q": [float(np.percentile([e["kF"] for e in d], q)) for q in (0, 10, 50, 90, 100)] if d else None,
                              "death_t_q": [float(np.percentile([e["t_rel"] for e in d], q)) for q in (0, 50, 100)] if d else None,
                              "n10pct_kF": n10["kF"] if n10 else None, "n10pct_t": n10["t_rel"] if n10 else None,
                              "extinct_t": ext["t_rel"] if ext else None, "extinct_kF": ext["kF"] if ext else None,
                              "half_area_kF": half["kF"] if half else None, "half_area_t": half["t_rel"] if half else None,
                              "e_max_end": recs[-1]["e_max"]}
    for f in CONSTS:
        a = arm(sd, f"C{f}")
        if a is None:
            continue
        recs, evs = a["recs"], a["evs"]
        late = [r for r in recs if r["t_rel"] >= recs[-1]["t_rel"] - 500]
        areas_late = np.concatenate([r["areas"] for r in late]) if any(r["n"] for r in late) else np.array([])
        ext = next((r for r in recs if r["n"] == 0), None)
        out["const"][f] = {"kF": recs[0]["kF"], "n_start": recs[0]["n"], "n_end": recs[-1]["n"], "area_start": recs[0]["body_area"],
                           "area_end": recs[-1]["body_area"], "n_late_mean": float(np.mean([r["n"] for r in late])),
                           "area_late_mean": float(np.mean([r["body_area"] for r in late])),
                           "cell_area_late_median": float(np.median(areas_late)) if areas_late.size else 0.0,
                           "cell_area_late_q": [float(np.percentile(areas_late, 25)), float(np.percentile(areas_late, 75))] if areas_late.size else None,
                           "deaths": sum(e["ev"] == "death" for e in evs), "split_children": sum(e["ev"] == "split_child" for e in evs),
                           "births": sum(e["ev"] == "birth" for e in evs), "extinct_t": ext["t_rel"] if ext else None,
                           "F_bath_late": float(np.mean([r["F_bath"] for r in late])), "e_max_end": recs[-1]["e_max"]}
    return out


def fig(sd, S):
    cols = {"R100": "#d62728", "R1000": "#ff7f0e", "R4000": "#1f77b4"}
    fig, ax = plt.subplots(1, 3, figsize=(14, 4.2))
    for name, c in cols.items():
        a = arm(sd, name)
        if a is None:
            continue
        t, n = series(a["recs"], "n"); _, kf = series(a["recs"], "kF"); _, A = series(a["recs"], "body_area")
        ax[0].plot(t, n, color=c, label=f"{name}: kF 0.1 -> 0 over {RAMPS[name]} t")
        ax[1].plot(kf, n, color=c); ax[2].plot(kf, A, color=c)
    for f, d in S["const"].items():
        lab = "constant kF, mean of last 500 t" if f == "1" else None
        ax[1].plot(d["kF"], d["n_late_mean"], "ks", mfc="none", ms=7, label=lab)
        ax[2].plot(d["kF"], d["area_late_mean"], "ks", mfc="none", ms=7, label=lab)
    ax[0].set_xscale("symlog", linthresh=100); ax[0].set_xlabel("time since branch (t)"); ax[0].set_ylabel("prey bodies (c_a > 0.5)"); ax[0].legend(fontsize=8)
    for k in (1, 2):
        ax[k].invert_xaxis(); ax[k].set_xlabel("current kF")
    ax[1].set_ylabel("prey bodies"); ax[2].set_ylabel("total prey body area (px)"); ax[1].legend(fontsize=8)
    fig.suptitle(f"world 2, seed {sd}: c52 prey only (pred_on 0, 128^2), branched at t=3000; kF lowered linearly from 0.1 or held at a fraction for 2000 t", fontsize=9)
    fig.tight_layout(); fig.savefig(f"{O}/fig_prey_s{sd}.png", dpi=80); plt.close(fig)


def snap_at(sd, name, tr):
    fs = sorted(glob.glob(f"{O}/prey/s{sd}/{name}/snaps/e_*.npy"))
    if not fs:
        return None, None
    ts = np.array([float(os.path.basename(f)[2:-4]) for f in fs])
    i = int(np.argmin(abs(ts - tr)))
    return np.load(fs[i]).astype(float), ts[i]


def fig_snaps(sd):
    rows = [("R4000", 4000, [0, 1000, 2000, 3000, 3400, 3600, 3800, 4000, 4200, 4600]),
            ("R1000", 1000, [0, 250, 500, 750, 850, 900, 950, 1000, 1100, 1300]),
            ("R100", 100, [0, 50, 100, 150, 200, 250, 300, 400, 500, 600])]
    fig, ax = plt.subplots(4, 10, figsize=(15.5, 6.8))
    for a in ax.ravel():
        a.axis("off")
    for i, (name, T, tl) in enumerate(rows):
        for j, tr in enumerate(tl):
            im, tt = snap_at(sd, name, tr)
            if im is None:
                continue
            ax[i, j].imshow(im, cmap="viridis", vmin=0, vmax=1)
            ax[i, j].set_title(f"{name} t+{tt:.0f}\nkF={KF0 * max(0, 1 - tt / T):.4f}", fontsize=6)
    for j, f in enumerate(CONSTS):
        im, tt = snap_at(sd, f"C{f}", 2000)
        if im is None:
            continue
        ax[3, j].imshow(im, cmap="viridis", vmin=0, vmax=1)
        ax[3, j].set_title(f"step to kF={KF0 * float(f):.3f}\nt+{tt:.0f}", fontsize=6)
    fig.suptitle(f"world 2 seed {sd}: prey material c_a (0-1). Rows 1-3: ramps of kF from 0.1 to 0; row 4: abrupt step to a constant kF, after 2000 t", fontsize=8)
    fig.tight_layout(); fig.savefig(f"{O}/fig_prey_snaps_s{sd}.png", dpi=75); plt.close(fig)


if __name__ == "__main__":
    allS = {}
    for sd in [int(x) for x in sys.argv[1].split(",")]:
        S = summarize(sd); allS[sd] = S; fig(sd, S); fig_snaps(sd)
    json.dump(allS, open(f"{O}/summary_prey.json", "w"), indent=1)
    for sd, S in allS.items():
        for k, v in S["ramps"].items(): print(sd, k, v)
        for k, v in S["const"].items(): print(sd, "C" + k, v)
