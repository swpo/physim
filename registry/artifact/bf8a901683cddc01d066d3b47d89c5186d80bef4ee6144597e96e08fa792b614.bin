
"""hier_metrics — shared measurement helpers for the physim world-search program.

Import from a probe script:
    import sys; sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
    from hier_metrics import *
All functions are numpy-only and cheap.
"""
import numpy as np


def macro_period_quality(x, dt=1.0, max_lag=None):
    """Dominant oscillation of a macro time series via autocorrelation.
    Returns {"period", "q", "n_cycles"}: q in [0,1] is the ACF value at the
    first peak (1 = perfect clock); n_cycles = observed cycles in the series.
    A credible emergent oscillator wants q >= 0.5 and n_cycles >= 5."""
    x = np.asarray(x, float)
    x = x - x.mean()
    if x.std() < 1e-12 or len(x) < 32:
        return {"period": None, "q": 0.0, "n_cycles": 0.0}
    n = len(x)
    max_lag = int(max_lag or n // 2)
    acf = np.correlate(x, x, "full")[n - 1:n - 1 + max_lag]
    acf = acf / acf[0]
    below = np.where(acf < 0)[0]
    if len(below) == 0 or below[0] >= max_lag - 2:
        return {"period": None, "q": 0.0, "n_cycles": 0.0}
    s = below[0]
    k = s + int(np.argmax(acf[s:]))
    return {"period": float(k * dt), "q": float(acf[k]),
            "n_cycles": float(n / max(k, 1))}


def relaxation_tau(x, dt=1.0):
    """Fit x(t) ~ a*exp(-t/tau) + c on a monotone-ish decay segment.
    Returns {"tau", "r2"} (r2 of the exp fit in log space where valid)."""
    x = np.asarray(x, float)
    c = x[-max(3, len(x) // 10):].mean()
    y = x - c
    sgn = np.sign(y[0]) or 1.0
    y = y * sgn
    good = y > max(1e-9, 0.02 * abs(y[0]))
    if good.sum() < 6:
        return {"tau": None, "r2": 0.0}
    t = np.arange(len(x))[good] * dt
    ly = np.log(y[good])
    A = np.vstack([t, np.ones_like(t)]).T
    (m, b), res, *_ = np.linalg.lstsq(A, ly, rcond=None)
    if m >= 0:
        return {"tau": None, "r2": 0.0}
    pred = A @ np.array([m, b])
    ss = 1 - ((ly - pred) ** 2).sum() / max(((ly - ly.mean()) ** 2).sum(), 1e-12)
    return {"tau": float(-1 / m), "r2": float(ss)}


def compact_top_fit(x, dt=1.0):
    """Try the small library of 'simple interpretable top' models on a macro
    series; return the best {"model", "r2", "params"}.
    Models: constant | relaxation (exp) | oscillator (sinusoid at ACF period)
    | switch (two-level threshold process, fitted as 2-means)."""
    x = np.asarray(x, float)
    out = []
    # constant
    out.append(("constant", 1 - x.var() / max(x.var(), 1e-12) if x.var() < 1e-12
                else 1 - (x - x.mean()).var() / max(x.var(), 1e-12), {}))
    # oscillator
    pq = macro_period_quality(x, dt)
    if pq["period"]:
        t = np.arange(len(x)) * dt
        w = 2 * np.pi / pq["period"]
        A = np.vstack([np.sin(w * t), np.cos(w * t), np.ones_like(t)]).T
        coef, *_ = np.linalg.lstsq(A, x, rcond=None)
        pred = A @ coef
        r2 = 1 - ((x - pred) ** 2).sum() / max(((x - x.mean()) ** 2).sum(), 1e-12)
        out.append(("oscillator", float(r2),
                    {"period": pq["period"], "q": pq["q"], "n_cycles": pq["n_cycles"]}))
    # relaxation
    rt = relaxation_tau(x, dt)
    if rt["tau"]:
        t = np.arange(len(x)) * dt
        c = x[-max(3, len(x) // 10):].mean()
        a = x[0] - c
        pred = a * np.exp(-t / rt["tau"]) + c
        r2 = 1 - ((x - pred) ** 2).sum() / max(((x - x.mean()) ** 2).sum(), 1e-12)
        out.append(("relaxation", float(r2), {"tau": rt["tau"]}))
    # switch (2-means step process)
    lo, hi = np.percentile(x, [20, 80])
    if hi - lo > 1e-9:
        lab = x > (lo + hi) / 2
        pred = np.where(lab, x[lab].mean(), x[~lab].mean() if (~lab).any() else 0.0)
        r2 = 1 - ((x - pred) ** 2).sum() / max(((x - x.mean()) ** 2).sum(), 1e-12)
        dwell = np.diff(np.where(np.diff(lab.astype(int)) != 0)[0])
        out.append(("switch", float(r2),
                    {"mean_dwell": float(dwell.mean() * dt) if len(dwell) else None,
                     "n_flips": int(len(dwell))}))
    out.sort(key=lambda z: -z[1])
    best = out[0]
    return {"model": best[0], "r2": round(best[1], 4), "params": best[2],
            "all": [(m, round(r, 3)) for m, r, _ in out]}


def powerlaw_tail(sizes, xmin=None):
    """MLE alpha for a discrete power-law tail + decades spanned + a crude KS.
    Honest reporting: also give decades; < 1.5 decades is NOT a power law."""
    s = np.asarray([v for v in sizes if v > 0], float)
    if len(s) < 50:
        return {"alpha": None, "decades": 0.0, "ks": 1.0, "n": int(len(s))}
    xmin = xmin or max(1.0, np.percentile(s, 30))
    tail = s[s >= xmin]
    if len(tail) < 30:
        return {"alpha": None, "decades": 0.0, "ks": 1.0, "n": int(len(tail))}
    alpha = 1 + len(tail) / np.log(tail / xmin).sum()
    xs = np.sort(tail)
    emp = 1 - np.arange(len(xs)) / len(xs)
    theo = (xs / xmin) ** (1 - alpha)
    ks = float(np.abs(emp - theo).max())
    return {"alpha": float(alpha), "decades": float(np.log10(xs[-1] / xmin)),
            "ks": ks, "n": int(len(tail))}


def scale_separation(micro_tau, macro_scale):
    """Ratio of the macro law's timescale to the micro update timescale."""
    if not micro_tau or not macro_scale:
        return 0.0
    return float(macro_scale / micro_tau)


def label_patches(field, thr):
    """Connected-component count + size list (4-neighbor, no wraparound care)."""
    from scipy import ndimage
    lab, n = ndimage.label(np.asarray(field) > thr)
    if n == 0:
        return 0, []
    sizes = ndimage.sum(np.ones_like(lab), lab, index=range(1, n + 1))
    return int(n), [float(v) for v in np.atleast_1d(sizes)]


def save_strip(fields, path, titles=None, cmap="magma", vmax=None):
    """Save a horizontal strip of 2D fields as one PNG (proof-of-emergence)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    n = len(fields)
    fig, axes = plt.subplots(1, n, figsize=(2.6 * n, 2.6))
    axes = np.atleast_1d(axes)
    for ax, f in zip(axes, fields):
        ax.imshow(f, cmap=cmap, vmax=vmax, interpolation="nearest")
        ax.set_xticks([]); ax.set_yticks([])
    if titles:
        for ax, t in zip(axes, titles):
            ax.set_title(str(t), fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=110, bbox_inches="tight")
    plt.close(fig)
    return path
