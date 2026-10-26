"""phoretic-colloids (c33): chemically interacting active colloids, two species, one shared chemical.

Overdamped particles of species s in {A, B}. Each particle makes (alpha_s > 0) or consumes (alpha_s < 0) a
chemical c at a fixed rate and drifts along its gradient with mobility mu_s (mu > 0: up the gradient):
    dx_i = mu_{s_i} grad c(x_i) dt + F_rep dt + sqrt(2 Dp dt) xi,
    0 = D lap c - kd c + sum_j alpha_{s_j} delta(x - x_j)        (quasi-static, screened Poisson, FFT)
Pair interactions through c are non-reciprocal whenever mu_a alpha_b != mu_b alpha_a (Soto & Golestanian
PRL 2014; Agudo-Canalejo & Golestanian PRL 2019). Default: alpha and mu are matrices [species][chemical]. Default two chemicals: A makes
c1, B makes c2; A climbs c1 and descends c2, B climbs both. So A and B each cohere, B is drawn to A and A is
pushed away from B: an A core with a B cap chases its own cap. Soft harmonic repulsion (diameter a) keeps particles apart. The particle's own source is
removed from its gradient by depositing with CIC and subtracting the CIC self-gradient analytically is
skipped; instead c is smoothed with a Gaussian of width ~a (spectral), which makes the self term vanish by
symmetry up to grid error. Optional turnover (off by default). WORLD_P (JSON) overrides P.
"""
import json, os, numpy as np
from numba import njit

P = dict(L=128.0, n=128, NA=1400, NB=400, alpha=[[1.0, 0.0], [0.0, 1.0]], mu=[[1.0, -1.0], [1.0, 0.5]], D=1.0, kd=0.05,
         Dp=0.02, a=1.0, krep=20.0, dt=0.02, sub=25, vmax=5.0, sig=1.0, chemo=1.0,
         NF=0, DpF=0.5, rcat=2.0, kA=0.0, kB=0.0, dA=0.0, dB=0.0, Bneeds_A=1)
P.update(json.loads(os.environ.get("WORLD_P", "{}")))

META = {"name": "phoretic-colloids", "family": "phoretic-colloids", "size": (128, 128), "steps_per_frame": 1,
        "dt": P["dt"] * P["sub"], "channels": ["A density", "B density", "chemicals (sum)"], "matter": [0, 1],
        "threshold": None, "smooth": 1.0, "periodic": True, "radial_channels": [0, 1, 2],
        "domain": (P["L"], P["L"])}


@njit(cache=False)
def repulsion(x, L, a, k):
    n = x.shape[0]; F = np.zeros_like(x); nc = max(3, int(L // a)); cs = L / nc
    head = -np.ones(nc * nc, np.int64); nxt = -np.ones(n, np.int64)
    for i in range(n):
        c = (int(x[i, 0] / cs) % nc) * nc + int(x[i, 1] / cs) % nc; nxt[i] = head[c]; head[c] = i
    for i in range(n):
        cx = int(x[i, 0] / cs) % nc; cy = int(x[i, 1] / cs) % nc
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                j = head[((cx + dx) % nc) * nc + (cy + dy) % nc]
                while j >= 0:
                    if j > i:
                        rx = x[j, 0] - x[i, 0]; ry = x[j, 1] - x[i, 1]
                        rx -= L * np.round(rx / L); ry -= L * np.round(ry / L)
                        r2 = rx * rx + ry * ry
                        if r2 < a * a and r2 > 1e-12:
                            r = np.sqrt(r2); f = k * (a - r)
                            F[i, 0] -= f * rx / r; F[i, 1] -= f * ry / r
                            F[j, 0] += f * rx / r; F[j, 1] += f * ry / r
                    j = nxt[j]
    return F


def _cic_deposit(x, w, n, L):
    g = x / L * n - 0.5; i0 = np.floor(g).astype(int); f = g - i0; out = np.zeros((n, n))
    for di in (0, 1):
        for dj in (0, 1):
            wx = f[:, 0] if di else 1 - f[:, 0]; wy = f[:, 1] if dj else 1 - f[:, 1]
            np.add.at(out, ((i0[:, 1] + dj) % n, (i0[:, 0] + di) % n), w * wx * wy)
    return out / (L / n) ** 2


def _cic_interp(fld, x, n, L):
    g = x / L * n - 0.5; i0 = np.floor(g).astype(int); f = g - i0; out = np.zeros(len(x))
    for di in (0, 1):
        for dj in (0, 1):
            wx = f[:, 0] if di else 1 - f[:, 0]; wy = f[:, 1] if dj else 1 - f[:, 1]
            out += fld[(i0[:, 1] + dj) % n, (i0[:, 0] + di) % n] * wx * wy
    return out


def init(seed, size):
    rng = np.random.default_rng(seed); L, n = P["L"], P["n"]; N = P["NA"] + P["NB"]
    N += P["NF"]; x = rng.uniform(0, L, (N, 2)); sp = np.r_[np.zeros(P["NA"], int), np.ones(P["NB"], int), 2 * np.ones(P["NF"], int)]
    k = 2 * np.pi * np.fft.fftfreq(n, d=L / n); KX, KY = np.meshgrid(k, k)  # KX varies along axis 1 (x)
    K2 = KX ** 2 + KY ** 2; G = np.exp(-0.5 * K2 * P["sig"] ** 2) / (P["D"] * K2 + P["kd"])
    return {"x": x, "sp": sp, "rng": rng, "size": size, "KX": KX, "KY": KY, "G": G, "c": np.zeros((n, n)), "t": 0.0}


def chem(s):
    """chemical k (one per column of alpha): returns c[k], grad c[k] on the grid"""
    n, L = P["n"], P["L"]; al = np.asarray(P["alpha"], float); out = []
    for k in range(al.shape[1]):
        w = np.r_[al, np.zeros((1, al.shape[1]))][s["sp"], k]
        if not np.any(w): out.append(None); continue
        ch = np.fft.fft2(_cic_deposit(s["x"], w, n, L)) * s["G"]
        out.append((np.real(np.fft.ifft2(ch)), np.real(np.fft.ifft2(1j * s["KX"] * ch)), np.real(np.fft.ifft2(1j * s["KY"] * ch))))
    return out


def step(s):
    x, rng, L, n = s["x"], s["rng"], P["L"], P["n"]; dt = P["dt"]
    mu0 = np.asarray(P["mu"], float); mu = np.r_[mu0, np.zeros((1, mu0.shape[1]))][s["sp"]] * P["chemo"]  # (N, K)
    Dp = np.where(s["sp"] == 2, P["DpF"], P["Dp"])[:, None]
    for _ in range(P["sub"]):
        cs = chem(s); v = np.zeros_like(x)
        for k, q in enumerate(cs):
            if q is None: continue
            v += np.stack([_cic_interp(q[1], x, n, L), _cic_interp(q[2], x, n, L)], 1) * mu[:, k:k + 1]
        sp = np.sqrt((v ** 2).sum(1))[:, None]; v = np.where(sp > P["vmax"], v * P["vmax"] / np.maximum(sp, 1e-12), v)
        F = repulsion(x, L, P["a"], P["krep"])
        x = (x + (v + F) * dt + np.sqrt(2 * Dp * dt) * rng.standard_normal(x.shape)) % L
        s["x"] = x
    if P["NF"]: turnover(s)
    s["c"] = sum(q[0] for q in cs if q is not None); s["t"] += dt * P["sub"]
    return s


def turnover(s):
    """closed particle ledger: food F -> A and F -> B catalysed by B within rcat (F -> B also needs an A
    within rcat when Bneeds_A); A -> F and B -> F at constant rates. Total particle number is fixed."""
    from scipy.spatial import cKDTree
    x, sp, rng, T = s["x"], s["sp"], s["rng"], P["dt"] * P["sub"]; L = P["L"]
    tB = cKDTree(x[sp == 1], boxsize=L) if np.any(sp == 1) else None
    tA = cKDTree(x[sp == 0], boxsize=L) if np.any(sp == 0) else None
    f = np.nonzero(sp == 2)[0]; new = sp.copy()
    if len(f) and tB is not None:
        nB = np.array([len(q) for q in tB.query_ball_point(x[f], P["rcat"])])
        nA = np.array([len(q) for q in tA.query_ball_point(x[f], P["rcat"])]) if tA is not None else np.zeros(len(f))
        pA = 1 - np.exp(-P["kA"] * nB * T); pB = 1 - np.exp(-P["kB"] * nB * T) * (1 if True else 0)
        if P["Bneeds_A"]: pB = np.where(nA > 0, pB, 0.0)
        u = rng.random(len(f)); toA = u < pA; toB = (~toA) & (u < pA + pB * (1 - pA))
        new[f[toA]] = 0; new[f[toB]] = 1
    for k, d in ((0, P["dA"]), (1, P["dB"])):
        m = np.nonzero(sp == k)[0]; new[m[rng.random(len(m)) < 1 - np.exp(-d * T)]] = 2
    s["sp"] = new


def fields(s):
    H, W = s["size"]; L = P["L"]; out = np.zeros((3, H, W), np.float32)
    ix = (s["x"] / L * W).astype(int) % W
    for ch in (0, 1):
        m = s["sp"] == ch; np.add.at(out[ch], (ix[m, 1] % H, ix[m, 0]), 1.0)
    from scipy.ndimage import gaussian_filter, zoom
    out[:2] = np.stack([gaussian_filter(o, 1.0, mode="wrap") for o in out[:2]])
    c = s["c"]; out[2] = zoom(c, H / c.shape[0], order=1) if c.shape[0] != H else c
    return out


def particles(s):
    return np.c_[s["x"], s["sp"]]


def stats(s):
    return {k: int((s["sp"] == i).sum()) for i, k in enumerate(("A", "B", "F"))}
