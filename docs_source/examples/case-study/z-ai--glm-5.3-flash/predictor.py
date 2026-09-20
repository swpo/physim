import numpy as np
from pathlib import Path

_W = Path(__file__).parent
_A = np.load(_W / "predictor_assets.npz")
pfit = _A["pfit"]; C0 = _A["C0"]; C1 = _A["C1"]; Cg = _A["Cg"]
sig0 = _A["sig0"]; sig1 = _A["sig1"]; sigG = _A["sigG"]
_FB = np.load(_W / "fam_bank.npz")
FAM = {}
for k in _FB.files:
    base, t0 = k.rsplit("_", 1)
    arr = _FB[k]
    FAM.setdefault(base, {})[float(t0)] = (arr[:, 0].copy(), arr[:, 1:].copy())
_OE = np.load(_W / "oe_bank.npz") if (_W / "oe_bank.npz").exists() else {}

l1, w1, l2, w2, r1_0, ps1_0, r2_0, ps2_0, nu, x30 = pfit
_NSL = {"device0": 13, "device1": 19, "global": 2}
_DIM = {"device0": 52, "device1": 76, "global": 8}
_OFF = {"device0": 0, "device1": 52, "global": 128}

def _state(t):
    t = np.atleast_1d(np.asarray(t, dtype=float))
    v1 = np.stack([r1_0*np.cos(w1*t + ps1_0), r1_0*np.sin(w1*t + ps1_0)], 1) * np.exp(l1*t)[:, None]
    v2 = np.stack([r2_0*np.cos(w2*t + ps2_0), r2_0*np.sin(w2*t + ps2_0)], 1) * np.exp(l2*t)[:, None]
    x3 = x30*np.exp(-nu*t)
    return np.hstack([v1, v2, x3[:, None]])

def _baseline(times):
    S = _state(times)
    X = np.hstack([S, np.ones((len(times), 1))])
    return {"device0": X @ C0, "device1": X @ C1, "global": X @ Cg}

def _dev_from_family(key, t0, times, scale=1.0, cols=None):
    bank = FAM.get(key)
    if bank is None or scale == 0.0:
        return None
    t0s = np.array(sorted(bank.keys()))
    tau = np.asarray(times, dtype=float) - t0
    out = None
    if t0 <= t0s[0]:
        out = np.zeros((len(times), _outdim(bank, t0s[0], cols)))
        _accum(bank, t0s[0], 1.0, tau, scale, cols, out)
    elif t0 >= t0s[-1]:
        out = np.zeros((len(times), _outdim(bank, t0s[-1], cols)))
        _accum(bank, t0s[-1], 1.0, tau, scale, cols, out)
    else:
        i = int(np.searchsorted(t0s, t0))
        t0a, t0b = t0s[i - 1], t0s[i]
        wa = (t0b - t0) / (t0b - t0a)
        out = np.zeros((len(times), _outdim(bank, t0a, cols)))
        _accum(bank, t0a, wa, tau, scale, cols, out)
        _accum(bank, t0b, 1.0 - wa, tau, scale, cols, out)
    return out

def _outdim(bank, tk, cols):
    d = bank[tk][1]
    return d.shape[1] if cols is None else d[:, cols].shape[1]

def _accum(bank, tk, wgt, tau, scale, cols, out):
    ta, d = bank[tk]
    dd = d if cols is None else d[:, cols]
    mask = np.clip(tau / 0.4, 0.0, 1.0)
    for j in range(dd.shape[1]):
        out[:, j] += wgt * scale * mask * np.interp(tau, ta, dd[:, j])

def _adjust_dev(key, uc, t0, times, sensor):
    nslot = _NSL[sensor]
    base_off = _OFF[sensor]
    cols = slice(base_off, base_off + 4 * nslot)
    dv1 = _dev_from_family(key, t0, times, scale=1.0, cols=cols)
    if dv1 is None and key[1] == "1" and key.endswith("d1"):
        dv1 = _dev_from_family("v1d1", t0, times, scale=1.0, cols=cols)
    if dv1 is None and key[1] == "2" and key.endswith("d1"):
        dv1 = _dev_from_family("v2d1", t0, times, scale=1.0, cols=cols)
    if dv1 is None and key[1] == "3" and key.endswith("d1"):
        dv1 = _dev_from_family("v3d1", t0, times, scale=1.0, cols=cols)
    if dv1 is None:
        return None
    dv = uc * dv1.copy()
    return dv

def predict(actions, queries, n_samples=64, seed=0):
    rng = np.random.default_rng(seed)
    qinfo = [(q["sensor"], np.asarray(q["t"], dtype=float)) for q in queries]
    dev_acc = {}
    for a in (actions or []):
        kind = a.get("kind")
        t0 = float(a["t"])
        if kind == "inject":
            p = int(a["port"]); amp = float(a["amp"]); dur = float(a["dur"])
            key = "p" + str(p)
            ncopies = max(1, int(round(dur / 0.2)))
            if p == 2:
                modal_ratio = min((dur / 0.2) ** 0.16, 1.30)
            elif p == 3:
                modal_ratio = min((dur / 0.2) ** 0.77, 6.2)
            elif p == 1:
                modal_ratio = (dur / 0.2) ** 0.90
            else:
                modal_ratio = (dur / 0.2) ** 0.96
            mscl = amp * modal_ratio / ncopies
            xscl = amp * dur / 0.2 / ncopies
            jobs = [(key, t0 + 0.2 * k, mscl, xscl) for k in range(ncopies)]
            for (kj, tj, ms, xs) in jobs:
                for sensor, ts in qinfo:
                    nslot = _NSL[sensor]
                    cm, cx = [], []
                    for c4 in range(4):
                        for s in range(nslot):
                            (cx if c4 == 2 else cm).append(c4 * nslot + s)
                    dm = _dev_from_family(kj, tj, ts, scale=ms, cols=None)
                    dx = _dev_from_family(kj, tj, ts, scale=xs, cols=None)
                    if dm is None:
                        continue
                    off = _OFF[sensor]
                    dv = np.zeros((len(ts), _DIM[sensor]))
                    dv[:, cm] += dm[:, off + np.array(cm)]
                    dv[:, cx] += dx[:, off + np.array(cx)]
                    dev_acc.setdefault(sensor, np.zeros((len(ts), _DIM[sensor])))
                    dev_acc[sensor] += dv
        elif kind == "adjust":
            u = [float(x) for x in a["u"]]
            d = int(a["device"])
            for ci, uc in enumerate(u):
                if uc == 0.0:
                    continue
                key = "u" + str(ci + 1) + "d" + str(d)
                for sensor, ts in qinfo:
                    dv = _adjust_dev(key, uc, t0, ts, sensor)
                    if dv is None:
                        continue
                    dev_acc.setdefault(sensor, np.zeros((len(ts), _DIM[sensor])))
                    dev_acc[sensor] += dv
    samples = []
    for sensor, ts in qinfo:
        base = _baseline(ts)[sensor]
        dv = dev_acc.get(sensor)
        mean = base if dv is None else base + dv
        T = len(ts)
        nslot = _NSL[sensor]
        sg = {"device0": sig0, "device1": sig1, "global": sigG}[sensor]
        tt = np.maximum(ts, 0.4)
        std = np.zeros((T, 4 * nslot))
        for c4 in range(4):
            for s in range(nslot):
                std[:, c4 * nslot + s] = sg[c4, s] * np.sqrt(tt)
        infl = 0.45 * (np.abs(dv) if dv is not None else 0.0)
        std_total = np.sqrt(std ** 2 + infl ** 2)
        S = np.empty((n_samples, T, 4, nslot))
        for k in range(n_samples):
            noise = rng.standard_normal((T, 4 * nslot)) * std_total
            S[k] = (mean + noise).reshape(T, 4, nslot)
        samples.append(S)
    return {"samples": samples}
