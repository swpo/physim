
"""Eco-evolutionary trophic tower: heritable predator attack genotype G.

Micro physics (per cell, torus, Euler dt=DT):
  f1 = a1 R/(1+b1 R)                       grazer intake
  f2 = (G a2) H / (1 + (G b2) H)           predator intake: G scales ATTACK
                                           RATE at fixed handling time h=b2/a2
  dR = R(1-R) - f1 H + DR lap R
  dH = (f1 - d1) H - f2 P + DH lap H
  dP = (f2 - d2 - c(G-1)) P + DP lap P     linear metabolic rent c per unit G
  genotype transport: Q = P*G advects/diffuses WITH biomass (lap Q);
  births copy the local parental G exactly (both P and Q gain f2*P with
  factor G) -> particulate copy inheritance; migration mixes clones
  biomass-weighted; mutation: every KMUT ticks G += m*sqrt(KMUT*DT)*xi.
Selection is NOT coded: no fitness function, no sorting — only differential
biomass growth of cells with different G.
"""
import sys, time
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower")
from hier_metrics import *
from trophic_core import (theory_to_raw, lap, smooth1d, front_transit,
                          front_width, spectral_wavelength, measure_teacup)

DT = 0.05
REC = 10
PATCH_EVERY = 100
CAP = 60.0
FLOOR = 1e-9
GMIN, GMAX = 0.25, 4.0
KMUT = 10

def run_evo(raw, evo, L=64, nticks=120000, seed=0, record_fields_at=None, nblk=16):
    """raw: ecological constants (theory_to_raw of TC*); evo: dict with
    c (price), m (mutation size, G-units per sqrt(tu)), G0 (init genotype)."""
    rng = np.random.default_rng(seed)
    a1, b1, d1 = raw["a1"], raw["b1"], raw["d1"]
    a2, b2, d2 = raw["a2"], raw["b2"], raw["d2"]
    DRl, DH, DP, nu = raw["DR"], raw["DH"], raw["DP"], raw["nu"]
    c, m, G0 = evo["c"], evo["m"], evo.get("G0", 1.0)
    # ecological warm start at G=G0 (same micro physics, 0-D pre-run)
    r0, h0, p0 = 0.6, 0.2, 0.1
    accR = accH = accP = 0.0; nacc = 0
    for i in range(12000):
        f1o = a1 * r0 / (1 + b1 * r0)
        f2o = (G0 * a2) * h0 / (1 + (G0 * b2) * h0)
        r0 += DT * (r0 * (1 - r0) - f1o * h0)
        h0 += DT * ((f1o - d1) * h0 - f2o * p0)
        p0 += DT * ((f2o - d2 - c * (G0 - 1)) * p0)
        r0 = min(max(r0, 1e-9), CAP); h0 = min(max(h0, 1e-9), CAP); p0 = min(max(p0, 1e-9), CAP)
        if i >= 8000:
            accR += r0; accH += h0; accP += p0; nacc += 1
    R0, H0, P0 = accR / nacc, accH / nacc, accP / nacc
    R = R0 * (0.8 + 0.4 * rng.random((L, L)))
    H = H0 * (0.7 + 0.6 * rng.random((L, L)))
    P = P0 * (0.7 + 0.6 * rng.random((L, L)))
    for _ in range(6):
        cx, cy = rng.integers(0, L, 2)
        xx, yy = np.meshgrid(np.arange(L), np.arange(L), indexing="ij")
        dd = ((xx - cx + L/2) % L - L/2)**2 + ((yy - cy + L/2) % L - L/2)**2
        H += 0.6 * H0 * np.exp(-dd / 18.0)
        P += 0.4 * P0 * np.exp(-dd / 30.0)
    G = np.full((L, L), float(G0)) + 0.02 * rng.standard_normal((L, L))
    G = np.clip(G, GMIN, GMAX)
    bs = L // nblk
    pr = np.linspace(8, L - 9, 4).astype(int)
    probe_ij = ([(i, j) for i in pr[:2] for j in pr] +
                [(i, j) for i in pr[2:] for j in pr])[:8]
    rec = dict(meanR=[], meanH=[], meanP=[], stdH=[], stdP=[], iface=[],
               blocksH=[], npatch=[], patch_med=[], patch_sizes_all=[],
               probeH=[], probeH4=[], probeR=[], snaps=[], snap_t=[],
               rowH=[], rowP=[],
               Gbar=[], sdG=[], Gq10=[], Gq90=[], snapsG=[],
               cap_hits=0, L=L, nticks=nticks, DT=DT, REC=REC)
    record_fields_at = set(record_fields_at or [])
    sqKdt = np.sqrt(KMUT * DT)
    for t in range(nticks):
        f1 = a1 * R / (1.0 + b1 * R)
        Ga2 = G * a2
        f2 = Ga2 * H / (1.0 + (G * b2) * H)
        growth = f2 - d2 - c * (G - 1.0)
        Rn = R + DT * (R * (1.0 - R) - f1 * H + DRl * lap(R))
        Hn = H + DT * ((f1 - d1) * H - f2 * P + DH * lap(H))
        Q = P * G
        Pn = P + DT * (growth * P + DP * lap(P))
        Qn = Q + DT * (growth * Q + DP * lap(Q))
        if nu > 0 and t % KMUT == 0:
            s = np.sqrt(KMUT * DT)
            dem = nu * s * np.sqrt(np.maximum(Hn, 0)) * rng.standard_normal((L, L))
            Hn = Hn + dem
            demP = nu * s * np.sqrt(np.maximum(Pn, 0)) * rng.standard_normal((L, L))
            Pn = Pn + demP
            Qn = Qn + demP * G          # demographic noise carries local genotype
        R = np.clip(Rn, FLOOR, CAP); H = np.clip(Hn, FLOOR, CAP)
        P = np.clip(Pn, FLOOR, CAP)
        G = np.clip(Qn / np.maximum(P, FLOOR), GMIN, GMAX)
        if m > 0 and t % KMUT == 0:
            if evo.get("logmut"):
                G = np.clip(G * np.exp(m * sqKdt * rng.standard_normal((L, L))),
                            GMIN, GMAX)
            else:
                G = np.clip(G + m * sqKdt * rng.standard_normal((L, L)), GMIN, GMAX)
        if t % 2000 == 0:
            if not (np.isfinite(H).all() and np.isfinite(P).all() and np.isfinite(G).all()):
                rec["status"] = "unstable"; return rec
            rec["cap_hits"] += int((H >= CAP).sum() + (P >= CAP).sum())
        rec["probeH"].append([H[i, j] for i, j in probe_ij])
        rec["probeH4"].append([H[i, (j + 4) % L] for i, j in probe_ij])
        rec["probeR"].append([R[i, j] for i, j in probe_ij])
        if t % REC == 0:
            rec["meanR"].append(R.mean()); rec["meanH"].append(H.mean())
            rec["meanP"].append(P.mean())
            rec["rowH"].append(H[L // 2].copy()); rec["rowP"].append(P[L // 2].copy())
            rec["stdH"].append(H.std()); rec["stdP"].append(P.std())
            rec["blocksH"].append(H.reshape(nblk, bs, nblk, bs).mean(axis=(1, 3)).ravel())
            g = np.abs(np.roll(R, -1, 0) - R) + np.abs(np.roll(R, -1, 1) - R)
            rec["iface"].append(float((g > 0.15).mean()))
            wsum = P.sum()
            gb = float((P * G).sum() / max(wsum, 1e-12))
            rec["Gbar"].append(gb)
            rec["sdG"].append(float(np.sqrt(max((P * (G - gb) ** 2).sum() / max(wsum, 1e-12), 0.0))))
            rec["Gq10"].append(float(np.percentile(G, 10)))
            rec["Gq90"].append(float(np.percentile(G, 90)))
        if t % PATCH_EVERY == 0:
            Hs = (H + np.roll(H, 1, 0) + np.roll(H, -1, 0) + np.roll(H, 1, 1)
                  + np.roll(H, -1, 1) + np.roll(np.roll(H, 1, 0), 1, 1)
                  + np.roll(np.roll(H, 1, 0), -1, 1) + np.roll(np.roll(H, -1, 0), 1, 1)
                  + np.roll(np.roll(H, -1, 0), -1, 1)) / 9.0
            thr = Hs.mean()
            n, sizes = label_patches(Hs, thr)
            rec["npatch"].append(n)
            rec["patch_med"].append(float(np.median(sizes)) if sizes else 0.0)
            if t > nticks * 0.4:
                rec["patch_sizes_all"].extend(sizes)
        if t in record_fields_at:
            rec["snaps"].append((R.copy(), H.copy(), P.copy()))
            rec["snapsG"].append(G.copy()); rec["snap_t"].append(t)
    rec["status"] = "ok"
    for k in ("meanR", "meanH", "meanP", "stdH", "stdP", "iface", "probeH",
              "probeH4", "probeR", "blocksH", "npatch", "patch_med",
              "rowH", "rowP", "Gbar", "sdG", "Gq10", "Gq90"):
        rec[k] = np.asarray(rec[k])
    return rec


def measure_evo(rec, eco_cut=0.6):
    """L4 metrics on biomass-weighted mean genotype Gbar.
    Relaxation protocol: Gbar starts displaced at G0; fit exp relaxation on
    the approach window; G* = plateau mean; require plateau stationarity.
    Eco tower (L1-L3) measured on the settled tail (cut_frac=eco_cut)."""
    out = dict(status=rec.get("status", "?"))
    if rec.get("status") != "ok":
        return out
    L, DTt, RECd = rec["L"], rec["DT"], rec["REC"]
    dt_mac = DTt * RECd
    eco = measure_teacup(rec, cut_frac=eco_cut)
    out["eco"] = {k: eco.get(k) for k in
                  ("status", "meanH_end", "meanP_end", "T3", "T2", "tau1",
                   "sep12", "sep23", "spatial_cv", "npatch_med", "G1", "G2",
                   "top_fit", "fast_amp_frac", "ell1", "ell2_spec")}
    if eco.get("status") != "ok":
        out["status"] = "eco_" + str(eco.get("status")); return out
    gb = rec["Gbar"]; sd = rec["sdG"]
    n = len(gb)
    q = max(n // 5, 10)
    Gstar = float(gb[-q:].mean())
    plate_sd = float(gb[-q:].std())
    out["Gstar"] = Gstar; out["G_plateau_sd"] = plate_sd
    out["G_init"] = float(gb[0])
    out["sdG_med"] = float(np.median(sd[n // 2:]))
    out["sdG_end"] = float(sd[-q:].mean())
    # plateau stationarity: linear drift over last 40% << plateau fluctuation
    tail = gb[-2 * q:]
    tt = np.arange(len(tail))
    slope = float(np.polyfit(tt, tail, 1)[0]) * len(tail)   # drift over window
    out["G_drift_tailwin"] = slope
    out["stationary"] = bool(abs(slope) < max(3 * plate_sd, 0.02))
    # --- L4 fit
    gap0 = gb[0] - Gstar
    mode = None; tau4 = None; T4 = None; fit4 = None
    thr = max(2.5 * plate_sd, 0.05 * abs(gap0), 0.01)
    if abs(gap0) > max(4 * plate_sd, 0.04):
        # relaxation experiment: fit on window until |gap| first < thr
        gap = np.abs(gb - Gstar)
        below = np.where(gap < thr)[0]
        t_conv = int(below[0]) if len(below) else n
        w = int(min(n, max(t_conv * 1.6, 30)))
        seg = gb[:w]
        fit4 = compact_top_fit(seg, dt=dt_mac)
        if fit4["model"] == "relaxation" and fit4["r2"] >= 0.85:
            mode = "relaxation"; tau4 = fit4["params"]["tau"]
        else:
            # robust log-linear fit of |gap| on the approach
            gseg = gap[:t_conv] if t_conv >= 20 else gap[:n // 2]
            good = gseg > thr
            if good.sum() >= 15:
                tt2 = np.arange(len(gseg))[good] * dt_mac
                ly = np.log(gseg[good])
                mfit, bfit = np.polyfit(tt2, ly, 1)
                pred = mfit * tt2 + bfit
                r2 = 1 - ((ly - pred) ** 2).sum() / max(((ly - ly.mean()) ** 2).sum(), 1e-12)
                if mfit < 0 and r2 >= 0.85:
                    mode = "relaxation_log"; tau4 = float(-1.0 / mfit)
                    fit4 = dict(model="relaxation_log", r2=round(float(r2), 4),
                                params=dict(tau=tau4))
        out["t_conv"] = float(t_conv * dt_mac)
    else:
        # started near attractor: check for slow eco-evo oscillation instead
        fit4 = compact_top_fit(gb[n // 4:], dt=dt_mac)
        if fit4["model"] == "oscillator" and fit4["params"].get("n_cycles", 0) >= 5 and fit4["r2"] >= 0.85:
            mode = "oscillator"; T4 = fit4["params"]["period"]
    out["fit4"] = fit4; out["mode"] = mode; out["tau4"] = tau4; out["T4"] = T4
    # --- entrainment: T3-band amplitude of Gbar ON THE PLATEAU vs plateau sd
    T3 = eco.get("T3")
    if T3:
        w3 = max(int((T3 / 2) / dt_mac), 4)
        gp = gb[-2 * q:]
        gfast = gp - smooth1d(gp, w3)
        pq3 = macro_period_quality(gp - gp.mean(), dt=dt_mac)
        out["G_T3band_amp"] = float(np.std(gfast[w3:-w3])) if len(gfast) > 3 * w3 else None
        out["G_plateau_acfT"] = pq3["period"]; out["G_plateau_acfq"] = pq3["q"]
        out["entrained"] = bool(pq3["period"] and T3 and
                                abs(pq3["period"] - T3) / T3 < 0.25 and pq3["q"] > 0.5)
    # --- gates
    scale4 = tau4 or T4
    out["sep34"] = (scale4 / T3) if (scale4 and T3) else None
    out["G1_4layer"] = bool(eco.get("G1") and out["sep34"] and out["sep34"] >= 5)
    out["G2_L4"] = bool(mode is not None and (fit4 or {}).get("r2", 0) >= 0.85)
    out["variance_ok"] = bool(out["sdG_med"] > 0.01)
    return out

def run_and_measure_evo(tc_eco, evo, L=64, nticks=120000, seed=0, snaps=True):
    raw = theory_to_raw(tc_eco)
    t0 = time.time()
    at = [int(nticks * f) for f in (0.55, 0.7, 0.85, 0.97)] if snaps else []
    rec = run_evo(raw, evo, L=L, nticks=nticks, seed=seed, record_fields_at=at)
    m = measure_evo(rec)
    m["runtime_s"] = round(time.time() - t0, 1)
    m["evo"] = dict(evo)
    return rec, m
