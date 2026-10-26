"""eco-lenia2: lab 1's eco-MIRd-Rplus (threads/lenia-multichannel) with a maintenance cost and
ecology switches, for C:ecology-with-reproduction.
Changes: all matter decays at rate DECAY (as mcfd-MIRd), so cells must keep eating; per-species
tracking (META species on each species' core channel); switches through WORLD_P:
  SEP=1   matched no-interaction twin: each species builds from its own food field (same rho, D,
          start value) and space exclusion is off (EXCL=0); the species then never affect each other.
  FORK="food", T_FORK=t: at time t all food is set to 0 and stops regrowing (both fields).
  FORK="cutA"/"cutB": at T_FORK, food is set to 0 and held at 0 inside a disk of radius CUT_R around
          the median-sized cell of that species (chosen by core-channel components), elsewhere untouched.
Original docstring follows.

Two-species multi-channel Lenia ecology.

Species A: Chan (2020) creature 'MIRd+' (M4HFAN<A39RG5); species B: 'R+' (ZJH3Z0<A39RG5), both from
Chakazul/Lenia Python/found (catalogue indices 1130, 1195). Each species keeps its own 3 channels and
its own 15-kernel rule; the species never sense each other through kernels. They interact only by
  (1) a shared food field F: matter can only be built from local food (yield Y), food regrows at
      rate rho toward Fmax and diffuses with D;
  (2) space exclusion: positive growth of one species is multiplied by (1 - occupancy of the other)^EXCL,
      occupancy = clip(sum of the other species' channels, 0, 1).
Planted creatures (not spontaneous), small multiplicative jitter per seed.
"""
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

"""rps-lenia: three kinds of Chan's MIRd+ replicator (identical rule, separate channel sets, one planted
founder each) on one shared, diffusing, regrowing food with matter built only from food (Y=2) and a
maintenance decay (as eco-lenia2), space exclusion by every kind except its own prey, and predation between kinds: kind i also builds
from kind j's matter within a Gaussian neighbourhood (sigma PSIG), taking at most PRATE of the local prey
per unit time (mass-conserving, yield YP), before drawing on food. MODE: cyclic (0 eats 1, 1 eats 2,
2 eats 0), transitive (0 eats 1 and 2, 1 eats 2), none (competition only). WORLD_P overrides P.
"""
import json as _json, os as _os  # noqa: E402
from scipy import ndimage as _nd  # noqa: E402
P = dict(MODE="cyclic", PRATE=1.0, PSIG=4.0, YP=1.0, DECAY=0.01, RHO=0.03, Y=2.0, DF=2.0, EXCL=1.0, DOMAIN=160, K=3)
P.update(_json.loads(_os.environ.get("WORLD_P", "{}")))
KN = int(P["K"])
META = {
    "name": "rps-lenia-" + P["MODE"],
    "family": "lenia",
    "parent": "collective/contrib/20261025T2214-c26-eco-lenia2-claim/world.py",
    "mutation": "three MIRd+ kinds with cyclic / transitive / no predation between kinds",
    "size": (int(P["DOMAIN"]), int(P["DOMAIN"])),
    "steps_per_frame": 20,
    "dt": 0.1,
    "channels": [f"K{k}c{c}" for k in range(KN) for c in range(3)] + ["F"],
    "matter": [3 * k for k in range(KN)],
    "smooth": 1.0,
    "species": {f"k{k}": [3 * k] for k in range(KN)},
}
R, T = 15, 10
RULE_A = [
    {"b": "1,0,5/6", "m": 0.1, "s": 0.01, "c": [0, 0]},
    {"b": "1/3,1", "m": 0.132, "s": 0.0473, "c": [0, 0]},
    {"b": "1", "m": 0.27, "s": 0.0756, "c": [0, 0]},
    {"b": "1,1/6,5/6", "m": 0.146, "s": 0.0165, "c": [1, 1]},
    {"b": "1/3,1", "m": 0.248, "s": 0.0702, "c": [1, 1]},
    {"b": "1", "m": 0.344, "s": 0.1034, "c": [1, 1]},
    {"b": "1,0,1/3", "m": 0.112, "s": 0.0227, "c": [2, 2]},
    {"b": "1/3,1", "m": 0.103, "s": 0.0695, "c": [2, 2]},
    {"b": "1", "m": 0.363, "s": 0.0916, "c": [2, 2]},
    {"b": "1/6,1", "m": 0.117, "s": 0.052, "c": [0, 1]},
    {"b": "1", "m": 0.514, "s": 0.0978, "c": [1, 0]},
    {"b": "1/2,1", "m": 0.149, "s": 0.063, "c": [1, 2]},
    {"b": "1", "m": 0.282, "s": 0.0828, "c": [2, 1]},
    {"b": "5/12,1", "m": 0.155, "s": 0.0507, "c": [2, 0]},
    {"b": "1", "m": 0.289, "s": 0.0827, "c": [0, 2]},
]
CELLS_A = [
    "50.$50.$50.$50.$50.$50.$50.$50.$50.$25.BGKLJB19.$23.E3.E2.pCG18.$19.BEH4.qDtGqOIqNR18.$17.DrKsX6.rJuVsOpWqXuWB17.$17.rWqX6.EpVqUpDBApLsGH16.$24.ABABHNOJ2.Q2G13.$24.INLUpVrBqWpOA2.qBTA12.$24.pMrIqVrNtFuLuBrOP.AMtNpH12.$23.BrGyNuEuBuFuLuFsGpKABVX.G11.$23.IwOyOwCtBsKsVtWtCqJJ.D14.$23.PvXyOwVqKqAsIwNwOsJU16.$21.qUtJsWvLyOvUSpDuH2yOvOpF5.A10.$21.pIuGwIxGyOwQIqIxX2yOxWpO5.pB10.$21.pCuRxGxNyNyBpNsR3yOxDpN5.pV10.$20.BrLvJxPyHyLyEwN3yOvCrQD6.D9.$20.qTtVwCxLyByCxSyC2yOpD9.pB9.$19.qAtNvLwPxBwRvRwSxQyCxH9.sDtFA8.$19.tWvTwNwWwFtKsXvTxHxKvF9.uCtM9.$19.wAxIxJwWvKuDvGwQxEwKtD20.$19.wLyByAxHwCvUwQxBwMuTqN20.$19.xAyLyMyDxLxGxIwXvWtTT20.$19.xN2yOyNyFxVxNwWvOsS21.$19.yG3yOyJxXxGwCuCqM21.$18.rR4yOyMyBwWuPrM22.$15.CpGrFvN5yOyJwWtL23.$15.LrCuX7yOxCpH23.$15.PsAxA7yOuL24.$15.JrKwG4yOwMtIvFsB24.$15.CqFuDxIyOyMwLtSsCsFsG24.$10.TqR3.ApKsDuLvPvKtXsFrGsEsFB23.$8.BKpBqWpB2.FpHqUsBsTsXsKrOrFrNqUH23.$8.ACEpKHTqGrBqAqB2qGqRrMrTrQqXpI24.$11.RBRvByOvQtBqIUpGqMqLpPpCE24.$11.GpEpUuDwXsQrXtQtWrJpIM27.$12.UqCrNqXKOrSyNyOqV28.$12.BVqApWBEpAwPyAsM28.$14.JpIqJpSpPrErHpKCG26.$15.APpXqBS2.QpSpC25.$17.BON.DPLI25.$50.$50.$50.$50.$50.!",
    "50.$50.$50.$50.$50.$50.$22.AITpFpKpFQNTXTG16.$21.FPpFpUqHqIqApGORpLpSpJQ15.$20.LpDqAqEpDIQpCpKpJpBQJpApCQKI12.$19.SpTqO2JWpSqTrTsMsLrSqSpWpHSpBpGpJXD10.$18.XqLrTKTpXrQtOvNxHyHyCwTvCtLsBqRpNQNUI10.$17.OqWsPSXqPwI9yOwDuArVqDXF11.$16.BqVsTqFOqPxB12yOvCsJqIXFN9.$15.KrAsTtIpMqEuLwIxKyB11yOvUsLqCqUsLpQD7.$14.NrJsBtBuTtUuWuKsQtDyJ12yOvNrIqLuTpNJA6.$14.qOqTqVrVvIwFvKqSpAvB14yOsIpGuOpR8.$13.QpHVpIqOtNrLN.pRxE6yOvVyF6yOtQpFDrC8.$13.QJDPrRO3.qTyM3yOxIsKI.tDxE6yOpJDpIC7.$13.UIFqIP4.rN3yOxPpE4.rE6yOuDDWE7.$12.G9.rG3yOvK3.pS2.qA5yOwXCpVC7.$22.qC3yOyNqF.pUtC.ApC6yOApLA7.$11.E10.tX2yOyNxXwVtRuI2.DpA5yOsN.E8.$11.H10.xRyKxVxAvVuXvAuKqR.FqM5yOtK.A8.$21.WrG.ApXqXrTtGvLwCtXsDuIyJyGyN2yOuA.J8.$10.F9.rXQ5.HpDsJvJvSrHCtDxFuTuHtIwVuGM8.$10.F8.rGvJ7.qDqC5.B.pLqOyOwC9.$9.CA8.uBqT7.PA8.pGxCM9.$9.IB8.sE19.A10.$9.rDpP17.qW9.ApL10.$8.tAtS12.AXpBA.qXtK10.wI10.$8.wKP2.B.pGrG11.qL10.MrO10.$7.NsV2.rKrVqDtFuTpT21.pK11.$7.qEpE.qTvHvFvHwHwNuJpH20.qT11.$7.rPQ.vDxWxQxDxJxPwLtDJ18.sAqL11.$6.CsUOpWxTyOyMyJ2yOxXuFpW18.qS12.$6.SsVpPqWyI6yOwArMqArVsWqMPpNqDpQ23.$5.FpNsBrErDxJ6yOxStXsMuGwEwFwQxPyLyOyHvQ21.$5.EpVsItUuUwR6yOyFvSvBwKxO6yOuS7.pC13.$6.pItCwQxWyK6yOyJwXxByH6yOxRT4.tIuMsE14.$6.BqKtTwLxU7yOyEyL7yOsL4.vUxGuPpP14.$7.EpNrJtXyN14yOvSQ3.tSuBrNqC15.$7.ApAqTsVvL14yOsB3.sOuDrNI16.$8.MpVrKtFvS12yOuUqGpArWuKuUtSrOM16.$8.CVpXrDsQvAyL9yOxSwQxGxVxDwIuFsBqAF16.$9.ESpMqJrOtMwC10yOxPwXwItHqBXN17.$10.CKVpMqLrTtKvBwLxOyE4yOyDvNtJqWTINB17.$12.CJTpKqHrGsFtCtR2uDvKuUsPqPpJTUpAI18.$14.BISpGpTqFqMqRqUqSqJpQUJNVL19.$16.CGMQSUVUOF24.$19.AB2CB26.$50.$50.$50.!",
    "29.ESNA17.$24.KH2.RqJqVqOpVK16.$22.GqFqSrIrRrTsAsMtDtJtAsKsCqWpVpMQA10.$20.CKqIrRrIrPrHpVpJsCvBvNuDW.rXuRrFqGpB10.$17.FpIpPpLqArWsP2sIrLpFIqUvXwBtR2.qAxCpUpOpPN9.$16.BpNpXqTsAtLuCsGrHrJsJA2.sXvKpS2.TuOyOwVtCrMpLMA6.$17.UpNqNtP2.GqMsPtK7.qVT3.pSvUvMqQVA5.$17.DMpFvQ13.wMuA5.xLtGqIS5.$16.BqGsEvNxW7.wFyM4.tPuA.DrM2.qPwWrApL5.$15.KsP3.DsGyOyMwL3.wDvP4.qK2.yOxTyO2.pNuXtJqTD3.$14.DrJQ5.yOwXyK3.uTuM3.uGuJ3.yGyO3.pPtQrT4.$14.MtKsJ7.pV8.pKrP8.MvIsRFE2.$14.qJvDwPuB2yOvJ22.2yOwJtApM2.$13.rIsTrM.VyOyDyO16.vPqI3.3yOrWvCI2.$19.uG3.qN5.vCtN7.tX3.2yO2.rFH2.$13.NL7.2yOuL3.WwKrX6.vMyM8.vB2.$13.2yOwM5.3yO23.sTtE.$13.5yOxH2.yDyO16.yOsB3.wOyOsOVpMR$16.qA2yOxDTJ16.xJ.tGsQ2.3yOrNVX$10.pPyO5.pXrTsCNC2.yOwG12.S.yOrR3.vCtAtWuMqR$10.2yO4.CqKpTK3.3yO13.QL6.vBuFpF$14.3yOvRVA3.2yO5.yOwC10.pIpM3.uVqSF$8.tM5.4yOA11.2yO9.C2yOuO2.uWqHF$7.qVtNyO5.2yO3.sB13.rOqC2.A2.O3yO.vTtOqMI$6.LyOyAyO10.sNqO5.F10.PpI2.sJuE2.uQrLpXB$20.wByN16.2yO6.sMVJ.$11.2yOwX2.wDA2.qQvU16.2yO6.pK3.$5.pMyO4.yOyMyO.tJtFpP17.pA2yO5.pPvQuFA3.$2.pA2.yOxPyO3.tVuR3.V13.B4.3yO3.J2yOxCqPB3.$2.qNrH.xC2yOR13.rB5.uBsAvC5.yO4.2yOxKG5.$.pGrVtCpA16.vRsE5.rPrFqH11.yOqH6.$LpOtBuCsX6.qX3yOqN5.pS10.pE2yO15.$2.tNtCyO3.tP3.X2yOrI16.yOqPyO3.2yOyD9.$2.tV2yO2.2yO23.wPyOvP3.yOwGwI9.$qJTsKuG2.yOxWyO9.sVvIrH2.pLsD14.tA10.$pFtIpP3.rDyOpS.pBvJ6.uDwDI2.pUyO3.2yO20.$.uTqD7.yO.qS5.tWpV8.3yO3.xF3yOwX11.$.tOtSpO6.xTwLpE15.3yO3.4yOtS11.$OtGuK2yOxP3.rLqH14.tLyOxFqO21.$TrErNxR2yO.IyOxD15.tGvXyO22.$AqOqEsGvB3.wTtWI10.rN4.uGtP3.2yO17.$.RsArUpK4.rR16.I3.4yOrBuSuUqB12.$2.IqVrID18.AxDuT4.uOuJtBxSvSpVH12.$3.pArGsQvKvBrN13.D3yOE7.qUuNrCJ12.$3.pIrXtPuTvQvA13.xRpQyAG3.Q4.DpU14.$3.pGsCsPuEvNsI13.qUxGX3.2yOxMqIqGrFrHpM14.$3.DqRqSqQrIpA18.xTyOxKuDyHwLtAsApNA13.$4.KqXrXsRsEpRCpOpG14.rS3.rRvRsBpVF14.$5.EqVsWuBuFtWtErFO2.pCpO9.pA3.KtApQ16.$7.pPrVtEtFsRrRqKpSqBqMrIrCKpBrRtCrJDpUtGvBuVrCsCtArGpNB15.$7.EpMqVrQsArWrAqHqDqApXqVrErCrOtCtFsEtWuNsFrApUM19.$9.BJMNOpApQqBpXpQpOpQqGrXsPsGtCtMsAqEK20.$16.DH3.FUpWqMqSqUqJpE21.!",
]
def _place(A, cr, n, rng, placed):
    H, W = A.shape[1:]
    h, w = cr.shape[1:]
    for _ in range(n):
        for _try in range(100):
            y, x = int(rng.integers(0, H)), int(rng.integers(0, W))
            if all(min(abs(y - py), H - abs(y - py)) > 2.5 * max(h, w) or
                   min(abs(x - px), W - abs(x - px)) > 2.5 * max(h, w) for py, px in placed):
                break
        placed.append((y, x))
        c = np.rot90(cr, int(rng.integers(4)), axes=(1, 2))
        A = np.maximum(A, np.roll(np.pad(c, ((0, 0), (0, H - c.shape[1]), (0, W - c.shape[2]))), (y, x), (1, 2)))
    return A



JITTER = 0.05


def _eat():
    E = np.zeros((KN, KN))
    if P["MODE"] == "cyclic":
        for i in range(KN):
            E[i, (i + 1) % KN] = 1
    elif P["MODE"] == "transitive":
        for i in range(KN):
            E[i, i + 1:] = 1
    return E


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    placed = []
    X = []
    for k in range(KN):
        A = _place(np.zeros((3, H, W)), _creature(CELLS_A), 1, rng, placed)
        X.append(np.clip(A * (1 + JITTER * rng.standard_normal(A.shape)), 0, 1))
    ky = 2 * np.pi * np.fft.fftfreq(H)[:, None]
    kx = 2 * np.pi * np.fft.rfftfreq(W)[None, :]
    return {"X": np.stack(X), "F": np.ones((H, W)), "lapK": -(kx ** 2 + ky ** 2), "t": 0.0,
            "L": Lenia(RULE_A, 3, size, R, T), "E": _eat(), "eaten": np.zeros((KN, KN))}


def step(s):
    dt = 0.1
    s["t"] += dt
    X, F, L, E = s["X"], s["F"], s["L"], s["E"]
    occ = np.clip(X.sum(1), 0, 1)                     # (K, H, W)
    tot = occ.sum(0)
    inc, dec = [], []
    for k in range(KN):
        G = L.growth(X[k])
        other = np.clip(tot - occ[k] - (E[k][:, None, None] * occ).sum(0), 0, 1)  # a kind is not blocked by its prey
        inc.append(np.clip(np.minimum(dt * G, 1 - X[k]), 0, None) * (1 - other) ** P["EXCL"])
        dec.append(np.clip(dt * G, None, 0))
    inc, dec = np.stack(inc), np.stack(dec)
    need = inc.sum(1)                                  # matter to build per kind (H, W)
    Sav = [_nd.gaussian_filter(X[j].sum(0), P["PSIG"], mode="wrap") for j in range(KN)]
    take = np.zeros((KN, ) + F.shape)                  # fraction of kind j removed per pixel
    fromP = np.zeros_like(need)
    for i in range(KN):
        for j in range(KN):
            if E[i, j]:
                g = np.minimum(np.maximum(need[i] - fromP[i] * P["YP"], 0) / P["YP"], dt * P["PRATE"] * Sav[j])
                fromP[i] += g
                fr = np.clip(g / np.maximum(Sav[j], 1e-12), 0, 1)
                tk = np.clip(_nd.gaussian_filter(fr, P["PSIG"], mode="wrap"), 0, 1)
                take[j] += tk
                s["eaten"][i, j] += float((X[j].sum(0) * tk).sum())
    rest = np.maximum(need - fromP * P["YP"], 0) / P["Y"]  # food needed for the rest
    scale = np.minimum(1, F / np.maximum(rest.sum(0), 1e-12))
    built = fromP * P["YP"] + rest * P["Y"] * scale
    sc = np.where(need > 0, built / np.maximum(need, 1e-12), 0)
    Xn = X + inc * np.clip(sc, 0, 1)[:, None] + dec - dt * P["DECAY"] * X - X * np.clip(take, 0, 1)[:, None]
    s["X"] = np.clip(Xn, 0, 1)
    F = F - rest.sum(0) * scale + dt * P["RHO"] * (1 - F)
    F = _irfft2(_rfft2(F) / (1 - dt * P["DF"] * s["lapK"]), F.shape)
    s["F"] = np.clip(F, 0, None)
    return s


def fields(s):
    return np.concatenate([s["X"].reshape(-1, *s["F"].shape), s["F"][None]])


def damage(s, mask):
    s["X"][:, :, mask] = 0
    return s
