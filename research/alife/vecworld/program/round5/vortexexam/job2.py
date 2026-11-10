"""job2 -- round 5, study vortexexam (track 2), GPU job 2: the fed-vortex exam pilot (simulate-to-train).

PILOT ONLY: the hidden parameters of the truths are drawn inside the job from the public prior and WRITTEN TO THE
OUTPUTS, so these truths, Lab data and exam items must NEVER be reused as an exam. The world secret (256 bits,
os.urandom) is never written; only its commitment is.

Public: the simulator (vxlib.Runner), the prior box and viability rule (prior.json), the episode shape, the program
mix, the level-2 scales. Hidden: theta (prior.json names) and the noise keys.

Episode (vxlib.run_episodes): declared initial law, T_ep ticks; at each tick of prog_ticks a program of the public
mix (classes a none, b blind, c aimed at the heaviest kind-b vortex of the revealed list, d regional; c_prog nats)
starts. The Lab, the agent's simulations and the exam's main runs all have this shape.

Stages (each writes to --out as it finishes; progress in OUT/progress.txt):
  A rate       member-ticks/s at the exam size; sizes are scaled to the time budget (declared presets).
  B episodes   one batch: the design (N_theta box draws x K_d episodes from the public simulator), and for every
               truth candidate (box draws, secret rng) its n_lab Lab episodes and J_main exam main runs (secret
               keys). Truths = the first n_truth candidates whose two screening episodes pass the public viability
               rule. Design -> p_v(theta). Lab budgets = nested prefixes; ticks and nats counted with vw.nats
               (episode cap = n_prog x c_prog).
  E identify   synthetic likelihood (vxsbi, from round4/sbi) on linear-regression summaries of level-1 histories
               and, separately, of level-2 histories; posterior under p_v by importance sampling.
  F exam       per truth J_main main runs; items = (run, anchor in prog_ticks): history = the run's level-1 list
               up to the anchor, test program = the mix program built at the anchor, R replicate truths with fresh
               secret noise from the hidden state, queries: level 2 = (N, s_b) at h in HS ticks.
               References: O = leave-one-out over the replicates; K = the other main runs at the same tick;
               K0 = design episodes at the same tick (the prior climatology). Time permitting, R_ctl further
               replicates per item run WITHOUT the test program ('O_noinput': the simulator from the hidden state
               that ignores the program), which measures how much the programs move level 2 (per program class).
  G predict    families net / ridge / law / lin2 (vxnet; lin2 = linear in the level-2 history only, the round-3
               closure's predictor) under the policies
                 D@n   trained on the Lab's first n episodes          P0   trained on the design (prior) episodes
                 S@n   theta-conditional, theta ~ posterior(n)        C    theta-conditional at the true theta
                 PM    theta-conditional at the prior mean            PP   theta-conditional, theta ~ prior
                 S2@n  as S@n with the level-2-only posterior         Cded trained on n_C simulations at the truth
                 Sded@4  unconditional, trained on n_C simulations at posterior(4) draws (time permitting)
  H report     fair energy scores per item and cell (vw.scoring), OES (vw.scoring.skill_report), sigma and rho per
               family and budget (round5/agentenv/evaluator/acceptance.py: the program's one implementation, with
               its bootstrap clustered by hidden world), the share of the oracle-predictable change of s_b reached
               by each predictor (pooled as in round 3, and within each truth).
No grader is defined here: scoring and acceptance are the shared modules above.
Outputs: every file is written atomically and kept under 20 MB (design summaries in parts); the total is audited
at the end (limit 50 MB on the gpu-jobs branch).
usage: python -B job2.py --out DIR [--prior prior.json] [--smoke] [--max-hours 2.6]

Changed AFTER the run of r5-vortexexam-003 (which used this file at 84550bc04), following the Mac's review of that
job: every JSON and npz output now carries PILOT_NEVER_REUSE_AS_EXAM; a file over the per-file limit, an output
dropped by the audit and a failed final report now give a non-zero exit. Nothing else differs.
"""
from __future__ import annotations

import argparse
import gc
import json
import os
import platform
import sys
import time
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import vxlib as VX  # noqa: E402
import vxsbi as SB  # noqa: E402
import vxnet as NN  # noqa: E402

sys.path.insert(1, os.path.join(os.path.dirname(HERE), "agentenv"))
from evaluator import acceptance as ACC  # noqa: E402  (sigma and rho: the shared implementation)

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

from vw.nats import NatsAccountant, NatsBudget  # noqa: E402
from vw.scoring import energy_fair, energy_loo, paired_gap, public_report, skill_report  # noqa: E402
from vw.secret import Secret  # noqa: E402
from vw.world import make_key, member_keys  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
ap.add_argument("--prior", default=os.path.join(HERE, "prior.json"))
ap.add_argument("--smoke", action="store_true")
ap.add_argument("--max-hours", type=float, default=2.6)
ap.add_argument("--preset", default="")
ap.add_argument("--smoke-names", default="", help="smoke only: hidden parameters (and boxes) taken from --prior")
args = ap.parse_args()
OUT = args.out
os.makedirs(OUT, exist_ok=True)
T0 = time.time()

PRESETS = {
    "xl": dict(n_cand=16, n_truth=12, N_theta=768, K_d=2, n_lab=16, budgets=[1, 2, 4, 8, 16], J_main=16, R=12, n_C=48),
    "full": dict(n_cand=14, n_truth=10, N_theta=512, K_d=2, n_lab=16, budgets=[1, 2, 4, 8, 16], J_main=12, R=8, n_C=32),
    "mid": dict(n_cand=12, n_truth=8, N_theta=384, K_d=2, n_lab=16, budgets=[1, 2, 4, 8, 16], J_main=12, R=8, n_C=24),
    # two steps added after r5-vortexexam-003: on an A100 at 169 member-ticks/s 'mid' missed its budget by 43 s and
    # the job fell from 773 thousand planned member-ticks to the 294 thousand of 'small'
    "mid2": dict(n_cand=11, n_truth=8, N_theta=320, K_d=2, n_lab=16, budgets=[1, 2, 4, 8, 16], J_main=10, R=8, n_C=16),
    "low": dict(n_cand=10, n_truth=8, N_theta=256, K_d=2, n_lab=8, budgets=[1, 2, 4, 8], J_main=10, R=6, n_C=12),
    "small": dict(n_cand=10, n_truth=6, N_theta=192, K_d=2, n_lab=8, budgets=[1, 2, 4, 8], J_main=8, R=6, n_C=0),
}
COMMON = dict(m=64, steps_sim=8000, steps_real={1: 600, 2: 800, 4: 1000, 8: 1500, 16: 2000}, steps_C=3000,
              rate_B=[256, 1024], n_post_draws=1000, sded_budget=4, R_ctl=6)
if args.smoke:
    PR = {"H": 32, "names": ["eps", "mut128"], "lo": [0.0, 0.00625], "hi": [0.4, 0.025], "T_ep": 24,
          "prog_ticks": [8, 14], "c_prog": 200.0, "hs": [2, 4, 6], "viability": {"n_min": 1.0, "t_from": 4},
          "const": {}, "smoke": True}
    VX.LAB_T, VX.LAB_TICK = 0.3, 3
    VX.THETA0["mut128"] = 0.0125
    NN.A_MIN, NN.STRIDE, NN.LAGS = 5, 1, (0, 1, 2, 4)
    NN.Cfg.EVAL_EVERY = 10
    SB.WINDOWS = ((3, 10), (10, 17), (17, 25))
    PRESETS = {"smoke": dict(n_cand=3, n_truth=2, N_theta=10, K_d=2, n_lab=4, budgets=[1, 2, 4], J_main=3, R=3, n_C=3)}
    COMMON = dict(m=6, steps_sim=30, steps_real={1: 20, 2: 20, 4: 20}, steps_C=20, rate_B=[4], n_post_draws=50,
                  sded_budget=2, R_ctl=2)
    N_SUB = 5
    if args.smoke_names:                           # the smoke test with another hidden set (boxes of --prior)
        _p = json.load(open(args.prior))
        _nm = args.smoke_names.split(",")
        PR.update(names=_nm, lo=[_p["lo"][_p["names"].index(n)] for n in _nm],
                  hi=[_p["hi"][_p["names"].index(n)] for n in _nm])
else:
    PR = json.load(open(args.prior))
    N_SUB = VX.N_SUB
H = int(PR["H"])
NAMES = list(PR["names"])
LO, HI = np.array(PR["lo"], float), np.array(PR["hi"], float)
CEN, HW = (LO + HI) / 2, (HI - LO) / 2
D_TH = len(NAMES)
VX.T_EP, VX.PROG_TICKS, VX.C_PROG, VX.HS = int(PR["T_ep"]), tuple(PR["prog_ticks"]), float(PR["c_prog"]), tuple(PR["hs"])
NN.set_const(PR.get("const", {}))
T_EP, PROG, HS, HB = VX.T_EP, VX.PROG_TICKS, VX.HS, max(VX.HS)
if not args.smoke:                                # four equal windows from the labelling to the end of the episode
    _e = np.linspace(VX.LAB_TICK, T_EP + 1, 5).round().astype(int)
    SB.WINDOWS = tuple((int(a), int(b)) for a, b in zip(_e[:-1], _e[1:]))
assert max(PROG) + HB <= T_EP, "the last anchor plus the longest horizon must fit in the episode"
VIAB = PR["viability"]
FAILED = []
CLOCK = {}
TRAIN = {}


def to_u(theta):
    return (np.asarray(theta, float) - CEN) / HW


def from_u(u):
    return CEN + np.asarray(u, float) * HW


def Q_of(thetas):
    th = np.atleast_2d(np.asarray(thetas, float))
    return VX.theta_batch(len(th), **{n: th[:, i] for i, n in enumerate(NAMES)})


def log(msg):
    line = f"{time.strftime('%H:%M:%S')} [{(time.time() - T0) / 60:6.1f} min] {msg}"
    print(line, flush=True)
    with open(os.path.join(OUT, "progress.txt"), "a") as f:
        f.write(line + "\n")


MARK = "PILOT_NEVER_REUSE_AS_EXAM"


def jdump(name, obj):
    def conv(o):
        if isinstance(o, (np.floating, np.integer)):
            return o.item()
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, np.bool_):
            return bool(o)
        return str(o)
    if isinstance(obj, dict):                      # every output says what it is (the Mac's review of job 2, point 2)
        obj = {MARK: True, **obj}
    elif isinstance(obj, list):
        obj = [({MARK: True, **o} if isinstance(o, dict) else o) for o in obj]
    p = os.path.join(OUT, name)
    with open(p + ".tmp", "w") as f:
        json.dump(obj, f, indent=1, default=conv)
    os.replace(p + ".tmp", p)


FILE_LIMIT = 19 * 2 ** 20          # bytes per output file (the gpu-jobs branch takes 20 MB)
TOTAL_LIMIT = 40 * 2 ** 20         # bytes of job 2 in OUT (the branch takes 50 MB per request; the scan adds 6)


def save_npz(name, **arrays):
    """Atomic compressed npz in OUT; returns its size in bytes (logged when large)."""
    p = os.path.join(OUT, name)
    tmp = p + ".tmp.npz"
    np.savez_compressed(tmp, **{MARK: np.array(True)}, **arrays)
    os.replace(tmp, p)
    n = os.path.getsize(p)
    if n > 2 ** 20:
        log(f"    wrote {name}: {n / 2 ** 20:.1f} MB")
    if n > FILE_LIMIT and f"output over the per-file limit: {name}" not in FAILED:
        log(f"    WARNING {name} is over the per-file limit ({n} > {FILE_LIMIT} bytes)")
        FAILED.append(f"output over the per-file limit: {name}")
    return n


def sparse_U(U):
    """Dense programs (E, T, m) float32 -> the non-zero entries (programs are a few ticks x a few coefficients)."""
    U = np.asarray(U, np.float32)
    idx = np.argwhere(U != 0)
    return {"U_idx": idx.astype(np.int32), "U_val": U[tuple(idx.T)], "U_shape": np.array(U.shape)}


def audit_outputs():
    """Sizes of everything in OUT; files over the per-file limit or beyond the total are deleted, least needed
    first (the design summaries are the only large ones), and the deletion is recorded."""
    def listing():
        out = {}
        for root, _, files in os.walk(OUT):
            for f in files:
                q = os.path.join(root, f)
                out[os.path.relpath(q, OUT)] = os.path.getsize(q)
        return out
    sizes, dropped = listing(), []
    for f, n in sorted(sizes.items()):
        if n > FILE_LIMIT:
            os.remove(os.path.join(OUT, f))
            dropped.append([f, n, "over the per-file limit"])
    order = sorted([f for f in listing() if f.startswith("design_S_")], reverse=True)
    while sum(listing().values()) > TOTAL_LIMIT and order:
        f = order.pop(0)
        dropped.append([f, os.path.getsize(os.path.join(OUT, f)), "total over the limit"])
        os.remove(os.path.join(OUT, f))
    sizes = listing()
    INFO["outputs"] = {"total_bytes": int(sum(sizes.values())), "largest": sorted(sizes.items(), key=lambda kv: -kv[1])[:6],
                       "dropped": dropped, "file_limit": FILE_LIMIT, "total_limit": TOTAL_LIMIT}
    log(f"outputs: {sum(sizes.values()) / 2 ** 20:.1f} MB in {len(sizes)} files; largest "
        f"{[(k, round(v / 2 ** 20, 1)) for k, v in INFO['outputs']['largest'][:3]]}; dropped {dropped}")
    if dropped:
        FAILED.append("dropped outputs over the size limits")


def hours():
    return (time.time() - T0) / 3600


def left_s():
    return args.max_hours * 3600 - (time.time() - T0)


def ticks(stage, n):
    CLOCK[stage] = CLOCK.get(stage, 0) + int(n)


def release():
    jax.clear_caches()
    gc.collect()


INFO = {"study": "round5/vortexexam job2", "pilot_never_reusable_as_exam": True,
        "versions": {"python": platform.python_version(), "jax": jax.__version__, "numpy": np.__version__},
        "backend": jax.default_backend(), "devices": [str(d) for d in jax.devices()], "smoke": args.smoke,
        "prior": PR, "common": {k: (v if not isinstance(v, dict) else {str(a): b for a, b in v.items()})
                                for k, v in COMMON.items()},
        "net": {k: getattr(NN.Cfg, k) for k in dir(NN.Cfg) if k.isupper()}, "lags": NN.LAGS, "hist": NN.HIST,
        "feature_windows": SB.WINDOWS,
        "const": NN.CONST, "precision": "float64 world, float32 vortex lists and nets"}
log(f"backend {INFO['backend']} devices {INFO['devices']} jax {jax.__version__} smoke={args.smoke} H={H} theta={NAMES}")
if not args.smoke:                               # a CPU fallback must not spend GPU-pod time (the Mac's review, point 1)
    assert jax.default_backend() == "gpu", f"job2 needs the GPU backend, got {jax.default_backend()!r} ({jax.devices()})"
SEC = Secret()
INFO["secret_commitment"] = SEC.commitment()
jdump("info.json", INFO)
RN = VX.Runner(H, n_sub=N_SUB)
BMAX = 256
CFG = {}


# ----------------------------------------------------------------------------- A rate and sizes
def stage_rate():
    global BMAX, CFG
    rows = []
    for B in COMMON["rate_B"]:
        try:
            Q = VX.theta_batch(B)
            keys = member_keys(make_key(901, H), B)
            X, M = RN.init(Q, keys)
            kp = RN.proc_keys(keys)
            U = np.zeros((2, B, RN.m))
            t0 = time.time()
            X, M, _ = RN.run(Q, X, M, kp, 0, U)
            t1 = time.time() - t0
            t0 = time.time()
            X, M, _ = RN.run(Q, X, M, kp, 2, U)
            dt = time.time() - t0
            rows.append({"B": B, "member_ticks_per_s": 2 * B / dt, "first_call_s": t1})
            log(f"  rate H={H} B={B}: {2 * B / dt:.1f} member-ticks/s (first call {t1:.0f}s)")
            del X, M
        except Exception as exc:
            rows.append({"B": B, "error": repr(exc)[:300]})
            log(f"  rate B={B} FAILED {repr(exc)[:200]}")
        release()
    ok = [r for r in rows if "error" not in r]
    best = max(ok, key=lambda r: r["member_ticks_per_s"])
    BMAX, rate = best["B"], best["member_ticks_per_s"]

    def work(p):
        nt = p["n_truth"]
        return ((p["N_theta"] * p["K_d"] + p["n_cand"] * (p["n_lab"] + p["J_main"])) * T_EP
                + nt * p["J_main"] * len(PROG) * (p["R"] + COMMON["R_ctl"]) * HB + 2 * nt * p["n_C"] * T_EP)
    budget = 0.72 * left_s()                       # the rest: compiles, training, scoring, slack
    name = None
    for nm in (["smoke"] if args.smoke else ["xl", "full", "mid", "mid2", "low", "small"]):
        if args.preset and nm != args.preset:
            continue
        if args.smoke or args.preset or work(PRESETS[nm]) / (0.8 * rate) <= budget:
            name = nm
            break
    if name is None:
        name = "small"
    CFG = dict(PRESETS[name], **COMMON)
    INFO.update(rate_rows=rows, bmax=BMAX, rate=rate, preset=name, config={k: (v if not isinstance(v, dict) else
                {str(a): b for a, b in v.items()}) for k, v in CFG.items()},
                planned_member_ticks=work(PRESETS[name]),
                planned_sim_seconds_at_0p8_rate=work(PRESETS[name]) / (0.8 * rate))
    jdump("info.json", INFO)
    log(f"== preset {name}: {work(PRESETS[name])} member-ticks planned, est {work(PRESETS[name]) / (0.8 * rate) / 60:.0f} min "
        f"of sims at batch {BMAX}; budget {budget / 60:.0f} min")


def run_eps(thetas, keys, seed, tag, classes=None, snaps=None, snap_idx=None):
    """vxlib.run_episodes in member chunks of BMAX; outputs concatenated. snaps: ticks at which the device states
    of the members snap_idx (sorted global indices) are kept -> out["snaps"][tick] = (X, M) in snap_idx order."""
    th = np.atleast_2d(np.asarray(thetas, float))
    B = len(th)
    outs = []
    kept = {a: [] for a in (snaps or ())}
    snap_idx = np.arange(B) if snap_idx is None else np.asarray(snap_idx)
    assert (np.diff(snap_idx) > 0).all()
    for s in range(0, B, BMAX):
        e = min(s + BMAX, B)
        loc = snap_idx[(snap_idx >= s) & (snap_idx < e)] - s
        o = VX.run_episodes(RN, Q_of(th[s:e]), keys[s:e], seed * 1000 + s, T=T_EP, prog_ticks=PROG, nats=VX.C_PROG,
                            classes=None if classes is None else classes[s:e], snaps=snaps if len(loc) else None,
                            log=log if (e - s) >= 64 else None, tag=tag)
        for a, (X, M) in (o.pop("snaps", None) or {}).items():       # keep only the members that are branched later
            kept[a].append((VX.take(X, loc), VX.take(M, loc)))
        outs.append(o)
        log(f"    {tag}: episodes {e}/{B} ({hours():.2f} h)")
    ticks(tag, B * T_EP)
    out = {k: np.concatenate([o[k] for o in outs]) for k in ("S", "U", "cls", "nats", "overflow", "finite")}
    out["viable"] = VX.viable(out["S"], out["overflow"], out["finite"], RN.K, VIAB["n_min"], VIAB["t_from"])
    if snaps:
        out["snaps"] = {a: (jax.tree_util.tree_map(lambda *xs: jnp.concatenate(xs), *[x for x, _ in kept[a]]),
                            jnp.concatenate([m for _, m in kept[a]])) for a in snaps}
    return out


# ----------------------------------------------------------------------------- B-D one batch of episodes
def stage_episodes():
    """Design episodes (public keys), and for every truth candidate its Lab episodes and exam main runs (secret
    keys), all in one batch for throughput. The truths are the first n_truth candidates (draw order) whose two
    screening episodes (Lab episodes 0 and 1) pass the public viability rule."""
    N, K, nc, nL, J = CFG["N_theta"], CFG["K_d"], CFG["n_cand"], CFG["n_lab"], CFG["J_main"]
    rng = SEC.rng("truth-draws")
    cand = LO + (HI - LO) * rng.random((nc, D_TH))
    Ud = np.random.default_rng(4402).uniform(-1, 1, (N, D_TH))
    th = np.concatenate([np.repeat(from_u(Ud), K, 0), np.repeat(cand, nL, 0), np.repeat(cand, J, 0)])
    keys = jnp.concatenate([member_keys(make_key(4402, H), N * K)]
                           + [SEC.child("lab", i).keys(nL, "episode") for i in range(nc)]
                           + [SEC.child("exam", i).keys(J, "main") for i in range(nc)])
    cls = np.concatenate([np.random.default_rng(4405).choice(list(VX.PROGRAM_CLASSES), size=(N * K, len(PROG))),
                          np.random.default_rng(7700).choice(list(VX.PROGRAM_CLASSES), size=(nc * nL, len(PROG))),
                          SEC.rng("exam-classes").choice(list(VX.PROGRAM_CLASSES), size=(nc * J, len(PROG)))])
    nD, nLb = N * K, nc * nL
    allr = run_eps(th, keys, 21, "episodes", classes=cls, snaps=PROG, snap_idx=np.arange(nD + nLb, nD + nLb + nc * J))
    sl = {"design": slice(0, nD), "lab": slice(nD, nD + nLb), "exam": slice(nD + nLb, nD + nLb + nc * J)}
    part = lambda nm: {k: allr[k][sl[nm]] for k in ("S", "U", "cls", "nats", "overflow", "finite", "viable")}  # noqa: E731
    sim, lab, exm = part("design"), part("lab"), part("exam")
    ticks("design", nD * T_EP)
    ticks("lab_all_candidates", nLb * T_EP)
    ticks("exam_main_all_candidates", nc * J * T_EP)
    CLOCK.pop("episodes", None)
    # truths
    okc = lab["viable"].reshape(nc, nL)[:, :2].all(1)
    sel = [i for i in range(nc) if okc[i]][:CFG["n_truth"]]
    forced = False
    if len(sel) < CFG["n_truth"]:
        if args.smoke:
            sel, forced = list(range(CFG["n_truth"])), True
        elif len(sel) < 4:
            raise RuntimeError(f"only {len(sel)} viable candidates")
    truths = cand[sel]
    jdump("truths.json", {"PILOT_NEVER_REUSE_AS_EXAM": True, "names": NAMES, "candidates": cand.tolist(),
                          "candidate_viable": okc.tolist(), "n_viable": int(okc.sum()), "selected": sel,
                          "truths": truths.tolist(), "forced_smoke": forced, "secret_commitment": SEC.commitment(),
                          "lab_viable_episodes": lab["viable"].reshape(nc, nL).sum(1).tolist(),
                          "exam_main_viable_runs": exm["viable"].reshape(nc, J).sum(1).tolist(),
                          "note": "candidates drawn inside the job from the public prior box (secret rng); truths = the "
                                  "first viable candidates in draw order (screening = Lab episodes 0 and 1 under the "
                                  "public viability rule); the secret is not stored"})
    log(f"truths {np.round(truths, 4).tolist()} ({int(okc.sum())}/{nc} candidates viable)")
    # design -> viability prior
    v = sim["viable"].reshape(N, K)
    pv = SB.ViabilityPrior().fit(Ud, v.all(1).astype(float))
    save_npz("design.npz", u=Ud, cls=sim["cls"], nats=sim["nats"], viable=v, overflow=sim["overflow"],
             names=np.array(VX.S2_NAMES), theta_names=np.array(NAMES), lo=LO, hi=HI, K_d=K, **sparse_U(sim["U"]))
    per_file = 512                                           # episodes per file: 512 x (T+1) x 14 float16 = 5.8 MB raw
    for q, s0 in enumerate(range(0, nD, per_file)):          # level-1 summaries of the design episodes, in parts
        save_npz(f"design_S_{q:02d}.npz", S=sim["S"][s0:s0 + per_file].astype(np.float16), first_episode=s0)
    jdump("viability_prior.json", {"diag": pv.diag, "w": pv.w.tolist(), "features": "poly_feats(u, 2)",
                                   "rule": VIAB, "frac_episodes_viable": float(v.mean()),
                                   "frac_theta_viable": float(v.all(1).mean())})
    log(f"design: {v.mean():.3f} of episodes viable, {v.all(1).mean():.3f} of thetas; p_v {pv.diag}")
    pdraws, pm, psd = SB.prior_draws(pv, D_TH, 20000, np.random.default_rng(4404))
    # Lab of the truths: accounting with vw.nats
    nT = len(sel)
    labS = lab["S"].reshape(nc, nL, T_EP + 1, -1)[sel]
    labU = lab["U"].reshape(nc, nL, T_EP, -1)[sel]
    cap = len(PROG) * VX.C_PROG * (1 + 1e-4)                   # programs are stored in float32
    budget = NatsBudget.isotropic(RN.m, VX.SIGMA_A, episode=cap, total=cap * nL)
    out = []
    for i in range(nT):
        acct = NatsAccountant(budget)
        per_ep = []
        for e in range(nL):
            acct.new_episode()
            prog = [(t, labU[i, e, t].astype(float)) for t in range(T_EP) if np.abs(labU[i, e, t]).max() > 0]
            acct.check_program(prog, episode_used=0.0)
            per_ep.append(float(sum(acct.charge(u) for _, u in prog)))
        cum = np.cumsum(per_ep)
        out.append({"truth": i, "usage_final": acct.usage(),
                    "per_budget": {str(n): {"episodes": n, "ticks": n * T_EP, "nats": float(cum[n - 1])}
                                   for n in CFG["budgets"]},
                    "caps": {"nats_episode": cap, "ticks_per_episode": T_EP},
                    "viable_episodes": int(lab["viable"].reshape(nc, nL)[sel[i]].sum())})
    jdump("lab.json", out)
    save_npz("lab.npz", S=labS.astype(np.float16), cls=lab["cls"].reshape(nc, nL, -1)[sel],
             nats=lab["nats"].reshape(nc, nL)[sel], viable=lab["viable"].reshape(nc, nL)[sel],
             **sparse_U(labU.reshape(len(sel) * nL, T_EP, -1)))
    # exam main runs of the truths and their snapshots (snapshots hold all candidates' runs, in member order)
    ex_loc = np.concatenate([i * J + np.arange(J) for i in sel])
    exam = {"S": exm["S"].reshape(nc, J, T_EP + 1, -1)[sel], "U": exm["U"].reshape(nc, J, T_EP, -1)[sel],
            "cls": exm["cls"].reshape(nc, J, -1)[sel], "viable": exm["viable"].reshape(nc, J)[sel],
            "snaps": {a: (VX.take(allr["snaps"][a][0], ex_loc), VX.take(allr["snaps"][a][1], ex_loc)) for a in PROG}}
    del allr
    gc.collect()
    return truths, Ud, sim, pv, pdraws, pm, psd, labS, labU, exam


# ----------------------------------------------------------------------------- E identification
def stage_identify(Ud, sim, labS, truths, pv, pm, psd):
    N, K = CFG["N_theta"], CFG["K_d"]
    res, draws, state = [], {}, {}
    rng = np.random.default_rng(4403)
    vth = sim["viable"].reshape(N, K).all(1)                    # the emulator is fitted where the prior has support
    if vth.sum() < 8:
        vth = np.ones(N, bool)
    for level in (1, 2):
        Fd, fn = SB.episode_features(sim["S"], VX.S2_NAMES, level)
        proj = SB.Projection().fit(Fd[np.repeat(vth, K)], np.repeat(Ud[vth], K, 0))
        Sd = proj(Fd).reshape(N, K, -1)
        em = SB.Emulator().fit(Ud[vth], Sd[vth])
        state[level] = {"projection_r2": proj.r2, "emulator": em.diag, "n_features": len(fn),
                        "n_theta_viable": int(vth.sum())}
        log(f"  level-{level} summaries: projection R2 {np.round(proj.r2, 3).tolist()}, emulator CV R2 "
            f"{np.round(em.diag['cv_r2_of_mean'], 3).tolist()}")
        for i, th in enumerate(truths):
            ut = to_u(th)
            Fl, _ = SB.episode_features(labS[i], VX.S2_NAMES, level)
            sl = proj(Fl)
            for n in CFG["budgets"]:
                sbar = sl[:n].mean(0)
                post = SB.posterior(em, pv, sbar, n, rng, D_TH)
                chk = SB.posterior_checks(post, em, pv, sbar, n, ut)
                draws[(level, i, n)] = post["u"]
                res.append({"level": level, "truth": i, "n_episodes": n, "ticks": n * T_EP, "ess": post["ess"],
                            "post_mean_theta": from_u(post["mean_u"]).tolist(),
                            "post_sd_theta": (post["sd_u"] * HW).tolist(),
                            "contraction_sd_ratio": (post["sd_u"] / psd).tolist(),
                            "abs_err_over_prior_sd": (np.abs(post["mean_u"] - ut) / psd).tolist(), **chk})
    cov = {}
    for level in (1, 2):
        for n in CFG["budgets"]:
            rr = [r for r in res if r["n_episodes"] == n and r["level"] == level]
            cov[f"L{level}@{n}"] = {
                "in50_frac": float(np.mean([r["in50"] for r in rr])), "in90_frac": float(np.mean([r["in90"] for r in rr])),
                "hpd_le_50_frac": float(np.mean([r["hpd_level"] <= 0.5 for r in rr])),
                "hpd_le_90_frac": float(np.mean([r["hpd_level"] <= 0.9 for r in rr])),
                "contraction_mean": np.mean([r["contraction_sd_ratio"] for r in rr], 0).tolist(),
                "abs_err_over_prior_sd_mean": np.mean([r["abs_err_over_prior_sd"] for r in rr], 0).tolist(),
                "n_truths": len(rr)}
            log(f"  L{level}@{n}: contraction {np.round(cov[f'L{level}@{n}']['contraction_mean'], 3).tolist()} "
                f"in90 {cov[f'L{level}@{n}']['in90_frac']:.2f} err/prior sd "
                f"{np.round(cov[f'L{level}@{n}']['abs_err_over_prior_sd_mean'], 2).tolist()}")
    jdump("identification.json", {
        "method": "Gaussian synthetic likelihood on d linear-regression summaries per episode (mean over the budget's "
                  "episodes); cubic emulator + emulator and CV-misfit covariance; importance sampling under p_v "
                  "(vxsbi, from round4/sbi/sbi_lib)",
        "names": NAMES, "prior_mean_u": pm.tolist(), "prior_sd_u": psd.tolist(), "prior_sd_theta": (psd * HW).tolist(),
        "state": state, "per_truth_budget": res, "coverage": cov})
    save_npz("posterior_draws.npz", **{f"L{l}_t{i}_n{n}": from_u(d[:CFG["n_post_draws"]]).astype(np.float32)
                                       for (l, i, n), d in draws.items()})
    return draws


# ----------------------------------------------------------------------------- F exam
def stage_exam(truths, exam):
    nT, J, R = len(truths), CFG["J_main"], CFG["R"]
    th = np.repeat(truths, J, 0)
    Bm = nT * J
    Um = exam["U"].reshape(Bm, T_EP, -1)
    Qall = Q_of(th)

    def replicates(tag, n_rep, with_program):
        """n_rep fresh-noise continuations of every main run from every anchor -> (Bm, nA, n_rep, nh, 2)."""
        out = np.zeros((Bm, len(PROG), n_rep, len(HS), 2), np.float32)
        idx = np.repeat(np.arange(Bm), n_rep)
        Qr = {k: v[idx] for k, v in Qall.items()}
        for ai, a in enumerate(PROG):
            X, M = exam["snaps"][a]
            kr = jnp.concatenate([SEC.child("exam", tag, a).keys(n_rep, "member", b) for b in range(Bm)])
            kp = RN.proc_keys(kr, fresh=True)
            Ur = np.repeat(Um[:, a:a + HB], n_rep, 0).transpose(1, 0, 2)               # (HB, Bm * n_rep, m)
            if not with_program:
                Ur = np.zeros_like(Ur)
            l2 = np.zeros((Bm * n_rep, HB, 2), np.float32)
            for s2 in range(0, Bm * n_rep, BMAX):
                e2 = min(s2 + BMAX, Bm * n_rep)
                ii = idx[s2:e2]
                _, _, Yl = RN.run({k: v[s2:e2] for k, v in Qr.items()}, VX.take(X, ii), VX.take(M, ii), kp[s2:e2], a,
                                  Ur[:, s2:e2])
                l2[s2:e2] = VX.level2(Yl.transpose(1, 0, 2), RN.K)
            out[:, ai] = l2.reshape(Bm, n_rep, HB, 2)[:, :, [h - 1 for h in HS]]
            log(f"    exam {tag} replicates at anchor {a} done ({hours():.2f} h)")
        ticks(f"exam_{tag}", Bm * len(PROG) * n_rep * HB)
        return out.reshape(nT, J, len(PROG), n_rep, len(HS), 2)
    Y = replicates("rep", R, True)
    save_npz("exam.npz", S=exam["S"].astype(np.float16), Y=Y, cls=exam["cls"], viable=exam["viable"],
             anchors=np.array(PROG), hs=np.array(HS), **sparse_U(Um))
    # controls without the test program (how much do the programs move level 2?), if the time allows
    Rc, Yc = CFG["R_ctl"], None
    need = Bm * len(PROG) * Rc * HB / (0.8 * INFO["rate"])
    reserve = 2 * nT * CFG["n_C"] * T_EP / (0.8 * INFO["rate"]) + 1500           # dedicated simulations and training
    if Rc > 0 and (args.smoke or left_s() > need + reserve):
        Yc = replicates("ctl", Rc, False)
        save_npz("exam.npz", S=exam["S"].astype(np.float16), Y=Y, Y_noinput=Yc, cls=exam["cls"], viable=exam["viable"],
                 anchors=np.array(PROG), hs=np.array(HS), **sparse_U(Um))
    elif Rc > 0:
        log(f"  SKIP no-input controls: need {need:.0f}s + reserve {reserve:.0f}s, {left_s():.0f}s left")
        FAILED.append("skipped input controls")
    exam.pop("snaps")
    log(f"exam: {nT} truths x {J} runs x {len(PROG)} anchors = {nT * J * len(PROG)} items, R = {R}; main runs viable "
        f"{exam['viable'].mean():.3f}")
    return exam["S"], exam["U"], Y, Yc, exam["cls"]


# ----------------------------------------------------------------------------- G predictors, H report
CELLS = [(h, c) for h in range(3) for c in ("joint", "N", "s_b")]
CLASSES = []         # program class of every item, in the pooled item order
SCORES = {}          # name -> list over truths of (n_items, n_cells)
MEANS = {}           # name -> list over truths of predictive means (n_items, nh, 2)


def es_cells(samples, truths):
    """samples (n, m, nh, 2), truths (n, R, nh, 2) in level-2 units -> (n, nh * 3) fair energy scores."""
    sc = NN.sc2()
    n, _, nh, _ = samples.shape
    out = np.zeros((n, nh, 3))
    for j in range(nh):
        X, Yt = samples[:, :, j] / sc, truths[:, :, j] / sc
        out[:, j, 0] = energy_fair(X, Yt)
        out[:, j, 1] = energy_fair(X[..., :1], Yt[..., :1])
        out[:, j, 2] = energy_fair(X[..., 1:], Yt[..., 1:])
    return out.reshape(n, -1)


def oracle_cells(truths):
    sc = NN.sc2()
    n, _, nh, _ = truths.shape
    out = np.zeros((n, nh, 3))
    for j in range(nh):
        Yt = truths[:, :, j] / sc
        out[:, j, 0] = energy_loo(Yt)
        out[:, j, 1] = energy_loo(Yt[..., :1])
        out[:, j, 2] = energy_loo(Yt[..., 1:])
    return out.reshape(n, -1)


def put(name, i, nT, samples, Yi):
    SCORES.setdefault(name, [None] * nT)[i] = es_cells(samples, Yi)
    MEANS.setdefault(name, [None] * nT)[i] = samples.mean(1)


def save_scores():
    blob = {}
    for k, v in SCORES.items():
        if all(a is not None for a in v):
            blob[k] = np.stack(v).astype(np.float32)
    for k, v in MEANS.items():
        if all(a is not None for a in v):
            blob["mean|" + k] = np.stack(v).astype(np.float32)
    save_npz("scores.npz", **blob)
    jdump("train_info.json", TRAIN)


def fam_fit(fam, ds, d_theta, steps, seed, tag):
    """Fit one family on a list of data sets -> list of models."""
    if fam == "net":
        params, info = NN.train_nets(ds, steps=steps, seed=seed, log=log, tag=f"[{tag}]")
        TRAIN[tag] = info
        return params
    if fam == "ridge":
        return [NN.fit_ridge(d, seed=seed) for d in ds]
    if fam == "lin2":
        return [NN.fit_ridge(d, seed=seed, cols=NN.lin2_cols(d_theta)) for d in ds]
    return [NN.fit_law(d, d_theta=d_theta, seed=seed) for d in ds]


def fam_samples(fam, model, X, m, seed):
    if fam == "net":
        return NN.net_samples(model, X, m, seed)
    if fam in ("ridge", "lin2"):
        return NN.ridge_samples(model, X, m, seed)
    return NN.law_samples(model, X, m, seed)


FAMS = ("net", "ridge", "law", "lin2")


def stage_predict(truths, Ud, sim, labS, labU, exS, exU, exY, exYc, exCls, draws, pdraws, pm):
    nT, J = exS.shape[:2]
    CLASSES[:] = np.asarray(exCls).reshape(-1).tolist()          # program class per item (truth, run, anchor order)
    m = CFG["m"]
    nI = J * len(PROG)
    # item features per truth
    Xi, Xc, L2a, Yi = [], [], [], []
    for i in range(nT):
        X, _, la = NN.features(exS[i], exU[i], list(PROG))
        Xz, _, _ = NN.features(exS[i], exU[i], list(PROG), theta_u=np.zeros((J, D_TH)))
        Xi.append(X.reshape(nI, len(HS), -1))
        Xc.append(Xz.reshape(nI, len(HS), -1))
        L2a.append(la.reshape(nI, 2))
        Yi.append(exY[i].reshape(nI, CFG["R"], len(HS), 2).astype(float))
    # references
    SCORES["oracle"] = [oracle_cells(Yi[i]) for i in range(nT)]
    if exYc is not None:                                         # the simulator from the hidden state, program ignored
        for i in range(nT):
            put("O_noinput", i, nT, exYc[i].reshape(nI, -1, len(HS), 2).astype(float), Yi[i])
    ix = {n: k for k, n in enumerate(VX.S2_NAMES)}
    clim = []
    for i in range(nT):
        L2 = exS[i][..., [ix["N"], ix["s_b"]]].astype(float)                        # (J, T+1, 2)
        smp = np.zeros((nI, J - 1, len(HS), 2))
        for j in range(J):
            oth = [q for q in range(J) if q != j]
            for ai, a in enumerate(PROG):
                smp[j * len(PROG) + ai] = np.stack([L2[oth, a + h] for h in HS], 1)
        clim.append(es_cells(smp, Yi[i]))
        MEANS.setdefault("K", [None] * nT)[i] = smp.mean(1)
    SCORES["K"] = clim
    MEANS["anchor"] = [L2a[i][:, None, :].repeat(len(HS), 1) for i in range(nT)]
    # K0: the prior climatology (level 2 of m viable design episodes at the same tick): no history, no Lab, no theta
    okd = np.flatnonzero(sim["viable"])
    L2d = sim["S"][..., [ix["N"], ix["s_b"]]].astype(float)
    rk = np.random.default_rng(77)
    k0 = []
    for i in range(nT):
        smp = np.zeros((nI, m, len(HS), 2))
        for j in range(J):
            for ai, a in enumerate(PROG):
                pick = rk.choice(okd, size=m, replace=len(okd) < m)
                smp[j * len(PROG) + ai] = np.stack([L2d[pick, a + h] for h in HS], 1)
        k0.append(es_cells(smp, Yi[i]))
        MEANS.setdefault("K0", [None] * nT)[i] = smp.mean(1)
    SCORES["K0"] = k0
    save_npz("items.npz", L2a=np.stack(L2a), Y=np.stack(Yi).astype(np.float32))
    save_scores()

    def score_all(fam, name, models, Xlist, seed):
        for i in range(nT):
            mdl = models[i] if isinstance(models, list) and len(models) == nT else models[0]
            smp = fam_samples(fam, mdl, Xlist[i], m, seed + i)
            put(f"{fam}|{name}", i, nT, NN.to_level2(smp, L2a[i]), Yi[i])

    # ---- simulation-trained: P0 (unconditional) and the theta-conditional predictor, from the design episodes
    ok = sim["viable"]
    thu = np.repeat(Ud, CFG["K_d"], 0)
    ds_p0 = NN.dataset(sim["S"][ok], sim["U"][ok], seed=1)
    ds_c = NN.dataset(sim["S"][ok], sim["U"][ok], theta_u=thu[ok], seed=1)
    log(f"  design training set: {int(ok.sum())} episodes, {len(ds_p0['Xtr'])} examples, {ds_p0['Xtr'].shape[1]} inputs")
    rng = np.random.default_rng(901)
    for fam in FAMS:
        t0 = time.time()
        try:
            mp0 = fam_fit(fam, [ds_p0], 0, CFG["steps_sim"], 300, f"{fam}|P0")
            mc = fam_fit(fam, [ds_c], D_TH, CFG["steps_sim"], 301, f"{fam}|cond")
            score_all(fam, "P0", mp0, Xi, 400)
            score_all(fam, "C", mc, [NN.with_theta(Xc[i], to_u(truths[i])) for i in range(nT)], 410)
            score_all(fam, "PM", mc, [NN.with_theta(Xc[i], pm) for i in range(nT)], 420)
            score_all(fam, "PP", mc, [NN.with_theta(Xc[i], pdraws[rng.choice(len(pdraws), nI * m)].reshape(nI, m, D_TH))
                                      for i in range(nT)], 430)
            if draws is not None:
                for n in CFG["budgets"]:
                    for lev, nm in ((1, "S"), (2, "S2")):
                        Xs = []
                        for i in range(nT):
                            dd = draws[(lev, i, n)]
                            Xs.append(NN.with_theta(Xc[i], dd[rng.choice(len(dd), nI * m)].reshape(nI, m, D_TH)))
                        score_all(fam, f"{nm}@{n}", mc, Xs, 440 + n)
            log(f"  family {fam}: simulation-trained policies scored in {time.time() - t0:.0f}s")
        except Exception as exc:
            FAILED.append(f"{fam} sim")
            log(f"  family {fam} sim FAILED {exc!r}\n{traceback.format_exc()}")
        save_scores()
        report()
    # ---- data-only: D@n
    for n in CFG["budgets"]:
        if left_s() < 600 and not args.smoke:
            log(f"  SKIP D@{n}: {left_s():.0f}s left")
            FAILED.append(f"skipped D@{n}")
            continue
        ds = [NN.dataset(labS[i][:n], labU[i][:n], seed=100 + n + i) for i in range(nT)]
        for fam in FAMS:
            try:
                mdl = fam_fit(fam, ds, 0, CFG["steps_real"][n], 500 + n, f"{fam}|D@{n}")
                score_all(fam, f"D@{n}", mdl, Xi, 600 + n)
            except Exception as exc:
                FAILED.append(f"{fam} D@{n}")
                log(f"  {fam} D@{n} FAILED {exc!r}\n{traceback.format_exc()}")
        save_scores()
    report()
    return Xi, L2a, Yi


def stage_dedicated(name, thetas, Xi, L2a, Yi, seed):
    """Dedicated (unconditional) models per truth, trained on n_C simulations at thetas[i] (n_C, d): at the true
    theta ('Cded') or at posterior draws ('Sded@n')."""
    nT, nC = len(thetas), CFG["n_C"]
    if nC <= 0:
        return
    need = nT * nC * T_EP / (0.8 * INFO["rate"]) + 240
    if left_s() < need and not args.smoke:
        log(f"  SKIP {name}: needs {need:.0f}s, {left_s():.0f}s left")
        FAILED.append(f"skipped {name}")
        return
    sim = run_eps(np.concatenate(thetas), member_keys(make_key(5500, H, seed), nT * nC), seed, f"sims_{name}")
    S = sim["S"].reshape(nT, nC, T_EP + 1, -1)
    U = sim["U"].reshape(nT, nC, T_EP, -1)
    ds = [NN.dataset(S[i], U[i], seed=700 + i) for i in range(nT)]
    for fam in FAMS:
        mdl = fam_fit(fam, ds, 0, CFG["steps_C"], 710 + seed, f"{fam}|{name}")
        for i in range(nT):
            smp = fam_samples(fam, mdl[i], Xi[i], CFG["m"], 720 + i)
            put(f"{fam}|{name}", i, nT, NN.to_level2(smp, L2a[i]), Yi[i])
    save_scores()


def report(final=False):
    try:
        return _report(final)
    except Exception as exc:
        log(f"  report failed: {exc!r}\n{traceback.format_exc()}")
        if final:
            FAILED.append("final report")
        return None


def _report(final=False):
    names = [k for k, v in SCORES.items() if all(a is not None for a in v)]
    nT = len(SCORES["oracle"])
    S = {k: np.concatenate(SCORES[k]) for k in names}
    S["climatology"] = S["K"]
    prim = [i for i, (h, c) in enumerate(CELLS) if c == "joint"]
    cl = [f"h{HS[h]}|{c}" for h, c in CELLS]
    valid = np.zeros(len(CELLS), bool)
    valid[prim] = True
    groups = np.array(CLASSES) if len(CLASSES) == len(S["oracle"]) else None
    rep = skill_report(S, cells=cl, valid=valid, n_boot=1000, groups=groups)
    L = {k: float(S[k][:, prim].mean()) for k in names}
    per_truth_L = {k: [float(SCORES[k][i][:, prim].mean()) for i in range(nT)] for k in names}
    worlds = np.concatenate([np.full(len(SCORES["oracle"][i]), i) for i in range(nT)])

    # acceptance (roadmap section 1) with the shared implementation: one predictor family per row; bootstrap over
    # items and clustered by hidden world (truth). Variants: S2 = the posterior from level-2 histories only;
    # ded = dedicated models (C = Cded, S = Sded at its budget) instead of the theta-conditional one.
    def shares(fam, n, s_name=None, c_name=None):
        pol = {"K": "K", "D": f"{fam}|D@{n}", "P0": f"{fam}|P0", "S": s_name or f"{fam}|S@{n}", "C": c_name or f"{fam}|C"}
        if any(pol[q] not in S for q in ("K", "P0", "C")):
            return None
        out = ACC.shares({q: S[v] for q, v in pol.items() if v in S}, valid, worlds=worlds, n_boot=1000)
        out["policies"] = {q: v for q, v in pol.items() if v in S}
        out.pop("L", None)
        return out
    acc = {}
    for fam in FAMS:
        for n in CFG["budgets"]:
            for tag, kw in (("", {}), ("|S2", {"s_name": f"{fam}|S2@{n}"}),
                            ("|ded", {"s_name": f"{fam}|Sded@{n}", "c_name": f"{fam}|Cded"})):
                if tag == "|S2" and f"{fam}|S2@{n}" not in S:
                    continue
                if tag == "|ded" and f"{fam}|Cded" not in S:
                    continue
                r_ = shares(fam, n, **kw)
                if r_:
                    acc[f"{fam}@{n}{tag}"] = r_
    # the share of the oracle-predictable change reached (round-3 cchg), from predictive means: pooled over all
    # items (as round 3 pooled its two arms), and within each truth (change about that truth's own mean drift)
    items = np.load(os.path.join(OUT, "items.npz"))
    Yt = items["Y"].astype(float)                                                   # (nT, nI, R, nh, 2)
    La = items["L2a"].astype(float)                                                 # (nT, nI, 2)
    Y = np.concatenate(list(Yt))
    L2a = np.concatenate(list(La))
    chg = Y - L2a[:, None, None, :]
    Vc = ((chg - chg.mean((0, 1), keepdims=True)) ** 2).mean((0, 1))                 # (nh, 2)
    Vu = Y.var(1, ddof=1).mean(0)
    chg_t = Yt - La[:, :, None, None, :]
    Vc_t = ((chg_t - chg_t.mean((1, 2), keepdims=True)) ** 2).mean((1, 2))           # (nT, nh, 2)
    Vu_t = Yt.var(2, ddof=1).mean(1)                                                # (nT, nh, 2)
    cchg = {"V_change": Vc.tolist(), "Vu": Vu.tolist(), "oracle_predictable_share": (1 - Vu / Vc).tolist(),
            "coords": ["N", "s_b"], "hs": list(HS), "reached": {},
            "within_truth": {"V_change_mean": Vc_t.mean(0).tolist(), "Vu_mean": Vu_t.mean(0).tolist(),
                             "oracle_predictable_share": (1 - Vu_t.sum(0) / Vc_t.sum(0)).tolist(),
                             "oracle_predictable_share_per_truth": (1 - Vu_t / Vc_t).tolist(), "reached": {},
                             "note": "sums over truths of (V_change - Ve) / (V_change - Vu), each truth about its own mean change"}}
    for k, v in MEANS.items():
        if all(a is not None for a in v):
            mu_t = np.stack(v).astype(float)                                        # (nT, nI, nh, 2)
            mu = np.concatenate(list(mu_t))
            Ve = ((Y - mu[:, None]) ** 2).mean((0, 1))
            cchg["reached"][k] = ((Vc - Ve) / (Vc - Vu)).tolist()
            Ve_t = ((Yt - mu_t[:, :, None]) ** 2).mean((1, 2))
            cchg["within_truth"]["reached"][k] = ((Vc_t.sum(0) - Ve_t.sum(0)) / (Vc_t.sum(0) - Vu_t.sum(0))).tolist()
    agg = rep["aggregate"]
    out = {"final": final, "n_truths": nT, "n_items_pooled": int(S["oracle"].shape[0]), "cells": cl,
           "primary_cells": [cl[i] for i in prim], "L_pooled": L, "L_per_truth": per_truth_L,
           "oes": {k: agg[k] for k in names}, "oes_se_items": {k: rep["se"][k] for k in names},
           "oes_per_cell": {k: rep["oes"][k] for k in names}, "acceptance": acc, "cchg": cchg,
           "oes_by_program_class": rep.get("by_group"),
           "items_by_program_class": {g: int((groups == g).sum()) for g in sorted(set(CLASSES))} if groups is not None else None,
           "member_ticks": CLOCK, "hours": hours(), "failed": FAILED}
    gaps = {}
    for fam in FAMS:
        for a, b in ((f"{fam}|C", f"{fam}|PM"), (f"{fam}|C", f"{fam}|P0"), (f"{fam}|C", f"{fam}|PP"),
                     (f"{fam}|Cded", f"{fam}|C"), (f"{fam}|P0", f"{fam}|PP")):
            if a in agg and b in agg:
                gaps[f"{a} - {b}"] = paired_gap(rep, a, b)
        for n in CFG["budgets"]:
            for a, b in ((f"{fam}|S@{n}", f"{fam}|P0"), (f"{fam}|C", f"{fam}|S@{n}"), (f"{fam}|S@{n}", f"{fam}|D@{n}"),
                         (f"{fam}|P0", f"{fam}|D@{n}"), (f"{fam}|S@{n}", f"{fam}|S2@{n}")):
                if a in agg and b in agg:
                    gaps[f"{a} - {b}"] = paired_gap(rep, a, b)
    for a, b in (("net|P0", "ridge|P0"), ("net|C", "ridge|C"), ("net|C", "law|C"), ("net|P0", "law|P0"),
                 ("net|C", "lin2|C"), ("net|P0", "lin2|P0"), ("ridge|C", "lin2|C"), ("law|C", "lin2|C"),
                 ("net|Cded", "lin2|Cded"), ("K", "K0"), ("oracle", "O_noinput")):
        if a in agg and b in agg:
            gaps[f"{a} - {b}"] = paired_gap(rep, a, b)
    out["gaps_oes_item_bootstrap"] = gaps
    jdump("prediction.json", out)
    show = [k for k in sorted(agg) if k.split("|")[-1] in ("P0", "C", "PM", "Cded") or k.endswith(f"@{CFG['budgets'][-1]}")
            or "Sded" in k]
    log("  OES " + ", ".join(f"{k} {agg[k]:.3f}" for k in show))
    if final:
        for k, v in acc.items():
            log(f"  acceptance {k}: " + ", ".join(f"{q} {v[q]:.3f}" if isinstance(v[q], float) else f"{q} {v[q]}"
                                                   for q in ("sigma", "rho", "null_is") if v.get(q) is not None))
    return out


def main():
    stage_rate()
    truths, Ud, sim, pv, pdraws, pm, psd, labS, labU, exam = stage_episodes()
    CFG["n_truth"] = len(truths)
    try:
        draws = stage_identify(Ud, sim, labS, truths, pv, pm, psd)
    except Exception as exc:
        FAILED.append("identify")
        log(f"identify FAILED {exc!r}\n{traceback.format_exc()}")
        draws = None
    exS, exU, exY, exYc, exCls = stage_exam(truths, exam)
    Xi, L2a, Yi = stage_predict(truths, Ud, sim, labS, labU, exS, exU, exY, exYc, exCls, draws, pdraws, pm)
    nC = CFG["n_C"]
    try:
        stage_dedicated("Cded", [np.repeat(t[None], nC, 0) for t in truths], Xi, L2a, Yi, 51)
        report()
    except Exception as exc:
        FAILED.append("Cded")
        log(f"Cded FAILED {exc!r}\n{traceback.format_exc()}")
    try:
        nb = CFG["sded_budget"]
        if draws is not None and nb in CFG["budgets"] and nC > 0:
            rng = np.random.default_rng(601)
            ths = [from_u(draws[(1, i, nb)][rng.choice(len(draws[(1, i, nb)]), nC)]) for i in range(len(truths))]
            stage_dedicated(f"Sded@{nb}", ths, Xi, L2a, Yi, 52)
    except Exception as exc:
        FAILED.append("Sded")
        log(f"Sded FAILED {exc!r}\n{traceback.format_exc()}")
    report(final=True)
    audit_outputs()
    INFO["member_ticks"] = CLOCK
    INFO["member_ticks_total"] = int(sum(CLOCK.values()))
    INFO["hours"] = hours()
    INFO["failed"] = FAILED
    jdump("info.json", INFO)
    log(f"done: {INFO['member_ticks_total']} member-ticks, {hours():.2f} h, failed {FAILED}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        log(f"FATAL {exc!r}\n{traceback.format_exc()}")
        INFO["fatal"] = repr(exc)
        INFO["member_ticks"] = CLOCK
        jdump("info.json", INFO)
        sys.exit(1)
    if [f for f in FAILED if not f.startswith("skipped")]:
        sys.exit(2)
