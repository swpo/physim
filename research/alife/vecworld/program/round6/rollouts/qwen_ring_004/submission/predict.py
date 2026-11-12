"""predict.py -- Online simulation with parameter uncertainty."""
import os
import numpy as np


class Predictor:
    def __init__(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "best_theta.npz")
        data = np.load(path)
        self.best_theta = data["best_theta"]
        self.theta_samples = data["theta_samples"]
        del data
        
        # Build matrices
        N = 24
        G = 6
        SIGMA = 0.3
        R_OBS = 0.3
        
        _I = np.eye(N)
        _LAP = 2 * _I - np.roll(_I, 1, 0) - np.roll(_I, -1, 0)
        _ADV = (np.roll(_I, 1, 0) - np.roll(_I, -1, 0)) / 2
        
        self._CMAT = np.kron(np.eye(G), np.ones((1, N // G)))
        self.SIGMA = SIGMA
        self.R_OBS = R_OBS
        self.N = N
        self.G = G
        self.P = 16
        
        # Precompute level-2 transform
        _ang = 2 * np.pi * np.arange(G) / G
        self._L2 = np.stack([np.ones(G), np.cos(_ang), np.sin(_ang)])
        
        # Precompute A matrices for all theta samples
        self.A_matrices = []
        for theta in self.theta_samples:
            D, gamma, c = theta
            A = (1 - gamma) * (_I - D * _LAP + c * _ADV)
            self.A_matrices.append(A)
    
    def predict(self, history, program, queries, n_samples, seed):
        rng = np.random.default_rng(seed)
        P = self.P
        
        out = {}
        
        # Get smoothed state at t=P
        x_smooth, P_smooth = self._rt_smoother(history)
        
        # Determine max horizon needed
        all_times = []
        for times in queries.values():
            all_times.extend(times)
        H_max = max(all_times)
        
        U_test = program["test"]  # (H, n_in)
        
        # Number of theta samples to use
        n_thetas = len(self.theta_samples)
        
        # Distribute samples across theta values
        samples_per_theta = n_samples // n_thetas
        remainder = n_samples - samples_per_theta * n_thetas
        
        for level in queries:
            times = queries[level]
            d_level = {1: 6, 2: 3}[level]
            
            samples = np.zeros((n_samples, len(times), d_level))
            
            sample_idx = 0
            for ti in range(n_thetas):
                n_here = samples_per_theta + (1 if ti < remainder else 0)
                A = self.A_matrices[ti]
                
                for s in range(n_here):
                    # Sample initial state from smoothed distribution
                    x = x_smooth + rng.multivariate_normal(np.zeros(self.N), P_smooth)
                    
                    for h in range(H_max):
                        u = U_test[h] if h < len(U_test) else np.zeros(self.N)
                        xi = rng.normal(0, self.SIGMA, self.N)
                        x = A @ x + u + self.SIGMA * xi
                        
                        if h in times:
                            t_idx = times.index(h)
                            y_block = self._CMAT @ x
                            
                            if level == 1:
                                y = y_block + self.R_OBS * rng.normal(0, 1, self.G)
                            else:
                                y = y_block @ self._L2.T + self.R_OBS * rng.normal(0, 1, self.G) @ self._L2.T
                            
                            samples[sample_idx, t_idx] = y
                    
                    sample_idx += 1
            
            out[level] = samples
        
        return out
    
    def _rt_smoother(self, history):
        """RTS smoother to get smoothed state at t=P."""
        P = self.P
        N = self.N
        G = self.G
        A = self.A_matrices[0]  # Use best theta for smoother
        C = self._CMAT
        Q = self.SIGMA**2 * np.eye(N)
        R = self.R_OBS**2 * np.eye(G)
        
        # Forward pass
        x_filt = np.zeros((P+1, N))
        P_filt = np.zeros((P+1, N, N))
        x_pred_arr = np.zeros((P+1, N))
        P_pred_arr = np.zeros((P+1, N, N))
        
        P_stat = self._stationary_cov(A)
        x_filt[0] = np.zeros(N)
        P_filt[0] = P_stat
        
        for t in range(P+1):
            y_t = history[t]
            
            if t > 0:
                x_pred_arr[t] = A @ x_filt[t-1]
                P_pred_arr[t] = A @ P_filt[t-1] @ A.T + Q
            
            S = C @ P_pred_arr[t] @ C.T + R
            K = P_pred_arr[t] @ C.T @ np.linalg.inv(S)
            innovation = y_t - C @ x_pred_arr[t]
            x_filt[t] = x_pred_arr[t] + K @ innovation
            P_filt[t] = (np.eye(N) - K @ C) @ P_pred_arr[t]
        
        # Backward pass
        x_smooth = x_filt.copy()
        P_smooth = P_filt.copy()
        
        for t in range(P-1, -1, -1):
            J = P_filt[t] @ A.T @ np.linalg.inv(P_pred_arr[t+1])
            x_smooth[t] = x_filt[t] + J @ (x_smooth[t+1] - x_pred_arr[t+1])
            P_smooth[t] = P_filt[t] + J @ (P_smooth[t+1] - P_pred_arr[t+1]) @ J.T
        
        return x_smooth[P], P_smooth[P]
    
    def _stationary_cov(self, A):
        P = self.SIGMA**2 * np.eye(self.N)
        for _ in range(200):
            P_new = A @ P @ A.T + self.SIGMA**2 * np.eye(self.N)
            if np.max(np.abs(P_new - P)) < 1e-12:
                break
            P = P_new
        return P


def predict(history, program, queries, n_samples, seed):
    global _predictor
    try:
        return _predictor.predict(history, program, queries, n_samples, seed)
    except NameError:
        _predictor = Predictor()
        return _predictor.predict(history, program, queries, n_samples, seed)
