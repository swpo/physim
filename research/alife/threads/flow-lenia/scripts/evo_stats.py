"""Per-kind mass and body counts over time for a parameter-localized world.

python threads/flow-lenia/scripts/evo_stats.py WORLD OUTPREFIX --steps 6000 --every 50 --seeds 0 1 2 --set k=v ...
Writes OUTPREFIX.json and OUTPREFIX.png (one panel per seed: mass and bodies per kind, plus total food).
Kind of a cell = nearest founder in log-parameter space; kind of a body = mass-weighted majority.
"""
import argparse
import ast
import json
import sys
from pathlib import Path

import numpy as np
from scipy import ndimage

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from labkit.world import load_world  # noqa: E402


def hard_kind(s):
    P, Fd = s["P"], s["founders"]
    lp = np.log(np.maximum(P, 1e-4))
    d = np.stack([((lp - np.log(np.maximum(f, 1e-4))[:, None, None]) ** 2).mean(0) for f in Fd])
    return d.argmin(0), d.min(0)


def run(world, seed, steps, every, sets):
    W = load_world(world)
    for kv in sets:
        k, v = kv.split("=", 1)
        try:
            v = ast.literal_eval(v)
        except Exception:
            pass
        W.CFG[k] = v
    s = W.init(seed, tuple(W.META["size"]))
    nk = len(s["founders"])
    rec = {"t": [], "mass": [], "bodies": [], "food": [], "dist": [], "gid_mass": []}
    thr = W.META.get("threshold") or 0.15
    for t in range(steps + 1):
        if t:
            s = W.step(s)
        if t % every == 0:
            A = s["A"].sum(0)
            kd, dist = hard_kind(s)
            rec["t"].append(t)
            rec["mass"].append([float(A[kd == j].sum()) for j in range(nk)])
            lab, n = ndimage.label(ndimage.gaussian_filter(A, 1, mode="wrap") > thr)
            cnt = [0] * nk
            for i in range(1, n + 1):
                m = lab == i
                if m.sum() < 6:
                    continue
                cnt[int(np.bincount(kd[m], A[m], nk).argmax())] += 1
            rec["bodies"].append(cnt)
            rec["food"].append(float(s["phi"].sum()) if "phi" in s else 0.0)
            rec["dist"].append(float((dist * A).sum() / max(A.sum(), 1e-9)))
            if "gid" in s:
                g = s["gid"].ravel(); w = np.bincount(g, A.ravel())
                rec["gid_mass"].append({int(i): float(w[i]) for i in np.nonzero(w > 1.0)[0]})
    if "gid" in s:
        rec["parents"] = s["parents"]; rec["born"] = s["born"]
        rec["P_by_gid"] = {int(g): s["P"][:, s["gid"] == g].mean(1).tolist() for g in np.unique(s["gid"][A > 0.1])}
    return rec


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("world"); ap.add_argument("out")
    ap.add_argument("--steps", type=int, default=6000)
    ap.add_argument("--every", type=int, default=50)
    ap.add_argument("--seeds", type=int, nargs="+", default=[0])
    ap.add_argument("--set", nargs="*", default=[])
    a = ap.parse_args()
    recs = {sd: run(a.world, sd, a.steps, a.every, a.set) for sd in a.seeds}
    Path(a.out + ".json").write_text(json.dumps({"args": vars(a), "runs": recs}))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    cols = ["tab:orange", "tab:cyan", "tab:purple", "tab:green"]
    fig, ax = plt.subplots(2, len(recs), figsize=(4 * len(recs), 5.5), squeeze=False)
    for c, (sd, r) in enumerate(recs.items()):
        t = np.array(r["t"]) * 0.2
        M = np.array(r["mass"]); B = np.array(r["bodies"])
        for j in range(M.shape[1]):
            ax[0, c].plot(t, M[:, j], color=cols[j % 4], label=f"kind{j} matter")
            ax[1, c].plot(t, B[:, j], color=cols[j % 4], label=f"kind{j} bodies")
        ax[0, c].plot(t, r["food"], "k:", lw=1, label="food")
        ax[0, c].set_title(f"seed {sd}: matter by kind"); ax[1, c].set_title(f"seed {sd}: bodies by kind")
        ax[0, c].legend(fontsize=7); ax[1, c].legend(fontsize=7); ax[1, c].set_xlabel("time")
    fig.suptitle(f"{Path(a.world).parent.name} {' '.join(a.set)}")
    fig.tight_layout(); fig.savefig(a.out + ".png", dpi=75)
    for sd, r in recs.items():
        print(sd, "final mass by kind", [round(x) for x in r["mass"][-1]], "bodies", r["bodies"][-1])
