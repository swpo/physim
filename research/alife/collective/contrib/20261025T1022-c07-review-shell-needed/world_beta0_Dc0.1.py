"""Metabolic FCH micelles: a shell-held autocatalyst turns a fed precursor into amphiphile.

u  amphiphile, functionalized Cahn-Hilliard (as fch-gated-micelles) with NO amphiphile feed; instead
   du/dt = lap mu + ks c p g - kdeg (u - u_bg)_+          g = (u - u_m)_+ (amphiphile-rich = body)
   amphiphile is made only where the catalyst c meets the precursor p inside a body, and it
   degrades back to solvent everywhere, so a body must keep metabolizing to persist.
p  precursor (the resource), fed from a reservoir and consumed by the catalyst:
   dp/dt = Dp lap p + F (1 - p) - (ks + kc) c p g
c  catalyst, autocatalytic inside bodies, decays everywhere, held in by the shell:
   dc/dt = div(Dc e^{-beta q} grad c) + kc c p g - kdc c
q  shell species, made by the body and adsorbed at its surface (fch-gated-micelles):
   dq/dt = div(Dq (grad q + q grad Vq)) + kq g - kdq q,  Vq = -chi_q exp(-((u - u_w)/sig_w)^2)
Initial condition: white-noise u (mean -1.3) and a uniform random catalyst c in [0, c0] everywhere.
Fork controls: F = 0 from t_cut (precursor supply cut), and kc = 0 / ks = 0 ablations.
"""
import numpy as np

META = {
    "name": "fch-metabolic-micelles-lowDc",
    "family": "fch-bilayer",
    "parent": "collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py",
    "mutation": "amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded",
    "size": (128, 128),
    "steps_per_frame": 200,
    "dt": 0.02,
    "channels": ["amphiphile u (u + 1.6)", "catalyst c", "shell q", "precursor p"],
    "matter": [0],
    "threshold": 0.5,
    "smooth": 1.0,
    "periodic": True,
    "radial_channels": [0, 1, 2, 3],
}

P = dict(eta1=4.0, eta2=5.0, delta=0.3, mean=-1.3, amp=0.3, dx=0.5, dt=0.02, S=4.0, u_bg=-1.6, u_m=-0.6,
         ks=0.03, kdeg=0.005, Dp=1.0, F=0.01, kc=0.05, kdc=0.01, Dc=0.1, beta=0.0, c0=0.2,
         chi_q=3.0, Dq=0.5, kq=0.02, kdq=0.002, u_w=-0.6, sig_w=0.8, csub=4, scale=1.0, t_cut=-1.0)


def Wp(u, d):
    return (u + 1) * ((u - 1) ** 2 / 2 - d) + 0.5 * (u + 1) ** 2 * (u - 1)


def Wpp(u, d):
    return ((u - 1) ** 2 / 2 - d) + 2 * (u + 1) * (u - 1) + 0.5 * (u + 1) ** 2


def bern(x):
    x = np.where(np.abs(x) < 1e-8, 1e-8, x)
    return x / np.expm1(x)


def v_div(c, V, D, dx):
    out = np.zeros_like(c)
    for ax in (0, 1):
        cr, a = np.roll(c, -1, ax), np.roll(V, -1, ax) - V
        F = (D / dx) * (bern(a) * c - bern(-a) * cr)
        out -= (F - np.roll(F, 1, ax)) / dx
    return out


def gate_div(c, q, D, beta, dx):
    g = D * np.exp(-beta * q)
    out = np.zeros_like(c)
    for ax in (0, 1):
        gr = np.roll(g, -1, ax)
        Df = 2 * g * gr / (g + gr + 1e-30)
        F = -Df * (np.roll(c, -1, ax) - c) / dx
        out -= (F - np.roll(F, 1, ax)) / dx
    return out


def lap(f, dx):
    return (np.roll(f, 1, 0) + np.roll(f, -1, 0) + np.roll(f, 1, 1) + np.roll(f, -1, 1) - 4 * f) / dx ** 2


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    dx = P["dx"] / P["scale"]
    u = P["mean"] + P["amp"] * rng.standard_normal((H, W))
    c = P["c0"] * rng.random((H, W))
    ky = 2 * np.pi * np.fft.fftfreq(H, d=dx)
    kx = 2 * np.pi * np.fft.fftfreq(W, d=dx)
    kk = ky[:, None] ** 2 + kx[None, :] ** 2
    return {"u": u, "c": c, "q": np.zeros((H, W)), "p": np.ones((H, W)), "kk": kk, "dx": dx, "t": 0.0}


def step(s):
    u, c, q, p, kk, d, dt, S, dx = s["u"], s["c"], s["q"], s["p"], s["kk"], P["delta"], P["dt"], P["S"], s["dx"]
    U = np.fft.fft2(u)
    lu = np.fft.ifft2(-kk * U).real
    wp = Wp(u, d)
    nl = np.fft.ifft2(kk * np.fft.fft2(wp)).real - Wpp(u, d) * (lu - wp) + P["eta1"] * lu - P["eta2"] * wp
    U = (U - dt * kk * np.fft.fft2(nl) + dt * S * kk ** 2 * U) / (1 + dt * (kk ** 3 + S * kk ** 2))
    g = np.maximum(u - P["u_m"], 0)
    Fp = P["F"] if (P["t_cut"] < 0 or s["t"] < P["t_cut"]) else 0.0
    make_u = P["ks"] * c * p * g
    h = dt / P["csub"]
    Vq = -P["chi_q"] * np.exp(-((u - P["u_w"]) / P["sig_w"]) ** 2)
    for _ in range(P["csub"]):
        rep = P["kc"] * c * p * g
        use = (P["ks"] + P["kc"]) * c * p * g
        p = np.maximum(p + h * (P["Dp"] * lap(p, dx) + Fp * (1 - p) - use), 0)
        c = np.maximum(c + h * (gate_div(c, q, P["Dc"], P["beta"], dx) + rep - P["kdc"] * c), 0)
        q = np.maximum(q + h * (v_div(q, Vq, P["Dq"], dx) + P["kq"] * g - P["kdq"] * q), 0)
    s["u"] = np.fft.ifft2(U).real + dt * (make_u - P["kdeg"] * np.maximum(u - P["u_bg"], 0))
    s["c"], s["q"], s["p"] = c, q, p
    s["t"] += dt
    return s


def fields(s):
    return np.stack([s["u"] - P["u_bg"], s["c"], s["q"], s["p"]]).astype(np.float32)


def stats(s):
    return {"mean_u": round(float(s["u"].mean()), 4), "c_tot": round(float(s["c"].sum() * s["dx"] ** 2), 2),
            "p_mean": round(float(s["p"].mean()), 3)}


def damage(s, mask):
    s["u"][mask] = P["u_bg"] + 0.1
    for k in ("c", "q"):
        s[k][mask] = 0
    return s
