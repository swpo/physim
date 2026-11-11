"""run_fx -- study foundryexam (round 6): an exam pilot where the hidden law is a network's weights (GPU job).

PILOT ONLY: every hidden world of this job is a public function of public seeds and its weights are written
to the outputs. These worlds, Lab data and items must NEVER be reused as an exam. The real-world noise secret
(256 bits, os.urandom) is never written.

Design, criteria and thresholds: DESIGN.md (committed before the first GPU request). Stages:
  gate     every pool world (results/pool.json) and every neighbour candidate: M free episodes at the exam's
           burn-in -> active or not (fx_lib.gate)
  arm P    hidden = 16 gate-passing enriched candidates of prior seed 2027 (numpy default_rng(20261111));
           training worlds = every other gate-passing pool world
  arm N30  per centre (3 shortlisted worlds): 48 training neighbours and 4 hidden neighbours at eps = 0.3
  arm N10  the same at eps = 0.1
Per arm: simulations of the training worlds (the agent's own simulator), per hidden world a Lab of exam-mix
episodes (vw.harness Lab on the hidden vw.World), a HistoryExam (items, replicate futures, climatology), the
plug-in simulators from the hidden state, the ridge Dr(N); then the nets (P0, P0s, amortised S, per-world C,
D(N), FT(N)), their samples for every item and the fair energy scores through the exam's own scorer.
Outputs per arm under OUT/<arm>/: scores.npz, meta.json, train_info.json, worlds.json; OUT/gate.json,
OUT/info.json, OUT/progress.txt. The summary is made offline by make_summary.py.

usage: python -B run_fx.py --out DIR [--size full|presmoke|smoke] [--arms P,N30,N10] [--max-hours 2.5] [--cpu-ok]
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
import fx_lib as FL  # noqa: E402
import fx_net as NN  # noqa: E402

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

import tnca as TN  # noqa: E402
from vw.scoring import public_report, skill_report  # noqa: E402
from vw.secret import Secret  # noqa: E402

ACC = FL.load_acceptance()
ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
ap.add_argument("--size", default="full", choices=("full", "presmoke", "smoke"))
ap.add_argument("--arms", default="P,N30,N10")
ap.add_argument("--max-hours", type=float, default=2.5)
ap.add_argument("--cpu-ok", action="store_true")
ap.add_argument("--full-hours", type=float, default=None, help="presmoke: the time the full pass will have (speed guard)")
ap.add_argument("--full-arms", default="P,N30,N10", help="presmoke: the arms of the full pass (speed guard)")
args = ap.parse_args()
OUT = args.out
os.makedirs(OUT, exist_ok=True)
T0 = time.time()
T_END = T0 + args.max_hours * 3600

SB_FULL = {"P": {"P0": 12000, "A": 12000, "P0s": 6000, "P0w": 6000}, "N30": {"P0": 8000, "A": 8000, "P0s": 4000},
           "N10": {"P0": 8000, "A": 8000, "P0s": 4000}}
# Sizes of job r6-foundryexam-004 (DESIGN.md section 5c). Job 003 had n_csim 1536, steps_C 4000 at batch 64, steps_Cft
# 1500, nb_train_cand 64, nb_train 32, 4000 / 3000 steps for the N arms' shared nets and seed_offset 0.
FULL = dict(burn=300, chunk=2048, gate_M=8, gate_on=True, pool_limit=None, n_hidden_P=16, n_centres=3, n_hidden_N=4,
            nb_train_cand=256, nb_train=128, nb_hidden_cand=16, epw=64, n_lab=512, lab_chunk=128, n_csim=4096, n_csmall=1024,
            n_items=32, R=12, n_clim=96, m=24, m_plug=8, budgets=[8, 32, 128, 512], s_budgets=[0, 2, 8, 32, 128, 512],
            seeds2=[32, 512], steps_big=SB_FULL, batch_big={"P": 256, "N30": 128, "N10": 128}, batch_world=64, batch_C=128,
            steps_C=8000, steps_Cft=3000, lr_Cft=3e-4, steps_D={8: 400, 32: 800, 128: 1500, 512: 3000},
            steps_FT={8: 200, 32: 400, 128: 1200, 512: 2400}, lr_FT=2e-4, nw_curve=[16, 64], eval_every=250,
            eval_every_small=100, chunk_steps=50, seed_offset=int(os.environ.get("FX_SEED_OFFSET", "1000")),
            n_cbig=int(os.environ.get("FX_N_CBIG", "0")), steps_Cbig=24000, lock_Cbig=8, shape_test=False)
# n_cbig > 0 (job 005, DESIGN.md section 5d): a third reference net "Cbig" on n_cbig true-weight episodes per hidden world
_SBT = {a: {k: 100 for k in v} for a, v in SB_FULL.items()}
PRESMOKE = dict(FULL, pool_limit=40, n_hidden_P=2, n_centres=1, n_hidden_N=1, nb_train_cand=6, nb_train=4,
                nb_hidden_cand=4, steps_big=_SBT, steps_C=100, steps_Cft=50, steps_Cbig=100, steps_D={8: 50, 32: 50, 128: 50, 512: 50},
                steps_FT={8: 50, 32: 50, 128: 50, 512: 50}, nw_curve=[16], eval_every=50, eval_every_small=50, shape_test=True)
_SBS = {a: {k: 20 for k in v} for a, v in SB_FULL.items()}
SMOKE = dict(burn=3, chunk=8, gate_M=2, gate_on=False, pool_limit=10, n_hidden_P=2, n_centres=1, n_hidden_N=1,
             nb_train_cand=3, nb_train=3, nb_hidden_cand=2, epw=4, n_lab=8, lab_chunk=4, n_csim=8, n_items=4, R=3,
             n_clim=4, m=4, m_plug=3, budgets=[8], s_budgets=[0, 2, 8], seeds2=[8], steps_big=_SBS,
             batch_big={"P": 16, "N30": 16, "N10": 16}, batch_world=16, batch_C=16, n_csmall=4, steps_C=20, steps_Cft=10,
             lr_Cft=3e-4, seed_offset=0, n_cbig=(12 if int(os.environ.get("FX_N_CBIG", "0")) > 0 else 0), steps_Cbig=20, lock_Cbig=1,
             steps_D={8: 20}, steps_FT={8: 10}, lr_FT=2e-4, nw_curve=[4], eval_every=10, eval_every_small=10,
             chunk_steps=10, shape_test=False)
CFG = {"full": FULL, "presmoke": PRESMOKE, "smoke": SMOKE}[args.size]
NN.Cfg.BATCH, NN.Cfg.CHUNK = CFG["batch_world"], CFG["chunk_steps"]
if args.size == "smoke":
    NN.Cfg.N_VAL, NN.Cfg.EVAL_ROWS, NN.Cfg.EVAL_DRAWS, NN.Cfg.KMAX = 32, 16, 4, 8
    NN.KS = (0, 1, 2, 4, 8)
STRICT = args.size != "full"                      # in a test pass a skipped or failed part fails the pass
ARMS = [a for a in args.arms.split(",") if a]
ARMS_FULL = [a for a in args.full_arms.split(",") if a]   # the arms of the full pass (the presmoke's speed guard projects these)
EPS = {"N30": 0.3, "N10": 0.1}
FAILED, SKIPPED = [], []
CLOCK = {}
C_FULL, C_AM, C_STATE = (NN.LAGS_FULL, True, "own"), (NN.LAGS_FULL, True, "random"), (NN.LAGS_STATE, False, "own")
SEED0 = int(CFG["seed_offset"])                    # added to every net seed (job 004: independent training seeds)


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


def theta_json(th):
    return {k: np.asarray(v).tolist() for k, v in th.items()}


# ----------------------------------------------------------------------------- start
if not os.path.exists(os.path.join(OUT, "progress.txt")):
    with open(os.path.join(OUT, "progress.txt"), "w") as f:
        f.write("PILOT_NEVER_REUSE_AS_EXAM: the hidden worlds of this job are public pilot material\n")
backend = jax.default_backend()
log(f"run_fx size {args.size} arms {ARMS} max_hours {args.max_hours}; jax {jax.__version__} numpy {np.__version__} "
    f"python {platform.python_version()} backend {backend} devices {jax.devices()}")
if backend != "gpu" and not args.cpu_ok:
    log("no GPU backend: refusing to run (use --cpu-ok for tests)")
    sys.exit(3)
POOL = json.load(open(os.path.join(HERE, "results", "pool.json")))
RUN = FL.Runner(CFG["chunk"], CFG["burn"])
SECRET = Secret()                                   # 256 bits from os.urandom; never written
RNG = np.random.default_rng(20261111)


def sim_free(ths, M, seed, tag):
    """M free episodes of every world of the list (world-major)."""
    TH = FL.stack_thetas([t for t in ths for _ in range(M)])
    return RUN.episodes(TH, seed, classes=None, log=log, tag=tag)


def sim_mix(ths, n_ep, seed, tag):
    """n_ep exam-mix episodes of every world of the list (world-major): the agent's own simulator."""
    TH = FL.stack_thetas([t for t in ths for _ in range(n_ep)])
    rng = np.random.default_rng([seed, 17])
    cls = [c for _ in ths for c in FL.mix_classes(n_ep, rng)]
    obs, U, _ = RUN.episodes(TH, seed, classes=cls, prog_seed=seed + 1, log=log, tag=tag)
    return obs, U, np.array(cls)


# ----------------------------------------------------------------------------- gate
def stage_gate():
    t = time.time()
    ws = POOL["worlds"][: CFG["pool_limit"]] if CFG["pool_limit"] else POOL["worlds"]
    if CFG["pool_limit"]:                            # test passes: keep both seeds in the short pool
        e27 = [w for w in POOL["worlds"] if w["arm"] == "enriched2027"][: CFG["pool_limit"] // 2]
        s26 = [w for w in POOL["worlds"] if w["arm"] == "screen2026"][: CFG["pool_limit"] - len(e27)]
        ws = e27 + s26
    cands = [dict(kind="pool", prior_seed=w["prior_seed"], index=w["index"], arm=w["arm"],
                  theta=TN.draw_theta(w["prior_seed"], w["index"])) for w in ws]
    centres = POOL["centres"]["chosen"][: CFG["n_centres"]]
    cth = {c: TN.draw_theta(POOL["centres"]["prior_seed"], c) for c in centres}
    for arm in ARMS:
        if arm == "P":
            continue
        for c in centres:
            js = list(range(CFG["nb_train_cand"])) + list(range(1000, 1000 + CFG["nb_hidden_cand"]))
            for j in js:
                cands.append(dict(kind=arm, centre=c, j=j, theta=FL.neighbour(cth[c], c, j, EPS[arm])))
    obs, _, cv = sim_free([c["theta"] for c in cands], CFG["gate_M"], 101, " gate")
    g = FL.gate(obs, cv, CFG["gate_M"])
    ok = g["ok"] if CFG["gate_on"] else np.ones(len(cands), bool)
    for i, c in enumerate(cands):
        c.update(ok=bool(ok[i]), cv_cell=float(g["cv_cell"][i]), vp1=float(g["vp1"][i]), vp16=float(g["vp16"][i]),
                 tick_r2=float(g["tick_r2"][i]))
    rows = [{k: v for k, v in c.items() if k != "theta"} for c in cands]
    by = {}
    for c in cands:
        k = c["kind"] if c["kind"] != "pool" else "pool:" + c["arm"]
        by.setdefault(k, [0, 0])
        by[k][0] += int(c["ok"])
        by[k][1] += 1
    jdump("gate.json", dict(what="exam-time gate (DESIGN.md section 2)", burn=CFG["burn"], M=CFG["gate_M"],
                            gate_on=CFG["gate_on"], thresholds=dict(cv_cell_min=FL.CV_UNIFORM, vp16_min=FL.VP_ACTIVE16,
                                                                     vp1_max=FL.VP_NOISY),
                            passed={k: dict(ok=v[0], of=v[1]) for k, v in by.items()}, rows=rows))
    log(f"gate: {len(cands)} worlds, passed " + ", ".join(f"{k} {v[0]}/{v[1]}" for k, v in by.items())
        + f" ({time.time() - t:.0f}s)")
    return cands, cth


# ----------------------------------------------------------------------------- arms
def gate_of(c):
    return {k: c[k] for k in ("cv_cell", "vp1", "vp16", "tick_r2")}


def arm_groups(arm, cands, cth):
    """[dict(gid, train (list of theta), hidden (list of dict(theta, label, plug_prior)))]"""
    if arm == "P":
        good = [c for c in cands if c["kind"] == "pool" and c["ok"]]
        e27 = [c for c in good if c["arm"] == "enriched2027"]
        pick = np.random.default_rng(20261111).permutation(len(e27))[: CFG["n_hidden_P"]]
        hid = [e27[i] for i in sorted(pick.tolist())]
        hid_ids = {(c["prior_seed"], c["index"]) for c in hid}
        train = [c for c in good if (c["prior_seed"], c["index"]) not in hid_ids]
        train = [train[i] for i in np.random.default_rng(20261112).permutation(len(train))]   # P0[n] = a random subset
        if len(hid) < CFG["n_hidden_P"] or len(train) < 4:
            raise RuntimeError(f"arm P: {len(hid)} hidden and {len(train)} training worlds pass the gate")
        hidden = [dict(theta=c["theta"], label=f"seed{c['prior_seed']}-{c['index']}", gate=gate_of(c),
                       plug_prior=train[i % len(train)]["theta"],
                       plug_label=f"seed{train[i % len(train)]['prior_seed']}-{train[i % len(train)]['index']}")
                  for i, c in enumerate(hid)]
        return [dict(gid="prior", train=[c["theta"] for c in train],
                     train_labels=[f"seed{c['prior_seed']}-{c['index']}" for c in train], hidden=hidden)]
    out = []
    for c0, thc in cth.items():
        tr = [c for c in cands if c["kind"] == arm and c["centre"] == c0 and c["j"] < 1000 and c["ok"]][: CFG["nb_train"]]
        hd = [c for c in cands if c["kind"] == arm and c["centre"] == c0 and c["j"] >= 1000 and c["ok"]][: CFG["n_hidden_N"]]
        if len(hd) < CFG["n_hidden_N"] or len(tr) < 2:
            SKIPPED.append(f"{arm} centre {c0}: {len(hd)} hidden and {len(tr)} training neighbours pass the gate")
            log("SKIP " + SKIPPED[-1])
            continue
        out.append(dict(gid=f"centre{c0}", train=[c["theta"] for c in tr], train_labels=[f"c{c0}-j{c['j']}" for c in tr],
                        hidden=[dict(theta=c["theta"], label=f"c{c0}-j{c['j']}", plug_prior=thc, plug_label=f"centre{c0}",
                                     gate=gate_of(c))
                                for c in hd]))
    return out


def tick_share(obs):
    """Share of the standardised block view's variance carried by the tick alone (criterion 7): variance over
    ticks of the mean over episodes and blocks, per channel, averaged; for the no-input half and all 33 frames."""
    y = np.asarray(obs, np.float64).reshape(obs.shape[0], FL.T1, FL.NCH, FL.NB)
    mu, sd = y.mean((0, 1, 3), keepdims=True), y.std((0, 1, 3), keepdims=True)
    z = (y - mu) / np.maximum(sd, 1e-300)
    m = z.mean((0, 3))                                                    # (T1, NCH)
    n = obs.shape[0] * FL.NB
    noise = 1.0 / n                                                       # variance of such a mean under no drift (upper bound: blocks correlate)
    return dict(first17=float(m[: FL.P + 1].var(0).mean()), all33=float(m.var(0).mean()), sampling_floor=noise)


def hidden_world(arm, gi, wi, hw, world, st_norm):
    """Lab, exam, references, plug-ins and the ridge of one hidden world. Returns a dict kept for the nets."""
    th = hw["theta"]
    FL.set_params(world, th)
    sec = SECRET.child("world", arm, wi)
    rng = np.random.default_rng([20261111, 5, ARMS_ALL.index(arm), wi])
    t = time.time()
    lab = FL.run_lab(world, sec, CFG["n_lab"], CFG["lab_chunk"], rng)
    ex = FL.build_exam(world, sec, CFG["n_items"], CFG["R"], CFG["n_clim"], f"{arm}-{wi}")
    hist, Ptest, klass = FL.item_arrays(ex)
    S = dict(FL.references(ex))
    S["Kp"] = FL.score_es(ex, FL.persistence_samples(hist))
    n, mp = ex.n, CFG["m_plug"]
    plugs = {"plugTrue": (th, False), "plugU0": (th, True), "plugPrior": (hw["plug_prior"], False)}
    for e_, nm in ((0.03, "plug03"), (0.1, "plug10"), (0.3, "plug30")):
        plugs[nm] = (TN.perturb_theta(th, 707000 + 1000 * ARMS_ALL.index(arm) + wi, 0, e_, hyper=False), False)
    for nm, (thp, zero) in plugs.items():
        S[nm] = FL.score_es(ex, FL.plugin(ex, world, thp, mp, sec.keys(n * mp, "plug", nm), zero_program=zero))
    for N in CFG["budgets"]:
        N_ = min(N, CFG["n_lab"])
        S[f"Dr@{N}"] = FL.score_es(ex, FL.ridge_samples(FL.ridge_fit(lab["obs"][:N_], lab["U"][:N_]), hist, Ptest, CFG["m"], 7 + N))
    CLOCK["hidden_s"] = CLOCK.get("hidden_s", 0.0) + time.time() - t
    X = NN.to_grid(lab["obs"])
    return dict(ex=ex, lab=lab, hist=hist, Ptest=Ptest, klass=klass, S=S, gi=gi, label=hw["label"], theta=th,
                gate=hw["gate"], plug_label=hw["plug_label"],
                lab_ST=NN.episode_stats(X), tick=tick_share(lab["obs"]),
                lab_nats=dict(mean=float(lab["nats"].mean()), max=float(lab["nats"].max()), usage=lab["usage"]),
                clim=dict(mean=ex.clim_mean, sd=ex.clim_sd))


def train_groups(cfg, jobs, steps, lock, lr=None, init_of=None, tag="", info=None, deadline=None, eval_every=None, pad=None,
                 batch=None):
    """jobs: list of (name, dataset, seed). Trains them in lockstep groups of `lock` nets (one compiled shape:
    the caller lists the jobs seed-major, `lock` = the number of hidden worlds); returns {name: params}. A group
    that fails is recorded and the finished groups are kept (review of 003)."""
    out = {}
    L = min(int(lock), NN.Cfg.MAX_LOCK)
    for s in range(0, len(jobs), L):
        grp = jobs[s:s + L]
        init = None if init_of is None else [init_of[g[0]] for g in grp]
        if deadline is not None and time.time() > deadline:
            SKIPPED.append(f"{tag} nets {s}-{s + len(grp)} (deadline)")
            log("SKIP " + SKIPPED[-1])
            continue
        try:
            ps, inf = NN.train(cfg, [g[1] for g in grp], steps, [g[2] + SEED0 for g in grp], lr=lr, init=init, log=log,
                               tag=f" {tag}[{s // L}]", deadline=deadline, eval_every=eval_every, pad=pad, batch=batch)
        except Exception:
            FAILED.append(f"{tag} group {s // L}")
            log("FAILED " + FAILED[-1] + "\n" + traceback.format_exc())
            continue
        inf["names"] = [g[0] for g in grp]
        if inf.get("ms_per_step"):
            log(f"  {tag}[{s // L}]: {inf['ms_per_step']:.1f} ms per step of {len(grp)} nets")
        if info is not None:
            info[f"{tag}|batch{s // L}"] = inf
        if inf["stopped_early"]:
            SKIPPED.append(f"{tag} batch {s // L} stopped at step {inf['stopped_early']} of {steps} (deadline)")
        for g, p in zip(grp, ps):
            out[g[0]] = p
    return out


def save_scores(arm, HW, fname):
    names = sorted(set().union(*[set(h["S"]) for h in HW]))
    names = [nm for nm in names if all(nm in h["S"] for h in HW)]
    S = {nm: np.concatenate([h["S"][nm] for h in HW]) for nm in names}
    world_of = np.repeat(np.arange(len(HW)), CFG["n_items"])
    klass = np.concatenate([h["klass"] for h in HW])
    npz(f"{arm}/{fname}", names=np.array(names), world=world_of, klass=klass, group=np.array([h["gi"] for h in HW]),
        cells=np.array(HW[0]["ex"].cells), **{"S__" + nm.replace("|", "__").replace("@", "_at_"): S[nm] for nm in names})
    return S, names, world_of, klass


def run_arm(arm, cands, cth, world, st_norm, t_arm_end):
    t_arm = time.time()
    groups = arm_groups(arm, cands, cth)
    if not groups:
        raise RuntimeError(f"arm {arm}: no group")
    smu, ssd = st_norm
    info = {}
    ai = ARMS_ALL.index(arm)
    pad_big = None if arm == "P" else (CFG["nb_train"] * CFG["epw"], NEX * CFG["nb_train"] * CFG["epw"])
    pad_lab = (CFG["n_lab"], NEX * CFG["n_lab"])
    # ---- the agent's simulator: training worlds of each group
    for gi, g in enumerate(groups):
        obs, U, cls = sim_mix(g["train"], CFG["epw"], 1000 + 100 * ai + gi, f" {arm} train g{gi}")
        X = NN.to_grid(obs)
        wo = np.repeat(np.arange(len(g["train"])), CFG["epw"])
        g["ds"] = NN.make_dataset(obs, U, smu, ssd, seed=gi, world_of=wo, ST=NN.episode_stats(X), EW=CFG["epw"])
        g["n_train_worlds"] = len(g["train"])
        g["obs_U_wo"] = (obs, U, wo)
        log(f"{arm} group {g['gid']}: {len(g['train'])} training worlds x {CFG['epw']} episodes, {len(g['hidden'])} hidden")
    # ---- hidden worlds
    HW = []
    for gi, g in enumerate(groups):
        for hw in g["hidden"]:
            try:                                     # one bad world is dropped and recorded, not the arm (review of 002, minor 4)
                HW.append(hidden_world(arm, gi, len(HW), hw, world, st_norm))
            except Exception:
                FAILED.append(f"{arm} hidden world {hw['label']}")
                log("FAILED " + FAILED[-1] + "\n" + traceback.format_exc())
            if len(HW) % 4 == 0:
                log(f"{arm} hidden world {len(HW)}: lab + exam + plug-ins + ridge done ({CLOCK.get('hidden_s', 0.0):.0f}s so far)")
    nH = len(HW)
    if nH < 1:
        raise RuntimeError(f"arm {arm}: no hidden world left")
    save_scores(arm, HW, "scores_refs.npz")          # references, plug-ins and the ridge, before any net
    worlds_json = dict(arm=arm, eps=EPS.get(arm), groups=[dict(gid=g["gid"], n_train=len(g["train"]), train_labels=g["train_labels"])
                                                          for g in groups],
                       hidden=[dict(label=h["label"], group=groups[h["gi"]]["gid"], tick_share=h["tick"], lab=h["lab_nats"],
                                    clim_mean=h["clim"]["mean"], clim_sd=h["clim"]["sd"], gate=h["gate"],
                                    plug_prior=h["plug_label"],
                                    theta=theta_json(h["theta"])) for h in HW])
    jdump(f"{arm}/worlds.json", worlds_json)
    # ---- simulations at the true weights (designer side, for C)
    n_ctot = max(CFG["n_csim"], CFG["n_cbig"])
    obsC, UC, _ = sim_mix([h["theta"] for h in HW], n_ctot, 5000 + 100 * ai, f" {arm} C")
    for i, h in enumerate(HW):
        sl = slice(i * n_ctot, i * n_ctot + CFG["n_csim"])
        h["dsC"] = NN.make_dataset(obsC[sl], UC[sl], smu, ssd, seed=i)
        ns = min(CFG["n_csmall"], CFG["n_csim"])
        h["dsCsm"] = NN.make_dataset(obsC[sl][:ns], UC[sl][:ns], smu, ssd, seed=i)
        if CFG["n_cbig"] > 0:
            sb_ = slice(i * n_ctot, i * n_ctot + CFG["n_cbig"])
            h["dsCbig"] = NN.make_dataset(obsC[sb_], UC[sb_], smu, ssd, seed=i)
    del obsC, UC
    # ---- nets, in priority order (a deadline cuts from the end; review of 002, minor 1): the prior nets, C, the
    #      largest Lab budget, the fine-tuned ceiling, the smaller budgets, the second seeds, P0's world-count curve
    nets = {}                                        # name -> (cfg, params)
    tn = time.time()
    sb, bb = CFG["steps_big"][arm], CFG["batch_big"][arm]
    for gi, g in enumerate(groups):
        for nm, cfg, seeds in (("P0", C_FULL, [0, 1]), ("A", C_AM, [10, 11]), ("P0s", C_STATE, [20, 21])):
            try:
                ps, inf = NN.train(cfg, g["ds"], sb[nm], [sd_ + SEED0 for sd_ in seeds], batch=bb, log=log, tag=f" {arm} {nm} g{gi}",
                                   deadline=t_arm_end, eval_every=CFG["eval_every"], pad=pad_big)
                info[f"{nm}|g{gi}"] = inf
                if inf["stopped_early"]:
                    SKIPPED.append(f"{arm} {nm} g{gi} stopped at step {inf['stopped_early']} (deadline)")
                for s, p in enumerate(ps):
                    nets[f"{nm}|g{gi}|s{s}"] = (cfg, p)
                log(f"{arm} {nm} g{gi}: {inf['ms_per_step']:.1f} ms per step ({len(seeds)} nets, batch {bb})")
            except Exception:
                FAILED.append(f"{arm} net {nm} g{gi}")
                log("FAILED " + FAILED[-1] + "\n" + traceback.format_exc())
    log(f"{arm} prior nets done ({time.time() - tn:.0f}s)")

    def p0_init(jobs):
        return {j[0]: nets[f"P0|g{HW[int(j[0].split('|')[1][1:])]['gi']}|s{j[0].split('|')[2][1:]}"][1] for j in jobs}
    dl = {}

    def lab_sets(N):
        if N not in dl:
            N_ = min(N, CFG["n_lab"])
            dl[N] = [NN.make_dataset(h["lab"]["obs"][:N_], h["lab"]["U"][:N_], smu, ssd, seed=N + i) for i, h in enumerate(HW)]
        return dl[N]

    def do(kind, N=None, s=None):
        if kind == "C":
            jobs = [(f"C|w{i}|s{sd}", h["dsC"], 100 + 2 * i + sd) for sd in (0, 1) for i, h in enumerate(HW)]
            got = train_groups(C_FULL, jobs, CFG["steps_C"], nH, tag=f"{arm} C", info=info, deadline=t_arm_end,
                               eval_every=CFG["eval_every"], batch=CFG["batch_C"])
        elif kind == "Csm":      # C on the first n_csmall true-weight episodes: is C converged in data?
            jobs = [(f"Csm|w{i}|s0", h["dsCsm"], 170 + 2 * i) for i, h in enumerate(HW)]
            got = train_groups(C_FULL, jobs, CFG["steps_C"], nH, tag=f"{arm} Csm", info=info, deadline=t_arm_end,
                               eval_every=CFG["eval_every"], batch=CFG["batch_C"], pad=(CFG["n_csim"], NEX * CFG["n_csim"]))
        elif kind == "Cbig":     # C on n_cbig true-weight episodes (the first n_csim of them are C's): the learning curve of C
            jobs = [(f"Cbig|w{i}|s0", h["dsCbig"], 190 + 2 * i) for i, h in enumerate(HW)]
            got = train_groups(C_FULL, jobs, CFG["steps_Cbig"], CFG["lock_Cbig"], tag=f"{arm} Cbig", info=info, deadline=t_arm_end,
                               eval_every=CFG["eval_every"], batch=CFG["batch_C"])
        elif kind == "Cft":      # P0 fine-tuned on the true-weight simulations (the other candidate for the ceiling)
            jobs = [(f"Cft|w{i}|s{sd}", h["dsC"], 150 + 2 * i + sd) for sd in (0, 1) for i, h in enumerate(HW)
                    if f"P0|g{h['gi']}|s{sd}" in nets]
            got = train_groups(C_FULL, jobs, CFG["steps_Cft"], nH, lr=CFG["lr_Cft"], init_of=p0_init(jobs), tag=f"{arm} Cft",
                               info=info, deadline=t_arm_end, eval_every=CFG["eval_every"], batch=CFG["batch_C"])
        elif kind == "D":
            jobs = [(f"D@{N}|w{i}|s{s}", lab_sets(N)[i], 200 + 2 * i + s) for i in range(nH)]
            got = train_groups(C_FULL, jobs, CFG["steps_D"][N], nH, tag=f"{arm} D@{N} s{s}", info=info, deadline=t_arm_end,
                               eval_every=CFG["eval_every_small"], pad=pad_lab)
        else:
            jobs = [(f"FT@{N}|w{i}|s{s}", lab_sets(N)[i], 300 + 2 * i + s) for i in range(nH) if f"P0|g{HW[i]['gi']}|s{s}" in nets]
            got = train_groups(C_FULL, jobs, CFG["steps_FT"][N], nH, lr=CFG["lr_FT"], init_of=p0_init(jobs),
                               tag=f"{arm} FT@{N} s{s}", info=info, deadline=t_arm_end, eval_every=CFG["eval_every_small"], pad=pad_lab)
        nets.update({k: (C_FULL, v) for k, v in got.items()})
    Nmax = max(CFG["budgets"])
    plan = [("C", None, None)] + ([("Cbig", None, None)] if CFG["n_cbig"] > 0 else []) \
        + [("D", Nmax, 0), ("FT", Nmax, 0), ("Cft", None, None), ("Csm", None, None)]
    for N in sorted(CFG["budgets"], reverse=True):
        if N != Nmax:
            plan += [("D", N, 0), ("FT", N, 0)]
    for N in sorted(CFG["seeds2"]):
        plan += [("D", N, 1), ("FT", N, 1)]
    for kind, N, s in plan:
        try:
            do(kind, N, s)
        except Exception:
            FAILED.append(f"{arm} nets {kind} {N} {s}")
            log("FAILED " + FAILED[-1] + "\n" + traceback.format_exc())
    for h in HW:
        h.pop("dsC")
        h.pop("dsCsm")
        h.pop("dsCbig", None)
    if arm == "P":
        obs, U, wo = groups[0]["obs_U_wo"]
        for nw in CFG["nw_curve"]:
            if nw >= groups[0]["n_train_worlds"]:
                continue
            if time.time() > t_arm_end:
                SKIPPED.append(f"{arm} P0[{nw}] (deadline)")
                log("SKIP " + SKIPPED[-1])
                continue
            try:
                sel = wo < nw
                ds = NN.make_dataset(obs[sel], U[sel], smu, ssd, seed=nw, world_of=wo[sel])
                ps, inf = NN.train(C_FULL, ds, sb["P0w"], [30 + SEED0], batch=bb, log=log, tag=f" {arm} P0[{nw}]",
                                   deadline=t_arm_end, eval_every=CFG["eval_every"])
                info[f"P0w{nw}|g0"] = inf
                if inf["stopped_early"]:
                    SKIPPED.append(f"{arm} P0[{nw}] stopped at step {inf['stopped_early']} (deadline)")
                nets[f"P0w{nw}|g0|s0"] = (C_FULL, ps[0])
            except Exception:
                FAILED.append(f"{arm} net P0[{nw}]")
                log("FAILED " + FAILED[-1] + "\n" + traceback.format_exc())
    for g in groups:
        g.pop("obs_U_wo", None)
    CLOCK[f"{arm}_nets_s"] = time.time() - tn
    log(f"{arm} all nets done ({time.time() - tn:.0f}s), {len(nets)} nets")
    jdump(f"{arm}/train_info.json", info)
    # ---- samples and scores
    ts = time.time()
    m = CFG["m"]
    for i, h in enumerate(HW):
        ex, gi = h["ex"], h["gi"]
        D0 = NN.item_dataset(h["hist"], h["Ptest"], smu, ssd)
        for key, (cfg, p) in nets.items():
            parts = key.split("|")
            nm, where, sd = parts[0], parts[1], parts[2]
            if where.startswith("g") and int(where[1:]) != gi:
                continue
            if where.startswith("w") and int(where[1:]) != i:
                continue
            try:
                if nm == "A":
                    for N in CFG["s_budgets"]:
                        N_ = min(N, CFG["n_lab"])
                        Dn = dict(D0)
                        Dn["CS"] = jnp.asarray(np.broadcast_to(h["lab_ST"][:N_].sum((0, 1)), (ex.n, NN.NS)), NN.F32)
                        Dn["CN"] = jnp.full((ex.n,), float(2 * N_), NN.F32)
                        h["S"][f"S@{N}|{sd}"] = FL.score_es(ex, NN.net_samples(cfg, p, Dn, m, 900 + N))
                else:
                    h["S"][f"{nm}|{sd}"] = FL.score_es(ex, NN.net_samples(cfg, p, D0, m, 800))
            except Exception:
                FAILED.append(f"{arm} scores {key} world {i}")
                log("FAILED " + FAILED[-1] + "\n" + traceback.format_exc())
    S, names, world_of, klass = save_scores(arm, HW, "scores.npz")
    npz(f"{arm}/items.npz", hist=np.stack([h["hist"] for h in HW]).astype(np.float32),
        Ptest=np.stack([h["Ptest"] for h in HW]).astype(np.float32))
    CLOCK[f"{arm}_scores_s"] = time.time() - ts
    # ---- quick report (the full analysis is make_summary.py)
    meta = dict(arm=arm, eps=EPS.get(arm), n_hidden=nH, n_items=CFG["n_items"], R=CFG["R"], m=m, names=names,
                hidden_labels=[h["label"] for h in HW], groups=[g["gid"] for g in groups],
                group_of_world=[h["gi"] for h in HW], cells=HW[0]["ex"].cells, quick=None,
                seconds=time.time() - t_arm, clock={k: v for k, v in CLOCK.items()})
    jdump(f"{arm}/meta.json", meta)                  # written before the quick report, which may fail on missing policies
    rep = quick_report(S, world_of, klass)
    meta["quick"] = rep
    jdump(f"{arm}/meta.json", meta)
    log(f"{arm} done in {(time.time() - t_arm) / 60:.1f} min; OES " + ", ".join(f"{k} {v:.3f}" for k, v in rep["oes"].items()))
    log(f"{arm} sigma {rep['sigma']:.3f} (null {rep['null_is']}), no-experiment share of C {rep['share_noexp']:.3f}, "
        f"rho@8 {rep.get('rho@8')}, rho@512 {rep.get('rho@512')}")
    return rep


def seedmean(S, nm):
    ks = [k for k in S if k == nm or k.startswith(nm + "|")]
    return np.mean([S[k] for k in ks], 0) if ks else None


def quick_report(S, world_of, klass):
    base = sorted({k.split("|")[0] for k in S})
    M = {b: seedmean(S, b) for b in base}
    SS = {"climatology": M["K"], "oracle": M["O"], **{b: M[b] for b in base if b not in ("K", "O")}}
    try:
        R = skill_report(SS, n_boot=200, groups=klass)
    except ValueError:                               # tiny test sizes: no cell with a significant denominator
        R = skill_report(SS, n_boot=200, groups=klass, valid=np.ones(M["K"].shape[1], bool))
    L = {b: float(M[b].sum(1).mean()) for b in base}
    if "Cft" in L and "C" in L and L["Cft"] < L["C"]:        # the ceiling is the better of the two (DESIGN.md section 4)
        L["Cscratch"], M["Cscratch"] = L["C"], M["C"]
        L["C"], M["C"] = L["Cft"], M["Cft"]
    Nmax = max(CFG["budgets"])
    nulls = {b: L[b] for b in (f"D@{Nmax}", f"FT@{Nmax}", f"Dr@{Nmax}", "P0", "S@0") if b in L}
    null_is = min(nulls, key=nulls.get) if nulls else None
    out = dict(oes={b: float(R["aggregate"][b]) for b in R["aggregate"] if b not in ("climatology",)},
               oes_pooled={b: float(R["aggregate_pooled"][b]) for b in R["aggregate_pooled"]}, L=L,
               valid=R["valid"], by_class={g: v for g, v in R.get("by_group", {}).items()})
    if "C" in L and null_is:
        out["sigma"] = (nulls[null_is] - L["C"]) / (L["K"] - L["C"])
        out["null_is"] = null_is
        noexp = min(L[b] for b in ("P0", "S@0", "P0s") if b in L)
        out["share_noexp"] = (L["K"] - noexp) / (L["K"] - L["C"])
        for N in CFG["s_budgets"]:
            if f"S@{N}" in L and "P0" in L and abs(L["P0"] - L["C"]) > 0:
                out[f"rho@{N}"] = (L["P0"] - L[f"S@{N}"]) / (L["P0"] - L["C"])
        acc = {"K": M["K"], "C": M["C"], "P0": M["P0"], "O": M["O"]}
        if f"D@{Nmax}" in M:
            acc["D"] = M[f"D@{Nmax}"]
        if f"S@{Nmax}" in M:
            acc["S"] = M[f"S@{Nmax}"]
        a = ACC.shares(acc, worlds=world_of, n_boot=500)
        out["acceptance_code"] = {k: a.get(k) for k in ("sigma", "rho", "null_is", "sigma_worlds", "rho_worlds", "pass_sigma", "pass_rho")}
    else:
        out.update(sigma=float("nan"), null_is=None, share_noexp=float("nan"))
    return out


def shape_test(st_norm):
    """Presmoke only: one lockstep group of MAX_LOCK nets and the shared big nets at the FULL job's array shapes
    (data are noise), 200 steps each, so that a memory failure shows within minutes and the speed is MEASURED.
    Speed guard (written after r6-foundryexam-002, whose nets ran several times slower than the round-5 basis):
    the net time of the full pass is projected from the measured ms per step; if it exceeds 1.25 x the time the
    full pass will have, minus 55 minutes for simulation, hidden worlds, compilation and scoring, the presmoke
    fails (exit 4) before the full pass spends anything."""
    smu, ssd = st_norm
    rng = np.random.default_rng(0)
    t = time.time()
    F = FULL
    E = F["n_csim"]
    obs = np.abs(rng.standard_normal((E, FL.T1, FL.NOBS))).astype(np.float32) + 0.1
    U = np.zeros((E, FL.P + FL.H, FL.NW), np.float32)
    ds = NN.make_dataset(obs, U, smu, ssd, seed=0)
    L16 = NN.Cfg.MAX_LOCK
    _, inf = NN.train(C_FULL, [ds] * L16, 200, list(range(L16)), log=log, tag=" shape lock16 C", eval_every=200, batch=F["batch_C"])
    msC = inf["ms_per_step"]
    dl = NN.make_dataset(obs[: F["n_lab"]], U[: F["n_lab"]], smu, ssd, seed=0)
    _, inf = NN.train(C_FULL, [dl] * L16, 200, list(range(L16)), log=log, tag=" shape lock16 lab", eval_every=200,
                      pad=(F["n_lab"], NEX * F["n_lab"]))
    ms16 = inf["ms_per_step"]
    msB = None
    if F["n_cbig"] > 0:
        Eb_ = F["n_cbig"]
        obsb = np.abs(rng.standard_normal((Eb_, FL.T1, FL.NOBS)).astype(np.float32)) + 0.1
        dsb = NN.make_dataset(obsb, np.zeros((Eb_, FL.P + FL.H, FL.NW), np.float32), smu, ssd, seed=0)
        _, inf = NN.train(C_FULL, [dsb] * F["lock_Cbig"], 200, list(range(F["lock_Cbig"])), log=log, tag=" shape Cbig", eval_every=200,
                          batch=F["batch_C"])
        msB = inf["ms_per_step"]
        del dsb, obsb
    del ds, dl
    nW = 400
    Eb = nW * F["epw"]
    obs = np.abs(rng.standard_normal((Eb, FL.T1, FL.NOBS))).astype(np.float32) + 0.1
    U = np.zeros((Eb, FL.P + FL.H, FL.NW), np.float32)
    wo = np.repeat(np.arange(nW), F["epw"])
    ds = NN.make_dataset(obs, U, smu, ssd, seed=0, world_of=wo, ST=NN.episode_stats(NN.to_grid(obs)), EW=F["epw"])
    ms2 = {}
    for cfg in (C_AM, C_FULL):
        _, inf = NN.train(cfg, ds, 200, [0, 1], batch=F["batch_big"]["P"], log=log, tag=f" shape big {cfg[2]}", eval_every=200)
        ms2[cfg[2]] = inf["ms_per_step"]
    lockC = 3 * F["steps_C"] + 2 * F["steps_Cft"]                      # C (2 seeds), Csm, Cft (2 seeds): lock-steps at batch_C
    lock = sum((F["steps_D"][N] + F["steps_FT"][N]) * (2 if N in F["seeds2"] else 1) for N in F["budgets"])
    sbP = F["steps_big"]["P"]
    proj = {"P": msC * lockC + ms16 * lock + ms2["own"] * (sbP["P0"] + sbP["P0s"] + sbP["P0w"]) + ms2["random"] * sbP["A"]}
    if msB is not None:
        proj["P"] += msB * F["steps_Cbig"] * (F["n_hidden_P"] / F["lock_Cbig"])
    for a in ("N30", "N10"):
        sbn = F["steps_big"][a]
        frac = F["batch_big"][a] / F["batch_big"]["P"]
        proj[a] = ((msC * lockC + ms16 * lock) * (F["n_centres"] * F["n_hidden_N"]) / L16
                   + F["n_centres"] * frac * (ms2["own"] * (sbn["P0"] + sbn["P0s"]) + ms2["random"] * sbn["A"]))
    arms = [a for a in ARMS_FULL if a in proj]
    total_h = sum(proj[a] for a in arms) / 3.6e6
    res = dict(ms_per_step_Cbig=msB, ms_per_step_lock16_C=msC, ms_per_step_lock16_lab=ms16, ms_per_net_step_lock16_lab=ms16 / L16, ms_per_step_big2=ms2,
               lock_steps_per_arm=dict(C=lockC, lab=lock), projected_net_hours={a: proj[a] / 3.6e6 for a in arms}, projected_net_hours_total=total_h,
               full_hours=args.full_hours, seconds=time.time() - t)
    ok = True
    if args.full_hours is not None:
        have = args.full_hours - (time.time() - T0) / 3600 - 55.0 / 60.0
        res["net_hours_available"] = have
        ok = total_h <= 1.25 * have
    res["speed_ok"] = bool(ok)
    jdump("shape_test.json", res)
    log(f"shape test: {msC:.1f} (C) and {ms16:.1f} (lab) ms per step of 16 nets, big nets {ms2}; projected net time "
        f"{total_h:.2f} h for arms {arms}; available {res.get('net_hours_available')}; speed_ok {ok} ({time.time() - t:.0f}s)")
    if not ok:
        log("TOO SLOW: the full pass would not finish its nets; stopping before it starts")
        sys.exit(4)


ARMS_ALL = ["P", "N30", "N10"]
ARM_WEIGHT = {"P": 2.0, "N30": 1.2, "N10": 1.2}       # shares of the time left (arm P is the primary arm)
NEX = sum(FL.T1 - h - FL.P for h in FL.HS)             # examples per episode (anchors t in [16, 32 - h])


def write_info(reps, todo, done=False):
    jdump("info.json", dict(size=args.size, arms=todo, finished=bool(done),
                            config={k: (v if not isinstance(v, dict) else {str(a): b for a, b in v.items()}) for k, v in CFG.items()},
                            platform=dict(jax=jax.__version__, numpy=np.__version__, python=platform.python_version(),
                                          backend=backend, devices=[str(d) for d in jax.devices()], world_dtype="float64",
                                          net_dtype="float32"),
                            member_ticks_public_simulator=RUN.member_ticks, hours=(time.time() - T0) / 3600, failed=FAILED,
                            skipped=SKIPPED, clock=CLOCK, secret_commitment=SECRET.commitment(),
                            arms_done=list(reps), quick={a: r for a, r in reps.items()}))


def main():
    cands, cth = stage_gate()
    world = FL.build_world(cands[0]["theta"], CFG["burn"])
    # public standardisation of the code: window statistics of simulated episodes of pool worlds that are not hidden
    # worlds of arm P (review of 002: the first version drew from all gate-passing pool worlds)
    hid = set()
    if "P" in ARMS:
        hid = {h["label"] for h in arm_groups("P", cands, cth)[0]["hidden"]}
    pool_ok = [c for c in cands if c["kind"] == "pool" and c["ok"] and f"seed{c['prior_seed']}-{c['index']}" not in hid]
    obs, U, _ = sim_mix([c["theta"] for c in pool_ok[:64]], 4, 77, " code-norm")
    st = NN.episode_stats(NN.to_grid(obs)).reshape(-1, NN.NS)
    st_norm = (st.mean(0), np.maximum(st.std(0), 1e-3))
    jdump("code_norm.json", dict(mean=st_norm[0], sd=st_norm[1], n_windows=int(st.shape[0]), n_worlds=len(pool_ok[:64])))
    if CFG["shape_test"]:
        shape_test(st_norm)
    reps = {}
    todo = [a for a in ARMS if a in ARMS_ALL]
    write_info(reps, todo)
    for k, arm in enumerate(todo):
        share = left() * ARM_WEIGHT[arm] / sum(ARM_WEIGHT[a] for a in todo[k:])
        if left() < 600 and args.size == "full":
            SKIPPED.append(f"arm {arm} (time left {left():.0f}s)")
            log("SKIP " + SKIPPED[-1])
            continue
        try:
            reps[arm] = run_arm(arm, cands, cth, world, st_norm, time.time() + 0.92 * share)
        except Exception:
            FAILED.append(f"arm {arm}")
            log("FAILED " + FAILED[-1] + "\n" + traceback.format_exc())
        write_info(reps, todo)
    write_info(reps, todo, done=True)
    log(f"done: arms {list(reps)}, {(time.time() - T0) / 3600:.2f} h, failed {FAILED}, skipped {SKIPPED}")
    bad = bool(FAILED) or (STRICT and bool(SKIPPED)) or not reps
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
