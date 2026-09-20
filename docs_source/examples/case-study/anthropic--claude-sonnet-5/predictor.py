
import os
import sys
import gzip
import pickle
import numpy as np

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)

from feature_lib import featurize2


def _load_pickle_maybe_gzip(path):
    with open(path, "rb") as fh:
        magic = fh.read(2)
    opener = gzip.open if magic == b"\x1f\x8b" else open
    with opener(path, "rb") as fh:
        return pickle.load(fh)


_MODELS_PATH = os.path.join(_THIS_DIR, "final_models.pkl")
_NOISE_PATH = os.path.join(_THIS_DIR, "noise_model.pkl")

_saved = _load_pickle_maybe_gzip(_MODELS_PATH)
MODELS = _saved["models"]                        # dict: channel(int) -> list of 34 fitted regressors
CHANNEL_TRANSFORM = _saved["channel_transform"]   # dict: channel(int) -> 'raw' | 'log1p'

NOISE_MODEL = _load_pickle_maybe_gzip(_NOISE_PATH)  # dict: channel(int) -> {xv, yv, L, idio_var}

DEVICE0_SLOTS = 13
DEVICE1_SLOTS = 19
GLOBAL_SLOTS = 2
TOTAL_SLOTS = DEVICE0_SLOTS + DEVICE1_SLOTS + GLOBAL_SLOTS  # 34

SENSOR_SLICE = {
    "device0": (0, DEVICE0_SLOTS),
    "device1": (DEVICE0_SLOTS, DEVICE0_SLOTS + DEVICE1_SLOTS),
    "global": (DEVICE0_SLOTS + DEVICE1_SLOTS, TOTAL_SLOTS),
}
SENSOR_NSLOTS = {"device0": DEVICE0_SLOTS, "device1": DEVICE1_SLOTS, "global": GLOBAL_SLOTS}

_CLIP_LOG = 40.0


def _inv_transform(y, kind):
    if kind == "log1p":
        return np.expm1(np.clip(y, -_CLIP_LOG, _CLIP_LOG))
    return y


def _predict_mean_transformed(actions, times):
    """Return dict channel -> (m, 34) array in the model's native (transformed) space."""
    m = len(times)
    if m == 0:
        return {c: np.zeros((0, TOTAL_SLOTS)) for c in range(4)}
    feats = np.stack([featurize2(actions, float(t)) for t in times], axis=0)
    out = {}
    for c in range(4):
        preds = np.zeros((m, TOTAL_SLOTS))
        models_c = MODELS[c]
        for slot in range(TOTAL_SLOTS):
            preds[:, slot] = models_c[slot].predict(feats)
        out[c] = preds
    return out


def _sample_brownian_ratio(times_sorted, n_samples, n_series, rng):
    """
    times_sorted: 1D sorted array of distinct non-negative times.
    Returns (n_samples, n_series, len(times_sorted)):
      value 0 exactly at t == 0; marginal variance 1 at each t > 0;
      cov(f(t1), f(t2)) = sqrt(min/max) for t1,t2 > 0; independent across series.
    """
    times_sorted = np.asarray(times_sorted, dtype=np.float64)
    m = len(times_sorted)
    out = np.zeros((n_samples, n_series, m))
    pos_mask = times_sorted > 0
    pos_times = times_sorted[pos_mask]
    if len(pos_times) > 0:
        prev = np.concatenate([[0.0], pos_times[:-1]])
        dt = np.maximum(pos_times - prev, 0.0)
        increments = rng.standard_normal(size=(n_samples, n_series, len(pos_times))) * np.sqrt(dt)[None, None, :]
        B = np.cumsum(increments, axis=2)
        f_vals = B / np.sqrt(pos_times)[None, None, :]
        out[:, :, pos_mask] = f_vals
    return out


def _time_key(t):
    return round(float(t) * 50.0)


def predict(actions, queries, n_samples=64, seed=0):
    n_samples = int(n_samples)
    rng = np.random.default_rng(int(seed))

    if len(queries) == 0:
        return {"samples": []}

    # union of all distinct requested times (rounded to the 0.02 grid for robust matching)
    key_to_time = {}
    for q in queries:
        for t in q.get("t", []):
            key_to_time[_time_key(t)] = float(t)
    all_keys_sorted = sorted(key_to_time.keys())
    all_times = np.array([key_to_time[k] for k in all_keys_sorted], dtype=np.float64)
    m = len(all_times)
    key_to_index = {k: i for i, k in enumerate(all_keys_sorted)}

    if m == 0:
        result = []
        for q in queries:
            nslots = SENSOR_NSLOTS[q["sensor"]]
            result.append(np.zeros((n_samples, 0, 4, nslots), dtype=np.float64))
        return {"samples": result}

    means_transformed = _predict_mean_transformed(actions, all_times)  # c -> (m,34)

    # build per-channel sample array in RAW (inverse-transformed) space: (n_samples, m, 34)
    channel_raw_samples = {}
    for c in range(4):
        nm = NOISE_MODEL[c]
        L = nm["L"]
        idio_var = nm["idio_var"]
        K = L.shape[1]

        factor_traj = _sample_brownian_ratio(all_times, n_samples, K, rng)       # (n_samples,K,m)
        idio_traj = _sample_brownian_ratio(all_times, n_samples, TOTAL_SLOTS, rng)  # (n_samples,34,m)

        common = np.einsum('sk,nkt->nst', L, factor_traj)          # (n_samples,34,m)
        idio_scale = np.sqrt(np.clip(idio_var, 0.0, None))[None, :, None]
        normalized = common + idio_scale * idio_traj               # (n_samples,34,m)
        normalized = np.transpose(normalized, (0, 2, 1))           # (n_samples,m,34)

        xv = nm["xv"]
        yv = nm["yv"]
        std_scale = np.stack([np.interp(all_times, xv, yv[:, slot]) for slot in range(TOTAL_SLOTS)], axis=1)  # (m,34)

        transformed_sample = means_transformed[c][None, :, :] + normalized * std_scale[None, :, :]
        kind = CHANNEL_TRANSFORM[c]
        raw_sample = _inv_transform(transformed_sample, kind)
        channel_raw_samples[c] = raw_sample

    results = []
    for q in queries:
        sensor = q["sensor"]
        times_q = q.get("t", [])
        nslots = SENSOR_NSLOTS[sensor]
        lo, hi = SENSOR_SLICE[sensor]
        n_t = len(times_q)
        if n_t == 0:
            results.append(np.zeros((n_samples, 0, 4, nslots), dtype=np.float64))
            continue
        idxs = [key_to_index[_time_key(t)] for t in times_q]
        arr = np.zeros((n_samples, n_t, 4, nslots), dtype=np.float64)
        for c in range(4):
            sub = channel_raw_samples[c][:, idxs, lo:hi]  # (n_samples, n_t, nslots)
            arr[:, :, c, :] = sub
        arr = np.nan_to_num(arr, nan=0.0, posinf=1e12, neginf=-1e12)
        results.append(arr)

    return {"samples": results}
