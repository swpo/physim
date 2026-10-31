"""One noise-free behaviour run at a given grid and dt (fixed 128-unit box), recorded at 128^2.

python behav.py --world fv|pm --seed S --N N [--dt DT] --T T [--rot 45] --out OUT.npz

Every frame (fv: 3 t, pm: 50 t, as the claims' packs) the run's fields are area-averaged
onto the 128^2 world-unit grid, so labkit's segmentation, tracking and lineage see the same
pixels at every resolution. phase_membrane also gets fine-grid census measures every 500 t
from t=2000 (L ring in world units, wall-normal anisotropy), as in c01's ringmeasure.py.
"""
import argparse
import json
import time

import numpy as np
from scipy import ndimage

import cc
from labkit import metrics as M

ap = argparse.ArgumentParser()
ap.add_argument("--world", required=True)
ap.add_argument("--seed", type=int, required=True)
ap.add_argument("--N", type=int, default=128)
ap.add_argument("--dt", type=float, default=None)
ap.add_argument("--T", type=float, required=True)
ap.add_argument("--rot", type=float, default=0.0)
ap.add_argument("--out", required=True)
a = ap.parse_args()

W, st = cc.start_state(a.world, a.seed, a.N, a.dt, a.rot)
dt = float(W.P["dt"])
fdt = 3.0 if a.world == "fv" else 50.0
spf = int(round(fdt / dt))
frames = int(round(a.T / fdt))
s = a.N / cc.N0           # pixels per world unit
dxw = 1.0 / s             # world units per pixel


def wall_anisotropy(phi):
    """|grad phi|-weighted <cos 4 psi> of the wall normal (0.1 < phi < 0.9): +1 axis-facing, -1 diagonal."""
    gy = (np.roll(phi, -1, 0) - np.roll(phi, 1, 0)) / (2 * dxw)
    gx = (np.roll(phi, -1, 1) - np.roll(phi, 1, 1)) / (2 * dxw)
    m = (phi > 0.1) & (phi < 0.9)
    w = np.hypot(gy, gx)[m]
    psi = np.arctan2(gy[m], gx[m])
    return float((w * np.cos(4 * psi)).sum() / max(w.sum(), 1e-12))


def ring_census(phi, L):
    """c01's ringmeasure in world units: rim d <= 2, core d >= 0.6 max d, max d >= 3.5, area >= 40."""
    ins = phi > 0.5
    big = np.tile(ins, (3, 3))
    n0 = ins.shape[0]
    d_in = ndimage.distance_transform_edt(big)[n0:2 * n0, n0:2 * n0] * dxw
    d_out = ndimage.distance_transform_edt(~big)[n0:2 * n0, n0:2 * n0] * dxw
    lab, n = M.periodic_label(ins, True)     # cells wrapped over the box edge are one cell
    ratios = []
    for i in range(1, n + 1):
        c = lab == i
        if c.sum() * dxw**2 < 40:
            continue
        dm = d_in[c].max()
        if dm < 3.5:
            continue
        rim, core = c & (d_in <= 2), c & (d_in >= 0.6 * dm)
        ratios.append(float(L[rim].mean() / max(L[core].mean(), 1e-9)))
    outside = (d_out >= 2) & (d_out <= 5)
    rim_all = ins & (d_in <= 2)
    return dict(cells=len(ratios), ring_median=float(np.median(ratios)) if ratios else None,
                rim_over_out=float(L[rim_all].mean() / max(L[outside].mean(), 1e-9)) if rim_all.any() else None)


rec, census, snaps = [], [], {}
t0 = time.process_time()
snap_t = {0, int(frames // 2), frames} if a.world == "fv" else {0, 40, 100, frames}
status = "ok"
for f in range(frames + 1):
    if f:
        for _ in range(spf):
            st = W.step(st)
    t = f * fdt
    if a.world == "fv":
        om = st["om"]
        if not np.isfinite(om).all():
            status = f"non-finite at frame {f}"
            break
        rec.append(cc.restrict(om).astype(np.float32))
        if f in snap_t:
            snaps[f"om_{f}"] = om.astype(np.float32)
            snaps[f"Y_{f}"] = st["Y"].astype(np.float32)
    else:
        phi, K, L = st["phi"], st["K"], st["L"]
        if not np.isfinite(phi).all():
            status = f"non-finite at frame {f}"
            break
        m = K + L + 4 * phi * (1 - phi)            # world.matter(fields)
        rec.append(np.stack([cc.restrict(m), cc.restrict(phi)]).astype(np.float32))
        if t >= 2000 and int(round(t)) % 500 == 0:
            census.append(dict(t=t, wall_A4=wall_anisotropy(phi), **ring_census(phi, L)))
        if f in snap_t:
            snaps[f"phi_{f}"] = phi.astype(np.float32)
            snaps[f"L_{f}"] = L.astype(np.float32)
cpu = time.process_time() - t0
meta = dict(world=a.world, seed=a.seed, N=a.N, dt=dt, T=a.T, rot=a.rot, fdt=fdt, spf=spf, frames=frames,
            overrides=cc.refine_overrides(a.world, a.N, a.dt), status=status, cpu_s=cpu)
np.savez_compressed(a.out, rec=np.stack(rec), meta=json.dumps(meta), census=json.dumps(census), **snaps)
print(json.dumps(dict(meta, census_last=census[-1] if census else None)), flush=True)
