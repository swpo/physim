"""Path of the largest body (the crawler that absorbs the others) in the noise-start world.
Every 0.25 time: label bodies (phi>1/2, periodic), take the largest, record its periodic centroid and area.
The centroid is unwrapped step to step; an absorption shifts it, so the net displacement over windows with no
change in body count is also reported. usage: python pathprobe.py world.py seed T out.json"""
import sys, json, importlib.util
import numpy as np
spec = importlib.util.spec_from_file_location("w", sys.argv[1]); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
seed, T, out = int(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
s = W.init(seed, W.META["size"]); L = W.P["L"]; dx = s["dx"]; every = int(round(0.25 / W.P["dt"])); k = 0; rows = []
while True:
    if k % every == 0:
        lab, nb = W.plabel(s["phi"] > 0.5)
        if nb:
            areas = np.bincount(lab.ravel())[1:]; j = int(areas.argmax()) + 1; m = lab == j
            c = [float((np.angle(np.exp(2j * np.pi * X[m] / L).mean()) % (2 * np.pi)) * L / (2 * np.pi)) for X in (s["x"], s["y"])]
            rows.append(dict(t=round(s["t"], 2), nb=int(nb), area=float(areas.max() * dx * dx), cx=c[0], cy=c[1]))
    if s["t"] >= T - 1e-9: break
    s = W.step(s); k += 1
# unwrap and summarise
t = np.array([r["t"] for r in rows]); c = np.array([[r["cx"], r["cy"]] for r in rows]); nb = np.array([r["nb"] for r in rows]); A = np.array([r["area"] for r in rows])
d = (np.diff(c, axis=0) + L / 2) % L - L / 2; path = np.r_[0, np.cumsum(np.hypot(*d.T))]; pos = np.r_[[c[0]], c[0] + np.cumsum(d, axis=0)]
diam = 2 * np.sqrt(A / np.pi)
res = dict(seed=seed, rows=rows)
# segments with constant body count (no absorption), from t>=2
segs = []; i0 = None
for i in range(len(t)):
    if t[i] < 2: continue
    if i0 is None: i0 = i
    if i == len(t) - 1 or nb[i + 1] != nb[i0]:
        net = float(np.hypot(*(pos[i] - pos[i0]))); segs.append(dict(t0=float(t[i0]), t1=float(t[i]), nb=int(nb[i0]), net=net, path=float(path[i] - path[i0]),
                     net_BL=net / float(diam[i0:i + 1].mean()), speed=net / max(float(t[i] - t[i0]), 1e-9)))
        i0 = None
res["segments"] = segs
m = t >= 2; res["total_path_fixed_1.7"] = float((path[m][-1] - path[m][0]) / 1.7)
res["net_t2_end_BL_own"] = float(np.hypot(*(pos[-1] - pos[m][0])) / diam[-1])
json.dump(res, open(out, "w"))
for g in segs: print(f"seed {seed} t {g['t0']:.2f}-{g['t1']:.2f} bodies {g['nb']} net {g['net']:.2f} = {g['net_BL']:.2f} own diameters, speed {g['speed']:.3f}")
print(f"seed {seed}: path t>=2 = {res['total_path_fixed_1.7']:.2f} x 1.7; net t=2..end = {res['net_t2_end_BL_own']:.2f} final diameters; final area {A[-1]:.2f}")
