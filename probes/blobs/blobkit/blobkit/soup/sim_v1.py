"""soup_sim.py — S1 soup assay simulator (complexity battery, phase 5).

Protocol (LOCKED after smoke):
  L=128 dx=0.5 dt=0.02 T=5000tu, periodic. N_SOUP=12 dressed pokes (dress=0.6,
  amp=2 sig=3 — the locked a1_panel revival convention), positions random with
  min separation 16px, species round-robin over activators. Working noise 2e-3
  on activators (machinev3 hold-noise). Acts listed in world KICKS get a
  kicked+dressed launch (their certified convention), kick direction random.
  Records every REC=5tu: per-act blob lists (periodic labeling, thr_frac=0.45)
  + thresholded biomass. Every CREC=25tu: per-act patch stats + coarse (8px
  block-mean) fields of memory channels (tau>=MEMTAU=30). Full snaps at
  0, 250, T/2, T for strips. Early exit only on blowup or all-dead>200tu.

Numerics: genome.py conventions verbatim (explicit reaction with OLD u in
channel drives, exact diffusion in k-space). FFT backend scipy.fft workers=4;
dtype float32 by default — GATED by a descriptor-parity run vs float64
(see VALIDATION.md, gate PAR-F32). Injected noise 2e-3 >> f32 roundoff.
"""
import os, sys, time
import numpy as np
import scipy.fft as sfft

HERE = os.path.dirname(os.path.abspath(__file__))
from .. import genome as G                     # [blobkit edit E10]

REC, CREC = 5.0, 25.0


def blob_list_fast(u, thr, dx, L):
    """Vectorized blob_list (bincount-based): same output as G.blob_list.
    O(N^2 + n_blob) instead of O(n_blob * N^2)."""
    from scipy import ndimage as ndi
    mask = u > thr
    lab, n = G.periodic_label(mask)
    if n == 0:
        return []
    N = u.shape[0]
    flat = lab.ravel()
    w = np.where(mask, np.clip(u - thr, 0.0, None), 0.0).ravel()
    tot = np.bincount(flat, weights=w, minlength=n + 1)[1:]
    ang_y = 2 * np.pi * (np.arange(N) + 0.5) / N
    ang_x = 2 * np.pi * (np.arange(N) + 0.5) / N
    PY = np.broadcast_to(ang_y[:, None], u.shape).ravel()
    PX = np.broadcast_to(ang_x[None, :], u.shape).ravel()
    zy = (np.bincount(flat, weights=w * np.cos(PY), minlength=n + 1)[1:]
          + 1j * np.bincount(flat, weights=w * np.sin(PY), minlength=n + 1)[1:])
    zx = (np.bincount(flat, weights=w * np.cos(PX), minlength=n + 1)[1:]
          + 1j * np.bincount(flat, weights=w * np.sin(PX), minlength=n + 1)[1:])
    area = np.bincount(flat, minlength=n + 1)[1:] * dx * dx
    peak = ndi.maximum(u, lab, index=np.arange(1, n + 1))
    out = []
    for j in range(n):
        if tot[j] <= 0:
            continue
        y = (np.angle(zy[j] / tot[j]) % (2 * np.pi)) / (2 * np.pi) * N * dx
        x = (np.angle(zx[j] / tot[j]) % (2 * np.pi)) / (2 * np.pi) * N * dx
        out.append(dict(y=float(y), x=float(x), area=float(area[j]),
                        peak=float(np.atleast_1d(peak)[j])))
    return out
MEMTAU = 30.0
N_SOUP, DMIN, DRESS = 12, 16.0, 0.6
NOISE = 2e-3
BLOCK = 8  # coarse block px


def seed_positions(rng, n, L, dmin):
    pts = []
    for _ in range(20000):
        p = rng.uniform(0, L, 2)
        if all(np.hypot(*G.min_image(p - q, L)) >= dmin for q in pts):
            pts.append(p)
            if len(pts) == n:
                break
    return np.array(pts)


def dressed_poke(F, g, act, x, y, dx, kick_px=0.0, kdir=(1.0, 0.0)):
    """u-bump + dress*W[c,act] channel shadows (id chans). kick_px>0: shadows
    displaced -kick_px*kdir (M1 kick convention -> blob travels +kdir)."""
    N = F.shape[1]; L = N * dx
    na = len(g["acts"])
    W = np.asarray(g["W"], float)
    F = G.poke(F, g, act, x, y, 2.0, 3.0, dx)
    c = (np.arange(N) + 0.5) * dx
    sx, sy = x - kick_px * kdir[0], y - kick_px * kdir[1]
    dyy = G.min_image(c - sy, L)[:, None]
    dxx = G.min_image(c - sx, L)[None, :]
    bump = 2.0 * np.exp(-(dyy ** 2 + dxx ** 2) / (2 * 3.0 ** 2))
    for ci, ch in enumerate(g["chans"]):
        if ch["g"] == "id" and W[ci, act] != 0.0:
            F[na + ci] += DRESS * W[ci, act] * bump
    return F


def coarse(a, block=BLOCK):
    n = a.shape[0] // block
    return a[:n * block, :n * block].reshape(n, block, n, block).mean(axis=(1, 3))


def run_soup(g, L=128.0, T=5000.0, seed=0, n_soup=N_SOUP, dtype="f32",
             kicks=None, noise=NOISE, workers=4):
    """Returns record dict (json/npz-safe)."""
    t0w = time.time()
    dx, dt = 0.5, 0.02
    na, nc = len(g["acts"]), len(g["chans"])
    N = int(round(L / dx))
    rng = np.random.default_rng(seed)
    kicks = kicks or {}

    # ---- seed soup
    F = G.state_vacuum(g, N)
    pts = seed_positions(rng, n_soup, L, DMIN)
    species = [i % na for i in range(n_soup)]
    rng.shuffle(species)
    # LOCKED: every blob dressed + kicked 0.5px in a random direction
    # (uniform protocol; avoids the unstable-symmetric-branch trap, BF5 lesson)
    for p, sp in zip(pts, species):
        kp = 0.5 if kicks is None else kicks.get(sp, 0.5)
        ang = rng.uniform(0, 2 * np.pi)
        F = dressed_poke(F, g, sp, p[0], p[1], dx, kick_px=kp,
                         kdir=(np.cos(ang), np.sin(ang)))

    # ---- precompute
    W = np.asarray(g["W"], float); K = np.asarray(g["K"], float)
    bilin = [tuple(b) for b in g.get("bilin", [])]
    lam = np.array([a["lam"] for a in g["acts"]])[:, None, None]
    k1 = np.array([a["k1"] for a in g["acts"]])[:, None, None]
    u0s = np.array([a["u0"] for a in g["acts"]])
    tau_c = np.array([c["tau"] for c in g["chans"]])
    thr_a = np.array([a["u0"] + 0.45 * (np.sqrt(max(a["lam"], 1e-9)) - a["u0"])
                      for a in g["acts"]])
    kf = 2 * np.pi * np.fft.fftfreq(N, d=dx)
    kr = 2 * np.pi * np.fft.rfftfreq(N, d=dx)
    k2 = kf[:, None] ** 2 + kr[None, :] ** 2
    Ds = np.array([a["Du"] for a in g["acts"]] + [c["D"] for c in g["chans"]])
    E = np.exp(-Ds[:, None, None] * k2[None] * dt)
    id_mask = np.array([c["g"] == "id" for c in g["chans"]])
    thr_ch = np.array([c.get("thr", 0.0) for c in g["chans"]])
    sc_ch = np.array([c.get("sc", 1.0) for c in g["chans"]])
    memch = [c for c in range(nc) if tau_c[c] >= MEMTAU]

    fdt = np.float32 if dtype == "f32" else np.float64
    F = F.astype(fdt); E = E.astype(fdt)
    lam = lam.astype(fdt); k1 = k1.astype(fdt)
    Wf = W.astype(fdt); Kf = K.astype(fdt)
    u0f = u0s[:, None, None].astype(fdt)
    Wid = Wf.copy(); Wid[~id_mask] = 0.0
    tanh_rows = [c for c in range(nc) if not id_mask[c]]
    inv_tau = (1.0 / tau_c)[:, None, None].astype(fdt)
    thr_f = thr_ch.astype(fdt); sc_f = sc_ch.astype(fdt)
    sq = np.sqrt(dt)
    nsig = fdt(noise * sq)

    steps = int(round(T / dt))
    rec = max(int(round(REC / dt)), 1)
    crec = max(int(round(CREC / dt)), 1)
    snap_t = sorted({0.0, 250.0, T / 2, float(T)})

    ts, blobs, mass = [], {i: [] for i in range(na)}, {i: [] for i in range(na)}
    cts, patches = [], {i: [] for i in range(na)}
    memf = {c: [] for c in memch}
    snaps = {}
    status, dead_since = "ok", None

    for t in range(steps + 1):
        tt = t * dt
        if t % rec == 0 or t == steps:
            if not np.isfinite(F[:na]).all():
                status = "blowup"; break
            ntot = 0
            for i in range(na):
                u = np.asarray(F[i], np.float64)
                bl = blob_list_fast(u, thr_a[i], dx, L)
                blobs[i].append([[b["y"], b["x"], b["area"], b["peak"]]
                                 for b in bl])
                mass[i].append(float(np.clip(u - thr_a[i], 0, None).sum()
                                     * dx * dx))
                ntot += len(bl)
            ts.append(tt)
            if ntot == 0:
                dead_since = dead_since if dead_since is not None else tt
                if tt - dead_since > 200.0 and tt > 400.0:
                    status = "all_dead"; break
            else:
                dead_since = None
        if t % crec == 0 or t == steps:
            cts.append(tt)
            for i in range(na):
                u = np.asarray(F[i], np.float64)
                labm, k = G.periodic_label(u > thr_a[i])
                sz = [float((labm == j).sum()) * dx * dx for j in range(1, k + 1)]
                patches[i].append(dict(n=k, sizes=sz,
                                       cover=float((u > thr_a[i]).mean())))
            for c in memch:
                memf[c].append(coarse(np.asarray(F[na + c], np.float64)))
        while snap_t and tt >= snap_t[0] - 1e-9:
            snaps[snap_t.pop(0)] = np.asarray(F[:na], np.float64).copy()
        if t == steps or status != "ok":
            break
        U = F[:na]; X = F[na:]
        Z = U - u0f
        R = np.empty_like(F)
        # activators: R_u = lam*u - u^3 + k1 - K@X (- bilin)
        np.multiply(U, U, out=R[:na]); R[:na] *= -U
        R[:na] += lam * U; R[:na] += k1
        R[:na] -= np.tensordot(Kf, X, axes=(1, 0))
        for (i, c, c2, coef) in bilin:
            R[i] -= fdt(coef) * X[c] * X[c2]
        # channels: id-rows batched; tanh rows individually
        Rch = np.tensordot(Wid, Z, axes=(1, 0))
        for c in tanh_rows:
            acc = None
            for a in range(na):
                if Wf[c, a] != 0.0:
                    v = np.tanh(np.clip(Z[a] - thr_f[c], 0, None) / sc_f[c])
                    v *= Wf[c, a]
                    acc = v if acc is None else acc + v
            if acc is not None:
                Rch[c] = acc
        Rch -= X; Rch *= inv_tau
        R[na:] = Rch
        F = F + fdt(dt) * R
        if noise > 0:
            F[:na] += nsig * rng.standard_normal((na, N, N), dtype=fdt) \
                if fdt == np.float32 else \
                nsig * rng.standard_normal((na, N, N))
        F = sfft.irfft2(sfft.rfft2(F, workers=workers) * E, s=(N, N),
                        workers=workers)

    return dict(world=g.get("id"), seed=seed, L=L, T=T, dtype=dtype,
                status=status, wall_s=round(time.time() - t0w, 1),
                na=na, nc=nc, memch=memch, thr=thr_a.tolist(),
                taus=tau_c.tolist(),
                t=np.array(ts), blobs=blobs, mass=mass,
                ct=np.array(cts), patches=patches,
                memf={c: np.array(v) for c, v in memf.items()},
                snaps=snaps, species_seeded=species,
                seed_pts=pts.tolist())


def save_run(r, path):
    """npz with pickled blob/patch lists."""
    np.savez_compressed(path, run=np.array([r], dtype=object))


def load_run(path):
    return np.load(path, allow_pickle=True)["run"][0]
