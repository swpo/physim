"""Flow-Lenia level-0 law (Plantec et al. 2023, arXiv:2212.07906), numpy, periodic box.

State: A, numpy float64 array of shape (C, H, W), non-negative matter per channel.
Law:   A_next = step(A, params[, t]).

One step (paper eqs. 1-7, matched to the reference code erwanplantec/FlowLenia):
  1. affinity  U_j = sum_i h_i * G_i(K_i * A_{c0_i}) [c1_i == j]           (FFT, periodic)
       K_i(D) = sigmoid(-(D-1)*10) * sum_q b_iq exp(-(D - a_iq)^2 / w_iq),
       D = |x| / ((R + 15) r_i), K_i normalised to sum 1,
       G_i(u) = 2 exp(-((u - m_i)/s_i)^2 / 2) - 1
  2. flow      F_c = (1 - alpha) grad U_c - alpha grad A_sum,
       alpha = clip((A_sum / theta_A)^n, 0, 1)     [paper eq. 5; params alpha_src="sum"]
       (the reference code uses A_c instead of A_sum: alpha_src="channel"; same for C = 1)
       gradients by 3x3 Sobel filters (8 x central difference), periodic here
  3. transport reintegration tracking: the mass of every cell p moves as a uniform square of
       side 2*sigma centred on p + clip(dt*F_c(p), -(dd - sigma), dd - sigma) and is split over
       the cells the square overlaps (at most 3x3 for sigma < 1). Every source sends out exactly
       what it holds, so the total mass of every channel is conserved to round-off.

Optional noise (params["noise"] = {"mode", "std", "seed"}), a deterministic function of
(seed, t):
  "flow":     F_c += std * N(0, 1) per cell and axis  (mass still conserved exactly)
  "additive": A_c += std * (N(0,1) - mean) per cell, then clipped at 0 (mass drifts by the clip)

params is a JSON-serialisable dict (see default_params / sample_params). Kernel FFTs are cached
per (params, grid shape); step has no other state.
"""
import json
import numpy as np
import scipy.fft as sfft

_CACHE = {}


# ----------------------------------------------------------------------------- parameters
def conn_from_matrix(M):
    """Reference conn_from_matrix: M[s, t] kernels sense channel s and update channel t."""
    M = np.asarray(M, int)
    C = M.shape[0]
    c0, c1 = [], []
    for s in range(C):
        for t in range(C):
            c0 += [s] * int(M[s, t])
            c1 += [t] * int(M[s, t])
    return c0, c1


def default_params(C=1, k=10):
    return {"C": C, "k": k, "R": 10.0, "r": [0.5] * k, "a": [[0.5, 0.5, 0.5]] * k,
            "b": [[1.0, 0.0, 0.0]] * k, "w": [[0.1, 0.1, 0.1]] * k, "m": [0.15] * k,
            "s": [0.015] * k, "h": [1.0] * k, "c0": [0] * k, "c1": [0] * k,
            "dt": 0.2, "sigma": 0.65, "dd": 5, "n": 2.0, "theta_A": float(C),
            "alpha_src": "sum", "R_scale": 1.0, "noise": {"mode": "none", "std": 0.0, "seed": 0}}


def sample_params(rng, C=2, k=10, M=None, R_scale=1.0):
    """Random rule from the reference priors (FlowLenia.__init__, paper table 1)."""
    p = default_params(C, k)
    p["R"] = float(rng.uniform(2.0, 25.0))
    p["r"] = rng.uniform(0.2, 1.0, k).tolist()
    p["m"] = rng.uniform(0.05, 0.5, k).tolist()
    p["s"] = rng.uniform(0.001, 0.18, k).tolist()
    p["h"] = rng.uniform(0.01, 1.0, k).tolist()
    p["a"] = rng.uniform(0.0, 1.0, (k, 3)).tolist()
    p["b"] = rng.uniform(0.001, 1.0, (k, 3)).tolist()
    p["w"] = rng.uniform(0.01, 0.5, (k, 3)).tolist()
    if M is None:
        M = [[k]] if C == 1 else None
    if M is None:  # random allocation: every channel senses and is updated by >= 1 kernel
        while True:
            M = rng.multinomial(k, np.ones(C * C) / (C * C)).reshape(C, C)
            if (M.sum(0) > 0).all() and (M.sum(1) > 0).all():
                break
    M = np.asarray(M, int)
    assert M.sum() == k
    p["M"] = M.tolist()
    p["c0"], p["c1"] = conn_from_matrix(M)
    p["R_scale"] = float(R_scale)
    return p


# ----------------------------------------------------------------------------- compiled law
def _key(params, shape):
    q = {kk: v for kk, v in params.items() if kk != "noise"}
    return json.dumps(q, sort_keys=True) + str(tuple(shape))


def kernels(params, H, W):
    """Real-space kernels (k, H, W), centred at index (0, 0) (periodic distance)."""
    y = np.minimum(np.arange(H), H - np.arange(H))[:, None].astype(float)
    x = np.minimum(np.arange(W), W - np.arange(W))[None, :].astype(float)
    dist = np.sqrt(x ** 2 + y ** 2)
    R = params["R"]
    Ks = []
    for i in range(params["k"]):
        D = dist / ((R + 15.0) * params["r"][i] * params.get("R_scale", 1.0))
        sig = 0.5 * (np.tanh(-(D - 1.0) * 10.0 / 2.0) + 1.0)
        a, b, w = (np.asarray(params[q][i])[None, None, :] for q in "abw")
        K = sig * (b * np.exp(-(D[..., None] - a) ** 2 / w)).sum(-1)
        Ks.append(K / K.sum())
    return np.stack(Ks)


def compile_params(params, shape):
    key = _key(params, shape)
    cp = _CACHE.get(key)
    if cp is not None:
        return cp
    C, H, W = shape
    k = params["k"]
    c1 = np.asarray(params["c1"], int)
    M1 = np.zeros((C, k))
    M1[c1, np.arange(k)] = 1.0
    sig = params["sigma"]
    cp = {
        "fK": sfft.rfft2(kernels(params, H, W), axes=(-2, -1)),
        "c0": np.asarray(params["c0"], int), "M1": M1,
        "m": np.asarray(params["m"])[:, None, None], "s": np.asarray(params["s"])[:, None, None],
        "h": np.asarray(params["h"])[:, None, None],
        "ma": params["dd"] - sig, "P": int(params["dd"]) + 1,
    }
    P = cp["P"]
    assert sig <= 1.0 and P <= min(H, W)
    cp["iyy"] = np.arange(H, dtype=np.intp)[:, None] + P
    cp["ixx"] = np.arange(W, dtype=np.intp)[None, :] + P
    cp["pbase"] = (np.arange(C, dtype=np.intp) * (H + 2 * P) * (W + 2 * P))[:, None, None]
    if len(_CACHE) > 64:
        _CACHE.clear()
    _CACHE[key] = cp
    return cp


# ----------------------------------------------------------------------------- operators
def sobel(X):
    """(..., H, W) -> (d/dy, d/dx), periodic Sobel (equals the reference convolve2d filters
    kx = [[1,0,-1],[2,0,-2],[1,0,-1]], ky = kx.T in the interior; 8 x central difference)."""
    sy = np.roll(X, -1, -2) - np.roll(X, 1, -2)
    gy = 2.0 * sy + np.roll(sy, 1, -1) + np.roll(sy, -1, -1)
    sx = np.roll(X, -1, -1) - np.roll(X, 1, -1)
    gx = 2.0 * sx + np.roll(sx, 1, -2) + np.roll(sx, -1, -2)
    return gy, gx


def affinity(A, params):
    """U (C, H, W): sum of h_i G_i(K_i * A_c0i) into channel c1_i."""
    C, H, W = A.shape
    cp = compile_params(params, A.shape)
    fA = sfft.rfft2(A, axes=(-2, -1))
    Uk = sfft.irfft2(fA[cp["c0"]] * cp["fK"], s=(H, W), axes=(-2, -1))
    G = (2.0 * np.exp(-0.5 * ((Uk - cp["m"]) / cp["s"]) ** 2) - 1.0) * cp["h"]
    return (cp["M1"] @ G.reshape(G.shape[0], -1)).reshape(C, H, W)


def flow(A, params, U=None):
    if U is None:
        U = affinity(A, params)
    gUy, gUx = sobel(U)
    gAy, gAx = sobel(A.sum(0))
    src = A.sum(0, keepdims=True) if params.get("alpha_src", "sum") == "sum" else A
    alpha = np.clip((src / params["theta_A"]) ** params["n"], 0.0, 1.0)
    return gUy * (1.0 - alpha) - gAy * alpha, gUx * (1.0 - alpha) - gAx * alpha


def reintegrate(A, Fy, Fx, params):
    """Reintegration tracking on the torus (exact for sigma <= 1: a 2*sigma square touches at
    most 3 cells per axis). Cells are unit squares centred on integer positions. The scatter goes
    into a grid padded by P = dd + 1 cells, whose margins are then folded back (periodic wrap)."""
    C, H, W = A.shape
    cp = compile_params(params, A.shape)
    sig, dt, ma, P = params["sigma"], params["dt"], cp["ma"], cp["P"]
    Hp, Wp = H + 2 * P, W + 2 * P
    dy = np.clip(dt * Fy, -ma, ma)                 # displacement of each source's square
    dx = np.clip(dt * Fx, -ma, ma)
    ry, rx = np.rint(dy), np.rint(dx)
    fy, fx = dy - ry, dx - rx                      # in [-0.5, 0.5]
    # overlap of [f - sigma, f + sigma] with the cells [o - 0.5, o + 0.5], o = -1, 0, 1
    wy = [np.clip(np.minimum(o + 0.5, fy + sig) - np.maximum(o - 0.5, fy - sig), 0, None) for o in (-1, 0, 1)]
    wx = [np.clip(np.minimum(o + 0.5, fx + sig) - np.maximum(o - 0.5, fx - sig), 0, None) for o in (-1, 0, 1)]
    # weights sum to (2 sigma)^2 analytically; dividing by the computed sum makes every source
    # send out exactly what it holds (to round-off)
    An = A / ((wy[0] + wy[1] + wy[2]) * (wx[0] + wx[1] + wx[2]))
    base = cp["pbase"] + (ry.astype(np.intp) + cp["iyy"]) * Wp + (rx.astype(np.intp) + cp["ixx"])
    Aw = np.empty((3, 3) + A.shape)
    idx = np.empty((3, 3) + A.shape, np.intp)
    for i, o in enumerate((-1, 0, 1)):
        t = An * wy[i]
        for j, o2 in enumerate((-1, 0, 1)):
            np.multiply(t, wx[j], out=Aw[i, j])
            np.add(base, o * Wp + o2, out=idx[i, j])
    out = np.bincount(idx.ravel(), Aw.ravel(), minlength=C * Hp * Wp).reshape(C, Hp, Wp)
    out[:, P:2 * P, :] += out[:, H + P:, :]
    out[:, H:H + P, :] += out[:, :P, :]
    out[:, :, P:2 * P] += out[:, :, W + P:]
    out[:, :, W:W + P] += out[:, :, :P]
    return np.ascontiguousarray(out[:, P:H + P, P:W + P])


def step(A, params, t=0):
    """One Flow-Lenia update A(t) -> A(t + dt). Pure: noise (if any) depends on (seed, t)."""
    Fy, Fx = flow(A, params)
    nz = params.get("noise") or {}
    mode, std = nz.get("mode", "none"), float(nz.get("std", 0.0))
    if std > 0 and mode == "flow":
        g = np.random.default_rng([int(nz.get("seed", 0)), int(t), 1])
        Fy = Fy + std * g.standard_normal(Fy.shape)
        Fx = Fx + std * g.standard_normal(Fx.shape)
    A = reintegrate(A, Fy, Fx, params)
    if std > 0 and mode == "additive":
        g = np.random.default_rng([int(nz.get("seed", 0)), int(t), 2])
        xi = g.standard_normal(A.shape)
        xi -= xi.mean(axis=(-2, -1), keepdims=True)
        A = np.clip(A + std * xi, 0.0, None)
    return A


def run(A, params, steps, t0=0, every=0, callback=None):
    for t in range(t0, t0 + steps):
        A = step(A, params, t)
        if every and callback is not None and (t + 1) % every == 0:
            callback(t + 1, A)
    return A


# ----------------------------------------------------------------------------- initial states
def init_patches(seed, C, H, W, n_patches=4, L=24, amp=1.0, min_sep=None):
    """n_patches LxL patches of U(0, amp) matter per channel at random (non-overlapping when
    possible) positions; deterministic given seed."""
    rng = np.random.default_rng(seed)
    A = np.zeros((C, H, W))
    centres = []
    min_sep = L * 1.2 if min_sep is None else min_sep
    for j in range(n_patches):
        for _ in range(200):
            cy, cx = rng.integers(0, H), rng.integers(0, W)
            ok = all(min(abs(cy - y), H - abs(cy - y)) ** 2 + min(abs(cx - x), W - abs(cx - x)) ** 2
                     >= min_sep ** 2 for y, x in centres)
            if ok:
                break
        centres.append((cy, cx))
        ys = (np.arange(L) + cy - L // 2) % H
        xs = (np.arange(L) + cx - L // 2) % W
        A[:, ys[:, None], xs[None, :]] = rng.uniform(0, amp, (C, L, L))
    return A
