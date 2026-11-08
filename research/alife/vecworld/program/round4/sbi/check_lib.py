"""check_lib -- CPU unit checks of sbi_lib / sbi_net (no simulation of the world).

1. params_batch == gworld.stack_params(theta_to_params(...)) for random theta.
2. sbi_lib.fit_ridge (vectorised) == gliders_exam/pilot.fit_ridge on random level-1 records.
3. Synthetic likelihood on a linear-Gaussian toy with the same interface: posterior coverage.
4. sbi_net: datasets, a few training steps of 2 nets in lockstep, sample shapes.
usage: python -B check_lib.py -> prints a JSON summary; exits non-zero on a failed check.
"""
import json
import sys
import time

import numpy as np

import sbi_lib as SL
import sbi_net as NN

GW, PL = SL.GW, SL.PL
out, bad = {}, []

# 1
rng = np.random.default_rng(0)
th = SL.LO + (SL.HI - SL.LO) * rng.random((3, 4))
A = SL.params_batch(th)
B = GW.stack_params([GW.theta_to_params(dict(zip(SL.NAMES, t))) for t in th])
d = max(float(np.abs(np.asarray(A[k]) - np.asarray(B[k])).max()) for k in B)
out["params_batch_max_abs_diff"] = d
out["params_keys_equal"] = sorted(A) == sorted(B)
if d > 0 or not out["params_keys_equal"]:
    bad.append("params_batch")

# 2
J, T1 = 3, 14
Y = rng.normal(0.1, 0.05, (J, T1, SL.N_OBS))
Y[..., SL.NC::GW.NF] = (rng.random((J, T1, GW.K)) > 0.4).astype(float)        # present flags
Y[..., SL.NC + 1::GW.NF] = rng.uniform(50, 200, (J, T1, GW.K))                  # masses
U = np.zeros((J, T1 - 1, SL.NW))
U[:, 5:9, :] = rng.normal(0, 0.05, (J, 4, SL.NW))
hs = [1, 2, 4, 8]
m_ref = PL.fit_ridge(Y, U, hs)
m_vec = SL.fit_ridge(Y, U, hs, chunk=7, max_res=10 ** 9)
diffs = {}
for h in hs:
    diffs[h] = [float(np.abs(a - b).max()) for a, b in zip(m_ref[h], m_vec[h])]
out["fit_ridge_max_abs_diff"] = diffs
if max(max(v) for v in diffs.values()) > 1e-9:
    bad.append("fit_ridge")

# 3 linear-Gaussian toy: s = M u + noise (per episode), design + truths from the uniform prior
q = 4
M = rng.normal(0, 1, (q, 4))
sd = np.array([1.0, 0.5, 2.0, 1.0])


def sim(u, n):
    return u @ M.T + 0.3 * (u ** 2) @ np.ones((4, q)) * 0.1 + sd * rng.standard_normal((n,) + u.shape[:-1] + (q,))


Ud = rng.uniform(-1, 1, (1000, 4))
S = np.stack([sim(Ud, 1)[0] for _ in range(4)], 1)
em = SL.Emulator().fit(Ud, S)


class Flat:
    def logp(self, u):
        return np.zeros(len(np.atleast_2d(u)))


cov = {}
t0 = time.time()
for n in (2, 32, 512):
    pits, hp = [], []
    for k in range(40):
        ut = rng.uniform(-1, 1, 4)
        sbar = sim(ut[None], n)[:, 0].mean(0)
        post = SL.posterior(em, Flat(), sbar, n, rng, M=20000)
        c = SL.posterior_checks(post, em, Flat(), sbar, n, ut)
        pits += c["pit"]
        hp.append(c["hpd_level"])
    pits = np.array(pits)
    cov[n] = {"in50": float(((pits > 0.25) & (pits < 0.75)).mean()), "in90": float(((pits > 0.05) & (pits < 0.95)).mean()),
              "hpd_le_50": float(np.mean(np.array(hp) <= 0.5)), "hpd_le_90": float(np.mean(np.array(hp) <= 0.9))}
out["toy_coverage"] = cov
out["toy_emulator"] = em.diag
out["toy_seconds"] = time.time() - t0
for n, c in cov.items():
    if not (0.3 < c["in50"] < 0.7 and 0.75 < c["in90"] <= 1.0):
        bad.append(f"toy coverage n={n}")

# 4 net
NN.Cfg.LAGS, NN.Cfg.HS = (0, 1, 2, 4), (1, 2, 4)
NN.Cfg.EVAL_EVERY = 5
E, T1 = 4, 13
obs = np.abs(rng.normal(0.1, 0.05, (E, T1, SL.N_OBS))).astype(np.float32)
obs[..., SL.NC::GW.NF] = (rng.random((E, T1, GW.K)) > 0.4)
obs[..., SL.NC + 1::GW.NF] = rng.uniform(50, 200, (E, T1, GW.K))
Uw = np.zeros((E, T1 - 1, SL.NW), np.float32)
Uw[:, 6:8] = rng.normal(0, 0.05, (E, 2, SL.NW))
ds = [NN.make_dataset(obs, Uw, seed=0), NN.make_dataset(obs[:2], Uw[:2], seed=1)]
params, info = NN.train_nets(ds, steps=10, seed=0)
items = [{"id": 5, "history": obs[0, :7], "program": [(1, {3: 0.1})], "queries": {1: [1, 2, 4], 2: [4]}}]
smp = NN.net_samples(params[0], items, 6, 0, [1, 2, 4], [4])
out["net"] = {"best_val": info["best_val"], "shapes": [list(smp[0][1].shape), list(smp[0][2].shape)],
              "finite": bool(np.isfinite(smp[0][1]).all() and np.isfinite(smp[0][2]).all())}
ds_c = [NN.make_dataset(obs, Uw, theta_u=rng.uniform(-1, 1, (E, 4)), seed=0)]
pc, _ = NN.train_nets(ds_c, cond=True, steps=5, seed=0)
smp_c = NN.net_samples(pc[0], items, 6, 0, [1, 2, 4], [4], cond=True, theta_u=rng.uniform(-1, 1, (1, 6, 4)))
out["net_cond_shapes"] = [list(smp_c[0][1].shape), list(smp_c[0][2].shape)]
if out["net"]["shapes"] != [[6, 3, 192], [6, 1, 3]] or not out["net"]["finite"]:
    bad.append("net")
out["failed"] = bad
print(json.dumps(out, indent=1, default=float))
sys.exit(1 if bad else 0)
