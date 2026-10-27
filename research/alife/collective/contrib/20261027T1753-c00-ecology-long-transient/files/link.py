"""c00: does comet alignment (polar order P) go with the end of division? Window-level test across runs.
For every run and every 6000-t window from 6000 to 42000 (all eligible for persistent splits): mean P (polar.json),
persistent splits of both kinds per predator body per 1000 t, and body-count changes (either kind) per body per 1000 t.
Only boxes >= 48^2 (>= ~7 pairs, random P <= ~0.35) enter the binned table, since with 2-4 pairs P is high by chance.
usage: link.py <out.json> <pack> [...]"""
import sys, json, numpy as np
from scipy import stats
rows = []
for pk in sys.argv[2:]:
    pk = pk.rstrip("/")
    d = json.load(open(f"{pk}/long.json")); pol = json.load(open(f"{pk}/polar.json"))
    L = d["size"][0]
    a = np.array(d["prey"]["n"]); b = np.array(d["predator"]["n"])
    for wp, wq in zip(d["prey"]["windows"], d["predator"]["windows"]):
        t0 = wp["t0"]
        if t0 < 6000 or t0 >= 42000:
            continue
        f0, f1 = int(t0 / 100), int(t0 / 100) + 60
        P = [r["P"] for r in pol["rows"] if t0 <= r["t"] < t0 + 6000 and r["P"] is not None]
        pairs = max(1.0, wq["mean_count"])
        ch = int(((np.diff(a[f0:f1 + 1]) != 0) | (np.diff(b[f0:f1 + 1]) != 0)).sum())
        rows.append({"run": pk.split("/")[-1], "L": L, "t0": t0, "P": float(np.mean(P)) if P else None,
                     "div_rate": 1000 * (wp["persistent_splits"] + wq["persistent_splits"]) / 6000 / pairs,
                     "change_rate": 1000 * ch / 6000 / pairs})
big = [r for r in rows if r["L"] >= 48 and r["P"] is not None]
out = {"rows": rows}
if big:
    P = np.array([r["P"] for r in big]); D = np.array([r["div_rate"] for r in big]); C = np.array([r["change_rate"] for r in big])
    rho, p = stats.spearmanr(P, D)
    rho2, p2 = stats.spearmanr(P, C)
    bins = [(0, 0.5), (0.5, 0.8), (0.8, 1.01)]
    tab = []
    for lo, hi in bins:
        s = (P >= lo) & (P < hi)
        tab.append({"P_bin": [lo, hi], "n_windows": int(s.sum()), "runs": sorted({big[i]["run"] for i in np.nonzero(s)[0]}),
                    "div_rate_mean": round(float(D[s].mean()), 4) if s.any() else None,
                    "frac_windows_without_division": round(float((D[s] == 0).mean()), 3) if s.any() else None,
                    "change_rate_mean": round(float(C[s].mean()), 4) if s.any() else None})
    out.update({"n_windows_L48plus": len(big), "spearman_P_vs_div": [round(float(rho), 3), float(p)],
                "spearman_P_vs_changes": [round(float(rho2), 3), float(p2)], "binned": tab})
    print("windows (L>=48):", len(big), "Spearman P vs division rate", round(float(rho), 3), "p", f"{p:.2g}",
          "| P vs count-change rate", round(float(rho2), 3), "p", f"{p2:.2g}")
    for t in tab:
        print("  ", t)
json.dump(out, open(sys.argv[1], "w"), indent=1)
