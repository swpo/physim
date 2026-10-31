"""Behaviour of c40's CIPS cells at two resolutions, same seeds, same physical times (no dynamics noise, as claimed).

usage: capab.py SEED DT N T_END T_CUT T_AFTER OUTNAME
  Main run from init(SEED) to T_END. Every 20 t: labkit segmentation of e > 0.5 (labkit.metrics.segment, 4-connected,
  periodic, min area 6 world units^2) and overlap links; at the end labkit's track + lineage_stats with K = 20 frames
  (400 t; the claim's packs used 20 frames of 100 t), so a persistent split needs both lineages to survive 400 t,
  each child 120 t as one component, and no sibling re-merge. Every 250 t: the s layer of every body by signed
  distance to the e = 0.5 contour in world units (ring.py's measure: rim |d| <= 1.5, core >= 3 inside, outside
  4-7 outside and nearest this body; a body passes when rim/core >= 1.5 and rim/outside >= 1.5).
  Local fuel cut (c42's cut.py rule): at T_CUT the body whose nearest other body is farthest; kF = 0 in a disk of
  radius max(14, 0.75 nearest distance) world units (c42 review, FRAC 0.75) around it for T_AFTER; the main run is its fed twin.
  N != 192: the native init(SEED) fields are resampled onto the finer grid (same initial continuum field) and
  Lsc, rf_len scale with N (fixed physical box of 192 world units).
"""
import os
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[v] = "1"
import copy, json, sys, time
import numpy as np
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv, ARGS = sys.argv[:1], sys.argv[1:]
import cconv as K  # noqa: E402
sys.path.insert(0, K.C.LAB)
from labkit import metrics as M  # noqa: E402

seed, dt, N, T_END, T_CUT, T_AFTER, name = int(ARGS[0]), float(ARGS[1]), int(ARGS[2]), float(ARGS[3]), float(ARGS[4]), float(ARGS[5]), ARGS[6]
dx = K.L_BOX / N
FRAME, RING_EVERY, KF = 20.0, 250.0, 20
MIN_AREA = int(np.ceil(6 / dx ** 2))
w = K.world(dt, N, sd=0.0, ell=0.0)
m = w.load(); K.C.one_worker(m)
s = m.init(seed, (N, N))
if N != K.L_BOX:
    m0 = K.world(0.1, K.L_BOX, sd=0.0, ell=0.0).load()
    s0 = m0.init(seed, (K.L_BOX, K.L_BOX))
    for f in K.FIELDS:
        s[f] = np.clip(K.regrid(s0[f], N), *K.CLIPS[f])
assert abs(s["par"]["dt"] - dt) < 1e-12 and abs(s["par"]["Lsc"] - 3.0 * N / K.L_BOX) < 1e-12


def ring_measure(e, sv):
    pad = int(np.ceil(24 / dx))
    E = np.pad(e, pad, mode="wrap"); S = np.pad(sv, pad, mode="wrap"); msk = E > 0.5
    din = ndimage.distance_transform_edt(msk, sampling=dx)
    dout, (iy, ix) = ndimage.distance_transform_edt(~msk, sampling=dx, return_indices=True)
    lab, n = ndimage.label(msk, structure=np.ones((3, 3)))
    near = lab[iy, ix]
    res = []
    for i in range(1, n + 1):
        b = lab == i
        if b.sum() * dx * dx < 6:
            continue
        cy, cx = ndimage.center_of_mass(b)
        if not (pad <= cy < pad + N and pad <= cx < pad + N):
            continue
        core = b & (din >= 3); rim = (b & (din <= 1.5)) | ((near == i) & (dout <= 1.5) & ~msk)
        outs = (near == i) & (dout >= 4) & (dout <= 7)
        if core.sum() < 3 or outs.sum() < 3:
            continue
        yy_, xx_ = np.nonzero(b)
        cov = np.cov(np.stack([yy_ - yy_.mean(), xx_ - xx_.mean()]))
        ev, evec = np.linalg.eigh(cov)
        aspect = float(np.sqrt(ev[1] / max(ev[0], 1e-12)))
        ang = float(np.degrees(np.arctan2(evec[0, 1], evec[1, 1])) % 180)   # long axis angle from the x axis
        res.append((float(S[rim].mean() / S[core].mean()), float(S[rim].mean() / S[outs].mean()), float(b.sum() * dx * dx), aspect, ang))
    return res


def bodies(e):
    seg = M.segment(e, 0.5, MIN_AREA, True)
    return seg


t0 = time.process_time()
comps, links, prev = [], [None], None
rings, counts = [], []
nsteps = int(round(T_END / dt))
fr_every, ring_every, cut_step = int(round(FRAME / dt)), int(round(RING_EVERY / dt)), int(round(T_CUT / dt))
cut_state = None
snaps = {}
fed_target = []
for k in range(0, nsteps + 1):
    if k % fr_every == 0:
        seg = bodies(s["e"])
        comps.append(dict(area=seg["area"], cy=seg["cy"], cx=seg["cx"], n=seg["n"]))   # pixels, as labkit (overlap counts are pixels)
        if prev is not None:
            links.append(M.overlaps(prev["lab"], prev["n"], seg["lab"], seg["n"]))
        prev = seg
        counts.append((round(k * dt, 3), int(seg["n"]), float(seg["area"].sum() * dx * dx), float(s["F"].mean()), float(s["e"].max())))
    if k % ring_every == 0 and k > 0:
        r = ring_measure(s["e"], s["s"])
        ok = [x for x in r if x[0] >= 1.5 and x[1] >= 1.5]
        rings.append(dict(t=round(k * dt), bodies=len(r), passed=len(ok),
                          rim_core_min=min(x[0] for x in r) if r else None, rim_core_median=float(np.median([x[0] for x in r])) if r else None,
                          rim_out_min=min(x[1] for x in r) if r else None, rim_out_median=float(np.median([x[1] for x in r])) if r else None,
                          elongated_axes=[(round(x[3], 2), round(x[4])) for x in r if x[3] >= 1.5]))
    if k % int(round(500 / dt)) == 0:
        snaps[f"t{int(round(k * dt))}"] = np.stack([s["e"], s["s"]]).astype(np.float32)
    if k == cut_step:
        cut_state = copy.deepcopy(s)
    if cut_state is not None and k >= cut_step and k <= cut_step + int(round(T_AFTER / dt)) and (k - cut_step) % int(round(10 / dt)) == 0:
        fed_target.append(s["e"].copy())
    if k < nsteps:
        s = m.step(s)
cpu_main = time.process_time() - t0
tracks, events = M.track(comps, links, (N, N), True)
lin = M.lineage_stats(tracks, events, len(comps), FRAME, (N, N), True, K=KF)
splits = [e for e in events if e["type"] == "split"]
merges = [e for e in events if e["type"] == "merge"]

# local fuel cut from the state at T_CUT
t1 = time.process_time()
seg = bodies(cut_state["e"])
cs = list(zip(seg["cy"], seg["cx"]))


def pdist(a, b):
    dy = abs(a[0] - b[0]); dy = min(dy, N - dy); dxx = abs(a[1] - b[1]); dxx = min(dxx, N - dxx)
    return float(np.hypot(dy, dxx)) * dx


nn = [min(pdist(c, d) for j, d in enumerate(cs) if j != i) for i, c in enumerate(cs)]
it = int(np.argmax(nn)); tgt = cs[it]; R = max(14.0, 0.75 * nn[it])
yy, xx = np.mgrid[0:N, 0:N]
ddy = (yy - tgt[0] + N / 2) % N - N / 2; ddx = (xx - tgt[1] + N / 2) % N - N / 2
disk = (ddy * ddy + ddx * ddx) * dx * dx <= R * R
a = copy.deepcopy(cut_state)
a["par"] = dict(a["par"], cut_t=T_CUT - 1e-9, cut_r=R / dx, cut_y=float(tgt[0]), cut_x=float(tgt[1]))
cut_log = []
n_after = int(round(T_AFTER / dt))
for k in range(n_after + 1):
    if k % int(round(10 / dt)) == 0:
        j = k // int(round(10 / dt))
        e_fed = fed_target[j] if j < len(fed_target) else None
        out_cut = bodies(np.where(disk, 0, a["e"]))["n"]
        out_fed = bodies(np.where(disk, 0, e_fed))["n"] if e_fed is not None else None
        cut_log.append(dict(t=round(T_CUT + k * dt), target_area_cut=float(((a["e"] > 0.5) & disk).sum() * dx * dx),
                            target_area_fed=float(((e_fed > 0.5) & disk).sum() * dx * dx) if e_fed is not None else None,
                            bodies_outside_cut=int(out_cut), bodies_outside_fed=out_fed, F_disk_cut=float(a["F"][disk].mean())))
    if k % int(round(200 / dt)) == 0:
        snaps[f"cut_t{int(round(T_CUT + k * dt))}"] = a["e"].astype(np.float32)
        j = k // int(round(10 / dt))
        if j < len(fed_target):
            snaps[f"fed_t{int(round(T_CUT + k * dt))}"] = fed_target[j].astype(np.float32)
    if k < n_after:
        a = m.step(a)
cpu_cut = time.process_time() - t1
died = next((r["t"] for r in cut_log if r["target_area_cut"] == 0.0), None)
res = dict(seed=seed, dt=dt, N=N, dx=dx, T_end=T_END, cpu_main_s=round(cpu_main, 1), cpu_cut_s=round(cpu_cut, 1),
           counts_columns=["t", "bodies", "body_area_wu2", "mean_F", "max_e"], counts=counts[::5] + [counts[-1]],
           births=[round(t["start"] * FRAME) for t in tracks if t["birth"] == "nucleation"],
           splits=[round(e["frame"] * FRAME) for e in splits], merges=[round(e["frame"] * FRAME) for e in merges],
           deaths=[round(t["end"] * FRAME) for t in tracks if t["end"] < len(comps) - 1 and not t["children"]],
           persistent_splits=[dict(t=round(e["frame"] * FRAME), parent=e["parent"], children=e["children"]) for e in lin["persistent_splits"]],
           max_generation=lin.get("max_generation"), lineage_keys=sorted(lin.keys()),
           rings=rings, layer_pass=f"{sum(r['passed'] for r in rings)}/{sum(r['bodies'] for r in rings)}",
           cut=dict(t_cut=T_CUT, target_idx=tgt, nearest_other_wu=nn[it], radius_wu=R, died_at=died,
                    log=cut_log[::5] + [cut_log[-1]]))
np.savez_compressed(os.path.join(HERE, "out", "cap", name + "_final.npz"), e=s["e"].astype(np.float32), s=s["s"].astype(np.float32),
                    cut_e=a["e"].astype(np.float32), cut_state_e=cut_state["e"].astype(np.float32), disk=disk, **snaps)
json.dump(res, open(os.path.join(HERE, "out", "cap", name + ".json"), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
print(json.dumps({k: res[k] for k in ("seed", "dt", "N", "cpu_main_s", "cpu_cut_s", "splits", "merges", "deaths", "max_generation", "layer_pass")}))
print("persistent", [p["t"] for p in res["persistent_splits"]], "cut died at", died, "R", round(R, 1), "outside cut/fed at end",
      cut_log[-1]["bodies_outside_cut"], cut_log[-1]["bodies_outside_fed"])
print("counts", [(c[0], c[1]) for c in counts[::25]])
