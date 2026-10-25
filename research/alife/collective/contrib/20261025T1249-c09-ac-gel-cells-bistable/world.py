"""Active-gel Allen-Cahn cells (c09 prototype for Q:active-gel-cells).

phi in [0, 1]: cell (1) vs medium (0), Allen-Cahn, carried by the gel flow in transport form and held
up by the gel it contains (as phase_membrane's cells are held up by their links):
    dphi/dt = -v.grad(phi) + Dp lap phi + r phi (1 - phi) (phi - 1/2 + tilt (<a>_lt - a_th)),  <a>_lt = a screened over range lt
Gel flow: gamma v - eta lap v = grad sigma, sigma = zeta phi a/(1 + a)/(1 + rho b).
a: generator, made from substrate inside cells (kc s a phi), decays (ka a), advected by v, diffuses.
b: regulator laid down by a (not advected); s: substrate, diffuses, regrows (ks (1 - s)).
WORLD_P overrides P.
"""
import numpy as np, json, os

META = {"name": "active-gel-ac-cells", "family": "active-gel", "parent": "20261025T1016-c09-active-gel-comets-claim",
        "mutation": "the gel lives inside Allen-Cahn cells that it holds up and carries",
        "size": (128, 128), "steps_per_frame": 100, "dt": 0.01,
        "channels": ["cell phi", "generator a", "regulator b", "substrate s"], "matter": [0],
        "threshold": 0.5, "smooth": 1.0, "periodic": True}
P = dict(L=64.0, gamma=1.0, eta=1.0, zeta=30.0, rho=0.5, Da=1.0, Db=0.1, ka=0.1, kb=0.01, kc=0.5, ks=0.05,
         Ds=1.0, Dp=0.5, r=2.0, tilt=0.5, a_th=0.5, amp=0.3, dt=0.01, scale=1.0, lt=3.0)
P.update(json.loads(os.environ.get("WORLD_P", "{}")))


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = int(round(size[0] * P["scale"])), int(round(size[1] * P["scale"]))
    dx = P["L"] / W
    ky = 2 * np.pi * np.fft.fftfreq(H, d=dx)[:, None]
    kx = 2 * np.pi * np.fft.rfftfreq(W, d=dx)[None, :]
    kk = kx ** 2 + ky ** 2
    kmax = np.pi / dx
    D = ((np.abs(ky) < 2 / 3 * kmax) & (np.abs(kx) < 2 / 3 * kmax)).astype(float)
    phi = np.clip(0.5 + P["amp"] * rng.standard_normal((H, W)), 0, 1)  # noise over the whole domain
    a = np.clip(0.5 + 0.3 * rng.standard_normal((H, W)), 0, None)
    return {"phi": phi, "a": a, "b": a.copy(), "s": np.ones((H, W)), "ikx": 1j * kx * D, "iky": 1j * ky * D,
            "kk": kk, "G": 1 / (P["gamma"] + P["eta"] * kk), "vmax": 0.0}


def step(s):
    dt, a, b, phi, sub = P["dt"], s["a"], s["b"], s["phi"], s["s"]
    f2, i2 = np.fft.rfft2, np.fft.irfft2; sh = a.shape; k2 = s["kk"]
    sig = P["zeta"] * phi * a / (1 + a) / (1 + P["rho"] * b)
    S = f2(sig) * s["G"]
    vx, vy = i2(s["ikx"] * S, sh), i2(s["iky"] * S, sh)
    s["vmax"] = float(np.sqrt(vx ** 2 + vy ** 2).max())
    Ph = f2(phi)
    adv_phi = vx * i2(s["ikx"] * Ph, sh) + vy * i2(s["iky"] * Ph, sh)
    a_s = i2(f2(a) / (1 + P["lt"] ** 2 * k2), sh)  # the cell is held up by its gel averaged over range lt
    reac = P["r"] * phi * (1 - phi) * (phi - 0.5 + P["tilt"] * (a_s - P["a_th"]))
    up = P["kc"] * sub * a * phi
    da = -i2(s["ikx"] * f2(a * vx) + s["iky"] * f2(a * vy), sh) + up - P["ka"] * a
    s["phi"] = np.clip(i2(f2(phi + dt * (reac - adv_phi)) / (1 + dt * P["Dp"] * k2), sh), 0, 1)
    s["a"] = np.maximum(i2(f2(a + dt * da) / (1 + dt * P["Da"] * k2), sh), 0)
    s["b"] = np.maximum(i2(f2(b + dt * P["kb"] * (a - b)) / (1 + dt * P["Db"] * k2), sh), 0)
    s["s"] = i2(f2(sub + dt * (P["ks"] * (1 - sub) - up)) / (1 + dt * P["Ds"] * k2), sh)
    return s


def fields(s):
    return np.stack([s["phi"], s["a"], s["b"], s["s"]]).astype(np.float32)


def stats(s):
    return {"cell_frac": round(float((s["phi"] > 0.5).mean()), 4), "vmax": round(s["vmax"], 3)}


def damage(s, mask):
    s["phi"][mask] = 0; s["a"][mask] = 0; s["b"][mask] = 0
    return s
