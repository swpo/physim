
import numpy as np
import json
from scipy import interpolate
from pathlib import Path

# Pre-load all training data at module load
DATA_DIR = Path("/workspace/training_data_v2")

# Global caches
_baseline_cache = {}
_inject_cache = {}

def _load_data():
    """Load and cache all training data"""
    global _baseline_cache, _inject_cache
    
    # Load baseline
    baseline_file = DATA_DIR / "baseline.npz"
    if baseline_file.exists():
        with np.load(baseline_file, allow_pickle=False) as f:
            req = json.loads(f["request"].item())
            _baseline_cache["times"] = np.array(req["queries"][0]["t"])
            _baseline_cache["device0"] = f["query0"][0].copy()
            if "query1" in f:
                _baseline_cache["global"] = f["query1"][0].copy()
    
    # Load inject experiments
    for f_path in DATA_DIR.glob("inject_*.npz"):
        try:
            with np.load(f_path, allow_pickle=False) as f:
                req = json.loads(f["request"].item())
                actions = req["actions"]
                if actions and actions[0]["kind"] == "inject":
                    action = actions[0]
                    key = (action["device"], action["port"], action["amp"], action["dur"])
                    _inject_cache[key] = {
                        "times": np.array(req["queries"][0]["t"]),
                        "device0": f["query0"][0].copy(),
                        "global": f["query1"][0].copy() if "query1" in f else None
                    }
        except Exception:
            pass

# Load data now
_load_data()

def _interpolate_values(times_src, values, times_dst):
    """Interpolate values from src times to dst times"""
    if values is None:
        return None
    n_channels = values.shape[1]
    n_slots = values.shape[2]
    result = np.zeros((len(times_dst), n_channels, n_slots))
    for ch in range(n_channels):
        for slot in range(n_slots):
            f = interpolate.interp1d(times_src, values[:, ch, slot],
                                     kind='linear', fill_value='extrapolate',
                                     bounds_error=False)
            result[:, ch, slot] = f(times_dst)
    return result

def _predict_single(sensor, times, actions):
    """Predict for a single sensor"""
    times = np.array(times)
    
    # Determine output slots
    if sensor == "device0":
        n_slots = 13
        data_key = "device0"
    elif sensor == "device1":
        n_slots = 19
        data_key = "device1"
    else:  # global
        n_slots = 2
        data_key = "global"
    
    # Check for inject action
    inject_action = None
    for a in actions:
        if a["kind"] == "inject":
            inject_action = a
            break
    
    if inject_action is not None:
        # Use inject model
        key = (inject_action["device"], inject_action["port"], 
               inject_action["amp"], inject_action["dur"])
        
        # Find nearest neighbor
        best_key = None
        best_dist = float('inf')
        for k in _inject_cache:
            if k[0] == inject_action["device"] and k[1] == inject_action["port"]:
                dist = (k[2] - inject_action["amp"])**2 + (k[3] - inject_action["dur"])**2
                if dist < best_dist:
                    best_dist = dist
                    best_key = k
        
        if best_key is not None:
            data = _inject_cache[best_key]
            if data_key in data and data[data_key] is not None:
                return _interpolate_values(data["times"], data[data_key], times)
    
    # Fall back to baseline
    if _baseline_cache and data_key in _baseline_cache:
        return _interpolate_values(_baseline_cache["times"], _baseline_cache[data_key], times)
    
    # Return zeros if nothing available
    return np.zeros((len(times), 4, n_slots))

def predict(actions, queries, n_samples=64, seed=0):
    """Main prediction function"""
    np.random.seed(seed)
    
    samples = []
    for query in queries:
        sensor = query["sensor"]
        times = query["t"]
        
        # Determine output slots
        if sensor == "device0":
            n_slots = 13
        elif sensor == "device1":
            n_slots = 19
        else:
            n_slots = 2
        
        # Predict mean
        mean = _predict_single(sensor, times, actions)
        
        # Add small noise for uncertainty
        noise_std = 0.01
        noise = np.random.randn(n_samples, len(times), 4, n_slots) * noise_std
        sample = mean[np.newaxis, :, :, :] + noise
        
        # Ensure finite values
        sample = np.clip(sample, -10, 10)
        samples.append(sample)
    
    return {"samples": samples}
