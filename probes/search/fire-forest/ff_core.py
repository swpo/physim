
"""fire-forest core v2: continuous fuel-fire excitable world with quench.

Fields (LxL torus, dt = 1 tick):
  B fuel in [Bfloor, 1]:  dB = g_i*B*(1-B) - eta*F*B     (slow logistic growth)
      g_i = g*exp(u_i), u_i ~ U(-gsig, gsig) static site quality map
  F fire in [0, 1]:       dF = beta*<F>_nn*sig(B)*(1-F) - delta*F
      sig(B) = 1/(1+exp(-(B-theta)/w))   flammability gate
      QUENCH: F < Fq -> 0   (fire extinguishes; between events F == 0)
  lightning: Poisson sparks, rate f per site per tick, sets F=max(F, 0.9*sig(B))

THEORY COORDINATES (searched):
  Lam   = f*L^2*Tg   sparks per nominal regrow time per field
  theta = ignition fuel threshold (critical fuel level)
  M     = beta/(4*delta)  spread margin (front propagates where M*sig(B) >~ 1)
  D     = eta/delta       burn depth (residual fuel factor)
  gsig  = site-quality log-heterogeneity (0 = homogeneous)
  g     = growth rate (micro price for G3 response curve)
fixed: delta=0.2 (hot residence ~ 10 ticks), w=0.05, Bfloor=0.01, Fq=0.02.
"""
import numpy as np, time, sys
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
from hier_metrics import *


def nominal_Tg(g, theta, Bfloor=0.01):
    return np.log((theta / (1 - theta)) * ((1 - Bfloor) / Bfloor)) / g


def run(L=64, T=60000, g=1e-3, Lam=30.0, theta=0.5, M=3.0, D=8.0, gsig=0.0,
        delta=0.2, w=0.05, Bfloor=0.01, Fq=0.02, seed=0, rec=5, snap_times=(),
        f_abs=None):
    rng = np.random.default_rng(seed)
    beta = 4.0 * delta * M
    eta = delta * D
    Tg = nominal_Tg(g, theta, Bfloor)
    f = f_abs if f_abs is not None else Lam / (L * L * Tg)
    gmap = g * np.exp(rng.uniform(-gsig, gsig, (L, L))) if gsig > 0 else g
    B = rng.uniform(0.05, 0.35, (L, L))
    F = np.zeros((L, L))
    hot_prev = np.zeros((L, L), bool)
    nrec = T // rec
    meanB = np.zeros(nrec); meanF = np.zeros(nrec)
    area = np.zeros(nrec, np.int32); ign = np.zeros(nrec, np.int32)
    hot_ticks = 0; ign_total = 0
    snaps = {}
    t0 = time.time()
    for t in range(T):
        Fn = 0.25 * (np.roll(F, 1, 0) + np.roll(F, -1, 0)
                     + np.roll(F, 1, 1) + np.roll(F, -1, 1))
        sig = 1.0 / (1.0 + np.exp(-(B - theta) / w))
        F += beta * Fn * sig * (1.0 - F) - delta * F
        nsp = rng.poisson(f * L * L)
        if nsp:
            xs = rng.integers(0, L, nsp); ys = rng.integers(0, L, nsp)
            F[xs, ys] = np.maximum(F[xs, ys], 0.9 * sig[xs, ys])
        F[F < Fq] = 0.0
        np.clip(F, None, 1.0, out=F)
        B += gmap * B * (1.0 - B) - eta * F * B
        np.clip(B, Bfloor, 1.0, out=B)
        hot = F > 0.1
        new = hot & ~hot_prev
        r = t // rec
        meanB[r] += B.mean(); meanF[r] += F.mean()
        a = int(hot.sum())
        if a > area[r]: area[r] = a
        ni = int(new.sum())
        ign[r] += ni
        hot_ticks += a; ign_total += ni
        hot_prev = hot
        if t in snap_times:
            snaps[t] = (B.copy(), F.copy())
    meanB /= rec; meanF /= rec
    return dict(meanB=meanB, meanF=meanF, area=area, ign=ign, rec=rec,
                hot_ticks=hot_ticks, ign_total=ign_total, snaps=snaps,
                runtime=time.time() - t0, f=float(f), Tg=float(Tg), L=L, T=T,
                params=dict(L=L, T=T, g=g, Lam=Lam, theta=theta, M=M, D=D,
                            gsig=gsig, delta=delta, w=w, Bfloor=Bfloor,
                            Fq=Fq, seed=seed))


def events_from_series(area, ign, rec, gap_recs=2):
    """events = maximal intervals with hot area>0 (gaps < gap_recs merged)."""
    active = area > 0
    ev = []
    i, n = 0, len(active)
    while i < n:
        if not active[i]:
            i += 1; continue
        j = i
        while j < n:
            if active[j]:
                j += 1
            else:
                k = j
                while k < n and not active[k] and (k - j) < gap_recs:
                    k += 1
                if k < n and active[k]:
                    j = k
                else:
                    break
        ev.append(dict(t0=int(i * rec), dur=int((j - i) * rec),
                       size=int(ign[i:j].sum()), peak=int(area[i:j].max())))
        i = j
    return ev


def wmedian(vals, wts):
    idx = np.argsort(vals)
    v = np.asarray(vals, float)[idx]; wt = np.asarray(wts, float)[idx]
    c = np.cumsum(wt)
    if c[-1] <= 0: return None
    return float(v[np.searchsorted(c, 0.5 * c[-1])])


def measure(out, drop=8000, coarse=25):
    rec = out["rec"]; i0 = drop // rec
    res = dict(runtime=round(out["runtime"], 2), f=out["f"], Tg=round(out["Tg"], 1))
    mB = out["meanB"][i0:]
    res["B_lo"], res["B_hi"] = float(mB.min()), float(mB.max())
    res["B_range"] = res["B_hi"] - res["B_lo"]
    res["meanF_mean"] = float(out["meanF"][i0:].mean())
    sub = max(1, coarse // rec)
    n = len(mB) // sub
    mBc = mB[:n * sub].reshape(n, sub).mean(1)
    top = compact_top_fit(mBc, dt=rec * sub)
    res["top_model"] = top["model"]; res["top_r2"] = top["r2"]
    res["top_params"] = top["params"]; res["top_all"] = top["all"]
    ev = events_from_series(out["area"][i0:], out["ign"][i0:], rec)
    sizes = [e["size"] for e in ev if e["size"] > 0]
    res["n_events"] = len(sizes)
    if sizes:
        res["size_max"] = int(max(sizes))
        res["size_med"] = float(np.median(sizes))
        durs = [e["dur"] for e in ev if e["size"] > 0]
        res["dur_med"] = float(np.median(durs))
        res["tau2"] = wmedian(durs, sizes)
        pl = powerlaw_tail(sizes)
        res["pl"] = {k: (round(v, 3) if isinstance(v, float) else v)
                     for k, v in pl.items()}
    else:
        res["size_max"] = 0; res["tau2"] = None; res["pl"] = None
    res["tau1"] = (out["hot_ticks"] / out["ign_total"]
                   if out["ign_total"] > 0 else None)
    tp = top["params"]
    tau3 = None
    if top["model"] == "oscillator":
        tau3 = tp.get("period")
    elif top["model"] == "switch" and tp.get("mean_dwell"):
        tau3 = 2 * tp["mean_dwell"]
    res["tau3"] = tau3
    res["sep21"] = (res["tau2"] / res["tau1"]) if (res["tau1"] and res["tau2"]) else None
    res["sep32"] = (tau3 / res["tau2"]) if (tau3 and res["tau2"]) else None
    return res


def gates(res, runtime_cap=180.0, min_events=20):
    g1 = (res.get("sep21") is not None and res.get("sep32") is not None
          and res["sep21"] >= 5 and res["sep32"] >= 5
          and res["n_events"] >= min_events)
    m, r2, p = res["top_model"], res["top_r2"], res["top_params"]
    g2 = r2 >= 0.85 and (
        (m == "oscillator" and p.get("n_cycles", 0) >= 5) or
        (m == "relaxation") or
        (m == "switch" and p.get("n_flips", 0) >= 6))
    g5 = res["runtime"] <= runtime_cap
    return dict(G1=bool(g1), G2=bool(g2), G5=bool(g5))
