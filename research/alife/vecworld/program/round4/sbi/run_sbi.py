"""run_sbi -- round 4, study sbi (track 2): simulate-to-train on the gliders exam world (GPU job).

PILOT ONLY: the hidden parameters of the truths are drawn fresh inside the job from the public prior and
written to the outputs, so these truths, Lab data and exam items must NEVER be reused as an exam.
The real-world secret (256 bits, os.urandom) is never written; only its commitment is.

Stages (each saves its outputs to --out as it finishes; progress in OUT/progress.txt):
  B truths       16 candidates from the prior box (secret rng) through the public viability rule
                 (viab_joint.viability, 50 + 100 ticks, no input); the first 8 viable are the truths.
  C prior        viability rule at 1,024 box draws -> logistic p_v(theta) (the conditioned prior density).
  D design       2,048 box draws x 4 exam-shaped episodes (the agent's own simulator) -> summaries.
  E Lab          per truth, a BatchLab (vw.harness.Lab, secret keys, nats caps tick 100 / episode 400 /
                 total 400 per episode, tick cap 33 per episode) runs 512 exam-shaped episodes: reset,
                 16 ticks without input, a test program from the public mix built from o(16), 16 ticks.
                 Budgets are the nested prefixes of 2, 8, 32, 128, 512 episodes (66 ... 16,896 ticks).
  F identify     synthetic likelihood on linear-regression summaries (4 numbers per episode, averaged over
                 the budget's episodes) with a cubic emulator + emulator / misfit variance; posterior by
                 importance sampling under p_v; contraction and coverage per budget.
  G exams        per truth a GExam (pilot's HistoryExam): 64 items, P = 16, level 1 (coarse) at h = 1, 2,
                 4, 8, 16 and level 2 (population) at h = 8, 16, R = 16 replicate truths, 128 climatology runs.
  H predictors   two classes (pilot's ridge; an energy-score conv net), each trained on
                 (a) real@n: the Lab's first n episodes; (b) post@n: 1,024 simulated episodes at posterior
                 draws; (c) prior_mean: at the box centre; (d) true: at the truth; (p) prior_pred: at draws
                 from the conditioned prior (no real data). Optional: one theta-conditioned net on the design
                 episodes (amortised), evaluated at the same theta choices.
  I scores       oracle-normalised fair energy skill (vw.scoring.skill_report), pooled over truths and per
                 truth; paired gaps.
usage: python -B run_sbi.py --out DIR [--smoke] [--max-hours 2.6]
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import sys
import time
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sbi_lib as SL  # noqa: E402
import sbi_net as NN  # noqa: E402

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

import viab_joint as VJ  # noqa: E402
from vw.secret import Secret  # noqa: E402
from vw.world import make_key, member_keys  # noqa: E402
from vw.scoring import energy_fair, paired_gap, public_report, skill_report  # noqa: E402

GW, PL = SL.GW, SL.PL

ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
ap.add_argument("--smoke", action="store_true", help="tiny sizes for a CPU test of the code path")
ap.add_argument("--max-hours", type=float, default=2.6, help="wall-clock guard: later groups are skipped")
ap.add_argument("--no-amortised", action="store_true")
args = ap.parse_args()
OUT = args.out
os.makedirs(OUT, exist_ok=True)
T0 = time.time()

FULL = dict(P=16, H=16, burn=GW.BURN, n_cand=16, n_truth=8, N_v=1024, v_chunk=512, N_theta=2048, K=4,
            budgets=[2, 8, 32, 128, 512], lab_chunk=128, n_items=64, R=16, n_clim=128, N_sim=1024, chunk=256,
            m=32, steps_real={2: 600, 8: 1000, 32: 1500, 128: 2500, 512: 3000}, steps_sim=3000, steps_amort=6000,
            queries={1: [1, 2, 4, 8, 16], 2: [8, 16]}, lags=(0, 1, 2, 4, 8), hs=(1, 2, 4, 8, 16), viab_T=100,
            n_post_draws=1000)
SMOKE = dict(P=4, H=4, burn=2, n_cand=4, n_truth=2, N_v=4, v_chunk=4, N_theta=8, K=2, budgets=[2, 4], lab_chunk=4,
             n_items=4, R=3, n_clim=4, N_sim=4, chunk=4, m=4, steps_real={2: 20, 4: 20}, steps_sim=20,
             steps_amort=20, queries={1: [1, 2, 4], 2: [4]}, lags=(0, 1, 2, 4), hs=(1, 2, 4), viab_T=6,
             n_post_draws=200)
CFG = SMOKE if args.smoke else FULL
P, H = CFG["P"], CFG["H"]
NN.Cfg.LAGS, NN.Cfg.HS = tuple(CFG["lags"]), tuple(CFG["hs"])
if args.smoke:
    NN.Cfg.EVAL_EVERY = 10
VJ.T = CFG["viab_T"]
QUERIES = CFG["queries"]
HS1, HS2 = QUERIES[1], QUERIES[2]
CLOCK = {"member_ticks": {}}
FAILED = []
STATE = {}


def log(msg):
    line = f"{time.strftime('%H:%M:%S')} [{(time.time() - T0) / 60:6.1f} min] {msg}"
    print(line, flush=True)
    with open(os.path.join(OUT, "progress.txt"), "a") as f:
        f.write(line + "\n")


def jdump(name, obj):
    def conv(o):
        if isinstance(o, (np.floating, np.integer)):
            return o.item()
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, np.bool_):
            return bool(o)
        return str(o)
    p = os.path.join(OUT, name)
    with open(p + ".tmp", "w") as f:
        json.dump(obj, f, indent=1, default=conv)
    os.replace(p + ".tmp", p)


def ticks(stage, n):
    CLOCK["member_ticks"][stage] = CLOCK["member_ticks"].get(stage, 0) + int(n)


def hours():
    return (time.time() - T0) / 3600


def stage(name):
    def deco(fn):
        def run(*a, **kw):
            t = time.time()
            log(f"== stage {name}")
            try:
                r = fn(*a, **kw)
                log(f"== stage {name} done in {time.time() - t:.0f}s")
                return r
            except Exception as exc:
                FAILED.append(name)
                log(f"== stage {name} FAILED: {exc!r}\n{traceback.format_exc()}")
                raise
        return run
    return deco


# ----------------------------------------------------------------------------- setup
INFO = {"study": "round4/sbi", "pilot_never_reusable_as_exam": True,
        "versions": {"python": platform.python_version(), "jax": jax.__version__, "numpy": np.__version__},
        "backend": jax.default_backend(), "devices": [str(d) for d in jax.devices()], "smoke": args.smoke,
        "config": {k: (v if not isinstance(v, dict) else {str(a): b for a, b in v.items()}) for k, v in CFG.items()},
        "prior": {"names": SL.NAMES, "lo": SL.LO.tolist(), "hi": SL.HI.tolist(),
                  "rule": "uniform box conditioned on viab_joint.viability (gliders_exam results/prior.json)"},
        "net": {k: getattr(NN.Cfg, k) for k in dir(NN.Cfg) if k.isupper()}}
log(f"backend {INFO['backend']} devices {INFO['devices']} jax {jax.__version__} smoke={args.smoke}")
SEC = Secret()
INFO["secret_commitment"] = SEC.commitment()
jdump("info.json", INFO)
RN = SL.VRunner(burn=CFG["burn"])
MIXN = list(PL.MIX.classes)


# ----------------------------------------------------------------------------- B truths
@stage("B truths")
def stage_truths():
    n = CFG["n_cand"]
    rng = SEC.rng("truth-draws")
    cand = SL.LO + (SL.HI - SL.LO) * rng.random((n, 4))
    rows, _ = VJ.viability(SL.NAMES, cand, SEC.keys(n, "viability"), RN=RN)
    ticks("truths", n * (CFG["burn"] + VJ.T))
    ok = [r["viable"] for r in rows]
    truths = [c for c, v in zip(cand, ok) if v][:CFG["n_truth"]]
    forced = False
    if len(truths) < CFG["n_truth"]:
        if not args.smoke:
            raise RuntimeError(f"only {len(truths)} viable candidates")
        truths = list(cand[:CFG["n_truth"]])
        forced = True
    out = {"PILOT_NEVER_REUSE_AS_EXAM": True, "names": SL.NAMES, "candidates": rows,
           "n_viable": int(sum(ok)), "truths": [t.tolist() for t in truths], "forced_smoke": forced,
           "secret_commitment": SEC.commitment(),
           "note": "truths drawn inside the job from the public prior (box + viability rule, first viable "
                   "candidates in draw order); the secret is not stored"}
    jdump("truths.json", out)
    log(f"truths {np.round(truths, 4).tolist()} ({sum(ok)}/{n} viable)")
    return np.array(truths)


# ----------------------------------------------------------------------------- C viability prior
@stage("C viability prior")
def stage_viability():
    N = CFG["N_v"]
    rng = np.random.default_rng(4401)
    U = rng.uniform(-1, 1, (N, 4))
    th = SL.from_u(U)
    rows = []
    for s in range(0, N, CFG["v_chunk"]):
        e = min(s + CFG["v_chunk"], N)
        r, _ = VJ.viability(SL.NAMES, th[s:e], member_keys(make_key(4401, s), e - s), RN=RN)
        rows += r
        log(f"  viability {e}/{N}")
    ticks("viability_design", N * (CFG["burn"] + VJ.T))
    y = np.array([r["viable"] for r in rows], float)
    pv = SL.ViabilityPrior().fit(U, y)
    keys = ["count_mean", "count_min", "speed_median", "frac_ticks_at_slot_cap", "mass_median", "rg_median"]
    np.savez_compressed(os.path.join(OUT, "viability_design.npz"), u=U, viable=y,
                        **{k: np.array([r[k] for r in rows], float) for k in keys})
    jdump("viability_prior.json", {"diag": pv.diag, "w": pv.w.tolist(), "features": "poly_feats(u, 2)"})
    log(f"viability design: {y.mean():.3f} viable; {pv.diag}")
    rng = np.random.default_rng(4404)
    ub = rng.uniform(-1, 1, (200_000, 4))
    wb = np.exp(pv.logp(ub))
    wb /= wb.sum()
    prior_draws = ub[rng.choice(len(ub), size=4 * CFG["N_sim"], p=wb)]
    return pv, prior_draws


# ----------------------------------------------------------------------------- D design
@stage("D design")
def stage_design():
    N, K = CFG["N_theta"], CFG["K"]
    rng = np.random.default_rng(4402)
    U = rng.uniform(-1, 1, (N, 4))
    th = np.repeat(SL.from_u(U), K, 0)
    sim = SL.sim_episodes(RN, th, member_keys(make_key(4402, 0), N * K), 4402, P, H, CFG["chunk"],
                          log=log if not args.smoke else None)
    ticks("design", N * K * (CFG["burn"] + P + H))
    F = SL.episode_features(sim["obs"])
    np.savez_compressed(os.path.join(OUT, "design_features.npz"), u=U, F=F.reshape(N, K, -1).astype(np.float32),
                        cls=sim["cls"].reshape(N, K), nats=sim["nats"].reshape(N, K), features=np.array(SL.FEATURES))
    return U, F.reshape(N, K, -1), sim


# ----------------------------------------------------------------------------- E Lab
@stage("E Lab")
def stage_lab(world, truths):
    nmax = max(CFG["budgets"])
    per_ep = 1 + P + H
    out, labdata = [], []
    for i, th in enumerate(truths):
        world.params = GW.theta_to_params(dict(zip(SL.NAMES, th)))
        lab = SL.BatchLab(world, SEC.child("lab", i), nats=PL.budget(total=SL.EP_CAP * nmax), max_ticks=nmax * per_ep)
        arng = np.random.default_rng([7700, i])                 # the agent's own program choices
        classes = arng.choice(MIXN, size=nmax)
        obs, U, nats = [], [], []
        for s in range(0, nmax, CFG["lab_chunk"]):
            e = min(s + CFG["lab_chunk"], nmax)

            def mk(j, hist, s=s):
                return PL.MIX.classes[classes[s + j]](np.random.default_rng([7701, i, s + j]), hist, H, SL.EP_CAP)
            r = lab.run_batch(list(range(s, e)), P, H, mk)
            obs.append(r["obs"])
            U.append(r["U"])
            nats.append(r["nats"])
        obs, U, nats = np.concatenate(obs), np.concatenate(U), np.concatenate(nats)
        ticks("lab_charged", nmax * per_ep)
        ticks("lab_burn_in_designer", nmax * CFG["burn"])
        F = SL.episode_features(obs)
        usage = lab.usage()
        cum = np.cumsum(nats)
        per_b = {str(n): {"episodes": n, "ticks": n * per_ep, "nats": float(cum[n - 1]),
                          "classes": {c: int((classes[:n] == c).sum()) for c in MIXN}} for n in CFG["budgets"]}
        out.append({"truth": i, "usage_final": usage, "per_budget": per_b,
                    "caps": {"max_ticks": nmax * per_ep, "nats_total": SL.EP_CAP * nmax, "nats_episode": SL.EP_CAP,
                             "nats_tick": PL.TICK_CAP}})
        labdata.append({"obs": obs, "U": U, "F": F, "cls": classes, "nats": nats})
        log(f"  Lab truth {i}: {usage}")
    jdump("lab.json", out)
    np.savez_compressed(os.path.join(OUT, "lab_features.npz"), F=np.stack([d["F"] for d in labdata]).astype(np.float32),
                        cls=np.stack([d["cls"] for d in labdata]), nats=np.stack([d["nats"] for d in labdata]))
    return labdata


# ----------------------------------------------------------------------------- F identification
@stage("F identification")
def stage_identify(Ud, Fd, labdata, truths, pv, prior_draws):
    N, K, nf = Fd.shape
    proj = SL.Projection().fit(Fd.reshape(N * K, nf), np.repeat(Ud, K, 0))
    S = proj(Fd.reshape(N * K, nf)).reshape(N, K, -1)
    em = SL.Emulator().fit(Ud, S)
    rng = np.random.default_rng(4403)
    # prior moments (box draws weighted by p_v)
    ub = rng.uniform(-1, 1, (200_000, 4))
    wb = np.exp(pv.logp(ub))
    wb /= wb.sum()
    pm = wb @ ub
    psd = np.sqrt(wb @ (ub - pm) ** 2)
    res, draws = [], {}
    for i, th in enumerate(truths):
        ut = SL.to_u(th)
        for n in CFG["budgets"]:
            sbar = proj(labdata[i]["F"][:n]).mean(0)
            post = SL.posterior(em, pv, sbar, n, rng)
            chk = SL.posterior_checks(post, em, pv, sbar, n, ut)
            draws[(i, n)] = post["u"]
            r = {"truth": i, "n_episodes": n, "ticks": n * (1 + P + H), "ess": post["ess"],
                 "ess_stages": post["ess_stages"], "post_mean_theta": SL.from_u(post["mean_u"]).tolist(),
                 "post_sd_theta": (post["sd_u"] * SL.HW_).tolist(), "contraction_sd_ratio": (post["sd_u"] / psd).tolist(),
                 "abs_err_over_prior_sd": (np.abs(post["mean_u"] - ut) / psd).tolist(), **chk}
            res.append(r)
            log(f"  truth {i} n={n}: sd/prior {np.round(post['sd_u'] / psd, 3).tolist()} pit "
                f"{np.round(chk['pit'], 2).tolist()} hpd {chk['hpd_level']:.2f} ess {post['ess']:.0f}")
    # coverage per budget (marginal central intervals, HPD level of the truth)
    cov = {}
    for n in CFG["budgets"]:
        rr = [r for r in res if r["n_episodes"] == n]
        cov[str(n)] = {"in50_frac": float(np.mean([r["in50"] for r in rr])),
                       "in90_frac": float(np.mean([r["in90"] for r in rr])),
                       "hpd_le_50_frac": float(np.mean([r["hpd_level"] <= 0.5 for r in rr])),
                       "hpd_le_90_frac": float(np.mean([r["hpd_level"] <= 0.9 for r in rr])),
                       "contraction_mean": np.mean([r["contraction_sd_ratio"] for r in rr], 0).tolist(),
                       "abs_err_over_prior_sd_mean": np.mean([r["abs_err_over_prior_sd"] for r in rr], 0).tolist(),
                       "n_truths": len(rr)}
    out = {"method": "Gaussian synthetic likelihood on 4 linear-regression summaries per episode (mean over the "
                     "budget's episodes); cubic emulator + emulator and CV-misfit covariance; importance sampling "
                     "under the viability prior p_v",
           "projection": proj.state(), "emulator": em.diag, "prior_mean_u": pm.tolist(), "prior_sd_u": psd.tolist(),
           "prior_sd_theta": (psd * SL.HW_).tolist(), "per_truth_budget": res, "coverage": cov}
    jdump("identification.json", out)
    np.savez_compressed(os.path.join(OUT, "posterior_draws.npz"),
                        **{f"t{i}_n{n}": SL.from_u(d[:CFG["n_post_draws"]]).astype(np.float32)
                           for (i, n), d in draws.items()},
                        prior=SL.from_u(prior_draws[:CFG["n_post_draws"]]).astype(np.float32))
    for n in CFG["budgets"]:
        log(f"  coverage n={n}: {cov[str(n)]}")
    return draws


# ----------------------------------------------------------------------------- G exams
@stage("G exams")
def stage_exams(world, truths):
    exams, refs = [], []
    for i, th in enumerate(truths):
        world.params = GW.theta_to_params(dict(zip(SL.NAMES, th)))
        ex = PL.GExam(world, SEC.child("truth", i), PL.MIX, n_items=CFG["n_items"], prefix=P, queries=QUERIES,
                      R=CFG["R"], derived={1: GW.coarse, 2: GW.population}, scales={1: PL.SC["level1"], 2: PL.SC2},
                      nats=PL.budget(), n_clim=CFG["n_clim"], name="sbi-pilot")
        n = CFG["n_items"]
        ticks("exam", n * (CFG["burn"] + P) + n * CFG["R"] * ex.H + CFG["n_clim"] * (CFG["burn"] + ex.H))
        ex._snap = None
        exams.append(ex)
        refs.append(ex.references())
        log(f"  exam truth {i}: classes {dict(zip(*np.unique(ex.classes, return_counts=True)))}")
    return exams, refs


# ----------------------------------------------------------------------------- H predictors and scores
SCORES = {}          # SCORES[i][name] = es (n_items, n_cells)
TRAIN = {}


def table(ex, samples):
    ids = [it.id for it in ex.items]
    return lambda item, n, seed: samples[ids.index(item["id"])]


def score(i, name, samples, exams):
    ex = exams[i]
    smp = ex.collect(table(ex, samples), CFG["m"], 0)                      # format checks
    SCORES.setdefault(i, {})[name] = ex._per_cell(lambda X, Y, s, l: energy_fair(X, Y, s), samples=smp)


def save_scores(exams, refs):
    blob = {}
    for i in SCORES:
        for k, v in SCORES[i].items():
            blob[f"t{i}|{k}"] = v
        blob[f"t{i}|oracle"] = refs[i]["oracle"]["es"]
        blob[f"t{i}|climatology"] = refs[i]["climatology"]["es"]
        blob[f"t{i}|classes"] = exams[i].classes
    np.savez_compressed(os.path.join(OUT, "scores.npz"), **blob)
    jdump("train_info.json", TRAIN)


def ridge_and_score(i_list, name, data_list, exams):
    hs = sorted(set(HS1) | set(HS2))
    for i, d in zip(i_list, data_list):
        model = SL.fit_ridge(d["obs"], d["U"], hs)
        items = exams[i].public()
        pred = PL.ridge_predictor(model)
        samples = [pred(it, CFG["m"], 0) for it in items]
        score(i, f"ridge|{name}", samples, exams)


def nets_and_score(i_list, name, data_list, exams, steps, seed):
    ds = [NN.make_dataset(d["obs"], d["U"], seed=seed + k) for k, d in enumerate(data_list)]
    params, info = NN.train_nets(ds, cond=False, steps=steps, seed=seed, log=log, tag=f"[{name}]")
    TRAIN[name] = info
    for k, i in enumerate(i_list):
        samples = NN.net_samples(params[k], exams[i].public(), CFG["m"], seed + 100 + i, HS1, HS2)
        score(i, f"net|{name}", samples, exams)
    return params


def sims_for(thetas, seed, tag):
    sim = SL.sim_episodes(RN, thetas, member_keys(make_key(5500, seed), len(thetas)), 5500 + seed, P, H, CFG["chunk"])
    ticks(f"sims_{tag}", len(thetas) * (CFG["burn"] + P + H))
    return {"obs": sim["obs"], "U": sim["U"]}


def report(exams, refs, final=False):
    try:
        return _report(exams, refs, final)
    except Exception as exc:
        log(f"  report failed: {exc!r}")
        return None


def _report(exams, refs, final=False):
    names = sorted(set.intersection(*[set(SCORES[i]) for i in SCORES]))
    tr = sorted(SCORES)
    S = {"climatology": np.concatenate([refs[i]["climatology"]["es"] for i in tr]),
         "oracle": np.concatenate([refs[i]["oracle"]["es"] for i in tr])}
    for k in names:
        S[k] = np.concatenate([SCORES[i][k] for i in tr])
    groups = np.concatenate([exams[i].classes for i in tr])
    cols = ~np.isnan(S["oracle"]).any(0)
    S = {k: v[:, cols] for k, v in S.items()}
    cells = [c for c, ok in zip(exams[0].cells, cols) if ok]
    rep = skill_report(S, cells=cells, groups=groups, n_boot=2000)
    per_truth = {}
    for i in tr:
        Si = {"climatology": refs[i]["climatology"]["es"][:, cols], "oracle": refs[i]["oracle"]["es"][:, cols]}
        Si.update({k: SCORES[i][k][:, cols] for k in names})
        try:
            ri = skill_report(Si, cells=cells, valid=np.asarray(rep["valid"]), n_boot=200)
            per_truth[str(i)] = ri["aggregate"]
        except Exception as exc:
            per_truth[str(i)] = {"error": repr(exc)}
    gaps = {}
    for cl in ("ridge", "net"):
        def g(a, b):
            if a in rep["aggregate"] and b in rep["aggregate"]:
                key = f"{a} - {b}"
                pg = paired_gap(rep, a, b)
                d = [per_truth[t][a] - per_truth[t][b] for t in per_truth if a in per_truth[t]]
                pg["truth_mean"] = float(np.mean(d))
                pg["truth_se"] = float(np.std(d, ddof=1) / np.sqrt(len(d))) if len(d) > 1 else float("nan")
                pg["n_truths"] = len(d)
                gaps[key] = pg
        for n in CFG["budgets"]:
            g(f"{cl}|post@{n}", f"{cl}|real@{n}")
            g(f"{cl}|true", f"{cl}|post@{n}")
            g(f"{cl}|post@{n}", f"{cl}|prior_mean")
            g(f"{cl}|post@{n}", f"{cl}|prior_pred")
            g(f"{cl}|real@{n}", f"{cl}|prior_pred")
            g(f"{cl}|true", f"{cl}|real@{n}")
        g(f"{cl}|true", f"{cl}|prior_mean")
        g(f"{cl}|prior_pred", f"{cl}|prior_mean")
    for n in CFG["budgets"]:
        for a, b in ((f"net|post@{n}", f"ridge|post@{n}"), (f"net|real@{n}", f"ridge|real@{n}"),
                     (f"amort|post@{n}", f"net|post@{n}")):
            if a in rep["aggregate"] and b in rep["aggregate"]:
                gaps[f"{a} - {b}"] = paired_gap(rep, a, b)
    out = {"final": final, "truths_scored": tr, "n_items_pooled": int(S["oracle"].shape[0]), "cells": cells,
           "report": public_report(rep), "per_truth_aggregate": per_truth, "gaps": gaps,
           "member_ticks": CLOCK["member_ticks"], "hours": hours(), "failed": FAILED}
    jdump("prediction.json", out)
    agg = rep["aggregate"]
    log("  OES " + ", ".join(f"{k} {agg[k]:.3f}" for k in sorted(agg)))
    return out


# ----------------------------------------------------------------------------- main
def group(name, fn):
    t = time.time()
    try:
        fn()
        log(f"  group {name} done in {time.time() - t:.0f}s")
        return time.time() - t
    except Exception as exc:
        FAILED.append(f"group {name}")
        log(f"  group {name} FAILED: {exc!r}\n{traceback.format_exc()}")
        return None


def main():
    truths = stage_truths()
    pv, prior_draws = stage_viability()
    Ud, Fd, design_sim = stage_design()
    world = SL.build_world(GW.theta_to_params(dict(zip(SL.NAMES, truths[0]))), burn=CFG["burn"])
    labdata = stage_lab(world, truths)
    try:
        draws = stage_identify(Ud, Fd, labdata, truths, pv, prior_draws)
    except Exception:
        draws = None
    exams, refs = stage_exams(world, truths)
    nT = len(truths)
    I = list(range(nT))
    budgets = CFG["budgets"]
    N = CFG["N_sim"]
    est = {"sim": 0.2}

    def guard(what, need_h):
        if hours() + need_h > args.max_hours:
            log(f"  SKIP {what}: {hours():.2f} h used, {need_h:.2f} h estimated, guard {args.max_hours} h")
            FAILED.append(f"skipped {what}")
            return False
        return True

    # (a) real data, per budget
    for n in budgets:
        def g_real(n=n):
            data = [{"obs": labdata[i]["obs"][:n], "U": labdata[i]["U"][:n]} for i in I]
            ridge_and_score(I, f"real@{n}", data, exams)
            nets_and_score(I, f"real@{n}", data, exams, CFG["steps_real"][n], seed=100 + n)
            save_scores(exams, refs)
        group(f"real@{n}", g_real)
    report(exams, refs)

    # (d) true theta
    def g_true():
        data = [sims_for(np.repeat(truths[i][None], N, 0), 10 + i, "true") for i in I]
        ridge_and_score(I, "true", data, exams)
        nets_and_score(I, "true", data, exams, CFG["steps_sim"], seed=200)
        save_scores(exams, refs)
    dt = group("true", g_true)
    if dt:
        est["sim"] = dt / 3600

    # (c) prior mean and (p) prior predictive
    def g_prior():
        shared = {"prior_mean": sims_for(np.repeat(SL.CEN[None], N, 0), 30, "prior_mean"),
                  "prior_pred": sims_for(SL.from_u(prior_draws[:N]), 31, "prior_pred")}
        for name, d in shared.items():
            ridge_and_score(I, name, [d] * nT, exams)
        ds = [NN.make_dataset(d["obs"], d["U"], seed=300 + k) for k, d in enumerate(shared.values())]
        params, info = NN.train_nets(ds, cond=False, steps=CFG["steps_sim"], seed=300, log=log, tag="[prior]")
        TRAIN["prior_mean+prior_pred"] = info
        for k, name in enumerate(shared):
            for i in I:
                score(i, f"net|{name}", NN.net_samples(params[k], exams[i].public(), CFG["m"], 400 + i, HS1, HS2),
                      exams)
        save_scores(exams, refs)
    group("prior", g_prior)
    report(exams, refs)

    # (b) posterior draws, per budget
    for n in (budgets if draws is not None else []):
        if not guard(f"post@{n}", est["sim"] * 1.1):
            continue

        def g_post(n=n):
            rng = np.random.default_rng(600 + n)
            data = [sims_for(SL.from_u(draws[(i, n)][rng.choice(len(draws[(i, n)]), N, replace=True)]),
                             1000 * n + i, f"post{n}") for i in I]
            ridge_and_score(I, f"post@{n}", data, exams)
            nets_and_score(I, f"post@{n}", data, exams, CFG["steps_sim"], seed=700 + n)
            save_scores(exams, refs)
        group(f"post@{n}", g_post)
        report(exams, refs)

    # amortised theta-conditioned net on the design episodes
    if not args.no_amortised and draws is not None and guard("amortised", 0.25):
        def g_amort():
            K = CFG["K"]
            ds = [NN.make_dataset(design_sim["obs"], design_sim["U"], theta_u=np.repeat(Ud, K, 0), seed=900)]
            params, info = NN.train_nets(ds, cond=True, steps=CFG["steps_amort"], seed=900, log=log, tag="[amort]")
            TRAIN["amortised"] = info
            m = CFG["m"]
            rng = np.random.default_rng(901)
            for i in I:
                items = exams[i].public()
                ni = len(items)
                choices = {"true": SL.to_u(truths[i]), "prior_mean": np.zeros(4),
                           "prior_pred": prior_draws[rng.choice(len(prior_draws), ni * m)].reshape(ni, m, 4)}
                for n in budgets:
                    d = draws[(i, n)]
                    choices[f"post@{n}"] = d[rng.choice(len(d), ni * m)].reshape(ni, m, 4)
                for name, th in choices.items():
                    score(i, f"amort|{name}", NN.net_samples(params[0], items, m, 950 + i, HS1, HS2, cond=True,
                                                             theta_u=th), exams)
            save_scores(exams, refs)
        group("amortised", g_amort)
    rep = report(exams, refs, final=True)
    INFO["member_ticks"] = CLOCK["member_ticks"]
    INFO["member_ticks_total"] = int(sum(CLOCK["member_ticks"].values()))
    INFO["hours"] = hours()
    INFO["failed"] = FAILED
    jdump("info.json", INFO)
    log(f"done: {INFO['member_ticks_total']} member-ticks, {hours():.2f} h, failed {FAILED}")
    return rep


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        log(f"FATAL {exc!r}\n{traceback.format_exc()}")
        INFO["fatal"] = repr(exc)
        INFO["member_ticks"] = CLOCK["member_ticks"]
        jdump("info.json", INFO)
        sys.exit(1)
    if [f for f in FAILED if not f.startswith("skipped")]:
        sys.exit(2)
