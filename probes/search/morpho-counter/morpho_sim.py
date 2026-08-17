
"""morpho_sim v2 -- Schnakenberg ring + slow wavelength-control field C.

Micro physics (all local, no scripted macro events):
  u_t = Du lap(u) + T(C)*(a - u + u^2 v) + noise
  v_t = Dv lap(v) + T(C)*(b - u^2 v)
  T(C) = C^(2*sigma)  => intrinsic Turing wavenumber k_c(C) = k_c(1)*C^sigma
Slow control field C:
  mode 'auto':  C_t = Dc lap(C) + eps * gate * (kstar2 - S)/kstar2   [autonomous]
  mode 'ramp':  C_t = Dc lap(C) + (Cset(t) - C)/tau_c               [instrument]
S = local mean-square wavenumber of the BAND-PASSED pattern field:
  w  = u - wide_smooth(u)          (remove DC)
  wf = narrow_smooth(w)            (kill harmonics >= 2k)
  S  = smooth(|grad wf|^2) / smooth(wf^2)   ~= k_local^2
gate = wf2s/(wf2s+gate2): no pattern -> no drive (C frozen until morphogenesis).
On a ring of length L the pattern wavenumber is quantized (k_n = 2 pi n / L);
if kstar lies between allowed modes, C hunts forever -> integer limit cycle.

Numerics: IMEX -- diffusion exact in Fourier space (periodic), reaction Euler.
1 tick = 1 IMEX step of dt.
"""
import numpy as np
from scipy.ndimage import uniform_filter


def steady_state(a, b):
    u = a + b
    v = b / u ** 2
    return u, v


def jacobian(a, b):
    u, v = steady_state(a, b)
    fu = -1.0 + 2.0 * u * v
    fv = u * u
    gu = -2.0 * u * v
    gv = -u * u
    return fu, fv, gu, gv


def turing_info(a, b, Du, Dv, T=1.0):
    fu, fv, gu, gv = jacobian(a, b)
    fu, fv, gu, gv = T * fu, T * fv, T * gu, T * gv
    k2 = np.linspace(0, 4.0, 4001)
    tr = (fu + gv) - (Du + Dv) * k2
    det = (fu - Du * k2) * (gv - Dv * k2) - fv * gu
    disc = tr * tr - 4 * det
    lam = np.where(disc >= 0, 0.5 * (tr + np.sqrt(np.maximum(disc, 0))), 0.5 * tr)
    i = int(np.argmax(lam))
    band = k2[lam > 0]
    return {"growth": float(lam[i]), "k_max": float(np.sqrt(k2[i])),
            "k_lo": float(np.sqrt(band[0])) if len(band) else None,
            "k_hi": float(np.sqrt(band[-1])) if len(band) else None,
            "hom_stable": bool((fu + gv) < 0 and (fu * gv - fv * gu) > 0)}


def make_ops(ny, nx, dx, dt, Du, Dv, Dc):
    ky = 2 * np.pi * np.fft.fftfreq(ny, d=dx)
    kx = 2 * np.pi * np.fft.rfftfreq(nx, d=dx)
    k2 = ky[:, None] ** 2 + kx[None, :] ** 2
    return (np.exp(-Du * k2 * dt), np.exp(-Dv * k2 * dt), np.exp(-Dc * k2 * dt))


def diffuse(f, E, ny, nx):
    return np.fft.irfft2(np.fft.rfft2(f) * E, s=(ny, nx))


def count_mode(prof, kmax_idx=None):
    """Integer stripe count on the ring = dominant FFT mode of y-mean profile."""
    p = prof - prof.mean()
    ph = np.abs(np.fft.rfft(p))
    ph[0] = 0.0
    hi = kmax_idx or len(ph) - 1
    ph = ph[: hi + 1]
    if len(ph) < 4:
        return 0, 1.0
    n = int(np.argmax(ph[1:])) + 1
    rest = ph.copy(); lo = max(1, n - 1); rest[lo:n + 2] = 0.0
    purity = float(rest.max() / max(ph[n], 1e-12))
    return n, purity


def count_zc(prof, smooth_w=3):
    """Robust integer count: mean-upcrossings of smoothed periodic profile."""
    p = np.asarray(prof, float)
    if smooth_w > 1:
        k = np.ones(smooth_w) / smooth_w
        ext = np.concatenate([p[-smooth_w:], p, p[:smooth_w]])
        p = np.convolve(ext, k, "same")[smooth_w:-smooth_w]
    p = p - p.mean()
    s = np.sign(p)
    s[s == 0] = 1
    return int(((s < 0) & (np.roll(s, -1) > 0)).sum())


def simulate(p):
    rng = np.random.default_rng(p.get("seed", 0))
    ny, nx, dx, dt = p["ny"], p["nx"], p.get("dx", 1.0), p["dt"]
    a, b, Du, Dv, Dc = p["a"], p["b"], p["Du"], p["Dv"], p["Dc"]
    sigma, eps, kstar2 = p["sigma"], p.get("eps", 0.0), p.get("kstar2", 1.0)
    steps, meas_every = p["steps"], p.get("meas_every", 25)
    noise = p.get("noise_amp", 2e-3)
    Cmin, Cmax = p.get("Cmin", 0.4), p.get("Cmax", 1.9)
    mode = p.get("mode", "auto")
    t_on = p.get("t_on", 200.0)            # drive enabled after settle
    lam0 = 2 * np.pi / max(p.get("k_ref", 0.6), 1e-6)
    w_wide = max(5, int(round(2.2 * lam0)) | 1)   # DC removal window
    w_bp = max(3, int(round(0.5 * lam0)) | 1)     # harmonic-kill window
    w_S = max(3, int(round(1.0 * lam0)) | 1)      # S averaging window
    gate2 = p.get("gate2", 1e-3)

    u0, v0 = steady_state(a, b)
    u = u0 + 0.05 * rng.standard_normal((ny, nx))
    v = v0 + 0.01 * rng.standard_normal((ny, nx))
    if p.get("seed_mode"):  # init ON branch n: seeded cosine ring mode
        xg = np.arange(nx) * dx
        u += 0.25 * np.cos(2 * np.pi * p["seed_mode"] * xg / (nx * dx))[None, :]
    C = np.full((ny, nx), float(p.get("C0", 1.0)))
    Eu, Ev, Ec = make_ops(ny, nx, dx, dt, Du, Dv, Dc)

    snap_at = set(p.get("snap_at", []))
    snaps = {}
    keys = ["t", "n", "nz", "purity", "amp", "Cm", "Csd", "Sm", "drive", "envmin"]
    nm = steps // meas_every
    rec = {k: np.zeros(nm) for k in keys}
    modes = np.zeros((nm, min(17, nx // 2)))
    kymo = np.zeros((nm, nx)) if p.get("kymo") else None
    tr_win = p.get("trace_win")  # (s_lo, s_hi) in ticks: per-tick pixel trace
    if tr_win:
        tr_lo, tr_hi = int(tr_win[0]), int(tr_win[1])
        trace = np.zeros(tr_hi - tr_lo)
    else:
        trace, tr_lo, tr_hi = None, 0, 0
    ramp = p.get("ramp")
    sqdt = np.sqrt(dt)
    sm = dict(mode="wrap")
    j = 0
    for s in range(steps):
        T = C ** (2 * sigma)
        uv2 = u * u * v
        u = u + dt * T * (a - u + uv2) + noise * sqdt * rng.standard_normal((ny, nx))
        v = v + dt * T * (b - uv2)
        u = diffuse(u, Eu, ny, nx)
        v = diffuse(v, Ev, ny, nx)
        # local wavenumber sensing (band-passed)
        w = u - uniform_filter(u, size=(1, w_wide), **sm)
        wf = uniform_filter(w, size=(1, w_bp), **sm)
        gx = 0.5 * (np.roll(wf, -1, 1) - np.roll(wf, 1, 1)) / dx
        g2 = gx * gx
        if ny > 4:
            gy = 0.5 * (np.roll(wf, -1, 0) - np.roll(wf, 1, 0)) / dx
            g2 = g2 + gy * gy
        g2s = uniform_filter(g2, size=(1, w_S), **sm)
        w2s = uniform_filter(wf * wf, size=(1, w_S), **sm)
        S = g2s / (w2s + 1e-9)
        gate = w2s / (w2s + gate2)
        t = s * dt
        if mode == "auto":
            if t >= t_on:
                err = np.clip((kstar2 - S) / kstar2, -1.0, 1.0)
                drv = eps * gate * err
            else:
                drv = 0.0 * S
            C = C + dt * drv
        else:
            C_lo, C_hi, P, tau_c = ramp
            ph = (t % P) / P
            Cset = C_lo + (C_hi - C_lo) * (2 * ph if ph < 0.5 else 2 - 2 * ph)
            drv = (Cset - C) / tau_c
            C = C + dt * drv
        C = diffuse(C, Ec, ny, nx)
        np.clip(C, Cmin, Cmax, out=C)
        if s % meas_every == 0 and j < nm:
            prof = u.mean(axis=0)
            n, pur = count_mode(prof, kmax_idx=nx // 3)
            rec["t"][j] = t
            rec["n"][j] = n
            rec["nz"][j] = count_zc(prof)
            modes[j] = np.abs(np.fft.rfft(prof - prof.mean()))[:modes.shape[1]]
            rec["purity"][j] = pur
            rec["amp"][j] = prof.std()
            rec["Cm"][j] = C.mean()
            rec["Csd"][j] = C.std()
            rec["Sm"][j] = float((S * gate).sum() / max(gate.sum(), 1e-9))
            rec["drive"][j] = float(np.mean(drv))
            rec["envmin"][j] = float(np.sqrt(max(w2s.min(), 0.0)))
            if kymo is not None:
                kymo[j] = prof
            j += 1
        if trace is not None and tr_lo <= s < tr_hi:
            trace[s - tr_lo] = u[0, nx // 3]
        if s in snap_at:
            snaps[s] = (u.copy(), C.copy())
        if s % 500 == 0 and not np.isfinite(u).all():
            rec["blown"] = s
            break
    rec["snaps"] = snaps
    rec["modes"] = modes[:j]
    if kymo is not None:
        rec["kymo"] = kymo[:j]
    if trace is not None:
        rec["trace"] = trace
    for k in keys:
        rec[k] = rec[k][:j]
    return rec
