"""run_fl -- study foundrylong (round 6), stage 1: is the long-horizon gap only the recipe's compute? (GPU job)

PILOT ONLY: every hidden world of this job is a public function of public seeds. These worlds, Lab data and
items must NEVER be reused as an exam. The noise secret (256 bits, os.urandom) is never written.

Declared in DECLARED.md (committed before the request). Stages, in the declared order:
  screen    the pre-screened draws of prior seed 2028 (inputs/sel_2028.json) through round 5's screen
            (round5/foundry/job2.run_arm, its sizes) and the four gates of criteria.py -> candidates
  gate      the pilot's exam-time gate on the candidates (33-frame window, burn-in 300) -> new prior worlds
  sims      64 mix episodes of each training world (the pilot's 210, then the new ones); n_c mix episodes at the
            true weights of each hidden world (for C)
  hidden    per hidden world: Lab (32 mix episodes), exam (96 items x 12 futures, 96 climatology runs), references,
            plug-ins from the hidden state, the ridge Dr(N)
  nets      P0(1000); C(16384) seed 0; FT(32), FT(8); D; C(16384) seed 1; C(4096); P0(210); P0(64); C(1024); P0x2
            each scored on every item as soon as it is trained; scores.npz is rewritten after every family
Outputs under OUT: scores.npz, items.npz, train_info.json, worlds.json, screen.json, screen_draws.npz, gate.json,
info.json, progress.txt, params_p0w1000.npz, cparams/c16384_wNN.npz. The summary is made offline (make_summary.py).

usage: python -B run_fl.py --out DIR [--size full|presmoke|smoke] [--max-hours 2.5] [--full-hours H] [--cpu-ok]
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
import fl_lib as LL  # noqa: E402  (first: sets the pilot modules' episode constants)

FL, NN = LL.FL, LL.NN

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

import criteria as CR  # noqa: E402
import tnca as TN  # noqa: E402
from vw.secret import Secret  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
ap.add_argument("--size", default="full", choices=("full", "presmoke", "smoke"))
ap.add_argument("--max-hours", type=float, default=2.5)
ap.add_argument("--full-hours", type=float, default=None, help="presmoke: the time the full pass will have (speed guard)")
ap.add_argument("--cpu-ok", action="store_true")
args = ap.parse_args()
OUT = args.out
os.makedirs(OUT, exist_ok=True)
T0 = time.time()
T_END = T0 + args.max_hours * 3600

FULL = dict(burn=300, chunk=2048, n_screen=None, gate_M=8, gate_on=True, n_pilot_train=210, n_new=790, epw=64, n_hidden=16,
            n_lab=32, lab_chunk=32, n_items=96, R=12, n_clim=96, m=24, m_plug=8, budgets=[8, 32],
            p0_worlds=[64, 210, 1000], p0_steps={64: 6000, 210: 16000, 1000: 40000}, p0x2_steps=80000, batch_p0=256,
            n_c=[1024, 4096, 16384], c_steps={1024: 4000, 4096: 8000, 16384: 16000}, c_lock={1024: 16, 4096: 16, 16384: 8},
            c_seeds={1024: 1, 4096: 1, 16384: 2}, batch_c=128, c_group=8, ft_lrs=[5e-5, 2e-4, 8e-4], ft_smax=400, ft_folds=4,
            d_steps={8: 400, 32: 800}, batch_lab=64, n_seeds=3, eval_big=500, eval_small=50, chunk_steps=50, shape_test=False,
            save_params=True)
PRESMOKE = dict(FULL, n_screen=256, n_pilot_train=8, n_new=8, n_hidden=2, p0_worlds=[8, 16], p0_steps={8: 100, 16: 100},
                p0x2_steps=100, n_c=[512, 1024, 2048], c_steps={512: 100, 1024: 100, 2048: 100},
                c_lock={512: 16, 1024: 16, 2048: 8}, c_seeds={512: 1, 1024: 1, 2048: 2}, c_group=2, ft_lrs=[2e-4, 8e-4],
                ft_smax=100, d_steps={8: 50, 32: 50}, n_seeds=2, eval_big=50, shape_test=True)
SMOKE = dict(burn=3, chunk=8, n_screen=16, gate_M=2, gate_on=False, n_pilot_train=3, n_new=3, epw=4, n_hidden=2, n_lab=8,
             lab_chunk=4, n_items=4, R=3, n_clim=4, m=4, m_plug=3, budgets=[4, 8], p0_worlds=[3, 6], p0_steps={3: 20, 6: 20},
             p0x2_steps=40, batch_p0=16, n_c=[4, 8], c_steps={4: 20, 8: 20}, c_lock={4: 2, 8: 2}, c_seeds={4: 1, 8: 2},
             batch_c=16, c_group=2, ft_lrs=[2e-4, 8e-4], ft_smax=20, ft_folds=2, d_steps={4: 20, 8: 20}, batch_lab=16,
             n_seeds=2, eval_big=10, eval_small=10, chunk_steps=10, shape_test=True, save_params=True)
# the shapes the shape test trains: the full job's, or (CPU smoke) tiny ones that only exercise the code
SHAPE_F = FULL if args.size != "smoke" else dict(FULL, p0_worlds=[4, 8], epw=4, n_c=[8, 16, 32], c_lock={8: 2, 16: 2, 32: 2}, n_lab=8,
                                                 c_steps={8: 20, 16: 20, 32: 20}, c_seeds={8: 1, 16: 1, 32: 2}, batch_p0=16, batch_c=16,
                                                 batch_lab=16)
SHAPE_STEPS = 200 if args.size != "smoke" else 20
CFG = {"full": FULL, "presmoke": PRESMOKE, "smoke": SMOKE}[args.size]
NN.Cfg.CHUNK = CFG["chunk_steps"]
if args.size == "smoke":
    NN.Cfg.EVAL_ROWS, NN.Cfg.EVAL_DRAWS = 16, 4
    LL.NV_H = 32
STRICT = args.size != "full"
FAILED, SKIPPED, CLOCK = [], [], {}
NEX = sum(LL.ANCHORS)
PRIOR_NEW = 2028


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


def left():
    return T_END - time.time()


if not os.path.exists(os.path.join(OUT, "progress.txt")):
    with open(os.path.join(OUT, "progress.txt"), "w") as f:
        f.write("PILOT_NEVER_REUSE_AS_EXAM: the hidden worlds of this job are public pilot material\n")
backend = jax.default_backend()
try:
    ram_gb = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 2 ** 30
except (ValueError, OSError):
    ram_gb = float("nan")
log(f"run_fl size {args.size} max_hours {args.max_hours}; jax {jax.__version__} numpy {np.__version__} python "
    f"{platform.python_version()} backend {backend} devices {jax.devices()} RAM {ram_gb:.0f} GiB; episode {LL.T1} frames, "
    f"horizons {LL.HS}, anchors {LL.ANCHORS}")
if backend != "gpu" and not args.cpu_ok:
    log("no GPU backend: refusing to run (use --cpu-ok for tests)")
    sys.exit(3)
PW = json.load(open(os.path.join(HERE, "inputs", "pilot_worlds.json")))
CN = json.load(open(os.path.join(HERE, "inputs", "code_norm.json")))
SEL = json.load(open(os.path.join(HERE, "inputs", "sel_2028.json")))
SMU, SSD = np.asarray(CN["mean"], np.float32), np.asarray(CN["sd"], np.float32)
RUN = FL.Runner(CFG["chunk"], CFG["burn"])
SECRET = Secret()                                   # 256 bits from os.urandom; never written
INFO = {}                                           # training records of every net family
SPEED = {}


def theta_of_label(lab):
    s, i = lab[4:].split("-")
    return TN.draw_theta(int(s), int(i))


def sim_mix(ths, n_ep, seed, tag):
    """n_ep exam-mix episodes of every world of the list (world-major)."""
    TH = FL.stack_thetas([t for t in ths for _ in range(n_ep)])
    rng = np.random.default_rng([seed, 17])
    cls = [c for _ in ths for c in FL.mix_classes(n_ep, rng)]
    t, mt = time.time(), RUN.member_ticks
    obs, U, _ = RUN.episodes(TH, seed, classes=cls, prog_seed=seed + 1, log=log, tag=tag)
    SPEED[f"sim{tag}"] = dict(member_ticks=RUN.member_ticks - mt, seconds=time.time() - t)
    return obs, U


# ----------------------------------------------------------------------------- screen and gate: new prior worlds
def stage_screen():
    """Round 5's screen on the pre-screened draws of prior seed 2028 -> candidate indices (all four gates)."""
    t = time.time()
    ids = SEL["index"][: CFG["n_screen"]] if CFG["n_screen"] else SEL["index"]
    work = os.path.join(os.environ.get("GPUJOB_DIR") or os.path.dirname(os.path.abspath(OUT)), f"fl_screen_{args.size}_{os.getpid()}")
    old = {k: os.environ.get(k) for k in ("OUT", "FOUNDRY_SIZE", "FOUNDRY_T_START")}
    os.environ.update(OUT=work, FOUNDRY_SIZE="tiny" if args.size == "smoke" else "full", FOUNDRY_T_START=str(time.time()))
    try:
        import job2 as J2                           # round5/foundry/job2.py: run_arm (its main() is not called)
    finally:
        for k, v in old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
    J2.T_LATE = 1e9
    ch = int(os.environ.get("FL_SCREEN_CHUNK", "0")) or None        # the chunk that fitted in the presmoke (job.sh)
    info = J2.run_arm("prior2028", ids, PRIOR_NEW, J2.SZ, chunk=ch)
    if info.get("failed") or info["n_done"] != len(ids):
        raise RuntimeError(f"screen: {info['n_done']} of {len(ids)} draws done ({info.get('failed')})")
    d0 = os.path.join(work, "prior2028")
    parts = [dict(np.load(os.path.join(d0, f))) for f in sorted(os.listdir(d0)) if f.startswith("chunk_")]
    m = {k: np.concatenate([p[k] for p in parts]) for k in parts[0] if not k.startswith("thumb")}
    idx = m["index"].astype(int)
    try:
        d = CR.derive(m, info["sizes"]["T"])
        typ = CR.classify(d)
        g = CR.gates(d, typ)
        cand = np.asarray(g["candidate"], bool)
    except Exception:
        if args.size != "smoke":
            raise
        d, typ, g, cand = {}, np.zeros(len(idx), int), {}, None
    if args.size == "smoke":                         # tiny sizes: the gates mean nothing; keep the code path
        cand = np.ones(len(idx), bool)
    keep = ("cv_cell", "nb_mean", "body_frac", "v_net", "events100", "ceil8", "gap_max", "vp_main1", "vp_main16")
    npz("screen_draws.npz", index=idx, type=np.asarray(typ), candidate=cand,
        **{k: np.asarray(d[k], np.float32) for k in keep if k in d})
    rate = info.get("member_ticks_per_s_steady")
    SPEED["screen"] = dict(member_ticks=int(sum(c["member_ticks"] for c in info["chunks"])), seconds=info["seconds"],
                           member_ticks_per_s_steady=rate, chunks=len(info["chunks"]), chunk=info["chunk"],
                           chunk_used=int(info["chunks"][-2 if len(info["chunks"]) > 1 else -1]["n"]),
                           errors=[e for e in J2.STATE.get("errors", [])])
    jdump("screen.json", dict(what="round 5's screen (job2.run_arm, its sizes) on the pre-screened draws of prior seed 2028",
                              prior_seed=PRIOR_NEW, n_draws=len(idx), n_candidates=int(cand.sum()), sizes=info["sizes"],
                              types={str(k): int((np.asarray(typ) == k).sum()) for k in np.unique(typ)},
                              gates={k: int(np.asarray(v).sum()) for k, v in g.items()}, speed=SPEED["screen"],
                              candidates=[int(i) for i in idx[cand]], seconds=time.time() - t))
    log(f"screen: {len(idx)} draws, {int(cand.sum())} candidates ({cand.mean():.3f}); {rate} member-ticks/s ({time.time() - t:.0f}s)")
    return [int(i) for i in idx[cand]]


def stage_gate(cand):
    """The pilot's exam-time gate (33-frame window) on the new candidates -> indices that pass, in index order."""
    t = time.time()
    if not cand:
        jdump("gate.json", dict(n=0, n_ok=0, rows=[]))
        return []
    ths = [TN.draw_theta(PRIOR_NEW, i) for i in cand]
    M = CFG["gate_M"]
    with LL.pilot_shape():
        TH = FL.stack_thetas([th for th in ths for _ in range(M)])
        obs, _, cv = RUN.episodes(TH, 102, classes=None, log=log, tag=" gate")
        g = FL.gate(obs, cv, M)
    ok = g["ok"] if CFG["gate_on"] else np.ones(len(cand), bool)
    rows = [dict(index=int(i), ok=bool(ok[j]), cv_cell=float(g["cv_cell"][j]), vp1=float(g["vp1"][j]), vp16=float(g["vp16"][j]))
            for j, i in enumerate(cand)]
    jdump("gate.json", dict(what="exam-time gate of the pilot (foundryexam DESIGN.md section 2) on the new candidates",
                            prior_seed=PRIOR_NEW, burn=CFG["burn"], M=M, gate_on=CFG["gate_on"],
                            thresholds=dict(cv_cell_min=FL.CV_UNIFORM, vp16_min=FL.VP_ACTIVE16, vp1_max=FL.VP_NOISY),
                            n=len(cand), n_ok=int(ok.sum()), rows=rows))
    log(f"gate: {int(ok.sum())} of {len(cand)} new candidates pass ({time.time() - t:.0f}s)")
    return [int(i) for j, i in enumerate(cand) if ok[j]]


# ----------------------------------------------------------------------------- hidden worlds
def hidden_world(wi, hw, world, plug_label):
    th = hw["theta"]
    FL.set_params(world, th)
    sec = SECRET.child("world", "P", wi)
    rng = np.random.default_rng([20261111, 6, wi])
    t = time.time()
    lab = FL.run_lab(world, sec, CFG["n_lab"], CFG["lab_chunk"], rng)
    ex = FL.build_exam(world, sec, CFG["n_items"], CFG["R"], CFG["n_clim"], f"P-{wi}")
    hist, Ptest, klass = FL.item_arrays(ex)
    S = dict(FL.references(ex))
    S["Kp"] = FL.score_es(ex, FL.persistence_samples(hist))
    n, mp = ex.n, CFG["m_plug"]
    for nm, (thp, zero) in {"plugTrue": (th, False), "plugU0": (th, True), "plugPrior": (theta_of_label(plug_label), False)}.items():
        S[nm] = FL.score_es(ex, FL.plugin(ex, world, thp, mp, sec.keys(n * mp, "plug", nm), zero_program=zero))
    for N in CFG["budgets"]:
        S[f"Dr@{N}"] = FL.score_es(ex, FL.ridge_samples(FL.ridge_fit(lab["obs"][:N], lab["U"][:N]), hist, Ptest, CFG["m"], 7 + N))
    CLOCK["hidden_s"] = CLOCK.get("hidden_s", 0.0) + time.time() - t
    return dict(ex=ex, lab=lab, hist=hist, Ptest=Ptest, klass=klass, S=S, label=hw["label"], theta=th, gate=hw["gate"],
                plug_label=plug_label, D0=NN.item_dataset(hist, Ptest, SMU, SSD),
                lab_nats=dict(mean=float(lab["nats"].mean()), max=float(lab["nats"].max()), usage=lab["usage"]),
                clim=dict(mean=ex.clim_mean, sd=ex.clim_sd))


def save_scores(HW):
    names = sorted(set().union(*[set(h["S"]) for h in HW]))
    names = [nm for nm in names if all(nm in h["S"] for h in HW)]
    npz("scores.npz", names=np.array(names), world=np.repeat(np.arange(len(HW)), CFG["n_items"]),
        item=np.tile(np.arange(CFG["n_items"]), len(HW)), klass=np.concatenate([h["klass"] for h in HW]),
        horizons=np.array(LL.HS), labels=np.array([h["label"] for h in HW]),
        **{"S__" + nm.replace("|", "__").replace("@", "_at_"): np.concatenate([h["S"][nm] for h in HW]) for nm in names})
    jdump("train_info.json", INFO)
    return names


def score_shared(HW, name, best, n_seeds):
    """best: leaves (NH, seeds, ...). Every hidden world's items, per seed."""
    t = time.time()
    for s in range(n_seeds):
        bk = LL.tree_at(best, slice(None), s)
        for h in HW:
            h["S"][f"{name}|s{s}"] = FL.score_es(h["ex"], LL.samples_h(bk, h["D0"], CFG["m"], 800))
    CLOCK["scores_s"] = CLOCK.get("scores_s", 0.0) + time.time() - t


def score_world_nets(HW, name, best, wids, seed):
    """best: leaves (NH, K, ...), net k belongs to hidden world wids[k]."""
    t = time.time()
    for k, i in enumerate(wids):
        h = HW[i]
        h["S"][f"{name}|s{seed}"] = FL.score_es(h["ex"], LL.samples_h(LL.tree_at(best, slice(None), k), h["D0"], CFG["m"], 800))
    CLOCK["scores_s"] = CLOCK.get("scores_s", 0.0) + time.time() - t


def quick(HW, names):
    """Log line: pooled skill per horizon of every policy (seed mean), items of all worlds."""
    base = sorted({n.split("|")[0] for n in names})
    L = {b: np.mean([np.concatenate([h["S"][n] for h in HW]) for n in names if n.split("|")[0] == b], 0).mean(0) for b in base}
    out = {}
    for b in base:
        if b in ("K", "O"):
            continue
        out[b] = [round(float((L["K"][j] - L[b][j]) / (L["K"][j] - L["O"][j])), 3) for j in range(LL.NH)]
    return out


# ----------------------------------------------------------------------------- shape test and speed guard (presmoke)
def shape_test(n_sel, n_cand_est):
    """The full job's largest training shapes on noise data, 200 steps each, and a projection of the whole job from
    the measured speeds (simulation from this presmoke's screen and Runner chunks). Exit 4 if the projection
    exceeds 1.25 x the time the full pass will have."""
    F, t, NS_ = SHAPE_F, time.time(), SHAPE_STEPS
    rng = np.random.default_rng(0)

    def noise(E):
        return (np.abs(rng.standard_normal((E, LL.T1, LL.NOBS), np.float32)) + 0.1), np.zeros((E, LL.P + LL.H, LL.NW), np.float32)
    ms = {}
    E = max(F["p0_worlds"]) * F["epw"]
    obs, U = noise(E)
    ds = LL.make_ds(obs, U, SMU, SSD, seed=0, world_of=np.repeat(np.arange(max(F["p0_worlds"])), F["epw"]))
    _, inf = LL.train(ds, NS_, [0, 1, 2], batch=F["batch_p0"], eval_every=NS_, log=log, tag=" shape P0(1000) x3")
    ms["p0_3"] = inf["ms_per_step"]
    _, inf = LL.train(ds, NS_, [0], batch=F["batch_p0"], eval_every=NS_, log=log, tag=" shape P0x2 x1")
    ms["p0_1"] = inf["ms_per_step"]
    del ds
    nC = max(F["n_c"])
    dsc = LL.make_ds(obs[:nC], U[:nC], SMU, SSD, seed=0)
    Lk = F["c_lock"][nC]
    _, inf = LL.train([dsc] * Lk, NS_, list(range(Lk)), batch=F["batch_c"], eval_every=NS_, log=log, tag=f" shape C({nC}) x{Lk}")
    ms["c_big"] = inf["ms_per_step"]
    nM = sorted(F["n_c"])[-2]
    dsm = LL.make_ds(obs[:nM], U[:nM], SMU, SSD, seed=0)
    Lm = min(F["c_lock"][nM], F["c_group"])
    _, inf = LL.train([dsm] * Lm, NS_, list(range(Lm)), batch=F["batch_c"], eval_every=NS_, log=log, tag=f" shape C({nM}) x{Lm}",
                      pad=(nM, NEX * nM, 3 * LL.NV_H))
    ms["c_mid"] = inf["ms_per_step"]
    del dsc, dsm
    nL = F["n_lab"]
    dl = LL.make_ds(obs[:nL], U[:nL], SMU, SSD, val_ep=(np.arange(nL) % 4 == 0))
    Kl = min(16, F["n_hidden"])
    _, inf = LL.train([dl] * Kl, NS_, list(range(Kl)), batch=F["batch_lab"], sched="const", eval_every=NS_, log=log, tag=f" shape lab x{Kl}",
                      pad=LAB_PAD)
    ms["lab"] = inf["ms_per_step"]
    del obs, U
    sr = SPEED["screen"].get("member_ticks_per_s_steady") or (SPEED["screen"]["member_ticks"] / SPEED["screen"]["seconds"])
    simk = [k for k in SPEED if k.startswith("sim C")]
    rr = sum(SPEED[k]["member_ticks"] for k in simk) / sum(SPEED[k]["seconds"] for k in simk)
    tick_ep = F["burn"] + LL.P + LL.H
    sim_s = (n_sel * 3276 / sr + (n_cand_est * F["gate_M"] * (F["burn"] + 32) + (F["n_pilot_train"] + F["n_new"]) * F["epw"] * tick_ep
                                  + F["n_hidden"] * max(F["n_c"]) * tick_ep) / rr + 400.0)
    p0 = ms["p0_3"] * sum(F["p0_steps"].values()) + ms["p0_1"] * F["p0x2_steps"]
    c = (ms["c_big"] * F["c_steps"][nC] * F["c_seeds"][nC] * (F["n_hidden"] / Lk)
         + ms["c_mid"] * sum(F["c_steps"][n] * F["c_seeds"][n] for n in F["n_c"] if n != nC) * (F["n_hidden"] / Lm))
    grp = F["n_hidden"] / Kl
    ft = ms["lab"] * F["n_seeds"] * len(F["budgets"]) * len(F["ft_lrs"]) * F["ft_smax"] * (F["ft_folds"] + 1) * grp
    dd = ms["lab"] * F["n_seeds"] * sum(F["d_steps"].values()) * grp
    net_s = (p0 + c + ft + dd) / 1e3
    total_h = (sim_s + net_s + 600.0) / 3600                       # 600 s: compilation, scoring, saving
    res = dict(ms_per_step=ms, screen_member_ticks_per_s=sr, runner_member_ticks_per_s=rr, projected_sim_hours=sim_s / 3600,
               projected_net_hours=net_s / 3600, projected_hours_total=total_h, full_hours=args.full_hours,
               n_selected=n_sel, n_candidates_estimate=n_cand_est, seconds=time.time() - t)
    ok = True
    if args.full_hours is not None:
        have = args.full_hours - (time.time() - T0) / 3600
        res["hours_available"] = have
        ok = total_h <= 1.25 * have
    res["speed_ok"] = bool(ok)
    jdump("shape_test.json", res)
    log(f"shape test: ms per step {ms}; screen {sr:.0f} and runner {rr:.0f} member-ticks/s; projected {total_h:.2f} h "
        f"(simulation {sim_s / 3600:.2f}, nets {net_s / 3600:.2f}); available {res.get('hours_available')}; speed_ok {ok}")
    if not ok:
        log("TOO SLOW: the full pass would not finish; stopping before it starts")
        sys.exit(4)


LAB_PAD = (CFG["n_lab"], NEX * CFG["n_lab"], 3 * NN.Cfg.EVAL_ROWS if args.size != "smoke" else NN.Cfg.EVAL_ROWS * 4)


def write_info(done=False, extra=None):
    jdump("info.json", dict(size=args.size, finished=bool(done), config={k: (v if not isinstance(v, dict) else {str(a): b for a, b in v.items()})
                                                                          for k, v in CFG.items()},
                            platform=dict(jax=jax.__version__, numpy=np.__version__, python=platform.python_version(), backend=backend,
                                          devices=[str(d) for d in jax.devices()], world_dtype="float64", net_dtype="float32",
                                          ram_gib=ram_gb),
                            episode=dict(frames=LL.T1, horizons=list(LL.HS), anchors=list(LL.ANCHORS)),
                            member_ticks_runner=RUN.member_ticks, speed=SPEED, hours=(time.time() - T0) / 3600, failed=FAILED,
                            skipped=SKIPPED, clock=CLOCK, secret_commitment=SECRET.commitment(), **(extra or {})))


def main():
    # ---- new prior worlds
    cand = stage_screen()
    new_ok = stage_gate(cand)
    n_new = min(CFG["n_new"], len(new_ok))
    if n_new < CFG["n_new"]:
        log(f"NOTE: only {n_new} new prior worlds pass (wanted {CFG['n_new']}): P0's largest set is smaller (a deviation if below 590)")
    train_labels = PW["train"][: CFG["n_pilot_train"]] + [f"seed{PRIOR_NEW}-{i}" for i in new_ok[:n_new]]
    p0cfg = sorted(CFG["p0_worlds"])                               # configured sizes; the actual ones are capped by the worlds found
    p0act = [min(w, len(train_labels)) for w in p0cfg]
    w_max = p0act[-1]
    p0w = sorted(set(p0act))
    steps_of = {a: CFG["p0_steps"][c] for c, a in zip(p0cfg, p0act)}  # the largest configured size wins a tie
    train_labels = train_labels[:w_max]
    hidden = [dict(label=h["label"], gate=h["gate"], theta=theta_of_label(h["label"])) for h in PW["hidden"][: CFG["n_hidden"]]]
    nH = len(hidden)
    extra = dict(n_train_worlds=len(train_labels), p0_worlds=p0w, n_new_ok=len(new_ok), n_candidates=len(cand))
    write_info(extra=extra)
    # ---- training simulations: the agent's simulator on the prior worlds, the designer's at the true weights
    obsP, UP = sim_mix([theta_of_label(l) for l in train_labels], CFG["epw"], 2000, " P0")
    woP = np.repeat(np.arange(len(train_labels)), CFG["epw"])
    nC = max(CFG["n_c"])
    CG = CFG["c_group"]
    simC = []
    for g0 in range(0, nH, CG):
        simC.append(sim_mix([h["theta"] for h in hidden[g0:g0 + CG]], nC, 6000 + g0, f" C g{g0 // CG}"))
    log(f"training simulations done: {len(train_labels)} prior worlds x {CFG['epw']}, {nH} hidden worlds x {nC}; "
        f"{RUN.member_ticks / 1e6:.1f} million member-ticks so far")
    if CFG["shape_test"]:
        frac = len(cand) / max(CFG["n_screen"] or len(SEL["index"]), 1)
        shape_test(len(SEL["index"]), int(round(frac * len(SEL["index"]))))
    # ---- hidden worlds
    world = FL.build_world(hidden[0]["theta"], CFG["burn"])
    HW = []
    for wi, hw in enumerate(hidden):
        HW.append(hidden_world(wi, hw, world, train_labels[wi % len(train_labels)]))
        if (wi + 1) % 4 == 0 or wi + 1 == nH:
            log(f"hidden world {wi + 1}/{nH}: lab + exam + plug-ins + ridge ({CLOCK['hidden_s']:.0f}s so far)")
    jdump("worlds.json", dict(train_labels=train_labels, p0_worlds=p0w,
                              hidden=[dict(label=h["label"], gate=h["gate"], lab=h["lab_nats"], clim_mean=h["clim"]["mean"],
                                           clim_sd=h["clim"]["sd"], plug_prior=h["plug_label"]) for h in HW]))
    npz("items.npz", hist=np.stack([h["hist"] for h in HW]).astype(np.float32), Ptest=np.stack([h["Ptest"] for h in HW]).astype(np.float32),
        lab_obs=np.stack([h["lab"]["obs"] for h in HW]).astype(np.float32), lab_U=np.stack([h["lab"]["U"] for h in HW]).astype(np.float32),
        lab_cls=np.stack([h["lab"]["cls"] for h in HW]))
    names = save_scores(HW)
    log(f"references: {quick(HW, names)}")
    nS = CFG["n_seeds"]
    P0 = {}

    def do_p0(w, steps, seeds, name):
        sel = woP < w
        ds = LL.make_ds(obsP[sel], UP[sel], SMU, SSD, seed=w, world_of=woP[sel])
        best, inf = LL.train(ds, steps, seeds, batch=CFG["batch_p0"], eval_every=CFG["eval_big"], log=log, tag=f" {name}",
                             deadline=T_END)
        INFO[name] = inf
        log(f"{name}: {inf['ms_per_step']} ms per step of {len(seeds)} nets; best steps {inf['best_step']}; trained {inf['trained']}")
        score_shared(HW, name, best, len(seeds))
        return best

    def do_c(n, seed):
        name = f"C{n}"
        Lk = CFG["c_lock"][n]
        for g0 in range(0, nH, CG):
            obs, U = simC[g0 // CG]
            wids = list(range(g0, min(nH, g0 + CG)))
            dss = [LL.make_ds(obs[j * nC: j * nC + n], U[j * nC: j * nC + n], SMU, SSD, seed=wids[j]) for j in range(len(wids))]
            for s in range(0, len(wids), Lk):
                grp = wids[s:s + Lk]
                best, inf = LL.train(dss[s:s + Lk], CFG["c_steps"][n], [100 + 2 * i + seed for i in grp], batch=CFG["batch_c"],
                                     eval_every=CFG["eval_big"], log=log, tag=f" {name} s{seed} w{grp[0]}-{grp[-1]}", deadline=T_END,
                                     pad=(n, NEX * n, 3 * LL.NV_H) if n == nC else (c_sizes[1], NEX * c_sizes[1], 3 * LL.NV_H))
                INFO[f"{name}|s{seed}|w{grp[0]}"] = dict(inf, worlds=grp)
                score_world_nets(HW, name, best, grp, seed)
                if CFG["save_params"] and n == nC and seed == 0:
                    hb = LL.host(best)
                    for k, i in enumerate(grp):
                        npz(f"cparams/c{n}_w{i:02d}.npz", **LL.flat_params(LL.tree_at(hb, slice(None), k)))
            del dss
        log(f"{name} seed {seed} done")

    def do_ft(N):
        for s in range(nS):
            name = f"FT@{N}|s{s}"
            init = [LL.tree_at(P0[w_max], 1, s)] * nH                # P0's parameters that were best at 16 ticks
            best, inf = LL.ft_cv([h["lab"]["obs"] for h in HW], [h["lab"]["U"] for h in HW], N, init, SMU, SSD,
                                 [300 + 2 * i + s for i in range(nH)], CFG["ft_lrs"], CFG["ft_smax"], folds=CFG["ft_folds"],
                                 batch=CFG["batch_lab"], eval_every=CFG["eval_small"], pad=LAB_PAD, log=log, tag=f" {name}",
                                 deadline=T_END)
            INFO[name] = inf
            score_world_nets(HW, f"FT@{N}", best, list(range(nH)), s)

    def do_d(N):
        for s in range(nS):
            dss = [LL.make_ds(h["lab"]["obs"][:N], h["lab"]["U"][:N], SMU, SSD, seed=N + i) for i, h in enumerate(HW)]
            for g0 in range(0, nH, 16):
                grp = list(range(g0, min(nH, g0 + 16)))
                best, inf = LL.train(dss[g0:g0 + 16], CFG["d_steps"][N], [200 + 2 * i + s for i in grp], batch=CFG["batch_lab"],
                                     eval_every=CFG["eval_small"], pad=LAB_PAD, deadline=T_END)
                INFO[f"D@{N}|s{s}|w{g0}"] = dict(inf, worlds=grp)
                score_world_nets(HW, f"D@{N}", best, grp, s)

    def p0_main():
        P0[w_max] = do_p0(w_max, steps_of[w_max], list(range(nS)), f"P0w{w_max}")
        if CFG["save_params"]:
            hb = LL.host(P0[w_max])
            flat = {}
            for s in range(nS):
                flat.update({f"s{s}/{k}": v for k, v in LL.flat_params(LL.tree_at(hb, slice(None), s)).items()})
            npz(f"params_p0w{w_max}.npz", **flat)

    def p0_small(w):
        do_p0(w, steps_of[w], [10 * (p0w.index(w) + 1) + s for s in range(nS)], f"P0w{w}")

    c_sizes = sorted(CFG["n_c"], reverse=True)
    Bs = sorted(CFG["budgets"], reverse=True)
    plan = [("P0 main", p0_main), (f"C{nC} s0", lambda: do_c(nC, 0))]
    plan += [(f"FT@{N}", lambda N=N: do_ft(N)) for N in Bs] + [(f"D@{N}", lambda N=N: do_d(N)) for N in Bs]
    plan += [(f"C{nC} s{s}", lambda s=s: do_c(nC, s)) for s in range(1, CFG["c_seeds"][nC])]
    plan += [(f"C{c_sizes[1]}", lambda: [do_c(c_sizes[1], s) for s in range(CFG["c_seeds"][c_sizes[1]])])]
    plan += [(f"P0w{w}", lambda w=w: p0_small(w)) for w in sorted(p0w[:-1], reverse=True)]
    plan += [(f"C{n}", lambda n=n: [do_c(n, s) for s in range(CFG["c_seeds"][n])]) for n in c_sizes[2:]]
    plan += [("P0x2", lambda: score_shared(HW, "P0x2", do_p0_x2(), 1))]

    def do_p0_x2():
        ds = LL.make_ds(obsP, UP, SMU, SSD, seed=w_max, world_of=woP)
        best, inf = LL.train(ds, CFG["p0x2_steps"], [0], batch=CFG["batch_p0"], eval_every=CFG["eval_big"], log=log, tag=" P0x2",
                             deadline=T_END)
        INFO["P0x2"] = inf
        log(f"P0x2: {inf['ms_per_step']} ms per step; best steps {inf['best_step']}; trained {inf['trained']}")
        return best
    for what, fn in plan:
        if left() < 240 and args.size == "full":
            SKIPPED.append(f"{what} (time left {left():.0f}s)")
            log("SKIP " + SKIPPED[-1])
            continue
        t = time.time()
        try:
            fn()
        except Exception:
            FAILED.append(what)
            log("FAILED " + what + "\n" + traceback.format_exc())
        CLOCK[f"{what}_s"] = time.time() - t
        names = save_scores(HW)
        write_info(extra=extra)
        log(f"{what} done ({time.time() - t:.0f}s); skill by horizon {LL.HS}: {quick(HW, names)}")
    stopped = [k for k, v in INFO.items() if isinstance(v, dict) and v.get("stopped_early")]
    if stopped:
        SKIPPED.append(f"stopped early by the deadline: {stopped}")
    write_info(done=True, extra=extra)
    log(f"done: {(time.time() - T0) / 3600:.2f} h, {RUN.member_ticks / 1e6:.1f} million member-ticks (runner), failed {FAILED}, "
        f"skipped {SKIPPED}")
    sys.exit(1 if (FAILED or (STRICT and SKIPPED)) else 0)


if __name__ == "__main__":
    main()
