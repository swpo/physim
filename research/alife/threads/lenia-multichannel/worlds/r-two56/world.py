"""Random multi-channel Lenia rule from screen two_s0.json (family 'two', rule 56).

2 channels, 6 kernels, R=10. Spontaneous: starts from uniform noise in a patch covering 60% of the grid side (no planted creature)."""
# ---- multi-channel Lenia engine (Chan 2020 update rule; copied into each world) ----
import numpy as np
import scipy.fft as sfft
from fractions import Fraction


def _rfft2(x):
    return sfft.rfft2(x, axes=(-2, -1), workers=2)


def _irfft2(X, shape):
    return sfft.irfft2(X, s=shape, axes=(-2, -1), workers=2)


def _radial(H, W):
    y = np.minimum(np.arange(H), H - np.arange(H))[:, None]
    x = np.minimum(np.arange(W), W - np.arange(W))[None, :]
    return np.sqrt(x ** 2 + y ** 2)


def _kernel_fft(H, W, R, k):
    """Chan's shell kernel: B rings with peaks b inside radius r*R, quad4 core."""
    D = _radial(H, W) / R
    r = k.get("r", 1.0)
    bs = np.asarray([float(Fraction(x)) for x in str(k["b"]).split(",")])
    Br = len(bs) * D / r
    b = bs[np.minimum(np.floor(Br).astype(int), len(bs) - 1)]
    K = (D < r) * (4 * (Br % 1) * (1 - Br % 1)) ** 4 * b
    return _rfft2(K / K.sum())


def _growth(U, m, s):
    return np.maximum(0, 1 - (U - m) ** 2 / (9 * s ** 2)) ** 4 * 2 - 1


def _ch2val(c):
    if c in ".b":
        return 0
    if c == "o":
        return 255
    if len(c) == 1:
        return ord(c) - ord("A") + 1
    return (ord(c[0]) - ord("p")) * 24 + (ord(c[1]) - ord("A") + 25)


def _rle2arr(st):
    rows, row, last, count = [], [], "", ""
    for ch in st.rstrip("!") + "$":
        if ch.isdigit():
            count += ch
        elif ch in "pqrstuvwxy@":
            last = ch
        else:
            if ch == "$" and last == "":
                rows.append(row)
                rows.extend([] for _ in range(int(count or 1) - 1))
                row = []
            else:
                row.extend([_ch2val(last + ch) / 255] * int(count or 1))
            last, count = "", ""
    w = max(len(r) for r in rows)
    return np.array([r + [0] * (w - len(r)) for r in rows])


def _creature(cells):
    arrs = [_rle2arr(c) for c in cells]
    h, w = max(a.shape[0] for a in arrs), max(a.shape[1] for a in arrs)
    out = np.zeros((len(arrs), h, w))
    for i, a in enumerate(arrs):
        out[i, :a.shape[0], :a.shape[1]] = a
    return out


class Lenia:
    def __init__(self, rule, C, size, R, T):
        H, W = size
        self.shape, self.C, self.dt = (H, W), C, 1.0 / T
        self.Kf = np.stack([_kernel_fft(H, W, R, k) for k in rule])
        self.src = np.array([k["c"][0] for k in rule])
        self.dst = np.array([k["c"][1] for k in rule])
        self.m = np.array([k["m"] for k in rule])[:, None, None]
        self.s = np.array([k["s"] for k in rule])[:, None, None]
        self.h = np.array([k.get("h", 1.0) for k in rule])
        hs = np.array([self.h[self.dst == c].sum() for c in range(C)])
        self.w = self.h / np.maximum(hs[self.dst], 1e-12)   # per-kernel weight into its target

    def growth(self, A):
        """Per-channel growth rate in [-1, 1] (before dt)."""
        U = _irfft2(_rfft2(A)[self.src] * self.Kf, self.shape)
        G = _growth(U, self.m, self.s) * self.w[:, None, None]
        D = np.zeros_like(A)
        np.add.at(D, self.dst, G)
        return D
# ---- end engine ----


from labkit import ops  # noqa: E402  (only for disk masks in damage)

META = {
    "name": "r-two56",
    "family": "lenia",
    "parent": 'screen:two#56',
    "mutation": "random 'two' channel/kernel graph",
    "size": (192, 192),
    "steps_per_frame": 5,
    "dt": 0.1,
    "channels": ["A0", "A1", "A2"][:2] + (["F"] if None else []),
    "matter": list(range(2)),
}

R, T = 10, 10
RULE = [
    {"b": "12/12", "m": 0.1523, "s": 0.0215, "h": 0.413, "r": 0.591, "c": [0, 0]},
    {"b": "8/12,9/12,12/12", "m": 0.4705, "s": 0.0955, "h": 0.917, "r": 0.717, "c": [0, 0]},
    {"b": "12/12", "m": 0.3056, "s": 0.0825, "h": 0.756, "r": 0.606, "c": [1, 1]},
    {"b": "12/12,5/12", "m": 0.3533, "s": 0.0989, "h": 0.436, "r": 0.852, "c": [1, 1]},
    {"b": "7/12,5/12,12/12", "m": 0.2344, "s": 0.0616, "h": 0.975, "r": 0.861, "c": [0, 1]},
    {"b": "12/12", "m": 0.4993, "s": 0.1726, "h": 0.685, "r": 0.843, "c": [1, 0]},
]
CELLS = None
N_SEED = 0
C = 2
NOISE = 0.6
# Optional metabolism: food field F (diffusing with D, regrowing at rate rho toward Fmax).
#  mode "conserve": matter can only be built from local food (yield Y); see step().
#  otherwise ("gate"): positive growth multiplied by F^gate, eating at eat*mass*F, starving at starve*(1-F).
FOOD = None


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    if CELLS is None:   # spontaneous: random noise in a square patch covering NOISE of the grid side
        A = np.zeros((C, H, W))
        p = int(NOISE * min(H, W))
        A[:, :p, :p] = rng.random((C, p, p))
        A = np.roll(A, (int(rng.integers(H)), int(rng.integers(W))), (1, 2))
        return _finish(A, size)
    cr = _creature(CELLS)
    A = np.zeros((len(CELLS), H, W))
    h, w = cr.shape[1:]
    placed = []
    for _ in range(N_SEED):
        for _try in range(50):
            y, x = int(rng.integers(0, H)), int(rng.integers(0, W))
            if all(min(abs(y - py), H - abs(y - py)) > max(h, w) * 1.2 or
                   min(abs(x - px), W - abs(x - px)) > max(h, w) * 1.2 for py, px in placed):
                break
        placed.append((y, x))
        c = np.rot90(cr, int(rng.integers(4)), axes=(1, 2))
        A = np.maximum(A, np.roll(np.pad(c, ((0, 0), (0, H - c.shape[1]), (0, W - c.shape[2]))), (y, x), (1, 2)))
    return _finish(A, size)


def _finish(A, size):
    H, W = size
    st = {"A": A, "L": Lenia(RULE, C, size, R, T)}
    if FOOD:
        st["F"] = np.full((H, W), FOOD.get("F0", 1.0))
        ky = 2 * np.pi * np.fft.fftfreq(H)[:, None]
        kx = 2 * np.pi * np.fft.rfftfreq(W)[None, :]
        st["lapK"] = -(kx ** 2 + ky ** 2)
    return st


def step(s):
    L, A = s["L"], s["A"]
    G = L.growth(A)
    if FOOD and FOOD.get("mode") == "conserve":
        # matter is built from food: positive growth is capped by the local food F (yield Y),
        # food spent = matter built / Y; decay just dissipates. Behaviour is unchanged where F is plentiful.
        F = s["F"]
        inc = np.clip(np.minimum(L.dt * G, 1 - A), 0, None)
        dec = np.clip(L.dt * G, None, 0)
        need = inc.sum(0) / FOOD["Y"]
        scale = np.minimum(1, F / np.maximum(need, 1e-12))
        A_new = np.clip(A + inc * scale + dec, 0, 1)
        F = F - need * scale + L.dt * FOOD["rho"] * (FOOD.get("Fmax", 1.0) - F)
        if FOOD["D"] > 0:   # implicit spectral diffusion
            F = _irfft2(_rfft2(F) / (1 - L.dt * FOOD["D"] * s["lapK"]), F.shape)
        s["F"] = np.clip(F, 0, None)
        s["A"] = A_new
    elif FOOD:
        F = s["F"]
        G = np.where(G > 0, G * F ** FOOD["gate"], G) - FOOD["starve"] * (1 - F) * A
        A_new = np.clip(A + L.dt * G, 0, 1)
        mass = A_new.sum(0)
        dF = FOOD["rho"] * (1 - F) - FOOD["eat"] * mass * F
        F = F + L.dt * dF
        if FOOD["D"] > 0:   # implicit spectral diffusion
            F = _irfft2(_rfft2(F) / (1 - L.dt * FOOD["D"] * s["lapK"]), F.shape)
        s["F"] = np.clip(F, 0, 1)
        s["A"] = A_new
    else:
        s["A"] = np.clip(A + L.dt * G, 0, 1)
    return s


def fields(s):
    return np.concatenate([s["A"], s["F"][None]]) if FOOD else s["A"]


def damage(s, mask):
    s["A"][:, mask] = 0
    return s
