"""run_ladder -- round 5, study ladder (track 2): the reference ladder on the gliders wind world in 9 cells,
observed view {block, object, pop} x number of hidden parameters {1, 4, 8} (GPU job).

PILOT ONLY: the hidden parameters of the truths are drawn fresh inside the job from the public priors and
written to the outputs, so these truths, Lab data and exam items must NEVER be reused as an exam.
The real-world secret (256 bits, os.urandom) is never written; only its commitment is.

Per hidden set n (order 4, 8, 1; outputs under OUT/n<n>/; simulations are shared by the three views):
  C prior     the box (ladder_lib.box) through the public viability rule at N_v draws -> logistic p_v(theta).
              Declared rule: if fewer than half of the draws are viable, the boxes of parameters 5-8 shrink
              by 0.75 (at most twice) before anything else is drawn.
  B truths    candidates from the box (secret rng) through the viability rule; the first T viable.
  D design    N_theta box draws x 10 exam-shaped episodes (2 per program class a, b, c, d, e): the agent's
              own simulator. Classes a-d are the public exam mix; e is the blind twin of the aimed push c.
  E Lab       per truth a BatchLab (secret keys; nats caps tick 100 / episode 400): 512 mix episodes
              (a-d in equal shares, shuffled; budgets = nested prefixes 2, 8, 32, 128, 512) and 128 class-e.
  F identify  per view and arm (mix; passive = a; blind = e; aimed = c; regional = d): summaries of the
              view only -> linear-regression summaries -> synthetic likelihood (ladder_lib.Emulator) ->
              posterior by importance sampling under p_v; contraction and coverage per budget.
  G exams     per truth a GExam (HistoryExam): history items, R replicate truths, climatology pool; the
              three views are its levels 1, 2, 3 at h = 1, 2, 4, 8, 16. References K (climatology), O
              (oracle, leave one out) and the state-given prior-mean plug-in (simulator at the box centre
              from the hidden state).
  H nets      per view: a theta-conditioned net on the design's mix episodes (policies C, PM, P0, S(N)), an
              unconditioned net on prior-predictive simulations (P0u), unconditioned nets on the Lab's
              first N episodes (D(N), all truths in lockstep, budgets <= 32 and > 32 as two groups), and a
              ridge on them (Dr(N)).
  I scores    fair energy score per item and cell through the exam's own scorer; OES (vw.scoring) and the
              acceptance shares sigma, rho (round5/agentenv/evaluator/acceptance.py) per cell.
usage: python -B run_ladder.py --out DIR [--smoke] [--sets 4,8,1] [--max-hours 2.2] [--cpu-ok]
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
import ladder_lib as LL  # noqa: E402
import ladder_net as NN  # noqa: E402

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

import viab_joint as VJ  # noqa: E402
from vw.scoring import energy_fair, energy_loo, public_report, skill_report  # noqa: E402
from vw.secret import Secret  # noqa: E402
from vw.world import make_key, member_keys  # noqa: E402

SL, GW, PL = LL.SL, LL.GW, LL.PL
ACC = LL.load_acceptance()

ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
ap.add_argument("--smoke", action="store_true", help="tiny sizes for a test of the code path")
ap.add_argument("--sets", default="4,8,1", help="hidden-set sizes, in run order")
ap.add_argument("--max-hours", type=float, default=2.2, help="wall-clock guard: later groups are skipped")
ap.add_argument("--cpu-ok", action="store_true", help="allow a CPU backend (tests only)")
args = ap.parse_args()
OUT = args.out
os.makedirs(OUT, exist_ok=True)
T0 = time.time()
T_END = T0 + args.max_hours * 3600

# sizes: N_v and N_theta per hidden set (a 1-parameter box needs fewer design points); member-ticks per set
# about 1.9-2.3 million (r4-sbi-002 measured 1,080-1,290 member-ticks/s for these stages, 520 for exams)
FULL = dict(P=16, H=16, burn=GW.BURN, n_cand=48, n_truth=8, N_v={1: 128, 4: 512, 8: 512}, v_chunk=256,
            N_theta={1: 256, 4: 448, 8: 512}, Kc=2,
            budgets=[2, 8, 32, 128, 512], arm_budgets=[2, 8, 32, 128], n_mix=512, n_e=32, lab_chunk=128,
            n_items=36, R=12, n_clim=64, chunk=256, m=32, m_plug=8, n_scale=128,
            steps_cond=6000, steps_p0=3000, steps_real=(1200, 2500), real_split=32, hs=(1, 2, 4, 8, 16),
            lags=(0, 1, 2, 4, 8), min_steps=300,
            viab_T=100, n_post_draws=500, post_M=20_000, post_M_arm=10_000)
SMOKE = dict(P=4, H=4, burn=2, n_cand=4, n_truth=2, N_v={1: 6, 4: 6, 8: 6}, v_chunk=6, N_theta={1: 5, 4: 5, 8: 5},
             Kc=2, budgets=[2, 8],
             arm_budgets=[2], n_mix=8, n_e=4, lab_chunk=4, n_items=4, R=3, n_clim=4, chunk=8, m=4, m_plug=3,
             n_scale=4, steps_cond=70, steps_p0=20, steps_real=(20, 20), real_split=2, hs=(1, 2, 4),
             lags=(0, 1, 2, 4), min_steps=40, viab_T=6,
             n_post_draws=50, post_M=2000, post_M_arm=1000)
CFG = SMOKE if args.smoke else FULL
P, H = CFG["P"], CFG["H"]
HS = list(CFG["hs"])
NN.Cfg.LAGS, NN.Cfg.HS = tuple(CFG["lags"]), tuple(CFG["hs"])
if args.smoke:
    NN.Cfg.EVAL_EVERY = 10
VJ.T = CFG["viab_T"]
QUERIES = {l: HS for l in (1, 2, 3)}
DCLS = [c for c in ("a", "b", "c", "d", "e") for _ in range(CFG["Kc"])]      # design classes per theta
KD = len(DCLS)
CLOCK = {"member_ticks": {}}
FAILED = []
SETS = [int(s) for s in args.sets.split(",") if s]


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
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if isinstance(obj, dict):
        obj = {"PILOT_NEVER_REUSE_AS_EXAM": True, **obj}
    with open(p + ".tmp", "w") as f:
        json.dump(obj, f, indent=1, default=conv)
    os.replace(p + ".tmp", p)


def npz(name, **arrs):
    p = os.path.join(OUT, name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    np.savez_compressed(p + ".tmp.npz", PILOT_NEVER_REUSE_AS_EXAM=np.array(True), **arrs)
    os.replace(p + ".tmp.npz", p)


def ticks(stage, n):
    CLOCK["member_ticks"][stage] = CLOCK["member_ticks"].get(stage, 0) + int(n)


def hours():
    return (time.time() - T0) / 3600


class Timer:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.t = time.time()
        log(f"== {self.name}")

    def __exit__(self, et, ev, tb):
        log(f"== {self.name} {'FAILED' if et else 'done'} in {time.time() - self.t:.0f}s")
        return False


# ----------------------------------------------------------------------------- setup
INFO = {"study": "round5/ladder",
        "versions": {"python": platform.python_version(), "jax": jax.__version__, "numpy": np.__version__},
        "backend": jax.default_backend(), "devices": [str(d) for d in jax.devices()], "smoke": args.smoke,
        "x64": bool(jax.config.jax_enable_x64), "sets": SETS, "max_hours": args.max_hours,
        "config": {k: (list(v) if isinstance(v, tuple) else {str(a): b for a, b in v.items()} if isinstance(v, dict) else v)
                   for k, v in CFG.items()},
        "views": {v: {"level_key": LL.LEVEL[v], "dim": LL.DIM[v]} for v in LL.VIEWS},
        "pop_names": LL.POP_NAMES, "design_classes_per_theta": DCLS, "arms": {k: list(v) for k, v in LL.ARMS.items()},
        "features": LL.FEATS, "net": {k: getattr(NN.Cfg, k) for k in dir(NN.Cfg) if k.isupper()},
        "grader": "fair energy score per item and cell: vw.harness.HistoryExam._per_cell + vw.scoring.energy_fair; "
                  "OES: vw.scoring.skill_report; sigma, rho: round5/agentenv/evaluator/acceptance.py"}
log(f"backend {INFO['backend']} devices {INFO['devices']} jax {jax.__version__} x64 {INFO['x64']} smoke={args.smoke}")
if jax.default_backend() != "gpu" and not args.cpu_ok:
    log("FATAL: no GPU backend (pass --cpu-ok for a CPU test)")
    sys.exit(3)
SEC = Secret()
INFO["secret_commitment"] = SEC.commitment()
jdump("info.json", INFO)
RN = SL.VRunner(burn=CFG["burn"])
PER_EP = 1 + P + H
EP_T = CFG["burn"] + P + H


# ----------------------------------------------------------------------------- A public scales
def stage_scales():
    N = CFG["n_scale"]
    sim = LL.sim_episodes(RN, ["lR"], np.ones((N, 1)), member_keys(make_key(5901, 0), N), 5901, P, H,
                          CFG["chunk"], classes=np.array(["a"] * N))
    ticks("scales", N * EP_T)
    SC = LL.public_scales(sim["obs"])
    jdump("scales.json", {"note": "public scales: SC1 = gliders_exam scales.npz level1; SCF = per-feature SD of "
                                  "the object view pooled over slots (no-input simulations at the prior mean, "
                                  "seed 5901); SCP / POPM = level-2 scales and means (first 3 from gliders_exam)",
                          "n_episodes": N, **{k: v for k, v in SC.items() if k != "SC1"}})
    return SC


# ----------------------------------------------------------------------------- C prior, B truths
def viab_design(names, lo, hi, n, tag):
    N, d = CFG["N_v"][n], len(names)
    rng = np.random.default_rng([4401, n, tag])
    U = rng.uniform(-1, 1, (N, d))
    th = (lo + hi) / 2 + U * (hi - lo) / 2
    rows = []
    for s in range(0, N, CFG["v_chunk"]):
        e = min(s + CFG["v_chunk"], N)
        r, _ = VJ.viability(names, th[s:e], member_keys(make_key(4401 + 10 * n + tag, s), e - s), RN=RN)
        rows += r
    ticks("viability_design", N * (CFG["burn"] + VJ.T))
    return U, np.array([r["viable"] for r in rows], float), rows


def stage_prior(n):
    shrink, tries = 1.0, []
    for tag in range(3):
        names, lo, hi = LL.box(n, shrink)
        U, y, rows = viab_design(names, lo, hi, n, tag)
        tries.append({"extra_shrink": shrink, "frac_viable": float(y.mean())})
        log(f"  n={n} box shrink {shrink:.3f}: {y.mean():.3f} viable of {len(y)}")
        if y.mean() >= 0.5 or n <= 4 or tag == 2 or args.smoke:
            break
        shrink *= 0.75
    pv = SL.ViabilityPrior().fit(U, y)
    d = len(names)
    pri_u, pm, psd = LL.prior_draws(pv, d, 4096, np.random.default_rng([4404, n]))
    keys = ["count_mean", "count_min", "speed_median", "frac_ticks_at_slot_cap", "mass_median", "rg_median"]
    npz(f"n{n}/viability_design.npz", u=U, viable=y, **{k: np.array([r[k] for r in rows], float) for k in keys})
    out = {"names": names, "lo": lo.tolist(), "hi": hi.tolist(), "shrink_rule_tries": tries, "diag": pv.diag,
           "w": pv.w.tolist(), "features": "poly_feats(u, 2)", "prior_mean_u": pm.tolist(), "prior_sd_u": psd.tolist(),
           "rule": "uniform box conditioned on viab_joint.viability; boxes 1-4 = gliders_exam prior.json, "
                   "boxes 5-8 = scanned box x 0.6 x extra_shrink"}
    jdump(f"n{n}/prior.json", out)
    return names, lo, hi, pv, pri_u, pm, psd


def stage_truths(n, names, lo, hi):
    nc, d = CFG["n_cand"], len(names)
    rng = SEC.rng("truth-draws", n)
    cand = lo + (hi - lo) * rng.random((nc, d))
    rows, _ = VJ.viability(names, cand, SEC.keys(nc, "viability", n), RN=RN)
    ticks("truths", nc * (CFG["burn"] + VJ.T))
    ok = [r["viable"] for r in rows]
    truths = [c for c, v in zip(cand, ok) if v][:CFG["n_truth"]]
    forced = False
    if len(truths) < CFG["n_truth"]:
        if not args.smoke:
            raise RuntimeError(f"only {len(truths)} viable candidates")
        truths, forced = list(cand[:CFG["n_truth"]]), True
    jdump(f"n{n}/truths.json", {"names": names, "candidates": rows,
                                "n_viable": int(sum(ok)), "truths": [t.tolist() for t in truths],
                                "forced_smoke": forced, "secret_commitment": SEC.commitment(),
                                "note": "truths drawn inside the job from the public prior (box + viability rule, "
                                        "first viable candidates in draw order); the secret is not stored"})
    log(f"  n={n} truths {np.round(truths, 3).tolist()} ({sum(ok)}/{nc} viable)")
    return np.array(truths)


# ----------------------------------------------------------------------------- D design, E Lab
def stage_design(n, names, lo, hi):
    N, d = CFG["N_theta"][n], len(names)
    rng = np.random.default_rng([4402, n])
    U = rng.uniform(-1, 1, (N, d))
    th = np.repeat((lo + hi) / 2 + U * (hi - lo) / 2, KD, 0)
    cls = np.tile(np.array(DCLS), N)
    sim = LL.sim_episodes(RN, names, th, member_keys(make_key(4402, n), N * KD), 4402 + n, P, H, CFG["chunk"],
                          classes=cls)
    ticks("design", N * KD * EP_T)
    return U, sim


def stage_lab(n, names, world, truths):
    n_mix, n_e = CFG["n_mix"], CFG["n_e"]
    n_lab = n_mix + n_e
    out, labdata = [], []
    for i, th in enumerate(truths):
        world.params = GW.theta_to_params(dict(zip(names, th)))
        lab = SL.BatchLab(world, SEC.child("lab", n, i), nats=PL.budget(total=SL.EP_CAP * n_lab),
                          max_ticks=n_lab * PER_EP)
        arng = np.random.default_rng([7700, n, i])               # the agent's own program choices
        classes = np.concatenate([arng.permutation(np.repeat(np.array(LL.MIXC), n_mix // 4)),
                                  np.array(["e"] * n_e)])
        obs, U, nats = [], [], []
        for s in range(0, n_lab, CFG["lab_chunk"]):
            e = min(s + CFG["lab_chunk"], n_lab)

            def mk(j, hist, s=s):
                return LL.CLASSES[classes[s + j]](np.random.default_rng([7701, n, i, s + j]), hist, H, SL.EP_CAP)
            r = lab.run_batch(list(range(s, e)), P, H, mk)
            obs.append(r["obs"])
            U.append(r["U"])
            nats.append(r["nats"])
        obs, U, nats = np.concatenate(obs), np.concatenate(U), np.concatenate(nats)
        ticks("lab_charged", n_lab * PER_EP)
        ticks("lab_burn_in_designer", n_lab * CFG["burn"])
        cum = np.cumsum(nats[:n_mix])
        out.append({"truth": i, "usage_final": lab.usage(),
                    "mix_per_budget": {str(b): {"episodes": b, "ticks": b * PER_EP, "nats": float(cum[b - 1]),
                                                "classes": {c: int((classes[:b] == c).sum()) for c in LL.MIXC}}
                                       for b in CFG["budgets"] if b <= n_mix},
                    "nats_per_episode_by_class": {c: float(nats[classes == c].mean()) for c in "abcde"},
                    "caps": {"max_ticks": n_lab * PER_EP, "nats_total": SL.EP_CAP * n_lab,
                             "nats_episode": SL.EP_CAP, "nats_tick": PL.TICK_CAP}})
        labdata.append({"obs": obs, "U": U, "cls": classes, "nats": nats})
        log(f"  n={n} Lab truth {i}: {lab.usage()}")
    jdump(f"n{n}/lab.json", {"per_truth": out})
    return labdata


# ----------------------------------------------------------------------------- F identification
def stage_identify(n, names, lo, hi, Ud, design, labdata, truths, pv, psd):
    N, d = Ud.shape
    cen, hw = (lo + hi) / 2, (hi - lo) / 2
    rng = np.random.default_rng([4403, n])
    res, draws, emus, feats = [], {}, {}, {}
    for view in LL.VIEWS:
        Fd = LL.view_features(view, design["obs"], design["U"], P)
        Fl = [LL.view_features(view, lab["obs"], lab["U"], P) for lab in labdata]
        feats[f"design_{view}"] = Fd.reshape(N, KD, -1).astype(np.float32)
        feats[f"lab_{view}"] = np.stack(Fl).astype(np.float32)
        for arm, classes in LL.ARMS.items():
            sel = np.isin(design["cls"], classes)
            Ka = int(sel.sum()) // N
            Fa = Fd[sel]
            Ua = np.repeat(Ud, Ka, 0)
            proj = SL.Projection().fit(Fa, Ua)
            em = LL.Emulator().fit(Ud, proj(Fa).reshape(N, Ka, d), rng=np.random.default_rng([4405, n]))
            emus[f"{view}|{arm}"] = {"emulator": em.diag, "projection_r2": proj.r2, "K": Ka}
            for i, th in enumerate(truths):
                ut = (th - cen) / hw
                lsel = np.flatnonzero(np.isin(labdata[i]["cls"], classes))
                for nb in (CFG["budgets"] if arm == "mix" else CFG["arm_budgets"]):
                    if nb > len(lsel):
                        continue
                    sbar = proj(Fl[i][lsel[:nb]]).mean(0)
                    post = LL.posterior(em, pv, sbar, nb, rng, M=CFG["post_M"] if arm == "mix" else CFG["post_M_arm"])
                    chk = SL.posterior_checks(post, em, pv, sbar, nb, ut)
                    if arm == "mix":
                        draws[(view, i, nb)] = post["u"]
                    res.append({"view": view, "arm": arm, "truth": i, "n_episodes": nb, "ticks": nb * PER_EP,
                                "nats": float(labdata[i]["nats"][lsel[:nb]].sum()), "ess": post["ess"],
                                "ess_stages": post["ess_stages"], "post_mean_u": post["mean_u"].tolist(),
                                "post_sd_u": post["sd_u"].tolist(),
                                "contraction_sd_ratio": (post["sd_u"] / psd).tolist(),
                                "abs_err_over_prior_sd": (np.abs(post["mean_u"] - ut) / psd).tolist(), **chk})
        rr = [r for r in res if r["view"] == view and r["arm"] == "mix"]
        for nb in CFG["budgets"]:
            c = np.array([r["contraction_sd_ratio"] for r in rr if r["n_episodes"] == nb])
            if len(c):
                log(f"  n={n} {view} mix N={nb}: sd/prior {np.round(c.mean(0), 3).tolist()}")
    summ = {}
    for view in LL.VIEWS:
        for arm in LL.ARMS:
            for nb in sorted({r["n_episodes"] for r in res if r["view"] == view and r["arm"] == arm}):
                rr = [r for r in res if r["view"] == view and r["arm"] == arm and r["n_episodes"] == nb]
                c = np.array([r["contraction_sd_ratio"] for r in rr])
                summ[f"{view}|{arm}|{nb}"] = {
                    "contraction_mean": c.mean(0).tolist(), "log_contraction_mean_over_params": float(np.log(c).mean()),
                    "abs_err_over_prior_sd_mean": np.mean([r["abs_err_over_prior_sd"] for r in rr], 0).tolist(),
                    "in50_frac": float(np.mean([r["in50"] for r in rr])), "in90_frac": float(np.mean([r["in90"] for r in rr])),
                    "hpd_le_90_frac": float(np.mean([r["hpd_level"] <= 0.9 for r in rr])),
                    "nats_mean": float(np.mean([r["nats"] for r in rr])), "ess_min": float(min(r["ess"] for r in rr)),
                    "n_truths": len(rr)}
    jdump(f"n{n}/identification.json", {
        "method": "per view and arm: Gaussian synthetic likelihood on d linear-regression summaries of the view's "
                  "own per-episode statistics (mean over the budget's episodes); polynomial emulator (degree by "
                  "cross-validation) + emulator and CV-misfit covariance; importance sampling under p_v",
        "names": names, "prior_sd_u": psd.tolist(), "emulators": emus, "summary": summ, "per_truth_budget": res})
    npz(f"n{n}/features.npz", u=Ud, design_cls=design["cls"].reshape(N, KD),
        lab_cls=np.stack([lab["cls"] for lab in labdata]), lab_nats=np.stack([lab["nats"] for lab in labdata]), **feats)
    npz(f"n{n}/posterior_draws.npz", **{f"{v}|t{i}|n{nb}": dr[:CFG["n_post_draws"]].astype(np.float32)
                                        for (v, i, nb), dr in draws.items()})
    return draws


# ----------------------------------------------------------------------------- G exams
def stage_exams(n, names, world, truths, SC, th_pm):
    exams, refs, plug = [], [], []
    p0 = GW.theta_to_params(dict(zip(names, map(float, th_pm))))        # the prior mean under p_v
    for i, th in enumerate(truths):
        world.params = GW.theta_to_params(dict(zip(names, th)))
        ex = PL.GExam(world, SEC.child("truth", n, i), PL.MIX, n_items=CFG["n_items"], prefix=P, queries=QUERIES,
                      R=CFG["R"], derived=LL.DERIVED, scales={1: SC["SC1"], 2: SC["SCO"], 3: SC["SCP"]},
                      nats=PL.budget(), n_clim=CFG["n_clim"], name="ladder-pilot")
        ni, m = CFG["n_items"], CFG["m_plug"]
        ticks("exam", ni * (CFG["burn"] + P) + ni * CFG["R"] * ex.H + CFG["n_clim"] * (CFG["burn"] + ex.H))
        # state-given prior-mean plug-in: the simulator at the prior mean from the hidden state x_P
        world.params = p0
        try:
            rep = ex._snap.clone(rep=m, keys=SEC.child("truth", n, i).keys(ni * m, "plug-prior"))
            Pfull = np.concatenate([np.zeros((ni, P, world.n_in)), ex._Ptest], 1)
            _, rec = world.designer.rollout(rep, np.repeat(Pfull, m, axis=0), T=ex.H, rec=("obs",))
        finally:
            world.params = GW.theta_to_params(dict(zip(names, th)))
        ticks("plugin_prior", ni * m * ex.H)
        obs = rec["obs"].reshape(ni, m, ex.H + 1, -1)
        smp = {l: ex._level(l, obs[:, :, ex.queries[l]]) for l in ex.queries}
        plug.append(ex._per_cell(lambda X, Y, s, l: energy_fair(X, Y, s),
                                 samples=[{l: smp[l][j] for l in smp} for j in range(ni)]))
        if i == 0:                                  # the per-view scorer is the exam's scorer
            for v in LL.VIEWS:
                a = LL.ViewCells(ex, LL.LEVEL[v]).score(smp[LL.LEVEL[v]])
                assert np.array_equal(a, plug[-1][:, LL.view_columns(ex, LL.LEVEL[v])]), "ViewCells != HistoryExam"
        ex._snap = None
        exams.append(ex)
        # the 'es' entries of HistoryExam.references() (its v1 and variogram scores are not used here)
        refs.append({"oracle": {"es": ex._per_cell(None, lambda Y, s, l: energy_loo(Y, s, True))},
                     "climatology": {"es": ex._per_cell(lambda X, Y, s, l: energy_fair(X, Y, s), pool=ex.clim)}})
        log(f"  n={n} exam truth {i}: classes {dict(zip(*np.unique(ex.classes, return_counts=True)))}")
    return exams, refs, plug


# ----------------------------------------------------------------------------- H nets, I scores
def stage_predict(n, names, Ud, design, labdata, truths, draws, pri_u, pm, pv, lo, hi, exams, refs, plug, SC, t_stop):
    N, d = Ud.shape
    nT, budgets, m = len(truths), [b for b in CFG["budgets"] if b <= CFG["n_mix"]], CFG["m"]
    cen, hw = (lo + hi) / 2, (hi - lo) / 2
    SCORES, TRAIN = {}, {}
    selm = np.isin(design["cls"], LL.MIXC)
    obs_m, U_m, th_m = design["obs"][selm], design["U"][selm], np.repeat(Ud, KD, 0)[selm]
    Km = int(selm.sum()) // N
    wv = np.exp(pv.logp(Ud))
    pick = np.random.default_rng([4406, n]).choice(N, size=N, p=wv / wv.sum())           # prior-predictive thetas
    ep0 = (pick[:, None] * Km + np.arange(Km)[None]).ravel()
    for i in range(nT):
        for v in LL.VIEWS:
            c = LL.view_columns(exams[i], LL.LEVEL[v])
            SCORES[f"t{i}|{v}|K"] = refs[i]["climatology"]["es"][:, c]
            SCORES[f"t{i}|{v}|O"] = refs[i]["oracle"]["es"][:, c]
            SCORES[f"t{i}|{v}|plugPM"] = plug[i][:, c]
        SCORES[f"t{i}|classes"] = exams[i].classes
    t_score = 120.0                                 # scoring time of one view (measured from the first on)
    WGT = {"cond": 3.0, "P0u": 1.5, "D0": 3.0, "D1": 4.0}       # shares of a view's net time; unused time rolls on
    for vi, view in enumerate(LL.VIEWS):
        if time.time() > T_END:
            FAILED.append(f"skipped n={n} view {view} (deadline)")
            log(f"  SKIP n={n} view {view}: deadline")
            continue
        l = LL.LEVEL[view]
        t0 = time.time()
        # the set's remaining time is shared by its remaining views; a net whose schedule does not fit its
        # share trains for fewer steps (never below min_steps), so every cell is scored
        tv = max((t_stop - t0) / (len(LL.VIEWS) - vi) - t_score, 0.0)
        kw = dict(log=log, deadline=T_END, min_steps=CFG["min_steps"])
        log(f"  n={n} view {view}: {tv:.0f}s for its nets")
        todo = dict(WGT)

        def share(name):
            w = todo.pop(name)
            return max(t0 + tv - time.time(), 0.0) * w / (w + sum(todo.values()))
        ds = NN.make_dataset(view, obs_m, U_m, SC, theta_u=th_m, seed=900 + n)
        pc, TRAIN[f"{view}|cond"] = NN.train_nets(view, [ds], cond=True, steps=CFG["steps_cond"], seed=900 + 10 * n + vi,
                                                  tag=f"[n{n} {view} cond]", time_budget=share("cond"), **kw)
        ds = NN.make_dataset(view, obs_m[ep0], U_m[ep0], SC, seed=950 + n)
        p0, TRAIN[f"{view}|P0u"] = NN.train_nets(view, [ds], cond=False, steps=CFG["steps_p0"], seed=950 + 10 * n + vi,
                                                 tag=f"[n{n} {view} P0u]", time_budget=share("P0u"), **kw)
        pD = {}                                 # D(N): two lockstep groups (small and large budgets)
        for gi, grp in enumerate(([b for b in budgets if b <= CFG["real_split"]],
                                  [b for b in budgets if b > CFG["real_split"]])):
            if not grp:
                continue
            order = [(i, nb) for i in range(nT) for nb in grp]
            dsets = [NN.make_dataset(view, labdata[i]["obs"][:nb], labdata[i]["U"][:nb], SC, seed=100 * nb + i)
                     for i, nb in order]
            prm, TRAIN[f"{view}|D|group{gi}"] = NN.train_nets(
                view, dsets, cond=False, steps=CFG["steps_real"][gi], seed=700 + 10 * n + vi + 100 * gi,
                tag=f"[n{n} {view} D {grp}]", time_budget=share(f"D{gi}"), **kw)
            TRAIN[f"{view}|D|group{gi}"]["order_truth_budget"] = order
            pD.update(dict(zip(order, prm)))
            del dsets
        del ds
        t_train = time.time() - t0
        rng = np.random.default_rng([4407, n, vi])
        for i in range(nT):
            items = exams[i].public()
            ni = len(items)
            vc = LL.ViewCells(exams[i], l)

            def put(name, S):
                try:
                    SCORES[f"t{i}|{view}|{name}"] = vc.score(S)
                except ValueError as exc:                      # e.g. non-finite samples: the policy is dropped
                    FAILED.append(f"n={n} {view} t{i} {name}: {exc}")
                    log(f"  n={n} {view} truth {i} {name} NOT SCORED: {exc}")
            ut = (truths[i] - cen) / hw
            put("C", NN.net_samples(view, pc[0], items, m, 400 + i, HS, SC, cond=True, theta_u=ut))
            put("PM", NN.net_samples(view, pc[0], items, m, 410 + i, HS, SC, cond=True, theta_u=pm))
            put("P0", NN.net_samples(view, pc[0], items, m, 420 + i, HS, SC, cond=True,
                                     theta_u=pri_u[rng.choice(len(pri_u), ni * m)].reshape(ni, m, d)))
            put("P0u", NN.net_samples(view, p0[0], items, m, 430 + i, HS, SC))
            for b, nb in enumerate(budgets):
                if draws is not None and (view, i, nb) in draws:
                    dr = draws[(view, i, nb)]
                    put(f"S@{nb}", NN.net_samples(view, pc[0], items, m, 440 + i, HS, SC, cond=True,
                                                  theta_u=dr[rng.choice(len(dr), ni * m)].reshape(ni, m, d)))
                put(f"D@{nb}", NN.net_samples(view, pD[(i, nb)], items, m, 450 + i, HS, SC))
                model = LL.ridge_fit(view, labdata[i]["obs"][:nb], labdata[i]["U"][:nb], HS, SC)
                put(f"Dr@{nb}", LL.ridge_samples(view, model, items, m, 0, HS, SC))
        npz(f"n{n}/scores.npz", **SCORES)
        jdump(f"n{n}/train_info.json", TRAIN)
        t_score = time.time() - t0 - t_train
        log(f"  n={n} view {view}: nets {t_train:.0f}s, scored in {t_score:.0f}s")
    npz(f"n{n}/scores.npz", **SCORES)
    return SCORES


def report(n, SCORES, nT, budgets):
    """Per view: OES of every policy (vw.scoring.skill_report) and sigma, rho per budget (evaluator.acceptance)."""
    out = {}
    worlds = np.concatenate([[i] * len(SCORES[f"t{i}|classes"]) for i in range(nT)])
    groups = np.concatenate([SCORES[f"t{i}|classes"] for i in range(nT)])
    for view in LL.VIEWS:
        names = sorted({k.split("|")[2] for k in SCORES if k.count("|") == 2 and k.split("|")[1] == view})
        names = [a for a in names if all(f"t{i}|{view}|{a}" in SCORES for i in range(nT))]
        if "C" not in names:
            continue
        S = {a: np.concatenate([SCORES[f"t{i}|{view}|{a}"] for i in range(nT)]) for a in names}
        rep = skill_report({"climatology": S["K"], "oracle": S["O"], **{a: S[a] for a in names if a not in ("K", "O")}},
                           cells=[(view, h) for h in HS], groups=groups, n_boot=1000,
                           valid=np.ones(len(HS), bool) if args.smoke else None)
        valid = np.array(rep["valid"], bool)
        acc = {}
        for nb in budgets:
            if f"S@{nb}" not in S:
                continue
            Ld = {a: float(S[a][:, valid].sum(1).mean()) for a in (f"D@{nb}", f"Dr@{nb}")}
            dbest = min(Ld, key=Ld.get)
            r = ACC.shares({"K": S["K"], "C": S["C"], "P0": S["P0"], "S": S[f"S@{nb}"], "D": S[dbest]}, valid,
                           worlds=worlds, n_boot=1000, seed=nb)
            acc[str(nb)] = {"D_is": dbest, **{k: r[k] for k in ("sigma", "null_is", "rho", "sigma_worlds", "rho_worlds",
                                                                 "pass_sigma", "pass_rho", "L")}}
        out[view] = {"report": public_report(rep), "acceptance": acc, "n_items": int(len(worlds))}
        agg = rep["aggregate"]
        log(f"  n={n} {view} OES " + ", ".join(f"{k} {agg[k]:.3f}" for k in sorted(agg) if k not in ("climatology", "oracle")))
        log(f"  n={n} {view} " + "; ".join(f"N={b}: sigma {a['sigma']:.3f} rho {a['rho']:.2f}" for b, a in acc.items()))
    jdump(f"n{n}/prediction.json", out)
    return out


# ----------------------------------------------------------------------------- main
def run_set(n, world_box, SC, t_stop):
    """One hidden set. Returns the seconds of the stages before the nets (simulation and identification)."""
    t_set = time.time()
    with Timer(f"n={n} C prior"):
        names, lo, hi, pv, pri_u, pm, psd = stage_prior(n)
    with Timer(f"n={n} B truths"):
        truths = stage_truths(n, names, lo, hi)
    with Timer(f"n={n} D design"):
        Ud, design = stage_design(n, names, lo, hi)
    if world_box[0] is None:
        world_box[0] = SL.build_world(GW.theta_to_params(dict(zip(names, truths[0]))), burn=CFG["burn"])
    world = world_box[0]
    with Timer(f"n={n} E Lab"):
        labdata = stage_lab(n, names, world, truths)
    draws = None
    try:
        with Timer(f"n={n} F identification"):
            draws = stage_identify(n, names, lo, hi, Ud, design, labdata, truths, pv, psd)
    except Exception as exc:
        FAILED.append(f"n={n} identification")
        log(f"  identification FAILED: {exc!r}\n{traceback.format_exc()}")
    with Timer(f"n={n} G exams"):
        exams, refs, plug = stage_exams(n, names, world, truths, SC, (lo + hi) / 2 + pm * (hi - lo) / 2)
    fixed = time.time() - t_set
    with Timer(f"n={n} H nets and I scores"):
        SCORES = stage_predict(n, names, Ud, design, labdata, truths, draws, pri_u, pm, pv, lo, hi, exams, refs, plug,
                               SC, t_stop)
    try:
        report(n, SCORES, len(truths), CFG["budgets"])
    except Exception as exc:
        FAILED.append(f"n={n} report")
        log(f"  report FAILED: {exc!r}\n{traceback.format_exc()}")
    return fixed


def main():
    with Timer("A public scales"):
        SC = stage_scales()
    world_box, done, per_set, fixed = [None], [], [], []
    for k, n in enumerate(SETS):
        left = T_END - time.time()
        # a set is skipped when the time left does not cover the longest simulation part so far plus the
        # shortest net schedules; otherwise the time left is shared equally by the remaining sets
        need = (1.05 * max(fixed) + 420) if fixed else 0.0
        if fixed and left < need:
            FAILED.append(f"skipped n={n} (deadline: {left / 60:.0f} min left, {need / 60:.0f} min needed)")
            log(f"SKIP n={n}: {left / 60:.0f} min left, about {need / 60:.0f} min needed")
            continue
        t = time.time()
        t_stop = t + (left - 60) / (len(SETS) - k)
        log(f"n={n}: {left / 60:.1f} min left, this set's share ends in {(t_stop - t) / 60:.1f} min")
        try:
            fixed.append(run_set(n, world_box, SC, t_stop))
            done.append(n)
        except Exception as exc:
            FAILED.append(f"n={n}")
            log(f"n={n} FAILED: {exc!r}\n{traceback.format_exc()}")
        per_set.append(time.time() - t)
        INFO.update(member_ticks=CLOCK["member_ticks"], hours=hours(), failed=FAILED, sets_done=done,
                    seconds_per_set=per_set, seconds_before_nets_per_set=fixed)
        jdump("info.json", INFO)
    INFO["member_ticks_total"] = int(sum(CLOCK["member_ticks"].values()))
    jdump("info.json", INFO)
    log(f"done: sets {done}, {INFO['member_ticks_total']} member-ticks, {hours():.2f} h, failed {FAILED}")
    return done


if __name__ == "__main__":
    try:
        done = main()
    except Exception as exc:
        log(f"FATAL {exc!r}\n{traceback.format_exc()}")
        INFO["fatal"] = repr(exc)
        INFO["member_ticks"] = CLOCK["member_ticks"]
        jdump("info.json", INFO)
        sys.exit(1)
    if not done:
        sys.exit(1)
    if [f for f in FAILED if not f.startswith("skipped")]:
        sys.exit(2)
