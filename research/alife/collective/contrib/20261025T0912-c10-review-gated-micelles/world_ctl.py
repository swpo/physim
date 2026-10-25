"""c10 copy of collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py with a WORLD_P override line (nothing else changed).

FCH micelles whose self-made shell gates a self-made core cargo, through fission.

Cargo transport here is gated diffusion only (chi = 0, no partitioning): face diffusivity is the
harmonic mean of Dc exp(-beta q), so the shell layer q slows cargo crossing the micelle surface.
Ablations: beta = 0 (no gate, shell still there) and chi_q = 0 (no shell layer).

Shell species q: made where amphiphile is dense (kq (u - u_m)_+), decays (kdq q), and moves by a
Scharfetter-Gummel flux in the potential -chi_q w(u), w(u) = exp(-((u - u_w)/sig_w)^2), which is
largest at intermediate amphiphile density, i.e. on the micelle surface: q adsorbs there and forms
a layer (the same idea as phase_membrane's wall-adsorption drift). chi_q = 0 is the ablation.
The cargo c and the amphiphile u are as in fch-cargo-fission (parent).


This file is the fch-protocell world with these changes: eta1=4, eta2=5 (micelle-fission regime), kd=0.002,
steps_per_frame 200, an amphiphile feed 5e-4, and chi=-3 < 0, so the self-made solute is pulled INTO amphiphile-rich
bodies (partitioning into the micelle core) instead of being pushed out of the bilayer.
The text below describes the parent (chi > 0).

u: amphiphile density, functionalized Cahn-Hilliard (see the fch-vesicles sighting):
    du/dt = lap mu_u + feed,  mu_u = (lap - W''(u))(lap u - W'(u)) + eta1 lap u - eta2 W'(u) + osm chi c
c: a solute with its own transport. It is made only where amphiphile is dense (by the bilayer,
   kp * max(u - u_m, 0)), decays everywhere (kd c), and is pushed out of amphiphile-rich
   regions by the same coupling chi c u that appears in the energy:
    dc/dt = div(Dc (grad c + chi c grad u)) + kp (u - u_m)_+ - kd c
   (Scharfetter-Gummel face fluxes, so c stays >= 0). The bilayer is a barrier of height
   ~chi * (u_bilayer - u_solvent): solute made by the membrane and released into a closed
   lumen is trapped there; solute released to the open outside spreads and decays.
   Ablation: chi = 0 (no barrier), everything else unchanged.
   osm scales the back-reaction chi c in mu_u (1 = the variational model). It is 0 by default:
   the explicit u-c cross-coupling becomes stiff (rate ~ osm chi^2 c Dc k^4) and blew up at
   dt = 0.02 once c ~ 1.6, so the solute is passive (it feels the barrier, the membrane does not
   feel it).
Units: epsilon = 1, dx = 0.5 (P['dx']); P['scale'] > 1 refines the grid at fixed physical size.
"""
import numpy as np

META = {
    "name": "fch-gated-micelles",
    "family": "fch-bilayer",
    "parent": "collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py",
    "mutation": "add a self-made shell species that adsorbs at the micelle surface, and let it gate the cargo (D e^{-beta q}); cargo partitioning off (chi=0)",
    "size": (128, 128),
    "steps_per_frame": 200,
    "dt": 0.02,
    "channels": ["amphiphile u (u + 1.6)", "cargo c", "shell q"],
    "matter": [0],
    "threshold": 0.5,
    "smooth": 1.0,
    "periodic": True,
    "radial_channels": [0, 1, 2],
}

P = dict(eta1=4.0, eta2=5.0, delta=0.3, mean=-1.3, amp=0.3, dx=0.5, dt=0.02, S=4.0, feed=0.0005,
         chi=0.0, Dc=1.0, kp=0.02, u_m=-0.6, kd=0.002, csub=4, u_bg=-1.6, scale=1.0, osm=0.0,
         chi_q=3.0, Dq=0.5, kq=0.02, kdq=0.002, u_w=-0.6, sig_w=0.8, beta=8.0)
import json as _json, os as _os
P.update(_json.loads(_os.environ.get("WORLD_P", "{}")))  # c10: overrides for controls


def Wp(u, d):
    return (u + 1) * ((u - 1) ** 2 / 2 - d) + 0.5 * (u + 1) ** 2 * (u - 1)


def Wpp(u, d):
    return ((u - 1) ** 2 / 2 - d) + 2 * (u + 1) * (u - 1) + 0.5 * (u + 1) ** 2


def bern(x):
    x = np.where(np.abs(x) < 1e-8, 1e-8, x)
    return x / np.expm1(x)


def c_div(c, u, D, chi, dx):
    out = np.zeros_like(c)
    for ax in (0, 1):
        cr, ur = np.roll(c, -1, ax), np.roll(u, -1, ax)
        a = chi * (ur - u)
        F = (D / dx) * (bern(a) * c - bern(-a) * cr)
        out -= (F - np.roll(F, 1, ax)) / dx
    return out


def gate_div(c, q, D, beta, dx):
    """div(D e^{-beta q} grad c), harmonic face mean of the cell diffusivities."""
    g = D * np.exp(-beta * q)
    out = np.zeros_like(c)
    for ax in (0, 1):
        gr = np.roll(g, -1, ax)
        Df = 2 * g * gr / (g + gr + 1e-30)
        F = -Df * (np.roll(c, -1, ax) - c) / dx
        out -= (F - np.roll(F, 1, ax)) / dx
    return out


def v_div(c, V, D, dx):
    """div of the SG flux D (grad c + c grad V) for a general potential V."""
    out = np.zeros_like(c)
    for ax in (0, 1):
        cr, a = np.roll(c, -1, ax), np.roll(V, -1, ax) - V
        F = (D / dx) * (bern(a) * c - bern(-a) * cr)
        out -= (F - np.roll(F, 1, ax)) / dx
    return out


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    dx = P["dx"] / P["scale"]
    u = P["mean"] + P["amp"] * rng.standard_normal((H, W))  # white noise over the whole domain
    c = np.zeros((H, W))
    ky = 2 * np.pi * np.fft.fftfreq(H, d=dx)
    kx = 2 * np.pi * np.fft.fftfreq(W, d=dx)
    kk = ky[:, None] ** 2 + kx[None, :] ** 2
    return {"u": u, "c": c, "q": np.zeros((H, W)), "kk": kk, "dx": dx}


def step(s):
    u, c, kk, d, dt, S = s["u"], s["c"], s["kk"], P["delta"], P["dt"], P["S"]
    U = np.fft.fft2(u)
    lu = np.fft.ifft2(-kk * U).real
    wp = Wp(u, d)
    nl = np.fft.ifft2(kk * np.fft.fft2(wp)).real - Wpp(u, d) * (lu - wp) + P["eta1"] * lu - P["eta2"] * wp + P["osm"] * P["chi"] * c
    U = (U - dt * kk * np.fft.fft2(nl) + dt * S * kk ** 2 * U) / (1 + dt * (kk ** 3 + S * kk ** 2))
    h = dt / P["csub"]
    prod = P["kp"] * np.maximum(u - P["u_m"], 0)
    q = s["q"]
    Vq = -P["chi_q"] * np.exp(-((u - P["u_w"]) / P["sig_w"]) ** 2)
    for _ in range(P["csub"]):
        c = c + h * (gate_div(c, q, P["Dc"], P["beta"], s["dx"]) + prod - P["kd"] * c)
        q = q + h * (v_div(q, Vq, P["Dq"], s["dx"]) + P["kq"] / P["kp"] * prod - P["kdq"] * q)
    s["q"] = np.maximum(q, 0)
    s["u"] = np.fft.ifft2(U).real + dt * P["feed"]
    s["c"] = np.maximum(c, 0)
    return s


def fields(s):
    return np.stack([s["u"] - P["u_bg"], s["c"], s["q"]]).astype(np.float32)


def stats(s):
    return {"mean_u": round(float(s["u"].mean()), 4), "c_tot": round(float(s["c"].sum() * s["dx"] ** 2), 2)}


def damage(s, mask):
    """Erase: amphiphile reset to solvent, solute deleted."""
    s["u"][mask] = P["u_bg"] + 0.1
    s["c"][mask] = 0
    s["q"][mask] = 0
    return s
