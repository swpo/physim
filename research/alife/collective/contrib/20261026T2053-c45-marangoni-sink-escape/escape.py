"""(c45) Per disc: bodies (phi > 0 components >= 6 px, periodic centroids) inside the final radius R at opening, and how many
bodies remain inside R at closing (frame of t0 + R/v), from frames.npz matter; plus how many of the bodies inside at opening
have a body within 1.5 body-radii of a point outside R at closing is not attempted: survivors are counted as bodies anywhere
whose labkit-free nearest-neighbour link (greedy, displacement <= v_max * life) starts inside. usage: escape.py frames.npz disc.jsonl [R=24] [v=0.08] [frame_dt=5]"""
import sys, json, numpy as np
from scipy import ndimage
z = np.load(sys.argv[1]); M = z["matter"]; T = len(M); H, W = M.shape[1:]
discs = [json.loads(l) for l in open(sys.argv[2])]
R = float(sys.argv[3]) if len(sys.argv) > 3 else 24.0; v = float(sys.argv[4]) if len(sys.argv) > 4 else 0.08
FT = float(sys.argv[5]) if len(sys.argv) > 5 else 5.0
life = R / v
def bodies(f):
    lab, n = ndimage.label(M[f] > 0)
    for a, b in ((lab[:, 0], lab[:, -1]), (lab[0, :], lab[-1, :])):
        for x, y in zip(a, b):
            if x and y and x != y: lab[lab == y] = x
    out = []
    for k in np.unique(lab[lab > 0]):
        ys, xs = np.nonzero(lab == k)
        if len(ys) < 6: continue
        cy = (np.angle(np.exp(2j * np.pi * ys / H).mean()) % (2 * np.pi)) * H / (2 * np.pi)
        cx = (np.angle(np.exp(2j * np.pi * xs / W).mean()) % (2 * np.pi)) * W / (2 * np.pi)
        out.append((cy, cx, len(ys)))
    return out
def d(a, b, c, e):
    dy = abs(a - c); dy = min(dy, H - dy); dx = abs(b - e); dx = min(dx, W - dx); return np.hypot(dy, dx)
tot_in = tot_left_inside = 0
print("disc t0  inside_at_open  inside_at_close  removed(arm I)")
for k, e in enumerate(discs):
    f0 = int(np.ceil(e["t0"] / FT)); f1 = int((e["t0"] + life) / FT)
    if f1 >= T or f0 >= T: continue
    b0 = [b for b in bodies(f0) if d(b[0], b[1], e["cy"], e["cx"]) <= R]
    b1 = [b for b in bodies(f1) if d(b[0], b[1], e["cy"], e["cx"]) <= R]
    n0 = len(e["inside"]) if e.get("inside") is not None else len(b0)
    tot_in += n0; tot_left_inside += len(b1)
    print(f"{k:3d} {e['t0']:6.0f} {n0:8d} {len(b1):10d}   {len(e.get('removed', []))}")
print(f"all closed discs: {tot_in} bodies inside at opening, {tot_left_inside} bodies inside at closing")
