"""Learned causal predictor for the laboratory task."""
import os
import pickle
import numpy as np

_H = 0.02
_N = 2501
_GRID = np.arange(_N, dtype=np.float64) * _H
_INJ_KERNELS = [
    (0.0, 0.0), (0.0, 0.10), (0.0, 0.22), (0.0, 0.45),
    (0.0, 0.9), (0.0, 1.8), (0.04, 0.0), (0.04, 0.35),
    (0.04, 1.0), (0.14, 0.0), (0.14, 0.6), (0.14, 1.6),
    (0.5, 0.0), (0.5, 1.2),
]
_ADJ_KERNELS = [
    (0.0, 0.0), (0.0, 0.10), (0.0, 0.25), (0.0, 0.55),
    (0.04, 0.0), (0.04, 0.35), (0.14, 0.0), (0.14, 0.8),
    (0.5, 0.0), (0.5, 1.5),
]
_LAG_EDGES = np.array([0, 5, 15, 40, 100, 250, 500, 1000, 2500], dtype=np.int64)
_BUNDLE = None
_BASE = None
_ZBASE = None


def _load():
    global _BUNDLE, _BASE, _ZBASE
    if _BUNDLE is None:
        here = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(here, "model_bundle.pkl"), "rb") as f:
            _BUNDLE = pickle.load(f)
        z = np.load(os.path.join(here, "baseline_full.npz"), allow_pickle=False)
        _BASE = {k: z[k].copy() for k in z.files}
        _ZBASE = _z2_series(np.zeros((2, 4, _N), dtype=np.float32))
    return _BUNDLE, _BASE


def _clean_actions(actions):
    # Zero-valued commands are scheduling events but have no physical effect.
    ans = []
    for a in actions:
        if a["kind"] == "inject":
            if abs(float(a["amp"])) > 1e-14:
                ans.append(a)
        else:
            if np.max(np.abs(np.asarray(a["u"], dtype=np.float64))) > 1e-14:
                ans.append(a)
    return ans


def _arrays(actions):
    """Piecewise current and adjustment-event arrays on the native 0.02 grid."""
    A = np.zeros((2, 4, _N), dtype=np.float32)
    E = np.zeros((2, _N, 13), dtype=np.float32)
    U = np.zeros((2, _N, 3), dtype=np.float32)
    for a in actions:
        if a["kind"] == "inject":
            d = int(a["device"])
            p = int(a["port"])
            i0 = int(round(float(a["t"]) / _H))
            i1 = int(round((float(a["t"]) + float(a["dur"])) / _H))
            i0 = min(max(i0, 0), _N)
            i1 = min(max(i1, 0), _N)
            if i1 > i0:
                A[d, p, i0:i1] += np.float32(a["amp"])
        else:
            d = int(a["device"])
            i = int(round(float(a["t"]) / _H))
            if 0 <= i < _N:
                u = np.asarray(a["u"], dtype=np.float32)
                U[d, i] += u
                E[d, i] += _phi(u)
    return A, E, U


def _phi(u):
    u = np.asarray(u, dtype=np.float32)
    return np.array([
        1.0, u[0], u[1], u[2],
        u[0] * u[0], u[1] * u[1], u[2] * u[2],
        u[0] ** 3, u[1] ** 3, u[2] ** 3,
        u[0] * u[1], u[0] * u[2], u[1] * u[2],
    ], dtype=np.float32)


def _exp_scalar(x, kernels):
    """Causal integrals of a scalar held-current input."""
    aa = np.asarray([complex(lam, -w) for lam, w in kernels])
    r = np.exp(-aa * _H)
    c = np.empty_like(r)
    nz = np.abs(aa) > 1e-14
    c[nz] = (1.0 - r[nz]) / aa[nz]
    c[~nz] = _H
    out = np.empty((_N, len(kernels)), dtype=np.complex64)
    state = np.zeros(len(kernels), dtype=np.complex128)
    for i in range(_N):
        out[i] = state
        state = r * state + c * x[i]
    return out


def _exp_vec(events, kernels):
    """Causal exponential traces of instantaneous vector kicks."""
    aa = np.asarray([complex(lam, -w) for lam, w in kernels])
    r = np.exp(-aa * _H)
    out = np.empty((_N, len(kernels), events.shape[1]), dtype=np.complex64)
    state = np.zeros((len(kernels), events.shape[1]), dtype=np.complex128)
    for i in range(_N):
        state += events[i][None, :]
        out[i] = state
        state = r[:, None] * state
    return out


def _features(A, E, target_device, inds):
    """The causal feature map used for the broad direct models."""
    ii = np.asarray(inds, dtype=np.int64)
    order = (target_device, 1 - target_device)
    fs = []
    tt = _GRID[ii] / 50.0
    fs.extend((tt, tt * tt, tt * tt * tt))
    for k in range(1, 13):
        fs.append(np.sin(2.0 * np.pi * k * tt))
        fs.append(np.cos(2.0 * np.pi * k * tt))
    for d in order:
        for p in range(4):
            x = A[d, p]
            for power in (1, 2, 3):
                fs.append((x[ii] ** power).astype(np.float32))
            for power in (1, 2):
                fil = _exp_scalar(x ** power, _INJ_KERNELS)[ii]
                for kk, (_, w) in enumerate(_INJ_KERNELS):
                    fs.append(fil[:, kk].real)
                    if w != 0.0:
                        fs.append(fil[:, kk].imag)
            for power in (1, 2):
                cum = np.r_[0.0, np.cumsum((x ** power) * _H, dtype=np.float64)]
                for lo, hi in zip(_LAG_EDGES[:-1], _LAG_EDGES[1:]):
                    fs.append((cum[np.maximum(ii - lo, 0)] - cum[np.maximum(ii - hi, 0)]).astype(np.float32))
    for d in order:
        fil = _exp_vec(E[d], _ADJ_KERNELS)[ii]
        for kk, (_, w) in enumerate(_ADJ_KERNELS):
            for q in range(13):
                fs.append(fil[:, kk, q].real)
            if w != 0.0:
                for q in range(13):
                    fs.append(fil[:, kk, q].imag)
        cum = np.r_[np.zeros((1, 13)), np.cumsum(E[d], axis=0, dtype=np.float64)]
        for lo, hi in zip(_LAG_EDGES[:-1], _LAG_EDGES[1:]):
            val = cum[np.maximum(ii - lo, 0)] - cum[np.maximum(ii - hi, 0)]
            for q in range(13):
                fs.append(val[:, q].astype(np.float32))
    return np.stack(fs, axis=1).astype(np.float32)


def _z2_series(A):
    # The port-2 shared accumulator is very accurately identified as linear.
    b, intercept = _load_coeffs()
    z = np.empty(_N, dtype=np.float64)
    z[0] = 0.012903489172458649
    u = A.sum(axis=0)
    for i in range(_N - 1):
        z[i + 1] = b[0] * z[i] + np.dot(b[1:], u[:, i]) + intercept
    return z


def _load_coeffs():
    # Kept separate to permit baseline initialization while loading the bundle.
    if _BUNDLE is None:
        # These are the learned coefficients.  This path is used only while
        # _load is constructing its cached baseline trace.
        return np.array([0.999899842, -1.21230304e-7, 1.05623218e-6,
                         1.99979784e-2, -1.99522613e-7], dtype=np.float64), 1.0923744131474677e-6
    return np.asarray(_BUNDLE["lin2coef"], dtype=np.float64), float(_BUNDLE["lin2int"])


def _c2_aug(A, U, target_device, inds):
    """Physics-motivated interaction features for the difficult channel 2."""
    ii = np.asarray(inds, dtype=np.int64)
    coef, intercept = _load_coeffs()
    order = (target_device, 1 - target_device)

    def source_z(inp, initial, use_intercept):
        z = np.empty(_N, dtype=np.float64)
        z[0] = initial
        for j in range(_N - 1):
            z[j + 1] = coef[0] * z[j] + coef[3] * inp[j] + (intercept if use_intercept else 0.0)
        return z

    ztot = _z2_series(A)
    zsrc = [source_z(A[d, 2], 0.0, False) for d in range(2)]
    fs = [ztot[ii], ztot[ii] ** 2]
    for d in order:
        fs.extend((zsrc[d][ii], zsrc[d][ii] ** 2, A[d, 2, ii], A[d, 2, ii] ** 2))
    ks = [(0.0, 0.0), (0.03, 0.0), (0.1, 0.0), (0.3, 0.0), (1.0, 0.0)]
    for d in order:
        raw = _exp_vec(U[d], ks)[ii].real
        sq = _exp_vec(U[d] ** 2, ks)[ii].real
        for fs0 in (raw, sq):
            for kk in range(len(ks)):
                for q in range(3):
                    v = fs0[:, kk, q]
                    fs.extend((v, ztot[ii] * v, zsrc[d][ii] * v))
        rr = raw[:, 2]
        fs.extend((rr[:, 0] * rr[:, 1], rr[:, 0] * rr[:, 2], rr[:, 1] * rr[:, 2],
                   ztot[ii] * rr[:, 0] * rr[:, 1], ztot[ii] * rr[:, 0] * rr[:, 2],
                   ztot[ii] * rr[:, 1] * rr[:, 2]))
    return np.stack(fs, axis=1).astype(np.float32)


def _predict_model(model, sx, sy, x):
    return sy.inverse_transform(model.predict(sx.transform(x)))


def _full_device(bundle, x, target):
    if target == 0:
        mods, sx, sy, slots = bundle["d0_models"], bundle["d0_sx"], bundle["d0_sy"], 13
        weights = np.asarray(bundle["W0c"], dtype=np.float64)
    else:
        mods, sx, sy, slots = bundle["d1_models"], bundle["d1_sx"], bundle["d1_sy"], 19
        weights = None
    ps = [_predict_model(m, sx, sy, x) for m in mods]
    if target == 1:
        return sum(ps) / float(len(ps))
    out = np.empty_like(ps[0])
    for c in range(4):
        sl = slice(c * slots, (c + 1) * slots)
        out[:, sl] = sum(weights[c, k] * ps[k][:, sl] for k in range(3))
    return out


def _analytic_injection_c2(bundle, base, A, inds, target):
    z = _z2_series(A)[inds]
    dz = z - _ZBASE[inds]
    if target == 0:
        return base["d0"][inds, 2, :] + dz[:, None] * np.asarray(bundle["K0"])[None, :]
    return base["d1"][inds, 2, :] + dz[:, None] * np.asarray(bundle["K1"])[None, :]


def _global_analytic_c2(A, inds):
    z = _z2_series(A)[inds]
    return np.stack((0.000900 + 0.001534 * z,
                     0.0000055 + 0.0000048 * z + 0.00076464 * z * z), axis=1)


def _device_prediction(bundle, base, A, E, U, inds, target, mode):
    x = _features(A, E, target, inds)
    slots = 13 if target == 0 else 19
    full = _full_device(bundle, x, target)
    if mode == "inject":
        if target == 0:
            special = _predict_model(bundle["inj0_model"], bundle["inj0_sx"], bundle["inj0_sy"], x[:, bundle["injcols"]])
            out = 0.75 * special + 0.25 * full
        else:
            special = _predict_model(bundle["inj1_model"], bundle["inj1_sx"], bundle["inj1_sy"], x[:, bundle["injcols"]])
            out = 0.50 * special + 0.50 * full
        out[:, 2 * slots:3 * slots] = _analytic_injection_c2(bundle, base, A, inds, target)
        return out
    if mode == "adjust":
        if target == 0:
            special = _predict_model(bundle["adj0_model"], bundle["adj0_sx"], bundle["adj0_sy"], x[:, bundle["adjcols"]])
            return 0.75 * special + 0.25 * full
        special = _predict_model(bundle["adj1_model"], bundle["adj1_sx"], bundle["adj1_sy"], x[:, bundle["adjcols"]])
        return 0.90 * special + 0.10 * full
    # Mixed inputs: use an interaction-specific channel-2 model.
    aug = _c2_aug(A, U, target, inds)
    compact = np.concatenate((x[:, bundle["p2cols"]], aug), axis=1)
    if target == 0:
        c2 = _predict_model(bundle["c20_model"], bundle["c20_sx"], bundle["c20_sy"], compact)
    else:
        c2 = _predict_model(bundle["c21_model"], bundle["c21_sx"], bundle["c21_sy"], compact)
    out = full.copy()
    sl = slice(2 * slots, 3 * slots)
    out[:, sl] = 0.75 * c2 + 0.25 * out[:, sl]
    return out


def predict(actions, queries, n_samples=64, seed=0):
    """Predict sensor arrays in the laboratory interface format."""
    bundle, base = _load()
    ns = int(n_samples)
    cleaned = _clean_actions(actions)
    allinds = []
    for q in queries:
        for t in q["t"]:
            allinds.append(int(round(float(t) / _H)))
    if allinds:
        inds = np.unique(np.clip(np.asarray(allinds, dtype=np.int64), 0, _N - 1))
    else:
        inds = np.empty(0, dtype=np.int64)
    if inds.size:
        A, E, U = _arrays(cleaned)
        # Select the expert from actions that have already begun at each time.
        # This keeps every earlier prediction invariant if a later action is
        # appended to the supplied program.
        inj_starts = np.asarray([float(a["t"]) for a in cleaned if a["kind"] == "inject"], dtype=np.float64)
        adj_starts = np.asarray([float(a["t"]) for a in cleaned if a["kind"] == "adjust"], dtype=np.float64)
        mode_at = []
        for ind in inds:
            now = float(ind) * _H
            hi = bool(inj_starts.size and np.any(inj_starts <= now + 1e-10))
            ha = bool(adj_starts.size and np.any(adj_starts <= now + 1e-10))
            mode_at.append("mixed" if hi and ha else ("inject" if hi else ("adjust" if ha else "baseline")))
        p0 = np.empty((len(inds), 52), dtype=np.float64)
        p1 = np.empty((len(inds), 76), dtype=np.float64)
        pg = np.empty((len(inds), 8), dtype=np.float64)
        for mode in ("baseline", "inject", "adjust", "mixed"):
            take = np.asarray([m == mode for m in mode_at])
            if not np.any(take):
                continue
            subinds = inds[take]
            if mode == "baseline":
                p0[take] = base["d0"][subinds].reshape(len(subinds), -1)
                p1[take] = base["d1"][subinds].reshape(len(subinds), -1)
                pg[take] = base["g"][subinds].reshape(len(subinds), -1)
                continue
            p0[take] = _device_prediction(bundle, base, A, E, U, subinds, 0, mode)
            p1[take] = _device_prediction(bundle, base, A, E, U, subinds, 1, mode)
            if mode == "adjust":
                pg[take] = base["g"][subinds].reshape(len(subinds), -1)
            else:
                xg = _features(A, E, 0, subinds)
                gsub = _predict_model(bundle["g_model"], bundle["g_sx"], bundle["g_sy"], xg)
                gsub = gsub.reshape(len(subinds), 4, 2)
                gsub[:, 2, :] = _global_analytic_c2(A, subinds)
                pg[take] = gsub.reshape(len(subinds), -1)
        p0 = p0.reshape(len(inds), 4, 13)
        p1 = p1.reshape(len(inds), 4, 19)
        pg = pg.reshape(len(inds), 4, 2)
    else:
        p0 = np.empty((0, 4, 13), dtype=np.float64)
        p1 = np.empty((0, 4, 19), dtype=np.float64)
        pg = np.empty((0, 4, 2), dtype=np.float64)
    lookup = {int(v): i for i, v in enumerate(inds)}
    result = []
    for q in queries:
        sensor = q["sensor"]
        source = p0 if sensor == "device0" else (p1 if sensor == "device1" else pg)
        qinds = [lookup[int(round(float(t) / _H))] for t in q["t"]]
        arr = source[qinds] if qinds else source[:0]
        # A deterministic mean predictor is deliberate: observed stochasticity
        # is much smaller than the learned dynamical uncertainty.
        result.append(np.repeat(arr[None, ...], ns, axis=0).astype(np.float64, copy=False))
    return {"samples": result}
