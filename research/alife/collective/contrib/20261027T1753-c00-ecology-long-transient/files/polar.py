"""c00: comet-orientation order and topological freezing of the c52 ecology.

Per render frame (400 t apart): every predator body (c_b > 0.5, >= 6 px, periodic) is paired with the prey body
(c_a > 0.5, >= 6 px) it overlaps most after a 3-px dilation; u = unit vector from the prey centroid to the predator
centroid (circular means, minimal image). Polar order P = |mean u| over pairs (1: all comets point the same way;
about 1/sqrt(N) for random orientations), and the fraction of predators that have a prey host.
Topological freezing (labkit per-species counts, every frame): t_last_change = last frame at which either count
changed; a run is FROZEN if neither count changed in its last 10000 t. Splits/merges with no net count change are
not seen by this test, so it is checked against the labkit persistent split frames and the images.
usage: polar.py <pack> [...]   (writes <pack>/polar.json)"""
import sys, json
import numpy as np
from scipy import ndimage
sys.path.insert(0, "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/paperexp/ecology-long-transient")
from analyze import bodies  # periodic labelling, area >= 6


def centroid(mask):
    H, W = mask.shape
    ys, xs = np.nonzero(mask)
    cy = np.angle(np.mean(np.exp(2j * np.pi * ys / H))) * H / (2 * np.pi) % H
    cx = np.angle(np.mean(np.exp(2j * np.pi * xs / W))) * W / (2 * np.pi) % W
    return cy, cx


def frame_order(ca, cb):
    H, W = ca.shape
    la, ia = bodies(ca)
    lb, ib = bodies(cb)
    us, hosted = [], 0
    for j, _ in ib:
        m = lb == j
        pad = np.pad(m, 3, mode="wrap")
        g = ndimage.binary_dilation(pad, iterations=3)[3:3 + H, 3:3 + W]
        ov = la[g & (la > 0)]
        ov = [v for v in ov if v in {i for i, _ in ia}]
        if not ov:
            continue
        hosted += 1
        host = np.bincount(ov).argmax()
        py, px = centroid(m)
        qy, qx = centroid(la == host)
        dy = (py - qy + H / 2) % H - H / 2
        dx = (px - qx + W / 2) % W - W / 2
        n = np.hypot(dy, dx)
        if n > 0.5:
            us.append((dy / n, dx / n))
    if not us:
        return {"n_pairs": 0, "P": None, "hosted_frac": 0.0 if ib else None, "n_pred": len(ib), "n_prey": len(ia)}
    u = np.array(us)
    P = float(np.hypot(*u.mean(0)))
    return {"n_pairs": len(us), "P": round(P, 3), "P_random": round(1 / np.sqrt(len(us)), 3),
            "angle_deg": round(float(np.degrees(np.arctan2(*u.mean(0)))), 1),
            "hosted_frac": round(hosted / len(ib), 3), "n_pred": len(ib), "n_prey": len(ia)}


for pk in sys.argv[1:]:
    pk = pk.rstrip("/")
    z = np.load(f"{pk}/frames.npz")
    R, rf = z["render"].astype(np.float32), z["render_f"] * 100.0
    rows = []
    for k in range(len(R)):
        if rf[k] < 2400:
            continue
        d = frame_order(R[k, 0], R[k, 1]); d["t"] = float(rf[k]); rows.append(d)
    m = json.load(open(f"{pk}/metrics.json"))
    a = np.array(m["species"]["prey"]["n_comp"]); b = np.array(m["species"]["predator"]["n_comp"])
    ch = np.nonzero((np.diff(a) != 0) | (np.diff(b) != 0))[0]
    t_last = float((ch[-1] + 1) * 100.0) if len(ch) else None
    T = (len(a) - 1) * 100.0
    n_changes_last10k = int(((ch + 1) * 100.0 > T - 10000).sum())
    Ps = [(r["t"], r["P"]) for r in rows if r["P"] is not None]
    def win(t0, t1):
        v = [p for t, p in Ps if t0 <= t < t1]
        return round(float(np.mean(v)), 3) if v else None
    out = {"pack": pk, "t_last_count_change": t_last, "count_changes_last_10000t": n_changes_last10k,
           "frozen": n_changes_last10k == 0, "final_counts": [int(a[-1]), int(b[-1])],
           "P_mean_by_6000t": {f"{t0}-{t0 + 6000}": win(t0, t0 + 6000) for t0 in range(0, 48000, 6000)},
           "P_random_typ": round(float(np.median([r["P_random"] for r in rows if r.get("P_random")])), 3),
           "hosted_frac_median": round(float(np.median([r["hosted_frac"] for r in rows if r["hosted_frac"] is not None])), 3),
           "rows": rows}
    json.dump(out, open(f"{pk}/polar.json", "w"))
    print(pk.split("/")[-1], "frozen", out["frozen"], "t_last_change", t_last, "changes last 10k", n_changes_last10k,
          "P by window", list(out["P_mean_by_6000t"].values()), "P_random~", out["P_random_typ"], "hosted", out["hosted_frac_median"])
