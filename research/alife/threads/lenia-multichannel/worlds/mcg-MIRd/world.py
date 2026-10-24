"""mcg-MIRd: food-limited, cycling MIRd+ replicators with a heritable trait (sprint 2).

Base: mcfd-MIRd (Chan's MIRd+ #1130; matter built from a regrowing, diffusing food field F with yield Y;
all matter decays at rate `decay` and must be rebuilt). New: a trait field g(x) carried by matter.
  * inheritance: matter built at x takes the trait g_loc = blur(g*M)/blur(M) of the matter around x
    (Gaussian, SIG_INH px, i.e. within a cell); surviving matter keeps its g; so daughters inherit.
  * mutation: replication-error events at rate MU per step: pick a random location with matter and
    add delta ~ N(0, DELTA) to g inside a disk of radius MUT_R (about a cell core).
  * phenotype: local yield Y_eff = Y * exp(SEL * g). SEL=0 is the neutral control (same mutations).
Rendered extra channels: g+ = max(g,0)*mask, g- = max(-g,0)*mask (mask = matter > 0.15).
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


from labkit import ops  # noqa: E402  (only for disk masks in damage)

META = {
    "name": "mcg-MIRd",
    "family": "lenia",
    "parent": "mcfd-MIRd + heredity mechanism forked from active-droplets (ad5-evolve: body-confined alleles, droplet-scale mutation events)",
    "mutation": "heritable trait field g carried by matter: new matter copies the local g of existing matter; rare cell-scale mutation events; g sets food yield Y*exp(SEL*g) (SEL=0: neutral control)",
    "size": (160, 160),
    "steps_per_frame": 20,
    "dt": 0.1,
    "channels": ["A0", "A1", "A2", "F", "g+", "g-"],
    "matter": [0],
}

R, T = 15, 10
RULE = [
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
CELLS = [
    "50.$50.$50.$50.$50.$50.$50.$50.$50.$25.BGKLJB19.$23.E3.E2.pCG18.$19.BEH4.qDtGqOIqNR18.$17.DrKsX6.rJuVsOpWqXuWB17.$17.rWqX6.EpVqUpDBApLsGH16.$24.ABABHNOJ2.Q2G13.$24.INLUpVrBqWpOA2.qBTA12.$24.pMrIqVrNtFuLuBrOP.AMtNpH12.$23.BrGyNuEuBuFuLuFsGpKABVX.G11.$23.IwOyOwCtBsKsVtWtCqJJ.D14.$23.PvXyOwVqKqAsIwNwOsJU16.$21.qUtJsWvLyOvUSpDuH2yOvOpF5.A10.$21.pIuGwIxGyOwQIqIxX2yOxWpO5.pB10.$21.pCuRxGxNyNyBpNsR3yOxDpN5.pV10.$20.BrLvJxPyHyLyEwN3yOvCrQD6.D9.$20.qTtVwCxLyByCxSyC2yOpD9.pB9.$19.qAtNvLwPxBwRvRwSxQyCxH9.sDtFA8.$19.tWvTwNwWwFtKsXvTxHxKvF9.uCtM9.$19.wAxIxJwWvKuDvGwQxEwKtD20.$19.wLyByAxHwCvUwQxBwMuTqN20.$19.xAyLyMyDxLxGxIwXvWtTT20.$19.xN2yOyNyFxVxNwWvOsS21.$19.yG3yOyJxXxGwCuCqM21.$18.rR4yOyMyBwWuPrM22.$15.CpGrFvN5yOyJwWtL23.$15.LrCuX7yOxCpH23.$15.PsAxA7yOuL24.$15.JrKwG4yOwMtIvFsB24.$15.CqFuDxIyOyMwLtSsCsFsG24.$10.TqR3.ApKsDuLvPvKtXsFrGsEsFB23.$8.BKpBqWpB2.FpHqUsBsTsXsKrOrFrNqUH23.$8.ACEpKHTqGrBqAqB2qGqRrMrTrQqXpI24.$11.RBRvByOvQtBqIUpGqMqLpPpCE24.$11.GpEpUuDwXsQrXtQtWrJpIM27.$12.UqCrNqXKOrSyNyOqV28.$12.BVqApWBEpAwPyAsM28.$14.JpIqJpSpPrErHpKCG26.$15.APpXqBS2.QpSpC25.$17.BON.DPLI25.$50.$50.$50.$50.$50.!",
    "50.$50.$50.$50.$50.$50.$22.AITpFpKpFQNTXTG16.$21.FPpFpUqHqIqApGORpLpSpJQ15.$20.LpDqAqEpDIQpCpKpJpBQJpApCQKI12.$19.SpTqO2JWpSqTrTsMsLrSqSpWpHSpBpGpJXD10.$18.XqLrTKTpXrQtOvNxHyHyCwTvCtLsBqRpNQNUI10.$17.OqWsPSXqPwI9yOwDuArVqDXF11.$16.BqVsTqFOqPxB12yOvCsJqIXFN9.$15.KrAsTtIpMqEuLwIxKyB11yOvUsLqCqUsLpQD7.$14.NrJsBtBuTtUuWuKsQtDyJ12yOvNrIqLuTpNJA6.$14.qOqTqVrVvIwFvKqSpAvB14yOsIpGuOpR8.$13.QpHVpIqOtNrLN.pRxE6yOvVyF6yOtQpFDrC8.$13.QJDPrRO3.qTyM3yOxIsKI.tDxE6yOpJDpIC7.$13.UIFqIP4.rN3yOxPpE4.rE6yOuDDWE7.$12.G9.rG3yOvK3.pS2.qA5yOwXCpVC7.$22.qC3yOyNqF.pUtC.ApC6yOApLA7.$11.E10.tX2yOyNxXwVtRuI2.DpA5yOsN.E8.$11.H10.xRyKxVxAvVuXvAuKqR.FqM5yOtK.A8.$21.WrG.ApXqXrTtGvLwCtXsDuIyJyGyN2yOuA.J8.$10.F9.rXQ5.HpDsJvJvSrHCtDxFuTuHtIwVuGM8.$10.F8.rGvJ7.qDqC5.B.pLqOyOwC9.$9.CA8.uBqT7.PA8.pGxCM9.$9.IB8.sE19.A10.$9.rDpP17.qW9.ApL10.$8.tAtS12.AXpBA.qXtK10.wI10.$8.wKP2.B.pGrG11.qL10.MrO10.$7.NsV2.rKrVqDtFuTpT21.pK11.$7.qEpE.qTvHvFvHwHwNuJpH20.qT11.$7.rPQ.vDxWxQxDxJxPwLtDJ18.sAqL11.$6.CsUOpWxTyOyMyJ2yOxXuFpW18.qS12.$6.SsVpPqWyI6yOwArMqArVsWqMPpNqDpQ23.$5.FpNsBrErDxJ6yOxStXsMuGwEwFwQxPyLyOyHvQ21.$5.EpVsItUuUwR6yOyFvSvBwKxO6yOuS7.pC13.$6.pItCwQxWyK6yOyJwXxByH6yOxRT4.tIuMsE14.$6.BqKtTwLxU7yOyEyL7yOsL4.vUxGuPpP14.$7.EpNrJtXyN14yOvSQ3.tSuBrNqC15.$7.ApAqTsVvL14yOsB3.sOuDrNI16.$8.MpVrKtFvS12yOuUqGpArWuKuUtSrOM16.$8.CVpXrDsQvAyL9yOxSwQxGxVxDwIuFsBqAF16.$9.ESpMqJrOtMwC10yOxPwXwItHqBXN17.$10.CKVpMqLrTtKvBwLxOyE4yOyDvNtJqWTINB17.$12.CJTpKqHrGsFtCtR2uDvKuUsPqPpJTUpAI18.$14.BISpGpTqFqMqRqUqSqJpQUJNVL19.$16.CGMQSUVUOF24.$19.AB2CB26.$50.$50.$50.!",
    "29.ESNA17.$24.KH2.RqJqVqOpVK16.$22.GqFqSrIrRrTsAsMtDtJtAsKsCqWpVpMQA10.$20.CKqIrRrIrPrHpVpJsCvBvNuDW.rXuRrFqGpB10.$17.FpIpPpLqArWsP2sIrLpFIqUvXwBtR2.qAxCpUpOpPN9.$16.BpNpXqTsAtLuCsGrHrJsJA2.sXvKpS2.TuOyOwVtCrMpLMA6.$17.UpNqNtP2.GqMsPtK7.qVT3.pSvUvMqQVA5.$17.DMpFvQ13.wMuA5.xLtGqIS5.$16.BqGsEvNxW7.wFyM4.tPuA.DrM2.qPwWrApL5.$15.KsP3.DsGyOyMwL3.wDvP4.qK2.yOxTyO2.pNuXtJqTD3.$14.DrJQ5.yOwXyK3.uTuM3.uGuJ3.yGyO3.pPtQrT4.$14.MtKsJ7.pV8.pKrP8.MvIsRFE2.$14.qJvDwPuB2yOvJ22.2yOwJtApM2.$13.rIsTrM.VyOyDyO16.vPqI3.3yOrWvCI2.$19.uG3.qN5.vCtN7.tX3.2yO2.rFH2.$13.NL7.2yOuL3.WwKrX6.vMyM8.vB2.$13.2yOwM5.3yO23.sTtE.$13.5yOxH2.yDyO16.yOsB3.wOyOsOVpMR$16.qA2yOxDTJ16.xJ.tGsQ2.3yOrNVX$10.pPyO5.pXrTsCNC2.yOwG12.S.yOrR3.vCtAtWuMqR$10.2yO4.CqKpTK3.3yO13.QL6.vBuFpF$14.3yOvRVA3.2yO5.yOwC10.pIpM3.uVqSF$8.tM5.4yOA11.2yO9.C2yOuO2.uWqHF$7.qVtNyO5.2yO3.sB13.rOqC2.A2.O3yO.vTtOqMI$6.LyOyAyO10.sNqO5.F10.PpI2.sJuE2.uQrLpXB$20.wByN16.2yO6.sMVJ.$11.2yOwX2.wDA2.qQvU16.2yO6.pK3.$5.pMyO4.yOyMyO.tJtFpP17.pA2yO5.pPvQuFA3.$2.pA2.yOxPyO3.tVuR3.V13.B4.3yO3.J2yOxCqPB3.$2.qNrH.xC2yOR13.rB5.uBsAvC5.yO4.2yOxKG5.$.pGrVtCpA16.vRsE5.rPrFqH11.yOqH6.$LpOtBuCsX6.qX3yOqN5.pS10.pE2yO15.$2.tNtCyO3.tP3.X2yOrI16.yOqPyO3.2yOyD9.$2.tV2yO2.2yO23.wPyOvP3.yOwGwI9.$qJTsKuG2.yOxWyO9.sVvIrH2.pLsD14.tA10.$pFtIpP3.rDyOpS.pBvJ6.uDwDI2.pUyO3.2yO20.$.uTqD7.yO.qS5.tWpV8.3yO3.xF3yOwX11.$.tOtSpO6.xTwLpE15.3yO3.4yOtS11.$OtGuK2yOxP3.rLqH14.tLyOxFqO21.$TrErNxR2yO.IyOxD15.tGvXyO22.$AqOqEsGvB3.wTtWI10.rN4.uGtP3.2yO17.$.RsArUpK4.rR16.I3.4yOrBuSuUqB12.$2.IqVrID18.AxDuT4.uOuJtBxSvSpVH12.$3.pArGsQvKvBrN13.D3yOE7.qUuNrCJ12.$3.pIrXtPuTvQvA13.xRpQyAG3.Q4.DpU14.$3.pGsCsPuEvNsI13.qUxGX3.2yOxMqIqGrFrHpM14.$3.DqRqSqQrIpA18.xTyOxKuDyHwLtAsApNA13.$4.KqXrXsRsEpRCpOpG14.rS3.rRvRsBpVF14.$5.EqVsWuBuFtWtErFO2.pCpO9.pA3.KtApQ16.$7.pPrVtEtFsRrRqKpSqBqMrIrCKpBrRtCrJDpUtGvBuVrCsCtArGpNB15.$7.EpMqVrQsArWrAqHqDqApXqVrErCrOtCtFsEtWuNsFrApUM19.$9.BJMNOpApQqBpXpQpOpQqGrXsPsGtCtMsAqEK20.$16.DH3.FUpWqMqSqUqJpE21.!",
]
N_SEED = 1
C = 3
NOISE = 0.6
JITTER = 0.05   # multiplicative noise on planted creatures, so seeds differ beyond exact symmetries
# Optional metabolism: food field F (diffusing with D, regrowing at rate rho toward Fmax).
#  mode "conserve": matter can only be built from local food (yield Y); see step().
#  otherwise ("gate"): positive growth multiplied by F^gate, eating at eat*mass*F, starving at starve*(1-F).
FOOD = {'mode': 'conserve', 'Y': 2, 'rho': 0.02, 'D': 2, 'decay': 0.03}



SEL = 1.0         # selection strength on yield; 0 = neutral control
MU = 0.012        # mutation events per step
DELTA = 0.5       # mutation size (std of the trait jump)
MUT_R = 8         # mutation disk radius (px), about a cell core
SIG_INH = 3.0     # inheritance blur (px)
G_CLIP = 2.0
GENE_MODE = "yield"   # "yield": g sets food yield; "m": g shifts the growth centre m of kernels GENE_K
GENE_K = [0, 3, 6]    # kernels whose m is shifted by ALPHA*g in mode "m"
ALPHA = 0.01
ONE_SIDED = True      # yield = Y*exp(SEL*min(g, 0)): wild type optimal, mutations can only hurt (False: two-sided)
TRADEOFF = False      # True: g also scales the maintenance decay by exp(SEL*g) (cheap building, fast turnover)
G_INIT = [0.0]        # trait of each planted creature (competition assays plant several kinds)


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    cr = _creature(CELLS)
    A = np.zeros((len(CELLS), H, W))
    g0 = np.zeros((H, W))
    y0, x0 = int(rng.integers(0, H)), int(rng.integers(0, W))
    for i, gv in enumerate(G_INIT):   # one planted creature per entry, spread around the torus
        y, x = (y0 + i * H // max(len(G_INIT), 1)) % H, (x0 + i * W // 2) % W
        c = np.rot90(cr, int(rng.integers(4)), axes=(1, 2))
        ci = np.roll(np.pad(c, ((0, 0), (0, H - c.shape[1]), (0, W - c.shape[2]))), (y, x), (1, 2))
        g0 = np.where(ci.sum(0) > 0, gv, g0)
        A = np.maximum(A, ci)
    A = np.clip(A * (1 + JITTER * rng.standard_normal(A.shape)), 0, 1)
    ky = 2 * np.pi * np.fft.fftfreq(H)[:, None]
    kx = 2 * np.pi * np.fft.rfftfreq(W)[None, :]
    r = _radial(H, W)
    Kg = np.exp(-r ** 2 / (2 * SIG_INH ** 2))
    return {"A": A, "L": Lenia(RULE, C, size, R, T), "F": np.full((H, W), FOOD.get("F0", 1.0)),
            "lapK": -(kx ** 2 + ky ** 2), "Kg": _rfft2(Kg / Kg.sum()), "g": g0,
            "rng": np.random.default_rng(10_000 + seed), "t": 0}


def step(s):
    L, A, F, g = s["L"], s["A"], s["F"], s["g"]
    H, W = F.shape
    M = A.sum(0)
    # local inherited trait of the matter around each pixel
    gl = _irfft2(_rfft2(g * M) * s["Kg"], (H, W)) / np.maximum(_irfft2(_rfft2(M) * s["Kg"], (H, W)), 1e-6)
    if GENE_MODE == "m":   # parameter localization: the trait shifts kernel growth centres
        U = _irfft2(_rfft2(A)[L.src] * L.Kf, (H, W))
        sel = np.zeros((len(L.src), 1, 1))
        sel[GENE_K] = 1.0
        mloc = L.m + SEL * ALPHA * sel * np.clip(gl, -G_CLIP, G_CLIP)[None]
        Gk = _growth(U, mloc, L.s) * L.w[:, None, None]
        G = np.zeros_like(A)
        np.add.at(G, L.dst, Gk)
    else:
        G = L.growth(A)
    inc = np.clip(np.minimum(L.dt * G, 1 - A), 0, None)
    dk = FOOD.get("decay", 0.0) * (np.exp(SEL * np.clip(gl, -G_CLIP, G_CLIP)) if TRADEOFF else 1.0)
    dec = np.clip(L.dt * G, None, 0) - L.dt * dk * A
    Yeff = FOOD["Y"] * np.exp(SEL * np.clip(gl, -G_CLIP, 0.0 if ONE_SIDED else G_CLIP)) if GENE_MODE == "yield" else FOOD["Y"]
    need = inc.sum(0) / Yeff
    scale = np.minimum(1, F / np.maximum(need, 1e-12))
    built = inc * scale
    A_new = np.clip(A + built + dec, 0, 1)
    M_new = A_new.sum(0)
    b = built.sum(0)
    kept = np.clip(M_new - b, 0, None)
    g = np.where(M_new > 1e-6, (g * kept + gl * np.minimum(b, M_new)) / np.maximum(kept + np.minimum(b, M_new), 1e-9), gl)
    # replication-error mutation events at the scale of a cell core
    rng = s["rng"]
    if rng.random() < MU * 1.0:
        ys, xs = np.nonzero(M_new > 0.3)
        if len(ys):
            k = int(rng.integers(len(ys)))
            yy = np.minimum(np.abs(np.arange(H) - ys[k]), H - np.abs(np.arange(H) - ys[k]))[:, None]
            xx = np.minimum(np.abs(np.arange(W) - xs[k]), W - np.abs(np.arange(W) - xs[k]))[None, :]
            disk = yy ** 2 + xx ** 2 <= MUT_R ** 2
            g = np.where(disk, g + rng.normal(0, DELTA), g)
    s["g"] = np.clip(g, -G_CLIP, G_CLIP)
    F = F - need * scale + L.dt * FOOD["rho"] * (FOOD.get("Fmax", 1.0) - F)
    F = _irfft2(_rfft2(F) / (1 - L.dt * FOOD["D"] * s["lapK"]), F.shape)
    s["F"] = np.clip(F, 0, None)
    s["A"] = A_new
    s["t"] += 1
    return s


def fields(s):
    mask = s["A"].sum(0) > 0.15
    g = s["g"]
    return np.concatenate([s["A"], s["F"][None], (np.maximum(g, 0) * mask)[None], (np.maximum(-g, 0) * mask)[None]])


def damage(s, mask):
    s["A"][:, mask] = 0
    return s
