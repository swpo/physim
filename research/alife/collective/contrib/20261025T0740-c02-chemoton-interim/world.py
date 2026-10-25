"""FCH field chemoton: bilayer vesicles from noise that keep an autocatalyst and make their own amphiphile.

Fork of c03's fch-vesicles (contrib 20261025T0745-c03-fch-vesicles): same FCH amphiphile field u
(eps = 1, dx = 0.5, eta1 = 2.5, eta2 = 5, asymmetric well, white-noise start), plus
  P  precursor:  dP/dt = DP lap P + F (1 - P) - a K^2 P - r K P              (crosses bilayers freely)
  K  catalyst :  dK/dt = div(DK g grad K) + a K^2 P - dK K,  g = exp(-beta (u - u_bg)), min face mean
  u  amphiphile: du/dt = lap mu_FCH + r K P - kap (u - u_bg)                 (made from P by K; degrades)
The bilayer slows K (gate); P passes. K is bistable-autocatalytic (Gray-Scott-like with D_K = D_P), so
free K spreads out and dies. Initial condition: FCH white noise as in c03, P = 1/2, K = K0 * uniform(0,1)
everywhere (unstructured).
"""
import numpy as np

META = {
    "name": "fch-chemoton",
    "family": "fch-bilayer",
    "parent": "collective/contrib/20261025T0745-c03-fch-vesicles/world.py",
    "mutation": "add a fed precursor P, a bilayer-gated autocatalyst K, amphiphile production r K P and amphiphile decay",
    "size": (128, 128),
    "steps_per_frame": 200,
    "dt": 0.02,
    "channels": ["amphiphile u - u_bg", "precursor P", "catalyst K"],
    "matter": [0],
    "threshold": 0.5,
    "smooth": 1.0,
    "periodic": True,
}

P = dict(eta1=2.5, eta2=5.0, delta=0.3, mean=-1.3, amp=0.3, dx=0.5, dt=0.02, S=4.0, u_bg=-1.6,
         DP=1.0, DK=1.0, beta=2.0, F=0.04, a=1.0, dK=0.1, r=0.04, kap=0.01, K0=1.0, Ksig=0.0, gate=1, kin=0)


def Wp(u, d):
    return (u + 1) * ((u - 1) ** 2 / 2 - d) + 0.5 * (u + 1) ** 2 * (u - 1)


def Wpp(u, d):
    return ((u - 1) ** 2 / 2 - d) + 2 * (u + 1) * (u - 1) + 0.5 * (u + 1) ** 2


def gdiv(c, g):
    """div(g grad c) / dx^2 on a periodic grid with the min face mobility."""
    out = np.zeros_like(c)
    for ax in (0, 1):
        for sh in (1, -1):
            out += np.minimum(g, np.roll(g, -sh, ax)) * (np.roll(c, -sh, ax) - c)
    return out / P["dx"] ** 2


def lap(c):
    return (np.roll(c, 1, 0) + np.roll(c, -1, 0) + np.roll(c, 1, 1) + np.roll(c, -1, 1) - 4 * c) / P["dx"] ** 2


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    u = P["mean"] + P["amp"] * rng.standard_normal((H, W))
    ky = 2 * np.pi * np.fft.fftfreq(H, d=P["dx"])
    kx = 2 * np.pi * np.fft.fftfreq(W, d=P["dx"])
    kk = ky[:, None] ** 2 + kx[None, :] ** 2
    K = rng.random((H, W))
    if P["Ksig"] > 0:  # a smooth random field: Gaussian-filtered white noise, rescaled to [0, 1]
        g = np.exp(-0.5 * kk * (P["Ksig"] * P["dx"]) ** 2)
        K = np.fft.ifft2(np.fft.fft2(K) * g).real
        K = (K - K.min()) / (K.max() - K.min())
    return {"u": u, "P": np.full((H, W), 0.5), "K": P["K0"] * K, "kk": kk, "n": 0}


def step(s):
    u, Pc, K, kk, d, dt, S = s["u"], s["P"], s["K"], s["kk"], P["delta"], P["dt"], P["S"]
    U = np.fft.fft2(u)
    lu = np.fft.ifft2(-kk * U).real
    wp = Wp(u, d)
    rr = lu - wp
    nl = np.fft.ifft2(kk * np.fft.fft2(wp)).real - Wpp(u, d) * rr + P["eta1"] * lu - P["eta2"] * wp
    U = (U - dt * kk * np.fft.fft2(nl) + dt * S * kk ** 2 * U) / (1 + dt * (kk ** 3 + S * kk ** 2))
    unew = np.fft.ifft2(U).real
    g = np.exp(-P["beta"] * np.clip(u - P["u_bg"], 0, None)) if P["gate"] else np.ones_like(u)
    if P["kin"]:  # Schlogl: bistable, P held at 1 (abundant precursor)
        auto = P["a"] * K * K * (1 - K)
        prod = P["r"] * K
        Pc = np.ones_like(Pc)
    else:
        auto = P["a"] * K * K * Pc
        prod = P["r"] * K * Pc
    s["P"] = Pc if P["kin"] else Pc + dt * (P["DP"] * lap(Pc) + P["F"] * (1 - Pc) - auto - prod)
    s["K"] = K + dt * (P["DK"] * gdiv(K, g) + auto - P["dK"] * K)
    s["u"] = unew + dt * (prod - P["kap"] * (u - P["u_bg"]))
    s["n"] += 1
    return s


def fields(s):
    return np.stack([s["u"] - P["u_bg"], s["P"], s["K"]]).astype(np.float32)


def damage(s, mask):
    """Erased matter is deleted: amphiphile reset to the solvent background, catalyst removed."""
    s["u"][mask] = P["u_bg"] + 0.1
    s["K"][mask] = 0.0
    return s
