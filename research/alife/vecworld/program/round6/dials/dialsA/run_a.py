"""run_a -- study A of round 6's dials plan, the gliders calibration (GPU job).

PILOT ONLY: the truths are round 5's public pilot truths; the Lab data, items and nets written here must
NEVER be reused as an exam. The world secret (256 bits, os.urandom) is never written; only its commitment.
What is declared is in DECLARED.md (committed before this file ran); what this file does, in order:

  0 presmoke  the same pipeline at FULL SHAPES and small counts (one truth, 512 episodes per family tiled to
              6,144 for the nets' shapes, a few steps per net), the zero point of the law switch on this
              backend, then a speed guard: the job stops (exit 4) if the measured rates cannot finish the
              required stages inside --max-hours. Same process, so the full pass reuses every compiled program.
  1 families  public (ladder_lib.sim_episodes, gworld.tick) and true-form (xlaw.sim_episodes_x, dlaw.tick,
              eta 0 at half of the points and 4 at the other half): 768 points x 8 mix episodes each.
  2 worlds    8 truths x eta in {0, 4}: a Lab (32 mix + 32 input-free episodes), two exams of 48 items x 12
              replicates (`sel`: picks only; `score`: every reported score), K, O and the state-given plug-in
              (the public law at the true theta from the hidden state).
  3 S         round 5's scripted inference for the block view (posterior draws per world and budget).
  4 base nets public-form and true-form conditioned nets, 3 seeds each, in lockstep; schedule 6,000 steps,
              doubled while the training rule is unmet (at most twice); every rung scored (P0, Cpub, Ctrue).
  5 N = 8     FT, the fine-tuned true-form net (CFT), RES, S; then D(32); then N = 32, N = 2, the controls on
              input-free Lab episodes, D(8), D(2), as the clock allows (DECLARED R17).
Scores: fair energy score per item and horizon through the exam's own scorer (ladder_lib.ViewCells).
The criteria are computed from scores.npz by make_summary.py (a_stats.py); the job prints a first look.

usage: python -B run_a.py --out DIR [--max-hours 2.0] [--smoke] [--cpu-ok] [--no-presmoke]
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
import xlaw as X  # noqa: E402
import a_nets as AN  # noqa: E402
import a_stats as ST  # noqa: E402

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

from vw.scoring import energy_fair, energy_loo  # noqa: E402
from vw.secret import Secret  # noqa: E402
from vw.world import make_key, member_keys  # noqa: E402

LL, NN, SL, GW, PL = X.LL, X.NN, X.SL, X.GW, X.PL
VIEW = "block"

ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
ap.add_argument("--max-hours", type=float, default=2.0, help="the script's own limit (the request's is larger)")
ap.add_argument("--smoke", action="store_true", help="tiny shapes for a CPU test of the code path")
ap.add_argument("--cpu-ok", action="store_true", help="allow a CPU backend (tests only)")
ap.add_argument("--no-presmoke", action="store_true")
ap.add_argument("--extension", action="store_true",
                help="DECLARED R19: 8 more truths, the first job's base nets and public-family features reused")
ap.add_argument("--prior", default=os.path.join(HERE, "results", "job"), help="the first job's outputs (extension)")
args = ap.parse_args()
EXT = bool(args.extension)
ROOT_OUT = args.out
os.makedirs(ROOT_OUT, exist_ok=True)
T0 = time.time()
T_END = T0 + args.max_hours * 3600
PILOT = "PILOT_NEVER_REUSE_AS_EXAM"

FULL = dict(P=16, H=16, burn=GW.BURN, n_theta=768, Kc=2, chunk=256, tile=1, truths=list(range(8)), etas=(0.0, 4.0),
            n_mix=32, n_free=32, n_items=48, R=12, n_clim=48, m=32, m_plug=8, budgets=(8, 32, 2), d_first=32,
            hs=(1, 2, 4, 8, 16), lags=(0, 1, 2, 4, 8), rungs=(6000, 12000, 24000), steps_d=1200, d_doublings=2,
            ft_steps=400, ft_doublings=2, seeds=3, post_M=20_000, n_ctrl=8, timing_runs=False)
# presmoke: every stage once at the full shapes (chunk 256, 576-member truth rollouts, 6 base nets on 6,144
# episodes, 16 fine-tunes in lockstep, 96-item sampling); counts are small
PRE = dict(FULL, n_theta=64, tile=12, truths=[0], rungs=(40, 120), steps_d=40, d_doublings=0, ft_steps=80,
           ft_doublings=0, post_M=4000, timing_runs=True)
SMOKE = dict(P=4, H=4, burn=2, n_theta=6, Kc=1, chunk=8, tile=1, truths=[0], etas=(0.0, 4.0),
             n_mix=8, n_free=4, n_items=4, R=3, n_clim=4, m=4, m_plug=2, budgets=(4, 8, 2), d_first=8,
             hs=(1, 2, 4), lags=(0, 1, 2, 4), rungs=(8, 16), steps_d=8, d_doublings=1,
             ft_steps=4, ft_doublings=1, seeds=2, post_M=2000, n_ctrl=4, timing_runs=False)
if args.smoke:
    FULL = SMOKE
    PRE = dict(SMOKE, rungs=(4, 8), d_doublings=0, ft_doublings=0, timing_runs=True)
    NN.Cfg.EVAL_EVERY, NN.Cfg.BATCH, NN.Cfg.M_TRAIN, NN.Cfg.C, NN.Cfg.BLOCKS = 4, 8, 2, 8, 1
    NN.Cfg.N_VAL, NN.Cfg.EVAL_ROWS, NN.Cfg.EVAL_DRAWS = 16, 8, 2
    AN.FT.BATCH, AN.FT.LOCK, AN.FT.GRID, AN.FT.N_TH, AN.FT.N_VAL = 4, 4, 2, 16, 16
NN.Cfg.LAGS, NN.Cfg.HS = tuple(FULL["lags"]), tuple(FULL["hs"])
HS = list(FULL["hs"])
P_, H_ = FULL["P"], FULL["H"]
PER_EP = 1 + P_ + H_
EP_T = FULL["burn"] + P_ + H_
SCALES = {"SC1": LL.SC1}
FAILED, SKIPPED, NOTES = [], [], []
RES_LAM = {}
STATE = {"out": ROOT_OUT, "phase": "start"}


def log(msg):
    line = f"{time.strftime('%H:%M:%S')} [{(time.time() - T0) / 60:6.1f} min] {msg}"
    print(line, flush=True)
    with open(os.path.join(ROOT_OUT, "progress.txt"), "a") as f:
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
    p = os.path.join(STATE["out"], name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if isinstance(obj, dict):
        obj = {PILOT: True, **obj}
    with open(p + ".tmp", "w") as f:
        json.dump(obj, f, indent=1, default=conv)
    os.replace(p + ".tmp", p)


def npz(name, **arrs):
    p = os.path.join(STATE["out"], name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    np.savez_compressed(p + ".tmp.npz", **{PILOT: np.array(True)}, **arrs)
    os.replace(p + ".tmp.npz", p)


def left():
    return T_END - time.time()


class Timer:
    def __init__(self, name, times=None):
        self.name, self.times = name, times

    def __enter__(self):
        self.t = time.time()
        log(f"== {self.name}")
        return self

    def __exit__(self, et, ev, tb):
        dt = time.time() - self.t
        if self.times is not None:
            self.times[self.name] = self.times.get(self.name, 0.0) + dt
        log(f"== {self.name} {'FAILED' if et else 'done'} in {dt:.0f}s")
        return False


# ----------------------------------------------------------------------------- setup
if not os.path.exists(os.path.join(ROOT_OUT, "progress.txt")):
    with open(os.path.join(ROOT_OUT, "progress.txt"), "w") as f:
        f.write(f"{PILOT}: this log is of a pilot on public pilot truths\n")
log(f"backend {jax.default_backend()} devices {[str(d) for d in jax.devices()]} jax {jax.__version__} "
    f"x64 {bool(jax.config.jax_enable_x64)} smoke={args.smoke} max_hours={args.max_hours}")
X.assert_one_checkout()
if jax.default_backend() != "gpu" and not args.cpu_ok:
    log("FATAL: no GPU backend (pass --cpu-ok for a CPU test)")
    sys.exit(3)
SEC = Secret()
NAMES, LO, HI = LL.box(4)
CEN, HW = (LO + HI) / 2, (HI - LO) / 2
R5 = os.path.join(X.PROG, "round5", "ladder", "results", "job", "n4")
TRUTHS = np.array(json.load(open(os.path.join(R5, "truths.json")))["truths"], float)          # (8, 4), public pilot
_prior = json.load(open(os.path.join(R5, "prior.json")))
assert _prior["names"] == NAMES and np.allclose(_prior["lo"], LO) and np.allclose(_prior["hi"], HI)
PV = SL.ViabilityPrior()
PV.w = np.array(_prior["w"], float)
PRI_U, PM, PSD = LL.prior_draws(PV, 4, 4096, np.random.default_rng([4404, 4]))
assert np.allclose(PM, _prior["prior_mean_u"], atol=0.02), "the viability prior is not round 5's"
RN = SL.VRunner(burn=FULL["burn"])
XR = X.XRunner(burn=FULL["burn"])
WORLD = X.build_world_x(X.xparams(NAMES, TRUTHS[0], 0.0), burn=FULL["burn"])
INFO = {"study": "round6/dials/dialsA (plan study A, gliders calibration)",
        "versions": {"python": platform.python_version(), "jax": jax.__version__, "numpy": np.__version__},
        "backend": jax.default_backend(), "devices": [str(d) for d in jax.devices()], "smoke": args.smoke,
        "x64": bool(jax.config.jax_enable_x64), "max_hours": args.max_hours, "secret_commitment": SEC.commitment(),
        "modules": X.module_files(), "names": NAMES, "lo": LO.tolist(), "hi": HI.tolist(),
        "truths_source": "round5/ladder/results/job/n4/truths.json", "truths": TRUTHS.tolist(),
        "law": {"term": "XW stress conversion (defect_gliders/dlaw.py)", "W0": X.W0, "DW": X.DW, "KXW": X.KXW},
        "net": {k: getattr(NN.Cfg, k) for k in dir(NN.Cfg) if k.isupper()},
        "ft": {k: getattr(AN.FT, k) for k in dir(AN.FT) if k.isupper()},
        "grader": "fair energy score per item and horizon: vw.harness.HistoryExam._per_cell + vw.scoring.energy_fair "
                  "through ladder_lib.ViewCells; L = sum over horizons, mean over items (acceptance.py)"}


if EXT:
    # DECLARED R19: the first 8 viable of 48 box draws (numpy seed [6601, 4]), round 5's viability rule under
    # the public law (viab_joint.viability, as run_ladder.stage_truths). Public pilot values, written out.
    import viab_joint as VJ  # noqa: E402
    VJ.T = 6 if args.smoke else 100
    n_cand, n_new = (6, 1) if args.smoke else (48, 8)
    cand = LO + (HI - LO) * np.random.default_rng([6601, 4]).random((n_cand, 4))
    rows, _ = VJ.viability(NAMES, cand, member_keys(make_key(6601, 4), n_cand), RN=RN)
    okv = [bool(r["viable"]) for r in rows]
    new = [c for c, v in zip(cand, okv) if v][:n_new]
    if len(new) < n_new:
        if not args.smoke:
            log(f"FATAL: only {len(new)} viable candidates for the extension")
            sys.exit(5)
        new = list(cand[:n_new])
    n_old = len(TRUTHS)
    TRUTHS = np.concatenate([TRUTHS, np.array(new)])
    new_idx = list(range(n_old, n_old + n_new))
    FULL = dict(FULL, truths=new_idx, rungs=())
    PRE = dict(PRE, truths=new_idx[:1], rungs=())
    INFO.update(extension=True, truths=TRUTHS.tolist(), prior_job_outputs=os.path.relpath(args.prior, HERE),
                extension_truths={"indices": new_idx, "rule": "first viable of box draws, numpy seed [6601, 4], "
                                  "viab_joint.viability under the public law (DECLARED R19)",
                                  "candidates": cand.tolist(), "viable": okv, "n_viable": int(sum(okv)),
                                  "member_ticks": n_cand * (FULL["burn"] + VJ.T)})
    log(f"extension: truths {new_idx} = {np.round(np.array(new), 3).tolist()} ({sum(okv)}/{n_cand} candidates viable)")
    X.assert_one_checkout()


def cfg_json(cfg):
    return {k: (list(v) if isinstance(v, (tuple, list)) else v) for k, v in cfg.items()}


def estimate_ticks(cfg):
    nw = len(cfg["truths"]) * len(cfg["etas"])
    ni, R, b = cfg["n_items"], cfg["R"], cfg["burn"]
    KD = 4 * cfg["Kc"]
    return {"families": 0 if EXT else 2 * cfg["n_theta"] * KD * EP_T, "lab": nw * (cfg["n_mix"] + cfg["n_free"]) * (b + PER_EP),
            "exams": nw * 2 * (ni * (b + P_) + ni * R * H_ + cfg["n_clim"] * (b + H_)),
            "plugins": nw * 2 * ni * cfg["m_plug"] * H_}


# ----------------------------------------------------------------------------- 1 families
def stage_families(cfg, times):
    N, KD = cfg["n_theta"], 4 * cfg["Kc"]
    cls1 = [c for c in LL.MIXC for _ in range(cfg["Kc"])]
    cls = np.tile(np.array(cls1), N)
    fam, rates = {}, {}
    for name, tag in (("pub", 0), ("true", 1)):
        rng = np.random.default_rng([6602, tag])
        Ud = rng.uniform(-1, 1, (N, 4))
        th = np.repeat(CEN + Ud * HW, KD, 0)
        keys = member_keys(make_key(6602, tag), N * KD)
        stamps = [time.time()]
        lg = lambda m: stamps.append(time.time())
        if name == "pub":
            sim = LL.sim_episodes(RN, NAMES, th, keys, 6602, P_, H_, cfg["chunk"], classes=cls, log=lg)
            th_u = np.repeat(Ud, KD, 0)
            eta_pt = np.zeros(N)
        else:
            eta_pt = 4.0 * (rng.permutation(N) >= N // 2)
            sim = X.sim_episodes_x(XR, NAMES, th, np.repeat(eta_pt, KD), keys, 6603, P_, H_, cfg["chunk"], classes=cls, log=lg)
            th_u = np.concatenate([np.repeat(Ud, KD, 0), np.repeat(eta_pt, KD)[:, None] / 4.0], 1)
        d = np.diff(stamps)
        rates[name] = {"member_ticks": N * KD * EP_T, "seconds": float(d.sum()), "seconds_last_chunk": float(d[-1]),
                       "rate_last_chunk": float(cfg["chunk"] * EP_T / d[-1])}
        fam[name] = {"Ud": Ud, "eta_pt": eta_pt, "obs": sim["obs"], "U": sim["U"], "cls": sim["cls"], "th_u": th_u,
                     "nats": sim["nats"], "KD": KD}
        log(f"  family {name}: {N} points x {KD} episodes, {d.sum():.0f}s, last chunk {rates[name]['rate_last_chunk']:.0f} "
            f"member-ticks/s; nats by class " + str({c: round(float(sim['nats'][cls == c].mean()), 1) for c in LL.MIXC}))
    times["family_rates"] = rates
    # channel-0 share of the block mass after the program, by class and eta (the term at work, level 1)
    tr = fam["true"]
    c0 = tr["obs"][:, :, :64].astype(float).sum(-1) / LL.SC1[0]
    eta_ep = np.repeat(tr["eta_pt"], KD)
    drop = 1.0 - c0[:, -1] / np.maximum(c0[:, P_], 1e-9)
    INFO_fam = {f"c0_block_sum_lost_P_to_end|eta{int(e)}|{c}": float(drop[(eta_ep == e) & (tr["cls"] == c)].mean())
                for e in (0.0, 4.0) for c in LL.MIXC if ((eta_ep == e) & (tr["cls"] == c)).any()}
    log("  true-form family, share of the channel-0 block sum lost over the program window: "
        + ", ".join(f"{k.split('|', 1)[1]} {v:+.3f}" for k, v in INFO_fam.items()))
    return fam, INFO_fam


# ----------------------------------------------------------------------------- 2 worlds
def lab_classes(cfg, t):
    arng = np.random.default_rng([7700, int(t)])
    mix = np.concatenate([arng.permutation(np.array(LL.MIXC)) for _ in range(cfg["n_mix"] // 4)])
    return np.concatenate([mix, np.array(["a"] * cfg["n_free"])])


def lab_c0_loss(cfg, w):
    """Level-1 bookkeeping on the Lab's mix episodes: share of the channel-0 block sum lost between the
    start and the end of the program, by class (the public law conserves it; the hidden term does not)."""
    nm = cfg["n_mix"]
    c0 = w["lab_obs"][:nm, :, :64].astype(float).sum(-1)
    drop = 1.0 - c0[:, -1] / np.maximum(c0[:, P_], 1e-9)
    return {c: float(drop[w["lab_cls"][:nm] == c].mean()) for c in LL.MIXC}


def stage_worlds(cfg, times):
    """Per (eta, truth): Lab data, two exams, references. The seeds depend on the truth only, so the two
    dial values are nested: the same starts, noise and Lab programs' random numbers."""
    worlds, secs = {}, []
    n_lab = cfg["n_mix"] + cfg["n_free"]
    ni, m = cfg["n_items"], cfg["m_plug"]
    for ei, eta in enumerate(cfg["etas"]):
        for t in cfg["truths"]:
            t_w = time.time()
            p_true = X.xparams(NAMES, TRUTHS[t], eta)
            p_pub = X.xparams(NAMES, TRUTHS[t], 0.0)
            WORLD.params = p_true
            lab = SL.BatchLab(WORLD, SEC.child("lab", int(t)), nats=PL.budget(total=SL.EP_CAP * n_lab),
                              max_ticks=n_lab * PER_EP)
            classes = lab_classes(cfg, t)

            def mk(j, hist, t=t, classes=classes):
                return LL.CLASSES[classes[j]](np.random.default_rng([7701, int(t), j]), hist, H_, SL.EP_CAP)
            r = lab.run_batch(list(range(n_lab)), P_, H_, mk)
            w = {"eta": float(eta), "truth": int(t), "lab_obs": r["obs"], "lab_U": r["U"], "lab_cls": classes,
                 "lab_nats": r["nats"], "lab_usage": lab.usage(), "exams": {}}
            for half in ("sel", "score"):
                WORLD.params = p_true
                ex = PL.GExam(WORLD, SEC.child("truth", int(t)), PL.MIX, n_items=ni, prefix=P_, queries={1: HS},
                              R=cfg["R"], derived=LL.DERIVED, scales={1: LL.SC1}, nats=PL.budget(),
                              n_clim=cfg["n_clim"], name=f"dialsA-{half}")
                vc = LL.ViewCells(ex, 1)
                ref = {"O": ex._per_cell(None, lambda Y, s, l: energy_loo(Y, s, True)),
                       "K": ex._per_cell(lambda Xs, Y, s, l: energy_fair(Xs, Y, s), pool=ex.clim)}
                WORLD.params = p_pub                    # the public law at the true theta, from the hidden state
                try:
                    rep = ex._snap.clone(rep=m, keys=SEC.child("truth", int(t)).keys(ni * m, "plug", half))
                    Pfull = np.concatenate([np.zeros((ni, P_, WORLD.n_in)), ex._Ptest], 1)
                    _, rec = WORLD.designer.rollout(rep, np.repeat(Pfull, m, axis=0), T=ex.H, rec=("obs",))
                finally:
                    WORLD.params = p_true
                obs = rec["obs"].reshape(ni, m, ex.H + 1, -1)
                ref["plug"] = vc.score(ex._level(1, obs[:, :, ex.queries[1]]))
                ex._snap = None
                w["exams"][half] = {"vc": vc, "items": ex.public(), "classes": ex.classes, "ref": ref}
            w["items"] = w["exams"]["sel"]["items"] + w["exams"]["score"]["items"]
            Ud = np.stack([LL.program_dense(it["program"], H_, LL.NW) for it in w["items"]])
            w["item_cls"] = np.array([AN.program_class(u) for u in Ud])
            w["item_reg"] = np.stack([AN.region(u) for u in Ud])
            w["item_z0"] = AN.block_scaled(np.stack([np.asarray(it["history"], float)[-1, :LL.NC] for it in w["items"]]))
            true_cls = np.concatenate([w["exams"]["sel"]["classes"], w["exams"]["score"]["classes"]])
            w["class_agree"] = float(np.mean(w["item_cls"] == true_cls))
            worlds[(ei, int(t))] = w
            secs.append(time.time() - t_w)
            log(f"  world eta={eta:g} truth {t}: {secs[-1]:.0f}s; lab {w['lab_usage']['ticks_used']} ticks "
                f"{w['lab_usage']['total_nats']:.0f} nats; structural class = mix class on {w['class_agree']:.3f} of items")
    times["world_seconds"] = secs
    return worlds


def put(SCO, name, ei, ti, s, w, S):
    """Score samples S (2 n_items, m, n_h, 192) of one world (sel items first) and store (2, n_items, n_h)."""
    ni = len(w["exams"]["sel"]["items"])
    a = np.stack([w["exams"]["sel"]["vc"].score(S[:ni]), w["exams"]["score"]["vc"].score(S[ni:])])
    if name not in SCO:
        SCO[name] = np.full(SCO["_shape"], np.nan, np.float32)
    SCO[name][ei, ti, s] = a


def save_scores(cfg, SCO, worlds, extra=None):
    out = {k: v for k, v in SCO.items() if not k.startswith("_")}
    cl = np.array([[np.stack([worlds[(ei, t)]["exams"][h]["classes"] for h in ("sel", "score")])
                    for t in cfg["truths"]] for ei in range(len(cfg["etas"]))])
    npz("scores.npz", classes=cl, etas=np.array(cfg["etas"]), truths=np.array(cfg["truths"]), hs=np.array(HS),
        axes=np.array("eta, truth, seed, half (0 sel, 1 score), item, horizon"), **out, **(extra or {}))


# ----------------------------------------------------------------------------- 3 scripted inference
def stage_identify(cfg, fam, worlds):
    if EXT:                                             # the first job's public-family features
        z = np.load(os.path.join(args.prior, "family_features.npz"))
        pub = {"Ud": z["pub_Ud"], "th_u": z["pub_th_u"].astype(float), "KD": int(z["KD"])}
        Fd = z["pub_features"].astype(float)
    else:
        pub = fam["pub"]
        Fd = LL.view_features(VIEW, pub["obs"], pub["U"], P_)
    N, KD = len(pub["Ud"]), pub["KD"]
    proj = SL.Projection().fit(Fd, pub["th_u"])
    em = LL.Emulator().fit(pub["Ud"], proj(Fd).reshape(N, KD, 4), rng=np.random.default_rng([4405, 4]))
    rng = np.random.default_rng([4403, 4])
    draws, rows = {}, []
    for (ei, t), w in worlds.items():
        Fl = LL.view_features(VIEW, w["lab_obs"][:cfg["n_mix"]], w["lab_U"][:cfg["n_mix"]], P_)
        ut = (TRUTHS[t] - CEN) / HW
        for nb in cfg["budgets"]:
            post = LL.posterior(em, PV, proj(Fl[:nb]).mean(0), nb, rng, M=cfg["post_M"])
            draws[(ei, t, nb)] = post["u"]
            rows.append({"eta": w["eta"], "truth": t, "n_episodes": nb, "ess": post["ess"],
                         "post_mean_u": post["mean_u"].tolist(), "post_sd_u": post["sd_u"].tolist(),
                         "contraction_sd_ratio": (post["sd_u"] / PSD).tolist(),
                         "abs_err_over_prior_sd": (np.abs(post["mean_u"] - ut) / PSD).tolist()})
    jdump("identification.json", {"method": "round 5's (ladder run_ladder.stage_identify), block view, mix arm, public law",
                                  "emulator": em.diag, "projection_r2": proj.r2, "per_world_budget": rows})
    if not EXT:
        npz("family_features.npz", pub_features=Fd.astype(np.float32), pub_th_u=pub["th_u"].astype(np.float32),
            pub_Ud=pub["Ud"], KD=np.array(KD))
    return draws


# ----------------------------------------------------------------------------- 4 base nets
def family_arrays(cfg, f):
    k = cfg["tile"]
    if k == 1:
        return f["obs"], f["U"], f["th_u"]
    return (np.tile(f["obs"], (k, 1, 1)), np.tile(f["U"], (k, 1, 1)), np.tile(f["th_u"], (k, 1)))


def train_base(cfg, fam, steps, tag):
    ns = cfg["seeds"]
    ds = []
    for name, s0 in (("pub", 900), ("true", 950)):
        obs, U, th = family_arrays(cfg, fam[name])
        ds += [NN.make_dataset(VIEW, obs, U, SCALES, theta_u=th, seed=s0 + s) for s in range(ns)]
    lines = []

    def lg(m):
        lines.append(m)
        log(m)
    prm, info = NN.train_nets(VIEW, ds, cond=True, steps=steps, seed=4000 + steps, log=lg, tag=tag, deadline=T_END)
    del ds
    info["rule_met"] = bool(all(b <= 0.8 * info["steps"] for b in info["best_step"])) and info["stopped_early"] is None
    info["log_lines"] = lines
    info["net_order"] = [f"P{s}" for s in range(ns)] + [f"T{s}" for s in range(ns)]
    return prm[:ns], prm[ns:], info


def u_truth(t, eta=None):
    u = (TRUTHS[t] - CEN) / HW
    return u if eta is None else np.concatenate([u, [float(eta) / 4.0]])


def prior_theta(rng, n, m):
    return PRI_U[rng.choice(len(PRI_U), n * m)].reshape(n, m, 4)


def score_base(cfg, SCO, worlds, Pn, Tn, suffix, keep=None):
    """P0, the public-form C and the true-form C of every world with the given nets."""
    m = cfg["m"]
    for (ei, t), w in worlds.items():
        ti = cfg["truths"].index(t)
        items = w["items"]
        for s in range(cfg["seeds"]):
            rng = np.random.default_rng([4407, ei, t, s])
            S0 = NN.net_samples(VIEW, Pn[s], items, m, 420 + 7 * t + s, HS, SCALES, cond=True,
                                theta_u=prior_theta(rng, len(items), m))
            put(SCO, "P0" + suffix, ei, ti, s, w, S0)
            if keep is not None:
                keep[(ei, t, s)] = S0.astype(np.float32)
            put(SCO, "Cpub" + suffix, ei, ti, s, w,
                NN.net_samples(VIEW, Pn[s], items, m, 400 + 7 * t + s, HS, SCALES, cond=True, theta_u=u_truth(t)))
            put(SCO, "Ctrue" + suffix, ei, ti, s, w,
                NN.net_samples(VIEW, Tn[s], items, m, 410 + 7 * t + s, HS, SCALES, cond=True, theta_u=u_truth(t, w["eta"])))


# ----------------------------------------------------------------------------- 5 budgets
def lab_view(cfg, w, which):
    if which not in w:
        nm = cfg["n_mix"]
        sl = slice(0, nm) if which == "A_mix" else slice(nm, None)
        w[which] = NN.view_arrays(VIEW, w["lab_obs"][sl], w["lab_U"][sl], SCALES)
    return w[which]


def stage_finetune(cfg, worlds, Pn, Tn, nb, which, kinds, steps, tag):
    """FT (public-form base, prior conditioning) and CFT (true-form base, conditioning at the truth) on the
    first nb episodes of `which` ('A_mix' or 'A_free') of every world and seed, cross-validated."""
    TH_prior = LL.pad_u(PRI_U[:AN.FT.N_TH])
    tasks = []
    for (ei, t), w in worlds.items():
        A = lab_view(cfg, w, which)
        lc = w["lab_cls"][:cfg["n_mix"]] if which == "A_mix" else w["lab_cls"][cfg["n_mix"]:]
        lc = [str(c) for c in lc[:nb]]                  # the experimenter's own program classes: stratified folds
        for s in range(cfg["seeds"]):
            if "FT" in kinds:
                tasks.append({"id": ("FT", ei, t, s), "base": Pn[s], "A": A, "eps": range(nb), "cls": lc, "TH": TH_prior})
            if "CFT" in kinds:
                tasks.append({"id": ("CFT", ei, t, s), "base": Tn[s], "A": A, "eps": range(nb), "cls": lc,
                              "TH": np.tile(LL.pad_u(u_truth(t, w["eta"])), (AN.FT.N_TH, 1))})
    T1 = worlds[next(iter(worlds))]["lab_obs"].shape[1]
    shapes = AN.fixed_shapes(max(cfg["n_mix"], cfg["n_free"]), T1)
    prm, info, timing = AN.finetune_cv(tasks, shapes, steps, seed=5000 + 97 * nb + (0 if which == "A_mix" else 50000),
                                       log=log, tag=tag)
    # the training rule on the mean cross-validation curve of each group (kind, eta)
    grid = AN.FT.GRID
    groups = {}
    for (kind, ei, t, s), v in info.items():
        groups.setdefault(f"{kind}|eta{cfg['etas'][ei]:g}", []).append(v["curve"])
    rule = {}
    for g, cs in groups.items():
        c = np.mean(np.array(cs), 0)
        rule[g] = {"mean_curve": c.tolist(), "argmin_step": int(np.argmin(c)) * grid,
                   "met": bool(int(np.argmin(c)) * grid <= 0.8 * steps),
                   "chosen_steps_hist": np.bincount(np.array([v["steps"] for k, v in info.items()
                                                              if f"{k[0]}|eta{cfg['etas'][k[1]]:g}" == g]) // grid,
                                                    minlength=steps // grid + 1).tolist()}
    return prm, {"per_net": {"|".join(map(str, k)): v for k, v in info.items()}, "rule": rule, "timing": timing,
                 "steps": int(steps), "rule_met": bool(all(r["met"] for r in rule.values()))}


def lab_means(cfg, worlds, Pn, cache):
    """P0's predictive mean on every Lab episode at the exam's anchor: (n_lab, n_h, 192) per world and seed."""
    m = cfg["m"]
    for (ei, t), w in worlds.items():
        its = AN.lab_items(w["lab_obs"], w["lab_U"], P_)
        for s in range(cfg["seeds"]):
            if (ei, t, s) in cache:
                continue
            rng = np.random.default_rng([4408, ei, t, s])
            S = NN.net_samples(VIEW, Pn[s], its, m, 460 + 7 * t + s, HS, SCALES, cond=True,
                               theta_u=prior_theta(rng, len(its), m))
            cache[(ei, t, s)] = S.mean(1)
        if "lab_struct" not in w:
            U2 = w["lab_U"][:, P_:].astype(float)
            w["lab_struct"] = {"cls": np.array([AN.program_class(u) for u in U2]),
                               "reg": np.stack([AN.region(u) for u in U2]),
                               "z0": AN.block_scaled(w["lab_obs"][:, P_, :LL.NC]),
                               "y": np.stack([AN.block_scaled(w["lab_obs"][:, P_ + h, :LL.NC]) for h in HS], 1)}


def res_samples(cfg, w, mean_lab, S0, eps):
    """RES fitted on the Lab episodes `eps` of world w: P0's samples S0 plus the fitted correction (the
    declared ridge), and the reported variant whose ridge is chosen by leave-one-episode-out."""
    ls = w["lab_struct"]
    eps = np.asarray(list(eps), int)
    R = ls["y"][eps] - AN.block_scaled(mean_lab[eps])
    W = AN.res_fit(ls["z0"][eps], R, ls["reg"][eps], ls["cls"][eps])
    corr = AN.res_apply(W, w["item_z0"], w["item_reg"], w["item_cls"], len(HS))
    Wc, chosen = AN.res_fit_cv(ls["z0"][eps], R, ls["reg"][eps], ls["cls"][eps])
    corr_c = AN.res_apply(Wc, w["item_z0"], w["item_reg"], w["item_cls"], len(HS))
    S0 = S0.astype(np.float64)
    return S0 + corr[:, None], S0 + corr_c[:, None], chosen


def score_budget(cfg, SCO, worlds, nb, ftp, draws, S0c, MLc, which="A_mix", suffix=None):
    m = cfg["m"]
    suffix = f"@{nb}" if suffix is None else suffix
    nm = cfg["n_mix"]
    for (ei, t), w in worlds.items():
        ti = cfg["truths"].index(t)
        items = w["items"]
        for s in range(cfg["seeds"]):
            rng = np.random.default_rng([4409, ei, t, s, nb])
            if ("FT", ei, t, s) in ftp:
                put(SCO, "FT" + suffix, ei, ti, s, w,
                    NN.net_samples(VIEW, ftp[("FT", ei, t, s)], items, m, 470 + 7 * t + s, HS, SCALES, cond=True,
                                   theta_u=prior_theta(rng, len(items), m)))
            if ("CFT", ei, t, s) in ftp:
                put(SCO, "CFT" + suffix, ei, ti, s, w,
                    NN.net_samples(VIEW, ftp[("CFT", ei, t, s)], items, m, 480 + 7 * t + s, HS, SCALES, cond=True,
                                   theta_u=u_truth(t, w["eta"])))
            eps = range(nb) if which == "A_mix" else range(nm, nm + nb)
            Sr, Sc, chosen = res_samples(cfg, w, MLc[(ei, t, s)], S0c[(ei, t, s)], eps)
            put(SCO, "RES" + suffix, ei, ti, s, w, Sr)
            put(SCO, "REScv" + suffix, ei, ti, s, w, Sc)
            RES_LAM.setdefault("RES" + suffix, {})[f"eta{w['eta']:g}|t{t}|s{s}"] = {k: str(v) for k, v in chosen.items()}
            if which == "A_mix" and draws is not None and (ei, t, nb) in draws:
                dr = draws[(ei, t, nb)]
                put(SCO, "S" + suffix, ei, ti, s, w,
                    NN.net_samples(VIEW, ftp["_P"][s], items, m, 440 + 7 * t + s, HS, SCALES, cond=True,
                                   theta_u=dr[rng.choice(len(dr), len(items) * m)].reshape(len(items), m, 4)))


def stage_D(cfg, SCO, worlds, nb, steps):
    """D(nb): round 5's unconditioned net on the first nb Lab mix episodes (seeds) and round 5's block ridge."""
    order = [(ei, t, s) for (ei, t) in worlds for s in range(cfg["seeds"])]
    infos, pD = [], {}
    for s0 in range(0, len(order), NN.Cfg.MAX_LOCK):
        part = order[s0:s0 + NN.Cfg.MAX_LOCK]
        ds = [NN.make_dataset(VIEW, worlds[(ei, t)]["lab_obs"][:nb], worlds[(ei, t)]["lab_U"][:nb], SCALES,
                              seed=100 * nb + 10 * t + s) for ei, t, s in part]
        prm, info = NN.train_nets(VIEW, ds, cond=False, steps=steps, seed=7000 + 13 * nb + s0, deadline=T_END,
                                  log=log if s0 == 0 else None, tag=f"[D({nb}) {steps}]")
        info["order"] = part
        infos.append({k: info[k] for k in ("best_step", "best_val", "steps", "seconds", "stopped_early", "order")})
        pD.update(dict(zip(part, prm)))
    met = bool(all(b <= 0.8 * i["steps"] for i in infos for b in i["best_step"]))
    for (ei, t), w in worlds.items():
        ti = cfg["truths"].index(t)
        for s in range(cfg["seeds"]):
            put(SCO, f"Dnet@{nb}", ei, ti, s, w,
                NN.net_samples(VIEW, pD[(ei, t, s)], w["items"], cfg["m"], 450 + 7 * t + s, HS, SCALES))
        Sr = LL.ridge_samples(VIEW, LL.ridge_fit(VIEW, w["lab_obs"][:nb], w["lab_U"][:nb], HS, SCALES), w["items"],
                              cfg["m"], 0, HS, SCALES)
        for s in range(cfg["seeds"]):
            put(SCO, f"Dridge@{nb}", ei, ti, s, w, Sr)
    return {"groups": infos, "rule_met": met, "steps": int(steps)}


# ----------------------------------------------------------------------------- the pipeline
def pipeline(cfg, out_dir, est=None):
    """est: seconds per stage projected from the presmoke (None in the presmoke itself)."""
    STATE["out"] = out_dir
    os.makedirs(out_dir, exist_ok=True)
    times, TR = {}, {"base": [], "ft": {}, "D": {}}
    nE, nT, nS = len(cfg["etas"]), len(cfg["truths"]), cfg["seeds"]
    info = dict(INFO, config=cfg_json(cfg), member_ticks_planned=estimate_ticks(cfg))
    info["member_ticks_planned"]["total"] = int(sum(info["member_ticks_planned"].values()))
    log(f"pipeline -> {out_dir}: {nT} truths x eta {list(cfg['etas'])}, member-ticks planned "
        f"{info['member_ticks_planned']['total']:,}")

    def flush(stage):
        info.update(times=times, failed=FAILED, skipped=SKIPPED, notes=NOTES, stage_done=stage,
                    hours=(time.time() - T0) / 3600)
        jdump("info.json", info)
        jdump("train_info.json", {**TR, "res_cv_ridge": RES_LAM})

    def fits(stage, need_after=0.0):
        """True if the presmoke's estimate of `stage` (plus what must still follow) fits the time left."""
        if est is None:
            return True
        need = est.get(stage, 0.0) + need_after + 90.0
        if left() < need:
            SKIPPED.append(f"{stage}: {left() / 60:.1f} min left, about {need / 60:.1f} min needed")
            log(f"SKIP {stage}: {left() / 60:.1f} min left, about {need / 60:.1f} min needed")
            return False
        return True

    fam = None
    if not EXT:
        with Timer("1 families", times):
            fam, info["family_check"] = stage_families(cfg, times)
    with Timer("2 worlds", times):
        worlds = stage_worlds(cfg, times)
    info["lab"] = {f"eta{w['eta']:g}|t{w['truth']}": {"usage": w["lab_usage"], "classes_first_8": w["lab_cls"][:8].tolist(),
                                                     "nats_by_class": {c: float(w["lab_nats"][:cfg["n_mix"]][w["lab_cls"][:cfg["n_mix"]] == c].mean())
                                                                       for c in LL.MIXC},
                                                     "c0_block_sum_lost_over_program_by_class": lab_c0_loss(cfg, w),
                                                     "structural_class_agreement_items": w["class_agree"],
                                                     "structural_class_agreement_lab": float(np.mean(
                                                         np.array([AN.program_class(u) for u in w["lab_U"][:, P_:].astype(float)]) == w["lab_cls"]))}
                   for w in worlds.values()}
    SCO = {"_shape": (nE, nT, nS, 2, cfg["n_items"], len(HS))}
    for (ei, t), w in worlds.items():
        ti = cfg["truths"].index(t)
        for name in ("K", "O", "plug"):
            if name not in SCO:
                SCO[name] = np.full(SCO["_shape"], np.nan, np.float32)
            SCO[name][ei, ti, :] = np.stack([w["exams"]["sel"]["ref"][name], w["exams"]["score"]["ref"][name]])[None]
    save_scores(cfg, SCO, worlds)
    flush("worlds")
    draws = None
    try:
        with Timer("3 scripted inference", times):
            draws = stage_identify(cfg, fam, worlds)
    except Exception as exc:
        FAILED.append(f"identification: {exc!r}"[:300])
        log(f"  identification FAILED: {exc!r}\n{traceback.format_exc()}")

    # ---- base nets: the schedule doubles while the rule is unmet
    Pn = Tn = None
    S0c, MLc = {}, {}
    rest = 0.0 if est is None else est["N8"] + est["D_first"] + est["final"]
    for r, steps in enumerate(cfg["rungs"]):
        if r > 0 and TR["base"][-1]["rule_met"] and not cfg["timing_runs"]:
            break
        if r > 0 and not fits(f"base_{steps}", rest):
            NOTES.append(f"training rule: the doubling to {steps} steps was cut by the clock")
            break
        with Timer(f"4 base nets, {steps} steps", times):
            Pn, Tn, inf = train_base(cfg, fam, steps, f"[base {steps}]")
            TR["base"].append({k: inf[k] for k in ("steps", "best_step", "best_val", "hist", "seconds", "rule_met",
                                                   "stopped_early", "net_order", "log_lines", "n_train_examples",
                                                   "n_episodes")})
            log(f"  base {steps}: best steps {inf['best_step']} best val {np.round(inf['best_val'], 4).tolist()} "
                f"rule met {inf['rule_met']} ({inf['seconds'] / max(inf['steps'], 1) * 1e3:.1f} ms/step with validation)")
        with Timer(f"4 scoring rung {steps}", times):
            S0c.clear()
            score_base(cfg, SCO, worlds, Pn, Tn, f"@r{steps}", keep=S0c)
        save_scores(cfg, SCO, worlds)
        flush(f"base_{steps}")
    if EXT:                                             # the first job's base nets, not retrained
        with Timer("4 base nets loaded and scored", times):
            zn = np.load(os.path.join(args.prior, "nets.npz"))
            tmpl = NN.init_params(VIEW, jax.random.key(0), True)
            Pn = [AN.tree_from_arrays(f"P{s}", zn, tmpl) for s in range(nS)]
            Tn = [AN.tree_from_arrays(f"T{s}", zn, tmpl) for s in range(nS)]
            final_steps = int(zn["steps"])
            score_base(cfg, SCO, worlds, Pn, Tn, "", keep=S0c)
        info["base_final_steps"] = final_steps
        info["base_nets_from"] = os.path.relpath(os.path.join(args.prior, "nets.npz"), HERE)
        save_scores(cfg, SCO, worlds)
        flush("base_loaded")
    else:
        final_steps = TR["base"][-1]["steps"]
        for k in ("P0", "Cpub", "Ctrue"):
            SCO[k] = SCO[f"{k}@r{final_steps}"].copy()
        info["base_final_steps"] = int(final_steps)
        info["base_rule_met"] = bool(TR["base"][-1]["rule_met"])
        if not info["base_rule_met"]:
            NOTES.append(f"training rule: base nets not converged by the rule at {final_steps} steps")
        arrs = {}
        for s in range(nS):
            arrs.update(AN.tree_to_arrays(f"P{s}", Pn[s]))
            arrs.update(AN.tree_to_arrays(f"T{s}", Tn[s]))
        npz("nets.npz", steps=np.array(final_steps), **arrs)
    with Timer("5 P0 on the Lab episodes", times):
        lab_means(cfg, worlds, Pn, MLc)
    quick(cfg, SCO, worlds, "after the base nets")

    def declared_after(nb):
        """Seconds the stages that the plan declares still need after budget nb's fine-tunes (presmoke's
        estimates): D at round 5's column, the budgets not yet run, the final writes."""
        i = cfg["budgets"].index(nb)
        return (est["D_first"] if i == 0 else 0.0) + sum(est[f"N{b}"] for b in cfg["budgets"][i + 1:]) + est["final"]

    def budget(nb, key, kinds=("FT", "CFT")):
        steps, k = cfg["ft_steps"], 0
        while True:
            with Timer(f"5 fine-tuning N={nb}, {steps} steps", times):
                ftp, inf = stage_finetune(cfg, worlds, Pn, Tn, nb, "A_mix", kinds, steps, f"[N={nb}]")
            TR["ft"].setdefault(str(nb), []).append(inf)
            log(f"  N={nb}: rule on the mean CV curves " + ", ".join(f"{g} min at {v['argmin_step']}" for g, v in inf["rule"].items())
                + f"; {inf['timing']['ms_per_lockstep_step_median']} ms per lockstep step")
            if inf["rule_met"] or k >= cfg["ft_doublings"]:
                break
            if est is not None and left() < 2.2 * times.get(f"5 fine-tuning N={nb}, {steps} steps", 0.0) + declared_after(nb) + 240:
                NOTES.append(f"training rule: fine-tunes at N={nb} not doubled past {steps} steps (clock)")
                break
            steps, k = 2 * steps, k + 1
        if not inf["rule_met"]:
            NOTES.append(f"training rule: fine-tunes at N={nb} not converged by the rule at {steps} steps")
        ftp["_P"] = Pn
        with Timer(f"5 scoring N={nb}", times):
            score_budget(cfg, SCO, worlds, nb, ftp, draws, S0c, MLc)
        save_scores(cfg, SCO, worlds)
        flush(key)

    def dstage(nb):
        steps, k = cfg["steps_d"], 0
        while True:
            with Timer(f"5 D({nb}), {steps} steps", times):
                inf = stage_D(cfg, SCO, worlds, nb, steps)
            TR["D"].setdefault(str(nb), []).append(inf)
            if inf["rule_met"] or k >= cfg["d_doublings"]:
                break
            steps, k = 2 * steps, k + 1
        if not inf["rule_met"]:
            NOTES.append(f"training rule: D({nb}) not converged by the rule at {steps} steps")
        save_scores(cfg, SCO, worlds)
        flush(f"D{nb}")

    b0 = cfg["budgets"][0]
    budget(b0, "N8")                                     # the primary budget: required
    quick(cfg, SCO, worlds, f"after N={b0}")
    dstage(cfg["d_first"])                               # D at round 5's column: required for sigma at the zero point
    for nb in cfg["budgets"][1:]:
        if fits(f"N{nb}"):
            try:
                budget(nb, f"N{nb}")
            except Exception as exc:
                FAILED.append(f"N={nb}: {exc!r}"[:300])
                log(f"  N={nb} FAILED: {exc!r}\n{traceback.format_exc()}")
    if fits("ctrl"):
        try:
            nc = cfg["n_ctrl"]
            with Timer(f"5 control: FT and RES on {nc} input-free Lab episodes", times):
                ftp, inf = stage_finetune(cfg, worlds, Pn, Tn, nc, "A_free", ("FT",), cfg["ft_steps"], "[free]")
                TR["ft"]["free"] = [inf]
                ftp["_P"] = Pn
                score_budget(cfg, SCO, worlds, nc, ftp, None, S0c, MLc, which="A_free", suffix=f"free@{nc}")
            save_scores(cfg, SCO, worlds)
            flush("ctrl")
        except Exception as exc:
            FAILED.append(f"control: {exc!r}"[:300])
            log(f"  control FAILED: {exc!r}\n{traceback.format_exc()}")
    for nb in cfg["budgets"]:
        if nb != cfg["d_first"] and fits(f"D{nb}"):
            try:
                dstage(nb)
            except Exception as exc:
                FAILED.append(f"D({nb}): {exc!r}"[:300])
                log(f"  D({nb}) FAILED: {exc!r}\n{traceback.format_exc()}")
    info["member_ticks_total"] = info["member_ticks_planned"]["total"]
    quick(cfg, SCO, worlds, "final")
    flush("done")
    return times, TR, info


def quick(cfg, SCO, worlds, when):
    """A first look in the log (the criteria come from make_summary.py; this must never stop the job)."""
    try:
        d = {k: v for k, v in SCO.items() if not k.startswith("_")}
        cl = np.array([[np.stack([worlds[(ei, t)]["exams"][h]["classes"] for h in ("sel", "score")])
                        for t in cfg["truths"]] for ei in range(len(cfg["etas"]))])
        rep = ST.first_look(d, cl, list(cfg["etas"]), cfg["budgets"][0], cfg["d_first"])
        log(f"first look {when}: " + json.dumps(rep))
        jdump("first_look.json", {"when": when, **rep})
    except Exception as exc:
        log(f"first look {when} not available: {exc!r}")


def presmoke():
    """Full shapes, small counts; the zero point of the switch on this backend; the speed guard."""
    out = os.path.join(ROOT_OUT, "presmoke")
    STATE["out"] = out
    os.makedirs(out, exist_ok=True)
    with Timer("0 zero point of the law switch"):
        z = X.one_tick_check(B=4 if args.smoke else 64, burn=1 if args.smoke else 4)
        tol = 0.0 if jax.default_backend() == "cpu" else max(1e-8, 100.0 * z["max_abs_gworld_rerun"])
        z["tolerance"] = tol
        z["ok"] = bool(z["max_abs_xw0_minus_gworld"] <= tol and z["max_abs_xw4_minus_gworld"] > 1e-3
                       and z["total_mass_rel_change_xw4"] < 1e-9)
        jdump("zero_point.json", z)
        log("  " + json.dumps(z))
        if not z["ok"]:
            raise RuntimeError("the law switch at xw = 0 is not gworld.tick on this backend")
    times, TR, info = pipeline(PRE, out)
    if FAILED:
        raise RuntimeError(f"presmoke: failed parts {FAILED}")
    # ---- projection for the full pass (stages measured after their programs were compiled)
    c, p = FULL, PRE
    nw = len(c["truths"]) * len(c["etas"])
    nwp = len(p["truths"]) * len(p["etas"])
    t_world = nw * float(np.min(times["world_seconds"]))
    if EXT:
        t_fam, ms_base = 0.0, 0.02                         # no base training; D nets at a prior of 20 ms per step
    else:
        fr = times["family_rates"]
        n_chunks = -(-c["n_theta"] * 4 * c["Kc"] // c["chunk"])
        t_fam = sum(n_chunks * fr[k]["seconds_last_chunk"] for k in ("pub", "true"))
        b_fast = TR["base"][-1]                            # the second base run: compiled before
        ms_base = b_fast["seconds"] / max(b_fast["steps"], 1)
        sc_rung = times[f"4 scoring rung {p['rungs'][-1]}"] / nwp * nw
    est = {"families": t_fam, "worlds": t_world, "final": 120.0, "seconds_per_base_step": ms_base}
    for st in c["rungs"]:
        est[f"base_{st}"] = st * ms_base + sc_rung
    med = lambda v: float(np.median(v[1:] if len(v) > 1 else v)) if len(v) else 0.0
    for nb in c["budgets"]:
        tm = TR["ft"][str(nb)][-1]["timing"]
        k_cv = len(AN.folds_of(nb))
        inst = nw * c["seeds"] * 2
        g_cv, g_fin = -(-inst * k_cv // AN.FT.LOCK), -(-inst // AN.FT.LOCK)
        sc = c["ft_steps"] / p["ft_steps"]
        est[f"N{nb}"] = (g_cv * med(tm["group_seconds_cv"]) + g_fin * med(tm["group_seconds_final"] or tm["group_seconds_cv"])) * sc \
            + times[f"5 scoring N={nb}"] / nwp * nw
        est[f"D{nb}"] = -(-nw * c["seeds"] // NN.Cfg.MAX_LOCK) * c["steps_d"] * ms_base * NN.Cfg.MAX_LOCK / (2 * c["seeds"]) + 90.0
    est["N8"] = est[f"N{c['budgets'][0]}"]
    est["D_first"] = est[f"D{c['d_first']}"]
    est["ctrl"] = 0.5 * est["N8"]
    required = (est["families"] + est["worlds"] + (est[f"base_{c['rungs'][0]}"] if c["rungs"] else 0.0) + est["N8"]
                + est["D_first"] + est["final"])
    everything = required + sum(est[f"base_{st}"] for st in c["rungs"][1:]) + sum(est[f"N{nb}"] for nb in c["budgets"][1:]) \
        + est["ctrl"] + sum(est[f"D{nb}"] for nb in c["budgets"] if nb != c["d_first"])
    g = {"estimates_seconds": est, "required_seconds": required, "everything_seconds": everything,
         "seconds_left": left(), "presmoke_seconds": time.time() - T0,
         "note": "per-stage times are upper estimates: presmoke stages include compilation where a stage ran once",
         "ok": bool(required < 0.95 * left())}
    jdump("guard.json", g)
    log(f"speed guard: required {required / 60:.1f} min, everything {everything / 60:.1f} min, left {left() / 60:.1f} min "
        f"-> {'go' if g['ok'] else 'STOP'}; estimates " + json.dumps({k: round(v) for k, v in est.items()}))
    return g


if __name__ == "__main__":
    try:
        est = None
        if not args.no_presmoke:
            g = presmoke()
            if not g["ok"]:
                log("FATAL: the measured rates cannot finish the required stages inside --max-hours")
                sys.exit(4)
            est = g["estimates_seconds"]
        FAILED.clear(), SKIPPED.clear(), NOTES.clear(), RES_LAM.clear()
        times, TR, info = pipeline(FULL, ROOT_OUT, est)
    except SystemExit:
        raise
    except Exception as exc:
        log(f"FATAL {exc!r}\n{traceback.format_exc()}")
        try:
            jdump("fatal.json", {"fatal": repr(exc), "failed": FAILED, "skipped": SKIPPED})
        except Exception:
            pass
        sys.exit(1)
    log(f"done in {(time.time() - T0) / 3600:.2f} h; failed {FAILED}; skipped {SKIPPED}; notes {NOTES}")
    if FAILED:
        sys.exit(2)
