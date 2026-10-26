"""c43: a conserved CIPS enzyme as consumer on c42's Cahn-Hilliard food-chain prey.

Prey (c42, 20261026T1302-c42-foodchain-both-divide-claim): condensate phi_a made from fuel u, decaying to waste w,
fuel regrown from waste (closed ledger for prey material):
    d phi_a = M lap(phi_a^3 - phi_a - kappa lap phi_a) + (2+e) R_a,  c_a = (phi_a + 1 + e)/(2 + e)
    R_a = k1 u c_a^2 + k0 u - kp c_a - y2 cat
Consumer: enzyme q, conserved except a slow uniform turnover (made everywhere at dq*q0, lost at dq*q), never made
from prey; it drifts up its product r (catalysis-induced phase separation, Cotton et al. 2022), and the catalysis
that makes r consumes prey material (to waste):
    d q = Dq lap q - div(chiq q(1-q) grad r) + dq (q0 - q)
    d r = Dr lap r + cat - ksr r,     cat = kr c_a^na q^2 (1 - r)
    d u = Du lap u - k1 u c_a^2 - k0 u + rr w ;  d w = Dw lap w + kp c_a + y2 cat - rr w
So a consumer condensate can exist only where it eats prey material, and nothing it is made of comes from food.
pred_on 0: q held at 0 (consumer-free twin). tcut >= 0: prey material set to its minimum (phi_a=-1) everywhere at
tcut and prey production stopped (E fork for the consumer).
"""
import os, json
import numpy as np
from labkit import ops

META = {
    "name": "cips-consumer", "family": "catalysis-induced-phase-separation",
    "parent": "collective/contrib/20261026T1302-c42-foodchain-both-divide-claim",
    "mutation": "c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material",
    "size": (128, 128), "steps_per_frame": 400, "dt": 0.25,
    "channels": ["prey a", "consumer q", "product r", "fuel u"],
    "matter": [0, 1], "threshold": None,
    "species": {"prey": [0], "consumer": [1]},
}
P = dict(M=0.03, kappa=1.0, A=2.0, e=0.1, k1=0.1, kp=0.02, k0=0.002, rr=0.01, Du=1.0, Dw=2.0,
         ma=-0.55, noise=0.3, u0=1.0,
         Dq=0.3, chiq=30.0, dq=0.002, q0=0.08, qnoise=0.02, Dr=1.0, kr=1.0, na=1.0, ksr=1.0, y2=0.03,
         pred_on=1, tcut=-1.0, dt=0.25)
P.update(json.loads(os.environ.get("WORLD_P", "{}")))


def _faces(u, ax):
    up, um = np.roll(u, -1, ax), np.roll(u, 1, ax)
    d1, d2 = u - um, up - u
    slope = np.where(d1 * d2 > 0, 2 * d1 * d2 / (d1 + d2 + 1e-300), 0.0)
    return u + 0.5 * slope, np.roll(u - 0.5 * slope, -1, ax)


def vf_flux_div(q, r, chi):
    """div of chi q(1-q) grad r, conservative (c40's MUSCL volume-filling face flux)."""
    out = np.zeros_like(q)
    for ax in (-2, -1):
        vf = chi * (np.roll(r, -1, ax) - r)
        L, R = _faces(q, ax)
        flux = np.where(vf > 0, vf * L * (1 - R), vf * R * (1 - L))
        out += flux - np.roll(flux, 1, ax)
    return out


def _ca(pa):
    return np.clip((pa + 1 + P["e"]) / (2 + P["e"]), 0, None)


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    def noise(sig):
        n = rng.standard_normal((H, W)); n = ops.fft_conv(n, ops.gauss_kernel(H, W, sig)); return n / n.std()
    pa = P["ma"] + P["noise"] * noise(2.0)
    q = np.clip(P["q0"] + P["qnoise"] * noise(4.0), 0, 1) if P["pred_on"] else np.zeros((H, W))
    ky, kx = ops.wavenumbers(H, W); k2 = kx ** 2 + ky ** 2; dt = P["dt"]
    return {"pa": pa, "q": q, "r": np.zeros((H, W)), "u": np.full((H, W), P["u0"]), "w": np.zeros((H, W)), "t": 0.0,
            "k2": k2, "shape": (H, W), "den": 1 + dt * P["M"] * k2 * (P["A"] + P["kappa"] * k2),
            "dq_": 1 + dt * P["Dq"] * k2, "dr_": 1 + dt * (P["Dr"] * k2 + P["ksr"]), "du_": 1 + dt * P["Du"] * k2,
            "dw_": 1 + dt * P["Dw"] * k2}


def step(s):
    dt, sh, k2 = P["dt"], s["shape"], s["k2"]
    pa, q, r, u, w = s["pa"], s["q"], s["r"], s["u"], s["w"]
    cut = P["tcut"] >= 0 and s["t"] >= P["tcut"]
    if cut and not s.get("cut_done"):
        pa = np.full(sh, -1.0); s["cut_done"] = True
    ca = _ca(pa)
    feed = 0.0 if cut else P["k1"] * u * ca ** 2 + P["k0"] * u
    feed = np.minimum(feed, 0.5 * np.clip(u, 0, None) / dt)
    cat = P["kr"] * ca ** P["na"] * np.clip(q, 0, None) ** 2 * (1 - r)
    eat = np.minimum(P["y2"] * cat, 0.5 * ca / dt)
    Ra = feed - P["kp"] * ca - eat
    mu = pa ** 3 - pa - P["A"] * pa
    s["pa"] = ops.irfft2((ops.rfft2(pa) - dt * P["M"] * k2 * ops.rfft2(mu) + dt * (2 + P["e"]) * ops.rfft2(Ra)) / s["den"], sh)
    if P["pred_on"]:
        qn = q - dt * vf_flux_div(q, r, P["chiq"]) + dt * P["dq"] * (P["q0"] - q)
        s["q"] = ops.irfft2(ops.rfft2(qn) / s["dq_"], sh)
    s["r"] = ops.irfft2(ops.rfft2(r + dt * cat) / s["dr_"], sh)
    s["u"] = ops.irfft2(ops.rfft2(u + dt * (P["rr"] * w - feed)) / s["du_"], sh)
    s["w"] = ops.irfft2(ops.rfft2(w + dt * (P["kp"] * ca + eat - P["rr"] * w)) / s["dw_"], sh)
    s["t"] += dt
    return s


def fields(s):
    return np.stack([_ca(s["pa"]), s["q"], s["r"], s["u"]])


def damage(s, mask):
    s["pa"][mask] = -1.0; s["q"][mask] = 0.0
    return s
