"""run_toy -- validate exam harness v0 on the closed-form ring world (toy.py).

Stages (each writes results/<stage>.json; rerun skips finished stages):
  A  nats accountant against closed-form KL: charge = level-0 path KL (exact), Monte Carlo
     log-likelihood ratio on vw-simulated paths, observed-level KL (stationary start and given a
     revealed history), information efficiency, mean shift against sqrt(2C), rejections.
  B  exam (world 0, n = 128 items, R = 16) and estimator checks: vw truths against the closed-form
     oracle law; fair and v1 energy scores against exact expectations for the oracle (LOO), the
     true-theta filter (B3) and climatology, on the exam and over 400 redraws; effect on OES.
  C  budgets x worlds: for 3 hidden theta drawn from the prior, budgets zero / small (1 x 128
     ticks) / large (32 x 128 ticks), passive or active (8 nats per episode): B0, B1, B2 (synthetic
     likelihood + PMC with the public simulator), B2x (exact likelihood), B3, controls.
  D  item counts: paired gaps of the chain at n = 64 and n = 128 (R = 16), and n = 256 with R = 4
     (equal truth cost to n = 64, R = 16).
Usage: run_toy.py [A|B|C|D|S]...   (default: all, then the summary S)
"""
from __future__ import annotations

import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import toy as T  # noqa: E402
from vw.harness import HistoryExam, Lab, program_dense  # noqa: E402
from vw.nats import card_guarantee, kl_check, shift_kl, shift_llr  # noqa: E402
from vw.ports import InputViolation  # noqa: E402
from vw.scoring import (energy_fair, energy_loo, energy_v1, paired_gap, public_report,  # noqa: E402
                        ring_weights)
from vw.secret import Secret  # noqa: E402

OUT = os.path.join(HERE, "results")
HID = os.path.join(HERE, "hidden")
os.makedirs(OUT, exist_ok=True)
os.makedirs(HID, exist_ok=True)
N_ITEMS, R_TRUTH, N_WORLDS = 128, 16, 3
M_PMC, NREP_SL, ROUNDS, J_POST = 256, 16, 4, 64
BUDGETS = {"zero": (0, 0, False), "small_passive": (1, 128, False), "small_active": (1, 128, True),
           "large_passive": (32, 128, False), "large_active": (32, 128, True)}


def master_secret() -> Secret:
    p = os.path.join(HID, "secret.hex")
    if not os.path.exists(p):
        open(p, "w").write(Secret().hex())
    return Secret.from_hex(open(p).read().strip())


SEC = master_secret()
SCALES = T.public_scales()


def theta(w):
    return T.draw_theta(SEC.rng("theta", w))


def jdump(obj, name):
    def conv(o):
        if isinstance(o, dict):
            return {str(k): conv(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [conv(v) for v in o]
        if isinstance(o, np.ndarray):
            return conv(o.tolist())
        if isinstance(o, (np.floating, float)):
            return None if not math.isfinite(float(o)) else float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, np.bool_):
            return bool(o)
        return o
    with open(os.path.join(OUT, name), "w") as f:
        json.dump(conv(obj), f, indent=1)


def make_exam(w, n=N_ITEMS, R=R_TRUTH, name="exam"):
    return HistoryExam(T.world(theta(w)), SEC.child("world", w), T.program_mix(), n_items=n, prefix=T.PREFIX,
                       queries=T.QUERIES, R=R, derived={2: T.stat2}, scales=SCALES, nats=T.nats_budget(),
                       n_clim=256, vs_weights={1: ring_weights(T.G)}, name=name)


# ----------------------------------------------------------------------------- A
def stage_A():
    clk = T.Clock()
    th = theta(0)
    A = T.A_of(th)
    ex = make_exam(0, n=16, R=4, name="kl-programs")
    progs = {}
    for it in ex.items:
        if it.klass not in progs and it.program:
            progs[it.klass] = it.program
    progs["agent_active"] = [(t, T._block_push(b, s, T.TICK_CAP)) for t, b, s in [(0, 1, 1), (16, 4, -1), (32, 2, 1), (48, 5, -1)]]
    nb = T.nats_budget()
    out = {"theta": th.tolist(), "programs": {}}
    Hh = 64
    for name, prog in progs.items():
        U = program_dense(prog, Hh, T.N)
        charge = nb.program_cost(prog)
        kl0 = shift_kl(U, T.SIGMA ** 2 * np.eye(T.N))
        # Monte Carlo LLR on vw-simulated level-0 paths (stationary starts, true theta)
        w = T.world(th)
        d = w.designer
        ens = d.ensemble(4000, seed=(11, len(name)))
        _, rec = d.rollout(ens, U, T=Hh, rec=("x",))
        X = rec["x"]                                             # (n, Hh+1, 24)
        res = X[:, 1:] - X[:, :-1] @ A.T
        chk = kl_check(shift_llr(res, U, T.SIGMA ** 2 * np.eye(T.N)), charge)
        _, rec0 = d.rollout(d.ensemble(4000, seed=(12, len(name))), None, T=Hh, rec=("x",))
        X0 = rec0["x"]
        chk0 = kl_check(shift_llr(X0[:, 1:] - X0[:, :-1] @ A.T, U, T.SIGMA ** 2 * np.eye(T.N)), -charge)
        # observed-level KL in closed form: stacked o(1..Hh) (stationary start), and given a history
        Sig = T.Sigma_of(th)
        Ap = [np.linalg.matrix_power(A, k) for k in range(Hh + 1)]
        dm_x, dmx = [], np.zeros(T.N)
        for t in range(Hh):
            dmx = A @ dmx + U[t]
            dm_x.append(dmx.copy())
        dm = np.concatenate([T.CMAT @ v for v in dm_x])
        dm2 = np.concatenate([T.L2 @ T.CMAT @ v for v in dm_x])

        def stacked_cov(P0):
            # Cov of x(1..Hh) given x(0) ~ N(., P0), no input; then observed
            Mx = [P0]
            for t in range(Hh):
                Mx.append(A @ Mx[-1] @ A.T + T.SIGMA ** 2 * np.eye(T.N))
            S = np.zeros((Hh * T.G, Hh * T.G))
            for i in range(1, Hh + 1):
                for j in range(1, i + 1):
                    blk = T.CMAT @ Ap[i - j] @ Mx[j] @ T.CMAT.T
                    if i == j:
                        blk = blk + T.R_OBS ** 2 * np.eye(T.G)
                    S[(i - 1) * T.G:i * T.G, (j - 1) * T.G:j * T.G] = blk
                    S[(j - 1) * T.G:j * T.G, (i - 1) * T.G:i * T.G] = blk.T
            return S
        S_st = stacked_cov(Sig)
        it0 = ex.items[0]
        _, Pf, _ = T.kalman_history(th[None], it0.history, np.zeros((T.PREFIX, T.N)))
        S_h = stacked_cov(Pf[0])
        L2b = np.kron(np.eye(Hh), T.L2)
        kl_st = 0.5 * dm @ np.linalg.solve(S_st, dm)
        kl_h = 0.5 * dm @ np.linalg.solve(S_h, dm)
        kl_h2 = 0.5 * dm2 @ np.linalg.solve(L2b @ S_h @ L2b.T, dm2)
        shift_sd = float(np.max(np.abs(dm) / np.sqrt(np.diag(S_h))))
        out["programs"][name] = {
            "n_commands": len(prog), "charge_nats": charge, "closed_form_level0_kl": kl0,
            "charge_minus_kl": charge - kl0, "mc_llr": chk, "mc_llr_under_P0": chk0,
            "kl_obs_level1_stationary": kl_st, "kl_obs_level1_given_history": kl_h,
            "kl_obs_level2_given_history": kl_h2,
            "efficiency_level1_given_history": kl_h / charge, "efficiency_level1_stationary": kl_st / charge,
            "max_mean_shift_sd_level1_given_history": shift_sd, "sqrt_2C": math.sqrt(2 * charge),
            "card": card_guarantee(charge)}
    # rejections before running
    lab = Lab(T.world(th), SEC.child("kl-lab"), nats=T.nats_budget(total=10.0), max_ticks=200)
    lab.reset(1)
    rej = {}
    before = dict(lab.usage())
    for nm, call in {"tick_cap": lambda: lab.step(T._block_push(0, 1, 2.5)),
                     "episode_cap": lambda: lab.run([(t, T._block_push(0, 1, 2.0)) for t in range(5)], [6]),
                     "max_ticks": lambda: lab.run([], [500])}.items():
        try:
            call()
            rej[nm] = "accepted (unexpected)"
        except (InputViolation, Exception) as e:  # noqa: B014
            rej[nm] = type(e).__name__ + ": " + str(e)[:160]
    rej["usage_unchanged"] = lab.usage() == before
    lab.run([(t, T._block_push(0, 1, 2.0)) for t in range(4)], [5])
    lab.reset(2)
    try:
        lab.run([(t, T._block_push(0, 1, 2.0)) for t in range(2)], [3])
        rej["total_cap"] = "accepted (unexpected)"
    except InputViolation as e:
        rej["total_cap"] = "InputViolation: " + str(e)[:160]
    out["rejections"] = rej
    out["cpu_s"] = clk()
    jdump(out, "stageA.json")
    print("A done", clk())


# ----------------------------------------------------------------------------- B
def _en(mu, S, rng, K=100000):
    """E |mu + L z| / sqrt(d) for each row of mu (n, d), covariance S (d, d) (Monte Carlo)."""
    L = np.linalg.cholesky(S)
    d = mu.shape[1]
    out = np.empty(len(mu))
    for i, m in enumerate(mu):
        z = rng.standard_normal((K, d)) @ L.T
        out[i] = np.linalg.norm(z + m, axis=1).mean() / math.sqrt(d)
    return out


def _cell_maps():
    """For each cell: (level, time, linear map from o (6) to the cell, scale)."""
    out = []
    for l, ts in T.QUERIES.items():
        Lm = np.eye(T.G) if l == 1 else T.L2
        for t in ts:
            out.append((l, t, Lm, SCALES[l]))
    return out


def stage_B():
    clk = T.Clock()
    th = theta(0)
    ex = make_exam(0)
    xP = np.asarray(ex._snap.x_flat())                           # (n, 24) hidden states at P
    n = ex.n
    rng = np.random.default_rng(5)
    Sig = T.Sigma_of(th)
    # closed-form laws per item and cell
    cells = _cell_maps()
    exact = {"oracle": np.zeros((n, len(cells))), "B3": np.zeros((n, len(cells))), "clim": np.zeros((n, len(cells)))}
    zres = []
    for i, it in enumerate(ex.items):
        test = program_dense(it.program, T.H, T.N)
        mo, So = T.predictive_moments(th, xP[i], np.zeros((T.N, T.N)), test, sorted(set(sum(T.QUERIES.values(), []))))
        mK, SKx, _ = T.kalman_history(th[None], it.history, np.zeros((T.PREFIX, T.N)))
        mk, Sk = T.predictive_moments(th, mK[0], SKx[0], test, sorted(set(sum(T.QUERIES.values(), []))))
        tl = sorted(set(sum(T.QUERIES.values(), [])))
        Sst = T.CMAT @ Sig @ T.CMAT.T + T.R_OBS ** 2 * np.eye(T.G)
        for c, (l, t, Lm, sc) in enumerate(cells):
            k = tl.index(t)
            D = np.diag(1 / sc)
            mo_c, So_c = D @ Lm @ mo[k], D @ Lm @ So[k] @ Lm.T @ D
            mk_c, Sk_c = D @ Lm @ mk[k], D @ Lm @ Sk[k] @ Lm.T @ D
            Sst_c = D @ Lm @ Sst @ Lm.T @ D
            exact["oracle"][i, c] = 0.5 * _en(np.zeros((1, len(mo_c))), 2 * So_c, rng)[0]
            exact["B3"][i, c] = (_en((mk_c - mo_c)[None], Sk_c + So_c, rng)[0]
                                 - 0.5 * _en(np.zeros((1, len(mo_c))), 2 * Sk_c, rng)[0])
            exact["clim"][i, c] = (_en((-mo_c)[None], Sst_c + So_c, rng)[0]
                                   - 0.5 * _en(np.zeros((1, len(mo_c))), 2 * Sst_c, rng)[0])
            if l == 1:      # vw truths against the closed-form oracle law (standardised residuals)
                Y = ex.truths[1][i, :, ex.queries[1].index(t)]
                zres.append(np.linalg.solve(np.linalg.cholesky(So[k]), (Y - mo[k]).T).T)
    zres = np.concatenate(zres)
    out = {"theta": th.tolist(), "n_items": n, "R": ex.R,
           "truth_law_check": {"n": int(len(zres)), "mean_abs_max": float(np.abs(zres.mean(0)).max()),
                               "cov_minus_I_abs_max": float(np.abs(np.cov(zres.T) - np.eye(T.G)).max()),
                               "se_mean": float(1 / math.sqrt(len(zres)))}}
    # estimates on the exam
    refs = ex.references()
    b3 = T.filter_predictor(th)
    sc_b3 = ex.score(ex.collect(b3, 64, 0))
    pool64 = {l: v[:64] for l, v in ex.clim.items()}
    est = {"oracle_fair_m15": refs["oracle"]["es"], "oracle_v1_m15": refs["oracle"]["es_v1"],
           "B3_fair_m64": sc_b3["es"], "B3_v1_m64": sc_b3["es_v1"],
           "clim_fair_m256": refs["climatology"]["es"], "clim_v1_m256": refs["climatology"]["es_v1"],
           "clim_fair_m64": ex._per_cell(lambda X, Y, s, l: energy_fair(X, Y, s), pool=pool64),
           "clim_v1_m64": ex._per_cell(lambda X, Y, s, l: energy_v1(X, Y, s), pool=pool64)}
    R4 = {l: v[:, :4] for l, v in ex.truths.items()}
    saved = ex.truths
    ex.truths = R4
    est["oracle_fair_m3"] = ex._per_cell(None, lambda Y, s, l: energy_loo(Y, s, True))
    est["oracle_v1_m3"] = ex._per_cell(None, lambda Y, s, l: energy_loo(Y, s, False))
    ex.truths = saved
    ref_of = {"oracle": "oracle", "B3": "B3", "clim": "clim"}
    chk = {}
    for k, v in est.items():
        e = exact[ref_of[k.split("_")[0]]]
        dlt = (v - e).mean(1)                                     # per item, mean over cells
        chk[k] = {"mean_est": float(v.mean()), "mean_exact": float(e.mean()), "bias": float((v - e).mean()),
                  "se": float(dlt.std(ddof=1) / math.sqrt(n)), "z": float((v - e).mean() / (dlt.std(ddof=1) / math.sqrt(n))),
                  "rel_bias": float((v - e).mean() / e.mean())}
    out["exam_estimates"] = chk
    # redraws: 400 fresh truth sets / sample sets from the closed-form laws for 32 items, all cells
    reps = 400
    rr = np.random.default_rng(9)
    red = {k: [] for k in ("oracle_fair_m15", "oracle_v1_m15", "oracle_fair_m3", "oracle_v1_m3", "B3_fair_m64", "B3_v1_m64")}
    exa = {"oracle": [], "B3": []}
    for i in range(32):
        it = ex.items[i]
        test = program_dense(it.program, T.H, T.N)
        tl = sorted(set(sum(T.QUERIES.values(), [])))
        mo, So = T.predictive_moments(th, xP[i], np.zeros((T.N, T.N)), test, tl)
        mK, SKx, _ = T.kalman_history(th[None], it.history, np.zeros((T.PREFIX, T.N)))
        mk, Sk = T.predictive_moments(th, mK[0], SKx[0], test, tl)
        for c, (l, t, Lm, scl) in enumerate(cells):
            k = tl.index(t)
            D = np.diag(1 / scl)
            mo_c, Lo = D @ Lm @ mo[k], np.linalg.cholesky(D @ Lm @ So[k] @ Lm.T @ D)
            mk_c, Lk = D @ Lm @ mk[k], np.linalg.cholesky(D @ Lm @ Sk[k] @ Lm.T @ D)
            d = len(mo_c)
            Y = mo_c + rr.standard_normal((reps, 16, d)) @ Lo.T
            X = mk_c + rr.standard_normal((reps, 64, d)) @ Lk.T
            red["oracle_fair_m15"].append(energy_loo(Y))
            red["oracle_v1_m15"].append(energy_loo(Y, fair=False))
            red["oracle_fair_m3"].append(energy_loo(Y[:, :4]))
            red["oracle_v1_m3"].append(energy_loo(Y[:, :4], fair=False))
            red["B3_fair_m64"].append(energy_fair(X, Y))
            red["B3_v1_m64"].append(energy_v1(X, Y))
            exa["oracle"].append(exact["oracle"][i, c])
            exa["B3"].append(exact["B3"][i, c])
    rchk = {}
    for k, v in red.items():
        v = np.array(v)                                           # (32*cells, reps)
        e = np.array(exa[k.split("_")[0]])
        dif = v.mean(0) - e.mean()                                # per redraw, mean over item-cells
        m = int(k.split("_m")[1])
        rchk[k] = {"bias": float(dif.mean()), "se": float(dif.std(ddof=1) / math.sqrt(reps)),
                   "rel_bias": float(dif.mean() / e.mean()), "m": m,
                   "theory_v1_bias": float(e.mean() / m) if "v1" in k and k.startswith("oracle") else None}
    out["redraw_estimates"] = rchk
    # effect on OES: B3's aggregate under exact, fair and v1 conventions
    valid = (exact["clim"] - exact["oracle"]).mean(0) > 0.0
    rep_f = ex.report({"B3": sc_b3}, key="es")
    rep_v = ex.report({"B3": {"es_v1": sc_b3["es_v1"]}}, key="es_v1", valid=np.array(rep_f["valid"]),
                      refs={"oracle": {"es_v1": refs["oracle"]["es_v1"]}, "climatology": {"es_v1": refs["climatology"]["es_v1"]}})
    vv = np.array(rep_f["valid"])
    oes_exact = ((exact["clim"].mean(0) - exact["B3"].mean(0)) / (exact["clim"].mean(0) - exact["oracle"].mean(0)))
    oes_v1_R4 = ((refs["climatology"]["es_v1"].mean(0) - sc_b3["es_v1"].mean(0)) /
                 (refs["climatology"]["es_v1"].mean(0) - est["oracle_v1_m3"].mean(0)))
    oes_f_R4 = ((refs["climatology"]["es"].mean(0) - sc_b3["es"].mean(0)) /
                (refs["climatology"]["es"].mean(0) - est["oracle_fair_m3"].mean(0)))
    out["oes_B3"] = {"valid_cells": vv.tolist(), "cells": [list(c) for c in ex.cells],
                     "exact": float(oes_exact[vv].mean()), "exact_per_cell": oes_exact.tolist(),
                     "fair_R16": rep_f["aggregate"]["B3"], "fair_R16_se": rep_f["se"]["B3"],
                     "v1_R16": rep_v["aggregate"]["B3"], "fair_R4": float(oes_f_R4[vv].mean()),
                     "v1_R4": float(oes_v1_R4[vv].mean()),
                     "per_cell_fair_R16": rep_f["oes"]["B3"], "per_cell_v1_R16": rep_v["oes"]["B3"],
                     "per_cell_fair_R4": oes_f_R4.tolist(), "per_cell_v1_R4": oes_v1_R4.tolist(),
                     "denominator_exact": (exact["clim"].mean(0) - exact["oracle"].mean(0)).tolist(),
                     "denominator_fair_R16": (refs["climatology"]["es"].mean(0) - refs["oracle"]["es"].mean(0)).tolist(),
                     "denominator_v1_R16": (refs["climatology"]["es_v1"].mean(0) - refs["oracle"]["es_v1"].mean(0)).tolist(),
                     "denominator_v1_R4": (refs["climatology"]["es_v1"].mean(0) - est["oracle_v1_m3"].mean(0)).tolist()}
    out["valid_exact_denominator"] = valid.tolist()
    out["cpu_s"] = clk()
    jdump(out, "stageB.json")
    print("B done", clk())


# ----------------------------------------------------------------------------- C
def _post_summary(TH, lw, th):
    w = np.exp(lw - lw.max())
    w /= w.sum()
    m = w @ TH
    sd = np.sqrt(w @ (TH - m) ** 2)
    return {"mean": m.tolist(), "sd": sd.tolist(), "true": th.tolist(), "z": ((m - th) / np.maximum(sd, 1e-12)).tolist(),
            "ess": float(1 / (w ** 2).sum())}


def stage_C(worlds=range(N_WORLDS)):
    sim = T.Simulator()
    for w in worlds:
        fn = os.path.join(OUT, f"stageC_w{w}.json")
        if os.path.exists(fn):
            continue
        clk = T.Clock()
        th = theta(w)
        ex = make_exam(w)
        refs = ex.references()
        scored, info, preds = {}, {}, {}
        fixed = {"B3_true_theta": T.filter_predictor(th),
                 "ctrl_prior_mean": T.filter_predictor(T.PRIOR_MEAN, reweight=False),
                 "ctrl_ignore_actions": T.filter_predictor(th, ignore_actions=True)}
        rng0 = np.random.default_rng([w, 1])
        prior_draws = np.stack([T.draw_theta(rng0) for _ in range(J_POST)])
        fixed["B2@zero"] = T.filter_predictor(prior_draws)
        fixed["B2@zero_noreweight"] = T.filter_predictor(prior_draws, reweight=False)
        fixed["B0@zero"] = T.prior_climatology(seed=w)
        for k, f in fixed.items():
            scored[k] = ex.score(ex.collect(f, 64, 0))
            preds[k] = f
        for bname, (E, L, active) in BUDGETS.items():
            if E == 0:
                continue
            c0 = T.Clock()
            lab = Lab(T.world(th), SEC.child("agent", w, bname),
                      nats=T.nats_budget(total=T.EPISODE_CAP * E if active else 0.0), max_ticks=E * (L + 1))
            eps = T.collect(lab, E, L, active, seed=w * 100 + len(bname))
            bi = {"usage": lab.usage()}
            b0 = T.climatology_from_data(eps)
            b1 = T.fit_arx(eps)
            bi["B1"] = b1.info
            rng = np.random.default_rng([w, len(bname), 2])
            mt0 = sim.member_ticks
            c1 = T.Clock()
            THs, lws, dg = T.pmc(T.synthetic_loglik(sim, eps, n_rep=NREP_SL, seed=w * 10 + len(bname)), rng,
                                 M=M_PMC, rounds=ROUNDS)
            bi["B2_cpu_s"] = c1()
            bi["B2_member_ticks"] = sim.member_ticks - mt0
            bi["B2_rounds"] = dg
            bi["B2_post"] = _post_summary(THs, lws, th)
            c2 = T.Clock()
            THx, lwx, dgx = T.pmc(T.exact_loglik(eps), np.random.default_rng([w, len(bname), 3]), M=M_PMC, rounds=ROUNDS)
            bi["B2x_cpu_s"] = c2()
            bi["B2x_rounds"] = dgx
            bi["B2x_post"] = _post_summary(THx, lwx, th)
            b2 = T.filter_predictor(T.posterior_draws(THs, lws, J_POST, rng))
            b2x = T.filter_predictor(T.posterior_draws(THx, lwx, J_POST, rng))
            todo = {"B0": b0, "B1": b1, "B2": b2, "B2x": b2x}
            if E >= 8:          # B2s: synthetic likelihood from 4-episode simulated datasets
                mt0 = sim.member_ticks
                c3 = T.Clock()
                THq, lwq, dgq = T.pmc(T.synthetic_loglik(sim, eps, n_rep=NREP_SL, seed=w * 10 + len(bname) + 5,
                                                         sim_episodes=4), np.random.default_rng([w, len(bname), 4]),
                                      M=M_PMC, rounds=ROUNDS)
                bi["B2s_cpu_s"] = c3()
                bi["B2s_member_ticks"] = sim.member_ticks - mt0
                bi["B2s_rounds"] = dgq
                bi["B2s_post"] = _post_summary(THq, lwq, th)
                todo["B2s"] = T.filter_predictor(T.posterior_draws(THq, lwq, J_POST, rng))
            for k, f in todo.items():
                scored[f"{k}@{bname}"] = ex.score(ex.collect(f, 64, 0))
                preds[f"{k}@{bname}"] = f
            bi["cpu_s"] = c0()
            info[bname] = bi
            print(w, bname, "cpu", round(c0(), 1), bi["B2_post"]["mean"], bi["B2x_post"]["mean"], th, flush=True)
        rep = ex.report(scored, key="es")
        repv = ex.report({k: v for k, v in scored.items()}, key="vs", valid=None)
        res = {"theta": th.tolist(), "n_items": ex.n, "R": ex.R, "budgets": info, "report": public_report(rep),
               "report_vs": public_report(repv), "cpu_s": clk()}
        chain = {}
        for b in BUDGETS:
            if b == "zero":
                continue
            ks = [f"B0@{b}", f"B1@{b}", f"B2@{b}", "B3_true_theta", "oracle"]
            chain[b] = {f"{c}-{a}": paired_gap(rep, c, a) for a, c in zip(ks[:-1], ks[1:])}
            chain[b][f"B0@{b}-climatology"] = paired_gap(rep, f"B0@{b}", "climatology")
            chain[b][f"B1@{b}-climatology"] = paired_gap(rep, f"B1@{b}", "climatology")
            chain[b][f"B2x@{b}-B2@{b}"] = paired_gap(rep, f"B2x@{b}", f"B2@{b}")
        res["gaps_n128"] = chain
        jdump(res, f"stageC_w{w}.json")
        if w == 0:
            stage_D(preds, ex, scored, refs)
        print("C world", w, "cpu", clk(), flush=True)


# ----------------------------------------------------------------------------- D
def stage_D(preds, ex128, scored, refs):
    clk = T.Clock()
    out = {}
    keys = ["B0@small_active", "B1@small_active", "B2@small_active", "B0@large_passive", "B1@large_passive",
            "B2@large_passive", "B1@large_active", "B2@large_active", "B3_true_theta", "B2@zero"]
    # n = 64 (first half) and n = 128, R = 16
    from vw.scoring import skill_report
    for nn in (64, 128):
        S = {"climatology": refs["climatology"]["es"][:nn], "oracle": refs["oracle"]["es"][:nn]}
        S.update({k: scored[k]["es"][:nn] for k in keys})
        rep = skill_report(S, cells=ex128.cells, groups=ex128.classes[:nn])
        out[f"n{nn}_R16"] = _chains(rep)
    # n = 256, R = 4 (equal truth cost to n = 64, R = 16)
    ex4 = make_exam(0, n=256, R=4, name="exam-R4")
    sc = {k: ex4.score(ex4.collect(preds[k], 64, 0)) for k in keys}
    rep4 = ex4.report(sc, key="es")
    out["n256_R4"] = _chains(rep4)
    out["cpu_s"] = clk()
    jdump(out, "stageD.json")
    print("D done", clk(), flush=True)


def _chains(rep):
    o = {"aggregate": rep["aggregate"], "se": rep["se"], "valid": rep["valid"]}
    for b in ("small_active", "large_passive", "large_active"):
        ks = [f"B0@{b}", f"B1@{b}", f"B2@{b}", "B3_true_theta", "oracle"]
        if not all(k in rep["aggregate"] for k in ks):
            continue
        o[b] = {f"{c}-{a}": paired_gap(rep, c, a) for a, c in zip(ks[:-1], ks[1:])}
        o[b][f"B0@{b}-climatology"] = paired_gap(rep, f"B0@{b}", "climatology")
    return o


if __name__ == "__main__":
    import jax  # noqa: F401
    stages = sys.argv[1:] or ["A", "B", "C"]
    t0 = time.process_time()
    for s in stages:
        if s == "A" and not os.path.exists(os.path.join(OUT, "stageA.json")):
            stage_A()
        elif s == "B" and not os.path.exists(os.path.join(OUT, "stageB.json")):
            stage_B()
        elif s == "C":
            stage_C()
        elif s.startswith("C") and s[1:].isdigit():
            stage_C([int(s[1:])])
    print("total cpu", time.process_time() - t0)
