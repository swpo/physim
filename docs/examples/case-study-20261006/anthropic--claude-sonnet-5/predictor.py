import os
import numpy as np
from scipy.interpolate import interp1d

_DIR = os.path.dirname(os.path.abspath(__file__))
_DATA_PATH = os.path.join(_DIR, 'model_data.npz')

SENSORS = ['device0', 'device1', 'global']
SLOTS = {'device0': 13, 'device1': 19, 'global': 2}
N_CHANNELS = 4

_cache = {}


def _data():
    if 'd' not in _cache:
        with np.load(_DATA_PATH) as f:
            _cache['d'] = {k: f[k] for k in f.files}
    return _cache['d']


def _baseline_fn(sensor):
    key = ('baseline', sensor)
    if key in _cache:
        return _cache[key]
    d = _data()
    t19 = d[f'base_t19_{sensor}']
    v19 = d[f'base_v19_{sensor}']
    at = d[f'base_anchor_t_{sensor}']
    am = d[f'base_anchor_mean_{sensor}']
    f_dense = interp1d(t19, v19, axis=0, kind='linear', fill_value='extrapolate')
    corr = am - f_dense(at)
    f_corr = interp1d(at, corr, axis=0, kind='linear', fill_value='extrapolate')

    def fn(t):
        t = np.asarray(t, dtype=float)
        return f_dense(t) + f_corr(t)

    _cache[key] = fn
    return fn


def _noise_std_fn(sensor):
    key = ('noise', sensor)
    if key in _cache:
        return _cache[key]
    d = _data()
    t = d[f'noise_t_{sensor}']
    std = d[f'noise_std_{sensor}']
    f = interp1d(t, std, axis=0, kind='linear', fill_value=(std[0], std[-1]), bounds_error=False)

    def fn(tq):
        tq = np.asarray(tq, dtype=float)
        v = f(tq)
        return np.maximum(v, 1e-6)

    _cache[key] = fn
    return fn


class InjectModel:
    def __init__(self, port, sensor):
        d = _data()
        self.GRID_A = d['GRID_A']
        self.AMPS = np.asarray(d['AMPS'], dtype=float)
        self.DURS_RT = np.asarray(d['DURS_RT'], dtype=float)  # [1,2,4,8,16]
        self.K = d[f'K_p{port}_{sensor}']    # amp sweep at dur=2 (exact driven phase for tau<=2)
        self.KL = d[f'KL_p{port}_{sensor}']  # amp sweep at dur=16 (exact driven phase for tau<=16)
        self.RT = d[f'RT_p{port}_{sensor}']  # (5 durs, 11 amps, 19 tau, 4 ch, slots) - measured relax grid
        self._fK = interp1d(self.GRID_A, self.K, axis=1, kind='linear')
        self._fKL = interp1d(self.GRID_A, self.KL, axis=1, kind='linear')
        self._fRT_amp = interp1d(self.AMPS, self.RT, axis=1, kind='linear')
        self.K_BOUND = 2.0
        self.KL_BOUND = 16.0

    def _amp_interp(self, table_at_tau, amp):
        amp_c = float(np.clip(amp, self.AMPS[0], self.AMPS[-1]))
        f_amp = interp1d(self.AMPS, table_at_tau, axis=0, kind='linear')
        return f_amp(amp_c)

    def _K_amp_tau(self, amp, tau_c):
        return self._amp_interp(self._fK(tau_c), amp)

    def _KL_amp_tau(self, amp, tau_c):
        return self._amp_interp(self._fKL(tau_c), amp)

    def _driven(self, amp, tau):
        # Driven-phase response is dur-independent (confirmed experimentally), so for
        # tau <= dur we can read it directly off the amp-sweep tables measured at fixed
        # dur=2 / dur=16, without any amp-scaling assumption. A pooled/separable scaling
        # fit was tried first and badly mispredicted slots with strong amp nonlinearity
        # (e.g. port3 ch1/slot6, whose amp-dependence is non-monotonic, not just saturating).
        tau_c = np.clip(tau, 0.0, self.GRID_A[-1])
        out = np.empty(tau_c.shape + self.K.shape[2:])
        short = tau_c <= self.K_BOUND
        mid = (~short) & (tau_c <= self.KL_BOUND)
        beyond = tau_c > self.KL_BOUND
        if np.any(short):
            out[short] = self._K_amp_tau(amp, tau_c[short])
        if np.any(mid):
            out[mid] = self._KL_amp_tau(amp, tau_c[mid])
        if np.any(beyond):
            n = int(np.sum(beyond))
            out[beyond] = self._KL_amp_tau(amp, np.full(n, self.KL_BOUND))
        return out

    def _relax(self, amp, dur, tau):
        # Post-pulse relaxation shape depends jointly on (amp,dur) in a non-separable way
        # (a dur=2/dur=16-anchor correction badly mispredicted dur=3 relaxation rates for
        # several slots). Instead, use the directly-measured (dur x amp) relaxation grid
        # RT (anchors dur=[1,2,4,8,16], full amp sweep at each) and bilinearly interpolate:
        # first across amp at each dur anchor, then across log(dur) between the two
        # bracketing anchors. dur<1 flat-extrapolates off the dur=1 anchor (driven phase
        # there is still exact via K/KL; only the relax shape loses a bit of precision).
        tau_c = np.clip(tau, 0.0, self.GRID_A[-1])
        amp_c = float(np.clip(amp, self.AMPS[0], self.AMPS[-1]))
        dur_c = float(np.clip(dur, self.DURS_RT[0], self.DURS_RT[-1]))

        at_amp = self._fRT_amp(amp_c)  # (5 durs, 19 tau, 4, slots)
        f_dur = interp1d(np.log(self.DURS_RT), at_amp, axis=0, kind='linear')
        curve = f_dur(np.log(dur_c))  # (19 tau, 4, slots)
        f_tau = interp1d(self.GRID_A, curve, axis=0, kind='linear')
        return f_tau(tau_c)

    def response(self, amp, dur, tau):
        tau = np.atleast_1d(np.asarray(tau, dtype=float))
        n_slots = self.K.shape[-1]
        out = np.zeros(tau.shape + (N_CHANNELS, n_slots))
        if amp == 0:
            return out
        valid = tau >= 0
        active = valid & (tau <= dur)
        relaxed = valid & (tau > dur)
        idx_d = np.where(active)[0]
        idx_r = np.where(relaxed)[0]
        if len(idx_d):
            out[idx_d] = self._driven(amp, tau[idx_d])
        if len(idx_r):
            out[idx_r] = self._relax(amp, dur, tau[idx_r])
        return out


class AdjustModel:
    def __init__(self, device, axis, sensor):
        d = _data()
        self.GRID_A = d['GRID_A']
        self.mags = np.asarray(d[f'ADJ_MAGS_d{device}_a{axis}'], dtype=float)
        self.table = d[f'ADJ_d{device}_a{axis}_{sensor}']
        self._fcurve = interp1d(self.GRID_A, self.table, axis=1, kind='linear')

    def response(self, mag, tau):
        tau = np.atleast_1d(np.asarray(tau, dtype=float))
        n_slots = self.table.shape[-1]
        out = np.zeros(tau.shape + (N_CHANNELS, n_slots))
        if mag == 0:
            return out
        valid = tau >= 0
        idx = np.where(valid)[0]
        if len(idx) == 0:
            return out
        tau_c = np.clip(tau[idx], 0.0, self.GRID_A[-1])
        vals_at_tau = self._fcurve(tau_c)
        mag_c = float(np.clip(mag, self.mags[0], self.mags[-1]))
        f_mag = interp1d(self.mags, vals_at_tau, axis=0, kind='linear')
        out[idx] = f_mag(mag_c)
        return out


def _get_inject_model(port, sensor):
    key = ('inject', port, sensor)
    if key not in _cache:
        _cache[key] = InjectModel(port, sensor)
    return _cache[key]


def _get_adjust_model(device, axis, sensor):
    key = ('adjust', device, axis, sensor)
    if key not in _cache:
        _cache[key] = AdjustModel(device, axis, sensor)
    return _cache[key]


_COLLISION_GAMMA = 1.0
_MODEL_ERR_REL = 0.25   # model (interpolation/extrapolation) error scales with response magnitude
_MODEL_ERR_FLOOR = 0.03  # floor for near-baseline predictions


def _mean_prediction(actions, sensor, times):
    # Each action's own contribution (additive superposition) is accurate in isolation
    # (validated against held-out single-action experiments). But when 2+ actions
    # substantially drive the SAME (channel,slot) at the same time, the true system
    # shows a large, non-additive nonlinear interaction there (confirmed via held-out
    # multi-action experiments 150/151/302: errors up to ~2, comparable in size to the
    # smaller of the colliding contributions, with no simple sum/max/average rule fitting
    # consistently - one case even flips sign relative to any of those combination rules).
    # Rather than risk a wrong correction, keep the additive sum as the mean and instead
    # report a 'collision' magnitude (total contribution minus the dominant one) so the
    # caller can inflate predictive uncertainty specifically where it's warranted.
    times = np.asarray(times, dtype=float)
    n_t = len(times)
    n_slots = SLOTS[sensor]
    mean = _baseline_fn(sensor)(times).astype(float).copy()
    sum_abs = np.zeros((n_t, N_CHANNELS, n_slots))
    max_abs = np.zeros((n_t, N_CHANNELS, n_slots))
    for act in actions:
        t0 = float(act['t'])
        tau = times - t0
        if act['kind'] == 'inject':
            port = int(act['port'])
            amp = float(act['amp'])
            dur = float(act['dur'])
            model = _get_inject_model(port, sensor)
            c = model.response(amp, dur, tau)
        elif act['kind'] == 'adjust':
            device = int(act['device'])
            u = act['u']
            c = np.zeros((n_t, N_CHANNELS, n_slots))
            for axis in range(3):
                mag = float(u[axis])
                if mag == 0:
                    continue
                model = _get_adjust_model(device, axis, sensor)
                c = c + model.response(mag, tau)
        else:
            continue
        mean += c
        a = np.abs(c)
        sum_abs += a
        max_abs = np.maximum(max_abs, a)
    collision = np.maximum(sum_abs - max_abs, 0.0)
    dev_mag = np.abs(mean - _baseline_fn(sensor)(times))
    return mean, collision, dev_mag


def predict(actions, queries, n_samples=64, seed=0):
    rng = np.random.default_rng(seed)
    samples = []
    for q in queries:
        sensor = q['sensor']
        times = q['t']
        n_t = len(times)
        n_slots = SLOTS[sensor]
        if n_t == 0:
            samples.append(np.zeros((n_samples, 0, N_CHANNELS, n_slots)))
            continue
        mean, collision, dev_mag = _mean_prediction(actions, sensor, times)
        std = _noise_std_fn(sensor)(times)
        model_std = np.sqrt(_MODEL_ERR_FLOOR ** 2 + (_MODEL_ERR_REL * dev_mag) ** 2)
        total_std = np.sqrt(std ** 2 + model_std ** 2 + (_COLLISION_GAMMA * collision) ** 2)
        noise = rng.standard_normal((n_samples,) + mean.shape)
        arr = mean[None, :, :, :] + total_std[None, :, :, :] * noise
        arr = np.asarray(arr, dtype=float)
        arr[~np.isfinite(arr)] = 0.0
        samples.append(arr)
    return {"samples": samples}
