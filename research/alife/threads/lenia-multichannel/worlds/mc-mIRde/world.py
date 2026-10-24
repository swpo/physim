"""Chan (2020) multi-channel Lenia creature '*mIRde' (code A39RG5<3G9TC1) from Chakazul/Lenia Python/found/233s.json, catalogue index 2728.

Positive control for the multi-channel engine: 3 channels, 15 kernels, R=15.
3 planted copies (random rotations); the structure is planted, not spontaneous."""
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
    "name": "mc-mIRde",
    "family": "lenia",
    "parent": 'Chakazul/Lenia found/233s.json#A39RG5<3G9TC1',
    "mutation": "reference creature in this thread's multi-channel engine",
    "size": (192, 192),
    "steps_per_frame": 10,
    "dt": 0.1,
    "channels": ["A0", "A1", "A2"][:3] + (["F"] if None else []),
    "matter": list(range(3)),
}

R, T = 15, 10
RULE = [
    {"b": "1,0,5/6", "m": 0.1, "s": 0.01, "c": [0, 0]},
    {"b": "5/12,1", "m": 0.162, "s": 0.0471, "c": [0, 0]},
    {"b": "1", "m": 0.245, "s": 0.0732, "c": [0, 0]},
    {"b": "1,1/4,3/4", "m": 0.123, "s": 0.012, "c": [1, 1]},
    {"b": "1/4,1", "m": 0.209, "s": 0.0722, "c": [1, 1]},
    {"b": "1", "m": 0.386, "s": 0.101, "c": [1, 1]},
    {"b": "1,1/12,1/3", "m": 0.132, "s": 0.0185, "c": [2, 2]},
    {"b": "1/4,1", "m": 0.127, "s": 0.0676, "c": [2, 2]},
    {"b": "1", "m": 0.403, "s": 0.0935, "c": [2, 2]},
    {"b": "1/6,1", "m": 0.147, "s": 0.0542, "c": [0, 1]},
    {"b": "1", "m": 0.548, "s": 0.0954, "c": [1, 0]},
    {"b": "5/12,1", "m": 0.14, "s": 0.0623, "c": [1, 2]},
    {"b": "1", "m": 0.318, "s": 0.0821, "c": [2, 1]},
    {"b": "5/12,1", "m": 0.135, "s": 0.0532, "c": [2, 0]},
    {"b": "1", "m": 0.301, "s": 0.0862, "c": [0, 2]},
]
CELLS = [
    "20.B11.$20.pUpH10.$21.pNS9.$16.2QF13.$14.XqGsWwSvLrJXB10.$7.F2UDBWpUrAtK2yOtMpDA11.$6.MpMpUpKpVrJsDrWrPtEsXpS14.$5.IpXqTqMqCrBsBsGrLrMqID6.XrHsJqDGpS3.$5.pRrIrMqGpEpLpXqHqLsBqVNA2.qKtUuKtDuCvKtESM3.$4.pOqVrLqJMAQqMrIsQwJuIqCK.LtDvXtLqQqErJpG5.$3.pAqQrCqNU2.qLsVvJxNxMxTvDrPqArTrIpT4.B5.$3.pXqPqXpSF.pRtT2yIyFyE2yLvWvUxJtMsFqXpVpFpJHA4.$2.WpJqUqTpFLpHsXyFyLyM2yLxRxN2yOyEsRpM10.$.SqBpJqTqASXsMxLyFyMyNyOxHwB2yOyNxKqH11.$.qNqApCpGKIpWwMxKwGyLyOxPvVxH2yOyFwGsC11.$.pUpWK2.BsXwTvTtXyKyOuVrLuQwNwUxGwJqA5.pNrErP3.$.RqRpG3.tSwFuBtCyGvMrKKpNpXsBtSsT6.rRqLrIrW2.$.TrWsH3.sBtMsItSxRuRpE.BA.2T6.sErGsItO2.$.pFrFuA3.XpSqDtUwVuQI3.pOpRpKCAB4.KpC3.$.pIpGsC6.qCvSuFpAB.pED.W12.$.pB.2pD5.BrIsAuGrKDC.H13.$.D2.M6.pSsLtJ2DEF14.$6.pX25.$6.CpF24.$7.qF24.$32.$32.$32.$32.$32.$32.$32.$32.$32.!",
    "32.$32.$32.$32.$32.$13.DEC16.$10.DQ2pBOC16.$8.GTpKpUpSpIRH2CEGIGA9.$6.BNpFqAqPqIpNpCpApEpMpRpUpRpIWNC8.$5.AMpHqBqQqIpJUTpDpTpVpKpLqOqJpOpDQG7.$5.FXpQ2qEpLRLQpApUqVqUqPrFrRqNpQpERI6.$5.LpGpTqBpUpFSRQHqGtFuOvEvUvSuSrKqApLWI5.$4.ARpKpVqBpSpIpBT.AqGuCwRyOxTsDrXuSrPpXpIRC4.$4.CXpPqAqCpU2pNpEKXsFxJyOwBqUpVpFsAqUqApERB4.$4.FpFpSqDqEpVpSqFrArMtFxBuKrAqLqMrCqNrDqNqKpAKA4.$4.GpIpWqMqKpXpVqSsOuLyAxAsTsFtIvXyOxQqJqFrBpDEB4.$4.GpIqFrDrCqKqCqWtCwDyOuOuCwT3yOyDqHpRqTpTqIqVqX3.$4.DpFqIrTsHrRqPqIsPwWwTuXxV2yOyCtNpEpFpGpTsJuBrGqKpD2.$4.ApAqFrWtDsUrLrQtItRrJuQ3yOsHpMpFpJ2rKrCsKVB3.$5.RpSrHsQuLwMyOxEuEqEtDwAwPvWpJpKpFqWwPvSrIC5.$5.JpBqNtNxG4yOsGqQrCvEwCsNpIpJsByCwAqB6.$5.CIqCtHvP4yOtSpHpTvRwLxJtMsTtRvUqF7.$7.qCsPsIrBpTvXxSsM2pPuPxPyOxE2yOyLpW7.$7.WvKtKTpCpEsUrMqIpArSuQvPxR2yOvL8.$8.uDyOuHPUsJrMrLqBpIsIwByCyMwPrT.B6.$8.BuKyOvEsHtXtVtPsIpUsEwExOwKtIIpB7.$9.EtMvEtTtNuIuLtNrIrKtGtIqS10.$12.XpKpFqLrLrNqQQ12.$16.TpW14.$32.$32.$32.$32.$32.!",
    "32.$32.$32.$11.4AB2DB13.$8.BINJ2.DpApOpMWG12.$7.HpBpGL3.CpKpTpDC13.$6.OpPpTO3.pAqCpVS15.$5.LpMqBpFF.SrFsOsDqSJ5.BV8.$4.EpAqApXpPOqBtGvUwHvKpUC7.pQpR6.$4.UqBqNqOpLqCtMxM2yOtVqQpXqOqVqJpLN3.BqFF4.$3.QqFrFqUqCpFrVwM2yOxTvLxN3yOyDvXtQrTpV2.pNqMB3.$2.BpQrJrDqCQpOtS3yOwL7yOwBsSqFJ.pGsKqIA2.$2.MqGrDpMP.qSvX2yOxExT6yOxFtKqM4.rCsKpO2.$.ATqEpUA.LsOyE2yOxH7yOuWpV6.pNrVH.$.DTpVpD2.pOuJ11yOyDqS7.qSrF.$.EQpUpS.HqLvG12yOsOpI6.qOsVM$.BJpKpR.DqGuR12yOwPsNqOwHuHsI.pFtItNpW$2.FT3.WsSxB10yOwTvJyOyLxEuK2.pOvJtEpJ$2.DC4.qAuDyD7yOwWuHtMtKtLyDrJ4.vUtQD$2.B6.qUuTyE7yOtAqJpVpI6.NuO.$2.A7.rAuIvXwDxL3yOvUpMC9.pF.$6.pX4.qOsNsRtTwPwKtKqF7.qT2.CpAL$6.X5.2pGpHqQrBD7.JsAABV.W$7.pJ16.CpXpT.JpBuR.$7.rMqC15.qBqOU.pPtIrX.$7.rWyKrN8.WD3.CsBUA2DtH2.$5.G2.wDuH9.U3.qIuIqOON.qJ2.$5.F2.S4.pW9.SpKVPNrC3.$6.J.pR4.yOvU8.AFHGpC4.$7.rCxCwF4.rJ8.A.A6.$8.sPyOvR6.rDsKpGFGM4.pE4.$9.rUyHwT2.FSqFsTsJrTRFsXtVsBqV6.$10.pWuByJyNwCtNsVqUqBrJD2.sErAqB6.$15.C16.!",
]
N_SEED = 3
C = 3
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
