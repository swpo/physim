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


META = {
    "name": "eco-lenia2",
    "family": "lenia",
    "parent": 'threads/lenia-multichannel/worlds/eco-MIRd-Rplus',
    "mutation": 'maintenance decay of all matter; no-interaction (separate food) twin; food forks',
    "size": (160, 160),
    "steps_per_frame": 10,
    "dt": 0.1,
    "channels": ["A0", "A1", "A2", "B0", "B1", "B2", "F"],
    "matter": [0, 3],   # core channel of each species (halos fuse neighbours otherwise)
    "smooth": 1.0,
    "species": {"A": [0], "B": [3]},
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
RULE_B = [
    {"b": "11/12,1/12,1", "m": 0.135, "s": 0.012, "c": [0, 0]},
    {"b": "1/2,1", "m": 0.125, "s": 0.0474, "c": [0, 0]},
    {"b": "1", "m": 0.248, "s": 0.0769, "c": [0, 0]},
    {"b": "1,1/6,3/4", "m": 0.1, "s": 0.0158, "c": [1, 1]},
    {"b": "1/6,1", "m": 0.161, "s": 0.0732, "c": [1, 1]},
    {"b": "1", "m": 0.38, "s": 0.1024, "c": [1, 1]},
    {"b": "1,0,1/4", "m": 0.109, "s": 0.0189, "c": [2, 2]},
    {"b": "1/6,1", "m": 0.131, "s": 0.0638, "c": [2, 2]},
    {"b": "1", "m": 0.354, "s": 0.0947, "c": [2, 2]},
    {"b": "1/12,1", "m": 0.138, "s": 0.0533, "c": [0, 1]},
    {"b": "1", "m": 0.598, "s": 0.0923, "c": [1, 0]},
    {"b": "1/2,1", "m": 0.147, "s": 0.0658, "c": [1, 2]},
    {"b": "1", "m": 0.283, "s": 0.0821, "c": [2, 1]},
    {"b": "1/3,1", "m": 0.131, "s": 0.0496, "c": [2, 0]},
    {"b": "1", "m": 0.292, "s": 0.0821, "c": [0, 2]},
]
CELLS_A = [
    "50.$50.$50.$50.$50.$50.$50.$50.$50.$25.BGKLJB19.$23.E3.E2.pCG18.$19.BEH4.qDtGqOIqNR18.$17.DrKsX6.rJuVsOpWqXuWB17.$17.rWqX6.EpVqUpDBApLsGH16.$24.ABABHNOJ2.Q2G13.$24.INLUpVrBqWpOA2.qBTA12.$24.pMrIqVrNtFuLuBrOP.AMtNpH12.$23.BrGyNuEuBuFuLuFsGpKABVX.G11.$23.IwOyOwCtBsKsVtWtCqJJ.D14.$23.PvXyOwVqKqAsIwNwOsJU16.$21.qUtJsWvLyOvUSpDuH2yOvOpF5.A10.$21.pIuGwIxGyOwQIqIxX2yOxWpO5.pB10.$21.pCuRxGxNyNyBpNsR3yOxDpN5.pV10.$20.BrLvJxPyHyLyEwN3yOvCrQD6.D9.$20.qTtVwCxLyByCxSyC2yOpD9.pB9.$19.qAtNvLwPxBwRvRwSxQyCxH9.sDtFA8.$19.tWvTwNwWwFtKsXvTxHxKvF9.uCtM9.$19.wAxIxJwWvKuDvGwQxEwKtD20.$19.wLyByAxHwCvUwQxBwMuTqN20.$19.xAyLyMyDxLxGxIwXvWtTT20.$19.xN2yOyNyFxVxNwWvOsS21.$19.yG3yOyJxXxGwCuCqM21.$18.rR4yOyMyBwWuPrM22.$15.CpGrFvN5yOyJwWtL23.$15.LrCuX7yOxCpH23.$15.PsAxA7yOuL24.$15.JrKwG4yOwMtIvFsB24.$15.CqFuDxIyOyMwLtSsCsFsG24.$10.TqR3.ApKsDuLvPvKtXsFrGsEsFB23.$8.BKpBqWpB2.FpHqUsBsTsXsKrOrFrNqUH23.$8.ACEpKHTqGrBqAqB2qGqRrMrTrQqXpI24.$11.RBRvByOvQtBqIUpGqMqLpPpCE24.$11.GpEpUuDwXsQrXtQtWrJpIM27.$12.UqCrNqXKOrSyNyOqV28.$12.BVqApWBEpAwPyAsM28.$14.JpIqJpSpPrErHpKCG26.$15.APpXqBS2.QpSpC25.$17.BON.DPLI25.$50.$50.$50.$50.$50.!",
    "50.$50.$50.$50.$50.$50.$22.AITpFpKpFQNTXTG16.$21.FPpFpUqHqIqApGORpLpSpJQ15.$20.LpDqAqEpDIQpCpKpJpBQJpApCQKI12.$19.SpTqO2JWpSqTrTsMsLrSqSpWpHSpBpGpJXD10.$18.XqLrTKTpXrQtOvNxHyHyCwTvCtLsBqRpNQNUI10.$17.OqWsPSXqPwI9yOwDuArVqDXF11.$16.BqVsTqFOqPxB12yOvCsJqIXFN9.$15.KrAsTtIpMqEuLwIxKyB11yOvUsLqCqUsLpQD7.$14.NrJsBtBuTtUuWuKsQtDyJ12yOvNrIqLuTpNJA6.$14.qOqTqVrVvIwFvKqSpAvB14yOsIpGuOpR8.$13.QpHVpIqOtNrLN.pRxE6yOvVyF6yOtQpFDrC8.$13.QJDPrRO3.qTyM3yOxIsKI.tDxE6yOpJDpIC7.$13.UIFqIP4.rN3yOxPpE4.rE6yOuDDWE7.$12.G9.rG3yOvK3.pS2.qA5yOwXCpVC7.$22.qC3yOyNqF.pUtC.ApC6yOApLA7.$11.E10.tX2yOyNxXwVtRuI2.DpA5yOsN.E8.$11.H10.xRyKxVxAvVuXvAuKqR.FqM5yOtK.A8.$21.WrG.ApXqXrTtGvLwCtXsDuIyJyGyN2yOuA.J8.$10.F9.rXQ5.HpDsJvJvSrHCtDxFuTuHtIwVuGM8.$10.F8.rGvJ7.qDqC5.B.pLqOyOwC9.$9.CA8.uBqT7.PA8.pGxCM9.$9.IB8.sE19.A10.$9.rDpP17.qW9.ApL10.$8.tAtS12.AXpBA.qXtK10.wI10.$8.wKP2.B.pGrG11.qL10.MrO10.$7.NsV2.rKrVqDtFuTpT21.pK11.$7.qEpE.qTvHvFvHwHwNuJpH20.qT11.$7.rPQ.vDxWxQxDxJxPwLtDJ18.sAqL11.$6.CsUOpWxTyOyMyJ2yOxXuFpW18.qS12.$6.SsVpPqWyI6yOwArMqArVsWqMPpNqDpQ23.$5.FpNsBrErDxJ6yOxStXsMuGwEwFwQxPyLyOyHvQ21.$5.EpVsItUuUwR6yOyFvSvBwKxO6yOuS7.pC13.$6.pItCwQxWyK6yOyJwXxByH6yOxRT4.tIuMsE14.$6.BqKtTwLxU7yOyEyL7yOsL4.vUxGuPpP14.$7.EpNrJtXyN14yOvSQ3.tSuBrNqC15.$7.ApAqTsVvL14yOsB3.sOuDrNI16.$8.MpVrKtFvS12yOuUqGpArWuKuUtSrOM16.$8.CVpXrDsQvAyL9yOxSwQxGxVxDwIuFsBqAF16.$9.ESpMqJrOtMwC10yOxPwXwItHqBXN17.$10.CKVpMqLrTtKvBwLxOyE4yOyDvNtJqWTINB17.$12.CJTpKqHrGsFtCtR2uDvKuUsPqPpJTUpAI18.$14.BISpGpTqFqMqRqUqSqJpQUJNVL19.$16.CGMQSUVUOF24.$19.AB2CB26.$50.$50.$50.!",
    "29.ESNA17.$24.KH2.RqJqVqOpVK16.$22.GqFqSrIrRrTsAsMtDtJtAsKsCqWpVpMQA10.$20.CKqIrRrIrPrHpVpJsCvBvNuDW.rXuRrFqGpB10.$17.FpIpPpLqArWsP2sIrLpFIqUvXwBtR2.qAxCpUpOpPN9.$16.BpNpXqTsAtLuCsGrHrJsJA2.sXvKpS2.TuOyOwVtCrMpLMA6.$17.UpNqNtP2.GqMsPtK7.qVT3.pSvUvMqQVA5.$17.DMpFvQ13.wMuA5.xLtGqIS5.$16.BqGsEvNxW7.wFyM4.tPuA.DrM2.qPwWrApL5.$15.KsP3.DsGyOyMwL3.wDvP4.qK2.yOxTyO2.pNuXtJqTD3.$14.DrJQ5.yOwXyK3.uTuM3.uGuJ3.yGyO3.pPtQrT4.$14.MtKsJ7.pV8.pKrP8.MvIsRFE2.$14.qJvDwPuB2yOvJ22.2yOwJtApM2.$13.rIsTrM.VyOyDyO16.vPqI3.3yOrWvCI2.$19.uG3.qN5.vCtN7.tX3.2yO2.rFH2.$13.NL7.2yOuL3.WwKrX6.vMyM8.vB2.$13.2yOwM5.3yO23.sTtE.$13.5yOxH2.yDyO16.yOsB3.wOyOsOVpMR$16.qA2yOxDTJ16.xJ.tGsQ2.3yOrNVX$10.pPyO5.pXrTsCNC2.yOwG12.S.yOrR3.vCtAtWuMqR$10.2yO4.CqKpTK3.3yO13.QL6.vBuFpF$14.3yOvRVA3.2yO5.yOwC10.pIpM3.uVqSF$8.tM5.4yOA11.2yO9.C2yOuO2.uWqHF$7.qVtNyO5.2yO3.sB13.rOqC2.A2.O3yO.vTtOqMI$6.LyOyAyO10.sNqO5.F10.PpI2.sJuE2.uQrLpXB$20.wByN16.2yO6.sMVJ.$11.2yOwX2.wDA2.qQvU16.2yO6.pK3.$5.pMyO4.yOyMyO.tJtFpP17.pA2yO5.pPvQuFA3.$2.pA2.yOxPyO3.tVuR3.V13.B4.3yO3.J2yOxCqPB3.$2.qNrH.xC2yOR13.rB5.uBsAvC5.yO4.2yOxKG5.$.pGrVtCpA16.vRsE5.rPrFqH11.yOqH6.$LpOtBuCsX6.qX3yOqN5.pS10.pE2yO15.$2.tNtCyO3.tP3.X2yOrI16.yOqPyO3.2yOyD9.$2.tV2yO2.2yO23.wPyOvP3.yOwGwI9.$qJTsKuG2.yOxWyO9.sVvIrH2.pLsD14.tA10.$pFtIpP3.rDyOpS.pBvJ6.uDwDI2.pUyO3.2yO20.$.uTqD7.yO.qS5.tWpV8.3yO3.xF3yOwX11.$.tOtSpO6.xTwLpE15.3yO3.4yOtS11.$OtGuK2yOxP3.rLqH14.tLyOxFqO21.$TrErNxR2yO.IyOxD15.tGvXyO22.$AqOqEsGvB3.wTtWI10.rN4.uGtP3.2yO17.$.RsArUpK4.rR16.I3.4yOrBuSuUqB12.$2.IqVrID18.AxDuT4.uOuJtBxSvSpVH12.$3.pArGsQvKvBrN13.D3yOE7.qUuNrCJ12.$3.pIrXtPuTvQvA13.xRpQyAG3.Q4.DpU14.$3.pGsCsPuEvNsI13.qUxGX3.2yOxMqIqGrFrHpM14.$3.DqRqSqQrIpA18.xTyOxKuDyHwLtAsApNA13.$4.KqXrXsRsEpRCpOpG14.rS3.rRvRsBpVF14.$5.EqVsWuBuFtWtErFO2.pCpO9.pA3.KtApQ16.$7.pPrVtEtFsRrRqKpSqBqMrIrCKpBrRtCrJDpUtGvBuVrCsCtArGpNB15.$7.EpMqVrQsArWrAqHqDqApXqVrErCrOtCtFsEtWuNsFrApUM19.$9.BJMNOpApQqBpXpQpOpQqGrXsPsGtCtMsAqEK20.$16.DH3.FUpWqMqSqUqJpE21.!",
]
CELLS_B = [
    "77.$77.$34.pJqGpArFuXvMuHrDpOQ33.$32.GpQpDNpNuUpVNuEtLtCuDX32.$31.qStBuEsKrQ6.KrTyLyOsQ30.$28.EpFrMtX14.yEyOS28.$27.pLrNpT17.qQyOqU27.$26.qLxLtR14.tHpH3.sCvJpG26.$25.qAxOsWqS14.2yOrB3.tNtX26.$24.NvP18.yOxI3.ItVrB25.$23.BrStS3.F15.T4.rJsPpF24.$23.qWtD3.sEsI6.RwKxLsT11.sGsEB23.$22.xG5.qV6.rR4yOvI5.yOxM3.sPuMqS23.$22.yO12.7yO4.vJyO5.qIqE22.$22.tR11.qE7yOuV12.X21.$22.uA9.NyNUwO7yOsCsQ10.pT21.$20.uVyOvL9.SyOuT9yO11.qW21.$18.tKxJ12.tB11yOsF9.tMqA21.$17.yOwC13.yK11yOrN9.qEtHA20.$15.wNyOwMsT13.sF11yOwJ11.rDpP19.$14.vEyOrCpGrKqM13.vG10yO13.rLsTQA16.$13.yN2yO2.tAwWrU13.9yOG13.pUxXyOxNuOpF14.$12.2yOyK2yOwTuKwPrPA13.7yOtU15.sIvGuSxWyOvRpOWI10.$11.yKyO2.3yORJqHH14.4yOvWqA21.uOyOvPsRqVF8.$10.xR2yO2.3yOC18.vH2yOpI24.tGvFuHtGqG7.$8.uPyK2yOwI2.rWyOS20.vAyOvNpT13.qT2yOsH7.qOqSEqOrH6.$8.2yOwFrA27.rIuAsQ13.xT6yO4.qSpN2.rDQ5.$6.rGqEyOqC10.pBV18.K14.rHsEsVxT5yO2.uOsO3.rQ5.$5.tEvFyOpS9.rJwE2yOrL37.yM4yOpCsOyOG2.qSJ4.$5.rHP10.3yOuRvB3yO36.pExOyOrS6.pIO4.$5.B11.uDyOxL6yO45.JM4.$5.F12.KsWwM5yOuC29.qWyFyOvD13.G3.$5.vB12.PpO2.vQ5yO25.ExIvGxN5yOuA10.S3.$5.tW11.pLrLqI3.qKyOxQyOxTyO24.tK9yOxS9.GQ2.$5.sH11.rQuTvI4.yNxEyOyDyFpJ22.uJsG10yO10.U2.$5.sA11.pHyGyOxO3.5yO23.uByN10yOwO9.I2.$5.yJ12.10yO26.DtUyD8yO12.$5.xM12.8yOwL30.yM7yO12.$5.uW11.yE6yOxK16.A15.wA3yOxMxLyOqS12.$5.pFpL5.uE5.wU2yOyLyJ30.sJpUEwR4yOsEqTI9.C3.$6.yO5.wUsU5.qTyOxU31.2uC6yOsLO10.H3.$7.yO2.pXxJ2yOqI39.JuQ6yOJ9.pJ4.$7.H2yOuQwU3yOtF38.T.tM5yO2.2yOvMpN3.W5.$8.qQyOyNqJrA4yOvPrUI18.qQrBsE14.sFtKqXsCvOuG2.sN2yOxMsH3.I5.$9.vTyOrH2.xJ4yOtN17.rRxHyGyLvL21.vRuAqVpO4.E5.$10.wMyOrC2.uM3yOuF16.yG5yOtL19.wGvHpT4.KO6.$11.uI2yOA2.tEwWM14.8yOuT18.UxKxMsQ3.pAqE7.$13.2yO18.9yOvL18.GuOvXsPM2.sGF7.$14.wEyO16.9yOwVN17.pK2.qBrIqRrMsTpR8.$15.3yOqH13.4yOyDtDpVpUvKvJpV13.RyH2yOrD3.qJrJpGC9.$15.A3yO12.yK3yOyMrC2.rP3yOE12.N3.yOuGpNqJqD12.$16.ApDyOuK11.xX4yOtPrCrKwK4yO16.pDxJuWpP13.$17.FpXsEvL12.vO11yO11.pB20.$21.yO5.tLwH5.11yO11.yIwNqLqDB16.$21.wO5.pAyOyC4.xB6yOsD14.yI20.$21.qF6.qVsA5.5yOyC14.pL21.$22.qI6.K4.pMpQuEvMvHtW9.pUtU3yOrT22.$22.AyOtE4.A17.CBsTvCyOyH24.$23.sPxK3.XS15.2AT2.rDxNyO24.$24.tR3.QpOG11.G2yOpRpGO3.sFxT24.$24.qH3.AD12.3yOvAI2.IyBxF25.$25.pOpBXE3.CqNL6.4yOpO2.PyOyH26.$26.rNyOrX4.qLpQ6.BqPqI4.xSyO27.$28.yOB17.pLyOpE27.$29.xUqK15.sBxH29.$30.vGpS4.CB6.pRxT31.$31.xVJ.PtSuMvFvDqRpL2NuVvL32.$33.wCuIqXDrXtTtUtBqRqC34.$77.$77.$77.!",
    "77.$77.$77.$77.$77.$30.GQpOrIsPtArRpB2.E36.$28.pDrWvDyN4yOxArWpVsEwMyOxNtG33.$27.pTtNxU6yOwCpO.qSxW4yOsQ31.$26.pLsOwM7yOtF3.sX5yOtQ30.$25.XsCuN8yOsS4.6yOsSF28.$25.rFtRwF8yOwLrJ3.wG6yOsTL27.$25.rMuPxI4yOyCwOyOyMwUuWtTtGtQ8yOrQ27.$25.qWuXxW4yOwSwByOyHxRxLxTyH9yOwC27.$25.qHuVyD7yOyJxIxM12yO27.$25.TtOxH7yOyKvIvR12yOpJ26.$26.pDsAuJ6yOwXsWqOsSxU9yOwU27.$29.pVyC3yOwMtUqQ3.vK6yOyNwEpP27.$31.xXyOvMJ6.6yOtW29.$31.pVwWsV7.yL4yOvU30.$32.vFsJ6.W5yOqP30.$13.ItRqP16.qCuW6.rV4yOvI31.$13.rQuH18.uIrI5.uA3yOyDqL31.$34.tEqB3.pAuP2yOyMsO13.pOwHyOyEG14.$17.pKuQvIqN14.pKpMWqNrWtGtUrXA13.pPxU4yOtJpE12.$16.rF2yOyKrJ16.qTuFuDsLpU14.RxH2yOyMyJyKyOwHqNP10.$16.yAyOxIrH18.tCwBuIqM13.RyA8yOxPqWB9.$15.sBxJvC20.RvTvQqR13.yB10yOxBpO9.$15.tSwCqU3.qLuXtI15.rQrK13.uH12yOtL9.$15.sKxFxSwFwU5yOsD28.13yOyI9.$15.qQ10yO27.sG13yOyBqG8.$16.11yO26.uW12yOwUvRsE8.$16.yD10yO26.xN10yOuXpTpEqWrN8.$16.qU7yOxHrRpFqP25.9yOwBsE4.R8.$17.xS6yOqS2.pUpI23.pM2yOvBvVyFxDxAwUvDrU14.$17.xS6yOA2.VtN23.3yOpR.pMqQpTrArPqE14.$12.2pH2.qN7yOrW2.K24.3yOvQqK.X2.pBO14.$2.C8.yF3yOwG9yOrKB24.P4yOxRsJO.HpOO14.$2.LC6.tX14yOxBpP24.EwR4yOvNrVqOrGrPpW14.$2.J6.C15yOpB26.uE5yOvQuTvKuVsIpK2.RK9.$7.pIpLsO13yOrR28.qWxS3yOyMyJ3yOyGvEtCsLsGrEpF8.$7.rU12yOyMtH31.tQyOxPuCtWwW7yOxDuUsAM7.$7.KyK11yOpC33.wXyOxDwB10yOuWrF7.$8.qD11yO34.qF13yOxWtMpNA5.$8.BqL9yOvT18.2yOwGA13.vV13yOtWpR6.$10.pOwD7yOrR16.qD5yOtA12.F12yOwVsQpC6.$7.qKqB2.VsExB4yOrT15.rMxR7yOL12.qAxU9yOxPuMrAD6.$7.CqBqF2.JpUrStFrJ15.pF6yOyCyM2yOpB12.JtO8yOwAuCsKV7.$32.6yOxHvCuTxNyOS12.CrP6yOyFuVsVsFqE8.$3.JpX26.6yOyFwW2vKxWyOW12.DpKtH4yOwMuIsUsFrB9.$3.AqDrU25.4yOuTqMrT5yOwX14.HqOuDvBtTsNrSrUrC10.$4.RrUsR23.wR4yOtGpVBpCyK4yOtI15.FpPpSpJpSW11.$5.pKsDsNpE19.uGwLyJ4yOtBpB2.A5yOvD31.$6.QqGqNS16.sOxUyM7yOL3.tE4yOxWuXqO29.$8.MpFpED14.wK9yOT3.uO4yOwNtHvNtH28.$8.AMpJqApS13.vAyK3yOyN4yOtBRpDqPpCvHyOyJtW2.xHwMvN27.$12.E13.qTxG3yOwFxD3yOvVqSX3.qVsN3.yMxRwPsC26.$27.uC2yOyIqUsRyI2yO11.yOxQuN27.$24.qP3.uQyOxIpBqAwPyOxO6.rUqN2.qMyOwVpA2.qC24.$24.WsI2.pMwUyOtFrRwDyOyK5.sN3yOsM2yOvG2.yOyN24.$25.yOqA2.tP2yOxGxLxSvE5.7yOpO.XtVpI24.$25.2yO2.sHyE3yOuU5.wU6yOsI2.uE26.$25.rVyOrBpGsCvBxNyOxTuD5.qC4yOvHqT2.tDL26.$26.qSP.qEP2.rFvVvXqR5.EpFpLQ2.qHsB27.$34.tD2yOtU10.sD28.$35.tGwFtK9.L29.$77.$77.$77.$77.$77.$77.!",
    "31.pJsHsVtDsOqLpB39.$29.BrFuStV8.HqNrGT32.$27.pXqOuAvSsN12.XsQrJA29.$25.GtFqH18.sHuLA28.$25.qMwDsR19.uBwFrS27.$24.sGvUxTpG20.rJsOsE26.$23.sCqW8.pGS16.sU25.$23.uIE4.sPrLqRqNvUvJpJ6.CqDT5.qPyOS24.$22.JvO4.KyHwDpP.VR8.uEtEpP4.qTyOrF24.$21.rLuRtA6.H12.rQxDtIQ4.vMxKpD23.$19.VrC4.qVyOxW16.qXuEqI5.rOpN23.$18.TrVsU5.yOyAFpJpG3.TtQyM2yOwJpL5.pDqKX3.TS23.$17.QqLsLxJ7.pUsBrAJ.BuG6yOtM4.GsLuMqB3.C23.$17.pKrPvUxVsU6.qUtOsNpCLsM8yOvOpVE.pFsAyOuC27.$17.pM3.uUuP5.qCuMtQrBsPyF2yOyDxV5yOwFrVqSrTrWyOvG27.$17.L4.tTrX.GH2.sGtJuExG2yOxNvXuQuNwG4yOvVsRrQrDuCsS27.$18.uS7.C3.qEuNyNyOyHwKtJqOqIsNvWyL2yOwQsXCpCPL27.$17.tByOxF11.tKyNyOyJwDrK2.rBuVxU2yOwXqG31.$18.vI13.xS2yOwTrN.DrSvMyD2yOwD3.VpI27.$14.FyL16.rJyLyOyFtXqNqWtUwV3yOrE3.qUU27.$12.BrL.yO17.uC2yOxXvUvLwTyM2yOxX4.pFpA10.HLNWqIWG10.$13.2yOwB18.tJ5yOyMxSwKrR3.qQR11.pOqRqOrFuIyCvTuPsD8.$8.CpPsX7.yDyO16.uPxBwAsKqWpH4.tCtP11.ErPsFP2.wGyOtL.qBrD6.$8.xD.qOsT6.3yO25.tLqL11.pMsUsE8.wBqR5.$9.2yOyB3.pSsMrGvByOvSqE36.QqGsJrI8.sAyHsH4.$14.wJyOETrMsVsMV34.pFsAqRqGqOqGpKI7.sVwFsH3.$6.yO7.yOxR.AHFB19.CrHsLpP11.pHtFvLqO3.pBuRuPrRJ6.rBpK2.$5.yCyO26.G21.sKvQqI5.qJvBvNsFL6.tT2.$5.uS4.uVyOsF3.EL4.rBxKsX8.XK29.BtRvArE6.wD2.$10.yEyKyO2.GvWxWvVqGApE3yOrR8.PT3.yOtX19.qMpN4.vQtNS5.wNsJ.$11.wTrX2.qJ3yOyEtNsPvS3yO13.xQtAtX16.rFvNxTvQpX3.DsTV5.qOtU.$3.qFyO11.xM2yOxKG3.vGyM6.vDV6.tUsH15.vP4yOuG12.qX.$4.yOpL10.uU2yOsF11.3yO.pH20.tJ6yOrP11.sCpF$2.pGyNuJ4.2yO5.uJyOxP7.pWpK3.yDpLsC.tPsO4.V13.yN2yOyIxIyK2yOyBrJ10.vDrR$.pHqO6.xXyO5.xMyOvB7.xTyON9.pCuVrTqO12.rI2yOwXuBuPvNxM2yOxBsXP8.uVsS$.U9.X4.2yOuQ7.2yOM8.qUsD15.wM2yOuTtOuUvKwN3yOxHtE8.rRqT$M2.pO7.wEwH2.pM2yOxMsD18.sAxVrQpKA.sCqF7.pOwOyOwSuBuXvDvPwQyJ3yOwG8.pTqE$pJsUvVuWyOvW5.2yOvX2.vK3yOsH2.2yO19.pML8.uBwMvNtNuVuTvEwKyM3yOvN8.qNsN$qDvBvT2yO6.yNyOuH3.wK3yOrJqNyOvF8.ItPpL18.rIvWwJtWtS2uHvS3yOyKqK8.rVtC$WsH9.rVyNN4.uJxLwMqO2.D8.vR2yOrArI2yOtN13.pTxDyOxLvHuFuJwK3yOwO9.qHsH$BpW6.xJyO23.wIyOvCpWsG2yOrC13.pMyB2yOxQwOxD3yOyEqJ9.BpO$.GrT5.2yO20.qN24.tM7yOyMtN9.pMQ.$.qOqUyE2yO8.yOuKpAqPR11.qQ25.rJ5yOxAsXpE3.J4.qCuGsF.$3.FxTyO8.2yOtLsQpG38.qAvDxBwCtRrGpJCQU2yOpM3.qGvCsSG$4.2yO3.2yOrF2.uVyOsFqSwCyOF19.sVpI17.pFqDqFpWpEpTqKqN2yOJ4.uLqX.$4.vR4.2yOpX6.wIyD18.pJ2yOwE18.FWpMpSrOsRpK7.rGN.$3.rAvBqA3.yEtL24.FNpKsE2yOrA18.GSXpR2yO8.pI2.$3.JrLtL2.tLrB23.xL2yOxPvBtHvGwAH18.tKA2.sWtE5.sIsQqGO2.$4.ErPuSwKxF4.2yO17.sD3yOtMqCpSqRuFsX17.rN2yO8.qOvKtTpX3.$5.pBqOsLtX3.U2yO17.uS2yOvL4.tLyDsB17.vMuI6.GUrBtCqJ4.$6.FQpIqVpEqV2yO18.rR2yOW4.sA2yOxE23.tMuOrTpXpM5.$9.IqLrUuGuA18.JxBvX5.tP3yOyLrKqES18.HuDtFrGX6.$10.UpLqRrN.pP11.wRrL4.wTxOtS4.wV4yOxF2yOqS13.rOuSsOKJqVpJ8.$10.AECA12.qRyOyK4.xN2yOwOsLsCwI4yOqBqR3yO8.A4.uJtJuArCpBR9.$27.2yOpM3.xE9yO3.tT2yOpX7.qCrT3.rNrJqOpMA10.$21.uHF4.wJwXqN3.vG8yOpP3.WyOxBA2.sCwRN3.sOtKpBOWOC12.$16.I4.rSuS4.sJvCrC3.pJwTyJ4yOyIvB4.KyDtH4.2yOsU.qDrIpUpE16.$21.tP5.rDvSsK8.NrKsC5.pDvSrO5.tNvTrQrApQV17.$21.uJ5.XyNxNpI11.S2.BqRvQyOxW5.pCpODCB17.$22.F.O3.wDyOtA10.vJ3yOrMqWsB2yO6.M20.$22.pEyOyJpX3.sTsBqAI8.vJ3yOqF2.pD3.2yOqCJ21.$24.pHyO6.B2yO7.rRwEuI7.vS24.$25.yO7.2yOqO16.tM24.$24.MpRT7.yOsD12.pN28.$26.wIyOtM18.sPyCyD27.$25.GrOvSyO18.tBqP28.$25.DX.xV48.$31.yHyOrI8.vB2yO32.$32.uAyO3.xGyO3.vEqER32.$34.qO.GyKqRyO3.uRsL32.$37.qV2.qPpEqEqSqC32.!",
]
N_A, N_B = 1, 1
FOOD = {'Y': 2, 'rho': 0.01, 'D': 2}
EXCL = 1.0
import json as _json, os as _os  # noqa: E402
P = dict(PRATE=0.5, PRED=0, YB=1.0, PSIG=4.0, T_INTRO=-1.0, DECB=-1.0, DOMAIN=160, DECAY=0.01, SEP=0, EXCL=1.0, RHO=0.03, FORK="none", T_FORK=-1.0, CUT_R=20)
P.update(_json.loads(_os.environ.get("WORLD_P", "{}")))
FOOD["rho"] = P["RHO"]
META["size"] = (int(P["DOMAIN"]), int(P["DOMAIN"]))
EXCL = 0.0 if P["SEP"] else P["EXCL"]
JITTER = 0.05


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


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    placed = []
    A = _place(np.zeros((3, H, W)), _creature(CELLS_A), N_A, rng, placed)
    B = _place(np.zeros((3, H, W)), _creature(CELLS_B), N_B, rng, placed)
    if P["T_INTRO"] >= 0:
        B[:] = 0
    A = np.clip(A * (1 + JITTER * rng.standard_normal(A.shape)), 0, 1)
    B = np.clip(B * (1 + JITTER * rng.standard_normal(B.shape)), 0, 1)
    ky = 2 * np.pi * np.fft.fftfreq(H)[:, None]
    kx = 2 * np.pi * np.fft.rfftfreq(W)[None, :]
    return {"A": A, "B": B, "F": np.full((H, W), FOOD.get("F0", 1.0)), "FB": np.full((H, W), FOOD.get("F0", 1.0)),
            "t": 0.0, "cut": None, "lapK": -(kx ** 2 + ky ** 2),
            "LA": Lenia(RULE_A, 3, size, R, T), "LB": Lenia(RULE_B, 3, size, R, T)}


def _fork(s):
    from scipy import ndimage
    H, W = s["F"].shape
    if P["FORK"] == "food":
        s["F"][:] = 0
        s["FB"][:] = 0
        FOOD["rho"] = 0.0
    elif P["FORK"] in ("cutA", "cutB"):
        X = s["A"] if P["FORK"] == "cutA" else s["B"]
        lab, n = ndimage.label(X[0] > 0.35)
        if n:
            ids = np.arange(1, n + 1)
            area = ndimage.sum(np.ones_like(X[0]), lab, ids)
            ok = ids[area >= 20]
            if len(ok):
                j = ok[np.argsort(area[ok - 1])[len(ok) // 2]]
                cy, cx = [float(v) for v in ndimage.center_of_mass(lab == j)]
                yy = np.minimum(np.abs(np.arange(H) - cy), H - np.abs(np.arange(H) - cy))[:, None]
                xx = np.minimum(np.abs(np.arange(W) - cx), W - np.abs(np.arange(W) - cx))[None, :]
                s["cut"] = (yy ** 2 + xx ** 2) <= P["CUT_R"] ** 2
                s["cut_center"] = (cy, cx)


def step(s):
    dt = 0.1
    s["t"] += dt
    if P["T_FORK"] >= 0 and abs(s["t"] - P["T_FORK"]) < dt / 2:
        _fork(s)
    if P["T_INTRO"] >= 0 and abs(s["t"] - P["T_INTRO"]) < dt / 2:  # plant the predator on the A colony
        from scipy import ndimage
        lab, n = ndimage.label(s["A"][0] > 0.35)
        if n:
            cy, cx = [int(v) for v in ndimage.center_of_mass(s["A"][0] > 0.35)]
            cr = _creature(CELLS_B)
            H, W = s["A"].shape[1:]
            pad = np.pad(cr, ((0, 0), (0, H - cr.shape[1]), (0, W - cr.shape[2])))
            s["B"] = np.maximum(s["B"], np.roll(pad, (cy - cr.shape[1] // 2, cx - cr.shape[2] // 2), (1, 2)))
    A, B, F = s["A"], s["B"], s["F"]
    occA, occB = np.clip(A.sum(0), 0, 1), np.clip(B.sum(0), 0, 1)
    incs, decs = [], []
    for X, L, occ_other in ((A, s["LA"], occB), (B, s["LB"], occA)):
        G = L.growth(X)
        inc = np.clip(np.minimum(dt * G, 1 - X), 0, None) * (1 - occ_other) ** EXCL
        incs.append(inc)
        decs.append(np.clip(dt * G, None, 0))
    dk = dt * P["DECAY"]
    if P["PRED"] == 2:  # B is an omnivore: it builds from A's nearby matter first (at most PRATE of the
        # local prey per unit time), the rest from the shared food; A is excluded by B as before
        from scipy import ndimage
        sig = P["PSIG"]
        incA, incB = incs
        Sav = ndimage.gaussian_filter(A.sum(0), sig, mode="wrap")
        needB = incB.sum(0) / P["YB"]
        fromP = np.minimum(needB, dt * P["PRATE"] * Sav)
        frac = np.clip(fromP / np.maximum(Sav, 1e-12), 0, 1)
        take = np.clip(ndimage.gaussian_filter(frac, sig, mode="wrap"), 0, 1)
        restB = (needB - fromP) * P["YB"] / FOOD["Y"]  # remaining B growth, in food units
        needA = incA.sum(0) / FOOD["Y"]
        need = needA + restB
        scale = np.minimum(1, F / np.maximum(need, 1e-12))
        builtB = fromP * P["YB"] + restB * FOOD["Y"] * scale          # B matter built per pixel
        scB = np.where(incB.sum(0) > 0, builtB / np.maximum(incB.sum(0), 1e-12), 0)
        s["A"] = np.clip(A + incA * scale + decs[0] - dk * A - A * take, 0, 1)
        s["B"] = np.clip(B + incB * np.clip(scB, 0, 1) + decs[1] - dk * B, 0, 1)
        F = F - need * scale + dt * FOOD["rho"] * (FOOD.get("Fmax", 1.0) - F)
        F = _irfft2(_rfft2(F) / (1 - dt * FOOD["D"] * s["lapK"]), F.shape)
        F = np.clip(F, 0, None)
        if s["cut"] is not None:
            F[s["cut"]] = 0
        s["F"] = F
        s["eaten"] = s.get("eaten", 0.0) + float((A * take).sum())
        return s
    if P["PRED"]:  # B is a predator: it builds only from A's matter within a Gaussian neighbourhood (mass-conserving)
        from scipy import ndimage
        sig = P["PSIG"]
        incB = np.clip(np.minimum(dt * s["LB"].growth(B), 1 - B), 0, None)  # B is not excluded by A
        Atot = A.sum(0)
        Sav = ndimage.gaussian_filter(Atot, sig, mode="wrap")
        needB = incB.sum(0) / P["YB"]
        scB = np.minimum(1, Sav / np.maximum(needB, 1e-12))
        frac = np.clip(needB * scB / np.maximum(Sav, 1e-12), 0, 1)        # share of the local prey taken
        take = ndimage.gaussian_filter(frac, sig, mode="wrap")             # adjoint of the blur
        needA = incs[0].sum(0) / FOOD["Y"]
        scA = np.minimum(1, F / np.maximum(needA, 1e-12))
        s["A"] = np.clip(A + incs[0] * scA + decs[0] - dk * A - A * np.clip(take, 0, 1), 0, 1)
        dkB = dt * (P["DECB"] if P["DECB"] >= 0 else P["DECAY"])
        s["B"] = np.clip(B + incB * scB + decs[1] - dkB * B, 0, 1)
        F = F - needA * scA + dt * FOOD["rho"] * (FOOD.get("Fmax", 1.0) - F)
        F = _irfft2(_rfft2(F) / (1 - dt * FOOD["D"] * s["lapK"]), F.shape)
        F = np.clip(F, 0, None)
        if s["cut"] is not None:
            F[s["cut"]] = 0
        s["F"] = F
        s["eaten"] = s.get("eaten", 0.0) + float((A * np.clip(take, 0, 1)).sum())
        return s
    if P["SEP"]:  # each species eats its own food field
        FB = s["FB"]
        needA, needB = incs[0].sum(0) / FOOD["Y"], incs[1].sum(0) / FOOD["Y"]
        scA = np.minimum(1, F / np.maximum(needA, 1e-12))
        scB = np.minimum(1, FB / np.maximum(needB, 1e-12))
        s["A"] = np.clip(A + incs[0] * scA + decs[0] - dk * A, 0, 1)
        s["B"] = np.clip(B + incs[1] * scB + decs[1] - dk * B, 0, 1)
        out = []
        for Fx, nd, sc in ((F, needA, scA), (FB, needB, scB)):
            Fx = Fx - nd * sc + dt * FOOD["rho"] * (FOOD.get("Fmax", 1.0) - Fx)
            Fx = _irfft2(_rfft2(Fx) / (1 - dt * FOOD["D"] * s["lapK"]), Fx.shape)
            Fx = np.clip(Fx, 0, None)
            if s["cut"] is not None:
                Fx[s["cut"]] = 0
            out.append(Fx)
        s["F"], s["FB"] = out
        return s
    need = (incs[0].sum(0) + incs[1].sum(0)) / FOOD["Y"]
    scale = np.minimum(1, F / np.maximum(need, 1e-12))
    s["A"] = np.clip(A + incs[0] * scale + decs[0] - dk * A, 0, 1)
    s["B"] = np.clip(B + incs[1] * scale + decs[1] - dk * B, 0, 1)
    F = F - need * scale + dt * FOOD["rho"] * (FOOD.get("Fmax", 1.0) - F)
    F = _irfft2(_rfft2(F) / (1 - dt * FOOD["D"] * s["lapK"]), F.shape)
    F = np.clip(F, 0, None)
    if s["cut"] is not None:
        F[s["cut"]] = 0
    s["F"] = F
    return s


def fields(s):
    return np.concatenate([s["A"], s["B"], s["F"][None]])


def damage(s, mask):
    s["A"][:, mask] = 0
    s["B"][:, mask] = 0
    return s
