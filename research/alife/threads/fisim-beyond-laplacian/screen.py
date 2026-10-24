"""Quick-look screening: run an x-genome from a soup IC, save a strip PNG of all fields."""
import copy, json, sys, time
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage
import xgenome as X

WORLDS = "/home/user/physim/packages/blobkit/blobkit/data/worlds/"


def load(name):
    return json.load(open(WORLDS + name + ".json"))


def soup(g, N, seed, n=6, dx=0.5, dmin=14.0, dress=0.6, kick=0.5, acts=None):
    rng = np.random.default_rng(seed)
    S = X.make_state(g, N)
    F = S["F"]
    L = N * dx
    na = len(g["acts"])
    W = np.asarray(g["W"], float)
    pts = []
    for _ in range(5000):
        p = rng.uniform(0, L, 2)
        if all(np.hypot(*(((p - q) + L / 2) % L - L / 2)) >= dmin for q in pts):
            pts.append(p)
            if len(pts) == n:
                break
    acts = acts if acts is not None else list(range(na))
    for k, p in enumerate(pts):
        a = acts[k % len(acts)]
        ang = rng.uniform(0, 2 * np.pi)
        X.poke(F, a, p[0], p[1], 2.0, 3.0, dx)
        sy, sx = p[0] - kick * np.sin(ang), p[1] - kick * np.cos(ang)
        tmp = np.zeros_like(F)
        X.poke(tmp, 0, sy, sx, 2.0 * dress, 3.0, dx)
        for c, ch in enumerate(g["chans"]):
            if ch["g"] == "id" and W[c, a] != 0:
                F[na + c] += W[c, a] * tmp[0]
    F[:na] += 0.01 * rng.standard_normal(F[:na].shape)
    return F


def run(g, N=128, T=200.0, seed=0, nsnap=8, F=None, noise=0.0, **kw):
    F = soup(g, N, seed, **kw) if F is None else F
    S = X.make_state(g, N, F=F, noise=noise, seed=seed)
    steps = int(round(T / S["dt"]))
    at = set(np.linspace(0, steps, nsnap).round().astype(int).tolist())
    snaps, ts = [], []
    t0 = time.time()
    for k in range(steps + 1):
        if k in at:
            snaps.append(S["F"].copy()); ts.append(k * S["dt"])
            if not np.isfinite(S["F"]).all():
                break
        if k < steps:
            X.step(S)
    return np.array(snaps), ts, time.time() - t0


def strip(snaps, ts, names, path, title=""):
    nf = snaps.shape[1]
    fig, ax = plt.subplots(nf, len(ts), figsize=(1.6 * len(ts), 1.6 * nf + 0.3), squeeze=False)
    for f in range(nf):
        lo, hi = np.nanpercentile(snaps[:, f], [0.5, 99.5])
        for k in range(len(ts)):
            ax[f, k].imshow(snaps[k, f], vmin=lo, vmax=hi, cmap="magma")
            ax[f, k].set_xticks([]); ax[f, k].set_yticks([])
            if f == 0:
                ax[f, k].set_title(f"t={ts[k]:.0f}", fontsize=7)
        ax[f, 0].set_ylabel(names[f] if f < len(names) else str(f), fontsize=7)
    fig.suptitle(title, fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=60)
    from PIL import Image
    Image.open(path).convert("RGB").quantize(64).save(path, optimize=True)
    plt.close(fig)


def blobs(u, u0, lam=2.0, frac=0.45):
    thr = u0 + frac * (np.sqrt(lam) - u0)
    lab, n = ndimage.label(u > thr)
    return n, (u > thr).mean()


def front_width(u, u0, lam=2.0):
    """Median 10-90% front width (px) of activator blobs, measured along the gradient:
    width ~ (u_hi - u_lo)*0.8 / |grad u| at the mid-level contour."""
    hi = np.percentile(u, 99.5)
    mid = 0.5 * (hi + u0)
    gy, gx = np.gradient(u)
    gm = np.hypot(gy, gx)
    band = np.abs(u - mid) < 0.08 * (hi - u0)
    if band.sum() < 5:
        return np.nan
    return float(0.8 * (hi - u0) / np.median(gm[band]))
