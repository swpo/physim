"""c58: the kind-specific-waste fed vortices (20261027T1245-c58-vortex-waste-novelty) with a trait VECTOR of nt components
(z is a stack of nt trait masses, theta_i = z_i/c; the waste carries nt waste-trait masses V_i). Mutation shifts theta by dm
along a random direction (nt standard-normal draws, normalised; the draws never read c, z or theta). The waste factor is
G = exp(-|theta - theta_W|^2 / (2 sw^2)); the directional term eps is not used (eps 0). nt 1 reproduces the parent with
a random sign. Parent docstring follows.
c58: fed vortices with a continuous heritable trait and a kind-specific waste (20261027T1230-c58-vortex-trait-climb plus
a waste W that eating releases, carrying the eater's trait as waste-trait mass V = W theta_W; W and V diffuse at Dw and decay at dw):
    dW = -u.grad W + Dw lap W + pw eat - dw W        dV = -u.grad V + Dw lap V + pw eat theta - dw V
The gain is k (1 + ew (1 - W/(1+W) G)), G = exp(-(theta - theta_W)^2 / (2 sw^2)): a vortex is held back by the waste of
vortices with a trait like its own (sw <= 0: G = 1, kind-blind waste; ew 0: no fitness effect, the neutral twin).
The waste reads the eater's trait (ecology); the copying and the mutation are as in the parent and never read it.
Parent docstring follows.
 c53's fed-vortex world (20261027T0712-c53-fed-vortex-claim, defaults
unchanged) with c53's two labels (20261027T0845-c53-fed-vortex-selection-claim) replaced by a label density c and a trait
mass z (trait theta = z/c), both advected by the flow, diffusing at Dl and decaying at dl elsewhere:
    dc = -u.grad c + Dl lap c + kl r c (1 - c) - dl c
    dz = -u.grad z + Dl lap z + kl r z (1 - c) - dl z         r = eat / Y (the vortex's own eating rate)
Copying is linear in z with a rate that depends only on c and on eating, so it carries theta unchanged and never reads it;
diffusion, advection and decay act on c and z alike, so theta mixes only by averaging between fluid parcels.
Mutation (trait-blind): every mut_dt one uniform draw picks an eating pixel (raster order) and one draw picks a sign;
theta is shifted by +-dm over the whole vortex there (the periodic connected component of eating pixels containing it,
dilated by 2 px), by z += +-dm c. Neither draw reads c, z or theta, and the sequences depend only on mut_seed.
Fitness effect (written): the vortex gain is k (1 + eps tanh(theta)) (fit "lin": k (1 + eps theta), theta clipped to +-5); eps 0 is the neutral twin, which receives the same draws.
mut_mode "disk" uses c53's 6-px disk instead of the whole vortex.
"""
import json, os
import numpy as np
from labkit import ops
import scipy.ndimage as ndi

META = {
    "name": "fed-vortices",
    "family": "fed-vortex",
    "size": (128, 128),
    "steps_per_frame": 100,
    "dt": 0.02,
    "channels": ["|vorticity|", "fuel Y", "label c", "trait z_1"],
    "matter": [0],
    "threshold": 0.06,
}

P = {"nu": 0.1, "mu": 0.1, "k": 0.5, "wi": 0.1, "kY": 1.0, "e": 10.0, "kF": 0.02, "noise": 0.06, "L": 4.0,
     "dt": 0.02, "fork_t": -1.0, "hyper": 0.005, "Y0": 0.6, "adv": 1.0,
     "lab_t": 300.0, "Dl": 0.02, "kl": 2.0, "dl": 0.05, "eps": 0.0, "mut_dt": -1.0, "mut_r": 6.0, "mut_seed": 1,
     "dm": 0.4, "mut_mode": "vortex", "fit": "tanh",
     "ew": 0.0, "sw": 0.4, "Dw": 1.0, "dw": 0.002, "pw": 0.25, "nt": 3}
P.update(json.loads(os.environ.get("WORLD_P", "{}")))


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    q = dict(P)
    n = ops.fft_conv(rng.standard_normal((H, W)), ops.gauss_kernel(H, W, q["L"]))
    n = n - ops.fft_conv(n, ops.gauss_kernel(H, W, 4 * q["L"]))      # band-pass: no large-scale swirl in the initial noise
    om = q["noise"] * n / n.std()
    Y = q["Y0"] * np.ones((H, W))
    ky, kx = ops.wavenumbers(H, W)
    k2 = kx ** 2 + ky ** 2
    dt = q["dt"]
    kmax = np.abs(ky).max(); kxm = np.abs(kx).max()
    da = ((np.abs(ky) < (2 / 3) * kmax) & (np.abs(kx) < (2 / 3) * kxm)).astype(float)
    inv = np.where(k2 > 0, 1.0 / np.where(k2 > 0, k2, 1), 0.0)
    return {"om": om, "Y": Y, "t": 0.0, "shape": (H, W), "par": q, "kx": kx, "ky": ky, "inv": inv, "da": da,
            "Lom": 1 / (1 + dt * (q["nu"] * k2 + q["hyper"] * k2 ** 2)),
            "LY": 1 / (1 + dt * (q["kY"] * k2 + q["hyper"] * k2 ** 2)), "eat": np.zeros((H, W)), "W": np.zeros((H, W)), "V": np.zeros((q["nt"], H, W)),
            "LW": 1 / (1 + dt * (q["Dw"] * k2 + q["dw"] + q["hyper"] * k2 ** 2)),
            "LL": 1 / (1 + dt * (q["Dl"] * k2 + q["dl"] + q["hyper"] * k2 ** 2)), "c": np.zeros((H, W)), "z": np.zeros((q["nt"], H, W)),
            "mrng": np.random.default_rng(q["mut_seed"])}


def _disk(sh, cy, cx, r):
    H, W = sh; yy, xx = np.ogrid[:H, :W]
    return ((((yy - cy + H / 2) % H - H / 2) ** 2 + ((xx - cx + W / 2) % W - W / 2) ** 2) <= r ** 2).astype(float)


def _vortex_mask(mask, cy, cx):
    """periodic connected component of mask containing (cy, cx), dilated by 2 px"""
    H, W = mask.shape
    lab, n = ndi.label(np.tile(mask, (3, 3)))
    l0 = lab[H + cy, W + cx]
    big = lab == l0
    m = big.reshape(3, H, 3, W).any(axis=(0, 2))
    fp = np.add.outer(np.arange(-2, 3) ** 2, np.arange(-2, 3) ** 2) <= 4
    m = ndi.maximum_filter(m, footprint=fp, mode="wrap")
    return m.astype(float)


def _vel(s):
    oh = ops.rfft2(s["om"]) * s["da"]; ph = oh * s["inv"]; sh = s["shape"]
    return ops.irfft2(-1j * s["kx"] * ph, sh), ops.irfft2(1j * s["ky"] * ph, sh)


def _adv(f, uy, ux, s):
    fh = ops.rfft2(f) * s["da"]; sh = s["shape"]
    a = uy * ops.irfft2(1j * s["ky"] * fh, sh) + ux * ops.irfft2(1j * s["kx"] * fh, sh)
    return ops.irfft2(ops.rfft2(a) * s["da"], sh)


def step(s):
    q, dt, sh = s["par"], s["par"]["dt"], s["shape"]
    om, Y = s["om"], s["Y"]
    kF = q["kF"]
    if q["fork_t"] >= 0 and s["t"] >= q["fork_t"]:
        kF = 0.0
        if abs(s["t"] - q["fork_t"]) < dt / 2:
            Y = 0.0 * Y
    uy, ux = _vel(s)
    uy, ux = q["adv"] * uy, q["adv"] * ux
    w2 = om ** 2
    sat = w2 / (w2 + q["wi"] ** 2)
    eat = np.minimum(q["e"] * Y * sat * w2, Y / dt)
    c, z = s["c"], s["z"]
    if q["lab_t"] >= 0 and abs(s["t"] - q["lab_t"]) < dt / 2:     # every eating vortex starts with theta 0
        c = np.where(eat > 1e-3, 1.0, 0.0); z = np.zeros((q["nt"],) + sh)
    if q["mut_dt"] > 0 and s["t"] > q["lab_t"] and int(round(s["t"] / dt)) % int(round(q["mut_dt"] / dt)) == 0:
        u = s["mrng"].random(); vec = s["mrng"].standard_normal(q["nt"]); vec = vec / np.linalg.norm(vec)
        idx = np.flatnonzero(eat > 1e-3)
        if idx.size:
            kk = idx[int(u * idx.size)]; cy, cx = divmod(kk, sh[1])
            m = _vortex_mask(eat > 1e-3, cy, cx) if q["mut_mode"] == "vortex" else _disk(sh, cy, cx, q["mut_r"])
            z = z + q["dm"] * vec[:, None, None] * (c * m)[None]
            s.setdefault("mutations", []).append((round(s["t"], 2), int(cy), int(cx), 0.0))
    th = z / np.maximum(c, 0.05)[None]
    gain = q["k"]
    Wf, V = s["W"], s["V"]
    if q["ew"] != 0:
        G = np.exp(-((th - V / np.maximum(Wf, 1e-6)[None]) ** 2).sum(0) / (2 * q["sw"] ** 2)) if q["sw"] > 0 else 1.0
        gain = gain + q["k"] * q["ew"] * (1 - Wf / (1 + Wf) * G)   # kind-specific waste (ecological fitness effect)
    nW = Wf + dt * (-_adv(Wf, uy, ux, s) + q["pw"] * eat)
    s["W"] = np.clip(ops.irfft2(ops.rfft2(nW) * s["LW"], sh), 0, None)
    s["V"] = np.stack([ops.irfft2(ops.rfft2(V[i] + dt * (-_adv(V[i], uy, ux, s) + q["pw"] * eat * th[i])) * s["LW"], sh) for i in range(q["nt"])])
    nom = om + dt * (-_adv(om, uy, ux, s) + (gain * Y * sat - q["mu"]) * om)
    rate = eat / np.maximum(Y, 1e-6)              # labels are copied only where the vortex eats
    nc = c + dt * (-_adv(c, uy, ux, s) + q["kl"] * rate * c * (1 - c))
    s["z"] = np.stack([ops.irfft2(ops.rfft2(z[i] + dt * (-_adv(z[i], uy, ux, s) + q["kl"] * rate * z[i] * (1 - c))) * s["LL"], sh) for i in range(q["nt"])])
    s["c"] = np.clip(ops.irfft2(ops.rfft2(nc) * s["LL"], sh), 0, None)
    nY = Y + dt * (-_adv(Y, uy, ux, s) - eat + kF * (1 - Y))
    s["om"] = ops.irfft2(ops.rfft2(nom) * s["Lom"], sh)
    s["Y"] = np.clip(ops.irfft2(ops.rfft2(nY) * s["LY"], sh), 0, None)
    s["eat"] = eat
    s["t"] += dt
    return s


def fields(s):
    return np.stack([np.abs(s["om"]), s["Y"], s["c"], s["z"][0]])
