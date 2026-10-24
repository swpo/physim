"""Multi-channel Lenia engine used for screening (worlds copy what they need).

Rule = list of kernels, each a dict:
    c0 (source channel), c1 (target channel), r (radius fraction of R), b (ring peaks),
    m, s (growth centre/width), h (weight), optional kn/gn (core / growth shapes).
Update (Chan 2020, LeniaNDKC.calc_once):
    A_c <- clip(A_c + dt * sum_{k: c1=c} h_k G_k(K_k * A_{c0}) / sum_{k: c1=c} h_k, 0, 1)
"""
import numpy as np
import scipy.fft as sfft
from fractions import Fraction

W = 2


def rfft2(x):
    return sfft.rfft2(x, axes=(-2, -1), workers=W)


def irfft2(X, shape):
    return sfft.irfft2(X, s=shape, axes=(-2, -1), workers=W)


def radial(H, Wd):
    y = np.minimum(np.arange(H), H - np.arange(H))[:, None]
    x = np.minimum(np.arange(Wd), Wd - np.arange(Wd))[None, :]
    return np.sqrt(x ** 2 + y ** 2)


CORES = {
    1: lambda r: (4 * r * (1 - r)) ** 4,
    2: lambda r: np.exp(4 - 1 / np.clip(r * (1 - r), 1e-9, None)),
}
GROWTH = {
    1: lambda n, m, s: np.maximum(0, 1 - (n - m) ** 2 / (9 * s ** 2)) ** 4 * 2 - 1,
    2: lambda n, m, s: np.exp(-(n - m) ** 2 / (2 * s ** 2)) * 2 - 1,
}


def parse_b(b):
    if isinstance(b, str):
        return [float(Fraction(x)) for x in b.split(",")]
    return [float(x) for x in b]


def kernel_fft(H, Wd, R, k):
    D = radial(H, Wd) / R
    r = k.get("r", 1.0)
    bs = np.asarray(parse_b(k.get("b", [1])))
    B = len(bs)
    Br = B * D / r
    b = bs[np.minimum(np.floor(Br).astype(int), B - 1)]
    core = CORES[k.get("kn", 1)](np.minimum(Br % 1, 1))
    K = (D < r) * core * b
    return rfft2(K / K.sum())


def ch2val(c):
    if c in ".b":
        return 0
    if c == "o":
        return 255
    if len(c) == 1:
        return ord(c) - ord("A") + 1
    return (ord(c[0]) - ord("p")) * 24 + (ord(c[1]) - ord("A") + 25)


def rle2arr(st):
    """2D Chan RLE -> array in [0, 1]."""
    rows, row = [], []
    last, count = "", ""
    st = st.rstrip("!") + "$"
    for ch in st:
        if ch.isdigit():
            count += ch
        elif ch in "pqrstuvwxy@":
            last = ch
        else:
            if ch == "$" and last == "":
                rows.append(row)
                for _ in range(int(count or 1) - 1):
                    rows.append([])
                row = []
            else:
                row.extend([ch2val(last + ch) / 255] * int(count or 1))
            last, count = "", ""
    w = max(len(r) for r in rows)
    return np.array([r + [0] * (w - len(r)) for r in rows])


class MCL:
    def __init__(self, rule, C, size, R, T, growth=1):
        self.H, self.W = size
        self.rule, self.C, self.R, self.dt = rule, C, R, 1.0 / T
        self.Kf = np.stack([kernel_fft(self.H, self.W, R, k) for k in rule])
        self.src = np.array([k["c0"] for k in rule])
        self.dst = np.array([k["c1"] for k in rule])
        self.m = np.array([k["m"] for k in rule])[:, None, None]
        self.s = np.array([k["s"] for k in rule])[:, None, None]
        self.h = np.array([k["h"] for k in rule])
        self.g = GROWTH[growth]
        self.hsum = np.array([self.h[self.dst == c].sum() for c in range(C)])

    def potentials(self, A):
        Af = rfft2(A)
        return irfft2(Af[self.src] * self.Kf, (self.H, self.W))

    def step(self, A):
        U = self.potentials(A)
        G = self.g(U, self.m, self.s) * self.h[:, None, None]
        D = np.zeros_like(A)
        np.add.at(D, self.dst, G)
        D = D / np.maximum(self.hsum, 1e-12)[:, None, None]
        return np.clip(A + self.dt * D, 0, 1)


def from_chan(entry):
    rule = []
    for p in entry["params"]:
        c0, c1 = p.get("c", [0, 0])
        rule.append(dict(c0=c0, c1=c1, r=p.get("r", 1), b=p["b"], m=p["m"], s=p["s"], h=p.get("h", 1),
                         kn=p.get("kn", 1)))
    cells = entry["cells"]
    if isinstance(cells, str):
        cells = [cells]
    arrs = [rle2arr(c) for c in cells]
    h = max(a.shape[0] for a in arrs)
    w = max(a.shape[1] for a in arrs)
    out = np.zeros((len(arrs), h, w))
    for i, a in enumerate(arrs):
        out[i, :a.shape[0], :a.shape[1]] = a
    return rule, out
