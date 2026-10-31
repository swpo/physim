"""Division axes of c40's CIPS cells under a rotated initial field and an isotropic drift stencil.

usage: rotdiv.py SEED THETA_DEG ISO N T_END NAME
  World: c40 cips-layered-divide (world.py defaults: dt 0.1, Lsc 3 at N=192; box 192 world units), no dynamics noise.
  ISO=1 loads world_iso.py (the same world with the 9-point isotropic combination of its drift face fluxes).
  THETA=0 and N=192: the world's own init(SEED). Otherwise the initial enzyme field is built from the SAME white
  draws as init(SEED) (rng(SEED).standard_normal((192,192)), one weight per native pixel), with the infinite
  periodic tiling of those points rotated by THETA about the box centre, the points that land in the box kept, and
  the periodic Gaussian (rf_len 16 world units) taken exactly in Fourier space and normalised as init does. This is
  a stationary random field with init's covariance; away from the box edges it is init's field rotated by THETA.
  p, F, s are then set as init sets them (p at its local steady state, F uniform, s = 0).
  Frames every 10 t: labkit segment(e > 0.5, min area 6 wu^2, 4-connected periodic), overlaps, and per component
  the periodic second moments (long-axis angle, aspect). End: labkit track + lineage_stats (K = 40 frames = 400 t).
  Division axis at each persistent split: angle of the min-image vector joining the two (largest surviving)
  daughter centroids, at the split frame and 50 / 100 t later; plus the parent's long axis 10 t and 100 t before.
  Every 250 t: capab.py's layer test and elongated-body long axes (the convergence study's measure).
"""
import os
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[v] = "1"
import json, sys, time
import numpy as np
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/swpo/residency-environments/environments/physim")
from physim import labworld as LW  # noqa: E402
LAB = "/home/user/physim/research/alife"
WORLD = f"{LAB}/collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py"
sys.path.insert(0, LAB)
from labkit import metrics as M  # noqa: E402

L_BOX, N0 = 192, 192
FRAME, RING_EVERY, KF, SNAP_EVERY = 10.0, 250.0, 40, 250.0


def wrap(d, L):
    return (d + L / 2) % L - L / 2


def rotated_xi(seed, theta_deg, N, rf_len=16.0, mmax=14):
    """Periodic Gaussian-smoothed white field from init's draws, the draws' periodic tiling rotated by theta."""
    rng = np.random.default_rng(seed)
    W = rng.standard_normal((N0, N0))
    ii, jj = np.mgrid[0:N0, 0:N0].astype(float)
    th = np.radians(theta_deg)
    c = L_BOX / 2
    Ys, Xs, Ws = [], [], []
    tiles = (0,) if theta_deg == 0 else (-1, 0, 1)
    for a in tiles:
        for b in tiles:
            y, x = ii + a * L_BOX - c, jj + b * L_BOX - c
            xr = c + np.cos(th) * x - np.sin(th) * y
            yr = c + np.sin(th) * x + np.cos(th) * y
            k = (xr >= 0) & (xr < L_BOX) & (yr >= 0) & (yr < L_BOX)
            Ys.append(yr[k]); Xs.append(xr[k]); Ws.append(W[k])
    Y, X, Wt = np.concatenate(Ys), np.concatenate(Xs), np.concatenate(Ws)
    m = np.arange(-mmax, mmax + 1)
    k1 = 2 * np.pi * m / L_BOX
    Ey = np.exp(-1j * np.outer(k1, Y))          # (2M+1, P)
    Ex = np.exp(-1j * np.outer(k1, X))
    C = (Ey * Wt) @ Ex.T                        # C[m, n] = sum_j w_j exp(-i (ky Y_j + kx X_j))
    C *= np.exp(-0.5 * rf_len ** 2 * (k1[:, None] ** 2 + k1[None, :] ** 2))
    full = np.zeros((N, N), complex)
    full[np.ix_(m % N, m % N)] = C
    g = np.fft.ifft2(full).real                 # sampled at grid points i * dx (dx = L_BOX / N)
    return (g - g.mean()) / g.std(), len(Wt)


def comp_moments(lab, n, N):
    """Per component (labels 1..n): periodic long-axis angle (deg, from x axis, y = row index) and aspect."""
    if n == 0:
        return np.zeros(0), np.zeros(0)
    yy, xx = np.indices(lab.shape)
    m = lab > 0
    l = lab[m] - 1
    w = np.ones(l.size)
    # circular centroid per label, unweighted (shape of the mask)
    out = []
    for coord in (yy[m], xx[m]):
        ang = 2 * np.pi * coord / N
        cs = np.bincount(l, np.cos(ang), n); sn = np.bincount(l, np.sin(ang), n)
        out.append((np.arctan2(sn, cs) % (2 * np.pi)) * N / (2 * np.pi))
    cy, cx = out
    dy, dx = wrap(yy[m] - cy[l], N), wrap(xx[m] - cx[l], N)
    cnt = np.bincount(l, w, n)
    syy = np.bincount(l, dy * dy, n) / cnt - (np.bincount(l, dy, n) / cnt) ** 2
    sxx = np.bincount(l, dx * dx, n) / cnt - (np.bincount(l, dx, n) / cnt) ** 2
    sxy = np.bincount(l, dx * dy, n) / cnt - (np.bincount(l, dx, n) / cnt) * (np.bincount(l, dy, n) / cnt)
    tr, det = sxx + syy, sxx * syy - sxy ** 2
    lam1 = tr / 2 + np.sqrt(np.maximum(tr ** 2 / 4 - det, 0)); lam2 = np.maximum(tr - lam1, 1e-12)
    ang = 0.5 * np.degrees(np.arctan2(2 * sxy, sxx - syy)) % 180    # long-axis angle
    return ang, np.sqrt(lam1 / lam2)


def ring_measure(e, sv, dx, N):
    """capab.py's layer test (signed distance to the e = 0.5 contour, world units) plus elongated long axes."""
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
        ang = float(np.degrees(np.arctan2(evec[0, 1], evec[1, 1])) % 180)
        res.append((float(S[rim].mean() / S[core].mean()), float(S[rim].mean() / S[outs].mean()), float(b.sum() * dx * dx), aspect, ang))
    return res


def main():
    seed, theta, iso, N, T_END, name = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]), sys.argv[6]
    dx = L_BOX / N
    over = {} if N == L_BOX else {"Lsc": 3.0 * N / L_BOX, "rf_len": 16.0 * N / L_BOX}
    w = LW.LabWorld(path=os.path.join(HERE, "world_iso.py") if iso else WORLD, fields=("e", "p", "F", "s"),
                    steps_per_tick=1, native_dt=0.1, overrides=over, dx=dx, sys_path=(LAB,))
    m = w.load()
    m.ops.WORKERS = 1
    if iso:
        assert m._w.vf_flux_div is m.vf_flux_div_iso and m._w.up_flux_div is m.up_flux_div_iso
    else:
        assert m.vf_flux_div.__name__ == "vf_flux_div"
    s = m.init(seed, (N, N))
    q = s["par"]; dt = q["dt"]
    info = {}
    xi_native = None
    if theta != 0 or N != L_BOX:
        xi, npts = rotated_xi(seed, theta, N)
        e = np.clip(q["e0"] + q["noise"] * xi, 0.0, 1.0)
        s["e"] = e
        s["p"] = m._ss_p(e, s["F"], q["kc"], q["ks"])
        info.update(n_points=int(npts))
    # construction check at theta 0 against init's own field (native grid)
    if N == L_BOX:
        x0, _ = rotated_xi(seed, 0.0, N)
        e_init = m.init(seed, (N, N))["e"]
        xi_native = (e_init - q["e0"]) / q["noise"]
        info["theta0_construction_vs_init_corr"] = float(np.corrcoef(x0.ravel(), xi_native.ravel())[0, 1])
        info["theta0_construction_vs_init_maxabs"] = float(np.abs(x0 - xi_native).max())
        if theta != 0:
            # rotation fidelity: compare with init's field evaluated at rotated coordinates (Fourier interpolation)
            Xf = np.fft.fft2(xi_native)
            k1 = 2 * np.pi * np.fft.fftfreq(N, d=dx)
            th = np.radians(-theta)
            yy, xx = np.mgrid[0:N, 0:N] * dx
            c = L_BOX / 2
            xs = c + np.cos(th) * (xx - c) - np.sin(th) * (yy - c)
            ys = c + np.sin(th) * (xx - c) + np.cos(th) * (yy - c)
            sel = np.abs(k1) <= 2 * np.pi * 14 / L_BOX
            kk = k1[sel]; Xs = Xf[np.ix_(sel, sel)] / N ** 2
            ey = np.exp(1j * ys.ravel()[:, None] * kk[None, :]); ex = np.exp(1j * xs.ravel()[:, None] * kk[None, :])
            frot = np.real(np.einsum("pm,mn,pn->p", ey, Xs, ex)).reshape(N, N)
            xi_now = (s["e"] - q["e0"]) / q["noise"]
            dist_edge = np.minimum.reduce([yy, xx, L_BOX - yy, L_BOX - xx])
            for d in (0, 24, 48):
                k = dist_edge >= d
                info[f"rotated_vs_init_rotated_corr_edge>={d}"] = float(np.corrcoef(xi_now[k], frot[k])[0, 1])
            info["frac_box_absdiff<0.25sd"] = float(np.mean(np.abs(xi_now - frot) < 0.25))
    MIN_AREA = int(np.ceil(6 / dx ** 2))
    t0 = time.process_time()
    comps, links, prev, mom = [], [None], None, []
    rings, counts, snaps = [], [], {}
    nsteps = int(round(T_END / dt))
    fr, re_, sn = int(round(FRAME / dt)), int(round(RING_EVERY / dt)), int(round(SNAP_EVERY / dt))
    for k in range(nsteps + 1):
        if k % fr == 0:
            seg = M.segment(s["e"], 0.5, MIN_AREA, True)
            comps.append(dict(area=seg["area"], cy=seg["cy"], cx=seg["cx"], n=seg["n"]))
            if prev is not None:
                links.append(M.overlaps(prev["lab"], prev["n"], seg["lab"], seg["n"]))
            prev = seg
            mom.append(comp_moments(seg["lab"], seg["n"], N))
            counts.append((round(k * dt, 3), int(seg["n"]), float(seg["area"].sum() * dx * dx), float(s["e"].max())))
        if k % re_ == 0 and k > 0:
            r = ring_measure(s["e"], s["s"], dx, N)
            rings.append(dict(t=round(k * dt), bodies=len(r), passed=sum(1 for x in r if x[0] >= 1.5 and x[1] >= 1.5),
                              rim_out_median=float(np.median([x[1] for x in r])) if r else None,
                              elongated_axes=[(round(x[3], 2), round(x[4], 1)) for x in r if x[3] >= 1.5]))
        if k % sn == 0:
            snaps[f"e_t{int(round(k * dt))}"] = s["e"].astype(np.float16)
        if k < nsteps:
            s = m.step(s)
    cpu = time.process_time() - t0
    tracks, events = M.track(comps, links, (N, N), True)
    lin = M.lineage_stats(tracks, events, len(comps), FRAME, (N, N), True, K=KF)

    def vec_angle(a, b):
        vy, vx = wrap(b[0] - a[0], N) * dx, wrap(b[1] - a[1], N) * dx
        return float(np.degrees(np.arctan2(vy, vx)) % 180), float(np.hypot(vy, vx))

    divs = []
    for ev in lin["persistent_splits"]:
        f = ev["frame"]
        ch = sorted(ev["surviving_children"], key=lambda c: -tracks[c]["area"][0])[:2]
        rec = dict(t=round(f * FRAME), parent=ev["parent"], children=ch, n_children=len(ev["children"]))
        for lag in (0, 5, 10):
            if all(tracks[c]["end"] >= f + lag for c in ch):
                a = (tracks[ch[0]]["cy"][lag], tracks[ch[0]]["cx"][lag]); b = (tracks[ch[1]]["cy"][lag], tracks[ch[1]]["cx"][lag])
                rec[f"daughter_axis_{int(lag * FRAME)}t"], rec[f"daughter_sep_{int(lag * FRAME)}t"] = vec_angle(a, b)
        P = tracks[ev["parent"]]
        for back in (1, 10):
            j = len(P["comp"]) - back
            if j >= 0:
                fi = P["start"] + j
                ci = P["comp"][j]
                rec[f"parent_long_axis_{int(back * FRAME)}t_before"] = round(float(mom[fi][0][ci]), 1)
                rec[f"parent_aspect_{int(back * FRAME)}t_before"] = round(float(mom[fi][1][ci]), 2)
        rec["parent_centroid"] = (round(float(P["cy"][-1]) * dx, 1), round(float(P["cx"][-1]) * dx, 1))
        divs.append(rec)
    all_splits = []
    for ev in events:
        if ev["type"] == "split" and len(ev["children"]) >= 2:
            ch = sorted(ev["children"], key=lambda c: -tracks[c]["area"][0])[:2]
            a = (tracks[ch[0]]["cy"][0], tracks[ch[0]]["cx"][0]); b = (tracks[ch[1]]["cy"][0], tracks[ch[1]]["cx"][0])
            all_splits.append((round(ev["frame"] * FRAME), *vec_angle(a, b)))
    res = dict(seed=seed, theta=theta, iso=iso, N=N, dx=dx, dt=dt, T_end=T_END, cpu_s=round(cpu, 1), info=info,
               births=[round(t["start"] * FRAME) for t in tracks if t["birth"] == "nucleation"],
               nucleation_sites=[(round(t["start"] * FRAME), round(float(t["cy"][0]) * dx, 1), round(float(t["cx"][0]) * dx, 1))
                                 for t in tracks if t["birth"] in ("nucleation", "initial") and t["start"] * FRAME <= 2000],
               n_splits=sum(1 for e in events if e["type"] == "split"), n_merges=sum(1 for e in events if e["type"] == "merge"),
               persistent_divisions=divs, all_splits=all_splits, max_generation=lin.get("max_generation"),
               counts_columns=["t", "bodies", "body_area_wu2", "max_e"], counts=counts[::10] + [counts[-1]],
               rings=rings, layer_pass=f"{sum(r['passed'] for r in rings)}/{sum(r['bodies'] for r in rings)}")
    np.savez_compressed(os.path.join(HERE, "out", name + "_snaps.npz"), s_final=s["s"].astype(np.float16), **snaps)
    np.savez_compressed(os.path.join(HERE, "out", name + "_state_end.npz"), **{f: s[f] for f in ("e", "p", "F", "s")}, t=s["t"])
    json.dump(res, open(os.path.join(HERE, "out", name + ".json"), "w"), indent=1,
              default=lambda o: o.tolist() if hasattr(o, "tolist") else (int(o) if isinstance(o, np.integer) else str(o)))
    print(json.dumps(dict(name=name, cpu_s=res["cpu_s"], info=info, births=res["births"], n_div=len(divs),
                          div_axes=[d.get("daughter_axis_0t") for d in divs], layer=res["layer_pass"])))


if __name__ == "__main__":
    main()
