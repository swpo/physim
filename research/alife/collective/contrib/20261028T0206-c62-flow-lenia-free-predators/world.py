"""c62: Flow-Lenia ecology of two conserved matters, both "drive, not build" (c18's fl_drive).

Prey matter A (2 channels, c18's rule 202 gliders): never made or destroyed by food; the gain of its growth field is
phi/(phi + K_drive), where food phi is consumed where prey matter is and regrows (c18's 20261025T1926-c18-fl-drive-sighting).
Predator matter B (2 channels, same kernels and rule): never made from prey; the gain of its growth field is q/(q + K_q),
where q is a digestion product made only where predator matter overlaps prey matter:
    dig = k_dig * A_sum * B_sum            (prey matter digested into waste w, in proportion to its channels)
    dq  = D_q lap q + k_q_yield * dig - k_qd q
    dw  = D_w lap w + dig - g_w w, and g_w w is returned to prey matter (both channels), so prey matter is conserved
          in A + w; predator matter is conserved exactly.
Each matter moves by its own Flow-Lenia velocity (its own growth gradient and its own density repulsion); the two do not
exclude each other. Switches: pred_on 0 (predator-free twin), kq_zero (q yield 0: eating kept, no product; the L4c arm),
qcut_* (yield 0 in a disk), bgA/bgB dilute backgrounds (bodies recruit them), init "patches" n patches of each kind or
"noise" (whole-domain noise of both matters).
"""
import json
import os
import numpy as np
import scipy.fft as sfft

META = {
    "name": "flow-lenia-digestion-ecology",
    "family": "flow-lenia",
    "parent": "collective/contrib/20261025T1932-c18-fl-drive-bg-sighting",
    "mutation": "a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter",
    "size": (128, 128),
    "steps_per_frame": 25,
    "dt": 0.2,
    "channels": ["prey A", "predator B", "food", "digestion q"],
    "matter": [0, 1],
    "smooth": 1.0, "threshold": 0.15,
    "species": {"prey": [0], "predator": [1]},
}

CFG = {
    "k": 10, "rule_seed": 202, "dd": 5, "dt": 0.2, "sigma": 0.65, "n": 2, "theta": 2.0, "R_scale": 0.4,
    "K_drive": 0.3, "k_cons": 0.02, "rho_f": 0.01, "phi0": 1.0, "D_food": 0.2,
    "bgA": 0.02, "bgB": 0.02, "init": "patches", "n_patches": 3, "patch": 12, "noise_amp": 0.3,
    "pred_on": 1, "t_pred": 100.0, "k_dig": 0.02, "k_qy": 1.0, "k_qd": 0.05, "D_q": 0.2, "K_q": 0.3,
    "D_w": 0.2, "g_w": 0.01, "qcut_t": -1.0, "qcut_r": 0.0, "qcut_y": 0.0, "qcut_x": 0.0,
}
CFG.update(json.loads(os.environ.get("WORLD_P", "{}")))
WORKERS = 2


def rfft2(x):
    return sfft.rfft2(x, axes=(-2, -1), workers=WORKERS)


def irfft2(X, shape):
    return sfft.irfft2(X, s=shape, axes=(-2, -1), workers=WORKERS)


def random_rule(rng, C, k):
    rule = {"R": rng.uniform(2, 25), "r": rng.uniform(0.2, 1, k),
            "m": rng.uniform(0.05, 0.5, k), "s": rng.uniform(0.001, 0.18, k), "h": rng.uniform(0.01, 1, k),
            "a": rng.uniform(0, 1, (k, 3)), "b": rng.uniform(0.001, 1, (k, 3)), "w": rng.uniform(0.01, 0.5, (k, 3))}
    rule["c0"] = rng.integers(0, C, k); rule["c1"] = rng.integers(0, C, k)
    return rule


def kernels_fft(H, W, rule, R_scale):
    y = np.minimum(np.arange(H), H - np.arange(H))[:, None]
    x = np.minimum(np.arange(W), W - np.arange(W))[None, :]
    dist = np.sqrt(x ** 2 + y ** 2)
    Ks = []
    for i in range(len(rule["r"])):
        D = dist / ((rule["R"] + 15) * rule["r"][i] * R_scale)
        sig = 0.5 * (np.tanh(-(D - 1) * 10 / 2) + 1)
        kf = (rule["b"][i] * np.exp(-(D[..., None] - rule["a"][i]) ** 2 / rule["w"][i])).sum(-1)
        K = sig * kf
        Ks.append(K / K.sum())
    return rfft2(np.stack(Ks))


def sobel(A):
    sy = np.roll(A, -1, -2) - np.roll(A, 1, -2)
    gy = 2 * sy + np.roll(sy, 1, -1) + np.roll(sy, -1, -1)
    sx = np.roll(A, -1, -1) - np.roll(A, 1, -1)
    gx = 2 * sx + np.roll(sx, 1, -2) + np.roll(sx, -1, -2)
    return gy, gx


def rt_move(A, Fy, Fx):
    """Reintegration tracking (c18): move every cell's mass as a 2 sigma square to x + dt F; mass conserved."""
    C, H, W = A.shape
    dt, dd, sigma = CFG["dt"], CFG["dd"], CFG["sigma"]
    ma = dd - sigma
    yy, xx = np.mgrid[0:H, 0:W]
    out = np.zeros((C, H * W))
    for c in range(C):
        my = yy + np.clip(dt * Fy[c], -ma, ma); mx = xx + np.clip(dt * Fx[c], -ma, ma)
        ry, rx = np.round(my), np.round(mx)
        for oy in (-1, 0, 1):
            ty = ry + oy
            wy = np.clip(np.minimum(ty + 0.5, my + sigma) - np.maximum(ty - 0.5, my - sigma), 0, None)
            for ox in (-1, 0, 1):
                tx = rx + ox
                wx = np.clip(np.minimum(tx + 0.5, mx + sigma) - np.maximum(tx - 0.5, mx - sigma), 0, None)
                idx = ((ty.astype(int) % H) * W + (tx.astype(int) % W)).ravel()
                out[c] += np.bincount(idx, (wy * wx / (4 * sigma * sigma) * A[c]).ravel(), H * W)
    return out.reshape(C, H, W)


def _patches(rng, H, W, n, L):
    A = np.zeros((2, H, W))
    for j in range(n):
        y0, x0 = rng.integers(0, H), rng.integers(0, W)
        ys = (np.arange(L) + y0) % H; xs = (np.arange(L) + x0) % W
        A[:, ys[:, None], xs[None, :]] = rng.uniform(0, 1, (2, L, L))
    return A


def init(seed, size):
    H, W = size
    rng = np.random.default_rng(seed)
    rule = random_rule(np.random.default_rng(CFG["rule_seed"]), 2, CFG["k"])
    Kf = kernels_fft(H, W, rule, CFG["R_scale"])
    if CFG["init"] == "noise":
        A = CFG["noise_amp"] * rng.uniform(0, 1, (2, H, W)) ** 4
        B = CFG["noise_amp"] * rng.uniform(0, 1, (2, H, W)) ** 4
    else:
        A = _patches(rng, H, W, CFG["n_patches"], CFG["patch"])
        B = _patches(rng, H, W, CFG["n_patches"], CFG["patch"])
    A = A + CFG["bgA"] * (1 + 0.1 * rng.standard_normal(A.shape)).clip(0)
    B = B + CFG["bgB"] * (1 + 0.1 * rng.standard_normal(B.shape)).clip(0)
    yy, xx = np.mgrid[0:H, 0:W]
    return {"A": A, "Bstore": B, "B": np.zeros_like(B), "phi": np.full((H, W), CFG["phi0"]), "q": np.zeros((H, W)),
            "w": np.zeros((H, W)), "Kf": Kf, "rule": rule, "t": 0, "yy": yy, "xx": xx}


def _U(X, s, gain):
    rule = s["rule"]; C, H, W = X.shape
    Uk = irfft2(rfft2(X)[rule["c0"]] * s["Kf"], (H, W))
    G = (2 * np.exp(-((Uk - rule["m"][:, None, None]) / rule["s"][:, None, None]) ** 2 / 2) - 1) * rule["h"][:, None, None]
    U = np.zeros((C, H, W)); np.add.at(U, rule["c1"], G)
    return U * gain[None]


def _vel(X, U):
    gUy, gUx = sobel(U); gXy, gXx = sobel(X.sum(0))
    al = np.clip((X / CFG["theta"]) ** CFG["n"], 0, 1)
    return gUy * (1 - al) - gXy * al, gUx * (1 - al) - gXx * al


def _lap(f):
    return np.roll(f, 1, 0) + np.roll(f, -1, 0) + np.roll(f, 1, 1) + np.roll(f, -1, 1) - 4 * f


def step(s):
    tt = s["t"] * CFG["dt"]
    if CFG["pred_on"] and abs(tt - CFG["t_pred"]) < CFG["dt"] / 2:
        s["B"] = s["Bstore"]
    A, B, phi = s["A"], s["B"], s["phi"]
    UA = _U(A, s, phi / (phi + CFG["K_drive"]))
    Fy, Fx = _vel(A, UA); s["A"] = rt_move(A, Fy, Fx)
    if CFG["pred_on"] and tt >= CFG["t_pred"] - CFG["dt"] / 2:
        q = s["q"]
        UB = _U(B, s, q / (q + CFG["K_q"]))
        Fy, Fx = _vel(B, UB); s["B"] = rt_move(B, Fy, Fx)
    A, B = s["A"], s["B"]
    As, Bs = A.sum(0), B.sum(0)
    # food (prey's resource)
    phi = phi - CFG["k_cons"] * phi * As + CFG["rho_f"] * (CFG["phi0"] - phi)
    s["phi"] = np.clip(phi + CFG["D_food"] * _lap(phi), 0, None)
    # digestion (predator's resource): prey matter -> waste; q made at yield k_qy
    dig = np.minimum(CFG["k_dig"] * As * Bs, 0.5 * As)
    frac = A / np.maximum(As, 1e-12)
    ret = CFG["g_w"] * s["w"]
    s["A"] = A - dig[None] * frac + 0.5 * ret[None]
    s["w"] = s["w"] + dig - ret + CFG["D_w"] * _lap(s["w"])
    ky = CFG["k_qy"]
    if CFG["qcut_t"] >= 0 and tt >= CFG["qcut_t"]:
        H, W = As.shape
        dy = (s["yy"] - CFG["qcut_y"] + H / 2) % H - H / 2; dx = (s["xx"] - CFG["qcut_x"] + W / 2) % W - W / 2
        ky = ky * ((dy * dy + dx * dx) > CFG["qcut_r"] ** 2)
    s["q"] = np.clip(s["q"] + ky * dig - CFG["k_qd"] * s["q"] + CFG["D_q"] * _lap(s["q"]), 0, None)
    s["t"] += 1
    return s


def fields(s):
    return np.stack([s["A"].sum(0), s["B"].sum(0), s["phi"], s["q"]])


def damage(s, mask):
    s["A"][:, mask] = 0
    return s
