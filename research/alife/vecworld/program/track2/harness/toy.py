"""toy -- the closed-form exam world for harness v0: a vw.lingauss ring with three hidden parameters.

Level 0 (public architecture, hidden theta = (D, gamma, c)): a ring of N = 24 sites,
    x(t+1) = A_theta x(t) + u(t) + sigma xi(t),   xi ~ N(0, I),  sigma = 0.3 (public)
    A_theta = (1 - gamma) (I - D Lap + c (S_minus - S_plus) / 2)     diffusion, damping, advection
    x(0) ~ N(0, Sigma_theta), the stationary law (public as code; a function of theta).
The input u (all 24 sites, identity embedding) is a shift before the Gaussian noise, so the nats
charge 1/2 |u|^2 / sigma^2 is public and equals the level-0 path KL exactly (EXAM 3.1).
Level 1 (public Phi): the 6 block sums of 4 sites (vw.lingauss.ring's coarse-graining); observed
through ObservePort(noise r = 0.3) with identity maps (no permutations, EXAM section 2).
Level 2 (declared statistic of the observation): (total, mode-1 cosine, mode-1 sine) of the 6 values.
Prior: D ~ U(0.05, 0.25), gamma ~ U(0.02, 0.12), c ~ U(-0.3, 0.3); the true theta is drawn from it.

This module holds the family (vw types), closed forms (stationary law, Kalman filter and
likelihood, oracle and filter predictive moments), the program classes (a)-(d), the agent's data
collection under a budget, and the baselines B0 (climatology from own data), B1 (ARX fitted on own
level-1 data), B2 (SBI: synthetic likelihood + population Monte Carlo with the public simulator,
then Kalman filtering under posterior draws), B2x (the same with the exact likelihood), B3 (true
theta filter: the ceiling, exact here), and controls (prior-mean theta, ignore-actions).
"""
from __future__ import annotations

import math
import sys
import time

import numpy as np

sys.path.insert(0, "/home/user/evalwork/vecworld/vw1")
import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402

import vw  # noqa: E402
from vw.harness import Lab, ProgramMix, blind_random, no_input, program_dense  # noqa: E402
from vw.lingauss import stationary_cov  # noqa: E402
from vw.nats import NatsBudget  # noqa: E402
from vw.world import Carry  # noqa: E402

N, G, SIGMA, R_OBS = 24, 6, 0.3, 0.3
NAMES = ("D", "gamma", "c")
LO = np.array([0.05, 0.02, -0.3])
HI = np.array([0.25, 0.12, 0.3])
PRIOR_MEAN = (LO + HI) / 2
I_N = np.eye(N)
LAP = 2 * I_N - np.roll(I_N, 1, 0) - np.roll(I_N, -1, 0)
ADV = (np.roll(I_N, 1, 0) - np.roll(I_N, -1, 0)) / 2        # (ADV x)_i = (x_{i-1} - x_{i+1}) / 2
CMAT = np.kron(np.eye(G), np.ones((1, N // G)))              # (6, 24) block sums
_ang = 2 * np.pi * np.arange(G) / G
L2 = np.stack([np.ones(G), np.cos(_ang), np.sin(_ang)])     # (3, 6) level-2 statistic (linear)
QUERIES = {1: [1, 2, 4, 8, 16], 2: [16, 32]}
PREFIX = 16
H = 32
# exam programs and the agent's experiments obey the same caps (EXAM 3.5)
TICK_CAP, EPISODE_CAP = 2.0, 8.0


def theta_dict(th):
    return {k: jnp.asarray(float(v)) for k, v in zip(NAMES, th)}


def A_of(th) -> np.ndarray:
    D, g, c = (float(v) for v in th)
    return (1 - g) * (I_N - D * LAP + c * ADV)


def Sigma_of(th) -> np.ndarray:
    return stationary_cov(A_of(th), SIGMA ** 2 * I_N)


def stat2(obs):
    """Level-2 statistic of observed block values (..., 6) -> (..., 3)."""
    return np.asarray(obs) @ L2.T


# ----------------------------------------------------------------------------- vw types
def _A_jnp(p):
    return (1 - p["gamma"]) * (jnp.eye(N) - p["D"] * jnp.asarray(LAP) + p["c"] * jnp.asarray(ADV))


def _chol_stat_jnp(p):
    """Cholesky factor of the stationary covariance (circulant: Fourier eigenvalues)."""
    k = 2 * jnp.pi * jnp.arange(N) / N
    lam2 = (1 - p["gamma"]) ** 2 * ((1 - 2 * p["D"] * (1 - jnp.cos(k))) ** 2 + (p["c"] * jnp.sin(k)) ** 2)
    s = SIGMA ** 2 / (1 - lam2)
    d = jnp.arange(N)
    col = (s[None, :] * jnp.cos(k[None, :] * d[:, None])).sum(1) / N     # circulant first column
    idx = (jnp.arange(N)[:, None] - jnp.arange(N)[None, :]) % N
    S = col[idx]
    return jnp.linalg.cholesky((S + S.T) / 2)


def level() -> vw.Level:
    def init(p, key):
        return _chol_stat_jnp(p) @ jax.random.normal(key, (N,))

    def step_xi(p, x, xi, u):
        return _A_jnp(p) @ x + u + SIGMA * xi

    return vw.Level(init=init, step_xi=step_xi, noise_dim=N, input_dim=N, params=theta_dict(PRIOR_MEAN),
                    conserved={}, name="ring3")


def spec() -> vw.WorldSpec:
    C = jnp.asarray(CMAT)
    return vw.WorldSpec(base=level(), chain=(vw.CoarseGrain.of(lambda x: C @ x, name="blocks"),),
                        inport=vw.InputPort(admissible=vw.Admissible(lo=-3.0, hi=3.0), in_map=tuple(range(N))),
                        outport=vw.ObservePort(noise=R_OBS, out_map=tuple(range(G)), out_sign=(1.0,) * G),
                        replay="initial", name="ring3")


def world(th) -> vw.World:
    return vw.World(spec(), 0, params=theta_dict(th))


def nats_budget(total=None) -> NatsBudget:
    return NatsBudget.isotropic(N, SIGMA, tick=TICK_CAP, episode=EPISODE_CAP, total=total,
                                note="u is a shift before N(0, 0.3^2 I) process noise on every site")


def draw_theta(rng) -> np.ndarray:
    return LO + (HI - LO) * rng.random(3)


def public_scales(n=256, seed=0) -> dict:
    """Coordinate scales from the prior predictive (public): stationary SDs averaged over theta."""
    rng = np.random.default_rng([seed, 77])
    v1, v2 = [], []
    for _ in range(n):
        S = CMAT @ Sigma_of(draw_theta(rng)) @ CMAT.T + R_OBS ** 2 * np.eye(G)
        v1.append(np.diag(S).mean())
        v2.append(np.diag(L2 @ S @ L2.T))
    return {1: np.full(G, math.sqrt(np.mean(v1))), 2: np.sqrt(np.mean(v2, 0))}


# ----------------------------------------------------------------------------- program classes
def _block_push(block, sign, nats):
    """Uniform push on the 4 sites of a block costing `nats`."""
    a = math.sqrt(2 * nats * SIGMA ** 2 / 4) * (1 - 1e-9)
    return {int(j): float(sign * a) for j in range(4 * block, 4 * block + 4)}


def aimed(rng, history, H_, nats_left):
    """(c) Oppose the largest block anomaly of the last revealed frame, for as many ticks as the
    episode budget allows at the tick cap (open loop: a function of the history only)."""
    o = history[-1]
    dev = o - o.mean()
    b = int(np.argmax(np.abs(dev)))
    prog, left, t = [], nats_left, 0
    while left >= TICK_CAP - 1e-9 and t < H_:
        prog.append((t, _block_push(b, -np.sign(dev[b]) or 1.0, TICK_CAP)))
        left -= TICK_CAP
        t += 1
    return prog


def regional(rng, history, H_, nats_left):
    """(d) A random 2-block region pushed uniformly at the tick cap until the episode budget."""
    b0, sign = int(rng.integers(G)), float(rng.choice([-1.0, 1.0]))
    a = math.sqrt(2 * TICK_CAP * SIGMA ** 2 / 8) * (1 - 1e-9)
    sites = [(4 * b0 + j) % N for j in range(8)]
    prog, left, t = [], nats_left, 0
    while left >= TICK_CAP - 1e-9 and t < H_:
        prog.append((t, {s: sign * a for s in sites}))
        left -= TICK_CAP
        t += 1
    return prog


def program_mix() -> ProgramMix:
    return ProgramMix({"a": no_input, "b": blind_random(nats_budget(), k=2, rate=0.25), "c": aimed, "d": regional})


# ----------------------------------------------------------------------------- closed forms
def _batch_A(TH):
    return np.stack([A_of(t) for t in TH])


def kalman_history(TH, hist, pre_dense, A=None, S0=None):
    """Filter a history under each theta in TH (J, 3). hist (P+1, 6) observations, pre_dense (P, 24)
    prefix inputs. Returns filtered means (J, 24), covariances (J, 24, 24), log-likelihoods (J,)."""
    J = len(TH)
    A = _batch_A(TH) if A is None else A
    S = np.stack([Sigma_of(t) for t in TH]) if S0 is None else S0.copy()
    m = np.zeros((J, N))
    C, R = CMAT, R_OBS ** 2 * np.eye(G)
    ll = np.zeros(J)
    P = hist.shape[0] - 1
    for t in range(P + 1):
        if t > 0:
            m = np.einsum("jab,jb->ja", A, m) + pre_dense[t - 1][None]
            S = A @ S @ np.transpose(A, (0, 2, 1)) + SIGMA ** 2 * I_N
        Sy = C @ S @ C.T + R                                    # (J, 6, 6)
        e = hist[t][None] - m @ C.T                             # (J, 6)
        Ly = np.linalg.cholesky(Sy)
        z = np.linalg.solve(Ly, e[..., None])[..., 0]
        ll += -0.5 * (z ** 2).sum(1) - np.log(np.diagonal(Ly, axis1=1, axis2=2)).sum(1) - 0.5 * G * math.log(2 * math.pi)
        K = S @ C.T @ np.linalg.inv(Sy)                         # (J, 24, 6)
        m = m + np.einsum("jab,jb->ja", K, e)
        S = S - K @ C @ S
        S = (S + np.transpose(S, (0, 2, 1))) / 2
    return m, S, ll


def predictive_moments(th, m, S, test_dense, times):
    """Mean and covariance of o(P + q), q in times, given x_P ~ N(m, S) (one theta): lists."""
    A = A_of(th)
    out_m, out_S = [], []
    mu, Sx = m.copy(), S.copy()
    for s in range(max(times)):
        mu = A @ mu + test_dense[s]
        Sx = A @ Sx @ A.T + SIGMA ** 2 * I_N
        if s + 1 in times:
            out_m.append(CMAT @ mu)
            out_S.append(CMAT @ Sx @ CMAT.T + R_OBS ** 2 * np.eye(G))
    return out_m, out_S


def sample_forward(TH, w, m, S, test_dense, n_samples, rng, A=None):
    """Joint samples of the queried levels: choose theta_j by weight w, draw x_P ~ N(m_j, S_j),
    simulate the test program with fresh noise, observe with port noise."""
    J = len(TH)
    j = rng.choice(J, size=n_samples, p=w)
    A = (_batch_A(TH) if A is None else A)[j]                   # (n, 24, 24)
    L = np.linalg.cholesky(S[j] + 1e-12 * I_N)
    x = m[j] + np.einsum("nab,nb->na", L, rng.standard_normal((n_samples, N)))
    obs = np.zeros((n_samples, H + 1, G))
    obs[:, 0] = x @ CMAT.T
    for t in range(H):
        x = np.einsum("nab,nb->na", A, x) + test_dense[t][None] + SIGMA * rng.standard_normal((n_samples, N))
        obs[:, t + 1] = x @ CMAT.T
    obs = obs + R_OBS * rng.standard_normal(obs.shape)
    return {1: obs[:, QUERIES[1]], 2: stat2(obs[:, QUERIES[2]])}


def filter_predictor(TH, logw=None, reweight=True, ignore_actions=False):
    """B2 / B3 / controls: Kalman filtering of the item history under parameter draws TH, the
    draws reweighted by the history likelihood, then forward samples under the test program."""
    TH = np.atleast_2d(np.asarray(TH, float))
    lw0 = np.zeros(len(TH)) if logw is None else np.asarray(logw, float)
    Ab = _batch_A(TH)
    S0 = np.stack([Sigma_of(t) for t in TH])

    def predict(item, n_samples, seed):
        rng = np.random.default_rng([seed, item["id"] % (2 ** 32)])
        hist = item["history"]
        pre = program_dense(item["prefix_program"], hist.shape[0] - 1, N)
        test = np.zeros((H, N)) if ignore_actions else program_dense(item["program"], H, N)
        m, S, ll = kalman_history(TH, hist, pre, Ab, S0)
        lw = lw0 + (ll if reweight else 0.0)
        w = np.exp(lw - lw.max())
        return sample_forward(TH, w / w.sum(), m, S, test, n_samples, rng, Ab)
    return predict


# ----------------------------------------------------------------------------- agent data under a budget
def collect(lab: Lab, n_episodes: int, length: int, active: bool, seed: int):
    """The agent's investigation: episodes from fresh labels; active=True spends the per-episode
    nats on block pushes every 16 ticks (2 nats each, alternating sign, random block)."""
    rng = np.random.default_rng([seed, 5])
    eps = []
    for e in range(n_episodes):
        prog = []
        if active:
            left = EPISODE_CAP
            for t in range(0, length, 16):
                if left < TICK_CAP - 1e-9:
                    break
                prog.append((t, _block_push(int(rng.integers(G)), 1.0 if (t // 16) % 2 == 0 else -1.0, TICK_CAP)))
                left -= TICK_CAP
        o = lab.run(prog, list(range(length + 1)), label=int(rng.integers(2 ** 40)))
        eps.append((o, program_dense(prog, length, N)))
    return eps


# ----------------------------------------------------------------------------- B0, B1
def climatology_from_data(eps, rng_seed=0):
    """B0: windows of the agent's own episodes (prior-predictive draws if there are none)."""
    wins = []
    for o, _ in eps:
        for t0 in range(0, o.shape[0] - H):
            wins.append(o[t0:t0 + H + 1])
    if not wins:
        return None
    W = np.stack(wins)

    def predict(item, n_samples, seed):
        rng = np.random.default_rng([seed, item["id"] % (2 ** 32), rng_seed])
        ow = W[rng.integers(len(W), size=n_samples)]
        return {1: ow[:, QUERIES[1]], 2: stat2(ow[:, QUERIES[2]])}
    return predict


def prior_climatology(n_pool=256, seed=0):
    """B0 at zero budget: the prior-predictive stationary law (public simulator, theta ~ prior)."""
    rng = np.random.default_rng([seed, 31])
    TH = np.stack([draw_theta(rng) for _ in range(64)])
    m = np.zeros((64, N))
    S = np.stack([Sigma_of(t) for t in TH])

    def predict(item, n_samples, s2):
        r = np.random.default_rng([s2, item["id"] % (2 ** 32), 9])
        return sample_forward(TH, np.full(64, 1 / 64), m, S, np.zeros((H, N)), n_samples, r)
    return predict


def _arx_design(o, u, p, q, use_u):
    rows, ys = [], []
    for t in range(max(p, q) - 1, o.shape[0] - 1):
        f = [o[t - l] for l in range(p)]
        if use_u:
            f += [u[t - l] for l in range(q)]
        rows.append(np.concatenate(f + [np.ones(1)]))
        ys.append(o[t + 1])
    return np.array(rows), np.array(ys)


def fit_arx(eps, p_grid=(1, 2, 4, 6), lam_grid=(1e-2, 1e-1, 1.0, 10.0), q=4):
    """B1: ARX(p, q) on the agent's level-1 data, ridge; p and lambda by holdout 1-step error;
    Gaussian residuals. Inputs enter only if the data contain any."""
    use_u = any(np.abs(u).sum() > 0 for _, u in eps)
    split = [(o, u) for o, u in eps]
    if len(split) >= 4:
        tr, va = split[: -len(split) // 4], split[-len(split) // 4:]
    else:                                   # one long series: last quarter of time for validation
        tr, va = [], []
        for o, u in split:
            c = int(0.75 * o.shape[0])
            tr.append((o[:c], u[:c]))
            va.append((o[c - 8:], u[c - 8:]))
    best = None
    for p in p_grid:
        Xt = [_arx_design(o, u, p, q, use_u) for o, u in tr]
        Xv = [_arx_design(o, u, p, q, use_u) for o, u in va]
        Xt_, Yt_ = np.concatenate([a for a, _ in Xt]), np.concatenate([b for _, b in Xt])
        Xv_, Yv_ = np.concatenate([a for a, _ in Xv]), np.concatenate([b for _, b in Xv])
        if Xt_.shape[0] < 10:
            continue
        for lam in lam_grid:
            reg = lam * Xt_.shape[0] * np.eye(Xt_.shape[1])
            reg[-1, -1] = 0
            B = np.linalg.solve(Xt_.T @ Xt_ + reg, Xt_.T @ Yt_)
            err = ((Xv_ @ B - Yv_) ** 2).mean()
            if best is None or err < best[0]:
                best = (err, p, lam)
    _, p, lam = best
    D = [_arx_design(o, u, p, q, use_u) for o, u in eps]
    X, Y = np.concatenate([a for a, _ in D]), np.concatenate([b for _, b in D])
    reg = lam * X.shape[0] * np.eye(X.shape[1])
    reg[-1, -1] = 0
    B = np.linalg.solve(X.T @ X + reg, X.T @ Y)
    res = Y - X @ B
    Se = res.T @ res / max(X.shape[0] - X.shape[1], 1)
    Le = np.linalg.cholesky(Se + 1e-12 * np.eye(G))
    info = {"p": p, "lambda": lam, "use_inputs": use_u, "n_rows": int(X.shape[0])}

    def predict(item, n_samples, seed):
        rng = np.random.default_rng([seed, item["id"] % (2 ** 32), 3])
        hist = item["history"]
        P = hist.shape[0] - 1
        pre = program_dense(item["prefix_program"], P, N)
        test = program_dense(item["program"], H, N)
        uall = np.concatenate([pre, test], 0)                      # absolute time 0..P+H-1
        obuf = [np.tile(hist[P - l], (n_samples, 1)) for l in range(p)]   # obuf[l] = o(t - l)
        out = np.zeros((n_samples, H + 1, G))
        out[:, 0] = hist[P]
        for s in range(H):
            t = P + s
            f = list(obuf)
            if use_u:
                f += [np.tile(uall[t - l] if t - l >= 0 else np.zeros(N), (n_samples, 1)) for l in range(q)]
            Xf = np.concatenate(f + [np.ones((n_samples, 1))], 1)
            onew = Xf @ B + rng.standard_normal((n_samples, G)) @ Le.T
            obuf = [onew] + obuf[:-1]
            out[:, s + 1] = onew
        return {1: out[:, QUERIES[1]], 2: stat2(out[:, QUERIES[2]])}
    predict.info = info
    return predict


# ----------------------------------------------------------------------------- B2: SBI
_LAGS = (1, 2, 4, 8)


def summaries_np(O, U):
    """Summary statistics of datasets. O (..., E, L+1, 6), U (..., E, L, 24) -> (..., n_s).
    Block-Fourier autocovariances (log variance, normalised lags) and, when inputs are present,
    the regression of later modes on the pushed modes (the input response)."""
    F = np.fft.fft(O, axis=-1)[..., :4]                           # (..., E, T, 4)
    Fc = F - F.mean(-2, keepdims=True)
    g0 = (np.abs(Fc) ** 2).mean((-3, -2))                         # (..., 4)
    out = [np.log(g0)]
    T = O.shape[-2]
    for tau in _LAGS:
        g = (Fc[..., tau:, :] * np.conj(Fc[..., :T - tau, :])).mean((-3, -2)) / g0
        out.append(g.real)
        out.append(g.imag[..., 1:3])
    if U is not None and np.abs(U).sum() > 0:
        Ub = U.reshape(U.shape[:-1] + (G, N // G)).sum(-1)       # block pushes (E, L, 6), shared by all datasets
        Fu = np.fft.fft(Ub, axis=-1)[..., :4]
        den = (np.abs(Fu) ** 2).sum((-3, -2)) + 1e-12
        L = U.shape[-2]
        for tau in _LAGS:
            num = (F[..., tau:L + 1, :][..., :L - tau + 1, :] * np.conj(Fu[..., :L - tau + 1, :])).sum((-3, -2))
            b = num / den
            out.append(b.real)
            out.append(b.imag[..., 1:3])
    return np.concatenate(out, -1)


class Simulator:
    """The agent's copy of the public simulator: the vw World run at any theta with the agent's
    own keys (one jit, vmapped over theta)."""

    def __init__(self):
        self.w = world(PRIOR_MEAN)
        w = self.w

        def run(p, ki, kd, A):
            c = jax.vmap(w._init_member, in_axes=(None, 0, 0))(p, ki, kd)
            _, rec = w._rollout_fn(p, c, A, ("obs",))
            return rec["obs"]                                     # (T+1, B, 6)
        self._run = jax.jit(jax.vmap(run, in_axes=(0, 0, 0, None)))
        self.member_ticks = 0

    def datasets(self, TH, n_rep, U, seed):
        """Simulate n_rep datasets with the design U (E, L, 24) at each theta: obs (M, n_rep, E, L+1, 6)."""
        M = len(TH)
        E, L, _ = U.shape
        B = n_rep * E
        base = vw.make_key(9_000_001, seed)
        ki = jax.vmap(lambda m: vw.member_keys(jax.random.fold_in(base, 2 * m), B))(jnp.arange(M))
        kd = jax.vmap(lambda m: vw.member_keys(jax.random.fold_in(base, 2 * m + 1), B))(jnp.arange(M))
        A = jnp.asarray(np.tile(np.transpose(U, (1, 0, 2)), (1, n_rep, 1)))          # (L, n_rep*E, 24)
        P = {k: jnp.asarray(TH[:, i]) for i, k in enumerate(NAMES)}
        obs = np.asarray(self._run(P, ki, kd, A))                  # (M, L+1, B, 6)
        self.member_ticks += M * B * L
        return np.transpose(obs.reshape(M, L + 1, n_rep, E, G), (0, 2, 3, 1, 4))


def _in_box(TH):
    return np.all((TH >= LO) & (TH <= HI), axis=1)


def _propose(rng, M, mean, cov):
    out = []
    while len(out) < M:
        z = rng.multivariate_normal(mean, cov, size=4 * M)
        out.extend(z[_in_box(z)])
    return np.array(out[:M])


def pmc(loglik_fn, rng, M=256, rounds=3, inflate=2.0):
    """Population Monte Carlo over the prior box. loglik_fn(TH) -> (M,) log-likelihoods.
    Returns (particles, normalised log-weights, diagnostics)."""
    TH = LO + (HI - LO) * rng.random((M, 3))
    logq = np.zeros(M)                                            # uniform prior proposal (constant)
    diag = []
    for r in range(rounds):
        ll = loglik_fn(TH)
        lw = ll - logq
        lw -= lw.max()
        w = np.exp(lw)
        w /= w.sum()
        ess = 1.0 / (w ** 2).sum()
        mean = w @ TH
        cov = (TH - mean).T @ ((TH - mean) * w[:, None]) + 1e-10 * np.eye(3)
        diag.append({"round": r, "ess": float(ess), "mean": mean.tolist(), "sd": np.sqrt(np.diag(cov)).tolist()})
        if r == rounds - 1:
            return TH, np.log(w + 1e-300), diag
        if ess < 20:          # degenerate weights: take the spread of the 20 best particles instead
            cov = np.cov(TH[np.argsort(-w)[:20]].T)
        covp = inflate * cov + np.diag(((HI - LO) * 1e-3) ** 2)
        TH = _propose(rng, M, mean, covp)
        d = TH - mean
        Ci = np.linalg.inv(covp)
        logq = -0.5 * np.einsum("ma,ab,mb->m", d, Ci, d)          # truncation constant cancels


def synthetic_loglik(sim: Simulator, eps, n_rep=16, seed=0, chunk=16, sim_episodes=None):
    """Gaussian synthetic likelihood of the observed summaries, with the covariance pooled over
    the round's particles (within-theta), means per theta. sim_episodes: simulate only that many
    episodes per dataset and scale the summary covariance by sim_episodes / E (summaries are
    averages over independent episodes), which cuts the simulation cost by E / sim_episodes."""
    O = np.stack([o for o, _ in eps])
    U = np.stack([u for _, u in eps])
    s_obs = summaries_np(O, U)
    E = len(eps)
    Es = E if sim_episodes is None else min(int(sim_episodes), E)
    Us = U[:Es]
    if Es < E and np.abs(U).sum() > 0:
        # keep the input design's energy per episode representative: use episodes with inputs
        Us = U[np.argsort(-np.abs(U).sum((1, 2)))[:Es]]
    counter = [0]

    def ll(TH):
        S = []
        for i in range(0, len(TH), chunk):
            counter[0] += 1
            obs = sim.datasets(TH[i:i + chunk], n_rep, Us, seed=seed * 1000 + counter[0])
            S.append(summaries_np(obs, Us))
        S = np.concatenate(S)                                     # (M, n_rep, n_s)
        mu = S.mean(1)
        resid = (S - mu[:, None]).reshape(-1, S.shape[-1])
        Sig = resid.T @ resid / (resid.shape[0] - len(TH)) * (Es / E + 1 / n_rep)
        Lc = np.linalg.cholesky(Sig + 1e-10 * np.eye(Sig.shape[0]) * np.trace(Sig) / Sig.shape[0])
        z = np.linalg.solve(Lc, (s_obs[None] - mu).T)
        return -0.5 * (z ** 2).sum(0)
    return ll


def exact_loglik(eps):
    """Exact Kalman log-likelihood of the agent's episodes (stationary starts, known inputs);
    the covariance recursion is shared by all episodes."""
    O = np.stack([o for o, _ in eps])                             # (E, L+1, 6)
    U = np.stack([u for _, u in eps])                             # (E, L, 24)
    E, T1, _ = O.shape
    C, R = CMAT, R_OBS ** 2 * np.eye(G)

    def ll(TH):
        out = np.zeros(len(TH))
        for j, th in enumerate(TH):
            A, S = A_of(th), Sigma_of(th)
            m = np.zeros((E, N))
            tot = 0.0
            for t in range(T1):
                if t > 0:
                    m = m @ A.T + U[:, t - 1]
                    S = A @ S @ A.T + SIGMA ** 2 * I_N
                Sy = C @ S @ C.T + R
                Ly = np.linalg.cholesky(Sy)
                e = O[:, t] - m @ C.T
                z = np.linalg.solve(Ly, e.T)
                tot += -0.5 * (z ** 2).sum() - E * np.log(np.diag(Ly)).sum()
                K = S @ C.T @ np.linalg.inv(Sy)
                m = m + e @ K.T
                S = S - K @ C @ S
                S = (S + S.T) / 2
            out[j] = tot
        return out
    return ll


def posterior_draws(TH, logw, J, rng):
    w = np.exp(logw - logw.max())
    w /= w.sum()
    idx = rng.choice(len(TH), size=J, p=w)
    return TH[idx]


class Clock:
    def __init__(self):
        self.t0 = time.process_time()

    def __call__(self):
        return time.process_time() - self.t0
