"""xcell-a-nogate: extended PhySim/blobkit genome world (thread fisim-beyond-laplacian).

ablation of xcell-a: membrane gating of cargo diffusion removed (beta=0)

Numerics: blobkit conventions (dx=0.5, dt=0.02, explicit reaction with old fields, exact
linear diffusion [+ Cahn-Hilliard k^4] in Fourier space). Stepper copied from
threads/fisim-beyond-laplacian/xgenome.py (parity with blobkit m4: 4e-14 after 1000 steps).
"""
import json
import numpy as np
import scipy.fft as sfft

GENOME = json.loads(r"""{"K": [[1.0, 1.5, 0.0, 0.0]], "W": [[1.0], [1.0], [2.0], [1.0]], "acts": [{"Du": 1.0, "k1": 1.058849797569872, "lam": 2.0, "u0": -0.7035399190279497}], "bilin": [], "chans": [{"D": 0.6666666666666666, "g": "id", "sc": 1.0, "tau": 6.0, "thr": 0.0}, {"D": 20.0, "g": "id", "sc": 1.0, "tau": 0.7, "thr": 0.0}, {"tau": 2.0, "D": 0.0, "g": "band", "thr": 0.0, "sc": 0.6, "ch": {"M": 1.0, "k": 1.0, "h": 0.5}}, {"tau": 5.0, "D": 4.0, "g": "id", "thr": 0.0, "sc": 1.0}], "id": "gt_m4", "provenance": {"kind": "reference", "orig": {"Du": 1.0, "Dv": 1.0, "Dw": 20.0, "k1": -0.7, "k3": 1.0, "k4": 1.5, "lam": 2.0, "tau": 3.0, "theta": 0.7}, "source": "M4 A=4 family"}, "perm": [[4, 2, 0.0]]}""")

META = {
    "name": "xcell-a-nogate",
    "family": "fisim-extended-rd",
    "parent": "xcell-a",
    "mutation": "ablation of xcell-a: membrane gating of cargo diffusion removed (beta=0)",
    "size": (160, 160),
    "steps_per_frame": 100,
    "dt": 0.02,
    "channels": ["u (body)", "v (slow inhib)", "w (fast inhib)", "m (CH membrane)", "c (cargo)"],
    "smooth": 1.0,
    "periodic": True,
}
SOUP_N = 8
SOUP_ACTS = [0]

import numpy as np
import scipy.fft as sfft

WORKERS = 2


def _roll_grad(f, dx):
    gy = (np.roll(f, -1, -2) - np.roll(f, 1, -2)) / (2 * dx)
    gx = (np.roll(f, -1, -1) - np.roll(f, 1, -1)) / (2 * dx)
    return gy, gx


def _lap(f, dx):
    return (np.roll(f, 1, -1) + np.roll(f, -1, -1) + np.roll(f, 1, -2)
            + np.roll(f, -1, -2) - 4 * f) / dx ** 2


def _div_face(f, coef, dx):
    """div(coef grad f) with face-averaged coefficient (conservative 5-point)."""
    out = np.zeros_like(f)
    for ax in (-2, -1):
        cf = 0.5 * (coef + np.roll(coef, -1, ax))
        flux = cf * (np.roll(f, -1, ax) - f) / dx
        out += (flux - np.roll(flux, 1, ax)) / dx
    return out


def _upwind_div(rho, vy, vx, dx):
    out = np.zeros_like(rho)
    for v, ax in ((vy, -2), (vx, -1)):
        vf = 0.5 * (v + np.roll(v, -1, ax))
        up = np.where(vf > 0, rho, np.roll(rho, -1, ax))
        flux = vf * up
        out += (flux - np.roll(flux, 1, ax)) / dx
    return out


def ring_kernel_hat(N, dx, R, w):
    y = np.minimum(np.arange(N), N - np.arange(N))[:, None] * dx
    x = np.minimum(np.arange(N), N - np.arange(N))[None, :] * dx
    r = np.sqrt(x ** 2 + y ** 2)
    k = np.exp(-((r - R) / w) ** 2 / 2)
    k /= k.sum()
    return sfft.rfft2(k)


def make_state(g, N, dx=0.5, dt=0.02, noise=0.0, seed=0, F=None):
    na, nc = len(g["acts"]), len(g["chans"])
    if F is None:
        F = np.zeros((na + nc, N, N))
        for i, a in enumerate(g["acts"]):
            F[i] += a["u0"]
    kf = 2 * np.pi * np.fft.fftfreq(N, d=dx)
    kr = 2 * np.pi * np.fft.rfftfreq(N, d=dx)
    k2 = kf[:, None] ** 2 + kr[None, :] ** 2
    Ds = np.array([a["Du"] for a in g["acts"]] + [c["D"] for c in g["chans"]], float)
    expo = Ds[:, None, None] * k2[None]
    for c, ch in enumerate(g["chans"]):
        if "ch" in ch:
            expo[na + c] += ch["ch"]["M"] * ch["ch"]["k"] * k2 ** 2
    E = np.exp(-expo * dt)
    khat = {c: ring_kernel_hat(N, dx, ch["kern"]["R"], ch["kern"]["w"])
            for c, ch in enumerate(g["chans"]) if "kern" in ch}
    return dict(g=g, F=np.array(F, float), E=E, Ds=Ds, khat=khat, N=N, dx=dx, dt=dt, na=na, nc=nc,
                W=np.asarray(g["W"], float), K=np.asarray(g["K"], float),
                lam=np.array([a["lam"] for a in g["acts"]])[:, None, None],
                k1=np.array([a["k1"] for a in g["acts"]])[:, None, None],
                u0=np.array([a["u0"] for a in g["acts"]])[:, None, None],
                tau=np.array([c["tau"] for c in g["chans"]])[:, None, None],
                noise=noise, rng=np.random.default_rng(seed), t=0)


def gfun(ch, z):
    kind = ch["g"]
    if kind == "id":
        return z
    s = np.tanh(np.clip(z - ch.get("thr", 0.0), 0, None) / ch["sc"])
    if kind == "tanh":
        return s
    if kind == "band":
        return 4 * s * (1 - s)
    raise ValueError(kind)


def rhs(S, F):
    g, na, nc, dx = S["g"], S["na"], S["nc"], S["dx"]
    U, X = F[:na], F[na:]
    Z = U - S["u0"]
    R = np.empty_like(F)
    R[:na] = S["lam"] * U - U ** 3 + S["k1"] - np.tensordot(S["K"], X, axes=(1, 0))
    for (i, c, c2, coef) in g.get("bilin", []):
        R[i] -= coef * X[c] * X[c2]
    for c, ch in enumerate(g["chans"]):
        drive = np.zeros_like(Z[0])
        for a in range(na):
            if S["W"][c, a] != 0.0:
                drive += S["W"][c, a] * gfun(ch, Z[a])
        if c in S["khat"]:
            drive = sfft.irfft2(sfft.rfft2(drive, workers=WORKERS) * S["khat"][c], s=drive.shape,
                                workers=WORKERS)
        R[na + c] = (drive - X[c]) / S["tau"][c]
        if "ch" in ch:
            M, h = ch["ch"]["M"], ch["ch"]["h"]
            x = X[c]
            R[na + c] += M * _lap(x * (x - h) * (x - 1.0), dx)
    for (i, c, chi) in g.get("taxis", []):
        gy, gx = _roll_grad(X[c], dx)
        m = np.clip(Z[i], 0, None)
        R[i] -= chi * _upwind_div(m, gy, gx, dx)
    for (i, Dm, p) in g.get("porous", []):
        R[i] += _div_face(U[i], Dm * np.clip(Z[i], 0, None) ** p, dx)
    for (f, c, beta) in g.get("perm", []):
        R[f] += _div_face(F[f], S["Ds"][f] * (np.exp(-beta * np.clip(X[c], 0, None)) - 1.0), dx)
    if g.get("adv"):
        c, alpha = g["adv"]
        gy, gx = _roll_grad(X[c], dx)
        vy, vx = -alpha * gy, -alpha * gx
        D = F.copy()
        D[:na] -= S["u0"]
        for f in range(na + nc):
            if f == na + c:
                continue
            R[f] -= _upwind_div(D[f], vy, vx, dx)
    return R


def step(S):
    F = S["F"]
    Fn = F + S["dt"] * rhs(S, F)
    if S["noise"] > 0:
        Fn[:S["na"]] += S["noise"] * np.sqrt(S["dt"]) * S["rng"].standard_normal(Fn[:S["na"]].shape)
    S["F"] = sfft.irfft2(sfft.rfft2(Fn, workers=WORKERS) * S["E"], s=Fn.shape[-2:], workers=WORKERS)
    S["t"] += 1
    return S


def poke(F, i, y, x, amp, sig, dx):
    N = F.shape[-1]
    L = N * dx
    c = (np.arange(N) + 0.5) * dx
    dy = (c - y + L / 2) % L - L / 2
    dxx = (c - x + L / 2) % L - L / 2
    F[i] += amp * np.exp(-(dy[:, None] ** 2 + dxx[None, :] ** 2) / (2 * sig ** 2))
    return F


def init(seed, size):
    N = size[0]
    dx = 0.5
    rng = np.random.default_rng(seed)
    g = GENOME
    S = make_state(g, N, seed=seed)
    F = S["F"]
    L = N * dx
    na = len(g["acts"])
    W = np.asarray(g["W"], float)
    pts = []
    for _ in range(5000):
        p = rng.uniform(0, L, 2)
        if all(np.hypot(*(((p - q) + L / 2) % L - L / 2)) >= 14.0 for q in pts):
            pts.append(p)
            if len(pts) == SOUP_N:
                break
    for k, p in enumerate(pts):
        a = SOUP_ACTS[k % len(SOUP_ACTS)]
        ang = rng.uniform(0, 2 * np.pi)
        poke(F, a, p[0], p[1], 2.0, 3.0, dx)
        tmp = np.zeros_like(F)
        poke(tmp, 0, p[0] - 0.5 * np.sin(ang), p[1] - 0.5 * np.cos(ang), 1.2, 3.0, dx)
        for c, ch in enumerate(g["chans"]):
            if ch["g"] == "id" and W[c, a] != 0:
                F[na + c] += W[c, a] * tmp[0]
    F[:na] += 0.01 * rng.standard_normal(F[:na].shape)
    return S


def fields(S):
    F = S["F"].copy()
    F[:S["na"]] -= S["u0"]          # report deviations: vacuum = 0 in every channel
    return F


def matter(Fd):
    return np.clip(Fd[0], 0, None)


def damage(S, mask):
    S["F"][:, mask] = 0.0
    S["F"][:S["na"], mask] = S["u0"][:, 0, 0][:, None]
    return S
