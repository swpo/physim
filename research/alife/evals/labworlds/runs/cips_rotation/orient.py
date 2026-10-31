"""Orientation history of each dividing body from the 250-t snapshots. usage: orient.py RUN [RUN ...]

For every persistent division, the parent is followed back through the snapshots (the component whose centroid is
nearest the previous match, within 12 world units). Per snapshot: long-axis angle (deg from grid x), aspect,
area. Reports, per division: the angle at the first snapshot with aspect >= 1.3 ("orientation chosen") and its
distance to the nearest grid diagonal, and the angle 250 t before the split.
"""
import json, sys
from pathlib import Path
import numpy as np

sys.path.insert(0, "/home/user/physim/research/alife")
from labkit import metrics as M  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parent))
from rotdiv import comp_moments, wrap  # noqa: E402

OUT = Path(__file__).resolve().parent / "out"


def d_diag(a):
    r = a % 90
    return 45 - min(r, 90 - r)


res = {}
for run in sys.argv[1:]:
    J = json.loads((OUT / f"{run}.json").read_text())
    Z = np.load(OUT / f"{run}_snaps.npz")
    N = J["N"]; dx = J["dx"]
    times = sorted(int(k[3:]) for k in Z.files if k.startswith("e_t"))
    snap = {}
    for t in times:
        e = Z[f"e_t{t}"].astype(float)
        seg = M.segment(e, 0.5, int(np.ceil(6 / dx ** 2)), True)
        ang, asp = comp_moments(seg["lab"], seg["n"], N)
        snap[t] = (seg["cy"] * dx, seg["cx"] * dx, ang, asp, seg["area"] * dx * dx)
    out = []
    for d in J["persistent_divisions"]:
        cy, cx = d["parent_centroid"]
        hist = []
        for t in [t for t in times if t < d["t"]][::-1]:
            Y, X, A, R, S = snap[t]
            if len(Y) == 0:
                break
            dist = np.hypot(wrap(Y - cy, N * dx), wrap(X - cx, N * dx))
            j = int(np.argmin(dist))
            if dist[j] > 12:
                break
            hist.append((t, round(float(A[j]), 1), round(float(R[j]), 2), round(float(S[j]))))
            cy, cx = Y[j], X[j]
        hist = hist[::-1]
        first = next((h for h in hist if h[2] >= 1.3), None)
        out.append(dict(t_split=d["t"], axis_at_split=round(d.get("daughter_axis_0t", np.nan), 1),
                        first_elongated=first, first_d_diag=round(d_diag(first[1]), 1) if first else None,
                        history=hist))
    res[run] = out
    fe = [o["first_d_diag"] for o in out if o["first_d_diag"] is not None]
    print(run, "first-elongation d_diag:", fe, "| times:", [o["first_elongated"][0] if o["first_elongated"] else None for o in out])
json.dump(res, open(OUT / "orient.json", "w"), indent=1)
