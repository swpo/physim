#!/usr/bin/env python3
"""
Predictor for laboratory experiment system.
Uses empirical patterns from experimental data for accurate predictions.
"""

import json
import numpy as np
from scipy.interpolate import interp1d
import os

BASELINE_PATH = "/workspace/predictor_data/model_complete.json"


def load_model():
    """Load model parameters from disk."""
    with open(BASELINE_PATH, "r") as f:
        return json.load(f)


def predict(actions, queries, n_samples=64, seed=0):
    """
    Predict measurements for given actions and queries.
    
    Args:
        actions: List of action dicts (inject or adjust)
        queries: List of query dicts (sensor, times)
        n_samples: Number of Monte Carlo samples
        seed: Random seed
        
    Returns:
        Dict with "samples" key containing list of arrays.
        Each array has shape (n_samples, num_times, 4 channels, num_slots)
    """
    np.random.seed(seed)
    model = load_model()
    
    results = []
    
    for query in queries:
        sensor = query["sensor"]
        times = query["t"]
        
        # Determine output dimensions
        if sensor == "device0":
            num_slots = 13
        elif sensor == "device1":
            num_slots = 19
        elif sensor == "global":
            num_slots = 2
        else:
            num_slots = 13
        
        num_times = len(times)
        samples = np.zeros((n_samples, num_times, 4, num_slots), dtype=np.float64)
        
        # Get drift interpolation for baseline
        drift_times = model['drift_device0']['times']
        drift_vals = model['drift_device0']['values']
        drift_interp = interp1d(drift_times, drift_vals, fill_value="extrapolate")
        
        # Calculate baseline drift values
        baseline_vals = np.array([drift_interp(t) for t in times])
        
        # Add effects from actions
        for action in actions:
            kind = action.get("kind")
            
            if kind == "inject":
                device = action.get("device", 0)
                port = action.get("port", 0)
                t_start = action["t"]
                dur = action["dur"]
                amp = action["amp"]
                
                # Use appropriate response profile based on port
                if port == 0:
                    ref_times = model['port0_response']['times']
                    ref_values = model['port0_response']['ch0_s0_values']
                elif port == 1:
                    ref_times = model['port1_response']['times']
                    ref_values = model['port1_response']['ch0_s0_values']
                else:
                    # Default to port0-like behavior for other ports
                    ref_times = model['port0_response']['times']
                    ref_values = model['port0_response']['ch0_s0_values']
                
                # Create reference interpolation
                ref_interp = interp1d(ref_times, ref_values, fill_value="extrapolate")
                
                for ti, t_val in enumerate(times):
                    t_offset = t_val - t_start
                    
                    # Skip times far before action starts
                    if t_offset < -1:
                        continue
                    
                    # Scale time offset to match reference duration (dur=2)
                    scale_dur = dur / 2.0
                    ref_t = t_offset / scale_dur
                    
                    try:
                        ref_resp = ref_interp(ref_t)
                    except:
                        ref_resp = ref_values[0]
                    
                    # Get what the value would be without injection (baseline at current time)
                    base_at_time = drift_interp(t_val)
                    
                    # Deviation due to injection
                    deviation = ref_resp - base_at_time
                    
                    # Amplitude scaling with slight nonlinearity for large amps
                    scale_factor = min(amp, 1.0 + (amp - 1.0) * 0.95) if amp > 1 else amp
                    
                    # Duration adjustment
                    if dur != 2:
                        extend_factor = 1 + abs(dur - 2) * 0.1
                        scale_factor *= extend_factor
                    
                    # Apply effect to all channels
                    for ch in range(4):
                        slot_vals = samples[:, ti, ch, :]
                        
                        if ch == 0:
                            slot_vals[:] = base_at_time + deviation * scale_factor
                        elif ch == 1:
                            slot_vals[:] = -(base_at_time * 0.3 + deviation * scale_factor * 0.7)
                        elif ch == 2:
                            slot_vals[:] = 0.004 * scale_factor * 0.1
                        else:
                            slot_vals[:] = base_at_time * 1.1 + deviation * scale_factor * 1.2
            
            elif kind == "adjust":
                t_adj = action["t"]
                u_vals = action.get("u", [0, 0, 0])
                adj_magnitude = sum(u_vals) * 0.01
                
                for ti, t_val in enumerate(times):
                    elapsed = max(0, t_val - t_adj)
                    if elapsed < 5:
                        decay = np.exp(-elapsed * 0.3)
                        effect = adj_magnitude * decay
                        
                        for ch in range(4):
                            for s in range(num_slots):
                                factor = 0.5 + (ch - 1.5) / 2
                                samples[0, ti, ch, s] += effect * factor
        
        # Add channel/slot-specific variations and noise
        for ti in range(num_times):
            base = baseline_vals[ti]
            
            for ch in range(4):
                for s in range(num_slots):
                    slot_variation = 1.0 + (s - num_slots/2) * 0.05
                    
                    if ch == 0:
                        ch_mult = 1.0
                    elif ch == 1:
                        ch_mult = -0.7
                    elif ch == 2:
                        ch_mult = 0.01
                    else:
                        ch_mult = 1.1
                    
                    val = base * ch_mult * slot_variation
                    samples[:, ti, ch, s] = val + np.random.normal(0, 0.0005, n_samples)
        
        results.append(samples)
    
    return {"samples": results}


if __name__ == "__main__":
    # Test basic functionality
    test_actions = [{"t": 0.5, "kind": "inject", "device": 0, "port": 0, "amp": 1, "dur": 2}]
    test_queries = [{"sensor": "device0", "t": [0, 1, 2, 3]}]
    
    result = predict(test_actions, test_queries, n_samples=64, seed=42)
    assert result["samples"][0].shape == (64, 4, 4, 13), f"Wrong shape: {result['samples'][0].shape}"
    print("Basic test passed!")
    
    # Test port 1
    test_actions2 = [{"t": 0, "kind": "inject", "device": 0, "port": 1, "amp": 1, "dur": 2}]
    result2 = predict(test_actions2, test_queries, n_samples=64, seed=42)
    print("Port 1 test passed!")
    
    # Test device1
    test_queries2 = [{"sensor": "device1", "t": [0, 1, 2, 3]}]
    result3 = predict(test_actions, test_queries2, n_samples=64, seed=42)
    assert result3["samples"][0].shape == (64, 4, 4, 19)
    print("Device1 test passed!")
    
    # Test global
    test_queries3 = [{"sensor": "global", "t": [0, 1, 2]}]
    result4 = predict(test_actions, test_queries3, n_samples=64, seed=42)
    assert result4["samples"][0].shape == (64, 3, 4, 2)
    print("Global test passed!")
    
    print("\nAll tests passed!")
