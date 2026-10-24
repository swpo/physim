"""Extended blobkit genome ("x-genome"): the deviation-form PhySim genome plus
vacuum-exact non-diffusive operators. Standalone (does not import blobkit).

Base (blobkit verbatim, op order: explicit reaction with OLD fields, exact diffusion
in Fourier space; dx=0.5, dt=0.02):
  du_i/dt = Du_i lap u_i + lam_i u_i - u_i^3 + k1_i - sum_c K[i,c] x_c - bilin
  dx_c/dt = (sum_a W[c,a] g_c(z_a) - x_c)/tau_c + D_c lap x_c,   z_a = u_a - u0_a

Extensions (all vanish identically at the vacuum u=u0, x=0, so the vacuum stays an
exact rest state for any coefficients). Each is an optional genome key:

  chan["kern"]   = {"R":r, "w":w}   channel drive is a ring-kernel convolution of
                                     g(z) (nonlocal coupling; Lenia-style shell)
  chan["g"]="band"                  rim deposit g(z)=4 s(1-s), s=tanh(max(z-thr,0)/sc):
                                     zero at vacuum and in saturated interiors, peaks at
                                     the activator's front
  chan["ch"]     = {"M":M,"k":kap,"h":h}  Cahn-Hilliard term on channel c:
                                     + M lap( x(x-h)(x-1) ) - M kap lap^2 x
                                     (wells at x=0 [vacuum] and x=1, barrier at h)
  "taxis": [[i, c, chi]]            u_i += -chi div( max(z_i,0) grad x_c )
                                     (chemotactic / cross-diffusive body transport)
  "porous": [[i, Dm, p]]            u_i += div( Dm max(z_i,0)^p grad u_i )
                                     (density-dependent diffusion)
  "adv": [c, alpha]                 every field f += -div( f_dev v ), v = -alpha grad x_c
  "perm": [[f, c, beta]]            diffusion of field f (act/channel NAME, or index in the
                                     stacked state) through channel c (NAME or channel index) is gated:
                                     div( D_f exp(-beta max(x_c,0)) grad f )
                                     (a membrane that blocks transport)
"""
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


def _resolve(g):
    """Allow names in perm/taxis entries: a field is an act or channel name (state index),
    a gate/gradient channel is a channel name (channel index). Numbers pass through."""
    na = len(g["acts"])
    an = {a.get("name"): i for i, a in enumerate(g["acts"]) if a.get("name")}
    cn = {c.get("name"): j for j, c in enumerate(g["chans"]) if c.get("name")}
    fld = lambda x: x if not isinstance(x, str) else (an[x] if x in an else na + cn[x])
    chn = lambda x: x if not isinstance(x, str) else cn[x]
    act = lambda x: x if not isinstance(x, str) else an[x]
    perm = [[fld(f), chn(c), b] for f, c, b in g.get("perm", [])]
    taxis = [[act(i), chn(c), k] for i, c, k in g.get("taxis", [])]
    return perm, taxis


def make_state(g, N, dx=0.5, dt=0.02, noise=0.0, seed=0, F=None):
    na, nc = len(g["acts"]), len(g["chans"])
    perm, taxis = _resolve(g)
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
    return dict(g=g, F=np.array(F, float), E=E, Ds=Ds, perm=perm, taxis=taxis, khat=khat, N=N, dx=dx, dt=dt, na=na, nc=nc,
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
    for (i, c, chi) in S["taxis"]:
        gy, gx = _roll_grad(X[c], dx)
        m = np.clip(Z[i], 0, None)
        R[i] -= chi * _upwind_div(m, gy, gx, dx)
    for (i, Dm, p) in g.get("porous", []):
        R[i] += _div_face(U[i], Dm * np.clip(Z[i], 0, None) ** p, dx)
    for (f, c, beta) in S["perm"]:
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
