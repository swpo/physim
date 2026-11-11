"""run_a2 -- study dialsA2 of round 6: the gliders stress-conversion exam reopened with a triggered bar (GPU job).

PILOT ONLY: the truths are public pilot values; the Lab data, items and nets written here must NEVER be reused as an
exam. The world secret (256 bits, os.urandom) is never written; only its commitment. What is declared is in
DECLARED.md (committed at 3fd4076c5, 19:26 UTC, before this file existed); what this file does, in order:

  0 presmoke  the same pipeline at FULL SHAPES and small counts (one truth at eta 0 and 4 plus the eta-1 arm, 512
              episodes per family tiled to 6,144 for the nets' shapes, a few hundred steps per net), the zero point
              of the law switch on this backend, then a speed guard (exit 4 if the required stages cannot finish
              inside --max-hours). Same process, so the full pass reuses every compiled program.
  1 truths    round 5's 8 and the first 8 viable of 48 box draws (seed [6601, 4]; DECLARED R3).
  2 families  public, true-form (eta 0 / 4 / uniform), designed (H's emulator): 768 points x 8 episodes each.
  3 worlds    16 truths x eta {0, 4}: Lab (32 aimed/regional + 32 input-free + 32 designed), two exams of 48
              aimed/regional items x 12 replicates (`sel`, `score`), K and O.
  4 inference S (round 5's, public law), H (designed episodes), H_mix (mix episodes): posterior draws.
  5 base nets public-form and true-form, 3 seeds each, in lockstep, 50 steps per dispatch; 24,000 steps, doubled
              while the training rule is unmet, at most to 192,000; every rung scored (P0, Cpub, Ctrue).
  6 N = 8     FT and CFT (rates 1e-4, 2e-5, grid 10 steps, widened by DECLARED R11), RES (cross-validated ridge)
              and RESfix, S, H, H_mix, blind C, D(8); then N = 32; then eta 1 and 2 for truths 0-3 (N = 8).
Scores: fair energy score per item and horizon (8, 12, 16) through the exam's own scorer (ladder_lib.ViewCells).
The criteria are computed from scores.npz by make_summary.py (a2_stats.py); the job prints a first look.

usage: python -B run_a2.py --out DIR [--max-hours 3.6] [--smoke] [--cpu-ok] [--no-presmoke]
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
import a2_lib as A2  # noqa: E402
import a2_stats as ST  # noqa: E402

X, AN = A2.X, A2.AN
import jax  # noqa: E402
import numpy as np  # noqa: E402

from vw.scoring import energy_fair, energy_loo  # noqa: E402
from vw.harness import ProgramMix  # noqa: E402
from vw.secret import Secret  # noqa: E402
from vw.world import make_key, member_keys  # noqa: E402

LL, NN, SL, GW, PL = X.LL, X.NN, X.SL, X.GW, X.PL
VIEW = "block"

ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
ap.add_argument("--max-hours", type=float, default=3.6, help="the script's own limit (the request's is larger)")
ap.add_argument("--smoke", action="store_true", help="tiny shapes for a CPU test of the code path")
ap.add_argument("--cpu-ok", action="store_true", help="allow a CPU backend (tests only)")
ap.add_argument("--no-presmoke", action="store_true")
args = ap.parse_args()
ROOT_OUT = args.out
os.makedirs(ROOT_OUT, exist_ok=True)
T0 = time.time()
T_END = T0 + args.max_hours * 3600
PILOT = "PILOT_NEVER_REUSE_AS_EXAM"

FULL = dict(P=16, H=16, burn=GW.BURN, n_theta=768, Kc=4, chunk=256, tile=1, truths=list(range(16)), etas=(0.0, 4.0),
            x_truths=[0, 1, 2, 3], x_etas=(1.0, 2.0), n_mix=32, n_free=32, n_des=32, n_items=48, R=12, n_clim=48, m=32,
            budgets=(8, 32), hs=(8, 12, 16), lags=(0, 1, 2, 4, 8), rungs=(24000, 48000, 96000, 192000),
            steps_d=1200, d_doublings=2, d_eval=50, ft_steps=400, ft_rates=(1e-4, 2e-5), ft_widen=2, seeds=3,
            post_M=20_000, n_ext=8, ext_cand=48, viab_T=100, timing_runs=False)
# presmoke: every stage once at the full shapes (chunk 256, 576-member truth rollouts, 6 base nets on 6,144 episodes,
# 16 fine-tunes in lockstep, 96-item sampling); small counts
PRE = dict(FULL, n_theta=64, tile=12, truths=[0], x_truths=[0], x_etas=(1.0,), rungs=(250, 500), steps_d=100,
           d_doublings=0, ft_steps=80, ft_widen=0, post_M=4000, timing_runs=True)
SMOKE = dict(P=4, H=4, burn=2, n_theta=8, Kc=1, chunk=8, tile=1, truths=[0, 8], etas=(0.0, 4.0), x_truths=[0],
             x_etas=(1.0,), n_mix=8, n_free=2, n_des=8, n_items=4, R=3, n_clim=4, m=4, budgets=(4, 8), hs=(1, 2, 4),
             lags=(0, 1, 2, 4), rungs=(50, 100), steps_d=50, d_doublings=1, d_eval=50, ft_steps=80,
             ft_rates=(1e-4, 2e-5), ft_widen=1, seeds=2, post_M=2000, n_ext=1, ext_cand=6, viab_T=6, timing_runs=False)
if args.smoke:
    FULL = SMOKE
    PRE = dict(SMOKE, rungs=(50,), d_doublings=0, ft_widen=0, truths=[0], timing_runs=True)
    NN.Cfg.EVAL_EVERY, NN.Cfg.BATCH, NN.Cfg.M_TRAIN, NN.Cfg.C, NN.Cfg.BLOCKS = 50, 8, 2, 8, 1
    NN.Cfg.N_VAL, NN.Cfg.EVAL_ROWS, NN.Cfg.EVAL_DRAWS = 16, 8, 2
    AN.FT.BATCH, AN.FT.LOCK, AN.FT.N_TH, AN.FT.N_VAL = 4, 4, 16, 16
    A2.TRN.SCAN = 25
NN.Cfg.LAGS, NN.Cfg.HS = tuple(FULL["lags"]), tuple(FULL["hs"])
AN.FT.GRID = 10                                    # DECLARED R11: held-out score every 10 steps
HS = list(FULL["hs"])
P_, H_ = FULL["P"], FULL["H"]
PER_EP = 1 + P_ + H_
EP_T = FULL["burn"] + P_ + H_
SCALES = {"SC1": LL.SC1}
FAILED, SKIPPED, NOTES = [], [], []
RES_LAM = {}
STATE = {"out": ROOT_OUT}
MIX2 = ProgramMix({"c": LL.CLASSES["c"], "d": LL.CLASSES["d"]})       # the exam's public mix (DECLARED R2)


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
PV5 = A2.Prior5(PV)
PRI_U, PM, PSD = LL.prior_draws(PV, 4, 4096, np.random.default_rng([4404, 4]))
assert np.allclose(PM, _prior["prior_mean_u"], atol=0.02), "the viability prior is not round 5's"
RN = SL.VRunner(burn=FULL["burn"])
XR = X.XRunner(burn=FULL["burn"])
WORLD = X.build_world_x(X.xparams(NAMES, TRUTHS[0], 0.0), burn=FULL["burn"])

# ---- DECLARED R3: truths 8-15, the first 8 viable of 48 box draws (seed [6601, 4]), round 5's viability rule
import viab_joint as VJ  # noqa: E402
VJ.T = FULL["viab_T"]
_t = time.time()
_cand = LO + (HI - LO) * np.random.default_rng([6601, 4]).random((FULL["ext_cand"], 4))
_rows, _ = VJ.viability(NAMES, _cand, member_keys(make_key(6601, 4), FULL["ext_cand"]), RN=RN)
_okv = [bool(r["viable"]) for r in _rows]
_new = [c for c, v in zip(_cand, _okv) if v][:FULL["n_ext"]]
if len(_new) < FULL["n_ext"]:
    if not args.smoke:
        log(f"FATAL: only {len(_new)} viable candidates for truths 8-15")
        sys.exit(5)
    _new = (_new + list(_cand))[:FULL["n_ext"]]
TRUTHS = np.concatenate([TRUTHS, np.array(_new)])
log(f"truths 8-{len(TRUTHS) - 1}: {np.round(np.array(_new), 3).tolist()} ({sum(_okv)}/{len(_cand)} candidates viable, "
    f"{time.time() - _t:.0f}s)")
X.assert_one_checkout()
INFO = {"study": "round6/dials/dialsA2 (the gliders stress-conversion exam reopened with a triggered bar)",
        "versions": {"python": platform.python_version(), "jax": jax.__version__, "numpy": np.__version__},
        "backend": jax.default_backend(), "devices": [str(d) for d in jax.devices()], "smoke": args.smoke,
        "x64": bool(jax.config.jax_enable_x64), "max_hours": args.max_hours, "secret_commitment": SEC.commitment(),
        "modules": X.module_files(), "names": NAMES, "lo": LO.tolist(), "hi": HI.tolist(), "truths": TRUTHS.tolist(),
        "truths_rule": "0-7 round5/ladder/results/job/n4/truths.json; 8-15 first viable of box draws, numpy seed "
                       "[6601, 4], viab_joint.viability under the public law (DECLARED R3)",
        "truth_candidates": _cand.tolist(), "truth_candidates_viable": _okv,
        "law": {"term": "XW stress conversion (defect_gliders/dlaw.py)", "W0": X.W0, "DW": X.DW, "KXW": X.KXW},
        "designed_arms": [{"nats_per_tick": a[0], "ticks": a[1], "target": a[2]} for a in A2.ARMS],
        "net": {k: getattr(NN.Cfg, k) for k in dir(NN.Cfg) if k.isupper()},
        "ft": {k: getattr(AN.FT, k) for k in dir(AN.FT) if k.isupper()},
        "trainer": {"steps_per_dispatch_base_D": A2.TRN.SCAN, "ft_steps_per_dispatch": A2.TRN.FT_DISPATCH * AN.FT.GRID},
        "grader": "fair energy score per item and horizon: vw.harness.HistoryExam._per_cell + vw.scoring.energy_fair "
                  "through ladder_lib.ViewCells; L = sum over horizons 8, 12, 16, mean over items (acceptance.py)"}


def cfg_json(cfg):
    return {k: (list(v) if isinstance(v, (tuple, list)) else v) for k, v in cfg.items()}


def estimate_ticks(cfg):
    nw = len(cfg["truths"]) * len(cfg["etas"]) + len(cfg["x_truths"]) * len(cfg["x_etas"])
    ni, R, b = cfg["n_items"], cfg["R"], cfg["burn"]
    return {"families": cfg["n_theta"] * (2 * 2 * cfg["Kc"] + len(A2.ARMS)) * EP_T,
            "lab": nw * (cfg["n_mix"] + cfg["n_free"] + cfg["n_des"]) * (b + PER_EP),
            "exams": nw * 2 * (ni * (b + P_) + ni * R * H_ + cfg["n_clim"] * (b + H_))}


# ----------------------------------------------------------------------------- 2 families
def stage_families(cfg, times):
    N = cfg["n_theta"]
    KD = 2 * cfg["Kc"]                                   # Kc aimed + Kc regional per point
    cls = np.tile(np.array([c for c in A2.TRIG for _ in range(cfg["Kc"])]), N)
    fam, rates = {}, {}
    for name, tag in (("pub", 0), ("true", 1), ("des", 2)):
        rng = np.random.default_rng([6602, tag])
        Ud = rng.uniform(-1, 1, (N, 4))
        th = np.repeat(CEN + Ud * HW, KD if name != "des" else len(A2.ARMS), 0)
        stamps = [time.time()]
        lg = lambda m: stamps.append(time.time())
        if name == "pub":
            keys = member_keys(make_key(6602, tag), N * KD)
            sim = LL.sim_episodes(RN, NAMES, th, keys, 6602, P_, H_, cfg["chunk"], classes=cls, log=lg)
            eta_pt = np.zeros(N)
            th_u = np.repeat(Ud, KD, 0)
            kd = KD
        elif name == "true":
            keys = member_keys(make_key(6602, tag), N * KD)
            eta_pt = np.zeros(N)
            perm = rng.permutation(N)
            eta_pt[perm[N // 4:N // 2]] = 4.0
            eta_pt[perm[N // 2:]] = rng.uniform(0.0, 4.0, N - N // 2)
            sim = X.sim_episodes_x(XR, NAMES, th, np.repeat(eta_pt, KD), keys, 6603, P_, H_, cfg["chunk"], classes=cls, log=lg)
            th_u = np.concatenate([np.repeat(Ud, KD, 0), np.repeat(eta_pt, KD)[:, None] / 4.0], 1)
            kd = KD
        else:
            kd = len(A2.ARMS)
            keys = member_keys(make_key(6602, tag), N * kd)
            eta_pt = rng.uniform(0.0, A2.ETA_MAX, N)
            dcls = np.tile(np.array(A2.DES), N)
            sim = A2.sim_designed(XR, NAMES, th, np.repeat(eta_pt, kd), keys, 6604, P_, H_, cfg["chunk"], classes=dcls, log=lg)
            th_u = None
        d = np.diff(stamps)
        rates[name] = {"member_ticks": N * kd * EP_T, "seconds": float(d.sum()), "seconds_last_chunk": float(d[-1]),
                       "rate_last_chunk": float(cfg["chunk"] * EP_T / d[-1])}
        fam[name] = {"Ud": Ud, "eta_pt": eta_pt, "obs": sim["obs"], "U": sim["U"], "cls": np.asarray(sim["cls"]),
                     "th_u": th_u, "nats": sim["nats"], "KD": kd}
        log(f"  family {name}: {N} points x {kd} episodes, {d.sum():.0f}s, last chunk {rates[name]['rate_last_chunk']:.0f} "
            f"member-ticks/s; nats by class " + str({c: round(float(sim['nats'][np.asarray(sim['cls']) == c].mean()), 1)
                                                     for c in sorted(set(np.asarray(sim['cls']).tolist()))}))
    times["family_rates"] = rates
    out = {}
    for name in ("true", "des"):
        f = fam[name]
        F = A2.summaries(f["obs"], f["U"], P_)
        eta_ep = np.repeat(f["eta_pt"], f["KD"])
        for c in sorted(set(f["cls"].tolist())):
            for lo, hi in ((0.0, 0.0), (3.99, 4.0), (0.01, 2.0), (2.0, 3.99)):
                m = (f["cls"] == c) & (eta_ep >= lo) & (eta_ep <= hi)
                if m.any():
                    out[f"{name}|{c}|eta[{lo:g},{hi:g}]|c0_lost_16"] = float(F[m, 13 + 4].mean())
    log("  channel-0 block sum lost 16 ticks after the anchor: " + ", ".join(f"{k} {v:+.3f}" for k, v in out.items()))
    return fam, out


# ----------------------------------------------------------------------------- 3 worlds
def lab_classes(cfg, t):
    arng = np.random.default_rng([7700, int(t)])
    mix = np.concatenate([arng.permutation(np.array(A2.TRIG)) for _ in range(cfg["n_mix"] // 2)])
    des = np.concatenate([arng.permutation(np.array(A2.DES)) for _ in range(cfg["n_des"] // len(A2.DES))])
    return np.concatenate([mix, np.array(["a"] * cfg["n_free"]), des])


def lab_slices(cfg):
    nm, nf = cfg["n_mix"], cfg["n_free"]
    return {"mix": slice(0, nm), "free": slice(nm, nm + nf), "des": slice(nm + nf, nm + nf + cfg["n_des"])}


def make_worlds(cfg, etas, truths, times, tag):
    """Per (eta, truth): Lab data, two exams, K and O. The seeds depend on the truth only, so the dial values
    are nested: the same starts, noise and Lab programs' random numbers."""
    worlds, secs = {}, []
    n_lab = cfg["n_mix"] + cfg["n_free"] + cfg["n_des"]
    ni = cfg["n_items"]
    for ei, eta in enumerate(etas):
        for t in truths:
            t_w = time.time()
            p_true = X.xparams(NAMES, TRUTHS[t], eta)
            WORLD.params = p_true
            lab = SL.BatchLab(WORLD, SEC.child("lab", int(t)), nats=PL.budget(total=SL.EP_CAP * n_lab),
                              max_ticks=n_lab * PER_EP)
            classes = lab_classes(cfg, t)

            def mk(j, hist, t=t, classes=classes):
                return A2.CLASSES[classes[j]](np.random.default_rng([7701, int(t), j]), hist, H_, SL.EP_CAP)
            r = lab.run_batch(list(range(n_lab)), P_, H_, mk)
            w = {"eta": float(eta), "truth": int(t), "lab_obs": r["obs"], "lab_U": r["U"], "lab_cls": classes,
                 "lab_nats": r["nats"], "lab_usage": lab.usage(), "exams": {}}
            for half in ("sel", "score"):
                WORLD.params = p_true
                ex = PL.GExam(WORLD, SEC.child("truth", int(t)), MIX2, n_items=ni, prefix=P_, queries={1: HS},
                              R=cfg["R"], derived=LL.DERIVED, scales={1: LL.SC1}, nats=PL.budget(),
                              n_clim=cfg["n_clim"], name=f"dialsA2-{half}")
                vc = LL.ViewCells(ex, 1)
                ref = {"O": ex._per_cell(None, lambda Y, s, l: energy_loo(Y, s, True)),
                       "K": ex._per_cell(lambda Xs, Y, s, l: energy_fair(Xs, Y, s), pool=ex.clim)}
                ex._snap = None
                w["exams"][half] = {"vc": vc, "items": ex.public(), "classes": ex.classes, "ref": ref}
            w["items"] = w["exams"]["sel"]["items"] + w["exams"]["score"]["items"]
            Ud = np.stack([LL.program_dense(it["program"], H_, LL.NW) for it in w["items"]])
            w["item_cls"] = np.array([AN.program_class(u) for u in Ud])
            w["item_reg"] = np.stack([AN.region(u) for u in Ud])
            w["item_z0"] = AN.block_scaled(np.stack([np.asarray(it["history"], float)[-1, :LL.NC] for it in w["items"]]))
            w["items_blind"] = [{**it, "program": []} for it in w["items"]]
            true_cls = np.concatenate([w["exams"]["sel"]["classes"], w["exams"]["score"]["classes"]])
            w["class_agree"] = float(np.mean(w["item_cls"] == true_cls))
            worlds[(ei, int(t))] = w
            secs.append(time.time() - t_w)
            log(f"  {tag} world eta={eta:g} truth {t}: {secs[-1]:.0f}s; lab {w['lab_usage']['ticks_used']} ticks "
                f"{w['lab_usage']['total_nats']:.0f} nats; structural class = mix class on {w['class_agree']:.3f} of items")
    times.setdefault("world_seconds", []).extend(secs)
    return worlds


def lab_record(cfg, worlds):
    sl = lab_slices(cfg)
    out = {}
    for w in worlds.values():
        c0 = w["lab_obs"][:, :, :64].astype(float).sum(-1)
        drop = 1.0 - c0[:, -1] / np.maximum(c0[:, P_], 1e-9)
        cls = w["lab_cls"]
        out[f"eta{w['eta']:g}|t{w['truth']}"] = {
            "usage": w["lab_usage"], "classes_mix_first_8": cls[sl["mix"]][:8].tolist(),
            "classes_des_first_8": cls[sl["des"]][:8].tolist(),
            "nats_by_class": {c: float(w["lab_nats"][cls == c].mean()) for c in sorted(set(cls.tolist()))},
            "c0_block_sum_lost_over_program_by_class": {c: float(drop[cls == c].mean()) for c in sorted(set(cls.tolist()))},
            "structural_class_agreement_items": w["class_agree"]}
    return out


def put(SCO, name, ei, ti, s, w, S):
    """Score samples S (2 n_items, m, n_h, 192) of one world (sel items first) and store (2, n_items, n_h)."""
    ni = len(w["exams"]["sel"]["items"])
    a = np.stack([w["exams"]["sel"]["vc"].score(S[:ni]), w["exams"]["score"]["vc"].score(S[ni:])])
    if name not in SCO:
        SCO[name] = np.full(SCO["_shape"], np.nan, np.float32)
    SCO[name][ei, ti, s] = a


def new_sco(cfg, etas, truths, worlds):
    SCO = {"_shape": (len(etas), len(truths), cfg["seeds"], 2, cfg["n_items"], len(HS)), "_etas": etas, "_truths": truths}
    for (ei, t), w in worlds.items():
        ti = truths.index(t)
        for name in ("K", "O"):
            if name not in SCO:
                SCO[name] = np.full(SCO["_shape"], np.nan, np.float32)
            SCO[name][ei, ti, :] = np.stack([w["exams"]["sel"]["ref"][name], w["exams"]["score"]["ref"][name]])[None]
    return SCO


def classes_of(SCO, worlds):
    return np.array([[np.stack([worlds[(ei, t)]["exams"][h]["classes"] for h in ("sel", "score")])
                      for t in SCO["_truths"]] for ei in range(len(SCO["_etas"]))])


def save_scores(fname, SCO, worlds, extra=None):
    out = {k: v for k, v in SCO.items() if not k.startswith("_")}
    npz(fname, classes=classes_of(SCO, worlds), etas=np.array(SCO["_etas"]), truths=np.array(SCO["_truths"]),
        hs=np.array(HS), axes=np.array("eta, truth, seed, half (0 sel, 1 score), item, horizon"), **out, **(extra or {}))


# ----------------------------------------------------------------------------- 4 inference
def build_inference(cfg, fam):
    """S (round 5's: public family, 13 features, 4 parameters), H (designed family) and H_mix (true-form family),
    told the form, 21 summaries, 5 parameters (DECLARED R13, R14)."""
    em = {}
    pub = fam["pub"]
    N, KD = len(pub["Ud"]), pub["KD"]
    Fd = LL.view_features(VIEW, pub["obs"], pub["U"], P_)
    proj = SL.Projection().fit(Fd, pub["th_u"])
    em["S"] = (proj, LL.Emulator().fit(pub["Ud"], proj(Fd).reshape(N, KD, 4), rng=np.random.default_rng([4405, 4])))
    for kind, fname, seed in (("H", "des", 4406), ("H_mix", "true", 4407)):
        f = fam[fname]
        F = A2.summaries(f["obs"], f["U"], P_)
        pr, e = A2.fit_told_form(F, f["cls"], A2.u5(f["Ud"], f["eta_pt"]), f["KD"], np.random.default_rng([seed, 4]))
        em[kind] = (pr, e)
    diag = {k: {"emulator": v[1].diag, "projection_r2": (v[0].r2 if hasattr(v[0], "r2") else None)} for k, v in em.items()}
    return em, diag


def infer(cfg, em, worlds, etas, budgets, rows):
    """Posterior draws per (kind, eta index, truth, N) and identification rows."""
    sl = lab_slices(cfg)
    rng = np.random.default_rng([4403, 4])
    draws = {}
    for (ei, t), w in worlds.items():
        ut = (TRUTHS[t] - CEN) / HW
        mixo, mixu = w["lab_obs"][sl["mix"]], w["lab_U"][sl["mix"]]
        deso, desu = w["lab_obs"][sl["des"]], w["lab_U"][sl["des"]]
        Fs = LL.view_features(VIEW, mixo, mixu, P_)
        Fm = A2.summaries(mixo, mixu, P_)
        Fd = A2.summaries(deso, desu, P_)
        cm, cd = w["lab_cls"][sl["mix"]], w["lab_cls"][sl["des"]]
        for nb in budgets:
            obs_s = {"S": em["S"][0](Fs[:nb]).mean(0),
                     "H": em["H"][0](Fd[:nb], cd[:nb]).mean(0),
                     "H_mix": em["H_mix"][0](Fm[:nb], cm[:nb]).mean(0)}
            for kind in ("S", "H", "H_mix"):
                pv = PV if kind == "S" else PV5
                post = LL.posterior(em[kind][1], pv, obs_s[kind], nb, rng, M=cfg["post_M"])
                draws[(kind, ei, t, nb)] = post["u"]
                truth_u = ut if kind == "S" else np.concatenate([ut, [w["eta"] / 2.0 - 1.0]])
                psd = PSD if kind == "S" else np.concatenate([PSD, [2.0 / np.sqrt(12.0)]])
                rows.append({"kind": kind, "eta": w["eta"], "truth": int(t), "n_episodes": int(nb), "ess": post["ess"],
                             "post_mean_u": post["mean_u"].tolist(), "post_sd_u": post["sd_u"].tolist(),
                             "abs_err_over_prior_sd": (np.abs(post["mean_u"] - truth_u) / psd).tolist(),
                             "eta_post_mean": (float(2.0 * (post["mean_u"][4] + 1.0)) if kind != "S" else None),
                             "eta_post_sd": (float(2.0 * post["sd_u"][4]) if kind != "S" else None)})
    return draws


# ----------------------------------------------------------------------------- 5 base nets
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
    prm, info = A2.train_nets(ds, cond=True, steps=steps, seed=4000 + steps, log=lg, tag=tag, deadline=T_END)
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


def samples(params, items, seed, theta_u, m):
    return NN.net_samples(VIEW, params, items, m, seed, HS, SCALES, cond=True, theta_u=theta_u)


def score_base(cfg, SCO, worlds, Pn, Tn, suffix, keep=None):
    """P0, the public-form C and the true-form C of every world with the given nets."""
    m = cfg["m"]
    for (ei, t), w in worlds.items():
        ti = SCO["_truths"].index(t)
        items = w["items"]
        for s in range(cfg["seeds"]):
            rng = np.random.default_rng([4407, ei, t, s, int(w["eta"] * 10)])
            S0 = samples(Pn[s], items, 420 + 7 * t + s, prior_theta(rng, len(items), m), m)
            put(SCO, "P0" + suffix, ei, ti, s, w, S0)
            if keep is not None:
                keep[(ei, t, s)] = S0.astype(np.float32)
            put(SCO, "Cpub" + suffix, ei, ti, s, w, samples(Pn[s], items, 400 + 7 * t + s, u_truth(t), m))
            put(SCO, "Ctrue" + suffix, ei, ti, s, w, samples(Tn[s], items, 410 + 7 * t + s, u_truth(t, w["eta"]), m))


# ----------------------------------------------------------------------------- 6 budgets
def lab_view(cfg, w):
    if "A_mix" not in w:
        sl = lab_slices(cfg)["mix"]
        w["A_mix"] = NN.view_arrays(VIEW, w["lab_obs"][sl], w["lab_U"][sl], SCALES)
    return w["A_mix"]


def stage_finetune(cfg, worlds, Pn, Tn, nb, kinds_of, steps, rates, tag):
    """FT (public-form base, prior conditioning) and CFT (true-form base, conditioning at the truth) on the first
    nb Lab mix episodes of every world and seed, cross-validated over (rate, steps). kinds_of(w) -> kinds."""
    TH_prior = LL.pad_u(PRI_U[:AN.FT.N_TH])
    tasks = []
    for (ei, t), w in worlds.items():
        A = lab_view(cfg, w)
        lc = [str(c) for c in w["lab_cls"][lab_slices(cfg)["mix"]][:nb]]
        for s in range(cfg["seeds"]):
            for kind in kinds_of(w):
                if kind == "FT":
                    tasks.append({"id": ("FT", ei, t, s), "base": Pn[s], "A": A, "eps": range(nb), "cls": lc, "TH": TH_prior})
                else:
                    tasks.append({"id": ("CFT", ei, t, s), "base": Tn[s], "A": A, "eps": range(nb), "cls": lc,
                                  "TH": np.tile(LL.pad_u(u_truth(t, w["eta"])), (AN.FT.N_TH, 1))})
    T1 = worlds[next(iter(worlds))]["lab_obs"].shape[1]
    shapes = AN.fixed_shapes(cfg["n_mix"], T1)
    prm, info, timing = A2.finetune_cv(tasks, shapes, steps, rates, seed=5000 + 97 * nb, log=log, tag=tag)
    groups = {}
    for (kind, ei, t, s), v in info.items():
        groups.setdefault(f"{kind}|eta{worlds[(ei, t)]['eta']:g}", []).append(v)
    rule = {}
    for g, vs in groups.items():
        c = np.mean(np.array([v["curves"] for v in vs]), 0)
        dec, s_best, r_best = A2.widen_decision(c, rates, steps)
        edge = [v for v in vs if v["steps"] == 0 or v["steps"] >= steps
                or (v["steps"] == AN.FT.GRID and v["rate_index"] == int(np.argmin(rates)))]
        rule[g] = {"mean_curves": np.round(c, 6).tolist(), "best_steps": s_best, "best_rate": r_best, "widen": dec,
                   "interior": dec is None, "share_nets_pick_at_edge": len(edge) / len(vs),
                   "share_nets_zero_steps": float(np.mean([v["steps"] == 0 for v in vs])),
                   "picked_steps": [v["steps"] for v in vs], "picked_rates": [v["rate"] for v in vs]}
    return prm, {"per_net": {"|".join(map(str, k)): {kk: vv for kk, vv in v.items() if kk != "curves"}
                             for k, v in info.items()},
                 "rule": rule, "timing": timing, "steps": int(steps), "rates": [float(r) for r in rates],
                 "interior": bool(all(r["interior"] for r in rule.values()))}


def lab_means(cfg, worlds, Pn, cache):
    """P0's predictive mean on every Lab mix episode at the exam's anchor: (n_mix, n_h, 192) per world and seed."""
    m = cfg["m"]
    sl = lab_slices(cfg)["mix"]
    for (ei, t), w in worlds.items():
        obs, U = w["lab_obs"][sl], w["lab_U"][sl]
        its = AN.lab_items(obs, U, P_)
        for s in range(cfg["seeds"]):
            if (ei, t, s) in cache:
                continue
            rng = np.random.default_rng([4408, ei, t, s, int(w["eta"] * 10)])
            cache[(ei, t, s)] = samples(Pn[s], its, 460 + 7 * t + s, prior_theta(rng, len(its), m), m).mean(1)
        if "lab_struct" not in w:
            U2 = U[:, P_:].astype(float)
            w["lab_struct"] = {"cls": np.array([AN.program_class(u) for u in U2]),
                               "reg": np.stack([AN.region(u) for u in U2]),
                               "z0": AN.block_scaled(obs[:, P_, :LL.NC]),
                               "y": np.stack([AN.block_scaled(obs[:, P_ + h, :LL.NC]) for h in HS], 1)}


def res_samples(w, mean_lab, S0, nb):
    """RES (cross-validated ridge, DECLARED R12) and RESfix (A's ridge 0.05, reported) on the first nb Lab mix
    episodes of world w: P0's samples S0 plus the fitted correction."""
    ls = w["lab_struct"]
    eps = np.arange(nb)
    R = ls["y"][eps] - AN.block_scaled(mean_lab[eps])
    Wc, chosen = AN.res_fit_cv(ls["z0"][eps], R, ls["reg"][eps], ls["cls"][eps])
    corr_c = AN.res_apply(Wc, w["item_z0"], w["item_reg"], w["item_cls"], len(HS))
    W = AN.res_fit(ls["z0"][eps], R, ls["reg"][eps], ls["cls"][eps])
    corr = AN.res_apply(W, w["item_z0"], w["item_reg"], w["item_cls"], len(HS))
    S0 = S0.astype(np.float64)
    return S0 + corr_c[:, None], S0 + corr[:, None], chosen


def score_budget(cfg, SCO, worlds, nb, ftp, draws, S0c, MLc, Pn, Tn):
    m = cfg["m"]
    sfx = f"@{nb}"
    for (ei, t), w in worlds.items():
        ti = SCO["_truths"].index(t)
        items = w["items"]
        for s in range(cfg["seeds"]):
            rng = np.random.default_rng([4409, ei, t, s, nb, int(w["eta"] * 10)])
            if ("FT", ei, t, s) in ftp:
                put(SCO, "FT" + sfx, ei, ti, s, w, samples(ftp[("FT", ei, t, s)], items, 470 + 7 * t + s,
                                                           prior_theta(rng, len(items), m), m))
            if ("CFT", ei, t, s) in ftp:
                put(SCO, "CFT" + sfx, ei, ti, s, w, samples(ftp[("CFT", ei, t, s)], items, 480 + 7 * t + s,
                                                            u_truth(t, w["eta"]), m))
                put(SCO, "CFT_blind" + sfx, ei, ti, s, w, samples(ftp[("CFT", ei, t, s)], w["items_blind"],
                                                                  481 + 7 * t + s, u_truth(t, w["eta"]), m))
            Sr, Sf, chosen = res_samples(w, MLc[(ei, t, s)], S0c[(ei, t, s)], nb)
            put(SCO, "RES" + sfx, ei, ti, s, w, Sr)
            put(SCO, "RESfix" + sfx, ei, ti, s, w, Sf)
            RES_LAM.setdefault("RES" + sfx, {})[f"eta{w['eta']:g}|t{t}|s{s}"] = {k: str(v) for k, v in chosen.items()}
            for kind, net, base_seed in (("S", Pn[s], 440), ("H", Tn[s], 490), ("H_mix", Tn[s], 500)):
                if (kind, ei, t, nb) not in draws:
                    continue
                dr = draws[(kind, ei, t, nb)]
                th = dr[rng.choice(len(dr), len(items) * m)].reshape(len(items), m, -1)
                if kind != "S":
                    th = A2.cond_of_u5(th)
                put(SCO, kind + sfx, ei, ti, s, w, samples(net, items, base_seed + 7 * t + s, th, m))
            if nb == cfg["budgets"][0]:
                put(SCO, "Ctrue_blind", ei, ti, s, w, samples(Tn[s], w["items_blind"], 411 + 7 * t + s,
                                                              u_truth(t, w["eta"]), m))


def stage_D(cfg, SCO, worlds, nb, steps):
    """D(nb): round 5's unconditioned net on the first nb Lab mix episodes (seeds) and round 5's block ridge."""
    sl = lab_slices(cfg)["mix"]
    order = [(ei, t, s) for (ei, t) in worlds for s in range(cfg["seeds"])]
    infos, pD = [], {}
    for s0 in range(0, len(order), NN.Cfg.MAX_LOCK):
        part = order[s0:s0 + NN.Cfg.MAX_LOCK]
        ds = [NN.make_dataset(VIEW, worlds[(ei, t)]["lab_obs"][sl][:nb], worlds[(ei, t)]["lab_U"][sl][:nb], SCALES,
                              seed=100 * nb + 10 * t + s) for ei, t, s in part]
        prm, info = A2.train_nets(ds, cond=False, steps=steps, seed=7000 + 13 * nb + s0, deadline=T_END,
                                  log=log if s0 == 0 else None, tag=f"[D({nb}) {steps}]", eval_every=cfg["d_eval"])
        info["order"] = part
        infos.append({k: info[k] for k in ("best_step", "best_val", "steps", "seconds", "stopped_early", "order", "ms_per_step")})
        pD.update(dict(zip(part, prm)))
    met = bool(all(b <= 0.8 * i["steps"] for i in infos for b in i["best_step"])) and all(i["stopped_early"] is None for i in infos)
    for (ei, t), w in worlds.items():
        ti = SCO["_truths"].index(t)
        for s in range(cfg["seeds"]):
            put(SCO, f"Dnet@{nb}", ei, ti, s, w,
                NN.net_samples(VIEW, pD[(ei, t, s)], w["items"], cfg["m"], 450 + 7 * t + s, HS, SCALES))
        Sr = LL.ridge_samples(VIEW, LL.ridge_fit(VIEW, w["lab_obs"][sl][:nb], w["lab_U"][sl][:nb], HS, SCALES), w["items"],
                              cfg["m"], 0, HS, SCALES)
        for s in range(cfg["seeds"]):
            put(SCO, f"Dridge@{nb}", ei, ti, s, w, Sr)
    return {"groups": infos, "rule_met": met, "steps": int(steps),
            "best_step_hist": np.bincount(np.array([b for i in infos for b in i["best_step"]]) // cfg["d_eval"]).tolist()}


# ----------------------------------------------------------------------------- the pipeline
def pipeline(cfg, out_dir, est=None):
    """est: seconds per stage projected from the presmoke (None in the presmoke itself)."""
    STATE["out"] = out_dir
    os.makedirs(out_dir, exist_ok=True)
    times, TR = {}, {"base": [], "ft": {}, "D": {}}
    etas, truths = list(cfg["etas"]), list(cfg["truths"])
    info = dict(INFO, config=cfg_json(cfg), member_ticks_planned=estimate_ticks(cfg))
    info["member_ticks_planned"]["total"] = int(sum(info["member_ticks_planned"].values()))
    log(f"pipeline -> {out_dir}: {len(truths)} truths x eta {etas}, member-ticks planned "
        f"{info['member_ticks_planned']['total']:,}")
    idrows = []

    def flush(stage):
        info.update(times=times, failed=FAILED, skipped=SKIPPED, notes=NOTES, stage_done=stage,
                    hours=(time.time() - T0) / 3600)
        jdump("info.json", info)
        jdump("train_info.json", {**TR, "res_cv_ridge": RES_LAM})
        jdump("identification.json", {"rows": idrows, "emulators": info.get("emulators")})

    def fits(stage, need_after=0.0):
        if est is None:
            return True
        need = est.get(stage, 0.0) + need_after + 90.0
        if left() < need:
            SKIPPED.append(f"{stage}: {left() / 60:.1f} min left, about {need / 60:.1f} min needed")
            log(f"SKIP {stage}: {left() / 60:.1f} min left, about {need / 60:.1f} min needed")
            return False
        return True

    with Timer("2 families", times):
        fam, info["family_check"] = stage_families(cfg, times)
    with Timer("3 worlds", times):
        worlds = make_worlds(cfg, etas, truths, times, "main")
    info["lab"] = lab_record(cfg, worlds)
    SCO = new_sco(cfg, etas, truths, worlds)
    save_scores("scores.npz", SCO, worlds)
    flush("worlds")
    with Timer("4 inference", times):
        em, info["emulators"] = build_inference(cfg, fam)
        draws = infer(cfg, em, worlds, etas, cfg["budgets"], idrows)
    flush("inference")

    # ---- base nets: the schedule doubles while the rule is unmet (DECLARED R9)
    Pn = Tn = None
    S0c, MLc = {}, {}
    rest = 0.0 if est is None else est["N8"] + est["D8"] + est["final"]
    for r, steps in enumerate(cfg["rungs"]):
        if r > 0 and TR["base"][-1]["rule_met"] and not cfg["timing_runs"]:
            break
        if r > 0 and not fits(f"base_{steps}", rest):
            NOTES.append(f"training rule: the doubling to {steps} steps was cut by the clock")
            break
        with Timer(f"5 base nets, {steps} steps", times):
            Pn, Tn, inf = train_base(cfg, fam, steps, f"[base {steps}]")
            TR["base"].append({k: inf[k] for k in ("steps", "best_step", "best_val", "hist", "seconds", "rule_met",
                                                   "stopped_early", "net_order", "log_lines", "n_train_examples",
                                                   "n_episodes", "ms_per_step", "steps_per_dispatch")})
            log(f"  base {steps}: best steps {inf['best_step']} best val {np.round(inf['best_val'], 4).tolist()} "
                f"rule met {inf['rule_met']} ({inf['ms_per_step']:.1f} ms/step without validation)")
        with Timer(f"5 scoring rung {steps}", times):
            S0c.clear()
            score_base(cfg, SCO, worlds, Pn, Tn, f"@r{steps}", keep=S0c)
        save_scores("scores.npz", SCO, worlds)
        flush(f"base_{steps}")
    final_steps = TR["base"][-1]["steps"]
    for k in ("P0", "Cpub", "Ctrue"):
        SCO[k] = SCO[f"{k}@r{final_steps}"].copy()
    info["base_final_steps"] = int(final_steps)
    info["base_rule_met"] = bool(TR["base"][-1]["rule_met"])
    if not info["base_rule_met"]:
        NOTES.append(f"training rule: base nets not converged by the rule at {final_steps} steps")
    arrs = {}
    for s in range(cfg["seeds"]):
        arrs.update(AN.tree_to_arrays(f"P{s}", Pn[s]))
        arrs.update(AN.tree_to_arrays(f"T{s}", Tn[s]))
    npz("nets.npz", steps=np.array(final_steps), **arrs)
    with Timer("6 P0 on the Lab episodes", times):
        lab_means(cfg, worlds, Pn, MLc)
    quick(cfg, SCO, worlds, "after the base nets")

    def budget(nb, wds, sco, drw, s0c, mlc, key, tagx=""):
        steps, rates, k = cfg["ft_steps"], list(cfg["ft_rates"]), 0
        while True:
            name = f"6 fine-tuning N={nb}{tagx}, {steps} steps, rates {rates}"
            with Timer(name, times):
                ftp, inf = stage_finetune(cfg, wds, Pn, Tn, nb, lambda w: ("FT",) if w["eta"] == 0 else ("FT", "CFT"),
                                          steps, rates, f"[N={nb}{tagx}]")
            TR["ft"].setdefault(f"{nb}{tagx}", []).append(inf)
            log(f"  N={nb}{tagx}: " + ", ".join(f"{g} best {v['best_steps']}@{v['best_rate']:g} widen {v['widen']}"
                                               for g, v in inf["rule"].items())
                + f"; {inf['timing']['ms_per_lockstep_step_median']} ms per lockstep step")
            decs = {v["widen"] for v in inf["rule"].values()} - {None}
            if not decs or k >= cfg["ft_widen"]:
                break
            if est is not None and left() < 2.5 * times[name] + est["final"] + 300:
                NOTES.append(f"FT grid at N={nb}{tagx} not widened past steps {steps}, rates {rates} (clock)")
                break
            if "steps" in decs:
                steps *= 2
            if "rate" in decs:
                rates = rates + [min(rates) / 5.0]
            k += 1
        if not inf["interior"]:
            NOTES.append(f"FT grid at N={nb}{tagx}: pick not interior in every group at steps {steps}, rates {rates}")
        with Timer(f"6 scoring N={nb}{tagx}", times):
            score_budget(cfg, sco, wds, nb, ftp, drw, s0c, mlc, Pn, Tn)

    def dstage(nb, wds, sco, tagx=""):
        steps, k = cfg["steps_d"], 0
        while True:
            with Timer(f"6 D({nb}){tagx}, {steps} steps", times):
                inf = stage_D(cfg, sco, wds, nb, steps)
            TR["D"].setdefault(f"{nb}{tagx}", []).append(inf)
            if inf["rule_met"] or k >= cfg["d_doublings"]:
                break
            steps, k = 2 * steps, k + 1
        if not inf["rule_met"]:
            NOTES.append(f"training rule: D({nb}){tagx} not converged by the rule at {steps} steps")

    b0 = cfg["budgets"][0]
    budget(b0, worlds, SCO, draws, S0c, MLc, "N8")       # the primary budget: required
    save_scores("scores.npz", SCO, worlds)
    flush(f"N{b0}")
    dstage(b0, worlds, SCO)                                # D(8) is a member of G*: required
    save_scores("scores.npz", SCO, worlds)
    flush(f"D{b0}")
    quick(cfg, SCO, worlds, f"after N={b0}")
    for nb in cfg["budgets"][1:]:
        if fits(f"N{nb}", est[f"D{nb}"] if est else 0.0):
            try:
                budget(nb, worlds, SCO, draws, S0c, MLc, f"N{nb}")
                dstage(nb, worlds, SCO)
                save_scores("scores.npz", SCO, worlds)
                flush(f"N{nb}")
            except Exception as exc:
                FAILED.append(f"N={nb}: {exc!r}"[:300])
                log(f"  N={nb} FAILED: {exc!r}\n{traceback.format_exc()}")
    # ---- eta 1 and 2 for truths 0-3 at N = 8 (reported)
    if cfg["x_etas"] and fits("x"):
        try:
            with Timer("7 eta 1 and 2 arm: worlds and inference", times):
                xw = make_worlds(cfg, list(cfg["x_etas"]), list(cfg["x_truths"]), times, "eta12")
                SCX = new_sco(cfg, list(cfg["x_etas"]), list(cfg["x_truths"]), xw)
                xd = infer(cfg, em, xw, list(cfg["x_etas"]), [b0], idrows)
                xS0, xML = {}, {}
                score_base(cfg, SCX, xw, Pn, Tn, "", keep=xS0)
                lab_means(cfg, xw, Pn, xML)
            budget(b0, xw, SCX, xd, xS0, xML, "x", tagx="|eta12")
            dstage(b0, xw, SCX, tagx="|eta12")
            save_scores("scores_eta12.npz", SCX, xw)
            info["lab_eta12"] = lab_record(cfg, xw)
            flush("eta12")
        except Exception as exc:
            FAILED.append(f"eta 1 and 2 arm: {exc!r}"[:300])
            log(f"  eta 1 and 2 arm FAILED: {exc!r}\n{traceback.format_exc()}")
    info["member_ticks_total"] = info["member_ticks_planned"]["total"]
    quick(cfg, SCO, worlds, "final")
    flush("done")
    return times, TR, info


def quick(cfg, SCO, worlds, when):
    """A first look in the log (the criteria come from make_summary.py; this must never stop the job)."""
    try:
        d = {k: v for k, v in SCO.items() if not k.startswith("_")}
        rep = ST.first_look(d, classes_of(SCO, worlds), list(SCO["_etas"]), cfg["budgets"][0])
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
    c, p = FULL, PRE
    nw = len(c["truths"]) * len(c["etas"])
    nwp = len(p["truths"]) * len(p["etas"])
    nwx = len(c["x_truths"]) * len(c["x_etas"])
    t_world = float(np.median(times["world_seconds"][1:] if len(times["world_seconds"]) > 1 else times["world_seconds"]))
    fr = times["family_rates"]
    t_fam = 0.0
    for k in ("pub", "true", "des"):
        n_ep = c["n_theta"] * (2 * c["Kc"] if k != "des" else len(A2.ARMS))
        t_fam += -(-n_ep // c["chunk"]) * fr[k]["seconds_last_chunk"]
    b_fast = TR["base"][-1]
    ms_base = b_fast["ms_per_step"] / 1e3 * 1.03            # + validation every 250 steps
    sc_rung = times[f"5 scoring rung {p['rungs'][-1]}"] / nwp * nw
    est = {"families": t_fam, "worlds": nw * t_world, "inference": times["4 inference"] / nwp * nw, "final": 120.0,
           "seconds_per_base_step": ms_base}
    for st in c["rungs"]:
        est[f"base_{st}"] = st * ms_base + sc_rung
    for nb in c["budgets"]:
        tm = TR["ft"][str(p["budgets"][0])][-1]["timing"]
        ms_ft = tm["ms_per_lockstep_step_median"] / 1e3
        k_cv = len(AN.folds_of(nb))
        n_ft = nw * c["seeds"] + (nw // 2) * c["seeds"]           # FT at every eta, CFT at eta 4
        runs = n_ft * k_cv * len(c["ft_rates"])
        g_cv, g_fin = -(-runs // AN.FT.LOCK), -(-n_ft // AN.FT.LOCK)
        sc_name = f"6 scoring N={p['budgets'][0]}"
        est[f"N{nb}"] = (g_cv + g_fin) * c["ft_steps"] * ms_ft * 1.1 + times[sc_name] / nwp * nw
        d_name = f"6 D({p['budgets'][0]}), {p['steps_d']} steps"
        est[f"D{nb}"] = times[d_name] / nwp * nw * c["steps_d"] / p["steps_d"] + 60.0
    est["N8"], est["D8"] = est[f"N{c['budgets'][0]}"], est[f"D{c['budgets'][0]}"]
    est["x"] = nwx * t_world + (est["N8"] + est["D8"]) * nwx / nw + 120.0
    required = (est["families"] + est["worlds"] + est["inference"] + est[f"base_{c['rungs'][0]}"] + est["N8"]
                + est["D8"] + est["final"])
    everything = required + sum(est[f"base_{st}"] for st in c["rungs"][1:]) + sum(
        est[f"N{nb}"] + est[f"D{nb}"] for nb in c["budgets"][1:]) + est["x"]
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
