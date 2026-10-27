"""Per-seed figures and numbers for the kF ramp / constant-kF arms of world_ramp.py (c40 layered CIPS cells)."""
import glob, json, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(__file__))
from loadlog import load, tracks, series

O = "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/paperexp/supply-ramp"
KF0 = 0.2


def arm(sd, name):
    p = f"{O}/arms/s{sd}/{name}/log.jsonl"
    if not os.path.exists(p):
        return None
    meta, recs, evs = load(p)
    return {"meta": meta, "recs": recs, "evs": evs, "tr": tracks(recs)}


def summarize(sd):
    out = {"seed": sd, "ramps": {}, "const": {}}
    for name in ("R100", "R1000", "R4000"):
        a = arm(sd, name)
        if a is None:
            continue
        recs, evs = a["recs"], a["evs"]
        n0 = recs[0]["n"]
        deaths = [e for e in evs if e["ev"] == "death"]
        splits = [e for e in evs if e["ev"] == "split_child"]
        births = [e for e in evs if e["ev"] == "birth"]
        merges = [e for e in evs if e["ev"] == "merge_child"]
        ext = next((r for r in recs if r["n"] == 0), None)
        # kF at which the body count first falls below its start value and at which total body area halves
        A0 = recs[0]["body_area"]
        half = next((r for r in recs if r["body_area"] < 0.5 * A0), None)
        last = recs[-1]
        out["ramps"][name] = {
            "n_start": n0, "area_start": A0, "n_end": last["n"], "t_end": last["t_rel"],
            "deaths": len(deaths), "splits_children": len(splits), "births": len(births), "merge_children": len(merges),
            "death_kF": sorted(round(e["kF"], 4) for e in deaths),
            "death_t": sorted(e["t_rel"] for e in deaths),
            "extinct_t": ext["t_rel"] if ext else None, "extinct_kF": ext["kF"] if ext else None,
            "half_area_t": half["t_rel"] if half else None, "half_area_kF": half["kF"] if half else None,
        }
    for f in ("1", "0.75", "0.5", "0.25", "0.15", "0.125", "0.1"):
        a = arm(sd, f"C{f}")
        if a is None:
            continue
        recs, evs = a["recs"], a["evs"]
        late = [r for r in recs if r["t_rel"] >= recs[-1]["t_rel"] - 500]
        ext = next((r for r in recs if r["n"] == 0), None)
        areas_late = np.concatenate([r["areas"] for r in late]) if any(r["n"] for r in late) else np.array([])
        out["const"][f] = {
            "kF": recs[0]["kF"], "n_start": recs[0]["n"], "area_start": recs[0]["body_area"],
            "n_end": recs[-1]["n"], "area_end": recs[-1]["body_area"], "t_end": recs[-1]["t_rel"],
            "n_late_mean": float(np.mean([r["n"] for r in late])),
            "area_late_mean": float(np.mean([r["body_area"] for r in late])),
            "cell_area_late_median": float(np.median(areas_late)) if areas_late.size else 0.0,
            "cell_area_late_q": [float(np.percentile(areas_late, 25)), float(np.percentile(areas_late, 75))] if areas_late.size else None,
            "deaths": sum(e["ev"] == "death" for e in evs), "split_children": sum(e["ev"] == "split_child" for e in evs),
            "births": sum(e["ev"] == "birth" for e in evs), "merge_children": sum(e["ev"] == "merge_child" for e in evs),
            "extinct_t": ext["t_rel"] if ext else None,
            "F_bath_late": float(np.mean([r["F_bath"] for r in late])),
            "F_in_late_median": float(np.median(np.concatenate([r["F_in"] for r in late]))) if areas_late.size else None,
        }
    out["other"] = {}
    for name in ("H0.03", "H0.025", "TURN", "UP"):
        a = arm(sd, name)
        if a is None:
            continue
        recs, evs = a["recs"], a["evs"]
        late = [r for r in recs if r["t_rel"] >= recs[-1]["t_rel"] - 500]
        areas_late = np.concatenate([r["areas"] for r in late]) if any(r["n"] for r in late) else np.array([])
        ext = next((r for r in recs if r["n"] == 0), None)
        first_body = next((r for r in recs if r["n"] > 0), None)
        out["other"][name] = {
            "kF_end": recs[-1]["kF"], "n_start": recs[0]["n"], "area_start": recs[0]["body_area"],
            "n_end": recs[-1]["n"], "area_end": recs[-1]["body_area"], "t_end": recs[-1]["t_rel"],
            "n_late_mean": float(np.mean([r["n"] for r in late])), "area_late_mean": float(np.mean([r["body_area"] for r in late])),
            "cell_area_late_median": float(np.median(areas_late)) if areas_late.size else 0.0,
            "cell_area_late_q": [float(np.percentile(areas_late, 25)), float(np.percentile(areas_late, 75))] if areas_late.size else None,
            "deaths": sum(e["ev"] == "death" for e in evs), "death_t": [e["t_rel"] for e in evs if e["ev"] == "death"],
            "split_children": sum(e["ev"] == "split_child" for e in evs), "births": sum(e["ev"] == "birth" for e in evs),
            "extinct_t": ext["t_rel"] if ext else None,
            "first_body_t": first_body["t_rel"] if first_body else None, "first_body_kF": first_body["kF"] if first_body else None,
            "e_max_end": recs[-1]["e_max"], "e_std_start": recs[0]["e_std"], "e_std_end": recs[-1]["e_std"],
        }
    return out


def fig_main(sd, S):
    cols = {"R100": "#d62728", "R1000": "#ff7f0e", "R4000": "#1f77b4"}
    fig, ax = plt.subplots(2, 2, figsize=(11, 8.2))
    for name, c in cols.items():
        a = arm(sd, name)
        if a is None:
            continue
        t, n = series(a["recs"], "n")
        _, kf = series(a["recs"], "kF")
        _, A = series(a["recs"], "body_area")
        ax[0, 0].plot(t, n, color=c, label=f"{name}: kF 0.2 -> 0 over {name[1:]} t")
        ax[0, 1].plot(kf, n, color=c)
        ax[1, 0].plot(kf, A, color=c)
        for e in a["evs"]:
            if e["ev"] == "death":
                ax[0, 1].plot(e["kF"], -0.6, "v", color=c, ms=5, alpha=0.7)
        if name == "R4000":
            for i, h in a["tr"].items():
                ax[1, 1].plot(h[:, 1], h[:, 2], color=c, lw=0.6, alpha=0.6)
    # constant-kF arms: end-of-arm state (mean over last 500 t)
    for f, d in S["const"].items():
        lab = "constant kF, mean of last 500 t" if f == "1" else None
        ax[0, 1].plot(d["kF"], d["n_late_mean"], "ks", ms=7, mfc="none", label=lab)
        ax[1, 0].plot(d["kF"], d["area_late_mean"], "ks", ms=7, mfc="none", label=lab)
        if d["cell_area_late_q"]:
            ax[1, 1].errorbar(d["kF"], d["cell_area_late_median"], yerr=[[d["cell_area_late_median"] - d["cell_area_late_q"][0]], [d["cell_area_late_q"][1] - d["cell_area_late_median"]]], fmt="ks", mfc="none", ms=7, capsize=3, label=lab)
        else:
            ax[1, 1].plot(d["kF"], 0, "kx", ms=8)
    for name, mk in (("H0.03", "^"), ("H0.025", "^")):
        d = S.get("other", {}).get(name)
        if not d:
            continue
        lab = "slow ramp to 0.03, then hold (mean of last 500 t)" if name == "H0.03" else None
        ax[0, 1].plot(d["kF_end"], d["n_late_mean"], mk, color="#1f77b4", ms=9, mfc="none", label=lab)
        ax[1, 0].plot(d["kF_end"], d["area_late_mean"], mk, color="#1f77b4", ms=9, mfc="none", label=lab)
        if d["cell_area_late_q"]:
            ax[1, 1].plot(d["kF_end"], d["cell_area_late_median"], mk, color="#1f77b4", ms=9, mfc="none", label=lab)
    ax[0, 0].set_xlabel("time since branch (t)"); ax[0, 0].set_ylabel("cells (components e>0.5)"); ax[0, 0].set_xscale("symlog", linthresh=100)
    ax[0, 0].legend(fontsize=8)
    ax[0, 1].set_xlabel("current kF"); ax[0, 1].set_ylabel("cells"); ax[0, 1].invert_xaxis(); ax[0, 1].legend(fontsize=8, loc="upper right")
    ax[0, 1].set_title("triangles: kF at each cell's death", fontsize=9)
    ax[1, 0].set_xlabel("current kF"); ax[1, 0].set_ylabel("total cell area (px)"); ax[1, 0].invert_xaxis(); ax[1, 0].legend(fontsize=8)
    ax[1, 1].set_xlabel("current kF"); ax[1, 1].set_ylabel("area of each cell (px)"); ax[1, 1].invert_xaxis()
    ax[1, 1].set_title("lines: each cell in the 4000 t ramp; squares: constant-kF median, IQR", fontsize=9)
    ax[1, 1].legend(fontsize=8)
    fig.suptitle(f"seed {sd}: c40 layered CIPS cells branched at t=6000; fuel regrowth kF lowered linearly (default 0.2) or held at a constant fraction for 2000 t", fontsize=10)
    fig.tight_layout()
    fig.savefig(f"{O}/fig_ramp_s{sd}.png", dpi=80)
    plt.close(fig)


def snap_at(sd, name, tr):
    d = f"{O}/arms/s{sd}/{name}/snaps"
    fs = sorted(glob.glob(f"{d}/e_*.npy"))
    if not fs:
        return None, None
    ts = np.array([float(os.path.basename(f)[2:-4]) for f in fs])
    i = int(np.argmin(abs(ts - tr)))
    return np.load(fs[i]).astype(float), ts[i]


def fig_snaps(sd):
    rows = [("R4000", 4000, [0, 1000, 2000, 2800, 3000, 3200, 3400, 3500, 3600, 3700]),
            ("R1000", 1000, [0, 250, 500, 700, 800, 850, 900, 950, 1000, 1100]),
            ("R100", 100, [0, 50, 80, 100, 110, 120, 130, 140, 150, 200])]
    ncol = 10
    fig, ax = plt.subplots(5, ncol, figsize=(1.55 * ncol, 8.4))
    for a in ax.ravel():
        a.axis("off")
    for i, (name, T, tl) in enumerate(rows):
        for j, tr in enumerate(tl):
            im, tt = snap_at(sd, name, tr)
            if im is None:
                continue
            ax[i, j].imshow(im, cmap="magma", vmin=0, vmax=1)
            kk = KF0 * max(0.0, 1 - tt / T)
            ax[i, j].set_title(f"{name} t+{tt:.0f}\nkF={kk:.4f}", fontsize=6)
    consts = [("C1", 0.2), ("C0.75", 0.15), ("C0.5", 0.1), ("C0.25", 0.05), ("C0.15", 0.03), ("C0.125", 0.025), ("C0.1", 0.02)]
    for j, (f, k) in enumerate(consts):
        im, tt = snap_at(sd, f, 2000)
        if im is None:
            continue
        ax[3, j].imshow(im, cmap="magma", vmin=0, vmax=1)
        ax[3, j].set_title(f"step to kF={k:.3f}\nt+{tt:.0f}", fontsize=6)
    holds = [("H0.03", 1500, "slow ramp, then hold 0.03"), ("H0.025", 1500, "slow ramp, then hold 0.025"),
             ("TURN", 1000, "slow ramp to 0.03, back up to 0.2"), ("TURN", 2000, "same, +1000 t at 0.2"),
             ("UP", 1000, "from empty, kF up 0->0.1"), ("UP", 2000, "from empty, kF up 0->0.2"), ("UP", 4000, "from empty, +2000 t at 0.2")]
    for j, (name, tr, lab) in enumerate(holds):
        im, tt = snap_at(sd, name, tr)
        if im is None:
            continue
        ax[4, j].imshow(im, cmap="magma", vmin=0, vmax=1)
        ax[4, j].set_title(f"{lab}\n{name} t+{tt:.0f}", fontsize=5.5)
    fig.suptitle(f"seed {sd}: enzyme e (colour 0-1). Rows 1-3: linear ramps of kF from 0.2 to 0 (time after the branch, current kF). "
                 f"Row 4: abrupt step to a constant kF, after 2000 t. Row 5: holds, turn-back and re-supply arms", fontsize=8)
    fig.tight_layout()
    fig.savefig(f"{O}/fig_snaps_s{sd}.png", dpi=75)
    plt.close(fig)


if __name__ == "__main__":
    allS = {}
    for sd in [int(x) for x in sys.argv[1].split(",")]:
        S = summarize(sd)
        allS[sd] = S
        fig_main(sd, S)
        fig_snaps(sd)
    json.dump(allS, open(f"{O}/summary_main.json", "w"), indent=1)
    print(json.dumps(allS, indent=1)[:6000])
