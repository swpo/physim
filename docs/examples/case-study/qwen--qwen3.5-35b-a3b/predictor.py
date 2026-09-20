import numpy as np

class LaboratoryPredictor:
    """
    Predicts laboratory experiment measurements based on learned patterns from experiments.
    
    Learned patterns:
    - Device 0 inject: Each port affects specific output slots
      * Port 0: affects Ch0 Slot0, modifies Ch1 first few slots  
      * Port 1: affects Ch0 Slot1, modifies Ch1 first few slots
      * Port 2: significantly elevates Channel 2 values (signature effect)
      * Port 3: affects Ch0 Slot3
    - Device 1 inject: Affects Channel 1 negatively at specific ports
    - Adjust action: Small modifications during [t, t+5) interval
    """
    
    def __init__(self):
        self.baselines = {
            'device0_t05': self._baseline_t05(),
            'device0_t20': self._baseline_t20(),
            'device0_t30': self._baseline_t30(),
            'device1_t20': self._baseline_device1(),
            'global': self._baseline_global()
        }
        
    def _baseline_t05(self):
        return [[0.297, 0.339, 0.073, 0.174, 0.338, 0.226, 0.529, 0.178, 0.053, 0.066, 0.370, 0.078, 0.218],
                [0.070, 0.451, -0.928, -0.732, 0.411, -0.436, 1.129, -0.693, -0.903, -0.929, 0.621, -0.951, -0.482],
                [0.000, 0.005, 0.004, 0.004, 0.006, 0.001, 0.013, 0.000, 0.000, 0.002, 0.018, 0.009, 0.014],
                [0.440, 0.606, -0.019, 0.162, 0.573, 0.337, 1.029, 0.186, -0.036, 0.005, 0.724, 0.045, 0.347]]
    
    def _baseline_t20(self):
        return [[0.310, 0.338, 0.074, 0.184, 0.341, 0.219, 0.523, 0.176, 0.053, 0.067, 0.372, 0.077, 0.218],
                [0.178, 0.448, -0.930, -0.689, 0.436, -0.485, 1.061, -0.665, -0.908, -0.928, 0.500, -0.952, -0.555],
                [0.000, 0.005, 0.004, 0.004, 0.006, 0.001, 0.012, 0.000, 0.000, 0.002, 0.018, 0.009, 0.014],
                [0.474, 0.606, -0.017, 0.182, 0.584, 0.320, 1.031, 0.202, -0.031, 0.004, 0.692, 0.033, 0.323]]
    
    def _baseline_t30(self):
        return [[0.247, 0.258, 0.048, 0.139, 0.265, 0.152, 0.433, 0.139, 0.038, 0.038, 0.261, 0.036, 0.139],
                [-0.037, 0.121, -0.922, -0.753, 0.145, -0.686, 0.919, -0.729, -0.902, -0.920, 0.097, -0.942, -0.745],
                [0.321, 0.326, 0.015, 0.108, 0.327, 0.105, 1.004, 0.104, 0.011, 0.013, 0.339, 0.020, 0.118],
                [0.475, 0.563, -0.016, 0.190, 0.555, 0.277, 0.994, 0.205, -0.024, 0.002, 0.609, 0.017, 0.272]]
    
    def _baseline_device1(self):
        ch0 = [0.005, 0.005, 0.008, 0.005, 0.093, 0.003, 0.002, 0.005, 0.004, 0.004, 0.006, 0.001, 
               0.000, 0.005, 0.004, 0.004, 0.006, 0.001, 0.000]
        ch1 = [-0.688, -0.779, -0.708, -0.718, -0.974, -0.703, -0.701, -0.817, 0.266, -0.902, 1.128, 
               -0.695, -0.908, -0.698, -0.723, -0.939, -0.717, -0.915, -0.832]
        ch2 = [0.006, 0.009, 0.001, 0.001, 0.009, 0.000, 0.006, 0.009, 0.001, 0.000, 0.009, 0.000,
               0.006, 0.009, 0.001, 0.000, 0.009, 0.000, 0.006]
        ch3 = [-0.008, -0.053, -0.017, -0.018, 0.031, -0.006, -0.008, -0.053, -0.017, -0.018, 0.034,
               -0.006, -0.008, -0.053, -0.017, -0.018, 0.033, -0.006, -0.006]
        return [ch0, ch1, ch2, ch3]
    
    def _baseline_global(self):
        return [[0.022, 0.006], [-0.681, 0.064], [0.001, 0.000], [0.022, 0.019]]
    
    def predict(self, actions, queries, n_samples=64, seed=0):
        """
        Predict measurement arrays given actions and queries.
        
        Args:
            actions: List of action dicts (inject or adjust)
            queries: List of query dicts with 'sensor' and 't' keys
            n_samples: Number of samples to generate
            seed: Random seed for reproducibility
            
        Returns:
            {"samples": [array_for_each_query]}
            Each array has shape (n_samples, n_times, 4, slots)
        """
        # Determine slots per query
        query_configs = []
        for q in queries:
            sensor = q['sensor']
            if sensor == 'device0':
                slots = 13
            elif sensor == 'device1':
                slots = 19
            else:  # global
                slots = 2
            query_configs.append((q['sensor'], slots))
        
        results = []
        
        for q_idx, (sensor, slots) in enumerate(query_configs):
            times = queries[q_idx]['t']
            n_times = len(times)
            
            rng = np.random.RandomState(seed + q_idx * 1000)
            pred = np.zeros((n_samples, n_times, 4, slots))
            
            # Pass 1: Set baseline values
            for si in range(n_samples):
                for ti in range(n_times):
                    t_val = times[ti]
                    ch_vals = self._get_baseline(sensor, t_val, slots)
                    
                    for ch in range(4):
                        for slot in range(slots):
                            val = ch_vals[ch][slot % len(ch_vals[ch])]
                            # Add noise
                            val += rng.randn() * (0.02 if sensor == 'device0' else 0.01)
                            pred[si, ti, ch, slot] = val
            
            # Pass 2: Apply action effects
            for action in actions:
                kind = action.get('kind', '')
                
                if kind == 'inject':
                    dev = action.get('device')
                    port = action.get('port')
                    amp = action.get('amp')
                    dur = action.get('dur')
                    inj_t = action.get('t')
                    
                    for ti in range(n_times):
                        t_val = times[ti]
                        
                        # Check if this time is within injection interval
                        if not (t_val >= inj_t and t_val < inj_t + dur):
                            continue
                        
                        if dev == 0:
                            if port == 0:
                                pred[:, ti, 0, 0] += amp * 0.06
                                pred[:, ti, 1, :5] -= amp * 0.3
                            elif port == 1:
                                pred[:, ti, 0, 1] += amp * 0.085
                                pred[:, ti, 1, :5] -= amp * 0.4
                            elif port == 2:
                                pred[:, ti, 2, :] += amp * 0.2  # Main signature: elevates Ch2
                                pred[:, ti, 0, 2] += amp * 0.01
                                pred[:, ti, 1, :5] -= amp * 0.2
                            elif port == 3:
                                pred[:, ti, 0, 3] += amp * 0.14
                                
                        elif dev == 1 and port is not None and port < slots:
                            pred[:, ti, 1, port] -= amp * 1.5
                            
                elif kind == 'adjust':
                    u = action.get('u', [0, 0, 0])
                    adj_t = action.get('t')
                    dev = action.get('device')
                    
                    # Adjust occupies [t, t+5)
                    for ti in range(n_times):
                        t_val = times[ti]
                        if adj_t <= t_val < adj_t + 5:
                            if dev == 0:
                                pred[:, ti, 0, 0] -= u[0] * 0.03
                                pred[:, ti, 1, 0] += u[0] * 0.15
            
            results.append(pred)
            
        return {"samples": results}
    
    def _get_baseline(self, sensor, t_val, slots):
        """Get baseline channel/slot values"""
        if sensor == 'device0':
            if abs(t_val - 0.5) < 0.1:
                return self.baselines['device0_t05']
            elif abs(t_val - 2.0) < 0.1:
                return self.baselines['device0_t20']
            elif abs(t_val - 3.0) < 0.1:
                return self.baselines['device0_t30']
            else:
                # Interpolate or use nearest
                if t_val > 3.0:
                    return self.baselines['device0_t30']
                return self.baselines['device0_t20']
        elif sensor == 'device1':
            return self.baselines['device1_t20']
        else:  # global
            return self.baselines['global']


def predict(actions, queries, n_samples=64, seed=0):
    """Module-level predict function matching the required API."""
    predictor = LaboratoryPredictor()
    return predictor.predict(actions, queries, n_samples, seed)
