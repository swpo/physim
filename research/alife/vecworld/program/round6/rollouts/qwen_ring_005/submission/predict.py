"""predict.py -- On-the-fly simulation predictor."""
import os
import numpy as np
from scipy.special import logsumexp
import physim2

def predict(history, program, queries, n_samples, seed):
    """
    history: (17, 6) observations o(0)..o(16)
    program: {"prefix": (16, 24), "test": (H, 24)}
    queries: {level: [times]}
    n_samples: 256
    seed: int
    
    Returns: {level: (n_samples, len(times), d_level)}
    """
    W = physim2.load_world()
    rng = np.random.default_rng(seed)
    
    sim = W.Simulator()
    
    # Step 1: Generate candidate thetas from prior
    n_candidates = 4096
    candidate_thetas = W.prior_sample(rng, n_candidates)
    
    # Step 2: Compute likelihood of history under each theta
    log_weights = np.zeros(n_candidates)
    
    for rep in range(2):
        seeds = rng.integers(0, 2**31, size=n_candidates) + rep * 50000
        sim_obs = sim.free_run(candidate_thetas, seed=int(seeds[0]), T=16)
        
        diff = sim_obs - history[np.newaxis, :, :]
        mse = np.mean(diff ** 2, axis=(1, 2))
        log_weights -= mse / 4.5
    
    # Normalize weights
    log_weights -= logsumexp(log_weights)
    weights = np.exp(log_weights)
    
    # Resample based on weights
    idx = rng.choice(n_candidates, size=n_samples, p=weights)
    selected_thetas = candidate_thetas[idx]
    
    # Step 3: Simulate futures at selected thetas with actual test program
    test_program = program["test"]
    H = test_program.shape[0]
    
    max_time = max(max(queries.get(l, [0])) for l in queries)
    
    out = {}
    
    for level in queries:
        times = queries[level]
        d_level = W.LEVEL_DIMS[level]
        level_samples = np.zeros((n_samples, len(times), d_level), dtype=np.float32)
        
        for i in range(n_samples):
            theta = selected_thetas[i]
            s = int(rng.integers(0, 2**31))
            
            # Use episodes method but with custom test program
            # The episodes method generates random programs, so we need to
            # simulate manually
            
            # Simulate P=16 ticks free run + H ticks with test program
            # Using the Simulator's internal methods correctly
            
            params = {k: np.array([[theta[j]]]) for j, k in enumerate(['D', 'gamma', 'c'])}
            
            # Run full episode: first P ticks no input, then remaining with test program
            # We'll do this in two steps using _start and _cont
            
            init_key = jax_random_key(s)
            cont_key = jax_random_key(s + 1)
            
            # Start with P=16 ticks of zero input
            state, obs_p = sim._start(params, init_key, cont_key, 
                                     np.zeros((1, 16, 24)))
            obs_p = np.asarray(obs_p)  # (1, 16, 6)
            
            # Continue with test program for max_time ticks
            test_input = test_program[:max_time][np.newaxis, :, :]  # (1, max_time, 24)
            state, obs_test = sim._cont(params, state, test_input)
            obs_test = np.asarray(obs_test)  # (1, max_time, 6)
            
            # Combine: obs_p has t=0..15, obs_test has t=0..max_time-1
            # Full observation at time P+t is obs_test[t]
            full_obs = np.concatenate([obs_p, obs_test], axis=1)  # (1, 16+max_time, 6)
            
            # Transform to requested level
            if level == 1:
                lev_obs = full_obs
            else:
                _L2 = np.array([np.ones(6), 
                               np.cos(2 * np.pi * np.arange(6) / 6), 
                               np.sin(2 * np.pi * np.arange(6) / 6)])
                lev_obs = (full_obs @ _L2.T)
            
            # Collect at queried times (relative to P, so offset by 16)
            for t_idx, t in enumerate(times):
                level_samples[i, t_idx, :] = lev_obs[0, 16 + t, :].astype(np.float32)
        
        out[level] = level_samples
    
    return out


def jax_random_key(seed):
    import jax
    return jax.random.key(int(seed) % (2**31))


if __name__ == "__main__":
    W = physim2.load_world()
    
    history = np.zeros((17, 6))
    program = {"prefix": np.zeros((16, 24)), "test": np.zeros((32, 24))}
    queries = {1: [1, 2, 4, 8, 16], 2: [16, 32]}
    
    result = predict(history, program, queries, 256, 42)
    for l in result:
        print(f"Level {l}: shape={result[l].shape}, dtype={result[l].dtype}")
