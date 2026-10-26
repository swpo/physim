"""(c45) Fate of the bodies a sink disc opens on (Q:marangoni-sink-escape), with labkit's own segmentation and tracker.
For each disc that closes within the run: the labkit components whose centroid lies within R of the centre at the first
frame after opening; follow each one's track and its descendants (children through splits and merges) to the closing frame.
A body ESCAPES if some descendant is alive at closing with centroid outside R, DISSOLVES if no descendant is alive at
closing, STAYS if descendants are alive but all inside R. Also: dividing tracks (split-born, >= 2 daughters living >= 20
frames) with D (net / median 4 sqrt(lambda_max), extract.py) and descendants alive two median cycles after birth, for the
selection regression. usage: fate.py frames.npz world.py disc.jsonl table.json label [R=24] [v=0.08]"""
import sys, json, importlib.util, numpy as np
sys.path.insert(0, "/home/user/physim/research/alife")
from labkit import run as LR, metrics as M
fn, wpath, discf, tabf, label = sys.argv[1:6]
R = float(sys.argv[6]) if len(sys.argv) > 6 else 24.0; v = float(sys.argv[7]) if len(sys.argv) > 7 else 0.08
F = np.load(fn); mat = F["matter"].astype(np.float32)
spec = importlib.util.spec_from_file_location("w", wpath); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
FT = W.META["steps_per_frame"] * W.P["dt"]
mn, thr, lo, hi = LR._normalize_matter(mat, W.META, True, W.META.get("threshold")); H, Wd = mn.shape[1:]
comps, links = LR._segment_frames(mn, thr, LR._default_min_area(H, Wd), True)
tracks, ev = M.track(comps, links, (H, Wd), True); byid = {t["id"]: t for t in tracks}; T = len(comps)
def dist(a, b, c, e):
    dy = abs(a - c); dy = min(dy, H - dy); dx = abs(b - e); dx = min(dx, Wd - dx); return np.hypot(dy, dx)
def track_at(f, j):
    for t in tracks:
        if t["start"] <= f <= t["end"] and t["comp"][f - t["start"]] == j: return t["id"]
def alive_desc(tid, f):
    out, stack, seen = [], [tid], set()
    while stack:
        x = stack.pop()
        if x in seen: continue
        seen.add(x); t = byid[x]
        if t["start"] <= f <= t["end"]: out.append(x)
        elif t["end"] < f: stack += t["children"]
    return out
discs = [json.loads(l) for l in open(discf)]
res = {"escape": 0, "dissolve": 0, "stay": 0}; rows = []
for e in discs:
    f0 = int(np.ceil(e["t0"] / FT)) + 1; f1 = int((e["t0"] + R / v) / FT)
    if f1 >= T: continue
    for j in range(len(comps[f0]["area"])):
        if dist(comps[f0]["cy"][j], comps[f0]["cx"][j], e["cy"], e["cx"]) > R: continue
        tid = track_at(f0, j)
        if tid is None: continue
        al = alive_desc(tid, f1)
        if not al: fate = "dissolve"
        else:
            out = [x for x in al if dist(byid[x]["cy"][f1 - byid[x]["start"]], byid[x]["cx"][f1 - byid[x]["start"]], e["cy"], e["cx"]) > R]
            fate = "escape" if out else "stay"
        res[fate] += 1; rows.append((round(e["t0"]), tid, fate))
n = sum(res.values())
print(f"{label}: bodies inside a disc's final radius one frame after it opened: {n}; escape {res['escape']}, dissolve {res['dissolve']}, stay {res['stay']}; escape share {res['escape'] / max(n, 1):.2f}")
# selection on dividing tracks: descendants alive two median cycles after birth
tab = json.load(open(tabf))["rows"]; dv = [r for r in tab if r["dividing"]]
if dv:
    mc = np.median([r["cycle"] for r in dv]) / FT
    X, Y = [], []
    for r in dv:
        f = int(r["start"] + 2 * mc)
        if f >= T: continue
        Y.append(len(alive_desc(r["id"], f))); X.append([r["disp_rl"], r["vpath"], r["straight"]])
    X = np.array(X, float); Y = np.array(Y, float)
    if len(Y) > 5:
        Z = (X - X.mean(0)) / X.std(0); A = np.c_[np.ones(len(Z)), Z]; w = Y / max(Y.mean(), 1e-9)
        beta = np.linalg.lstsq(A, w, rcond=None)[0]
        rng = np.random.default_rng(0); bs = []
        for _ in range(2000):
            i = rng.integers(0, len(Y), len(Y)); bs.append(np.linalg.lstsq(A[i], w[i], rcond=None)[0])
        lo_, hi_ = np.percentile(bs, [2.5, 97.5], axis=0)
        print(f"  selection (relative descendants at birth + 2 median cycles ({2 * mc:.0f} frames) on standardized D, speed, straightness; n={len(Y)}, mean descendants {Y.mean():.2f}):")
        for k, nm in enumerate(["D", "path speed", "straightness"]):
            print(f"    gradient on {nm}: {beta[k + 1]:+.3f} [{lo_[k + 1]:+.3f}, {hi_[k + 1]:+.3f}]")
    D = np.array([r["disp_rl"] for r in dv])
    print(f"  dividing tracks {len(dv)}: median D {np.median(D):.2f}, D>=3 {int((D >= 3).sum())}, median path speed {np.median([r['vpath'] for r in dv]):.3f}, median cycle {np.median([r['cycle'] for r in dv]):.0f}")
