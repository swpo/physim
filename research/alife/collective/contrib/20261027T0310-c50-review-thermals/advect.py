"""(c50) Is a rising cap carried by its own flow or a burning front? For each dividing track (divmove.json rows), at every
rendered frame inside the track: the fluid velocity averaged over the cap (heat-weighted, from the vorticity channel by a
periodic Poisson solve, psi = -lap^-1 om, u = (dpsi/dy, -dpsi/dx) in the world's sign convention checked against the cap
motion) projected on the cap's net direction, against the cap's own centroid speed along that direction.
usage: advect.py pack_seed_dir world.py"""
import sys, json, importlib.util, numpy as np
sys.path.insert(0, "/home/user/physim/research/alife")
from labkit import run as R, metrics as M
pack, wpath = sys.argv[1:3]
spec = importlib.util.spec_from_file_location("w", wpath); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
F = np.load(f"{pack}/frames.npz"); mat = F["matter"].astype(np.float32); rend = F["render"].astype(np.float64); rf = [int(x) for x in F["render_f"]]
ri = {f: i for i, f in enumerate(rf)}
m = json.load(open(f"{pack}/metrics.json")); dtf = m["steps_per_frame"] * m["dt"]
mn, thr, lo, hi = R._normalize_matter(mat, W.META, True, W.META.get("threshold")); H, Wd = mn.shape[1:]
comps, links = R._segment_frames(mn, thr, R._default_min_area(H, Wd), True)
tracks, ev = M.track(comps, links, (H, Wd), True); byid = {t["id"]: t for t in tracks}
L = W.P["L"] if "L" in W.P else 1.0
dx = 1.0
ky = 2 * np.pi * np.fft.fftfreq(H, d=dx)[:, None]; kx = 2 * np.pi * np.fft.fftfreq(Wd, d=dx)[None, :]
k2 = kx ** 2 + ky ** 2; k2[0, 0] = 1
ch = W.META["channels"]; iom = [i for i, c in enumerate(ch) if "vort" in c][0]; iT = 0
rows = json.load(open(f"{pack}/divmove.json"))["rows"]
res = []
for r in rows:
    t = byid[r["id"]]; n = len(t["cy"])
    sy = M._wrap(np.diff(t["cy"]), H); sx = M._wrap(np.diff(t["cx"]), Wd)
    u = np.array([sy.sum(), sx.sum()]); nu = np.hypot(*u)
    if nu == 0: continue
    u /= nu
    vc, vf = [], []
    for k in range(1, n - 1):
        f = t["start"] + k
        if f not in ri: continue
        om = rend[ri[f], iom]; Tm = rend[ri[f], iT]
        psih = np.fft.fft2(om) / k2; psih[0, 0] = 0
        uy = np.fft.ifft2(-1j * kx * psih).real; ux = np.fft.ifft2(1j * ky * psih).real
        msk = comps[f]["lab"] == t["comp"][k] + 1; w = Tm[msk]; w = w / w.sum()
        vf.append(((uy[msk] * w).sum() * u[0] + (ux[msk] * w).sum() * u[1]))
        vc.append((M._wrap(t["cy"][k + 1] - t["cy"][k - 1], H) * u[0] + M._wrap(t["cx"][k + 1] - t["cx"][k - 1], Wd) * u[1]) / (2 * dtf))
    if len(vc) >= 3: res.append((r["id"], r["BL_sqrtA"], float(np.mean(vc)), float(np.mean(vf))))
print(pack)
print(" id  BL_sqrtA  cap speed  fluid speed at cap (both along net direction, px/t; fluid sign up to the stream-function convention)")
for x in res: print(f" {x[0]} {x[1]:.1f} {x[2]:.3f} {x[3]:+.3f}")
a = np.array([[x[2], x[3]] for x in res])
print(f"median cap speed {np.median(a[:, 0]):.3f}, median |fluid| along {np.median(np.abs(a[:, 1])):.3f}, ratio fluid/cap {np.median(np.abs(a[:, 1]) / a[:, 0]):.2f}, sign agreement {np.mean(np.sign(a[:, 1]) == np.sign(a[:, 0])):.2f} (or {np.mean(np.sign(a[:, 1]) != np.sign(a[:, 0])):.2f} flipped)")
