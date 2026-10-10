"""Empirical predictor for the laboratory world.

The model separates the unadjusted apparatus, for which the observations are
well described by smooth causal pulse-response features, from adjustment-only
programs.  It is intentionally self contained: the fitting data are the
laboratory observations captured during investigation.
"""

import glob
import json
import os

import joblib
import numpy as np
from scipy.interpolate import CubicSpline
from sklearn.linear_model import Ridge
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler


_SLOTS = {"device0": 13, "device1": 19, "global": 2}
_CENTERS = np.array(
    [0.0, 0.05, 0.12, 0.25, 0.5, 0.8, 1.3, 2.0, 3.0, 4.5,
     6.5, 9.0, 13.0, 18.0, 25.0, 35.0, 45.0], dtype=float
)
_WIDTHS = np.maximum(0.08, _CENTERS * 0.30)
_CACHE = None


def _adjusted_q_feature(q, centers, rbf=False):
    """Position features used by the serialized adjusted-readout models."""
    q = np.asarray(q, dtype=float)
    ans = [*q, *(q * q), *(q * q * q), q[0] * q[1], q[0] * q[2],
           q[1] * q[2], float(np.linalg.norm(q))]
    if rbf:
        r = np.sum((np.asarray(centers, dtype=float) - q) ** 2, axis=1)
        ans.extend(np.exp(-r / .35))
        ans.extend(np.exp(-r / 1.4))
    return np.asarray(ans, dtype=float)


def _load_adjusted_models():
    """Load the offline position/readout fit if it accompanies this file."""
    path = os.path.join(os.path.dirname(__file__), "adjusted_models.joblib")
    try:
        item = joblib.load(path)
        if item.get("version") == 1 and "models" in item and "centers" in item:
            return item
    except Exception:
        pass
    return None


def _num(x):
    return float(x)


def _q_at(actions, device, t):
    q = np.zeros(3, dtype=float)
    for a in actions:
        if a.get("kind") == "adjust" and int(a["device"]) == device and _num(a["t"]) <= t + 1e-10:
            q += np.asarray(a["u"], dtype=float)
    return q


def _has_injection(actions):
    return any(a.get("kind") == "inject" and abs(_num(a.get("amp", 0.0))) > 1e-14 for a in actions)


def _has_nonzero_adjustment(actions):
    return any(
        a.get("kind") == "adjust" and np.max(np.abs(np.asarray(a["u"], dtype=float))) > 1e-14
        for a in actions
    )


def _q0_feature(actions, t):
    """Causal features for the q=0 controlled world.

    At the unadjusted origin the two inject interfaces are experimentally
    equivalent, so ports are aggregated over devices.  A rectangular pulse is
    represented by causal start and end histories.
    """
    z = [t / 50.0, (t / 50.0) ** 2]
    for w in (0.015, 0.025, 0.04, 0.06, 0.08, 0.12, 0.18, 0.27, 0.40):
        z.extend((np.sin(w * t), np.cos(w * t)))
    for port in range(4):
        current = 0.0
        starts = []
        ends = []
        for a in actions:
            if a.get("kind") != "inject" or int(a["port"]) != port:
                continue
            s = _num(a["t"])
            e = s + _num(a["dur"])
            amp = _num(a["amp"])
            if t >= s:
                starts.append((t - s, amp))
            if t >= e:
                ends.append((t - e, amp))
            if s <= t < e:
                current += amp
        z.append(current)
        for c, w in zip(_CENTERS, _WIDTHS):
            z.append(sum(a * np.exp(-0.5 * ((u - c) / w) ** 2) for u, a in starts))
            z.append(sum(a * np.exp(-0.5 * ((u - c) / w) ** 2) for u, a in ends))
            tau = max(0.15, c + 0.10)
            z.append(
                sum(a * np.exp(-u / tau) for u, a in starts)
                - sum(a * np.exp(-u / tau) for u, a in ends)
            )
    return np.asarray(z, dtype=float)


def _adjust_feature(actions, device, t):
    b = [t / 50.0]
    for w in (0.02, 0.04, 0.06, 0.08, 0.12, 0.18, 0.28):
        b.extend((np.sin(w * t), np.cos(w * t)))
    q = _q_at(actions, device, t)
    v = list(q) + list(q * q) + list(q * q * q) + [q[0] * q[1], q[0] * q[2], q[1] * q[2]]
    return np.asarray(b + v + [x * y for x in b for y in v], dtype=float)


def _parse_observations():
    records = []
    for path in sorted(glob.glob("/observations/experiment_*.npz")):
        try:
            with np.load(path, allow_pickle=False) as data:
                request = json.loads(data["request"].item())
                entries = []
                for i, q in enumerate(request.get("queries", [])):
                    sensor = q.get("sensor")
                    if sensor not in _SLOTS:
                        continue
                    ts = np.asarray(q.get("t", []), dtype=float)
                    vals = data[f"query{i}"][0].astype(float, copy=True)
                    entries.append((sensor, ts, vals))
                records.append((path, request.get("actions", []), entries))
        except Exception:
            # A partially written or unrelated observation should not prevent a
            # valid predictor from using the remaining measurements.
            continue
    return records


class _SensorQ0:
    def __init__(self, sensor, rows):
        self.sensor = sensor
        self.slots = _SLOTS[sensor]
        self.ready = False
        if not rows:
            return
        x = np.asarray([_q0_feature(a, t) for a, t, _ in rows], dtype=float)
        y = np.asarray([v.reshape(4, self.slots) for _, _, v in rows], dtype=float)
        self.xscale = StandardScaler().fit(x)
        xs = self.xscale.transform(x)

        # The three direct channels are close to linear in the causal pulse
        # basis.  Channel one has the notable saturation/nonlinear response,
        # for which a compact MLP is much more accurate.
        alphas = (100.0, None, 0.001, 0.1)
        self.raw = {}
        for c in (0, 2, 3):
            self.raw[c] = Ridge(alpha=alphas[c]).fit(xs, y[:, c, :])

        yc = y[:, 1, :]
        self.c1_scale = np.percentile(np.abs(yc), 80, axis=0) + 0.03
        ty = np.sign(yc) * np.log1p(np.abs(yc) / self.c1_scale)
        self.c1_y_scale = StandardScaler().fit(ty)
        self.c1 = MLPRegressor(
            hidden_layer_sizes=(320, 320),
            activation="relu",
            max_iter=900,
            early_stopping=True,
            validation_fraction=0.12,
            alpha=5e-4,
            learning_rate_init=8e-4,
            batch_size=128,
            random_state=31,
        ).fit(xs, self.c1_y_scale.transform(ty))
        self.ready = True

    def predict(self, actions, times):
        n = len(times)
        out = np.zeros((n, 4, self.slots), dtype=float)
        if not self.ready or n == 0:
            return out
        x = np.asarray([_q0_feature(actions, float(t)) for t in times], dtype=float)
        xs = self.xscale.transform(x)
        for c, model in self.raw.items():
            out[:, c, :] = model.predict(xs)
        z = self.c1_y_scale.inverse_transform(self.c1.predict(xs))
        out[:, 1, :] = np.sign(z) * self.c1_scale * np.expm1(np.clip(np.abs(z), 0.0, 5.0))
        return out

    def c2(self, actions, times):
        if not self.ready:
            return np.zeros((len(times), self.slots), dtype=float)
        x = np.asarray([_q0_feature(actions, float(t)) for t in times], dtype=float)
        return self.raw[2].predict(self.xscale.transform(x))


class _AdjustmentOnly:
    def __init__(self, sensor, rows):
        self.sensor = sensor
        self.device = 0 if sensor == "device0" else 1
        self.slots = _SLOTS[sensor]
        self.ready = False
        if not rows:
            return
        x = np.asarray([_adjust_feature(a, self.device, t) for a, t, _ in rows], dtype=float)
        y = np.asarray([v for _, _, v in rows], dtype=float)
        self.scale = StandardScaler().fit(x)
        # Broad regularization is deliberately preferred here: adjustment
        # samples cover a wide, continuous position space.
        alpha = 10.0 if sensor == "device0" else 100.0
        self.model = Ridge(alpha=alpha).fit(self.scale.transform(x), y)
        self.ready = True

    def predict(self, actions, times):
        if not self.ready or len(times) == 0:
            return np.zeros((len(times), 4, self.slots), dtype=float)
        x = np.asarray([_adjust_feature(actions, self.device, float(t)) for t in times], dtype=float)
        return self.model.predict(self.scale.transform(x)).reshape(len(times), 4, self.slots)


class _WorldModel:
    def __init__(self):
        self.records = _parse_observations()
        self.adjusted_models = _load_adjusted_models()
        self.baselines = self._fit_baselines()
        no_adjust = {s: [] for s in _SLOTS}
        only_adjust = {"device0": [], "device1": []}
        for _, actions, entries in self.records:
            clean = not _has_nonzero_adjustment(actions)
            inj = _has_injection(actions)
            for sensor, ts, vals in entries:
                for t, v in zip(ts, vals):
                    row = (actions, float(t), v.reshape(-1))
                    if clean:
                        no_adjust[sensor].append(row)
                    if not inj and sensor in only_adjust:
                        only_adjust[sensor].append(row)
        self.q0 = {s: _SensorQ0(s, no_adjust[s]) for s in _SLOTS}
        self.adjust = {s: _AdjustmentOnly(s, only_adjust[s]) for s in ("device0", "device1")}
        self._fit_global_c2()

    def adjusted_device_prediction(self, sensor, actions, times):
        """Predict a position-controlled device readout from frozen experts."""
        if self.adjusted_models is None or sensor not in self.adjusted_models["models"]:
            return None
        experts = self.adjusted_models["models"][sensor]
        slots = _SLOTS[sensor]
        device = 0 if sensor == "device0" else 1
        centers = self.adjusted_models["centers"]
        n = len(times)
        basic_rows = []
        rbf_rows = []
        eye = np.eye(slots)
        for t in times:
            h = _q0_feature(actions, float(t))
            q = _q_at(actions, device, float(t))
            b = np.r_[h, _adjusted_q_feature(q, centers, False)]
            r = np.r_[h, _adjusted_q_feature(q, centers, True)]
            basic_rows.append(np.c_[np.repeat(b[None, :], slots, axis=0), eye])
            rbf_rows.append(np.c_[np.repeat(r[None, :], slots, axis=0), eye])
        basic = np.concatenate(basic_rows, axis=0)
        radial = np.concatenate(rbf_rows, axis=0)
        out = np.empty((n, 4, slots), dtype=float)
        for channel in range(4):
            pred = []
            for pack in experts.get(channel, []):
                x = radial if pack.get("rbf") else basic
                z = pack["yscale"].inverse_transform(
                    pack["model"].predict(pack["xscale"].transform(x))[:, None]
                ).ravel()
                if pack.get("kind") == "signed_log":
                    scale = float(pack["target_scale"])
                    z = np.sign(z) * scale * np.expm1(np.clip(np.abs(z), 0.0, 5.0))
                pred.append(z)
            if pred:
                out[:, channel, :] = np.mean(np.asarray(pred), axis=0).reshape(n, slots)
            else:
                out[:, channel, :] = 0.0
        # Intensities are nonnegative apart from the laboratory's negligible
        # numerical jitter.  This avoids an unconstrained extrapolation from
        # inventing a large negative pulse.
        out[:, 2, :] = np.maximum(out[:, 2, :], -1e-4)
        return out

    def _fit_baselines(self):
        # experiment_001 is the sole densely sampled unforced reference for
        # all three interfaces.  Cubic interpolation also supports .02 query
        # times cleanly.
        base = {}
        if not self.records:
            return base
        chosen = None
        for _, actions, entries in self.records:
            if not actions and {x[0] for x in entries} >= set(_SLOTS):
                chosen = entries
                break
        if chosen is None:
            chosen = self.records[0][2]
        for sensor, ts, vals in chosen:
            flat = vals.reshape(len(ts), -1)
            if len(ts) >= 2:
                try:
                    base[sensor] = CubicSpline(ts, flat, axis=0)
                except Exception:
                    base[sensor] = (ts.copy(), flat.copy())
        return base

    def baseline(self, sensor, times):
        n = len(times)
        slots = _SLOTS[sensor]
        b = self.baselines.get(sensor)
        if b is None:
            return np.zeros((n, 4, slots), dtype=float)
        if isinstance(b, tuple):
            tt, vv = b
            ans = np.empty((n, vv.shape[1]), dtype=float)
            for j in range(vv.shape[1]):
                ans[:, j] = np.interp(times, tt, vv[:, j])
        else:
            ans = b(np.asarray(times, dtype=float))
        return np.asarray(ans, dtype=float).reshape(n, 4, slots)

    def _fit_global_c2(self):
        self.global_c2 = None
        xs = []
        ys = []
        for _, actions, entries in self.records:
            if _has_nonzero_adjustment(actions):
                continue
            lookup = {s: (t, v) for s, t, v in entries}
            if "device0" not in lookup or "global" not in lookup:
                continue
            td, vd = lookup["device0"]
            tg, vg = lookup["global"]
            # Align only timestamps present in both requests.
            for j, t in enumerate(tg):
                k = np.where(np.isclose(td, t, atol=1e-9))[0]
                if len(k):
                    xs.append((_q0_feature(actions, float(t)), vg[j, 2, :].reshape(-1)))
        if len(xs) < 12 or not self.q0["device0"].ready:
            return
        f = np.asarray([x for x, _ in xs], dtype=float)
        target = np.asarray([y for _, y in xs], dtype=float)
        # First use the especially accurate local channel-two model, then a
        # small nonlinear static map to the global variance channel.
        d0 = self.q0["device0"].raw[2].predict(self.q0["device0"].xscale.transform(f))
        z = np.c_[
            d0,
            np.sqrt(np.maximum(d0, 0.0)),
            np.log1p(np.maximum(d0, 0.0)),
            d0 * d0,
            d0 * d0 * d0,
        ]
        self.global_c2_scale = StandardScaler().fit(z)
        self.global_c2 = Ridge(alpha=0.01).fit(self.global_c2_scale.transform(z), target)

    def _q0_prediction(self, sensor, actions, times):
        out = self.q0[sensor].predict(actions, times)
        if sensor == "global" and self.global_c2 is not None and len(times):
            d0 = self.q0["device0"].c2(actions, times)
            z = np.c_[
                d0,
                np.sqrt(np.maximum(d0, 0.0)),
                np.log1p(np.maximum(d0, 0.0)),
                d0 * d0,
                d0 * d0 * d0,
            ]
            out[:, 2, :] = self.global_c2.predict(self.global_c2_scale.transform(z))
        return out

    def predict_sensor(self, sensor, actions, times):
        times = np.asarray(times, dtype=float)
        n = len(times)
        if n == 0:
            return np.empty((0, 4, _SLOTS[sensor]), dtype=float)
        injected = _has_injection(actions)
        adjusted = _has_nonzero_adjustment(actions)
        if sensor != "global" and adjusted:
            model_out = self.adjusted_device_prediction(sensor, actions, times)
            if model_out is not None:
                # At an exactly unadjusted readout position, retain the more
                # accurate causal origin model.  This also handles a clean
                # cancellation of adjustments before a requested time.
                reference = self._q0_prediction(sensor, actions, times) if injected else self.baseline(sensor, times)
                device = 0 if sensor == "device0" else 1
                for i, t in enumerate(times):
                    if np.max(np.abs(_q_at(actions, device, float(t)))) < 1e-12:
                        model_out[i] = reference[i]
                return model_out
        if not injected:
            if sensor == "global" or not adjusted:
                return self.baseline(sensor, times)
            # For pure adjustment programs, positions are directly observed in
            # the adjustment-only calibration set.  Preserve the exact baseline
            # at any timestamp whose cumulative displacement is zero.
            out = self.adjust[sensor].predict(actions, times)
            base = self.baseline(sensor, times)
            dev = 0 if sensor == "device0" else 1
            for i, t in enumerate(times):
                if np.max(np.abs(_q_at(actions, dev, float(t)))) < 1e-12:
                    out[i] = base[i]
            return out
        # Position-controlled sources are much less well constrained than the
        # unadjusted response.  The zero-position pulse model remains the most
        # reliable extrapolator; it is also exactly correct whenever all
        # adjustments cancel before an injection.
        return self._q0_prediction(sensor, actions, times)


def _model():
    global _CACHE
    if _CACHE is None:
        _CACHE = _WorldModel()
    return _CACHE


def predict(actions, queries, n_samples=64, seed=0):
    """Return coherent samples for the requested laboratory measurements."""
    # The learned posterior is sharply concentrated compared with the response
    # scale.  Repeating its conditional mean avoids injecting spurious,
    # uncorrelated noise between simultaneously requested interfaces.
    ns = int(n_samples)
    m = _model() if queries else None
    result = []
    for q in queries:
        sensor = q["sensor"]
        slots = _SLOTS[sensor]
        ts = np.asarray(q["t"], dtype=float)
        if len(ts):
            mean = m.predict_sensor(sensor, actions, ts)
        else:
            mean = np.empty((0, 4, slots), dtype=float)
        mean = np.nan_to_num(mean, nan=0.0, posinf=1e6, neginf=-1e6)
        mean = np.clip(mean, -1e6, 1e6)
        result.append(np.repeat(mean[None, ...], ns, axis=0).astype(float, copy=False))
    return {"samples": result}
