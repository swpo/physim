"""c53: fed vortices with a heritable label (20261027T0712-c53-fed-vortex-claim plus labels a, b carried by the vortex fluid,
copied only where the vortex eats, decaying elsewhere; trait-blind mutation swaps a and b in a disk at a random eating pixel;
the label scales the vortex gain by (1 + eps b): the ancestral kind a keeps the base gain). A 2D incompressible fluid with no gravity and no imposed direction, in which vorticity is the body
and grows only where it eats a fuel that diffuses and regrows.

Vorticity-streamfunction form on a periodic box:
    d omega = -u.grad omega + nu lap omega + (k Y s - mu) omega          s = omega^2 / (omega^2 + wi^2)
    d Y     = -u.grad Y + kY lap Y - e Y s omega^2 + kF (1 - Y)
    u = (dpsi/dy, -dpsi/dx),  lap psi = -omega
Weak vorticity decays at mu; strong vorticity grows where fuel is present and eats it (bistable, ignition-like).
Nothing marks a body or a direction. Switches: Y0 (initial uniform fuel level); adv 0 (no flow: the same reaction-diffusion with advection off, the
Laplacian-only twin); fork_t (fuel emptied at fork_t, regrowth off).
"""
import json, os
import numpy as np
from labkit import ops

META = {
    "name": "fed-vortices",
    "family": "fed-vortex",
    "size": (128, 128),
    "steps_per_frame": 100,
    "dt": 0.02,
    "channels": ["|vorticity|", "fuel Y", "label a", "label b"],
    "matter": [0],
    "threshold": 0.06,
}

P = {"nu": 0.1, "mu": 0.1, "k": 0.5, "wi": 0.1, "kY": 1.0, "e": 10.0, "kF": 0.02, "noise": 0.06, "L": 4.0,
     "dt": 0.02, "fork_t": -1.0, "hyper": 0.005, "Y0": 0.6, "adv": 1.0,
     "lab_t": 300.0, "Dl": 0.02, "kl": 2.0, "dl": 0.05, "eps": 0.0, "mut_dt": -1.0, "mut_r": 6.0, "mut_seed": 1}
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
            "LY": 1 / (1 + dt * (q["kY"] * k2 + q["hyper"] * k2 ** 2)), "eat": np.zeros((H, W)),
            "LL": 1 / (1 + dt * (q["Dl"] * k2 + q["dl"] + q["hyper"] * k2 ** 2)), "a": np.zeros((H, W)), "b": np.zeros((H, W)),
            "mrng": np.random.default_rng(q["mut_seed"])}


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
    a, b = s["a"], s["b"]
    if q["lab_t"] >= 0 and abs(s["t"] - q["lab_t"]) < dt / 2:     # every eating vortex starts as kind a
        a = np.where(eat > 1e-3, 1.0, 0.0); b = np.zeros(sh)
    if q["mut_dt"] > 0 and s["t"] > q["lab_t"] and int(round(s["t"] / dt)) % int(round(q["mut_dt"] / dt)) == 0:
        # trait-blind mutation: one uniform draw picks an eating pixel (raster order) and a, b are swapped in a disk there;
        # the draw sequence depends only on mut_seed, never on the labels
        u = s["mrng"].random(); idx = np.flatnonzero(eat > 1e-3)
        if idx.size:
            kk = idx[int(u * idx.size)]; cy, cx = divmod(kk, sh[1]); H, W = sh
            yy, xx = np.ogrid[:H, :W]; d2 = ((yy - cy + H / 2) % H - H / 2) ** 2 + ((xx - cx + W / 2) % W - W / 2) ** 2
            m = d2 <= q["mut_r"] ** 2; a, b = np.where(m, b, a), np.where(m, a, b)
            s.setdefault("mutations", []).append((round(s["t"], 2), int(cy), int(cx)))
    gain = q["k"] * (1 + q["eps"] * b)            # kind b's gain per unit fuel differs by eps (written fitness effect);
                                                  # the ancestral kind a has the base world's gain
    nom = om + dt * (-_adv(om, uy, ux, s) + (gain * Y * sat - q["mu"]) * om)
    rate = eat / np.maximum(Y, 1e-6)              # labels are copied only where the vortex eats
    na = a + dt * (-_adv(a, uy, ux, s) + q["kl"] * rate * a * (1 - a - b))
    nb = b + dt * (-_adv(b, uy, ux, s) + q["kl"] * rate * b * (1 - a - b))
    s["a"] = np.clip(ops.irfft2(ops.rfft2(na) * s["LL"], sh), 0, None)
    s["b"] = np.clip(ops.irfft2(ops.rfft2(nb) * s["LL"], sh), 0, None)
    nY = Y + dt * (-_adv(Y, uy, ux, s) - eat + kF * (1 - Y))
    s["om"] = ops.irfft2(ops.rfft2(nom) * s["Lom"], sh)
    s["Y"] = np.clip(ops.irfft2(ops.rfft2(nY) * s["LY"], sh), 0, None)
    s["eat"] = eat
    s["t"] += dt
    return s


def fields(s):
    return np.stack([np.abs(s["om"]), s["Y"], s["a"], s["b"]])
