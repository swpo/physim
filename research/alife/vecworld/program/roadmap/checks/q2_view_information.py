"""Q2 difficulty check: how much information about the 4 hidden gliders parameters does ONE
33-tick episode carry in each view? Re-uses the round-4 sbi design set (2,048 parameter draws x 4
simulated episodes x 22 phase-insensitive features; no new simulation).

Linear-Gaussian summary model per view: features f = a + J u + e, e ~ N(0, S), u = box coordinates in
[-1, 1]^4. J from least squares on the per-draw feature means, S = pooled within-draw covariance of
the 4 episodes. Fisher information per episode I = J^T S^-1 J, reported in prior-sd units
(uniform box: sd 1/sqrt 3). Also cross-validated R^2 of a linear read-out of u from one episode.
The study itself used a cubic emulator on 4 projections; this is the linear version, for ratios only."""
import json, os
import numpy as np
D = "/home/user/physim/research/alife/vecworld/program/round4/sbi/results/job/design_features.npz"
z = np.load(D, allow_pickle=True)
U, F, names = z["u"], z["F"].astype(float), [str(s) for s in z["features"]]
ok = np.isfinite(F).all((1, 2))
U, F = U[ok], F[ok]
VIEWS = {
    "all 22 (block + object views)": names,
    "block view only (memoryless)": ["mass_c0", "mass_c1", "log_m2_mean", "log_sd_c0", "log_sd_c1", "corr_c0c1",
                                     "log_sd_m2", "log_dC1", "log_dC4", "log_max_m2"],
    "object view only (tracker memory)": ["count_mean", "count_sd", "count_absdiff", "log_mass_body", "mass_cv",
                                          "frac_c1", "log_rg", "aniso", "speed_mean", "speed_sd",
                                          "log_tracked_mass", "log_density"],
    "level-2 population statistics": ["count_mean", "count_sd", "count_absdiff", "speed_mean", "log_tracked_mass"],
}
PRIOR_VAR = 1.0 / 3.0
out = {"source": D, "n_draws": int(len(U)), "episodes_per_draw": int(F.shape[1]), "param_names": ["lR", "dm_00", "ls_00", "lh"]}
for view, feats in VIEWS.items():
    idx = [names.index(f) for f in feats]
    f = F[:, :, idx]
    mu, sd = f.reshape(-1, len(idx)).mean(0), f.reshape(-1, len(idx)).std(0) + 1e-12
    f = (f - mu) / sd
    fbar = f.mean(1)
    X = np.c_[np.ones(len(U)), U]
    J = np.linalg.lstsq(X, fbar, rcond=None)[0][1:].T                     # (features, 4)
    res = f - fbar[:, None, :]
    S = np.einsum("nki,nkj->ij", res, res) / (len(U) * (F.shape[1] - 1)) + 1e-9 * np.eye(len(idx))
    I = J.T @ np.linalg.solve(S, J) * PRIOR_VAR                           # per episode, prior-sd units
    w = np.sort(np.linalg.eigvalsh(I))[::-1]
    # cross-validated linear read-out of u from a single episode (5 folds over draws)
    rng = np.random.default_rng(0)
    fold = rng.integers(0, 5, len(U))
    pred = np.zeros((len(U), F.shape[1], 4))
    for k in range(5):
        tr, te = fold != k, fold == k
        Xtr = np.c_[np.ones(tr.sum() * F.shape[1]), f[tr].reshape(-1, len(idx))]
        W = np.linalg.lstsq(Xtr, np.repeat(U[tr], F.shape[1], 0), rcond=None)[0]
        pred[te] = (np.c_[np.ones(te.sum() * F.shape[1]), f[te].reshape(-1, len(idx))] @ W).reshape(te.sum(), F.shape[1], 4)
    r2 = 1 - ((pred - U[:, None, :]) ** 2).mean((0, 1)) / U.var(0)
    post_sd_ratio = lambda N: np.sqrt(np.diag(np.linalg.inv(np.eye(4) + N * I)))
    out[view] = {
        "n_features": len(idx),
        "fisher_eigs_per_episode_prior_units": [round(float(x), 3) for x in w],
        "info_gain_nats_1_episode": round(float(0.5 * np.linalg.slogdet(np.eye(4) + I)[1]), 3),
        "info_gain_nats_2_episodes": round(float(0.5 * np.linalg.slogdet(np.eye(4) + 2 * I)[1]), 3),
        "predicted_posterior_sd_ratio_2_episodes": [round(float(x), 3) for x in post_sd_ratio(2)],
        "episodes_for_mean_sd_ratio_squared_0.125": None,
        "cv_r2_single_episode_linear_readout": [round(float(x), 3) for x in r2],
    }
    lo, hi = 0.0, 1.0
    g = lambda N: float(np.mean(post_sd_ratio(N) ** 2))
    while g(hi) > 0.125 and hi < 1e9:
        hi *= 2
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if g(mid) > 0.125 else (lo, mid)
    out[view]["episodes_for_mean_sd_ratio_squared_0.125"] = round(hi, 2)
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "q2_view_information.json"), "w"), indent=1)
