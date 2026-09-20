import os
import json
import pickle
import numpy as np

_ROOT = os.path.dirname(os.path.abspath(__file__))
_DATA = np.load(os.path.join(_ROOT, "model_data.npz"), allow_pickle=False)
_T = _DATA["times"].astype(float)
_BASE = [_DATA["base0"].astype(float), _DATA["base1"].astype(float), _DATA["baseg"].astype(float)]
_PARAMS = _DATA["params"].astype(float)
_LIB = [_DATA["libD0"].astype(float), _DATA["libD1"].astype(float), _DATA["libDg"].astype(float)]
_P2C = [_DATA["p2c0"].astype(float), _DATA["p2c1"].astype(float), _DATA["p2cg"].astype(float)]
_NOISE_T = _DATA["noise_times"].astype(float)
_NOISE_S = _DATA["noise_stds"].astype(float)
with open(os.path.join(_ROOT, "adj_models.pkl"), "rb") as _f:
    _ADJ_MODELS = pickle.load(_f)
with open(os.path.join(_ROOT, "local_models.pkl"), "rb") as _f:
    _LOCAL_MODELS = pickle.load(_f)
# Single-threaded tree prediction is bitwise repeatable across calls.
for _m in list(_ADJ_MODELS) + list(_LOCAL_MODELS):
    if hasattr(_m, "n_jobs"):
        _m.n_jobs = 1

# The feature layout is shared with the fitted tree models.
def _time_features(t):
    t = np.asarray(t, dtype=float)
    return np.column_stack((t / 10.0, np.sin(.1*t), np.cos(.1*t),
                            np.sin(.264*t), np.cos(.264*t)))

def _interp_field(field, tq):
    """Linear interpolation of a (time, channel, slot) field."""
    tq = np.asarray(tq, dtype=float)
    flat = field.reshape(field.shape[0], -1)
    out = np.empty((len(tq), flat.shape[1]), dtype=float)
    for j in range(flat.shape[1]):
        out[:, j] = np.interp(tq, _T, flat[:, j])
    return out.reshape((len(tq),) + field.shape[1:])

def _hist_features(actions, t):
    # Must match the compact model's 76 history features.
    vals = []
    for p in range(4):
        acs = [a for a in actions if a.get("kind") == "inject" and int(a["port"]) == p]
        current = sum(float(a["amp"]) for a in acs
                      if float(a["t"]) <= t < float(a["t"]) + float(a["dur"]))
        integ = sum(float(a["amp"]) * max(0.0, min(t-float(a["t"]), float(a["dur"])))
                     for a in acs if t > float(a["t"]))
        past_amp = sum(float(a["amp"]) for a in acs if float(a["t"]) <= t)
        vals += [current, integ, past_amp]
        for lam in (.005, .05, .1, .2):
            z = 0.0
            for a in acs:
                s = float(a["t"]); d = float(a["dur"]); amp = float(a["amp"])
                if t > s:
                    age = max(0.0, min(t-s, d))
                    tail = max(0.0, t-s-d)
                    z += amp * (1.0-np.exp(-lam*age))/lam * np.exp(-lam*tail)
            vals.append(z)
        for freq in (.1, .264, .5):
            co = si = 0.0
            for a in acs:
                s = float(a["t"])
                if t > s:
                    age = t-s; amp = float(a["amp"])
                    w = amp*np.exp(-.05*age)
                    co += w*np.cos(freq*age); si += w*np.sin(freq*age)
            vals += [co, si]
    for dev in (0, 1):
        acs = [a for a in actions if a.get("kind") == "adjust" and int(a["device"]) == dev]
        for j in range(3):
            vals.append(sum(float(a["u"][j]) for a in acs if float(a["t"]) <= t))
        for j in range(3):
            vals.append(sum(float(a["u"][j]) for a in acs
                            if float(a["t"]) <= t and t-float(a["t"]) < 5.0))
        for lam in (.02, .1):
            for j in range(3):
                vals.append(sum(float(a["u"][j])*np.exp(-lam*max(0.0,t-float(a["t"])))
                                for a in acs if float(a["t"]) <= t))
    return vals

def _nearest_inject_response(action, sensor, times):
    p = int(action["port"]); s = float(action["t"]); amp = float(action["amp"]); dur = float(action["dur"])
    ids = np.flatnonzero(_PARAMS[:, 1].astype(int) == p)
    # The library is sparse. Favor start time, then amplitude and duration.
    dist = ((_PARAMS[ids, 2]-s)/10.0)**2 + ((_PARAMS[ids, 3]-amp)/1.5)**2 + ((_PARAMS[ids, 4]-dur)/4.0)**2
    ii = int(ids[int(np.argmin(dist))])
    ref = max(float(_PARAMS[ii, 3]), 1.e-6)
    raw = _LIB[sensor][ii] * (amp/ref)
    out = np.zeros((len(times),) + raw.shape[1:], dtype=float)
    src = _PARAMS[ii, 2] + (np.asarray(times, dtype=float)-s)
    mask = (np.asarray(times) >= s) & (src <= 50.0)
    if np.any(mask):
        out[mask] = _interp_field(raw, src[mask])
    # Port 2 is an exactly observed leaky integrator. Preserve that exact part
    # instead of interpolating a noisy training trajectory.
    if p == 2:
        lam = .005
        tt = np.asarray(times, dtype=float)
        x = np.zeros(len(tt), dtype=float)
        on = (tt > s) & (tt <= s + dur)
        after = tt > s + dur
        x[on] = amp * (1.0 - np.exp(-lam*(tt[on]-s))) / lam
        x[after] = amp * (1.0 - np.exp(-lam*dur)) / lam * np.exp(-lam*(tt[after]-s-dur))
        out[:, 2, :] = x[:, None] * _P2C[sensor][None, :]
    return out

def _inject_delta(actions, times):
    out = [np.zeros((len(times), 4, n), dtype=float) for n in (13, 19, 2)]
    for a in actions:
        if a.get("kind") != "inject":
            continue
        for sensor in range(3):
            out[sensor] += _nearest_inject_response(a, sensor, times)
    return out

def _adjust_delta(actions, times):
    out = np.zeros((len(times), 136), dtype=float)
    groups = {}
    for a in actions:
        if a.get("kind") == "adjust":
            groups.setdefault(round(float(a["t"]), 9), []).append(a)
    tt = np.asarray(times, dtype=float)
    for s, group in groups.items():
        u = np.zeros(6, dtype=float)
        for a in group:
            d = int(a["device"])*3
            u[d:d+3] += np.asarray(a["u"], dtype=float)
        mask = tt >= s
        if not np.any(mask):
            continue
        tau = tt[mask] - s
        feat = np.c_[np.broadcast_to(u, (len(tau), 6)), _time_features(tau)]
        r0 = _ADJ_MODELS[0].predict(feat)
        r1 = _ADJ_MODELS[1].predict(feat)
        out[mask, :52] += r0
        out[mask, 52:128] += r1
    return out

def _alias_fix(flat, times, actions):
    # Exact shared slots hold unless that device has already received an adjust.
    adj0 = [float(a["t"]) for a in actions if a.get("kind") == "adjust" and int(a["device"]) == 0]
    adj1 = [float(a["t"]) for a in actions if a.get("kind") == "adjust" and int(a["device"]) == 1]
    for k,t in enumerate(times):
        a0 = any(s <= t for s in adj0); a1 = any(s <= t for s in adj1)
        for c in range(4):
            for s0,s1 in ((6,10),(8,9),(11,4)):
                i0 = c*13+s0; i1 = 52+c*19+s1
                if not a0: flat[k,i0] = flat[k,i1]
                if not a1: flat[k,i1] = flat[k,i0]
    return flat

def _noise(times, n_samples, rng):
    if n_samples <= 0:
        return np.zeros((0,len(times),136), dtype=float)
    tt = np.asarray(times, dtype=float)
    std = np.empty((len(tt),136), dtype=float)
    for j in range(136):
        std[:,j] = np.interp(tt, _NOISE_T, _NOISE_S[:,j])
    # Measurement/process noise is small. Independent innovations are safer
    # than inventing large long-range correlations for arbitrary query grids.
    return rng.normal(size=(n_samples,len(tt),136)) * (0.7*std[None,:,:])

def predict(actions, queries, n_samples=64, seed=0):
    n_samples = int(n_samples)
    if not queries:
        return {"samples": []}
    # Empty queries still need correctly shaped arrays.
    nonempty = [q for q in queries if len(q.get("t", []))]
    if not nonempty:
        return {"samples": [np.zeros((n_samples, 0, 4,
                                        13 if q.get("sensor")=="device0" else 19 if q.get("sensor")=="device1" else 2), dtype=float)
                              for q in queries]}
    alltimes = np.unique(np.asarray([float(t) for q in nonempty for t in q["t"]], dtype=float))
    # Baseline and additive action response.
    base = [_interp_field(_BASE[i], alltimes) for i in range(3)]
    inj = _inject_delta(actions, alltimes)
    adj = _adjust_delta(actions, alltimes)
    addflat = np.concatenate([(base[i]+inj[i]).reshape(len(alltimes),-1) for i in range(3)], axis=1) + adj
    # Match fitted feature layout: 136 additive outputs + 76 history + 5 time features.
    hf = np.asarray([_hist_features(actions, float(t)) for t in alltimes], dtype=float)
    feat = np.c_[addflat, hf, _time_features(alltimes)]
    flat = addflat.copy()
    # Center the learned nonlinear correction on the no-action trajectory.
    # This removes tree-regression bias from the exactly reproducible baseline.
    zhist = np.zeros((len(alltimes), 76), dtype=float)
    zfeat = np.c_[np.concatenate([base[i].reshape(len(alltimes), -1) for i in range(3)], axis=1),
                  zhist, _time_features(alltimes)]
    flat[:, :52] += _LOCAL_MODELS[0].predict(feat) - _LOCAL_MODELS[0].predict(zfeat)
    flat[:, 52:128] += _LOCAL_MODELS[1].predict(feat) - _LOCAL_MODELS[1].predict(zfeat)
    if len(_LOCAL_MODELS) > 2:
        flat[:, 128:] += _LOCAL_MODELS[2].predict(feat) - _LOCAL_MODELS[2].predict(zfeat)
    # The port-2 channel-2 field is an exact leaky-integrator readout for
    # inject-only port-2 programs.
    nonzero_ports = {int(a["port"]) for a in actions
                     if a.get("kind") == "inject" and abs(float(a.get("amp", 0.0))) > 1.e-12}
    if (not any(a.get("kind") == "adjust" for a in actions)) and nonzero_ports and nonzero_ports <= {2}:
        flat[:, 2*13:3*13] = addflat[:, 2*13:3*13]
        flat[:, 52+2*19:52+3*19] = addflat[:, 52+2*19:52+3*19]
    flat = _alias_fix(flat, alltimes, actions)
    rng = np.random.default_rng(seed)
    eps = _noise(alltimes, n_samples, rng)
    # Keep the exact aliases in the stochastic draws too.
    samples_flat = flat[None,:,:] + eps
    # Enforce alias noise equality with the same time-dependent rule.
    for k,t in enumerate(alltimes):
        a0 = any(float(a["t"]) <= t for a in actions if a.get("kind")=="adjust" and int(a["device"])==0)
        a1 = any(float(a["t"]) <= t for a in actions if a.get("kind")=="adjust" and int(a["device"])==1)
        for c in range(4):
            for s0,s1 in ((6,10),(8,9),(11,4)):
                i0=c*13+s0; i1=52+c*19+s1
                if not a0: samples_flat[:,k,i0]=samples_flat[:,k,i1]
                if not a1: samples_flat[:,k,i1]=samples_flat[:,k,i0]
    results=[]
    for q in queries:
        ts=np.asarray(q.get("t", []), dtype=float)
        slots=13 if q.get("sensor")=="device0" else 19 if q.get("sensor")=="device1" else 2
        if len(ts)==0:
            results.append(np.zeros((n_samples,0,4,slots),dtype=float)); continue
        ix=np.searchsorted(alltimes,ts)
        if q.get("sensor")=="device0": vals=samples_flat[:,:,0:52].reshape(n_samples,len(alltimes),4,13)[:,ix]
        elif q.get("sensor")=="device1": vals=samples_flat[:,:,52:128].reshape(n_samples,len(alltimes),4,19)[:,ix]
        else: vals=samples_flat[:,:,128:136].reshape(n_samples,len(alltimes),4,2)[:,ix]
        results.append(np.asarray(vals,dtype=float))
    return {"samples": results}
