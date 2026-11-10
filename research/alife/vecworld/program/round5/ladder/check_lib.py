"""check_lib -- CPU checks of ladder_lib / ladder_net pieces that do not need a long simulation.

  1. params_batch(names, thetas) equals gworld.stack_params(theta_to_params) for the three hidden sets.
  2. pop5(obs)[..., :3] equals gworld.population(obs); public_scales shapes.
  3. Emulator + posterior on a synthetic d-parameter problem (linear Gaussian summaries): the posterior mean
     moves to the truth and the sd shrinks with n, for d = 1, 4, 8.
  4. The three view nets: one lockstep training step runs, samples have the exam's shapes and are finite;
     the three data-only ridges fit and sample.
  5. ViewCells.score equals vw.scoring.energy_fair applied by hand; acceptance.shares reproduces sigma, rho
     from pooled means.
usage: python -B check_lib.py  -> results/check_lib.json
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ladder_lib as LL  # noqa: E402
import ladder_net as NN  # noqa: E402

import jax  # noqa: E402
import numpy as np  # noqa: E402

from vw.scoring import energy_fair  # noqa: E402

GW, SL = LL.GW, LL.SL
out = {}
rng = np.random.default_rng(0)

# 1 parameters
worst = 0.0
for n in (1, 4, 8):
    names, lo, hi = LL.box(n)
    th = lo + (hi - lo) * rng.random((5, n))
    a = LL.params_batch(names, th)
    b = GW.stack_params([GW.theta_to_params(dict(zip(names, map(float, t)))) for t in th])
    assert set(a) == set(b)
    worst = max(worst, max(float(np.abs(np.asarray(a[k]) - np.asarray(b[k])).max()) for k in a))
out["params_batch_max_abs_diff"] = worst
assert worst == 0.0, worst

# 2 views on a synthetic observation table
E, T1 = 6, 13
obs = np.zeros((E, T1, LL.N_OBS))
obs[..., :LL.NC] = rng.random((E, T1, LL.NC))
O = np.zeros((E, T1, LL.K, LL.NF))
pres = rng.random((E, T1, LL.K)) < 0.6
ang = rng.uniform(0, 2 * np.pi, (E, T1, LL.K, 2))
O[..., 0] = pres
O[..., 1] = pres * rng.uniform(80, 250, pres.shape)
O[..., 2] = pres * rng.random(pres.shape)
O[..., 3], O[..., 4] = pres * np.cos(ang[..., 0]), pres * np.sin(ang[..., 0])
O[..., 5], O[..., 6] = pres * np.cos(ang[..., 1]), pres * np.sin(ang[..., 1])
O[..., 7] = pres * rng.uniform(3, 8, pres.shape)
O[..., 8:10] = pres[..., None] * rng.normal(0, 0.2, pres.shape + (2,))
O[..., 10:12] = pres[..., None] * rng.normal(0, 1.0, pres.shape + (2,))
obs[..., LL.NC:] = O.reshape(E, T1, -1)
d = float(np.abs(LL.pop5(obs)[..., :3] - GW.population(obs)).max())
out["pop5_first3_vs_gworld_population"] = d
assert d < 1e-9
SC = LL.public_scales(obs)
assert SC["SCO"].shape == (144,) and SC["SCP"].shape == (5,) and SC["POPM"].shape == (5,)
U = np.zeros((E, T1 - 1, LL.NW))
U[:, 4:8] = rng.normal(0, 0.1, (E, 4, LL.NW)) * (rng.random((E, 4, LL.NW)) < 0.1)
for v in LL.VIEWS:
    F = LL.view_features(v, obs, U, 4)
    assert F.shape == (E, len(LL.FEATS[v])) and np.isfinite(F).all(), v
F0 = LL.view_features("object", obs, np.zeros_like(U), 4)
assert np.all(F0[:, LL.FEATS["object"].index("resp_v")] == 0.0)

# 3 emulator and posterior
class FlatPrior:
    def logp(self, u):
        return np.zeros(len(np.atleast_2d(u)))


out["sbi_synthetic"] = {}
for dpar in (1, 4, 8):
    N, Kk = 400, 4
    Ud = rng.uniform(-1, 1, (N, dpar))
    A = rng.normal(0, 1, (dpar, dpar)) + 2 * np.eye(dpar)
    S = (Ud @ A)[:, None, :] + 0.05 * (Ud ** 2).sum(1)[:, None, None] + rng.normal(0, 1.0, (N, Kk, dpar))
    em = LL.Emulator().fit(Ud, S, rng=np.random.default_rng(1))
    ut = rng.uniform(-0.6, 0.6, dpar)
    row = {"deg_mean": em.diag["deg_mean"], "cv_chi2": em.diag["cv_chi2_mean_with_misfit"]}
    for nn in (2, 32, 512):
        sbar = ut @ A + 0.05 * (ut ** 2).sum() + rng.normal(0, 1.0 / np.sqrt(nn), dpar)
        post = LL.posterior(em, FlatPrior(), sbar, nn, np.random.default_rng(2), M=20000)
        row[str(nn)] = {"sd_mean": float(post["sd_u"].mean()), "abs_err_mean": float(np.abs(post["mean_u"] - ut).mean()),
                        "ess": post["ess"]}
        chk = SL.posterior_checks(post, em, FlatPrior(), sbar, nn, ut)
        assert len(chk["pit"]) == dpar
    assert row["512"]["sd_mean"] < row["2"]["sd_mean"] and row["512"]["abs_err_mean"] < 0.2, row
    out["sbi_synthetic"][str(dpar)] = row

# 4 nets and ridges
NN.Cfg.LAGS, NN.Cfg.HS, NN.Cfg.EVAL_EVERY = (0, 1, 2, 4), (1, 2, 4), 2
items = [{"id": 1000 + i, "history": obs[i, :5], "program": LL.PL.dense_to_prog(U[i, 4:8]),
          "queries": {1: [1, 2, 4]}} for i in range(3)]
out["nets"] = {}
for v in LL.VIEWS:
    for cond in (False, True):
        ds = [NN.make_dataset(v, obs[:k], U[:k], SC, theta_u=(rng.uniform(-1, 1, (k, 4)) if cond else None), seed=k)
              for k in (2, 6)]
        prm, info = NN.train_nets(v, ds, cond=cond, steps=4, seed=3)
        th = rng.uniform(-1, 1, (3, 5, 4)) if cond else None
        S = NN.net_samples(v, prm[1], items, 5, 7, [1, 2, 4], SC, cond=cond, theta_u=th)
        assert S.shape == (3, 5, 3, LL.DIM[v]) and np.isfinite(S).all(), (v, cond, S.shape)
        if cond:
            S1 = NN.net_samples(v, prm[1], items, 5, 7, [1, 2, 4], SC, cond=True, theta_u=np.zeros(4))
            assert S1.shape == S.shape and np.isfinite(S1).all()
        out["nets"][f"{v}|cond={cond}"] = {"best_val": info["best_val"], "n_in": NN.n_in(v, cond)}
    model = LL.ridge_fit(v, obs, U, [1, 2, 4], SC)
    R = LL.ridge_samples(v, model, items, 5, 0, [1, 2, 4], SC)
    assert R.shape == (3, 5, 3, LL.DIM[v]) and np.isfinite(R).all(), (v, R.shape)

# 5 scoring path and acceptance
class FakeExam:
    n = 3
    queries = {1: [1, 2, 4], 2: [1, 2, 4], 3: [1, 2, 4]}
    cells = [(l, t) for l in (1, 2, 3) for t in (1, 2, 4)]


ex = FakeExam()
ex.truths = {l: rng.normal(0, 1, (3, 4, 3, dd)) for l, dd in ((1, 192), (2, 144), (3, 5))}
ex.scales = {1: SC["SC1"], 2: SC["SCO"], 3: SC["SCP"]}
for v in LL.VIEWS:
    l = LL.LEVEL[v]
    Sm = rng.normal(0, 1, (3, 6, 3, LL.DIM[v]))
    a = LL.ViewCells(ex, l).score(Sm)
    b = np.stack([energy_fair(Sm[:, :, j], ex.truths[l][:, :, j], ex.scales[l]) for j in range(3)], 1)
    assert np.allclose(a, b), v
ACC = LL.load_acceptance()
S = {"K": np.full((10, 2), 1.0), "C": np.full((10, 2), 0.4), "P0": np.full((10, 2), 0.5), "S": np.full((10, 2), 0.45),
     "D": np.full((10, 2), 0.7)}
r = ACC.shares(S, worlds=np.repeat([0, 1], 5), n_boot=50)
assert abs(r["sigma"] - (1.0 - 0.8) / (2.0 - 0.8)) < 1e-12 and abs(r["rho"] - 0.5) < 1e-12 and r["null_is"] == "P0"
out["scoring_path"] = "ViewCells.score == vw.scoring.energy_fair per cell; acceptance.shares reproduces sigma, rho"
out["jax"] = jax.__version__
os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
json.dump(out, open(os.path.join(HERE, "results", "check_lib.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
print("check_lib PASSED")
