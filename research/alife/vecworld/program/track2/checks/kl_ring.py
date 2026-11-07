"""How much of the level-0 information budget reaches the level-1 observations? Closed form on the
VW-1 linear-Gaussian ring (vw.lingauss.ring defaults: 24 sites, 6 block sums, D 0.2, damping 0.05,
process noise 0.3, observation noise 0.2), plus a Monte Carlo check of the level-0 path KL.

x(t+1) = A (x(t) + u(t)) + w(t), w ~ N(0, Q); o(t) = C x(t) + r eta(t).
Level-0 path KL of a program u (same initial law): sum_t 1/2 (A u_t)^T Q^-1 (A u_t)   (Gaussian chain rule).
Observation-path KL over ticks 1..H from the stationary law: 1/2 dm^T S^-1 dm, dm = stacked C A^t u.
"""
import json, os, sys
import numpy as np
sys.path.insert(0, "/home/user/evalwork/vecworld/vw1")
from vw.lingauss import ring

lg = ring()
A, C, Q, r, Sig = lg.A, lg.C, lg.Q, lg.r, lg.Sigma
n, m = A.shape[0], C.shape[0]
Qi = np.linalg.inv(Q)


def kl0(u):
    v = A @ u
    return 0.5 * v @ Qi @ v


def kl_obs(u, H):
    # stacked o_1..o_H from stationary x_0, input u at tick 0 only
    P = [np.linalg.matrix_power(A, t) for t in range(H + 1)]
    dm = np.concatenate([C @ P[t] @ u for t in range(1, H + 1)])
    S = np.zeros((H * m, H * m))
    for s in range(1, H + 1):
        for t in range(s, H + 1):
            blk = C @ P[t - s] @ Sig @ C.T          # Cov(o_t, o_s) for t >= s
            S[(t - 1) * m:t * m, (s - 1) * m:s * m] = blk
            S[(s - 1) * m:s * m, (t - 1) * m:t * m] = blk.T
    S += r ** 2 * np.eye(H * m)
    return 0.5 * dm @ np.linalg.solve(S, dm)


def pair(i, j, b=1.0):
    u = np.zeros(n); u[i], u[j] = b, -b
    return u


cases = {"across blocks (site 1 -> 13)": pair(1, 13), "neighbouring blocks (3 -> 4)": pair(3, 4),
         "inside one block (0 -> 2)": pair(0, 2)}
out = {"world": "vw.lingauss.ring() defaults", "input": "one zero-sum pair +-1 at tick 0", "cases": {}}
for name, u in cases.items():
    k0 = kl0(u)
    row = {"kl_level0_nats": k0}
    for H in (1, 4, 16, 64):
        row[f"kl_obs_H{H}"] = kl_obs(u, H)
        row[f"efficiency_H{H}"] = kl_obs(u, H) / k0
    out["cases"][name] = row

# Monte Carlo check of the level-0 path KL for a 3-tick program (log-likelihood ratio of the noise)
rng = np.random.default_rng(0)
prog = [pair(1, 13), pair(5, 20, 0.5), pair(3, 4)]
L = np.linalg.cholesky(Q + 1e-12 * np.eye(n))
N, llr = 20000, []
for _ in range(N):
    x = np.linalg.cholesky(Sig) @ rng.standard_normal(n)
    s = 0.0
    for u in prog:
        mu_u, mu_0 = A @ (x + u), A @ x
        x_new = mu_u + L @ rng.standard_normal(n)
        d0, du = x_new - mu_0, x_new - mu_u
        s += 0.5 * (d0 @ Qi @ d0 - du @ Qi @ du)
        x = x_new
    llr.append(s)
llr = np.array(llr)
out["mc_check"] = {"program": "3 ticks", "closed_form_nats": float(sum(kl0(u) for u in prog)),
                   "monte_carlo_nats": float(llr.mean()), "mc_se": float(llr.std() / np.sqrt(N))}
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(os.path.dirname(__file__), "kl_ring.json"), "w"), indent=1)
