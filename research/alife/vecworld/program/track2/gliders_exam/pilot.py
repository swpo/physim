"""pilot -- part (b): the vw exam harness (Lab, Item, ProgramMix, HistoryExam, vw.scoring) on the gliders
wind world with 4 hidden global parameters, at small scale.

World      gworld.level(sigma_w = 0.05) (wind input, 128 coefficients, identity in/out maps, no
           permutations), level 1 = <Phi_coarse, Phi_objects> (336 numbers, quantum 1e-3), burn-in 50
           ticks, replay 'initial'; aworld.MapWorld (lax.map batching). One World object; the hidden theta
           is swapped through world.params (the compiled programs take params as an argument).
Hidden     theta = the 4 parameters of results/prior.json: uniform on the box, conditioned on the public
           viability rule (viab_joint.viability); truths are the first viable draws. The prior-mean control
           uses the box centre (= A_gliders), not the mean of the conditioned prior.
Budget     NatsBudget.isotropic(128, sigma_w): c(u) = |u|^2 / (2 sigma_w^2); tick cap 100, episode cap 400.
Programs   ProgramMix, equal shares: (a) none; (b) blind random (8 coefficients at random ticks, rate 0.25,
           U(0, 50] nats each); (c) aimed: 200 nats over 4 ticks on the 2 x 2 blocks around the fastest body
           of the last revealed observation, along its left normal; (d) regional: 300 nats over 4 ticks on
           the 4 x 4 blocks around the heaviest 2 x 2 group, random direction.
Exam       HistoryExam (subclass: level 1 scored on the coarse view, level 2 = population (count, tracked
           mass, mean speed) of the objects readout): P = 16, queries level 1 at h = 1, 2, 4, 8, 16 and
           level 2 at h = 8, 16; R = 8 truths per item; climatology pool of 16 no-input runs.
Controls   oracle (LOO over the R truths) and climatology (built in);
           plug-in pair (designer side, from the hidden x_P, m = 8 fresh-noise members, same test program):
               'plugin_true' (theta) and 'plugin_prior' (prior mean theta_0);
           ridge pair (behaviour level, history only): a translation-equivariant patch ridge per horizon on
               3 lags of the 3 x 3 block neighbourhood plus the program's summed wind there, empirical
               residual vectors as the predictive spread, trained on simulations under theta ('ridge_true')
               or theta_0 ('ridge_prior'); 'ridge_true_noact' drops the wind features (ignore-actions).
usage: python -B pilot.py [n_truths]   -> results/pilot.json, results/pilot_scores.npz
"""
import json
import math
import os
import sys
import time

import jax
import jax.numpy as jnp
import numpy as np

import gworld as GW
import phi as PH
import aworld as AW
import vw
from vw.harness import HistoryExam, Lab, ProgramMix, program_dense
from vw.nats import NatsAccountant, NatsBudget
from vw.ports import BudgetExhausted, InputViolation
from vw.scoring import paired_gap, public_report, skill_report
from vw.secret import Secret
from vw.world import make_key, member_keys

HERE = GW.HERE
RES = GW.RES
SIG = GW.SIGMA_W
P_PRE, QUERIES, R_TRUTH, N_ITEMS, N_CLIM, M_PLUG = 16, {1: [1, 2, 4, 8, 16], 2: [8, 16]}, 8, 8, 16, 8
HMAX = 16
TICK_CAP, EP_CAP, C_AIM, C_REG = 100.0, 400.0, 200.0, 300.0
J_TR, CH_TR, N_CH = 4, 10, 6                 # ridge training: members per theta, chunk ticks, chunks
M_RIDGE = 32
CLOCK = {"t0": time.time(), "member_ticks": 0}
SMOKE = os.environ.get("GE_SMOKE") == "1"          # tiny end-to-end test of the code path (separate outputs)
if SMOKE:
    P_PRE, QUERIES, R_TRUTH, N_ITEMS, N_CLIM, M_PLUG, HMAX = 3, {1: [1, 2], 2: [2]}, 3, 4, 4, 3, 2
    J_TR, CH_TR, N_CH, M_RIDGE = 2, 6, 2, 4
TAG = "pilot_smoke" if SMOKE else "pilot"


def log(*a):
    print(f"[{time.time() - CLOCK['t0']:7.1f}s]", *a, flush=True)


def secret():
    os.makedirs(os.path.join(HERE, "hidden"), exist_ok=True)
    f = os.path.join(HERE, "hidden", "secret.hex")
    if not os.path.exists(f):
        open(f, "w").write(os.urandom(32).hex())
    return Secret.from_hex(open(f).read().strip())


# ----------------------------------------------------------------------------- world and exam
def build_world(params):
    lev = GW.level(SIG, params)
    pc = PH.phi_coarse(GW.CFG, GW.G)
    po, _, _ = PH.phi_objects_jax("A_gliders")
    n_obs = GW.NC + GW.NO
    spec = vw.WorldSpec(base=lev, chain=(PH.pair(pc, po),),
                        inport=vw.InputPort(admissible=vw.Admissible(k=None, lo=-1.0, hi=1.0), in_map=tuple(range(GW.NW))),
                        outport=vw.ObservePort(noise=0.0, quantum=1e-3, out_map=tuple(range(n_obs)),
                                               out_sign=tuple([1.0] * n_obs)),
                        burn_in=GW.BURN, replay="initial", name="gliders_wind_hidden4",
                        public_notes="wind input: 128 coefficients (2 x 8 x 8), cost |u|^2 / (2 sigma_w^2) nats")
    return AW.MapWorld(spec, world_seed=0, params=params)


class GExam(HistoryExam):
    """HistoryExam whose level 1 is the coarse part of the observation (derived like level 2)."""

    def _level(self, l, obs):
        return np.asarray(self.derived[l](obs))


def budget(total=None):
    return NatsBudget.isotropic(GW.NW, SIG, tick=TICK_CAP, episode=EP_CAP, total=total,
                                note="wind coefficients enter as a shift before N(0, sigma_w^2 I) actuation noise")


def dense_to_prog(U):
    return [(int(t), {int(j): float(U[t, j]) for j in np.flatnonzero(U[t])}) for t in range(U.shape[0]) if np.any(U[t])]


def cls_none(rng, hist, H, left):
    return []


def cls_blind(rng, hist, H, left, k=8, rate=0.25, cmax=50.0):
    U = np.zeros((H, GW.NW))
    for t in range(H):
        if rng.random() >= rate or left <= 1e-6:
            continue
        idx = rng.choice(GW.NW, size=k, replace=False)
        v = rng.standard_normal(k)
        c_t = min(rng.uniform(0, cmax), left)
        v *= math.sqrt(2 * c_t * SIG ** 2 / float((v ** 2).sum())) * (1 - 1e-9)
        v = np.clip(v, -0.99, 0.99)
        U[t, idx] = v
        left -= GW.nats_of(v)
    return dense_to_prog(U)


def cls_aimed(rng, hist, H, left):
    U, _ = GW.aimed_push(hist[-1, GW.NC:GW.NC + GW.NO], min(C_AIM, left), SIG, H=H)
    return dense_to_prog(U)


def cls_regional(rng, hist, H, left):
    U = GW.regional_push(hist[-1, :GW.NC], rng.uniform(0, 2 * np.pi), min(C_REG, left), SIG, H=H)
    return dense_to_prog(U)


MIX = ProgramMix({"a": cls_none, "b": cls_blind, "c": cls_aimed, "d": cls_regional})


# ----------------------------------------------------------------------------- prior
def load_prior():
    pr = json.load(open(os.environ.get("GE_PRIOR", os.path.join(RES, "prior.json"))))
    return pr["names"], np.array(pr["lo"], float), np.array(pr["hi"], float)


def theta_dict(names, v):
    return {k: float(x) for k, x in zip(names, v)}


# ----------------------------------------------------------------------------- plug-in controls
def plugin_samples(ex, world, params, m, keys):
    old = world.params
    world.params = params
    try:
        rep = ex._snap.clone(rep=m, keys=keys)
        Pfull = np.concatenate([np.zeros((ex.n, ex.P, world.n_in)), ex._Ptest], 1)
        _, rec = world.designer.rollout(rep, np.repeat(Pfull, m, axis=0), T=ex.H, rec=("obs",))
    finally:
        world.params = old
    CLOCK["member_ticks"] += ex.n * m * ex.H
    obs = rec["obs"].reshape(ex.n, m, ex.H + 1, -1)
    return {l: ex._level(l, obs[:, :, ex.queries[l]]) for l in ex.queries}


def table_predictor(ex, S):
    ids = [it.id for it in ex.items]

    def predict(item, n_samples, seed):
        i = ids.index(item["id"])
        return {l: S[l][i] for l in S}
    return predict


# ----------------------------------------------------------------------------- ridge (behaviour level)
SC = np.load(os.path.join(RES, "scales.npz"))
SC1 = SC["level1"].reshape(3, GW.G, GW.G)
SC2 = SC["level2"]
OFFS = [(dy, dx) for dy in (-1, 0, 1) for dx in (-1, 0, 1)]


def nbhd(F):
    """(c, G, G) -> (c * 9, G, G): the 3 x 3 periodic neighbourhood of every block."""
    return np.concatenate([np.roll(np.roll(F, -dy, -2), -dx, -1) for dy, dx in OFFS], 0)


def feats(y3, usum, act=True):
    """y3 (3, 336) lags [t, t-1, t-2]; usum (NW,) summed wind -> (64, n_f) per-block features."""
    fs = [nbhd(y3[l, :GW.NC].reshape(3, GW.G, GW.G) / SC1) for l in range(3)]
    if act:
        fs.append(nbhd(usum.reshape(2, GW.G, GW.G) / SIG))
    X = np.concatenate(fs, 0).reshape(-1, GW.G * GW.G).T
    return np.concatenate([X, np.ones((X.shape[0], 1))], 1)


def feats2(y3, usum):
    p = GW.population(y3) / SC2                       # (3, 3)
    return np.concatenate([p.ravel(), [GW.nats_of(usum) / 100.0, 1.0]])


def fit_ridge(Y, U, hs, lam=1.0, act=True):
    """Y (J, T+1, 336) and U (J, T, NW) from training runs -> {h: (W1, res1, W2, res2)}."""
    model = {}
    for h in hs:
        X1, T1, X2, T2, keys = [], [], [], [], []
        for j in range(Y.shape[0]):
            for t in range(2, Y.shape[1] - h):
                y3 = Y[j, [t, t - 1, t - 2]]
                us = U[j, t:t + h].sum(0)
                X1.append(feats(y3, us, act))
                d = (Y[j, t + h, :GW.NC] - Y[j, t, :GW.NC]).reshape(3, GW.G, GW.G) / SC1
                T1.append(d.reshape(3, -1).T)
                X2.append(feats2(y3, us))
                T2.append((GW.population(Y[j, t + h]) - GW.population(Y[j, t])) / SC2)
        X1 = np.stack(X1); T1 = np.stack(T1)                 # (N, 64, f), (N, 64, 3)
        A = X1.reshape(-1, X1.shape[-1]); B = T1.reshape(-1, 3)
        W1 = np.linalg.solve(A.T @ A + lam * np.eye(A.shape[1]), A.T @ B)
        res1 = (B - A @ W1).reshape(T1.shape)                 # (N, 64, 3)
        res1 = res1.transpose(0, 2, 1).reshape(len(T1), -1)   # (N, 192) coarse layout, scaled
        X2 = np.stack(X2); T2 = np.stack(T2)
        W2 = np.linalg.solve(X2.T @ X2 + lam * np.eye(X2.shape[1]), X2.T @ T2)
        res2 = T2 - X2 @ W2
        model[h] = (W1, res1, W2, res2)
    return model


def ridge_predictor(model, act=True):
    def predict(item, n_samples, seed):
        hist = np.asarray(item["history"], float)
        y3 = hist[[-1, -2, -3]]
        U = program_dense(item["program"], HMAX, GW.NW)
        rng = np.random.default_rng([seed, int(item["id"]) % (2 ** 32)])
        out = {}
        for l, ts in item["queries"].items():
            arr = []
            for h in ts:
                W1, res1, W2, res2 = model[h]
                us = U[:h].sum(0)
                if l == 1:
                    mu = (feats(y3, us, act) @ W1).T.reshape(-1) * SC1.reshape(-1) + y3[0, :GW.NC]
                    r = res1[rng.integers(0, len(res1), n_samples)] * SC1.reshape(-1)
                else:
                    mu = feats2(y3, us) @ W2 * SC2 + GW.population(y3[0])
                    r = res2[rng.integers(0, len(res2), n_samples)] * SC2
                arr.append(mu[None] + r)
            out[l] = np.stack(arr, 1)
        return out
    return predict


def train_sims(thetas, sec):
    """Training runs for the ridge predictors: J_TR members per theta, init + burn-in, then N_CH chunks of
    CH_TR ticks, each starting with a program of class b, c or d (equal odds; class a adds no wind
    information) built from the member's current observation."""
    RN = GW.Runner()
    B = len(thetas) * J_TR
    P = GW.stack_params([GW.theta_to_params(th) for th in thetas for _ in range(J_TR)])
    k = sec.keys(B, "train-init")
    sig = jnp.full((B,), SIG)
    A, m = RN.init_burn(P, k, sig)
    kd = GW.dyn_keys(k)
    Ys, Us = [], []
    y_last = np.asarray(jax.vmap(RN.obs)(A, m))
    t = 0
    for c in range(N_CH):
        U = np.zeros((B, CH_TR, GW.NW))
        for b in range(B):
            rng = sec.rng("train-prog", b, c)
            cl = ("b", "c", "d")[int(rng.integers(0, 3))]
            prog = MIX.classes[cl](rng, y_last[b][None], CH_TR, EP_CAP)
            U[b] = program_dense(prog, CH_TR, GW.NW)
        y, ext, glob, A, m = RN.run(P, A, m, kd, jnp.full((B,), t, jnp.int64), jnp.asarray(U), sig)
        y = np.asarray(y)
        Ys.append(y if c == 0 else y[:, 1:])
        Us.append(U)
        y_last = y[:, -1]
        t += CH_TR
    CLOCK["member_ticks"] += B * (GW.BURN + N_CH * CH_TR)
    Y = np.concatenate(Ys, 1)
    U = np.concatenate(Us, 1)
    return Y.reshape(len(thetas), J_TR, *Y.shape[1:]), U.reshape(len(thetas), J_TR, *U.shape[1:])


# ----------------------------------------------------------------------------- Lab smoke test
def lab_smoke(world, sec):
    lab = Lab(world, sec.child("lab"), nats=budget(total=150.0), max_ticks=60)
    out = {"card_keys": sorted(lab.card().keys())}
    o0 = lab.reset("episode-1")
    u = np.zeros(GW.NW); u[5] = 0.2                                    # 8 nats
    o1 = lab.step({5: 0.2})
    out["o_shape"] = list(o0.shape)
    out["step_changed_obs"] = bool(np.abs(o1 - o0).max() > 0)
    rej = {}
    try:
        lab.step({j: 0.5 for j in range(4)})                           # 200 nats > tick cap
    except InputViolation as e:
        rej["tick_cap"] = str(e)
    try:
        lab.run([(t, {7: 0.6}) for t in range(4)], [4])                # 72 nats per tick, 288 > episode... total cap
    except InputViolation as e:
        rej["program_cap"] = str(e)
    try:
        lab.run([], [100])
    except BudgetExhausted as e:
        rej["max_ticks"] = str(e)
    out["rejections"] = rej
    out["usage"] = lab.usage()
    CLOCK["member_ticks"] += GW.BURN + 1 + 1
    return out


# ----------------------------------------------------------------------------- truth draws
def draw_truths(names, lo, hi, n, sec, extra=3):
    """Prior = uniform box conditioned on the public viability rule (viab_joint.viability, one member,
    50 + 100 ticks, no input): candidates drawn from the box in order, the first n viable ones kept
    (EXAM section 2, selection on world-level properties with public code). Smoke mode skips the check."""
    rng = sec.rng("truth-draws")
    cand = [lo + (hi - lo) * rng.random(len(names)) for _ in range(n + (0 if SMOKE else extra))]
    if SMOKE:
        return cand[:n], {"checked": False}
    import viab_joint as VJ
    rows, _ = VJ.viability(names, cand, sec.keys(len(cand), "viability"))
    CLOCK["member_ticks"] += len(cand) * (GW.BURN + VJ.T)
    acc = [c for c, r in zip(cand, rows) if r["viable"]][:n]
    if len(acc) < n:
        raise RuntimeError("draw_truths: too few viable candidates")
    log("truth draws", [r["viable"] for r in rows])
    return acc, {"checked": True, "candidates": rows, "n_candidates": len(cand),
                 "n_viable": int(sum(r["viable"] for r in rows))}


# ----------------------------------------------------------------------------- main
def main():
    n_truth = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    names, lo, hi = load_prior()
    mean = (lo + hi) / 2
    sec = secret()
    th0 = theta_dict(names, mean)
    out_f = os.path.join(RES, f"{TAG}.json")
    out = json.load(open(out_f)) if os.path.exists(out_f) else {}
    if "truth_draws" in out:
        truths = [np.array(t) for t in out["truths"]]
    else:
        truths, out["truth_draws"] = draw_truths(names, lo, hi, n_truth, sec)
    out.update({"hidden": names, "prior_lo": lo.tolist(), "prior_hi": hi.tolist(), "prior_mean": mean.tolist(),
                "truths": [t.tolist() for t in truths], "design": {
                    "P": P_PRE, "queries": QUERIES, "R": R_TRUTH, "n_items_per_truth": N_ITEMS, "n_clim": N_CLIM,
                    "m_plugin": M_PLUG, "m_ridge": M_RIDGE, "tick_cap": TICK_CAP, "episode_cap": EP_CAP,
                    "C_aimed": C_AIM, "C_regional": C_REG, "sigma_w": SIG, "ridge_train": {
                        "members_per_theta": J_TR, "ticks": CH_TR * N_CH, "burn_in": GW.BURN}},
                "secret_commitment": sec.commitment()})
    world = build_world(GW.theta_to_params(th0))
    nb = budget()
    if "lab_smoke" not in out:
        out["lab_smoke"] = lab_smoke(world, sec)
        log("lab smoke", out["lab_smoke"])
    # ridge training sims (theta_0 and every truth): one batched call
    tr_f = os.path.join(RES, f"{TAG}_train.npz")
    if os.path.exists(tr_f):
        z = np.load(tr_f)
        Ytr, Utr = z["Y"].astype(float), z["U"].astype(float)
    else:
        t1 = time.time()
        Ytr, Utr = train_sims([th0] + [theta_dict(names, t) for t in truths], sec.child("train"))
        np.savez_compressed(tr_f, Y=Ytr.astype(np.float32), U=Utr.astype(np.float32))
        out["train_seconds"] = time.time() - t1
        log("training sims", Ytr.shape, round(time.time() - t1, 1), "s")
    hs = sorted(set(QUERIES[1]) | set(QUERIES[2]))
    ridge0 = fit_ridge(Ytr[0], Utr[0], hs)
    per = out.get("per_truth", {})
    all_scores = {}
    sc_f = os.path.join(RES, f"{TAG}_scores.npz")
    if os.path.exists(sc_f):
        z = np.load(sc_f, allow_pickle=True)
        all_scores = z["scores"].item()
    for i, tv in enumerate(truths):
        if str(i) in per:
            continue
        t1 = time.time()
        th = theta_dict(names, tv)
        pth = GW.theta_to_params(th)
        world.params = pth
        ex = GExam(world, sec.child("truth", i), MIX, n_items=N_ITEMS, prefix=P_PRE, queries=QUERIES, R=R_TRUTH,
                   derived={1: GW.coarse, 2: GW.population}, scales={1: SC["level1"], 2: SC2}, nats=nb,
                   n_clim=N_CLIM, name="pilot")
        CLOCK["member_ticks"] += N_ITEMS * (GW.BURN + P_PRE) + N_ITEMS * R_TRUTH * HMAX + N_CLIM * (GW.BURN + HMAX)
        t_ex = time.time() - t1
        log("truth", i, th, "exam built", round(t_ex, 1), "s")
        S_true = plugin_samples(ex, world, pth, M_PLUG, sec.keys(N_ITEMS * M_PLUG, "plugin-true", i))
        S_prior = plugin_samples(ex, world, GW.theta_to_params(th0), M_PLUG, sec.keys(N_ITEMS * M_PLUG, "plugin-prior", i))
        world.params = pth
        log("plug-ins done")
        ridge_t = fit_ridge(Ytr[1 + i], Utr[1 + i], hs)
        ridge_t_na = fit_ridge(Ytr[1 + i], Utr[1 + i], hs, act=False)
        scored = {"plugin_true": ex.score(ex.collect(table_predictor(ex, S_true), M_PLUG, 0)),
                  "plugin_prior": ex.score(ex.collect(table_predictor(ex, S_prior), M_PLUG, 0)),
                  "ridge_true": ex.score(ex.collect(ridge_predictor(ridge_t), M_RIDGE, 0)),
                  "ridge_prior": ex.score(ex.collect(ridge_predictor(ridge0), M_RIDGE, 0)),
                  "ridge_true_noact": ex.score(ex.collect(ridge_predictor(ridge_t_na, act=False), M_RIDGE, 0))}
        refs = ex.references()
        rep = ex.report(scored, key="es", refs=refs)
        gaps = {f"{a}-{b}{('_' + md) if md else ''}": paired_gap(rep, a, b, md)
                for a, b in (("plugin_true", "plugin_prior"), ("ridge_true", "ridge_prior"),
                             ("ridge_true", "ridge_true_noact")) for md in ("", "pooled")}
        nats = [NatsAccountant(nb).check_program(it.program) for it in ex.items]
        per[str(i)] = {"theta": th, "report": public_report(rep), "gaps": gaps, "classes": ex.classes.tolist(),
                       "program_nats": nats, "cells": [list(c) for c in ex.cells], "seconds": time.time() - t1,
                       "seconds_exam_build": t_ex}
        all_scores[str(i)] = {"refs": {k: v["es"] for k, v in refs.items()},
                              "scored": {k: v["es"] for k, v in scored.items()}, "classes": ex.classes}
        out["per_truth"] = per
        out["member_ticks_so_far"] = CLOCK["member_ticks"]
        json.dump(out, open(out_f + ".tmp", "w"), indent=1, default=float)
        os.replace(out_f + ".tmp", out_f)
        np.savez_compressed(sc_f, scores=np.array(all_scores, dtype=object))
        a = rep["aggregate"]
        log("truth", i, {k: round(v, 3) for k, v in a.items()}, "valid", rep["valid"])
        log("gaps", {k: (round(v["gap"], 3), round(v["z"], 1)) for k, v in gaps.items()})
        del ex
    # pooled over truths
    keys = list(all_scores[next(iter(all_scores))]["scored"])
    S = {"climatology": np.concatenate([all_scores[k]["refs"]["climatology"] for k in sorted(all_scores)]),
         "oracle": np.concatenate([all_scores[k]["refs"]["oracle"] for k in sorted(all_scores)])}
    for k in keys:
        S[k] = np.concatenate([all_scores[t]["scored"][k] for t in sorted(all_scores)])
    groups = np.concatenate([all_scores[k]["classes"] for k in sorted(all_scores)])
    cols = ~np.isnan(S["oracle"]).any(0)
    S = {k: v[:, cols] for k, v in S.items()}
    cells = [c for c, ok in zip(per["0"]["cells"], cols) if ok]
    rep = skill_report(S, cells=cells, groups=groups)
    out["pooled"] = {"n_items": int(S["oracle"].shape[0]), "report": public_report(rep),
                     "gaps": {f"{a}-{b}{('_' + md) if md else ''}": paired_gap(rep, a, b, md)
                              for a, b in (("plugin_true", "plugin_prior"), ("ridge_true", "ridge_prior"),
                                           ("ridge_true", "ridge_true_noact")) for md in ("", "pooled")}}
    out["member_ticks_total_this_run"] = CLOCK["member_ticks"]
    out["wall_seconds_this_run"] = time.time() - CLOCK["t0"]
    json.dump(out, open(out_f + ".tmp", "w"), indent=1, default=float)
    os.replace(out_f + ".tmp", out_f)
    log("pooled", {k: round(v, 3) for k, v in rep["aggregate"].items()})
    log("pooled gaps", out["pooled"]["gaps"])


if __name__ == "__main__":
    main()
