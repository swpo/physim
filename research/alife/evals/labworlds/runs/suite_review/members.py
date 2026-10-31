"""Per-member distance to the truths in device1 groups (scaled RMS), native vs band vs null; and the
band's early-window ratios for comparison with the null's 1.52x global/phi claim. No simulation."""
import json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, "/home/user/swpo/residency-environments/environments/physim")
from physim.blobround6_eval import _energy_score
out = Path("/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/suite/pm")
suite = json.loads((out / "suite.json").read_text())
times = suite["cases"][0]["request"]["queries"][0]["t"]
G = {g["id"]: g for g in suite["groups"]}
def load(p):
    with np.load(p) as z:
        return [z[f"query{i}"] for i in range(3)]
def sel(a, g, T=1e9):
    keep = [(s, sc) for s, sc in zip(g["selectors"], g["scales"]) if times[s["time_index"]] <= T]
    return np.column_stack([a[s["query"]][:, s["time_index"], s["port"], s["slot"]] for s, _ in keep]) / np.array([sc for _, sc in keep])
d1 = [k for k in G if k.startswith("device1/")]
for cid in ("c006", "c007", "c013", "c002"):
    tr = load(out / "truth" / f"{cid}.npz")
    X = lambda a: np.hstack([sel(a, G[g]) for g in d1])
    T = X(tr)
    print(cid, "truth-truth rms", round(float(np.sqrt(((T[0] - T[1]) ** 2).mean())), 2))
    for name, p in (("native", out / "controls" / cid / "independent_native.npz"), ("band", out / "band" / f"{cid}.npz"),
                    ("null", out / "controls" / cid / "numerical_null.npz")):
        A = X(load(p))
        dist = np.sqrt(((A[:, None, :] - T[None]) ** 2).mean(axis=2)).min(axis=1)
        print(f"  {name:>6} member->nearest-truth rms:", np.round(np.sort(dist), 2))
# early window: band vs native, same as window_check for the null
cases = [c["request"]["id"] for c in suite["cases"]]
for T in (10, 50):
    rows = {k: {g: [] for g in G} for k in ("native", "band", "null")}
    for cid in cases:
        tr = load(out / "truth" / f"{cid}.npz")
        for k, p in (("native", out / "controls" / cid / "independent_native.npz"), ("band", out / "band" / f"{cid}.npz"),
                     ("null", out / "controls" / cid / "numerical_null.npz")):
            a = load(p)
            for g in G:
                rows[k][g].append(_energy_score(sel(a, G[g], T), sel(tr, G[g], T)))
    for k in ("band", "null"):
        print(f"T<={T} {k}/native per group:", {g.replace('global/', 'g/').replace('device', 'd'): round(np.mean(rows[k][g]) / np.mean(rows['native'][g]), 2) for g in G})
    # bootstrap the null global/phi early ratio
    rng = np.random.default_rng(0)
    for k in ("band", "null"):
        num, den = np.array(rows[k]["global/phi"]), np.array(rows["native"]["global/phi"])
        idx = rng.integers(0, len(num), (4000, len(num)))
        r = num[idx].mean(1) / den[idx].mean(1)
        print(f"   T<={T} {k} global/phi ratio {num.mean()/den.mean():.2f} 90% [{np.quantile(r,.05):.2f}, {np.quantile(r,.95):.2f}]")
