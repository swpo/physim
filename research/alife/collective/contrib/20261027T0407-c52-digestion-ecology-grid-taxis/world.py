"""c52: digestion-driven predators on c46's fuel-driven condensate prey (both kinds are active-chi condensates).

Change from 20261026T2103-c46-hunting-ecology-claim: the predator material phi_b is CONSERVED (never made from prey, never
decays) and miscible on its own (r0b > 0). It condenses only up its own digestion product q, which is made where the predator
digests prey material, so the predator needs prey the way the prey needs fuel:
    dig = k2 c_a^ne c_b^2                          (prey material digested into waste w; w is remade into prey material at g)
    mu_b = phi_b^3 + r0b phi_b - betab q - kappa lap phi_b,   d phi_b = Mb lap mu_b       (no source, no sink)
    d q = Dq lap q + kd dig - kqs q
Predators hunt because they are drawn up q, which they make at their prey-facing side (no written taxis by default: chiF 0).
Defaults (c52 claim): Mb 0.005, k2 0.02, kd 400, ma -0.4, mb -0.8 and c46's fuel-depletion taxis chiF 0.5.
Switches: pred_on 0 (predator-free twin); dfork_t (all prey material, condensed and dissolved, removed at dfork_t and waste
no longer remade into prey material: the prey-removal fork for the predators' E); fork_t (c46's fuel cut for the prey's E).
Original c46 docstring follows.


Prey material phi_a (c_a = (phi_a+1)/2) is a Cahn-Hilliard field whose double well exists only where the prey's own
catalysis makes a product p from a consumed, regrowing fuel F:
    mu_a = phi_a^3 - r phi_a - beta p - kappa lap phi_a,   r = -r0 + alpha p   (r0 > 0: miscible without p;
           the prey material is drawn up its own product p, as in catalysis-induced phase separation)
    d phi_a = M lap mu_a + 2 (g w - eat)                                (no fuel term: matter is never made from fuel)
    d p   = Dp lap p + kc F c_a^n (1-p) - ks p
    d F   = DF lap F - y kc F c_a^n (1-p) + kF (1-F)                   (open energy supply)
Predator: c42's Cahn-Hilliard predator (c_b = (phi_b+1)/2) growing on prey material, decaying to waste w,
and waste is turned back into prey material everywhere (closed material ledger sum(c_a + c_b + w)):
    eat = k2 c_a^ne c_b^2,   d phi_b = M lap(phi_b^3 - phi_b - kappa lap phi_b) + 2 (eat - kq c_b)
    d w = Dw lap w + kq c_b - g w
    plus fuel-depletion taxis of the predator material: - 2 div(chiF c_b (1-c_b) grad(-F)) (predators drift down the
    fuel gradient, toward fuel-consuming prey; prey do not respond: nonreciprocal)
So the prey's matter does not need fuel; only its condensed state does. Switches: pred_on 0 (predator-free twin),
fork_t (F set to 0 and kF -> 0 from fork_t), pred_t (predator noise added at pred_t), cut_* (local kF cut in a disk).
"""
import json, os
import numpy as np
from labkit import ops

META = {
    "name": "digestion-driven-predators",
    "family": "active-emulsion",
    "parent": "collective/contrib/20261026T2103-c46-hunting-ecology-claim",
    "mutation": "predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel",
    "size": (128, 128),
    "steps_per_frame": 500,
    "dt": 0.2,
    "channels": ["prey a", "predator b", "fuel F", "product p", "digestion q"],
    "matter": [0, 1],
    "threshold": 0.5,
    "species": {"prey": [0], "predator": [1]},
}

P = {"M": 0.1, "kappa": 1.0, "A": 3.0, "r0": 0.3, "alpha": 0.0, "beta": 6.0, "kc": 2.0, "ks": 1.0, "n": 2.0, "Dp": 1.0,
     "DF": 10.0, "kF": 0.1, "y": 1.0, "ma": -0.4, "noise": 0.1, "dt": 0.2,
     "pred_on": 1, "Mb": 0.005, "k2": 0.02, "kq": 0.0015, "g": 0.01, "Dw": 2.0, "mb": -0.8, "nb": 0.1,
     "pred_t": 2000.0, "chiF": 0.5, "r0b": 0.3, "betab": 6.0, "kd": 400.0, "kqs": 1.0, "Dq": 1.0, "dfork_t": -1.0, "nbx": 2.0, "dx": 1.0, "ne": 2.0, "fork_t": -1.0, "cut_t": -1.0, "cut_r": 0.0, "cut_y": 0.0, "cut_x": 0.0}
P.update(json.loads(os.environ.get("WORLD_P", "{}")))


def _faces(u, ax):
    up, um = np.roll(u, -1, ax), np.roll(u, 1, ax)
    d1, d2 = u - um, up - u
    slope = np.where(d1 * d2 > 0, 2 * d1 * d2 / (d1 + d2 + 1e-300), 0.0)
    return u + 0.5 * slope, np.roll(u - 0.5 * slope, -1, ax)


def vf_flux_div(c, f, chi):
    """div of chi c(1-c) grad f, conservative MUSCL volume-filling face flux (kstrail / c40)."""
    out = np.zeros_like(c)
    for ax in (-2, -1):
        vf = chi * (np.roll(f, -1, ax) - f)
        L, R = _faces(c, ax)
        flux = np.where(vf > 0, vf * L * (1 - R), vf * R * (1 - L))
        out += flux - np.roll(flux, 1, ax)
    return out


def _c(phi):
    return np.clip((phi + 1) / 2, 0, None)


def _noise(rng, H, W, L=2.0, dx=1.0):
    L = L / dx
    n = rng.standard_normal((H, W))
    n = ops.fft_conv(n, ops.gauss_kernel(H, W, L))
    return n / n.std()


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    q = dict(P)
    pa = q["ma"] + q["noise"] * _noise(rng, H, W, dx=q["dx"])
    nb = _noise(rng, H, W, dx=q["dx"])
    pb = (q["mb"] + q["nb"] * nb) if (q["pred_on"] and q["pred_t"] < 0) else -np.ones((H, W))
    ca = _c(pa)
    F = np.ones((H, W))
    p = q["kc"] * ca ** q["n"] / (q["kc"] * ca ** q["n"] + q["ks"])
    ky, kx = ops.wavenumbers(H, W, q["dx"])
    k2 = kx ** 2 + ky ** 2
    dt = q["dt"]
    yy, xx = np.mgrid[0:H, 0:W]
    return {"pa": pa, "pb": pb, "p": p, "F": F, "w": np.zeros((H, W)), "q": np.zeros((H, W)), "t": 0.0, "shape": (H, W), "par": q,
            "k2": k2, "nbfield": nb, "yy": yy, "xx": xx,
            "dena": 1 + dt * q["M"] * k2 * (q["A"] + q["kappa"] * k2),
            "denb": 1 + dt * q["Mb"] * k2 * (q["A"] + q["kappa"] * k2), "Lq": 1 / (1 + dt * (q["Dq"] * k2 + q["kqs"])),
            "Lp": 1 / (1 + dt * (q["Dp"] * k2 + q["ks"])), "LF": 1 / (1 + dt * q["DF"] * k2),
            "Lw": 1 / (1 + dt * q["Dw"] * k2)}


def step(s):
    q, dt, sh, k2 = s["par"], s["par"]["dt"], s["shape"], s["k2"]
    pa, pb, p, F, w = s["pa"], s["pb"], s["p"], s["F"], s["w"]
    if q["pred_on"] and q["pred_t"] >= 0 and abs(s["t"] - q["pred_t"]) < dt / 2:
        pb = q["mb"] + q["nb"] * s["nbfield"]
    if q["dfork_t"] >= 0 and abs(s["t"] - q["dfork_t"]) < dt / 2:
        pa = -np.ones(sh)
    if q["dfork_t"] >= 0 and s["t"] >= q["dfork_t"]:
        w = 0.0 * w
    ca, cb = _c(pa), _c(pb)
    cat = q["kc"] * F * ca ** q["n"] * (1 - p)
    eat = q["k2"] * ca ** q["ne"] * cb ** q["nbx"] if q["pred_on"] else 0.0 * ca
    eat = np.minimum(eat, 0.5 * ca / dt)
    regen = q["g"] * w
    r = -q["r0"] + q["alpha"] * p
    mu_a = pa ** 3 - r * pa - q["beta"] * p - q["A"] * pa
    ha = (ops.rfft2(pa) - dt * q["M"] * k2 * ops.rfft2(mu_a) + dt * 2.0 * ops.rfft2(regen - eat)) / s["dena"]
    s["pa"] = ops.irfft2(ha, sh)
    mu_b = pb ** 3 + q["r0b"] * pb - q["betab"] * s["q"] - q["A"] * pb
    taxis = 2.0 * vf_flux_div(np.clip(cb, 0, 1), -F, q["chiF"]) / q["dx"] ** 2 if q["chiF"] else 0.0 * cb
    hb = (ops.rfft2(pb) - dt * q["Mb"] * k2 * ops.rfft2(mu_b) - dt * ops.rfft2(taxis)) / s["denb"]
    s["pb"] = ops.irfft2(hb, sh)
    s["q"] = ops.irfft2(ops.rfft2(s["q"] + dt * q["kd"] * eat) * s["Lq"], sh)
    s["p"] = ops.irfft2(ops.rfft2(p + dt * cat) * s["Lp"], sh)
    kF = q["kF"]
    if q["fork_t"] >= 0 and s["t"] >= q["fork_t"]:
        kF = 0.0
        if abs(s["t"] - q["fork_t"]) < dt / 2:
            F = 0.0 * F
    if q["cut_t"] >= 0 and s["t"] >= q["cut_t"]:
        H, W = sh
        dy = (s["yy"] - q["cut_y"] + H / 2) % H - H / 2
        dx = (s["xx"] - q["cut_x"] + W / 2) % W - W / 2
        kF = kF * ((dy * dy + dx * dx) > q["cut_r"] ** 2)
    s["F"] = ops.irfft2(ops.rfft2(F + dt * (-q["y"] * cat + kF * (1 - F))) * s["LF"], sh)
    s["w"] = ops.irfft2(ops.rfft2(w + dt * (eat - regen)) * s["Lw"], sh)
    s["t"] += dt
    return s


def fields(s):
    return np.stack([_c(s["pa"]), _c(s["pb"]), s["F"], s["p"], s["q"]])


def q_bath(s):
    return s["par"]["mb"]


def damage(s, mask):
    s["pa"] = np.where(mask, -1.0, s["pa"])
    s["pb"] = np.where(mask, q_bath(s), s["pb"])
    return s
