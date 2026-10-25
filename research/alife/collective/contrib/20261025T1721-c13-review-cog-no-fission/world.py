"""lcn-cog: the unmodified r-two56 rule (2-channel random Lenia, spontaneous shelled cogs; lab 1 L3 high) on a
CLOSED food-waste cycle.

Every unit of matter A0+A1 is built from local food F at yield Y; every unit lost (the Lenia growth function's
own negative growth, maintenance decay 0.002) becomes waste W at that pixel. Build and loss are charged GROSS
in each step (decay that is rebuilt in the same step costs food and makes waste), unlike the parent lcn world,
which charged only each pixel's net change; W regrows into food at
rate kr and diffuses. N = sum(A)/Y + sum(F) + sum(W) is conserved to round-off (asserted every 100 steps).
No refill, no sink. Starts from uniform noise over the whole domain (S).
Optional: P["beta"] gates food diffusion by the shell A1 (not used, 0); P["h0"] scales the core self-kernel k0
(1.0 = r-two56); P["T"] sets dt = 1/T (10 = lab convention; 20 = dt/2 check); P["k4"] scales the core->shell
kernel k4, the shell's source (0 = shell-source ablation).
Fork tests set s["_mask"] and P["starve_disk"]: food inside the disk is moved out every step (kept in the ledger)."""
import json
import os
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

P = {"Y": 2.0, "D": 1.0, "DW": 1.0, "kr": 0.02, "beta": 0.0, "decay": 0.002, "F0": 1.0, "amp": 1.0, "dens": 1.0,
     "starve_disk": None, "h0": 1.0, "T": 10, "k4": 1.0, "R": 10, "mod": None, "N": None}
P.update(json.loads(os.environ.get("WORLD_P", "{}")))  # screening override only; packs use the defaults above

META = {
    "name": "lcn-cog",
    "family": "lenia",
    "parent": "threads/lenia-multichannel/worlds/rf-two56-mu0.01",
    "mutation": "unmodified r-two56 kernels on a closed food-waste cycle (losses become waste that regrows into food, no refill), full-domain noise",
    "size": (P["N"] or int(round(192 * P["R"] / 10)),) * 2,
    "steps_per_frame": int(P["T"]),
    "dt": 1.0 / P["T"],
    "channels": ["A0", "A1", "F", "W"],
    "matter": [0, 1],
    "radial_channels": [0, 1, 2, 3],
}

R, T = int(P["R"]), int(P["T"])
_SC = (R / 10.0) ** 2   # diffusivities in px^2/t scale with the kernel radius so bodies keep their size in physical units
RULE = [
    {"b": "12/12", "m": 0.1523, "s": 0.0215, "h": 0.413, "r": 0.591, "c": [0, 0]},
    {"b": "8/12,9/12,12/12", "m": 0.4705, "s": 0.0955, "h": 0.917, "r": 0.717, "c": [0, 0]},
    {"b": "12/12", "m": 0.3056, "s": 0.0825, "h": 0.756, "r": 0.606, "c": [1, 1]},
    {"b": "12/12,5/12", "m": 0.3533, "s": 0.0989, "h": 0.436, "r": 0.852, "c": [1, 1]},
    {"b": "7/12,5/12,12/12", "m": 0.2344, "s": 0.0616, "h": 0.975, "r": 0.861, "c": [0, 1]},
    {"b": "12/12", "m": 0.4993, "s": 0.1726, "h": 0.685, "r": 0.843, "c": [1, 0]},
]
C = 2
RULE[0]["h"] = RULE[0]["h"] * P["h0"]   # weight of the narrow core self-kernel k0 (the size limiter)
RULE[4]["h"] = RULE[4]["h"] * P["k4"]
if P["mod"]:   # screening: [[kernel, "m"|"s"|"h", factor], ...]
    for _k, _f, _x in P["mod"]:
        RULE[_k][_f] = RULE[_k][_f] * _x
RULE[4]["h"] = RULE[4]["h"]   # core->shell set-point kernel k4 (the shell's source); 0 = B ablation


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    A = P["amp"] * rng.random((C, H, W)) * (rng.random((1, H, W)) < P["dens"])
    F = np.full((H, W), float(P["F0"]))
    s = {"A": A, "F": F, "W": np.zeros((H, W)), "L": Lenia(RULE, C, size, R, T), "t": 0}
    s["N0"] = A.sum() / P["Y"] + F.sum()
    return s


def _hm(a, b):
    return 2 * a * b / np.maximum(a + b, 1e-30)


def gated_div(F, Dc):
    """div(Dc grad F) with harmonic face means, periodic, conservative."""
    Dx = _hm(Dc, np.roll(Dc, -1, 1))
    Dy = _hm(Dc, np.roll(Dc, -1, 0))
    fx = Dx * (np.roll(F, -1, 1) - F)
    fy = Dy * (np.roll(F, -1, 0) - F)
    return fx - np.roll(fx, 1, 1) + fy - np.roll(fy, 1, 0)


def step(s):
    L, A, F = s["L"], s["A"], s["F"]
    Y, dt = P["Y"], L.dt
    G = L.growth(A)
    inc = np.clip(np.minimum(dt * G, 1 - A), 0, None)
    dec = np.clip(dt * G, None, 0) - dt * P["decay"] * A
    need = inc.sum(0) / Y
    scale = np.minimum(1, F / np.maximum(need, 1e-12))
    A_mid = A + inc * scale                 # gross build, paid in food (<= 1 by construction of inc)
    A_new = np.clip(A_mid + dec, 0, 1)      # gross loss: negative growth + decay, clipped at 0
    built = (inc * scale).sum(0) / Y
    lost = (A_mid - A_new).sum(0) / Y
    F = np.maximum(F - built, 0)            # every unit built costs food (gross, not net per step)
    Wst = s["W"] + lost                     # every unit lost becomes waste
    s["paid"] = s.get("paid", 0.0) + float(built.sum())   # running food bill (diagnostic)
    reg = dt * P["kr"] * Wst                # waste slowly regrows into food (closed cycle)
    Wst = Wst - reg; F = F + reg
    Dc = P["D"] * _SC * np.exp(-P["beta"] * A_new[1])
    F = F + dt * gated_div(F, Dc)
    Wst = Wst + dt * P["DW"] * _SC * gated_div(Wst, np.ones_like(Wst))
    s["W"] = Wst
    if P["starve_disk"] is not None:        # fork test: food inside the disk is moved far away (kept in ledger)
        m = s.get("_mask")
        if m is not None:
            moved = F[m].sum(); F[m] = 0; F[~m] += moved / (~m).sum()
    s["A"], s["F"] = A_new, F
    s["t"] += 1
    if s["t"] % 100 == 0:
        N = A_new.sum() / Y + F.sum() + s["W"].sum()
        assert abs(N - s["N0"]) < 1e-6 * s["N0"], (N, s["N0"])
    return s


def fields(s):
    return np.concatenate([s["A"], s["F"][None], s["W"][None]])


def damage(s, mask):
    s["N0"] -= s["A"][:, mask].sum() / P["Y"]   # erased matter leaves the world (ledger adjusted)
    s["A"][:, mask] = 0
    return s
