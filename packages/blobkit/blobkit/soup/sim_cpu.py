"""soup_sim_v2.py — S1 soup simulator with CHUNKED CONTINUATION (phase 6, v2).

Same locked protocol + numerics as soup_sim.py (verbatim op order: explicit
reaction w/ OLD u, noise, exact k-space diffusion; f32; scipy.fft). Differences:
1. init_soup()/advance()/snapshot_rec() state machine: a run can be extended
   chunk by chunk (adaptive horizon, M4) and is BITWISE-identical to a single
   long run at the same final T (same RNG stream, same op order; parity-gated).
2. Extra CREC record (M2): per-act ORGANISM patches at thr_lo
   (u0 + 0.30*(sqrt(lam)-u0)); v1 blob lists at thr_hi = segments. Includes
   periodic-safe span of the 3 largest organisms (M6 box-limit).
Chunk boundaries MUST be multiples of CREC=25tu (record grid alignment).
"""
import time
import numpy as np
import scipy.fft as sfft
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
from .. import genome as G                     # [blobkit edit E11]
from .sim_v1 import (blob_list_fast, seed_positions, dressed_poke, coarse,
                     REC, CREC, MEMTAU, N_SOUP, DMIN, DRESS, NOISE, BLOCK,
                     save_run, load_run)

THR_LO_FRAC = 0.30   # organism threshold fraction (segments use 0.45)


def _perio_span(idx, N):
    """Span (px) of a set of pixel indices along one periodic axis: N - maxgap."""
    u = np.unique(idx)
    if len(u) == N:
        return float(N)
    gaps = np.diff(u)
    wrap = u[0] + N - u[-1]
    return float(N - max(gaps.max(initial=0), wrap))


def org_patches(u, thr_lo, dx, L):
    """Organism-level patch stats at thr_lo: n, sizes, cover, top-3 spans (px)."""
    mask = u > thr_lo
    lab, k = G.periodic_label(mask)
    sizes = []
    if k:
        cnt = np.bincount(lab.ravel(), minlength=k + 1)[1:]
        sizes = (cnt * dx * dx).tolist()
    spans = []
    if k:
        order = np.argsort(cnt)[::-1][:3]
        for j in order:
            ys, xs = np.nonzero(lab == j + 1)
            spans.append(round(max(_perio_span(ys, u.shape[0]),
                                   _perio_span(xs, u.shape[1])) * dx, 2))
    return dict(n=int(k), sizes=[round(s, 2) for s in sizes],
                cover=float(mask.mean()), spans=spans)


def init_soup(g, L=128.0, seed=0, n_soup=N_SOUP, dtype="f32", kicks=None,
              noise=NOISE, workers=4):
    """Build the persistent sim state S. No steps taken yet (t=0 unrecorded)."""
    dx, dt = 0.5, 0.02
    na, nc = len(g["acts"]), len(g["chans"])
    N = int(round(L / dx))
    rng = np.random.default_rng(seed)
    kicks = kicks or {}

    F = G.state_vacuum(g, N)
    pts = seed_positions(rng, n_soup, L, DMIN)
    species = [i % na for i in range(n_soup)]
    rng.shuffle(species)
    for p, sp in zip(pts, species):
        kp = 0.5 if kicks is None else kicks.get(sp, 0.5)
        ang = rng.uniform(0, 2 * np.pi)
        F = dressed_poke(F, g, sp, p[0], p[1], dx, kick_px=kp,
                         kdir=(np.cos(ang), np.sin(ang)))

    W = np.asarray(g["W"], float); K = np.asarray(g["K"], float)
    bilin = [tuple(b) for b in g.get("bilin", [])]
    lam = np.array([a["lam"] for a in g["acts"]])[:, None, None]
    k1 = np.array([a["k1"] for a in g["acts"]])[:, None, None]
    u0s = np.array([a["u0"] for a in g["acts"]])
    tau_c = np.array([c["tau"] for c in g["chans"]])
    thr_a = np.array([a["u0"] + 0.45 * (np.sqrt(max(a["lam"], 1e-9)) - a["u0"])
                      for a in g["acts"]])
    thr_lo = np.array([a["u0"] + THR_LO_FRAC *
                       (np.sqrt(max(a["lam"], 1e-9)) - a["u0"])
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

    S = dict(g=g, L=L, dx=dx, dt=dt, na=na, nc=nc, N=N, rng=rng,
             F=F, E=E, lam=lam, k1=k1, u0f=u0f, Wf=Wf, Kf=Kf, Wid=Wid,
             bilin=bilin, tanh_rows=tanh_rows, inv_tau=inv_tau,
             thr_f=thr_ch.astype(fdt), sc_f=sc_ch.astype(fdt),
             thr_a=thr_a, thr_lo=thr_lo, tau_c=tau_c, memch=memch,
             fdt=fdt, nsig=fdt(noise * np.sqrt(dt)), noise=noise,
             workers=workers, seed=seed, dtype=dtype,
             rec=max(int(round(REC / dt)), 1),
             crec=max(int(round(CREC / dt)), 1),
             snap_t=[0.0, 250.0],
             t_step=0, recorded_at=-1,
             ts=[], blobs={i: [] for i in range(na)},
             mass={i: [] for i in range(na)},
             cts=[], patches={i: [] for i in range(na)},
             orgs={i: [] for i in range(na)},
             memf={c: [] for c in memch}, snaps={},
             status="ok", dead_since=None, wall_s=0.0,
             species_seeded=species, seed_pts=pts.tolist())
    return S


def _record(S, t):
    """Record step t (REC and/or CREC grids). Returns False on blowup/dead."""
    dt, dx, L, na = S["dt"], S["dx"], S["L"], S["na"]
    tt = t * dt
    F = S["F"]
    if t % S["rec"] == 0:
        if not np.isfinite(F[:na]).all():
            S["status"] = "blowup"
            return False
        ntot = 0
        for i in range(na):
            u = np.asarray(F[i], np.float64)
            bl = blob_list_fast(u, S["thr_a"][i], dx, L)
            S["blobs"][i].append([[b["y"], b["x"], b["area"], b["peak"]]
                                  for b in bl])
            S["mass"][i].append(float(np.clip(u - S["thr_a"][i], 0, None)
                                      .sum() * dx * dx))
            ntot += len(bl)
        S["ts"].append(tt)
        if ntot == 0:
            if S["dead_since"] is None:
                S["dead_since"] = tt
            if tt - S["dead_since"] > 200.0 and tt > 400.0:
                S["status"] = "all_dead"
                return False
        else:
            S["dead_since"] = None
    if t % S["crec"] == 0:
        S["cts"].append(tt)
        for i in range(na):
            u = np.asarray(F[i], np.float64)
            labm, k = G.periodic_label(u > S["thr_a"][i])
            sz = [float((labm == j).sum()) * dx * dx for j in range(1, k + 1)]
            S["patches"][i].append(dict(n=k, sizes=sz,
                                        cover=float((u > S["thr_a"][i]).mean())))
            S["orgs"][i].append(org_patches(u, S["thr_lo"][i], dx, L))
        for c in S["memch"]:
            S["memf"][c].append(coarse(np.asarray(F[na + c], np.float64)))
    while S["snap_t"] and tt >= S["snap_t"][0] - 1e-9:
        S["snaps"][S["snap_t"].pop(0)] = np.asarray(F[:na], np.float64).copy()
    return True


def advance(S, T_target):
    """Integrate until t = T_target (tu). Chunk-safe: records exactly once per
    grid point; resuming records nothing twice. Returns S["status"]."""
    t0w = time.time()
    dt = S["dt"]
    steps_target = int(round(T_target / dt))
    if steps_target % S["crec"] != 0:
        raise ValueError("T_target must be a multiple of CREC")
    na, N = S["na"], S["N"]
    fdt, rng, workers = S["fdt"], S["rng"], S["workers"]
    F, E = S["F"], S["E"]
    lam, k1, u0f = S["lam"], S["k1"], S["u0f"]
    Wf, Kf, Wid = S["Wf"], S["Kf"], S["Wid"]
    thr_f, sc_f, inv_tau = S["thr_f"], S["sc_f"], S["inv_tau"]
    bilin, tanh_rows = S["bilin"], S["tanh_rows"]
    nsig, noise = S["nsig"], S["noise"]

    t = S["t_step"]
    while S["status"] == "ok" and t <= steps_target:
        if S["recorded_at"] < t:
            ok = _record(S, t)
            S["recorded_at"] = t
            if not ok:
                break
        if t == steps_target:
            break
        # ---- one step (verbatim soup_sim op order)
        U = F[:na]; X = F[na:]
        Z = U - u0f
        R = np.empty_like(F)
        np.multiply(U, U, out=R[:na]); R[:na] *= -U
        R[:na] += lam * U; R[:na] += k1
        R[:na] -= np.tensordot(Kf, X, axes=(1, 0))
        for (i, c, c2, coef) in bilin:
            R[i] -= fdt(coef) * X[c] * X[c2]
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
        F = F + fdt(S["dt"]) * R
        if noise > 0:
            F[:na] += nsig * rng.standard_normal((na, N, N), dtype=fdt) \
                if fdt == np.float32 else \
                nsig * rng.standard_normal((na, N, N))
        F = sfft.irfft2(sfft.rfft2(F, workers=workers) * E, s=(N, N),
                        workers=workers)
        t += 1
        S["F"] = F
    S["t_step"] = t
    S["wall_s"] += time.time() - t0w
    return S["status"]


def snapshot_rec(S):
    """Build a metrics-compatible record dict from current state (cheap views;
    do NOT mutate returned lists). Adds v2 keys: orgs, thr_lo."""
    na = S["na"]
    return dict(world=S["g"].get("id"), seed=S["seed"], L=S["L"],
                T=S["t_step"] * S["dt"], dtype=S["dtype"],
                status=S["status"], wall_s=round(S["wall_s"], 1),
                na=na, nc=S["nc"], memch=S["memch"],
                thr=S["thr_a"].tolist(), thr_lo=S["thr_lo"].tolist(),
                taus=S["tau_c"].tolist(),
                t=np.array(S["ts"]), blobs=S["blobs"], mass=S["mass"],
                ct=np.array(S["cts"]), patches=S["patches"],
                orgs=S["orgs"],
                memf={c: np.array(v) for c, v in S["memf"].items()},
                snaps=S["snaps"], species_seeded=S["species_seeded"],
                seed_pts=S["seed_pts"])
