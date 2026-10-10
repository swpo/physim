"""Baseline-from-data + simulated injection response (reaction-diffusion model in a local box around the devices),
blended with a calibrated rule; predictive spread from calibrated error tables."""
import os
import numpy as np
import scipy.fft as sfft
from scipy.spatial import cKDTree

SLOTS = {"device0": 13, "device1": 19, "global": 2}
SID = {"device0": 0, "device1": 1, "global": 2}
_HERE = os.path.dirname(os.path.abspath(__file__))
ZMIN, ZMAX = np.log(0.5), np.log(3.0)
DT = 0.02
NSTEP = 2500
H = 0.5
DOMAIN_AREA = 128.0 * 128.0     # periodic world domain (physical units)
GN = 128                        # simulation box: GN x GN cells of size H, rest state outside the fitted windows
GX0, GY0 = -32.0, -30.0
MARGIN = 3.0
D0 = np.array([[0, 3], [3, 0], [-6, 0], [-3, 3], [-3, 0], [-3, -3], [0, 0], [3, 3], [0, 6], [6, 0], [0, -3], [0, -6], [3, -3]], float)
_a = 6 * np.sqrt(3) / 2
D1 = np.array([[0, -12], [-2 * _a, 6], [-_a, 9], [_a, 9], [0, -6], [0, 12], [-_a, -3], [-2 * _a, 0], [-2 * _a, -6], [0, 6],
               [0, 0], [2 * _a, -6], [-_a, 3], [2 * _a, 6], [_a, -9], [_a, -3], [2 * _a, 0], [_a, 3], [-_a, -9]], float)
OFF = {"device0": D0, "device1": D1}
REST = np.array([0.0, -0.70, 0.0, 0.0])
ALPHA = 0.25
PNAMES = ['av', 'bv', 'p0', 'p1', 'p2', 'p3', 'k3', 'k4', 'gam', 'g0', 'gs',
          'kc', 'alpha', 'pu0', 'ps', 'aw', 'bw', 'Dv', 'Du', 'Dw', 'c0', 'cm',
          'A', 'Bw', 'Bv', 'ur', 'c2', 'cm2', 'Ev', 'Fv', 'Ew', 'Fw']
PDEF_TAIL = {'c0': 1e6, 'cm': 1.0, 'A': 0.0, 'Bw': 0.0, 'Bv': 0.0, 'ur': -0.705, 'c2': 1e6, 'cm2': 1.0,
             'Ev': 0.0, 'Fv': 0.0, 'Ew': 0.0, 'Fw': 0.0}
DIFF_CH = [0, 1, 3]
WORKERS = 4
THREADS = int(os.environ.get("PRED_THREADS", "4"))   # batch chunks stepped in parallel threads
F32 = os.environ.get("PRED_F32", "1") == "1"   # single-precision injection simulations
_cache = {}
NOISE = os.environ.get("PRED_NOISE", "1") == "1"

# noise mixes a per-sample common factor, a time-correlated per-slot field (AR(1) on 0.5 tu knots) and white noise
MIX = (0.5, 0.0, 0.87)          # weights: common, smooth, white
NOISE_A = float(os.environ.get("PRED_NOISE_A", "-1"))   # if >= 0: common weight, white weight sqrt(1 - NOISE_A^2)
RHO = 0.85                      # knot-to-knot correlation of the smooth field
SD_INFL = 1.0
ENS_SD = float(os.environ.get("PRED_ENS_SD", "0.3"))    # scale of table spread around each member
BASE_SD = float(os.environ.get("PRED_BASE_SD", "0.7"))  # scale of the baseline spread table
MODELS = ["model_as4es.npz"]
# parameter ensemble around the first model: antithetic pairs p*(1 +/- ENS_PERT*xi), p0 keeps the rest state
ENS_M = int(os.environ.get("PRED_ENS_M", "16"))
ENS_PERT = float(os.environ.get("PRED_ENS_PERT", "0.003"))
ENS_BASE = os.environ.get("PRED_ENS_BASE", "0") == "1"   # keep the unperturbed model as member 0 ...
ENS_W0 = float(os.environ.get("PRED_ENS_W0", "0.5"))     # ... with this fraction of the samples
ENS_SEED = int(os.environ.get("PRED_ENS_SEED", "1"))
ENS_XI = os.environ.get("PRED_ENS_XI", "")   # optional file (pred_data) of fixed perturbation directions (M, len(PERT_NAMES))
PERT_NAMES = ['av', 'p1', 'p3', 'k3', 'k4', 'aw', 'Du', 'Dv', 'Dw', 'A', 'Bv']
RESB = os.environ.get("PRED_RESB", "1") == "1"   # baseline = model free run + interpolated data residuals
# static excitability sources added to the u reaction term: (x, y, sigma, amplitude)
HOT = [tuple(float(a) for a in h.split(",")) for h in os.environ.get("PRED_HOT", "-7,5,2,0.004").split(";") if h]


# ----------------------------------------------------------------------------------------------- data
def _base():
    """KD table of baseline observations; values are stored as residuals from the model's free run."""
    if "b" not in _cache:
        z = np.load(os.environ.get("PRED_INTERIM", os.path.join(_HERE, "pred_data", "interim.npz")))
        X = z["X"].astype(float).copy()
        V = z["V"].astype(float)
        if RESB:
            V = V - _free_at(X[:, 0], X[:, 1], X[:, 2])
        X[:, 2] *= ALPHA
        _cache["b"] = (cKDTree(X), V, z["gmean"], z["gstd"])
    return _cache["b"]


def _free():
    """Free run (no injections) of the first ensemble member, restarted at every window state; frames every 0.5 tu."""
    if "f" not in _cache:
        _models()
        Mo = _cache["m0"]
        box = Box(GX0, GY0, GN, [Mo['p']])
        wt = Mo['wt']
        F = np.zeros((NSTEP // 25 + 1, 4, GN, GN))
        for k in range(len(wt)):
            X = Mo['W'][k][None].copy()
            n0 = _step_of(wt[k])
            n1 = _step_of(wt[k + 1]) if k + 1 < len(wt) else NSTEP
            for n in range(n0, n1 + 1):
                if n > n0:
                    X = box.step(X)
                if n % 25 == 0:
                    F[n // 25] = X[0]
        _cache["f"] = (box, F)
    return _cache["f"]


def _free_at(px, py, t):
    """Free-run values (n,4) at points/times (bilinear in space, linear in time); rest state outside the box."""
    box, F = _free()
    x = np.clip(np.asarray(t, float) * 2.0, 0, len(F) - 1)
    i0 = np.minimum(np.floor(x).astype(int), len(F) - 2)
    fr = x - i0
    out = np.empty((len(px), 4))
    for i in np.unique(i0):
        m = i0 == i
        a = box.interp(F[i], px[m], py[m]); b = box.interp(F[i + 1], px[m], py[m])
        out[m] = ((1 - fr[m]) * a + fr[m] * b).T
    out[~box.inside(px, py, MARGIN)] = REST
    return out


def _load_model(path):
    z = np.load(path)
    box = z["box"]
    p = list(z["p"].astype(float))
    for n in PNAMES[len(p):]:
        p.append(PDEF_TAIL[n])
    Wb = z["W"].astype(float)
    bn = int(box[2])
    i0 = int(round((float(box[0]) - GX0) / H)); j0 = int(round((float(box[1]) - GY0) / H))
    W = np.empty((len(Wb), 4, GN, GN))
    for k in range(len(Wb)):
        e = np.concatenate([Wb[k][:, 0, :], Wb[k][:, -1, :], Wb[k][:, :, 0], Wb[k][:, :, -1]], 1)
        W[k] = np.median(e, 1)[:, None, None]
        W[k][:, i0:i0 + bn, j0:j0 + bn] = Wb[k]
    return dict(p=np.array(p), W=W, wt=z["wt"].astype(float))


def _rest_terms(P, u):
    return (P['p1'] * u + P['p2'] * u ** 2 + P['p3'] * u ** 3 - P['k3'] * (u + P['bv'] / P['av'])
            - P['k4'] * (u + P['bw'] / P['aw']))


def _with_rest(P0, P, ur):
    """Adjust bv, bw, p0 of P so that the rest state (u, v, w) of P0 is kept."""
    P = dict(P)
    P['bv'] = P0['bv'] * P['av'] / P0['av']
    P['bw'] = P0['bw'] * P['aw'] / P0['aw']
    P['p0'] = -_rest_terms(P, ur)
    return P


def _perturbed(base):
    """ENS_M members sharing the base window states; parameters perturbed in antithetic pairs."""
    from scipy.optimize import brentq
    P0 = dict(zip(PNAMES, base['p']))
    ur = brentq(lambda u: P0['p0'] + _rest_terms(P0, u), -2.0, -0.3)
    out = []
    for xi in _xi():
        P = dict(P0)
        for n, x in zip(PERT_NAMES, xi):
            P[n] = P0[n] * (1 + ENS_PERT * x)
        P = _with_rest(P0, P, ur)
        out.append(dict(p=np.array([P[n] for n in PNAMES]), W=base['W'], wt=base['wt']))
    return out


def _xi():
    """Perturbation directions: fixed (ENS_XI file) or ENS_M // 2 random antithetic pairs."""
    if ENS_XI:
        return np.load(ENS_XI if os.path.isabs(ENS_XI) else os.path.join(_HERE, "pred_data", ENS_XI))
    rng = np.random.default_rng(ENS_SEED)
    out = []
    for _ in range(ENS_M // 2):
        xi = rng.standard_normal(len(PERT_NAMES))
        out += [xi, -xi]
    return np.array(out).reshape(-1, len(PERT_NAMES))


def _models():
    """Ensemble members (list of dicts with p, W, wt)."""
    if "m" not in _cache:
        names = os.environ.get("PRED_MODELS", ",".join(MODELS)).split(",")
        ms = [_load_model(n if os.path.isabs(n) else os.path.join(_HERE, "pred_data", n)) for n in names]
        _cache["m0"] = ms[0]
        _cache["m"] = (([ms[0]] if ENS_BASE else []) + _perturbed(ms[0])) if _perturbing() else ms
    return _cache["m"]


def _perturbing():
    return (ENS_M > 1 or bool(ENS_XI)) and ENS_PERT > 0


def _member_of(n, M):
    """Ensemble member of every sample; with a base member, the first round(ENS_W0*n) samples use member 0."""
    if M == 1:
        return np.zeros(n, int)
    if not (ENS_BASE and _perturbing()):
        return np.arange(n) % M
    n0 = int(round(ENS_W0 * n))
    i = np.arange(n)
    return np.where(i < n0, 0, 1 + (i - n0) % (M - 1))


def _calib():
    if "c" not in _cache:
        z = np.load(os.environ.get("PRED_CALIB", os.path.join(_HERE, "pred_data", "calib.npz")))
        _cache["c"] = {k: z[k].astype(float) for k in z.files}
    return _cache["c"]


def _bin(edges, x):
    return np.clip(np.searchsorted(edges, x, side='right') - 1, 0, len(edges) - 2)


def _baseline(P, T):
    """P (n,2) positions, T (n,) times -> (n,4) baseline values from data, distance to nearest datum."""
    tree, V, _, _ = _base()
    pts = np.concatenate([P, T[:, None] * ALPHA], 1)
    d, idx = tree.query(pts, k=8)
    w = 1.0 / (d + 0.05) ** 2
    mu = (w[:, :, None] * V[idx]).sum(1) / w.sum(1)[:, None]
    far = np.clip((d[:, 0] - 1.5) / 3.0, 0, 1)[:, None]
    if RESB:
        return _free_at(P[:, 0], P[:, 1], T) + (1 - far) * mu, d[:, 0]
    return (1 - far) * mu + far * REST[None], d[:, 0]


# ----------------------------------------------------------------------------------------------- program
def _step_of(t):
    return int(round(float(t) / DT))


def _tracks(actions):
    st = {0: [(-np.inf, 0.0, 0.0, 0.0)], 1: [(-np.inf, 0.0, 0.0, 0.0)]}
    for a in actions:
        if a["kind"] != "adjust":
            continue
        d = int(a["device"])
        t, cx, cy, z = st[d][-1]
        u = a["u"]
        st[d].append((float(a["t"]), cx + float(u[0]), cy + float(u[1]), float(np.clip(z + float(u[2]), ZMIN, ZMAX))))
    return st


def _positions(tracks, sensor, times):
    st = tracks[0 if sensor == "device0" else 1]
    out = np.zeros((len(times), len(OFF[sensor]), 2))
    for i, t in enumerate(times):
        cur = st[0]
        for s in st:
            if s[0] <= t + 1e-9:
                cur = s
        out[i] = np.array([cur[1], cur[2]]) + np.exp(cur[3]) * OFF[sensor]
    return out


def _injections(actions):
    pos = {0: [0.0, 0.0], 1: [0.0, 0.0]}
    out = []
    for a in actions:
        d = int(a["device"])
        if a["kind"] == "adjust":
            pos[d][0] += float(a["u"][0]); pos[d][1] += float(a["u"][1])
        elif a["kind"] == "inject":
            n0 = _step_of(a["t"]); ns = _step_of(a["dur"])
            if float(a["amp"]) != 0.0:
                out.append(dict(n0=n0, n1=n0 + ns, port=int(a["port"]), amp=float(a["amp"]), x=pos[d][0], y=pos[d][1]))
    return out


# ----------------------------------------------------------------------------------------------- model
def _sig(x):
    return 0.5 * (1.0 + np.tanh(0.5 * x))


def _react(X, P):
    v, u, c, w = X[..., 0, :, :], X[..., 1, :, :], X[..., 2, :, :], X[..., 3, :, :]
    h2 = c * np.maximum(1.0 + c / P['c2'], 1e-6) ** (-P['cm2'])
    du = u - P['ur']
    R = np.empty_like(X)
    Rv = P['av'] * (u - v) + P['bv']
    Ru = P['p0'] + u * (P['p1'] + u * (P['p2'] + u * P['p3'])) - P['k3'] * v - P['k4'] * w
    Rw = P['aw'] * (u - w) + P['bw']
    if np.any(P['gam'] != 0):           # terms with all-zero coefficients are skipped (exactly zero)
        g = P['gs'] * np.logaddexp(0.0, (u - P['g0']) / P['gs'])
        hc = c * np.maximum(1.0 + c / P['c0'], 1e-6) ** (-P['cm'])
        Ru = Ru - P['gam'] * hc * g
    R[..., 1, :, :] = Ru - h2 * (P['A'] * du - P['Bw'] * w - P['Bv'] * v)
    if np.any(P['Ev'] != 0) or np.any(P['Fv'] != 0):
        Rv = Rv + h2 * (P['Ev'] * du - P['Fv'] * v)
    if np.any(P['Ew'] != 0) or np.any(P['Fw'] != 0):
        Rw = Rw + h2 * (P['Ew'] * du - P['Fw'] * w)
    R[..., 0, :, :] = Rv
    R[..., 2, :, :] = -P['kc'] * c + P['alpha'] * _sig((u - P['pu0']) / P['ps'])
    R[..., 3, :, :] = Rw
    return R


def _tpool():
    if "pool" not in _cache:
        from concurrent.futures import ThreadPoolExecutor
        _cache["pool"] = ThreadPoolExecutor(THREADS)
    return _cache["pool"]


class Box:
    """Periodic simulation box; a batch of states (B,4,N,N) with per-batch-element parameters."""

    def __init__(self, x0, y0, N, plist, f32=False):
        self.x0, self.y0, self.N = x0, y0, N
        self.xs = x0 + np.arange(N) * H
        self.ys = y0 + np.arange(N) * H
        self.L = N * H
        k = 2 * np.pi * np.fft.fftfreq(N, d=H)
        kr = 2 * np.pi * np.fft.rfftfreq(N, d=H)
        self.K2 = k[:, None] ** 2 + kr[None, :] ** 2
        pa = np.array(plist, float)                          # (B, npar)
        self.P = {n: pa[:, i][:, None, None] for i, n in enumerate(PNAMES)}
        self.E = np.stack([np.exp(-pa[:, PNAMES.index(n)][:, None, None] * self.K2[None] * DT)
                           for n in ['Dv', 'Du', 'Dw']], 1)  # (B,3,N,N//2+1)
        self.S = sum(a * self.gauss(hx, hy, hs) for hx, hy, hs, a in HOT) if HOT else None
        if f32:                                              # single-precision stepping (states must be float32 too)
            self.P = {k: v.astype(np.float32) for k, v in self.P.items()}
            self.E = self.E.astype(np.float32)
            self.S = None if self.S is None else self.S.astype(np.float32)
        nb = len(pa)
        self.sl = [slice(a[0], a[-1] + 1) for a in np.array_split(np.arange(nb), min(THREADS, nb)) if len(a)]
        self.Pc = [{k: v[sl] for k, v in self.P.items()} for sl in self.sl]
        self.Ec = [self.E[sl] for sl in self.sl]

    def gauss(self, cx, cy, sig=2.0):
        L = self.L
        dx = (self.xs - cx + L / 2) % L - L / 2
        dy = (self.ys - cy + L / 2) % L - L / 2
        return np.exp(-dx[:, None] ** 2 / (2 * sig ** 2)) * np.exp(-dy[None, :] ** 2 / (2 * sig ** 2))

    def step(self, X):
        if len(self.sl) == 1:
            return self._step(X, self.P, self.E, WORKERS)
        out = np.empty_like(X)

        def job(j):
            out[self.sl[j]] = self._step(X[self.sl[j]], self.Pc[j], self.Ec[j], 1)
        list(_tpool().map(job, range(len(self.sl))))
        return out

    def _step(self, X, P, E, workers):
        R = _react(X, P)
        if self.S is not None:
            R[:, 1] += self.S
        Z = X + DT * R
        Zh = sfft.rfft2(Z[:, DIFF_CH], workers=workers)
        Z[:, DIFF_CH] = sfft.irfft2(Zh * E, s=(self.N, self.N), workers=workers)
        return Z

    def smooth(self, A, sig):
        return sfft.irfft2(sfft.rfft2(A, workers=WORKERS) * np.exp(-0.5 * sig * sig * self.K2), s=(self.N, self.N),
                           workers=WORKERS)

    def inside(self, px, py, margin):
        return ((px >= self.x0 + margin) & (px < self.x0 + self.L - H - margin) &
                (py >= self.y0 + margin) & (py < self.y0 + self.L - H - margin))

    def interp(self, X, px, py):
        """X (...,N,N) -> (...,n) bilinear at positions (periodic)."""
        N = self.N
        gx = (px - self.x0) / H; gy = (py - self.y0) / H
        ix = np.floor(gx).astype(int); iy = np.floor(gy).astype(int)
        fx = gx - ix; fy = gy - iy
        ix0 = ix % N; iy0 = iy % N; ix1 = (ix + 1) % N; iy1 = (iy + 1) % N
        return (X[..., ix0, iy0] * (1 - fx) * (1 - fy) + X[..., ix1, iy0] * fx * (1 - fy)
                + X[..., ix0, iy1] * (1 - fx) * fy + X[..., ix1, iy1] * fx * fy)


def _simulate(injs, need):
    """need: dict step -> list of (key, px, py). Every ensemble member is run with and without injections.
    Returns dict (key, step) -> (mask, pa (M,4,n), pb (M,4,n), s5 (M,n)) and dict step -> (d1 (M,4), d2 (M,4))."""
    Ms = _models()
    M = len(Ms)
    nf = min(i['n0'] for i in injs)
    wt = Ms[0]['wt']
    k = int(np.searchsorted(wt, nf * DT + 1e-9) - 1)
    k = max(0, min(k, len(wt) - 1))
    pre = Box(GX0, GY0, GN, [m['p'] for m in Ms], F32)
    X = np.stack([m['W'][k] for m in Ms]).astype(np.float32 if F32 else float)
    for n in range(int(round(wt[k] / DT)) + 1, nf + 1):
        X = pre.step(X)
    box = Box(GX0, GY0, GN, [m['p'] for m in Ms for _ in range(2)], F32)
    G = [box.gauss(i['x'], i['y']) for i in injs]
    nend = max(need) if need else nf
    XX = np.repeat(X, 2, axis=0)                 # (2M,4,N,N): even = with injections, odd = without
    out = {}
    gl = {}
    cell = H * H / DOMAIN_AREA
    for n in range(nf + 1, nend + 1):
        for i, g in zip(injs, G):
            if i['n0'] < n <= i['n1']:
                XX[0::2, i['port']] += DT * i['amp'] * g
        XX = box.step(XX)
        if n in need:
            s5f = None
            for key, px, py in need[n]:
                if key == 'global':
                    Xa, Xb = XX[0::2].astype(float), XX[1::2].astype(float)
                    d1 = (Xa - Xb).sum(axis=(2, 3)) * cell
                    d2 = (Xa ** 2 - Xb ** 2).sum(axis=(2, 3)) * cell
                    gl[n] = (d1, d2)
                    continue
                if s5f is None:
                    s5f = box.smooth(np.abs(XX[0::2, 1] - XX[1::2, 1]), 5.0)
                m = box.inside(px, py, MARGIN)
                if not m.any():
                    continue
                v = box.interp(XX, px[m], py[m])     # (2M,4,n)
                out[(key, n)] = (m, v[0::2], v[1::2], np.maximum(box.interp(s5f, px[m], py[m]), 0.0))
    return out, gl


# ----------------------------------------------------------------------------------------------- mean + spread
def _mean(actions, queries):
    """Per query: (steps, mu (M,T,4,S), sd (M,T,4,S)) for M ensemble members."""
    C = _calib()
    M = len(_models())
    tracks = _tracks(actions)
    injs = _injections(actions)
    nf = min([i['n0'] for i in injs] + [10 ** 9])
    need = {}
    qinfo = []
    for qi, q in enumerate(queries):
        T = np.array(q["t"], float)
        steps = np.array([_step_of(t) for t in T], int)
        P = None if (q["sensor"] == "global" or len(T) == 0) else _positions(tracks, q["sensor"], T)
        qinfo.append((T, steps, P))
        for k, n in enumerate(steps):
            if n > nf:
                if q["sensor"] == "global":
                    need.setdefault(n, []).append(('global', None, None))
                else:
                    need.setdefault(n, []).append(((qi, k), P[k, :, 0], P[k, :, 1]))
    sim, gl = (_simulate(injs, need) if need else ({}, {}))
    F0 = C['F0'][None, :, None]; PW = C['PW'][None, :, None]
    res = []
    for qi, q in enumerate(queries):
        T, steps, P = qinfo[qi]
        S = SLOTS[q["sensor"]]
        if len(T) == 0:
            res.append((steps, np.zeros((M, 0, 4, S)), np.zeros((M, 0, 4, S))))
            continue
        if q["sensor"] == "global":
            _, _, gm, gs = _base()
            mu = np.broadcast_to(gm[None, None], (M, len(T), 4, 2)).copy()
            sd = np.broadcast_to(gs[None, None], (M, len(T), 4, 2)).copy() + 1e-6
            for k, n in enumerate(steps):
                if n in gl:
                    d1, d2 = gl[n]
                    m0 = gm[None, :, 0]; ex2 = gm[None, :, 1] + m0 ** 2
                    m1 = m0 + d1; ex2n = ex2 + d2
                    mu[:, k, :, 0] = m1
                    mu[:, k, :, 1] = np.maximum(ex2n - m1 ** 2, 0.0)
                    sd[:, k] = (C['gl_b'][None] * np.abs(mu[:, k] - gm[None]) + gs[None]) * ENS_SD + 1e-6
            res.append((steps, mu, sd * SD_INFL))
            continue
        B, d0 = _baseline(P.reshape(-1, 2), np.repeat(T, S))
        mu = np.repeat(B.reshape(len(T), S, 4).transpose(0, 2, 1)[None], M, 0)
        bi = _bin(C['D0E'], d0)
        if 'base_sd2' in C:                 # separate baseline spread tables near / far from the origin
            Pf = P.reshape(-1, 2)
            ri = (np.hypot(Pf[:, 0], Pf[:, 1]) >= float(C['RSPLIT'])).astype(int)
            bs = C['base_sd2'][ri, :, bi].T
        else:
            bs = C['base_sd'][:, bi]
        bs = bs * BASE_SD
        sd = np.repeat(bs.reshape(4, len(T), S).transpose(1, 0, 2)[None], M, 0)
        for k, n in enumerate(steps):
            r = sim.get(((qi, k), n))
            if r is None:
                continue
            m, pa, pb, s5 = r
            g = 1.0 / (1.0 + (s5[:, None] / F0) ** PW)          # (M,4,n)
            mu[:, k][:, :, m] = pa + g * (mu[:, k][:, :, m] - pb)
            rs = C['res_sd'][:, _bin(C['S5E'], s5), _bin(C['TAE'], np.array([(n - nf) * DT]))[0]]   # (4,M,n)
            rs = rs.transpose(1, 0, 2) * ENS_SD
            sd[:, k][:, :, m] = np.sqrt(sd[:, k][:, :, m] ** 2 + rs ** 2)
        res.append((steps, mu, np.maximum(sd, 1e-6) * SD_INFL))
    return res


def _noise(seed, sensor, steps, n_samples, S):
    """Standard-normal-scale noise (n_samples, T, 4, S); a deterministic function of (seed, sensor, step, sample)."""
    sid = SID[sensor]
    s0 = int(seed) % (2 ** 32)
    a, b, c = MIX if NOISE_A < 0 else (NOISE_A, 0.0, float(np.sqrt(max(1.0 - NOISE_A ** 2, 0.0))))
    cm = np.random.default_rng([s0, 1000]).standard_normal((n_samples, 4))
    z = a * np.broadcast_to(cm[:, None, :, None], (n_samples, len(steps), 4, S))
    if b > 0:
        NK = NSTEP // 25 + 1
        e = np.random.default_rng([s0, 2000 + sid]).standard_normal((n_samples, NK, 4, S))
        f = np.empty_like(e)
        f[:, 0] = e[:, 0]
        r = np.sqrt(1 - RHO ** 2)
        for k in range(1, NK):
            f[:, k] = RHO * f[:, k - 1] + r * e[:, k]
        x = np.clip(steps / 25.0, 0, NK - 1)
        i0 = np.minimum(np.floor(x).astype(int), NK - 2)
        fr = (x - i0)[None, :, None, None]
        z = z + b * ((1 - fr) * f[:, i0] + fr * f[:, i0 + 1])
    if c > 0:
        w = np.empty((n_samples, len(steps), 4, S))
        for k, n in enumerate(steps):
            w[:, k] = np.random.default_rng([s0, 3000 + sid, int(n)]).standard_normal((n_samples, 4, S))
        z = z + c * w
    return z


# ----------------------------------------------------------------------------------------------- predict
def predict(actions, queries, n_samples=64, seed=0):
    res = _mean(actions, queries)
    member = _member_of(n_samples, len(_models()))
    out = []
    for q, (steps, mu, sd) in zip(queries, res):
        S = SLOTS[q["sensor"]]
        if len(steps) == 0:
            out.append(np.zeros((n_samples, 0, 4, S)))
            continue
        if not NOISE:
            out.append(mu[member])
            continue
        z = _noise(seed, q["sensor"], steps, n_samples, S)
        out.append(mu[member] + z * sd[member])
    return {"samples": out}
