"""Active-gel cells: a Cahn-Hilliard droplet field phi carried by an active-gel flow (c09, exploratory).

phi in [-1, 1]: cell material (+1) vs medium (-1), conserved CH dynamics, advected by the gel flow:
    dphi/dt = -v.grad(phi) + M lap(phi^3 - phi - eps^2 lap phi) + kg a (1 - phi)/2 * [phi > -0.5 nearby]
The gel flow solves gamma v - eta lap v = grad sigma with an active stress that exists only inside cells:
    sigma = zeta h(phi) a/(1 + a)/(1 + rho b),  h = (1 + phi)/2
a: stress generator, made from substrate s inside cells (kc s a h), decays (ka a), carried by v.
b: regulator laid down by a (not advected), decays slowly; weakens the stress.
s: substrate, diffuses, regrows (ks (1 - s)), consumed by a.
Idea: a contractile focus that escapes its own regulator drags the cell (motility); a cell that grows
large enough holds two foci that pull apart (division). WORLD_P overrides P.
"""
import numpy as np, json, os

META = {"name": "active-gel-cells", "family": "active-gel", "parent": "20261025T1016-c09-active-gel-comets-claim",
        "mutation": "the active gel lives inside Cahn-Hilliard droplets that its flow carries",
        "size": (128, 128), "steps_per_frame": 100, "dt": 0.01,
        "channels": ["cell phi (phi + 1)", "generator a", "regulator b", "substrate s"], "matter": [0],
        "threshold": 1.0, "smooth": 1.0, "periodic": True}
P = dict(L=64.0, gamma=1.0, eta=1.0, zeta=30.0, rho=0.5, Da=1.0, Db=0.1, ka=0.1, kb=0.01, kc=0.2, ks=0.02,
         Ds=1.0, M=0.5, eps=1.0, kg=0.02, phi0=-0.6, amp=0.3, a0=0.5, dt=0.01, scale=1.0, cadv=1.0)
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
    phi = P["phi0"] + P["amp"] * rng.standard_normal((H, W))  # noise over the whole domain
    a = P["a0"] * np.maximum(1 + 0.05 * rng.standard_normal((H, W)), 0)
    return {"phi": phi, "a": a, "b": a.copy(), "s": np.ones((H, W)), "ikx": 1j * kx * D, "iky": 1j * ky * D,
            "kk": kk, "G": 1 / (P["gamma"] + P["eta"] * kk), "dx": dx, "vmax": 0.0}


def step(s):
    dt, a, b, phi, sub = P["dt"], s["a"], s["b"], s["phi"], s["s"]
    f2, i2 = np.fft.rfft2, np.fft.irfft2
    sh = a.shape
    h = np.clip((1 + phi) / 2, 0, 1)
    sig = P["zeta"] * h * a / (1 + a) / (1 + P["rho"] * b)
    S = f2(sig) * s["G"]
    vx, vy = i2(s["ikx"] * S, sh), i2(s["iky"] * S, sh)
    s["vmax"] = float(np.sqrt(vx ** 2 + vy ** 2).max())
    div = lambda c: i2(s["ikx"] * f2(c * vx) + s["iky"] * f2(c * vy), sh)
    up = P["kc"] * sub * a * h
    da = -div(a) + up - P["ka"] * a
    db = P["kb"] * (a - b)
    ds = P["ks"] * (1 - sub) - up
    # CH for phi, advected (cadv) and grown where the generator is (kg a (1 - phi)/2 inside or at cells)
    mu_nl = phi ** 3 - phi
    grow = P["kg"] * a * (1 - phi) / 2 * (phi > -0.9)
    Ph = f2(phi)
    rhs = -P["cadv"] * (vx * i2(s["ikx"] * Ph, sh) + vy * i2(s["iky"] * Ph, sh)) + grow  # transport form
    k2, k4 = s["kk"], s["kk"] ** 2
    Phi = (f2(phi) + dt * (f2(rhs) - P["M"] * k2 * f2(mu_nl) + 2 * P["M"] * k2 * f2(phi))) / (1 + dt * P["M"] * (P["eps"] ** 2 * k4 + 2 * k2))
    s["phi"] = np.clip(i2(Phi, sh), -1.5, 1.5)
    s["a"] = np.maximum(i2(f2(a + dt * da) / (1 + dt * P["Da"] * k2), sh), 0)
    s["b"] = np.maximum(i2(f2(b + dt * db) / (1 + dt * P["Db"] * k2), sh), 0)
    s["s"] = i2(f2(sub + dt * ds) / (1 + dt * P["Ds"] * k2), sh)
    return s


def fields(s):
    return np.stack([s["phi"] + 1, s["a"], s["b"], s["s"]]).astype(np.float32)


def stats(s):
    return {"cells_area": round(float((s["phi"] > 0).mean()), 4), "vmax": round(s["vmax"], 3)}


def damage(s, mask):
    s["phi"][mask] = -1; s["a"][mask] = 0; s["b"][mask] = 0
    return s
