from pathlib import Path

import numpy as np
from scipy.fft import irfftn, rfftn
from scipy.interpolate import PchipInterpolator

from research import DEVICE_OFFSETS, device_pose


BACKGROUND = -0.7035395588874817
TIME_STEP = 0.02
GRID_SPACING = 0.5
MEMORY_DECAY = 0.0050055
NOISE_AMPLITUDE = 0.002 * np.sqrt(TIME_STEP)
_MODEL = None
_NOISE_MODEL = None


def _load_model(filename):
    with np.load(Path(__file__).with_name(filename), allow_pickle=False) as archive:
        model = {key: archive[key].copy() for key in archive.files}
    model['baseline_interpolator'] = PchipInterpolator(model['times'], model['baseline'], axis=0)
    model['global_interpolator'] = PchipInterpolator(model['times'], model['global_values'], axis=0)
    return model


def _model():
    global _MODEL
    if _MODEL is None:
        _MODEL = _load_model('model_data.npz')
    return _MODEL


def _noise_model():
    global _NOISE_MODEL
    if _NOISE_MODEL is None:
        _NOISE_MODEL = _load_model('noise_model.npz')
    return _NOISE_MODEL


def _baseline(time, model=None):
    if model is None:
        model = _model()
    return model['baseline_interpolator'](time), model['global_interpolator'](time)


def _activation(state):
    parameters = _model()['activation']
    activity = np.maximum(state[1] - parameters[2], 0)
    return parameters[0] * np.tanh(parameters[1] * activity)


def _sample_field(field, coordinates, origin=None, periodic=False):
    size = field.shape[-1]
    background_fill = origin is None
    if origin is None:
        origin = (size // 2) * GRID_SPACING
    coordinates = (np.asarray(coordinates) + origin) / GRID_SPACING
    lower = np.floor(coordinates).astype(int)
    fractions = coordinates - lower
    first_indices = lower[:, 0]
    second_indices = lower[:, 1]
    output = np.zeros((*field.shape[:-2], len(coordinates)))
    for shift_first in (0, 1):
        for shift_second in (0, 1):
            first_weights = fractions[:, 0] if shift_first else 1 - fractions[:, 0]
            second_weights = fractions[:, 1] if shift_second else 1 - fractions[:, 1]
            first = first_indices + shift_first
            second = second_indices + shift_second
            valid = (first >= 0) & (first < size) & (second >= 0) & (second < size)
            output[..., valid] += field[..., first[valid], second[valid]] * (first_weights * second_weights)[valid]
            if background_fill:
                output[1, ~valid] += BACKGROUND * (first_weights * second_weights)[~valid]
    return output


def _simulation_baseline(time, grid_size, model=None):
    baseline, global_values = _baseline(time, model)
    source_origin = baseline.shape[-1] // 2
    target_origin = grid_size // 2
    if grid_size <= baseline.shape[-1]:
        beginning = source_origin - target_origin
        return baseline[:, beginning:beginning + grid_size, beginning:beginning + grid_size], global_values
    embedded = np.zeros((4, grid_size, grid_size))
    embedded[1] = BACKGROUND
    beginning = target_origin - source_origin
    embedded[:, beginning:beginning + baseline.shape[-1], beginning:beginning + baseline.shape[-1]] = baseline
    return embedded, global_values


def _simulate(actions, measurement_steps, parameters=None, grid_size=256, n_paths=1, seed=0, stochastic=False, model=None, reference_path=False, include_gradients=False):
    if model is None:
        model = _model()
    if parameters is None:
        parameters = model['parameters']
    activator_diffusion, linear, cubic, fast_feedback, slow_feedback, adaptation, fast_diffusion, fast_rate, slow_diffusion, slow_rate, adaptation_rate = parameters
    frequencies = 2 * np.pi * np.fft.fftfreq(grid_size, d=GRID_SPACING)
    half_frequencies = 2 * np.pi * np.fft.rfftfreq(grid_size, d=GRID_SPACING)
    squared_frequencies = frequencies[:, None]**2 + half_frequencies[None, :]**2
    diffusing_channels = [0, 1, 3]
    diffusion = np.exp(-TIME_STEP * np.array([fast_diffusion, activator_diffusion, slow_diffusion])[:, None, None, None] * squared_frequencies)
    grid_axis = (np.arange(grid_size) - grid_size // 2) * GRID_SPACING
    first_grid, second_grid = np.meshgrid(grid_axis, grid_axis, indexing='ij')
    centers = np.zeros((2, 2))
    scales = np.ones(2)
    simulated_paths = n_paths + int(reference_path)
    perturbation = np.zeros((4, simulated_paths, grid_size, grid_size))
    area_fraction = (grid_size * GRID_SPACING / 128)**2
    generator = np.random.default_rng(int(seed) % (1 << 64))
    scheduled = {}
    for action in actions:
        scheduled.setdefault(round(action['t'] / TIME_STEP), []).append(action)
    active = []
    has_perturbation = stochastic
    actual_memory = None
    reference_memory = None
    records = {}
    if not measurement_steps:
        return records
    maximum_step = max(measurement_steps)
    requested = set(measurement_steps)
    for step in range(maximum_step + 1):
        time = TIME_STEP * step
        for action in scheduled.get(step, []):
            device = action['device']
            if action['kind'] == 'adjust':
                controls = np.array(action['u'], dtype=float)
                centers[device] += controls[:2]
                scales[device] = np.clip(scales[device] * np.exp(controls[2]), 0.5, 3)
            else:
                first_distance = first_grid - centers[device, 0]
                second_distance = second_grid - centers[device, 1]
                profile = action['amp'] * np.exp(-(first_distance**2 + second_distance**2) / 8)
                ending = step + round(action['dur'] / TIME_STEP)
                active.append((ending, action['port'], profile))
                has_perturbation = has_perturbation or action['amp'] > 0
        if step in requested:
            baseline, baseline_global = _baseline(time, model)
            local_baseline = _simulation_baseline(time, grid_size, model)[0]
            measured = [
                np.swapaxes(
                    _sample_field(baseline, centers[device] + scales[device] * DEVICE_OFFSETS[device])[:, None]
                    + _sample_field(perturbation, centers[device] + scales[device] * DEVICE_OFFSETS[device], origin=grid_size * GRID_SPACING / 2),
                    0, 1,
                )
                for device in range(2)
            ]
            mean_change = area_fraction * perturbation.mean(axis=(-2, -1))
            variance_change = area_fraction * (2 * local_baseline[:, None] * perturbation + perturbation**2).mean(axis=(-2, -1)) - 2 * baseline_global[:, 0, None] * mean_change - mean_change**2
            global_values = np.repeat(baseline_global[:, None], simulated_paths, axis=1)
            global_values[:, :, 0] += mean_change
            global_values[:, :, 1] = np.maximum(global_values[:, :, 1] + variance_change, 0)
            measured.append(np.swapaxes(global_values, 0, 1))
            if include_gradients:
                gradients = []
                for device in range(2):
                    coordinates = centers[device] + scales[device] * DEVICE_OFFSETS[device]
                    directional = []
                    for axis in range(2):
                        shift = np.zeros(2)
                        shift[axis] = .1
                        differences = []
                        for sign in (-1, 1):
                            shifted = coordinates + sign * shift
                            values = _sample_field(baseline, shifted)[:, None] + _sample_field(perturbation, shifted, origin=grid_size * GRID_SPACING / 2)
                            differences.append(np.swapaxes(values, 0, 1))
                        directional.append((differences[1] - differences[0]) / .2)
                    gradients.append(np.array(directional))
                measured.append(gradients)
            records[step] = measured
        if step == maximum_step:
            break
        if not has_perturbation:
            continue
        baseline = _simulation_baseline(time, grid_size, model)[0][:, None]
        if actual_memory is None:
            reference_memory = np.array(baseline[2, 0], dtype=np.float32, copy=True)
            actual_memory = np.repeat(reference_memory[None], simulated_paths, axis=0)
        active = [entry for entry in active if entry[0] > step]
        for ending, port, profile in active:
            if port == 2:
                actual_memory += np.asarray(TIME_STEP * profile, dtype=np.float32)
                perturbation[2] = actual_memory - reference_memory
            else:
                perturbation[port] += TIME_STEP * profile
        full_state = baseline + perturbation
        reaction = perturbation.copy()
        reaction[0] += TIME_STEP * fast_rate * (perturbation[1] - perturbation[0])
        reaction[3] += TIME_STEP * slow_rate * (perturbation[1] - perturbation[3])
        actual_memory += np.asarray(TIME_STEP * (adaptation_rate * _activation(full_state) - MEMORY_DECAY * actual_memory), dtype=np.float32)
        reference_memory += np.asarray(TIME_STEP * (adaptation_rate * _activation(baseline)[0] - MEMORY_DECAY * reference_memory), dtype=np.float32)
        reaction[2] = actual_memory - reference_memory
        adaptation_change = full_state[2] * full_state[0] - baseline[2] * baseline[0]
        reaction[1] += TIME_STEP * (
            linear * perturbation[1]
            + cubic * perturbation[1] * (3 * baseline[1]**2 + perturbation[1] * (3 * baseline[1] + perturbation[1]))
            + fast_feedback * perturbation[0]
            + slow_feedback * perturbation[3]
            - adaptation * adaptation_change
        )
        if stochastic:
            pairs = (n_paths + 1) // 2
            noise = generator.standard_normal((pairs, grid_size, grid_size)) * NOISE_AMPLITUDE
            paired_noise = np.stack([noise, -noise], axis=1).reshape(2 * pairs, grid_size, grid_size)
            reaction[1, :n_paths] += paired_noise[:n_paths]
        workers = 4 if n_paths > 1 else 1
        perturbation[diffusing_channels] = irfftn(rfftn(reaction[diffusing_channels], axes=(-2, -1), workers=workers) * diffusion, s=(grid_size, grid_size), axes=(-2, -1), workers=workers)
        perturbation[2] = reaction[2]
    return records


def predict(actions, queries, n_samples=64, seed=0):
    measurement_steps = {round(time / TIME_STEP) for query in queries for time in query['t']}
    if not measurement_steps:
        return {'samples': [np.empty((n_samples, 0, 4, {'device0': 13, 'device1': 19, 'global': 2}[query['sensor']])) for query in queries]}
    n_paths = 1 if n_samples <= 1 else min(32, 2 * ((n_samples + 1) // 2))
    records = _simulate(actions, measurement_steps, include_gradients=n_samples > 1)
    uncertainty = None
    coefficients = None
    frequencies = None
    phases = None
    if n_samples > 1:
        uncertainty = _simulate(actions, measurement_steps, n_paths=n_paths, seed=seed, stochastic=True, model=_noise_model(), reference_path=True)
        spatial_generator = np.random.default_rng(271828)
        frequencies = spatial_generator.standard_normal((64, 2)) / 6
        phases = spatial_generator.uniform(0, 2 * np.pi, 64)
        generator = np.random.default_rng((int(seed) ^ 0xB41D8A53) % (1 << 64))
        paired = generator.standard_normal(((n_paths + 1) // 2, 2, 64))
        coefficients = np.stack([paired, -paired], axis=1).reshape(-1, 2, 64)[:n_paths]
    sample_indices = np.arange(n_samples) % n_paths
    samples = []
    for query in queries:
        sensor_index = {'device0': 0, 'device1': 1, 'global': 2}[query['sensor']]
        slots = [13, 19, 2][sensor_index]
        trajectories = np.empty((n_paths, len(query['t']), 4, slots))
        for time_index, time in enumerate(query['t']):
            step = round(time / TIME_STEP)
            trajectories[:, time_index] = records[step][sensor_index][0]
            if uncertainty is not None:
                noisy_values = uncertainty[step][sensor_index]
                trajectories[:, time_index] += noisy_values[:n_paths] - noisy_values[n_paths]
                if sensor_index < 2:
                    center, scale = device_pose(actions, sensor_index, time)
                    coordinates = center + scale * DEVICE_OFFSETS[sensor_index]
                    features = np.cos(coordinates @ frequencies.T + phases)
                    features /= np.maximum(np.linalg.norm(features, axis=1, keepdims=True), 1e-12)
                    displacements = .00025 * time * (coefficients @ features.T)
                    weight = np.clip((np.linalg.norm(coordinates, axis=1) - 27) / 5, 0, 1)
                    weight = weight**2 * (3 - 2 * weight)
                    gradients = records[step][3][sensor_index][:, 0]
                    trajectories[:, time_index] += weight * (displacements[:, :, None] * gradients[None]).sum(axis=1)
        samples.append(trajectories[sample_indices])
    return {'samples': samples}
