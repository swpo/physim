"""Q2 difficulty check (closed form, numpy only, about a CPU-minute): how fast do four hidden level-0
parameters become known through each observed level of a linear-Gaussian ring, and what does that do
to the exam regret?

World (a variant of vw.lingauss.ring with a parameterised law; input enters after the map, where the
noise is, so its nats charge is public):
    x(t+1) = A(theta) x(t) + u(t) + w(t),  w ~ N(0, sigma^2 I),  24 sites on a ring
    A = (1 - gamma) (I - D Lap1 - D2 Lap2 + v Adv)
    level 1 = 6 block sums (4 sites each); level 2 = 2 sums of 3 adjacent blocks; port noise r
    hidden theta = (D, D2, gamma, v), independent Gaussian prior with the sds below.
At long wavelength D and D2 act only through D + 4 D2, so the difference is a 'sloppy' direction
for coarse observers by construction (the hopping-model example of Machta et al. 2013).

Quantities (all exact for Gaussian laws, derivatives by central differences):
  I_k   Fisher information of one T-tick passive episode observed at level k, in prior-sd units
  H_j   exam Hessian at level j: Fisher information of o(P+h) given o(1..P), summed over h in HS;
        to second order the expected log-score regret of predicting with theta + d is d^T H d / 2
  R(N)  = tr(H (I + N I_k)^-1) / 2, the regret after N episodes; R(0) is the prior headroom
  N_10  = episodes needed for R(N) = R(0) / 10
"""
import json, os
import numpy as np

n, nb, sig, r = 24, 6, 0.3, 0.2
TH0 = np.array([0.15, 0.0125, 0.05, 0.05])          # D, D2, gamma, v
PSD = np.array([0.03, 0.0075, 0.01, 0.02])          # prior sds
NAMES = ["D", "D2", "gamma", "v"]
T, P, HS = 16, 8, (1, 4, 16)
I_ = np.eye(n)
Lap1 = 2 * I_ - np.roll(I_, 1, 0) - np.roll(I_, -1, 0)
Lap2 = 2 * I_ - np.roll(I_, 2, 0) - np.roll(I_, -2, 0)
Adv = (np.roll(I_, 1, 0) - np.roll(I_, -1, 0)) / 2
C1 = np.kron(np.eye(nb), np.ones((1, n // nb)))
C2 = np.kron(np.eye(2), np.ones((1, 3))) @ C1
PHI = {0: I_, 1: C1, 2: C2}


def Amat(th):
    D, D2, g, v = th
    return (1 - g) * (I_ - D * Lap1 - D2 * Lap2 + v * Adv)


def stat_cov(A):
    S = sig ** 2 * np.eye(n)
    M = A.copy()
    for _ in range(60):                              # doubling: S = sum_k A^k Q A^kT
        S = S + M @ S @ M.T
        M = M @ M
    return (S + S.T) / 2


def cov_times(th, C, times, ema=None, W=96):
    """Covariance of the stacked observations at `times` (stationary start). ema = a applies the
    causal memory y(t) = a C x(t) + (1 - a) y(t-1) before the port noise (W past ticks kept)."""
    A = Amat(th)
    Sg = stat_cov(A)
    m = C.shape[0]
    if ema is None:
        ts = list(times)
    else:
        ts = list(range(min(times) - W, max(times) + 1))
    pw = {0: np.eye(n)}
    for d in range(1, max(ts) - min(ts) + 1):
        pw[d] = A @ pw[d - 1]
    S = np.zeros((len(ts) * m, len(ts) * m))
    for i, ti in enumerate(ts):
        for j, tj in enumerate(ts[: i + 1]):
            blk = C @ pw[ti - tj] @ Sg @ C.T
            S[i * m:(i + 1) * m, j * m:(j + 1) * m] = blk
            S[j * m:(j + 1) * m, i * m:(i + 1) * m] = blk.T
    if ema is not None:
        F = np.zeros((len(times) * m, len(ts) * m))
        for i, ti in enumerate(times):
            for j, tj in enumerate(ts):
                if tj <= ti:
                    F[i * m:(i + 1) * m, j * m:(j + 1) * m] = ema * (1 - ema) ** (ti - tj) * np.eye(m)
        S = F @ S @ F.T
    return S + r ** 2 * np.eye(S.shape[0])


def fim_cov(C, times, ema=None):
    """Gaussian Fisher information (zero mean) in prior-sd units."""
    S0 = cov_times(TH0, C, times, ema)
    Si = np.linalg.inv(S0)
    dS = []
    for i in range(4):
        e = np.zeros(4); e[i] = 1e-4 * PSD[i] / 0.01
        dS.append((cov_times(TH0 + e, C, times, ema) - cov_times(TH0 - e, C, times, ema)) / (2 * e[i]) * PSD[i])
    G = [Si @ d for d in dS]
    return np.array([[0.5 * np.sum(G[i] * G[j].T) for j in range(4)] for i in range(4)])


def fim_mean(C, times, u):
    """Extra Fisher information from the mean response to a pulse u at tick 0 (o(t) mean = C A^(t-1) u)."""
    def mean(th):
        A = Amat(th); v = u.copy(); out = []
        for t in range(1, max(times) + 1):
            if t in times:
                out.append(C @ v)
            v = A @ v
        return np.concatenate(out)
    J = np.stack([(mean(TH0 + PSD[i] * 1e-3 * np.eye(4)[i]) - mean(TH0 - PSD[i] * 1e-3 * np.eye(4)[i])) / 2e-3
                  for i in range(4)], 1)
    S0 = cov_times(TH0, C, times)
    return J.T @ np.linalg.solve(S0, J)


def exam_hessian(C, hs=HS):
    H = np.zeros((4, 4))
    past = list(range(1, P + 1))
    Ip = fim_cov(C, past)
    for h in hs:
        H += fim_cov(C, past + [P + h]) - Ip
    return H


def regret(H, Ik, N):
    return 0.5 * np.trace(H @ np.linalg.inv(np.eye(4) + N * Ik))


def n_frac(H, Ik, frac=0.1):
    R0 = regret(H, np.zeros((4, 4)), 0)
    lo, hi = 0.0, 1.0
    while regret(H, Ik, hi) > frac * R0 and hi < 1e12:
        hi *= 2
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if regret(H, Ik, mid) > frac * R0 else (lo, mid)
    return hi


def pred_order(C, ema=None, pmax=24, tol=0.01):
    """Smallest window p whose one-step predictive variance is within tol of the pmax-window one."""
    m = C.shape[0]
    S = cov_times(TH0, C, list(range(1, pmax + 2)), ema)
    def cvar(p):
        idx = np.arange((pmax - p) * m, pmax * m); tgt = np.arange(pmax * m, (pmax + 1) * m)
        Spp, Spt, Stt = S[np.ix_(idx, idx)], S[np.ix_(idx, tgt)], S[np.ix_(tgt, tgt)]
        return np.trace(Stt - Spt.T @ np.linalg.solve(Spp, Spt))
    full = cvar(pmax)
    marg = np.trace(S[-m:, -m:])
    for p in range(1, pmax + 1):
        if cvar(p) - full <= tol * (marg - full):
            return p, float((marg - full) / marg)
    return pmax, float((marg - full) / marg)


out = {"world": {"n": n, "blocks": nb, "sigma": sig, "r": r, "theta0": dict(zip(NAMES, TH0.tolist())),
                 "prior_sd": dict(zip(NAMES, PSD.tolist())), "episode_ticks": T, "history": P, "horizons": HS}}
ep = list(range(1, T + 1))
I, H = {}, {}
for k in (0, 1, 2):
    I[k] = fim_cov(PHI[k], ep)
    if k:
        H[k] = exam_hessian(PHI[k])
I["1m"] = fim_cov(C1, ep, ema=0.3)
H["1m"] = H[1]
levels = {}
for k in (0, 1, 2, "1m"):
    w, V = np.linalg.eigh(I[k])
    w = np.maximum(w, 1e-300)
    levels[str(k)] = {
        "numbers_per_tick": int(PHI[1 if k == "1m" else k].shape[0]),
        "fisher_eigs_per_episode_prior_units": w[::-1].tolist(),
        "episodes_to_halve_prior_variance_by_direction": (1 / w[::-1]).tolist(),
        "stiffest_direction": dict(zip(NAMES, V[:, -1].round(3).tolist())),
        "sloppiest_direction": dict(zip(NAMES, V[:, 0].round(3).tolist())),
        "log10_condition": float(np.log10(w[-1] / w[0])),
        "info_gain_one_episode_nats": float(0.5 * np.linalg.slogdet(np.eye(4) + I[k])[1]),
    }
out["observed_level"] = levels

reg = {}
for k, j in ((0, 1), (1, 1), (2, 2), (0, 2), (1, 2), ("1m", 1)):
    R0 = regret(H[j], np.zeros((4, 4)), 0)
    reg[f"observe_{k}_exam_{j}"] = {
        "prior_headroom_nats_per_item": float(R0),
        "episodes_for_10pct_regret": float(n_frac(H[j], I[k])),
        "asymptotic_constant_trHIinv_over_2": float(0.5 * np.trace(H[j] @ np.linalg.inv(I[k]))),
        "regret_after_1_2_8_64_episodes": [float(regret(H[j], I[k], N)) for N in (1, 2, 8, 64)],
    }
out["regret"] = reg

# what is the exam itself sensitive to? generalised eigenvalues of (H_j, I_k): exam weight per unit lab information
gen = {}
for k, j in ((1, 1), (2, 2)):
    w = np.sort(np.linalg.eigvals(np.linalg.solve(I[k], H[j])).real)[::-1]
    gen[f"observe_{k}_exam_{j}"] = w.tolist()
out["exam_weight_per_unit_lab_information"] = gen

# active versus passive: one aimed zero-sum pulse at tick 0, charged c = |u|^2 / (2 sigma^2) nats
act = {}
for label, (i, j) in {"across_blocks": (1, 13), "neighbouring_blocks": (3, 4), "inside_one_block": (0, 2)}.items():
    u = np.zeros(n); u[i], u[j] = 1.0, -1.0
    u *= np.sqrt(2 * sig ** 2 * 5.0 / (u @ u))          # 5 nats
    row = {}
    for k in (1, 2):
        Ia = fim_mean(PHI[k], ep, u)
        row[f"level{k}_trace_active_over_passive_at_5_nats"] = float(np.trace(Ia) / np.trace(I[k]))
        row[f"level{k}_nats_of_theta_information_passive"] = float(0.5 * np.linalg.slogdet(np.eye(4) + I[k])[1])
        row[f"level{k}_nats_of_theta_information_passive_plus_pulse"] = float(
            0.5 * np.linalg.slogdet(np.eye(4) + I[k] + Ia)[1])
        row[f"level{k}_same_at_50_nats"] = float(0.5 * np.linalg.slogdet(np.eye(4) + I[k] + 10 * Ia)[1])
    act[label] = row
out["input_pulse"] = act

out["predictive_order_h1_within_1pct"] = {
    "level1_memoryless": pred_order(C1), "level1_ema_0.3": pred_order(C1, ema=0.3), "level2": pred_order(C2)}

print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "q2_ring_difficulty.json"), "w"), indent=1)
