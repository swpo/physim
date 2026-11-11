"""predict.py -- Parameter-inference predictor for the ring world.

Uses Kalman filtering at prior mean parameters to estimate hidden state from history,
then simulates futures with proper uncertainty quantification via state posterior sampling.
"""
import numpy as np

# --------------------------------------------------------------------------- globals
_W = None


def _get_world():
    """Lazy-load the world module."""
    global _W
    if _W is None:
        import physim2
        _W = physim2.load_world()
    return _W


def predict(history, program, queries, n_samples, seed):
    """Main prediction function.
    
    Args:
        history: (P+1, n_obs) = (17, 6) observations o(0)..o(P)
        program: {"prefix": (P, n_in), "test": (H, n_in)}
        queries: {level: [times after P]}
        n_samples: number of samples to return
        seed: random seed
    
    Returns:
        {level: (n_samples, len(times), d_level)}
    """
    W = _get_world()
    
    P = history.shape[0] - 1  # 16
    H = program["test"].shape[0]  # 32
    history_obs = history  # (P+1, 6)
    
    N = 24
    G = 6
    SIGMA = W.SIGMA
    
    # Observation matrix: block sums of 4 sites each
    C_mat = np.kron(np.eye(G), np.ones((1, N // G)))
    R_obs = SIGMA**2 * np.eye(G)
    
    # Use prior mean parameters
    D, gamma, c = W.PRIOR_MEAN
    
    # Build transition matrix A
    _I = np.eye(N)
    _LAP = 2 * _I - np.roll(_I, 1, 0) - np.roll(_I, -1, 0)
    _ADV = (np.roll(_I, 1, 0) - np.roll(_I, -1, 0)) / 2
    A = (1 - gamma) * (_I - D * _LAP + c * _ADV)
    
    rng = np.random.default_rng(seed)
    
    # Compute stationary covariance: P = A P A^T + Q
    Q = SIGMA**2 * np.eye(N)
    P_stat = np.eye(N) * 10.0
    for _ in range(100):
        P_new = A @ P_stat @ A.T + Q
        if np.max(np.abs(P_new - P_stat)) < 1e-10:
            break
        P_stat = P_new
    
    # Run Kalman filter on history to get filtered state at time P
    P_filt = P_stat.copy()
    mu_filt = np.zeros(N)
    
    for t in range(P + 1):
        mu_pred = A @ mu_filt
        P_pred = A @ P_filt @ A.T + Q
        
        y = history_obs[t]
        S = C_mat @ P_pred @ C_mat.T + R_obs
        
        try:
            S_inv = np.linalg.inv(S)
        except np.linalg.LinAlgError:
            S_inv = np.linalg.pinv(S)
        
        K = P_pred @ C_mat.T @ S_inv
        innovation = y - C_mat @ mu_filt
        mu_filt = mu_pred + K @ innovation
        P_filt = (np.eye(N) - K @ C_mat) @ P_pred
    
    # Blend filtered and stationary covariances for better uncertainty calibration
    alpha = 0.5
    P_blend = (1 - alpha) * P_filt + alpha * P_stat
    
    # Simulate forward from blended posterior
    all_futures = {l: [] for l in queries}
    
    for i in range(n_samples):
        # Sample x(P) from blended posterior
        x = mu_filt.copy()
        try:
            x += rng.multivariate_normal(np.zeros(N), P_blend)
        except np.linalg.LinAlgError:
            diag_vals = np.diag(P_blend)
            diag_vals = np.maximum(diag_vals, 0)
            x += rng.standard_normal(N) * np.sqrt(diag_vals)
        
        U_test = program["test"]
        
        future_data = {l: [] for l in queries}
        
        for h in range(H + 1):
            if h == 0:
                obs_now = C_mat @ x + SIGMA * rng.standard_normal(6)
            else:
                u = U_test[h - 1]
                x = A @ x + u + SIGMA * rng.standard_normal(24)
                obs_now = C_mat @ x + SIGMA * rng.standard_normal(6)
            
            for l in queries:
                times = queries[l]
                if h in times:
                    if l == 1:
                        future_data[l].append(obs_now.copy())
                    elif l == 2:
                        _L2 = np.stack([np.ones(6), np.cos(2*np.pi*np.arange(6)/6), np.sin(2*np.pi*np.arange(6)/6)])
                        future_data[l].append((obs_now @ _L2.T).copy())
        
        for l in queries:
            arr = np.array(future_data[l])
            all_futures[l].append(arr)
    
    out = {}
    for l in queries:
        out[l] = np.array(all_futures[l], dtype=np.float32)
    
    return out
