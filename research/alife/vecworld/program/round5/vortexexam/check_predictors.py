"""check_predictors -- CPU pre-flight of job 2's predictor families on job 1's law runs (minutes).

Data: origin/gpu-jobs:jobs/r5-vortexexam-002/out/law.npz (128^2, 5 selection coefficients x 64 members x 440 ticks,
no stirring, every other parameter at its default). Train on the first 48 members of every eps, test on the last
16 (one truth per item, so no oracle: scores are compared between predictors only). Families as in job 2 (vxnet):
net / ridge / law / lin2, each unconditional ('P0': eps unknown, prior = the five values) and conditional on the
true eps ('C'). Reported per horizon for s_b and N: the share of the variance of the change explained by the
predictive mean, 1 - MSE / V_change (V_change about the pooled mean change over the test items; its ceiling is the
oracle-predictable share, 0.51-0.56 for s_b in round 3), and the mean fair energy score of the joint change.
This checks that the families train at real size before GPU time is spent, and gives a first reading of the
linear-versus-nonlinear question; job 2 answers it with replicate truths, stirring and four hidden parameters.
usage: python -B check_predictors.py LAW_NPZ [--steps 3000]   -> results/check_predictors.json
"""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import vxlib as VX  # noqa: E402
import vxnet as NN  # noqa: E402

import numpy as np  # noqa: E402

from vw.scoring import energy_fair  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("law")
ap.add_argument("--steps", type=int, default=3000)
ap.add_argument("--m", type=int, default=32)
args = ap.parse_args()
PR = json.load(open(os.path.join(HERE, "prior.json")))
NN.set_const(PR["const"])
Z = np.load(args.law)
S1, eps = Z["S"].astype(np.float32), Z["eps"]                      # (nE, J, T, 12): state after i + 1 ticks
nE, J, T, _ = S1.shape
S = np.concatenate([S1[:, :, :1], S1], 2)                          # state index = ticks done (state 0 := state 1)
S = np.concatenate([S, np.zeros(S.shape[:3] + (2,), np.float32)], -1)   # near_lo, near_hi were not saved in job 1
NN.HIST = tuple(h for h in NN.HIST if h not in ("near_lo", "near_hi"))
u_eps = ((eps - 0.2) / 0.2)[:, None]                               # box units
n_tr = 48
tr = (S[:, :n_tr].reshape(nE * n_tr, T + 1, -1), np.repeat(u_eps, n_tr, 0))
te = (S[:, n_tr:].reshape(nE * (J - n_tr), T + 1, -1), np.repeat(u_eps, J - n_tr, 0))
anchors = [130, 210, 290, 370]
t0 = time.time()
out = {"source": "origin/gpu-jobs:jobs/r5-vortexexam-002/out/law.npz", "eps": eps.tolist(), "train_members_per_eps": n_tr,
       "test_members_per_eps": J - n_tr, "anchors": anchors, "hs": list(VX.HS), "steps": args.steps, "m": args.m,
       "history_channels": list(NN.HIST), "note": "one truth per item: no oracle; compare predictors with each other"}
Xte, Yte, L2a = NN.features(te[0], None, anchors)                  # (E, A, nh, F), (E, A, nh, 2)
Xte_c = NN.features(te[0], None, anchors, theta_u=te[1])[0]
nI = Xte.shape[0] * len(anchors)
Y = Yte.reshape(nI, len(VX.HS), 2).astype(float)                   # scaled changes
Vc = ((Y - Y.mean(0)) ** 2).mean(0)                                # (nh, 2)
res = {}
for cond in (False, True):
    ds = NN.dataset(tr[0], None, theta_u=tr[1] if cond else None, seed=1)
    X = (Xte_c if cond else Xte).reshape(nI, len(VX.HS), -1)
    d = 1 if cond else 0
    for fam in ("lin2", "ridge", "law", "net"):
        if fam == "net":
            mdl = NN.train_nets([ds], steps=args.steps, seed=3)[0][0]
            smp = NN.net_samples(mdl, X, args.m, 5)
        elif fam == "law":
            smp = NN.law_samples(NN.fit_law(ds, d_theta=d), X, args.m, 5)
        else:
            smp = NN.ridge_samples(NN.fit_ridge(ds, cols=NN.lin2_cols(d) if fam == "lin2" else None), X, args.m, 5)
        mu = smp.mean(1)
        es = [float(energy_fair(smp[:, :, j], Y[:, None, j]).mean()) for j in range(len(VX.HS))]
        res[f"{fam}|{'C' if cond else 'P0'}"] = {
            "explained_N": (1 - ((Y - mu) ** 2).mean(0) / Vc)[:, 0].round(3).tolist(),
            "explained_s_b": (1 - ((Y - mu) ** 2).mean(0) / Vc)[:, 1].round(3).tolist(),
            "energy_joint": np.round(es, 4).tolist()}
        print(fam, "C" if cond else "P0", res[f"{fam}|{'C' if cond else 'P0'}"], f"({time.time() - t0:.0f}s)", flush=True)
out.update(n_items=int(nI), n_train_examples=int(len(ds["Xtr"])), V_change_scaled=Vc.round(4).tolist(), predictors=res,
           seconds=time.time() - t0)
json.dump(out, open(os.path.join(HERE, "results", "check_predictors.json"), "w"), indent=1)
