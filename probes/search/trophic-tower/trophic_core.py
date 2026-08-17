
"""Trophic tower core: Hastings-Powell R->H->P reaction-diffusion on a torus.

Nondimensional HP chain:
  dR/dt = R(1-R) - f1(R) H          f1(R) = a1 R/(1+b1 R)
  dH/dt = f1(R) H - f2(H) P - d1 H  f2(H) = a2 H/(1+b2 H)
  dP/dt = f2(H) P - d2 P
plus diffusion (DR, DH, DP), demographic noise nu, torus, Euler dt=DT.
One TICK = one Euler step (DT time units).

Theory coordinates:
  sigma1=b1 (level-1 saturation), g1=a1/b1 (grazer max intake),
  xi1=g1/d1 (grazer gain/death), sigma2=b2, xi2=(a2/b2)/d2,
  rho=d2/d1 (predator/grazer timescale ratio), DH, Delta=DP/DH, nu.
"""
import sys, time, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
from hier_metrics import *

DT = 0.05      # time units per tick
REC = 10       # record macro/blocks every REC ticks
PATCH_EVERY = 100
CAP = 60.0
FLOOR = 1e-9   # rare-immigration floor (honest note in SUMMARY)
DR = 0.01      # resource barely diffuses (plants)

def theory_to_raw(tc):
    """Theory coords -> raw constants.
    tc: d1 (grazer turnover), sigma1=b1, mu1=R*/R_peak (Hopf coord, <1 cycles),
        sigma2=b2, eta2=H*/H_free (predator efficiency, <1 invades),
        rho=d2/d1 (timescale ratio), DH, Delta=DP/DH, nu.
    Derived: xi1 = 1 + 2/(mu1 (sigma1-1));  R* = 1/(sigma1 (xi1-1));
             H_free = (1-R*)(1+sigma1 R*)/a1;  xi2 = 1 + 1/(sigma2 eta2 H_free).
    """
    s1 = tc["sigma1"]; mu1 = tc["mu1"]; d1 = tc["d1"]
    xi1 = 1.0 + 2.0 / (mu1 * (s1 - 1.0))
    g1 = xi1 * d1               # grazer max intake a1/b1
    a1 = g1 * s1; b1 = s1
    Rstar = 1.0 / (s1 * (xi1 - 1.0))
    H_free = (1.0 - Rstar) * (1.0 + s1 * Rstar) / a1
    s2 = tc["sigma2"]; eta2 = tc["eta2"]
    Hstar = eta2 * H_free
    xi2 = 1.0 + 1.0 / (s2 * Hstar)
    d2 = tc["rho"] * d1
    b2 = s2; a2 = xi2 * d2 * s2
    DH = tc["DH"]; DP = tc["Delta"] * tc["DH"]
    return dict(a1=a1, b1=b1, d1=d1, a2=a2, b2=b2, d2=d2,
                DR=DR, DH=DH, DP=DP, nu=tc["nu"],
                Rstar=Rstar, H_free=H_free, Hstar=Hstar, xi1=xi1, xi2=xi2)

def lap(X):
    return (np.roll(X, 1, 0) + np.roll(X, -1, 0) +
            np.roll(X, 1, 1) + np.roll(X, -1, 1) - 4.0 * X)

def run(raw, L=64, nticks=40000, seed=0, record_fields_at=None, nblk=16):
    """Simulate; return recorder dict."""
    rng = np.random.default_rng(seed)
    a1, b1, d1 = raw["a1"], raw["b1"], raw["d1"]
    a2, b2, d2 = raw["a2"], raw["b2"], raw["d2"]
    DRl, DH, DP, nu = raw["DR"], raw["DH"], raw["DP"], raw["nu"]
    # init: near coexistence-ish, noisy blobs to break symmetry (life after "terrain")
    R = 0.5 + 0.15 * rng.random((L, L))
    H = 0.15 + 0.1 * rng.random((L, L))
    P = 0.05 + 0.05 * rng.random((L, L))
    for _ in range(6):   # blobs
        cx, cy = rng.integers(0, L, 2)
        xx, yy = np.meshgrid(np.arange(L), np.arange(L), indexing="ij")
        dd = ((xx - cx + L/2) % L - L/2)**2 + ((yy - cy + L/2) % L - L/2)**2
        H += 0.2 * np.exp(-dd / 18.0)
        P += 0.1 * np.exp(-dd / 30.0)
    bs = L // nblk  # block size
    # probes: 8 pairs (p, p+4 in x) on a grid
    pr = np.linspace(8, L - 9, 4).astype(int)
    probe_ij = [(i, j) for i in pr[:2] for j in pr] + [(i, j) for i in pr[2:] for j in pr]
    probe_ij = probe_ij[:8]
    rec = dict(meanR=[], meanH=[], meanP=[], stdH=[], stdP=[], iface=[],
               blocksH=[], npatch=[], patch_med=[], patch_sizes_all=[],
               probeH=[], probeH4=[], probeR=[], snaps=[], snap_t=[],
               cap_hits=0, L=L, nticks=nticks, DT=DT, REC=REC)
    record_fields_at = set(record_fields_at or [])
    noise_every = 10
    for t in range(nticks):
        f1 = a1 * R / (1.0 + b1 * R)
        f2 = a2 * H / (1.0 + b2 * H)
        Rn = R + DT * (R * (1.0 - R) - f1 * H + DRl * lap(R))
        Hn = H + DT * ((f1 - d1) * H - f2 * P + DH * lap(H))
        Pn = P + DT * ((f2 - d2) * P + DP * lap(P))
        if nu > 0 and t % noise_every == 0:
            s = np.sqrt(noise_every * DT)
            Hn = Hn + nu * s * np.sqrt(np.maximum(Hn, 0)) * rng.standard_normal((L, L))
            Pn = Pn + nu * s * np.sqrt(np.maximum(Pn, 0)) * rng.standard_normal((L, L))
        R, H, P = (np.clip(Rn, FLOOR, CAP), np.clip(Hn, FLOOR, CAP),
                   np.clip(Pn, FLOOR, CAP))
        if t % 2000 == 0:
            if not np.isfinite(H).all() or not np.isfinite(P).all():
                rec["status"] = "unstable"; return rec
            rec["cap_hits"] += int((H >= CAP).sum() + (P >= CAP).sum())
        # probes every tick
        rec["probeH"].append([H[i, j] for i, j in probe_ij])
        rec["probeH4"].append([H[i, (j + 4) % L] for i, j in probe_ij])
        rec["probeR"].append([R[i, j] for i, j in probe_ij])
        if t % REC == 0:
            rec["meanR"].append(R.mean()); rec["meanH"].append(H.mean())
            rec["meanP"].append(P.mean())
            rec["stdH"].append(H.std()); rec["stdP"].append(P.std())
            rec["blocksH"].append(H.reshape(nblk, bs, nblk, bs).mean(axis=(1, 3)).ravel())
            gx = np.abs(np.roll(R, -1, 0) - R); gy = np.abs(np.roll(R, -1, 1) - R)
            g = gx + gy
            rec["iface"].append(float((g > 0.15).mean()))
        if t % PATCH_EVERY == 0:
            thr = H.mean()
            n, sizes = label_patches(H, thr)
            rec["npatch"].append(n)
            rec["patch_med"].append(float(np.median(sizes)) if sizes else 0.0)
            if t > nticks * 0.4:
                rec["patch_sizes_all"].extend(sizes)
        if t in record_fields_at:
            rec["snaps"].append((R.copy(), H.copy(), P.copy())); rec["snap_t"].append(t)
    rec["status"] = "ok"
    rec["finalR"], rec["finalH"], rec["finalP"] = R, H, P
    for k in ("meanR", "meanH", "meanP", "stdH", "stdP", "iface", "probeH",
              "probeH4", "probeR", "blocksH", "npatch", "patch_med"):
        rec[k] = np.asarray(rec[k])
    return rec

def acf_1e(x, dt=1.0):
    """First 1/e crossing of the autocorrelation (FFT). Returns time or None."""
    x = np.asarray(x, float); x = x - x.mean()
    n = len(x)
    if n < 16 or x.std() < 1e-12: return None
    nf = int(2 ** np.ceil(np.log2(2 * n)))
    f = np.fft.rfft(x, nf)
    ac = np.fft.irfft(f * np.conj(f))[:n]
    ac /= ac[0]
    below = np.where(ac < np.exp(-1.0))[0]
    return float(below[0] * dt) if len(below) else None

def pattern_tau(blocks, meanH, dt):
    """Pattern-memory time: corr of block-residual pattern between t and t+lag."""
    Bres = blocks - meanH[:, None]
    T = len(Bres)
    lags = np.unique(np.linspace(1, T // 3, 60).astype(int))
    cs = []
    for lg in lags:
        A = Bres[:-lg][::5]; Bm = Bres[lg:][::5]
        A = A - A.mean(1, keepdims=True); Bm = Bm - Bm.mean(1, keepdims=True)
        num = (A * Bm).sum(1)
        den = np.sqrt((A * A).sum(1) * (Bm * Bm).sum(1)) + 1e-12
        cs.append(float(np.mean(num / den)))
    cs = np.asarray(cs)
    below = np.where(cs < np.exp(-1.0))[0]
    if len(below) == 0: return None, (lags * dt).tolist(), cs.tolist()
    return float(lags[below[0]] * dt), (lags * dt).tolist(), cs.tolist()

def wave_speed(probeH, probeH4, meanH_up, dt_tick, max_lag_ticks=2000):
    """Cross-correlate probe pairs 4 px apart -> speed in cells/unit."""
    speeds = []
    for k in range(probeH.shape[1]):
        x = probeH[:, k] - meanH_up; y = probeH4[:, k] - meanH_up
        x = x - x.mean(); y = y - y.mean()
        if x.std() < 1e-9 or y.std() < 1e-9: continue
        n = len(x); ml = min(max_lag_ticks, n // 4)
        xc = [np.dot(x[:-lg or None], y[lg:]) for lg in range(1, ml)]
        lg = int(np.argmax(xc)) + 1
        if 1 <= lg < ml - 1:
            speeds.append(4.0 / (lg * dt_tick))
    return float(np.median(speeds)) if speeds else None

def front_width(field, gthr_frac=0.35):
    """Median jump/|grad| over strong-gradient pixels -> width in cells."""
    g = np.sqrt((np.roll(field, -1, 0) - field) ** 2 + (np.roll(field, -1, 1) - field) ** 2)
    p95 = np.percentile(g, 97)
    act = g > gthr_frac * p95
    if act.sum() < 20 or p95 < 1e-6: return None
    jump = np.percentile(field, 90) - np.percentile(field, 10)
    w = jump / (g[act] + 1e-12)
    return float(np.clip(np.median(w), 0.5, field.shape[0]))

def measure(rec, cut_frac=0.4):
    """All layer metrics + gate evaluation from a recorder."""
    out = dict(status=rec.get("status", "?"), cap_hits=int(rec.get("cap_hits", 0)))
    if rec.get("status") != "ok":
        return out
    L, DTt, RECd = rec["L"], rec["DT"], rec["REC"]
    dt_mac = DTt * RECd
    n = len(rec["meanH"]); c = int(n * cut_frac)
    mH, mP, mR = rec["meanH"][c:], rec["meanP"][c:], rec["meanR"][c:]
    out["meanH_end"] = float(mH[-200:].mean()); out["meanP_end"] = float(mP[-200:].mean())
    out["meanR_end"] = float(mR[-200:].mean())
    if out["meanP_end"] < 1e-6: out["status"] = "extinct_P"; return out
    if out["meanH_end"] < 1e-6: out["status"] = "extinct_H"; return out
    # --- L3 top law
    fits = {}
    for name, x in (("H", mH), ("P", mP)):
        f = compact_top_fit(x, dt=dt_mac)
        ok = False; Tn = None
        if f["model"] == "oscillator" and f["params"].get("n_cycles", 0) >= 5:
            ok = f["r2"] >= 0.85; Tn = f["params"]["period"]
        elif f["model"] == "switch" and (f["params"].get("n_flips") or 0) >= 6:
            ok = f["r2"] >= 0.85
            Tn = 2 * f["params"]["mean_dwell"] if f["params"]["mean_dwell"] else None
        elif f["model"] == "relaxation":
            ok = f["r2"] >= 0.85; Tn = f["params"]["tau"]
        fits[name] = dict(fit=f, ok=bool(ok), T_units=Tn)
    top = max(fits, key=lambda k: fits[k]["fit"]["r2"] if fits[k]["ok"] else -1)
    out["top_var"] = "mean" + top
    out["top_fit"] = fits[top]["fit"]; out["top_ok"] = fits[top]["ok"]
    out["fits_all"] = {k: (v["fit"]["model"], v["fit"]["r2"]) for k, v in fits.items()}
    T_units = fits[top]["T_units"]
    out["T_units"] = T_units
    out["G2"] = bool(fits[top]["ok"] and fits[top]["fit"]["model"] != "constant")
    # --- L2 patches
    npq = rec["npatch"][int(len(rec["npatch"]) * cut_frac):]
    out["npatch_med"] = float(np.median(npq))
    pm = rec["patch_med"][int(len(rec["patch_med"]) * cut_frac):]
    med_sz = float(np.median([s for s in pm if s > 0]) if (pm > 0).any() else 0)
    out["patch_med_size"] = med_sz
    out["ell2"] = float(np.sqrt(med_sz)) if med_sz else None
    cv = rec["stdH"][c:] / np.maximum(rec["meanH"][c:], 1e-9)
    out["spatial_cv"] = float(np.median(cv))
    blocks = rec["blocksH"][c:]
    tau2, laglist, cslist = pattern_tau(blocks, rec["meanH"][c:], dt_mac)
    out["tau2_units"] = tau2
    # --- L1 fronts
    cut_t = int(len(rec["probeH"]) * cut_frac)
    mH_up = np.repeat(rec["meanH"], RECd)[:len(rec["probeH"])]
    v = wave_speed(rec["probeH"][cut_t:], rec["probeH4"][cut_t:], mH_up[cut_t:], DTt)
    out["wave_speed"] = v
    ell1s = []
    for (R, H, P) in rec["snaps"][-4:]:
        w = front_width(R)
        if w: ell1s.append(w)
    out["ell1"] = float(np.median(ell1s)) if ell1s else None
    tau1 = (out["ell1"] / v) if (v and out["ell1"]) else None
    out["tau1_units"] = tau1
    mR_up = np.repeat(rec["meanR"], RECd)[:len(rec["probeR"])]
    tt = [acf_1e(rec["probeR"][cut_t:, k] - mR_up[cut_t:], DTt)
          for k in range(rec["probeR"].shape[1])]
    tt = [x for x in tt if x]
    out["tau1_pixR"] = float(np.median(tt)) if tt else None
    # --- separations & gates
    t1 = tau1 or out["tau1_pixR"]
    sep12 = (tau2 / t1) if (tau2 and t1) else None
    sep23 = (T_units / tau2) if (T_units and tau2) else None
    l12 = (out["ell2"] / out["ell1"]) if (out["ell2"] and out["ell1"]) else None
    l23 = (L / out["ell2"]) if out["ell2"] else None
    out["sep12_t"], out["sep23_t"], out["sep12_l"], out["sep23_l"] = sep12, sep23, l12, l23
    ok12 = (sep12 or 0) >= 5 or (l12 or 0) >= 5
    ok23 = (sep23 or 0) >= 5 or (l23 or 0) >= 5
    patchy = out["spatial_cv"] >= 0.20 and out["npatch_med"] >= 6
    out["G1"] = bool(ok12 and ok23 and patchy)
    out["patchy"] = bool(patchy)
    # bonus: power-law tail of patch sizes
    if len(rec["patch_sizes_all"]) >= 50:
        out["patch_powerlaw"] = powerlaw_tail(rec["patch_sizes_all"])
    return out

def run_and_measure(tc, L=64, nticks=40000, seed=0, snaps=True):
    raw = theory_to_raw(tc)
    t0 = time.time()
    at = [int(nticks * f) for f in (0.5, 0.65, 0.8, 0.95)] if snaps else []
    rec = run(raw, L=L, nticks=nticks, seed=seed, record_fields_at=at)
    m = measure(rec)
    m["runtime_s"] = round(time.time() - t0, 1)
    m["raw"] = {k: round(v, 5) for k, v in raw.items()}
    return rec, m
