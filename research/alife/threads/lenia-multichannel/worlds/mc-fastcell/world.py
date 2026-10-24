"""Chan (2020) multi-channel Lenia creature '*fast cell' (code N5NYG2<L6218A) from Chakazul/Lenia Python/found/233s.json, catalogue index 2841.

Positive control for the multi-channel engine: 3 channels, 15 kernels, R=20.
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
    "name": "mc-fastcell",
    "family": "lenia",
    "parent": 'Chakazul/Lenia found/233s.json#N5NYG2<L6218A',
    "mutation": "reference creature in this thread's multi-channel engine",
    "size": (192, 192),
    "steps_per_frame": 5,
    "dt": 0.1,
    "channels": ["A0", "A1", "A2"][:3] + (["F"] if None else []),
    "matter": [1, 2],   # track the compact core (A1+A2); the cyan shell sheds debris
    "smooth": 2.0,
}

R, T = 20, 10
RULE = [
    {"b": "1,1/6,3/4", "m": 0.177, "s": 0.0111, "c": [0, 0]},
    {"b": "5/12,1", "m": 0.166, "s": 0.054, "c": [0, 0]},
    {"b": "1", "m": 0.176, "s": 0.0663, "c": [0, 0]},
    {"b": "1,1/12,3/4", "m": 0.102, "s": 0.0217, "c": [1, 1]},
    {"b": "1/6,1", "m": 0.203, "s": 0.0632, "c": [1, 1]},
    {"b": "1", "m": 0.305, "s": 0.1087, "c": [1, 1]},
    {"b": "1,0,5/12", "m": 0.191, "s": 0.01, "c": [2, 2]},
    {"b": "1/3,1", "m": 0.134, "s": 0.0593, "c": [2, 2]},
    {"b": "1", "m": 0.315, "s": 0.0966, "c": [2, 2]},
    {"b": "1/12,1", "m": 0.3, "s": 0.0595, "c": [0, 1]},
    {"b": "1", "m": 0.743, "s": 0.0875, "c": [1, 0]},
    {"b": "1/3,1", "m": 0.13, "s": 0.0807, "c": [1, 2]},
    {"b": "1", "m": 0.392, "s": 0.0883, "c": [2, 1]},
    {"b": "1/3,1", "m": 0.147, "s": 0.0428, "c": [2, 0]},
    {"b": "1", "m": 0.449, "s": 0.0901, "c": [0, 2]},
]
CELLS = [
    "20.BLPLHFGMpCpVqIqLqKqJqGpXpJPC12.$15.rBsO3sNsPsTtAtD2tBtGtVuUvOvVwAvWvPvEuOtTsOrApHE10.$13.rCwVrPNpQsGvHxOyM7yOyGxPxHxDwWwOwDvOvBuGsVqVVA8.$12.uKyApB.pAsOvX15yOyHxPwWwHvOuTtSsApRF7.$11.yOxPpApFuByN20yOxQwVwCvEuEsRqKN6.$9.xJyOT.qPyF8yOyMxWxNxOyAyL9yOyBxFwJvKuLtErAWA4.$8.vJqB2.CwO7yOxXxAvXvEuUuXvLwGxGyE7yOyNxXxGwKvMuOtJrGpCA3.$7.tEqR3.vE4yOyLxBwAvHuPtRsTsGsDsKsVtOuMvRwXxWyJyN2yOyHxSxOxIwUwDvGuKtGrEpBA2.$6.uDsEO.qLyB4yOvRtAqXpWpRpSpPpJpOqF2qMqUrKsJtSvHwPxLxWxNwTwIwFwJwHvXvKuRuBsSqRT2.$4.rUuLsKuDwIyM3yOyCuJqM8.Q2qKS2.CpGrCtCuSvMvCuPuMuNuVvEvFvAuPuEtLsApXI.$3.qQrG.rWvX4yOtT12.pWpR7.pAqPrKrTsGsUtHtXuHuJuHuCtQsSrApBA$3.vBrQsCuGwIyC2yOrQ25.MpTrCsEsWtOtW2uBtTtErSpSF$2.rIyOyMvEwQxWyNqQGA27.pKrFsMtItTuBuDtXtLsHqFK$2.sR2yOwWxWvVrQTA.G26.GqJsJtPuFuKuJuEtRsRqMM$2.tN2yOxVxFvGsFSBpE28.qBsIuDvCvHuXuKtVtAqRM$2.2yOxNxJyHyNxAqMqTqC28.pUsPuSvXwIvUuTuCtFqUK$.qSyOtEvAxG2yOwCsAtDqV28.pJsUvMwXxIwUvIuItKqXI$.tAvWsGvQyJ2yOwPsMqOrHpC27.MsXwGxXyGxRwBuStPrBG$.yJsFtJwGyN2yOxLsLADRNA26.tAwXyJyOyJwUvDtXrAE$.yOwLxQyHyN3yOtD31.tExKyM2yOxMvMuHqWC$.yOxFxSyHyN3yOtC31.tVxQ3yOyAvXuQqVB$pE2yOxSyHyNyOxHuDX30.UvFxX4yOwNvBqTA$pP2yOxQyGyNyCwWtNH30.rHwJyH4yOxDvKqP.$D2yOxKyEyMxWwDsE31.uBxHyN4yOxPvPqI.$.xKuQqTvQyDxHuKqA30.qWvIyA5yOxWvNpU.$.vEA.tMxGxKuQrDC.pIX26.sIwFyI5yOxXuSpD.$.qVqS.sVyB2yJuVsBvEvGpU25.MsVwLyL5yOxPtBJ.$2.xXuAwDxOyFvLsLrLvSxNpS24.CpMtAwLyM5yOvWqQ2.$2.tTyKxFxNwVuJsCrAsBuMqV24.pMqQtDwMyN4yOxIsRQ2.$2.SrKtVxEwNtUrWrAqQrHrL24.pEqXtPwRyM2yOxUxFuFpO3.$2.KqAqVvKvUtGsCrUrLqWqV25.rBuXxRyOyKxIwDuTqUB3.$3.pIpOsCuGtIsQtEsTrIqF3.AD19.IsMwL2yOyGwGuHrSM4.$3.PpJpXsWtVuEuKuBsNrM4.ABA17.rHuHxS2yOxJuIrNW5.$4.pJpVsGuMvMwAwBvNvHR5.ERKC11.pGqPsBuTxM2yOyDuSrAN6.$4.pAqJrSuGwHyDyIyKxMrJpW4.IqCVA10.pStAuUwJyH3yOvRrQI7.$4.TrHrJuGxGyAyIyMwQvXuUsLX2.pRsLC10.pEtOwLyD4yOwStBpE8.$4.DsGtPwCwRxSyFxWyByJxVwGtWwRrRvGuARA.CB5.qAuDxD6yOuHqR9.$5.qIwWyOvWuDtEvEwRxPyFyL2yOvOwCvWsJqIpBB5.tMwMyG6yOwTsAP9.$6.qByOyEqDpOrUxLyIyM4yOtCpRD6.rDxU7yOyNyOtJpF10.$8.2yOsVxJxTyCyIyM3yOwNrRQB2ADpBuK7yOyLvXvFvEV11.$9.tG3yOxUyByIyNyKwUuAqTpFpWrR8yOyMyAwGsQpVvCpA12.$10.qKvD2yOxLwKxCyMyIwRuGwH6yOsOrErTuItLrHpPBpSsI13.$12.wGyOuSrCuGwUyDyIyK2yL4yOqW3.uCuSrWpWqQtU14.$13.sIwWtQtFvOxAxFwOwGvTvEwCxCtStHqOrR2yOyFxVvWrQ15.$15.uJ4yOvNsCH.BrJsBqXqPrM21.$16.rWvHxW2yO3.pWqH25.$18.qUxSyNqLpKsJqU26.$19.pBrPsKqM28.!",
    "51.$51.$51.$51.$51.$51.$51.$51.$51.$51.$32.IG17.$20.CECBDF2GFECAJPJ16.$18.pDqKqSqIpQpHpKqAqQrDrCqMpQVI2SJ15.$17.qTsVtTtStArXrIrTtMwDyFyCvQsTqQpGTpAWK14.$16.rHvBxJyJyOyJ2xW6yOwUsUqPpHpEpHpAJ13.$15.pIvN14yOuJrSqFpGpLpIUD12.$15.tQ14yOyEuMrWqQpTpJpKpBK12.$14.sO14yOyGvVtNrOqPqDpMpIpEQ12.$12.pGuMxX13yOxTvSuEsVrPqTqMpW2pLpBE11.$12.rVwEyL5yOwPvIwK5yOwVuXtStDsOrVrIqNpXqFpSP11.$11.pEuCxH4yOvOqL2.PqVvB3yOxJvQuRuOuRuFtArLqLrCqPpF11.$11.rPvJyB3yOvDD5.pUuOyG2yOxMwUxGyBxUvOsMqNrIrApL11.$10.OtHwKyM3yOqM4.B2.sDwX7yOyGtFqDqMqLpC11.$10.qMuHxF3yOyMpO3.GpNG.rDwS8yOsTpJUpEF11.$10.rLuSxI4yOtK3.GXA.rHyE7yOxRrAK14.$10.rHuAwKyG4yOqO6.uA8yOtVpE15.$10.QrNuBwRyL3yOuP5.qFwG7yOwVqXH15.$13.tGxM3yOyGqC3.qMvO7yOyNtFpL16.$13.CwLyM3yOxJtRtFvDyD8yOuRrDN16.$14.wAyF14yOyBuUsFpL17.$13.pTvRxNyL12yOxMuGsGpXB17.$13.sJuTwExDxXyM9yOxWuHrXpWB18.$13.qWsPtPuJvGwLxPyHyN5yOyAuVsEpT20.$14.VpOpKpIqStDvMxGyCyBxIwOvKtSrQpL21.$20.FC.EpJqApQT23.$51.$51.$51.$51.$51.$51.$51.$51.$51.$51.$51.$51.$51.!",
    "51.$51.$51.$51.$51.$51.$51.$51.$24.AHKHC22.$23.OpDpGpHpRqIqSqTqKpLLCEFEB12.$19.I2.XpRpXqDrKtUuDsPrVrUsFsQsIqSpBQKD11.$18.ABpID.GRrBvKwMtMsQsGsCsHsTtEtFsVqTpBNE10.$25.tHyOvWvBuQuCtPtQuDuRuVuItNrNpDLC9.$24.rEyOxXuJvHvXwA2vUwEwOwSwHvCtRqXUGA8.$22.rLuSvTtGrSuOxAyIyOyNyM3yOyDwSuUsVpLIB8.$15.pGsVtKuEtIpNA3.JsJwFyL8yOyDvUtQqOJB8.$19.M4.MrRvDwWxVyL8yOwOtWrKIA8.$17.SK3.JpWrUuGvVwKxCxSyI7yOwTtWrPK9.$15.BWpWrLsMtLuMvNwMxDxCwPwJwMwWxNyH6yOwNtQrMK9.$15.GpXrLtVvFwIxExUyJ2yOxXwSwFwHwTxR6yOvUtGrHG9.$15.LpItFvJwTxPyCyL4yOxOwIvXwHxEyK4yOxQuVsSrCA9.$15.OpOtXvXxFxTyCyJ5yOwUvXwBwWyG4yOwGtSsHqQ10.$14.J.rAuCvWxBxNxTyF5yOxKwFwBwTyC3yOxEuPsLsCpP10.$14.M.rNuBvQwSxHxPyCyN4yOxPwGwBvEuKvMwSwKuXsUrHsIG10.$14.K.rDuBvKwLxDxOyCyN4yOxFvUuSrRqXsMuAuGtArGqQrS11.$12.qIqHqQpUrJuCvGwHxCxQyEyN3yOxXvXuQrEMPrEsWsRrJqFrIpO11.$11.qUsIsRuAtHsHtIvDwBwXxQyFyM2yOxSvQtOqA2.pGrUsGrNqPqNrJC11.$11.qJrXsUuEvBsSsIuCvPwMxHxUyCxUwRuOsC3.xDyEvXuGsUrRrDqC12.$11.PqTsItLuLsJpWqTtQvMwDwJwAuTsDB3.yOvNsKtGtHsJrFqGpG12.$12.pUrQsMtCpUA.FrDsNsTsAX4.tOrO.VsGsCqUpTpFR12.$12.pHrHrUpDCPK3.G3.B2.I.pKsDrIpUpA2OF12.$13.pI4.LS2WR2LA4.CrPrKpTWLKH13.$20.WrVpHA2.rE3.FpLrIqDpEOC14.$21.sBuQpU2.pQ3.FqVpVH17.$20.UqMsGDS.2L2.CpL19.$21.pErJ.rKpSpLQ2.R20.$22.S.rVrHrD24.$51.$51.$51.$51.$51.$51.$51.$51.$51.$51.$51.!",
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
