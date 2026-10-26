"""c43: motion of CGLE gain pulses. Label |A|>0.5 in every saved frame, link each body to the nearest body in the next
frame (periodic) when the centroid moved < 4 px and the area changed by < 30%; a track ends at any other event
(split, merge, area jump). Net displacement of each track in body lengths, with body length = the long axis
(2 x sqrt of the largest eigenvalue of the pixel covariance x 2), never less than sqrt(area).
usage: python motion.py frames.npz DT_FRAME OUT.json"""
import sys, json, numpy as np
from scipy import ndimage
M = np.load(sys.argv[1])["matter"]; dtf = float(sys.argv[2]); H, W = M.shape[1:]
def bodies(f):
    lab, n = ndimage.label(f > 0.5)
    out = []
    for i in range(1, n + 1):
        yy, xx = np.nonzero(lab == i)
        if len(yy) < 8: continue
        # periodic-safe centroid via angles
        cy = (np.angle(np.exp(2j * np.pi * yy / H).mean()) * H / (2 * np.pi)) % H
        cx = (np.angle(np.exp(2j * np.pi * xx / W).mean()) * W / (2 * np.pi)) % W
        dy = (yy - cy + H / 2) % H - H / 2; dx = (xx - cx + W / 2) % W - W / 2
        ev = np.linalg.eigvalsh(np.cov(np.stack([dy, dx])))
        L = max(4 * np.sqrt(ev[-1]), np.sqrt(len(yy)))
        out.append((cy, cx, len(yy), L))
    return out
B = [bodies(f) for f in M]
def wrap(d, P): return (d + P / 2) % P - P / 2
tracks, active = [], {}
for t in range(len(B) - 1):
    nxt = {}
    used = set()
    for j, (cy, cx, a, L) in enumerate(B[t]):
        cands = [(np.hypot(wrap(b[0] - cy, H), wrap(b[1] - cx, W)), k) for k, b in enumerate(B[t + 1])]
        if not cands: continue
        d, k = min(cands)
        b = B[t + 1][k]
        # unique match both ways
        back = min((np.hypot(wrap(c[0] - b[0], H), wrap(c[1] - b[1], W)), q) for q, c in enumerate(B[t]))[1]
        if d < 4 and abs(b[2] / a - 1) < 0.3 and back == j and k not in used:
            used.add(k)
            tr = active.get(j, {"t0": t, "path": [(0.0, 0.0)], "L": [L], "a": [a]})
            py, px = tr["path"][-1]
            tr["path"].append((py + wrap(b[0] - cy, H), px + wrap(b[1] - cx, W))); tr["L"].append(b[3]); tr["a"].append(b[2])
            nxt[k] = tr
        elif j in active:
            tracks.append(active[j])
    for j in active:
        if j not in [k for k in nxt] and all(active[j] is not v for v in nxt.values()) and active[j] not in tracks:
            tracks.append(active[j])
    active = nxt
tracks += [v for v in active.values() if v not in tracks]
res = []
for tr in tracks:
    if len(tr["path"]) < 10: continue
    p = np.array(tr["path"]); net = float(np.hypot(*(p[-1] - p[0]))); Lm = float(np.median(tr["L"]))
    path = float(np.sum(np.hypot(*np.diff(p, axis=0).T)))
    res.append({"t0": tr["t0"] * dtf, "dur": (len(p) - 1) * dtf, "net_px": net, "path_px": path, "body_len_px": Lm,
                "net_body_lengths": net / Lm, "area_med": float(np.median(tr["a"]))})
res.sort(key=lambda r: -r["net_body_lengths"])
json.dump({"n_tracks_ge10frames": len(res), "n_ge3_lengths": sum(r["net_body_lengths"] >= 3 for r in res), "tracks": res}, open(sys.argv[3], "w"), indent=0)
print(len(res), sum(r["net_body_lengths"] >= 3 for r in res)); [print({k: round(v, 1) for k, v in r.items()}) for r in res[:8]]
