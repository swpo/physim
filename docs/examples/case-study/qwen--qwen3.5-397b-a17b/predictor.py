
import json
import numpy as np
from scipy.interpolate import interp1d
import os

# Training data is embedded in the predictor for portability
TRAINING_DATA = None

def get_training_data():
    global TRAINING_DATA
    if TRAINING_DATA is None:
        with open('/workspace/training_data.json', 'r') as f:
            TRAINING_DATA = json.load(f)
    return TRAINING_DATA

# Slot counts per sensor
SLOT_COUNTS = {
    'device0': 13,
    'device1': 19,
    'global': 2
}

def interpolate_baseline(baseline_data, sensor, times):
    """Interpolate baseline to given times."""
    base_times = np.array(baseline_data[sensor]['times'])
    base_data = np.array(baseline_data[sensor]['data'])  # (base_times, 4, slots)
    
    result = np.zeros((len(times), 4, base_data.shape[2]))
    for ch in range(4):
        for slot in range(base_data.shape[2]):
            f = interp1d(base_times, base_data[:, ch, slot], kind='linear',
                        bounds_error=False, fill_value='extrapolate')
            result[:, ch, slot] = f(times)
    return result

def find_nearest_inject(inject_list, device, port, amp, dur):
    """Find nearest inject experiment."""
    best_dist = float('inf')
    best_entry = None
    
    for entry in inject_list:
        if entry['device'] != device or entry['port'] != port:
            continue
        dist = (entry['amp'] - amp)**2 + (entry['dur'] - dur)**2
        if dist < best_dist:
            best_dist = dist
            best_entry = entry
    
    return best_entry

def interpolate_inject_response(entry, sensor, times):
    """Interpolate inject response to given times."""
    meas = entry['measurements'].get(sensor)
    if meas is None:
        slots = SLOT_COUNTS[sensor]
        return np.zeros((len(times), 4, slots))
    
    meas_times = np.array(meas['times'])
    meas_data = np.array(meas['data'])
    
    result = np.zeros((len(times), 4, meas_data.shape[2]))
    for ch in range(4):
        for slot in range(meas_data.shape[2]):
            f = interp1d(meas_times, meas_data[:, ch, slot], kind='linear',
                        bounds_error=False, fill_value='extrapolate')
            result[:, ch, slot] = f(times)
    return result

def predict(actions, queries, n_samples=64, seed=0):
    """Predict measurements for given actions and queries."""
    np.random.seed(seed)
    
    training_data = get_training_data()
    baseline_data = training_data['baseline']
    inject_list = training_data['inject']
    
    # Check for inject action
    inject_action = None
    for action in actions:
        if action['kind'] == 'inject':
            inject_action = action
            break
    
    samples = []
    for query in queries:
        sensor = query['sensor']
        times = np.array(query['t'])
        slots = SLOT_COUNTS[sensor]
        
        if inject_action is None:
            # No inject - use baseline
            base_pred = interpolate_baseline(baseline_data, sensor, times)
        else:
            # Has inject - find nearest and use its response
            entry = find_nearest_inject(
                inject_list,
                inject_action['device'],
                inject_action['port'],
                inject_action['amp'],
                inject_action['dur']
            )
            
            if entry is not None:
                base_pred = interpolate_inject_response(entry, sensor, times)
            else:
                base_pred = interpolate_baseline(baseline_data, sensor, times)
        
        # Generate n_samples with noise
        query_samples = np.zeros((n_samples, len(times), 4, slots))
        for s in range(n_samples):
            noise = np.random.randn(len(times), 4, slots) * 0.001
            query_samples[s] = base_pred + noise
        
        samples.append(query_samples)
    
    return {"samples": samples}
