
import numpy as np
from pathlib import Path

_DIR = Path(__file__).resolve().parent
_P = np.load(_DIR / "model_params.npz")
THETA = np.asarray(_P["Theta"], dtype=np.float64)
IC = np.asarray(_P["IC"], dtype=np.float64)
D0_U = np.asarray(_P["d0_U"], dtype=np.float64)
D0_T = np.asarray(_P["d0_T"], dtype=np.float64)
D1_U = np.asarray(_P["d1_U"], dtype=np.float64)
D1_T = np.asarray(_P["d1_T"], dtype=np.float64)
WCH2 = np.asarray(_P["wch2"], dtype=np.float64)
CH2_IDX = np.array(
    list(range(26, 39)) + list(range(90, 109)) + list(range(132, 134)),
    dtype=int,
)
SLOTS = {"device0": 13, "device1": 19, "global": 2}
DT = 0.02
EPS = 0.005
DECAY = np.exp(-EPS * DT)
GAIN = (1.0 - DECAY) / EPS
V0_CH2 = IC[CH2_IDX].copy()


def _round_t(t):
    # snap to 0.02 grid
    return round(round(float(t) / DT) * DT, 10)


def _inject_table(actions, nstep):
    I = np.zeros((nstep + 1, 4), dtype=np.float64)
    for a in actions:
        if a.get("kind") != "inject":
            continue
        t0 = float(a["t"])
        dur = float(a["dur"])
        amp = float(a["amp"])
        port = int(a["port"])
        i0 = int(round(t0 / DT))
        i1 = int(round((t0 + dur) / DT))
        i0 = max(0, i0)
        i1 = min(nstep + 1, i1)
        if i1 > i0:
            I[i0:i1, port] += amp
    return I


def _U_of(actions, device, t):
    U = np.zeros(3, dtype=np.float64)
    for a in actions:
        if a.get("kind") != "adjust":
            continue
        if int(a["device"]) != device:
            continue
        if float(a["t"]) <= t + 1e-12:
            U = U + np.asarray(a["u"], dtype=np.float64)
    return U


def _rhs_batch(X, Irow):
    n = X.shape[0]
    feat = np.empty((n, 277), dtype=np.float64)
    feat[:, :136] = X
    np.tanh(X / 3.0, out=feat[:, 136:272])
    feat[:, 272:276] = Irow
    feat[:, 276] = 1.0
    return feat @ THETA


def _interp_T(U, Ugrid, Tgrid):
    d2 = np.sum((Ugrid - U) ** 2, axis=1)
    j = int(np.argmin(d2))
    if d2[j] < 1e-16:
        return Tgrid[j]
    w = 1.0 / (d2 + 1e-4)
    w /= w.sum()
    return np.tensordot(w, Tgrid, axes=(0, 0))


def _apply_device(d_ns, U, which):
    if np.max(np.abs(U)) < 1e-15:
        return d_ns
    T = _interp_T(U, D0_U, D0_T) if which == 0 else _interp_T(U, D1_U, D1_T)
    return np.einsum("ij,...j->...i", T, d_ns)


def _unpack_batch(X):
    n = X.shape[0]
    d0 = X[:, :52].reshape(n, 4, 13)
    d1 = X[:, 52:128].reshape(n, 4, 19)
    g = X[:, 128:136].reshape(n, 4, 2)
    return d0, d1, g


def _simulate(actions, t_need, n_samples, seed):
    t_need = np.array(sorted(set(_round_t(t) for t in t_need)), dtype=np.float64)
    n = int(n_samples)
    X = np.broadcast_to(IC, (n, IC.size)).copy()
    out = {}
    if t_need.size == 0:
        return out, t_need
    t_end = float(t_need[-1])
    nstep = int(round(t_end / DT)) if t_end > 0 else 0
    Itab = _inject_table(actions, nstep)
    ptr = 0
    if ptr < t_need.size and abs(t_need[ptr]) < 1e-12:
        out[0] = X.copy()
        ptr += 1
    ch2 = X[:, CH2_IDX].copy()
    wch = WCH2[CH2_IDX]
    for s in range(nstep):
        I = Itab[s]
        X = X + DT * _rhs_batch(X, I)
        np.clip(X, -6.0, 8.0, out=X)
        I2 = I[2]
        ch2 = DECAY * ch2 + (1.0 - DECAY) * V0_CH2 + GAIN * I2 * wch
        X[:, CH2_IDX] = ch2
        t = (s + 1) * DT
        while ptr < t_need.size and t + 1e-9 >= t_need[ptr]:
            out[ptr] = X.copy()
            ptr += 1
    while ptr < t_need.size:
        out[ptr] = X.copy()
        ptr += 1
    return out, t_need


def predict(actions, queries, n_samples=64, seed=0):
    actions = list(actions or [])
    queries = list(queries or [])
    n_samples = int(n_samples)
    all_t = []
    for q in queries:
        all_t.extend(q.get("t") or [])
    sim, t_need = _simulate(actions, all_t, 1, seed)
    t_to_idx = {_round_t(t_need[i]): i for i in range(len(t_need))}
    samples = []
    for q in queries:
        sensor = q["sensor"]
        times = list(q.get("t") or [])
        nslots = SLOTS[sensor]
        nT = len(times)
        arr = np.zeros((1, nT, 4, nslots), dtype=np.float64)
        for ti, tt in enumerate(times):
            rt = _round_t(tt)
            idx = t_to_idx.get(rt, None)
            if idx is None:
                idx = int(np.argmin(np.abs(t_need - rt))) if t_need.size else 0
            X = sim[idx]
            d0, d1, g = _unpack_batch(X)
            if sensor == "device0":
                y = _apply_device(d0, _U_of(actions, 0, float(tt)), 0)
            elif sensor == "device1":
                y = _apply_device(d1, _U_of(actions, 1, float(tt)), 1)
            else:
                y = g
            arr[0, ti] = y[0]
        if n_samples != 1:
            arr = np.repeat(arr, n_samples, axis=0)
        samples.append(arr)
    return {"samples": samples}
