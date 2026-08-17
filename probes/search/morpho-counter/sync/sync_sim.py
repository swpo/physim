
"""sync_sim -- TWO coupled morpho-counter rings (batched, internal coupling).

Ring i (i=1,2): certified round-1 counter physics — Schnakenberg (a,b,Du,Dv)
with rate T(C_i)=C_i^(2*sigma); C_i driven by the ring's OWN measured
wavenumber error with gain eps_i toward the shared mid-gap setpoint kstar2.
Detuning: eps1 != eps2 => natural periods differ (T ~ 3.8/eps law).
COUPLING (internal, no schedule): mutual C leakage, pointwise
    dC_i/dt += kappa_c * (C_j - C_i)
= transverse diffusion between two stacked annuli. Nothing else is shared.
"""
import numpy as np
from scipy.ndimage import uniform_filter
import sys, os
_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_here))
from morpho_sim import steady_state, count_mode, count_zc


def make_ops2(ny, nx, dx, dt, Du, Dv, Dc):
    ky = 2 * np.pi * np.fft.fftfreq(ny, d=dx)
    kx = 2 * np.pi * np.fft.rfftfreq(nx, d=dx)
    k2 = ky[:, None] ** 2 + kx[None, :] ** 2
    return tuple(np.exp(-D * k2 * dt) for D in (Du, Dv, Dc))


def diffuse_b(f, E, ny, nx):
    return np.fft.irfft2(np.fft.rfft2(f) * E, s=(ny, nx))


def simulate2(p):
    rng = np.random.default_rng(p.get("seed", 0))
    ny, nx, dx, dt = p["ny"], p["nx"], p.get("dx", 1.0), p["dt"]
    a, b, Du, Dv, Dc = p["a"], p["b"], p["Du"], p["Dv"], p["Dc"]
    sigma, kstar2 = p["sigma"], p["kstar2"]
    eps = np.array([p["eps1"], p["eps2"]]).reshape(2, 1, 1)
    kc = p.get("kappa_c", 0.0)
    steps, meas_every = p["steps"], p.get("meas_every", 50)
    noise = p.get("noise_amp", 2e-3)
    Cmin, Cmax = p.get("Cmin", 0.5), p.get("Cmax", 1.9)
    t_on = p.get("t_on", 250.0)
    lam0 = 2 * np.pi / max(p.get("k_ref", 0.62), 1e-6)
    w_wide = max(5, int(round(2.2 * lam0)) | 1)
    w_bp = max(3, int(round(0.5 * lam0)) | 1)
    w_S = max(3, int(round(1.0 * lam0)) | 1)
    gate2 = p.get("gate2", 1e-3)

    u0, v0 = steady_state(a, b)
    u = u0 + 0.05 * rng.standard_normal((2, ny, nx))
    v = v0 + 0.01 * rng.standard_normal((2, ny, nx))
    C = np.full((2, ny, nx), float(p.get("C0", 1.0)))
    Eu, Ev, Ec = make_ops2(ny, nx, dx, dt, Du, Dv, Dc)

    nm = steps // meas_every
    rec_t = np.zeros(nm)
    per_ring = ["nz", "n", "amp", "Cm", "envmin", "Sm", "drive"]
    rec = {k: np.zeros((nm, 2)) for k in per_ring}
    kymo = np.zeros((nm, 2, nx)) if p.get("kymo") else None
    tr_win = p.get("trace_win")
    if tr_win:
        tr_lo, tr_hi = int(tr_win[0]), int(tr_win[1])
        trace = np.zeros(tr_hi - tr_lo)
    else:
        trace, tr_lo, tr_hi = None, 0, 0
    sqdt = np.sqrt(dt)
    j = 0
    for s in range(steps):
        T = C ** (2 * sigma)
        uv2 = u * u * v
        u = u + dt * T * (a - u + uv2) + noise * sqdt * rng.standard_normal((2, ny, nx))
        v = v + dt * T * (b - uv2)
        u = diffuse_b(u, Eu, ny, nx)
        v = diffuse_b(v, Ev, ny, nx)
        w = u - uniform_filter(u, size=(1, 1, w_wide), mode="wrap")
        wf = uniform_filter(w, size=(1, 1, w_bp), mode="wrap")
        gx = 0.5 * (np.roll(wf, -1, 2) - np.roll(wf, 1, 2)) / dx
        g2 = gx * gx
        if ny > 4:
            gy = 0.5 * (np.roll(wf, -1, 1) - np.roll(wf, 1, 1)) / dx
            g2 = g2 + gy * gy
        g2s = uniform_filter(g2, size=(1, 1, w_S), mode="wrap")
        w2s = uniform_filter(wf * wf, size=(1, 1, w_S), mode="wrap")
        S = g2s / (w2s + 1e-9)
        gate = w2s / (w2s + gate2)
        t = s * dt
        if t >= t_on:
            err = np.clip((kstar2 - S) / kstar2, -1.0, 1.0)
            drv = eps * gate * err
        else:
            drv = np.zeros_like(S)
        C = C + dt * (drv + kc * (C[::-1] - C))
        C = diffuse_b(C, Ec, ny, nx)
        np.clip(C, Cmin, Cmax, out=C)
        if s % meas_every == 0 and j < nm:
            prof = u.mean(axis=1)          # (2, nx)
            rec_t[j] = t
            for i in (0, 1):
                pi = prof[i]
                rec["nz"][j, i] = count_zc(pi)
                n_, _ = count_mode(pi, kmax_idx=nx // 3)
                rec["n"][j, i] = n_
                rec["amp"][j, i] = pi.std()
                rec["Cm"][j, i] = C[i].mean()
                rec["envmin"][j, i] = np.sqrt(max(w2s[i].min(), 0.0))
                rec["Sm"][j, i] = float((S[i] * gate[i]).sum() / max(gate[i].sum(), 1e-9))
                rec["drive"][j, i] = float(drv[i].mean())
            if kymo is not None:
                kymo[j] = prof
            j += 1
        if trace is not None and tr_lo <= s < tr_hi:
            trace[s - tr_lo] = u[0, 0, nx // 3]
        if s % 2000 == 0 and not np.isfinite(u).all():
            rec["blown"] = s
            break
    out = {"t": rec_t[:j]}
    for k in per_ring:
        out[k] = rec[k][:j]
    if kymo is not None:
        out["kymo"] = kymo[:j]
    if trace is not None:
        out["trace"] = trace
    if "blown" in rec:
        out["blown"] = rec["blown"]
    return out
