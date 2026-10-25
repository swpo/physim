"""FCH vesicles that make and trap their own solute.

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
    "name": "fch-protocell",
    "family": "fch-bilayer",
    "parent": "collective/contrib/20261025T0745-c03-fch-vesicles/world.py",
    "mutation": "add a solute made by the bilayer, excluded from it by chi c u (barrier), decaying everywhere",
    "size": (128, 128),
    "steps_per_frame": 800,
    "dt": 0.01,
    "channels": ["amphiphile u (u + 1.6)", "solute c"],
    "matter": [0],
    "threshold": 0.5,
    "smooth": 1.0,
    "periodic": True,
    "radial_channels": [0, 1],
}

P = dict(eta1=2.5, eta2=5.25, delta=0.3, mean=-1.3, amp=0.3, dx=0.5, dt=0.01, S=4.0, feed=0.0,
         chi=6.0, Dc=1.0, kp=0.02, u_m=-0.6, kd=0.001, csub=4, u_bg=-1.6, scale=1.0, osm=0.0)


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


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    dx = P["dx"] / P["scale"]
    u = P["mean"] + P["amp"] * rng.standard_normal((H, W))  # white noise over the whole domain
    c = np.zeros((H, W))
    ky = 2 * np.pi * np.fft.fftfreq(H, d=dx)
    kx = 2 * np.pi * np.fft.fftfreq(W, d=dx)
    kk = ky[:, None] ** 2 + kx[None, :] ** 2
    return {"u": u, "c": c, "kk": kk, "dx": dx}


def step(s):
    u, c, kk, d, dt, S = s["u"], s["c"], s["kk"], P["delta"], P["dt"], P["S"]
    U = np.fft.fft2(u)
    lu = np.fft.ifft2(-kk * U).real
    wp = Wp(u, d)
    nl = np.fft.ifft2(kk * np.fft.fft2(wp)).real - Wpp(u, d) * (lu - wp) + P["eta1"] * lu - P["eta2"] * wp + P["osm"] * P["chi"] * c
    U = (U - dt * kk * np.fft.fft2(nl) + dt * S * kk ** 2 * U) / (1 + dt * (kk ** 3 + S * kk ** 2))
    h = dt / P["csub"]
    prod = P["kp"] * np.maximum(u - P["u_m"], 0)
    for _ in range(P["csub"]):
        c = c + h * (c_div(c, u, P["Dc"], P["chi"], s["dx"]) + prod - P["kd"] * c)
    s["u"] = np.fft.ifft2(U).real + dt * P["feed"]
    s["c"] = np.maximum(c, 0)
    return s


def fields(s):
    return np.stack([s["u"] - P["u_bg"], s["c"]]).astype(np.float32)


def stats(s):
    return {"mean_u": round(float(s["u"].mean()), 4), "c_tot": round(float(s["c"].sum() * s["dx"] ** 2), 2)}


def damage(s, mask):
    """Erase: amphiphile reset to solvent, solute deleted."""
    s["u"][mask] = P["u_bg"] + 0.1
    s["c"][mask] = 0
    return s
