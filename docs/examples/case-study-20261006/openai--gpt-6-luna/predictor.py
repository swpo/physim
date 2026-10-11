import os

import numpy as np
from scipy.interpolate import CubicSpline


SENSORS = ("device0", "device1", "global")
SLOTS = {"device0": 13, "device1": 19, "global": 2}
RATES = (0.005, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0)
IMPULSE_RATES = (0.005, 0.05, 0.2, 1.0)
P2_K = 0.0050137463589797265
P2_NOISE_TIMES = np.asarray([0.0, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0])


def _load_model():
    path = os.path.join(os.path.dirname(__file__), "model.npz")
    if not os.path.exists(path):
        return {}
    with np.load(path, allow_pickle=False) as data:
        return {key: data[key].copy() for key in data.files}


_MODEL = _load_model()
_MODEL_NAMES = set(str(name) for name in _MODEL.get("model_names", ()))
_TREE_NAMES = set(str(name) for name in _MODEL.get("tree_model_names", ()))
_BASE_SPLINES = {
    sensor: CubicSpline(np.arange(51.0), _MODEL["base_" + sensor], axis=0, bc_type="natural")
    for sensor in SENSORS
    if "base_" + sensor in _MODEL
}


def _control_states(actions, times):
    times = np.asarray(times, dtype=float)
    states = np.zeros((len(times), 2, 3), dtype=float)
    adjustments = [action for action in actions if action["kind"] == "adjust"]
    for index, time in enumerate(times):
        for action in adjustments:
            if action["t"] <= time + 1e-9:
                states[index, action["device"]] += np.asarray(action["u"], dtype=float)
    return states


def _event_contexts(actions):
    state = np.zeros((2, 3), dtype=float)
    contexts = {}
    for index, action in enumerate(actions):
        if action["kind"] == "adjust":
            state[action["device"]] += np.asarray(action["u"], dtype=float)
        else:
            contexts[index] = state.copy()
    return contexts


def _injection_summary(actions, time, contexts=None):
    summary = np.zeros(1 + 2 * 4 * 28, dtype=float)
    summary[0] = time / 50.0
    if contexts is None:
        contexts = {}
    port_data = [[] for _ in range(2 * 4)]
    for index, action in enumerate(actions):
        if action["kind"] != "inject" or action["amp"] == 0.0:
            continue
        if time <= action["t"] + 1e-9:
            continue
        port_data[action["device"] * 4 + action["port"]].append((index, action, contexts.get(index, np.zeros((2, 3)))))

    offset = 1
    for events in port_data:
        if events:
            ages = [max(time - action["t"], 0.0) for _, action, _ in events]
            mass = sum(
                action["amp"] * min(age, action["dur"])
                for age, (_, action, _) in zip(ages, events)
            )
            active = sum(
                action["amp"]
                for age, (_, action, _) in zip(ages, events)
                if age < action["dur"] - 1e-9
            )
            dose = sum(action["amp"] * action["dur"] for _, action, _ in events)
            count = float(len(events))
            sum_amp = sum(action["amp"] for _, action, _ in events)
            sum_dur = sum(action["dur"] for _, action, _ in events)
            sum_amp_sq = sum(action["amp"] ** 2 for _, action, _ in events)
            sum_dur_sq = sum(action["dur"] ** 2 for _, action, _ in events)
            _, last_action, _ = max(events, key=lambda item: (item[1]["t"], item[0]))
            last_age = max(time - last_action["t"], 0.0)
            last_after = max(last_age - last_action["dur"], 0.0)
            direct = [
                mass,
                active,
                dose,
                count,
                sum_amp,
                sum_dur,
                sum_amp_sq,
                sum_dur_sq,
                last_action["amp"],
                last_action["dur"],
                last_action["t"] / 50.0,
                last_age / 50.0,
                last_after / 50.0,
            ]
            rates = []
            for rate in RATES:
                value = 0.0
                for age, (_, action, _) in zip(ages, events):
                    elapsed = min(age, action["dur"])
                    after = max(age - action["dur"], 0.0)
                    value += action["amp"] * (-np.expm1(-rate * elapsed)) / rate * np.exp(-rate * after)
                rates.append(value)
            impulse = []
            for rate in IMPULSE_RATES:
                start_value = 0.0
                end_value = 0.0
                for age, (_, action, _) in zip(ages, events):
                    amount = action["amp"] * action["dur"]
                    start_value += amount * np.exp(-rate * age)
                    end_value += amount * np.exp(-rate * max(age - action["dur"], 0.0))
                impulse.extend([start_value, end_value])
            values = direct + rates + impulse
            summary[offset:offset + 28] = values
        offset += 28
    return summary


def _joint_features(actions, time, control_state=None, contexts=None):
    if control_state is None:
        control_state = _control_states(actions, [time])[0]
    if contexts is None:
        contexts = _event_contexts(actions)
    injection = _injection_summary(actions, time, contexts)
    features = [time / 50.0]
    features.extend(control_state.reshape(-1))
    features.extend(injection[1:])

    per_port = injection[1:].reshape(2, 4, 28)
    for source_device in range(2):
        for port in range(4):
            mass = per_port[source_device, port, 0]
            slow = per_port[source_device, port, 15]
            for device in range(2):
                for axis in range(3):
                    features.append(control_state[device, axis] * mass)
                    features.append(control_state[device, axis] * slow)

    context_values = np.zeros((2, 4, 2, 3, 2), dtype=float)
    for index, action in enumerate(actions):
        if action["kind"] != "inject" or action["amp"] == 0.0 or time <= action["t"] + 1e-9:
            continue
        context = contexts.get(index)
        if context is None:
            continue
        age = max(time - action["t"], 0.0)
        elapsed = min(age, action["dur"])
        mass = action["amp"] * elapsed
        dose = action["amp"] * action["dur"]
        context_values[action["device"], action["port"], :, :, 0] += context * dose
        context_values[action["device"], action["port"], :, :, 1] += context * mass
    features.extend(context_values.reshape(-1))
    return np.asarray(features, dtype=float)


def _interpolate(values, knots, times):
    values = np.asarray(values, dtype=float)
    knots = np.asarray(knots, dtype=float)
    times = np.asarray(times, dtype=float)
    if len(times) == 0:
        return np.empty((0,) + values.shape[1:], dtype=float)
    indices = np.searchsorted(knots, times, side="right")
    left = np.clip(indices - 1, 0, len(knots) - 1)
    right = np.clip(indices, 0, len(knots) - 1)
    width = knots[right] - knots[left]
    fraction = np.divide(
        times - knots[left], width,
        out=np.zeros_like(times), where=width > 0.0,
    )
    fraction = np.clip(fraction, 0.0, 1.0)
    shape = (len(times),) + (1,) * (values.ndim - 1)
    fraction = fraction.reshape(shape)
    return values[left] * (1.0 - fraction) + values[right] * fraction


def _network_predict(name, features):
    features = np.asarray(features, dtype=float)
    if name not in _MODEL_NAMES:
        return np.zeros((len(features), 0), dtype=float)
    x = (features - _MODEL[name + "__xmean"]) / _MODEL[name + "__xscale"]
    ymean = _MODEL[name + "__ymean"]
    yscale = _MODEL[name + "__yscale"]
    ensemble_size = int(_MODEL[name + "__ensemble"])
    layer_count = int(_MODEL[name + "__layers"])
    predictions = []
    for ensemble in range(ensemble_size):
        value = x
        for layer in range(layer_count):
            value = value @ _MODEL[f"{name}__w{ensemble}_{layer}"] + _MODEL[f"{name}__b{ensemble}_{layer}"]
            if layer + 1 < layer_count:
                value = np.tanh(value)
        predictions.append(value * yscale + ymean)
    return np.mean(predictions, axis=0)


def _tree_predict(name, features):
    features = np.asarray(features, dtype=float)
    if name not in _TREE_NAMES:
        return np.zeros((len(features), 0), dtype=float)
    ensemble_size = int(_MODEL[name + "__ensemble"])
    first_values = _MODEL[f"{name}__tree0__leaf_values"]
    output = np.zeros((len(features), first_values.shape[1]), dtype=float)
    for tree_index in range(ensemble_size):
        prefix = f"{name}__tree{tree_index}"
        left = _MODEL[prefix + "__left"]
        right = _MODEL[prefix + "__right"]
        split_feature = _MODEL[prefix + "__feature"]
        threshold = _MODEL[prefix + "__threshold"]
        nodes = np.zeros(len(features), dtype=np.int32)
        for _ in range(128):
            active = left[nodes] >= 0
            if not np.any(active):
                break
            rows = np.flatnonzero(active)
            active_nodes = nodes[rows]
            columns = split_feature[active_nodes]
            go_left = features[rows, columns] <= threshold[active_nodes]
            nodes[rows] = np.where(go_left, left[active_nodes], right[active_nodes])
        else:
            raise RuntimeError("tree traversal exceeded maximum depth")
        leaf_rows = _MODEL[prefix + "__leaf_index"][nodes]
        if np.any(leaf_rows < 0):
            raise RuntimeError("tree traversal did not reach a leaf")
        output += _MODEL[prefix + "__leaf_values"][leaf_rows]
    return output / ensemble_size


def _predict_p2_concentration(actions, times):
    times = np.asarray(times, dtype=float)
    concentration = np.zeros(len(times), dtype=float)
    for action in actions:
        if action["kind"] != "inject" or action["port"] != 2 or action["amp"] == 0.0:
            continue
        age = np.maximum(times - action["t"], 0.0)
        elapsed = np.minimum(age, action["dur"])
        after = np.maximum(age - action["dur"], 0.0)
        concentration += action["amp"] * (-np.expm1(-P2_K * elapsed)) / P2_K * np.exp(-P2_K * after)
    return concentration


def _p2_noise_scale(concentration, times):
    times = np.asarray(times, dtype=float)
    reference_age = np.maximum(times, 0.0)
    reference_elapsed = np.minimum(reference_age, 1.0)
    reference_after = np.maximum(reference_age - 1.0, 0.0)
    reference = (-np.expm1(-P2_K * reference_elapsed)) / P2_K * np.exp(-P2_K * reference_after)
    ratio = np.divide(concentration, reference, out=np.zeros_like(concentration), where=reference > 1e-8)
    return np.clip(np.sqrt(np.maximum(ratio, 0.0)), 0.0, 3.0)


def _has_adjustment_before(actions, time):
    for action in actions:
        if action["kind"] == "adjust" and action["t"] <= time + 1e-9:
            if np.any(np.abs(np.asarray(action["u"], dtype=float)) > 1e-12):
                return True
    return False


def _has_injection_before(actions, time):
    return any(
        action["kind"] == "inject"
        and action["amp"] != 0.0
        and time > action["t"] + 1e-9
        for action in actions
    )


def _injection_count_before(actions, times):
    times = np.asarray(times, dtype=float)
    injections = [
        action for action in actions
        if action["kind"] == "inject" and action["amp"] != 0.0
    ]
    return np.asarray([
        sum(time > action["t"] + 1e-9 for action in injections)
        for time in times
    ], dtype=int)


def _mean_for_sensor(actions, sensor, times, control_states, contexts):
    slots = SLOTS[sensor]
    if len(times) == 0:
        return np.empty((0, 4, slots), dtype=float)
    baseline = np.asarray(_BASE_SPLINES[sensor](times), dtype=float)
    mean = baseline.copy()
    injection_features = np.stack([
        _injection_summary(actions, time, contexts) for time in times
    ])

    if sensor in ("device0", "device1"):
        device = int(sensor[-1])
        control_features = np.column_stack([
            times / 50.0,
            control_states[:, device, :],
        ])
        has_local_control = np.any(np.abs(control_states[:, device, :]) > 1e-12, axis=1)
        for channel in range(4):
            name = f"adj_{sensor}_c{channel}"
            correction = _network_predict(name, control_features)
            if correction.shape[1] == slots:
                mean[:, channel, :] += correction * has_local_control[:, None]

    has_injection = np.asarray([_has_injection_before(actions, time) for time in times], dtype=bool)
    injection_counts = _injection_count_before(actions, times)
    single_injection_mask = injection_counts == 1
    multi_injection_mask = injection_counts >= 2
    for channel in range(4):
        for group, mask in (("single", single_injection_mask), ("multi", multi_injection_mask)):
            if not np.any(mask):
                continue
            correction = _network_predict(
                f"inj_{group}_{sensor}_c{channel}", injection_features
            )
            if correction.shape[1] == slots:
                mean[:, channel, :] += correction * mask[:, None]

    has_adjustment = np.asarray([_has_adjustment_before(actions, time) for time in times], dtype=bool)
    mix_mask = has_injection & has_adjustment
    tree_enabled = sensor in ("device0", "device1") and any(
        f"tree_mix_{sensor}_{group}" in _TREE_NAMES for group in ("single", "multi")
    )
    if np.any(mix_mask):
        joint = np.stack([
            _joint_features(actions, time, control_states[index], contexts)
            for index, time in enumerate(times)
        ])
        for group, count_mask in (("single", single_injection_mask), ("multi", multi_injection_mask)):
            group_mask = mix_mask & count_mask
            if not np.any(group_mask):
                continue
            tree_name = f"tree_mix_{sensor}_{group}"
            if tree_name in _TREE_NAMES:
                correction = _tree_predict(tree_name, joint[group_mask])
                if correction.shape[1] == 4 * slots:
                    mean[group_mask] += correction.reshape(-1, 4, slots)
            else:
                for channel in range(4):
                    correction = _network_predict(
                        f"mix_{group}_{sensor}_c{channel}", joint
                    )
                    if correction.shape[1] == slots:
                        mean[group_mask, channel, :] += correction[group_mask]

    if sensor in ("device0", "device1"):
        concentration = _predict_p2_concentration(actions, times)
        mean[:, 2, :] += concentration[:, None] * _MODEL["p2_profile_" + sensor][None, :]
        p2_mix_mask = mix_mask & (concentration > 1e-9)
        if np.any(p2_mix_mask) and not tree_enabled:
            p2_correction = _network_predict("p2mix_" + sensor, joint)
            if p2_correction.shape[1] == slots:
                mean[:, 2, :] += p2_correction * p2_mix_mask[:, None]
    return mean


def predict(actions, queries, n_samples=64, seed=0):
    n_samples = int(n_samples)
    rng = np.random.default_rng(seed)
    contexts = _event_contexts(actions)
    outputs = []
    baseline_noise_ids = rng.integers(0, 6, size=n_samples)
    p2_noise_ids = rng.integers(0, 4, size=n_samples)

    for query in queries:
        sensor = query["sensor"]
        times = np.asarray(query["t"], dtype=float)
        slots = SLOTS[sensor]
        control_states = _control_states(actions, times)
        mean = _mean_for_sensor(actions, sensor, times, control_states, contexts)
        concentration = _predict_p2_concentration(actions, times)
        noise_scale = _p2_noise_scale(concentration, times)
        baseline_noise_templates = _MODEL["noise_base_" + sensor]
        p2_noise_templates = _MODEL["noise_p2_" + sensor]
        sample_array = np.empty((n_samples, len(times), 4, slots), dtype=float)
        for sample_index in range(n_samples):
            baseline_noise = _interpolate(
                baseline_noise_templates[baseline_noise_ids[sample_index]],
                np.arange(51.0),
                times,
            )
            p2_noise = _interpolate(
                p2_noise_templates[p2_noise_ids[sample_index]],
                P2_NOISE_TIMES,
                times,
            )
            sample_array[sample_index] = (
                mean
                + baseline_noise
                + p2_noise * noise_scale[:, None, None]
            )
        outputs.append(sample_array)
    return {"samples": outputs}
