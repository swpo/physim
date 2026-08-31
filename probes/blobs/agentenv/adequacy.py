"""adequacy.py — Track A A0 measurement adequacy study (W3). EVALUATOR-SIDE.

Design (locked for A0):
  EPISODE = 500 control steps x 5tu = 2500tu on (world, seed), replayed from a
  ONE-TIME cached sim (f16 frames @5tu + truth blob lists + f32 snapshot at
  T0=1700 with RNG state). Passive policies replay exactly (sensors do not
  disturb the field); only injection branches need live stepping and those are
  cached once per (world, seed) too (calib amps + announced + control; the
  control branch doubles as a snapshot-parity gate vs the main run).

  PHASES (steps): A 1-200 passive observation | B 201-245 motion probe |
  C 246-275 dilation size scan | D 276-320 closed-loop tracking |
  R 321-339 dead-reckon home (no reads) | E 340-500 contract window with
  P1 anchors at t=1700/1850/2000/2150, horizons 50/200tu; P2 windows 50tu
  over (1700,2500]; P3 announced injection (port->act0, amp 3, dur 10tu) at
  device 0's HOME anchor starting t=1700, response scored on device B over
  (1700,1950] (r1: B = self; r2: B = the second device).

  TIERS scale the sensor duty (fraction of steps read; all devices read
  together) and motion/injection budgets: x4 = full duty, x1 = 1/4, q4 = 1/16.
  Baseline '1x' in the spec = x1 here; x4/q4 bracket it by 4x each way.

  Reference-pipeline read allocator (scripted, same for every cell):
  E-phase anchor bursts are always funded first (contracts are the product),
  then motion probe (B) if >= its fixed cost, then size scan (C), then
  tracking duty (D), remainder to passive observation (A). Underfunded
  phases are SKIPPED and recorded — budget cliffs are findings, not bugs.

CLI (run from repo root with the blobkit venv python):
  python probes/blobs/agentenv/adequacy.py cache --world p4g2_044 --seed 928
  python probes/blobs/agentenv/adequacy.py evalgroup --world p4g2_044 --seed 928
  python probes/blobs/agentenv/adequacy.py aggregate
"""
import argparse
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import device as D
import refpipes as R
from device import CTRL_TU, MAX_STEP

CACHE = os.path.join(HERE, "cache")
RESULTS = os.path.join(HERE, "results")
FC = os.path.normpath(os.path.join(HERE, "..", "l0", "deepsearch",
                                   "v2_analysis", "film_candidates"))

WORLDS = dict(E1="p4g2_044", E2="p6g8_033", E3="p3g9_022")
BASE_SEEDS = dict(p4g2_044=928, p6g8_033=942, p3g9_022=921)
N_SEEDS = 3
T_EP = 2500.0
T0 = 1700.0
T_BRANCH = 250.0
CALIB_AMPS = (1.0, 2.0, 4.0)
ANN_AMP, ANN_DUR = 3.0, 10.0
P1_ANCHOR_STEPS = (340, 370, 400, 430)
P1_HORIZONS = (50.0, 200.0)
P2_WIN = 50.0
LOCK_RADIUS = 6.0

ROSTERS = dict(
    r1=[dict(lattice="hex", n_rings=3, base_ds=3.0)],
    r2=[dict(lattice="square", n_rings=3, base_ds=3.5),
        dict(lattice="hex", n_rings=3, base_ds=3.0)],
)

TIERS = dict(
    x4=dict(duty=1.0, motion=2400.0, injection=240.0, calib=(1.0, 2.0, 4.0)),
    x1=dict(duty=0.25, motion=600.0, injection=60.0, calib=(1.0, 2.0)),
    q4=dict(duty=0.0625, motion=150.0, injection=15.0, calib=(1.0,)),
)

# episode phases (control steps of 5tu). Order: A observe, B motion probe,
# D track (parks the device ON a blob), C dilation size scan (starts locked),
# R dead-reckon home, E contract window (device parked, anchors at P1 steps).
PH_A = (1, 201)
PH_B = (201, 243)
PH_D = (243, 315)
PH_C = (315, 323)
PH_R = (323, 340)
PH_E = (340, 501)
N_STEPS = 500

COST_B = 33          # dil probe (2cyc=10+3) + seek(<=5) + motion n_rep=1
COST_B_FULL = 42     # dil probe (3cyc) + seek + motion n_rep=2
COST_C = 12          # wait <=6 + scan <=6
COST_E = 16          # 4 anchors x 3 conditioning + 4 spot


def world_key(world, seed):
    return f"{world}|s{seed}|A0"


def load_genome(world):
    return json.load(open(os.path.join(FC, world + ".json")))["genome"]


def cache_paths(world, seed):
    base = os.path.join(CACHE, f"{world}_s{seed}")
    return base + ".npz", base + "_branches.npz"


# ===================================================================== cache
def branch_specs(tiers=TIERS):
    specs = [dict(name="control", amp=0.0)]
    for a in CALIB_AMPS:
        specs.append(dict(name=f"calib{a:g}", amp=a))
    specs.append(dict(name="announced", amp=ANN_AMP))
    return specs


def build_cache(world, seed, workers=3):
    t0w = time.time()
    os.makedirs(CACHE, exist_ok=True)
    g = load_genome(world)
    main_path, br_path = cache_paths(world, seed)
    if not os.path.exists(main_path):
        D.run_cached(g, seed, T_EP, main_path, L=128.0, workers=workers,
                     snap_times=(T0,))
        print(f"[cache] {world} s{seed}: main run done "
              f"({time.time() - t0w:.0f}s)", flush=True)
    if os.path.exists(br_path):
        print(f"[cache] {world} s{seed}: branches exist", flush=True)
        return
    c = D.CachedRun(main_path)
    nf = c.meta["na"] + c.meta["nc"]
    # device-0 secrets are identical for r1/r2 world keys (same key string);
    # injection anchor = dev0 home center; port = the one mapping to act0.
    sec = D.world_secrets(world_key(world, seed), nf, ROSTERS["r2"], 128.0)
    inj_yx = np.array(sec["devices"][0]["center"])
    port_perm = np.asarray(sec["port_perm"], int)
    inj_port = int(np.where(port_perm == 0)[0][0])
    steps_per = int(round(CTRL_TU / 0.02))
    n_fr = int(round(T_BRANCH / CTRL_TU))
    out = {}
    for spec in branch_specs():
        S = c.snapshot_state(g, T0, workers=workers)
        N = S["N"]
        frames = np.empty((n_fr + 1, nf, N, N), np.float16)
        frames[0] = np.asarray(S["F"], np.float32).astype(np.float16)
        for i in range(1, n_fr + 1):
            t_rel = (i - 1) * CTRL_TU
            injs = []
            if spec["amp"] > 0 and t_rel < ANN_DUR:
                injs = [dict(field=0, y=inj_yx[0], x=inj_yx[1],
                             amp=spec["amp"])]
            D.step_chunk(S, steps_per, injections=injs)
            frames[i] = np.asarray(S["F"], np.float32).astype(np.float16)
        out[spec["name"]] = frames
        print(f"[cache] {world} s{seed}: branch {spec['name']} "
              f"({time.time() - t0w:.0f}s)", flush=True)
    np.savez(br_path,
             meta=json.dumps(dict(world=world, seed=seed, t0=T0,
                                  t_branch=T_BRANCH, inj_port=inj_port,
                                  inj_yx=inj_yx.tolist(), ann_amp=ANN_AMP,
                                  ann_dur=ANN_DUR, ctrl_tu=CTRL_TU)),
             **out)
    print(f"[cache] {world} s{seed}: ALL DONE {time.time() - t0w:.0f}s",
          flush=True)


# ============================================================ read allocation
def read_plan(duty):
    """Per-phase read-step sets for the scripted pipeline at this duty."""
    total = int(round(duty * N_STEPS))
    plan = dict(total=total)
    reads_E_want = COST_E if duty < 1.0 else (PH_E[1] - PH_E[0])
    reads_E = min(reads_E_want, total)
    rem = total - reads_E
    if duty >= 1.0:
        b_cost = COST_B_FULL
        do_B, do_C = True, True
        d_reads = PH_D[1] - PH_D[0]
        a_reads = PH_A[1] - PH_A[0]
    else:
        do_B = rem >= COST_B + 10          # keep >=10 for A or B is pointless
        b_cost = COST_B if do_B else 0
        rem2 = rem - b_cost
        do_C = do_B and rem2 >= COST_C + 8
        rem3 = rem2 - (COST_C if do_C else 0)
        d_reads = int(0.30 * rem3) if do_B else 0
        a_reads = rem3 - d_reads
    e_steps = set()
    for a in P1_ANCHOR_STEPS:
        e_steps |= {a - 2, a - 1, a}
    spot = [PH_E[0] + 25, PH_E[0] + 75, PH_E[0] + 115, PH_E[1] - 2]
    for s in spot:
        if len(e_steps) >= reads_E:
            break
        e_steps.add(s)
    if duty >= 1.0:
        e_steps = set(range(PH_E[0], PH_E[1]))
    plan.update(
        A=R.burst_schedule(PH_A[0], PH_A[1], a_reads,
                           burst=10 if a_reads >= 30 else 6),
        do_B=do_B, do_C=do_C, b_nrep=2 if duty >= 1.0 else 1,
        C_wait=(4 if duty >= 1.0 else 3),
        D_duty=(1.0 if duty >= 1.0 else
                (min(d_reads / (PH_D[1] - PH_D[0]), 1.0) if do_B else 0.0)),
        E=e_steps)
    return plan


# ================================================================== truth ops
def truth_blob_track(blobs, t_idx0, start_yx, act_sel, L=128.0):
    """Follow the truth blob nearest start_yx at frame t_idx0 through frames
    via NN linkage. Returns dict frame_idx -> (y, x) while trackable."""
    def nearest(frame_i, ref, acts):
        best, bd = None, 1e9
        for a in acts:
            for b in blobs[frame_i][a]:
                d = np.hypot(*((np.array(b[:2]) - ref + L / 2) % L - L / 2))
                if d < bd:
                    bd, best = d, np.array(b[:2])
        return best, bd
    pos, d0 = nearest(t_idx0, np.asarray(start_yx, float), act_sel)
    if pos is None:
        return {}
    out = {t_idx0: pos.copy()}
    cur = pos
    for i in range(t_idx0 + 1, len(blobs)):
        nxt, d = nearest(i, cur, act_sel)
        if nxt is None or d > 6.0:      # linkage break (speed<1.2u/tu ok)
            break
        cur = nxt
        out[i] = cur.copy()
    return out


def sample_truth(cached, i_ctrl, dev, port_perm):
    """Full-precision-path truth streams at frame i for a device (stream
    order), from the same f16 cache the pipeline reads (consistent)."""
    fields = cached.fields_at(i_ctrl)[port_perm]
    return dev.sample(fields, cached.meta["dx"])


# ================================================================= cell eval
def run_cell(world, seed, roster_name, tier_name, verbose=True,
             cached=None, brz=None):
    t0w = time.time()
    g = load_genome(world)
    main_path, br_path = cache_paths(world, seed)
    cached = cached or D.CachedRun(main_path)
    brz = brz if brz is not None else np.load(br_path, allow_pickle=False)
    br_meta = json.loads(str(brz["meta"]))
    cfgs = ROSTERS[roster_name]
    tier = TIERS[tier_name]
    wk = world_key(world, seed)
    k_total = sum(len(D.lattice_offsets(c["lattice"], c["n_rings"]))
                  for c in cfgs)
    sensor_budget = tier["duty"] * N_STEPS * k_total * CTRL_TU
    # branches add read opportunity: budget covers them at same duty
    n_br_frames = int(round(T_BRANCH / CTRL_TU))
    n_branches = len(tier["calib"]) + 1          # calib + announced window
    sensor_budget *= (1.0 + tier["duty"] * 0.0)  # branch reads charged below
    budgets = dict(sensor=sensor_budget, motion=tier["motion"],
                   injection=tier["injection"])
    env = D.ReplayEnv(cached, g, cfgs, budgets, wk)
    env._move_ledger = []          # agent-side accepted-move log (dev0)
    nf = env.nf
    dev0 = 0
    devB = 1 if roster_name == "r2" else 0
    plan = read_plan(tier["duty"])
    hist = R.History()
    res = dict(world=world, seed=seed, roster=roster_name, tier=tier_name,
               plan={k: (len(v) if isinstance(v, set) else v)
                     for k, v in plan.items()})

    # ---------------- phase A: passive observation
    step = 0
    while step < PH_A[1] - 1:
        step += 1
        obs = env.step({}, read=(step in plan["A"]))
        if step in plan["A"]:
            hist.add(obs)
    r1 = R.r1_geometry(env, hist, dev0)
    r2 = R.r2_particulate(hist, r1 if r1.get("ok") else dict(ok=True,
                          center=0), dev0) if len(hist.t) >= 12 else None
    # R1 also on second device (from same reads)
    r1b = R.r1_geometry(env, hist, devB) if roster_name == "r2" else None

    # ---------------- phase B: dilation radial probe + motion probe
    dil, snap = None, None
    if plan["do_B"] and r1.get("ok"):
        dil = R.r1_dilation_probe(env, r1, dev0, n_cyc=2)
        if dil.get("ok"):
            snap = R.r1_template_snap(r1, dil, env.devices[dev0].k)
            if snap is not None:
                r1 = snap                     # refined geometry
    r1_ctl = r1
    B_emb, bq, bspend = None, 0.0, dict(reads=0, motion=0.0)
    if plan["do_B"] and r1_ctl.get("ok"):
        B_emb, bq, bspend = R.r1_motion_probe(
            env, r1_ctl, dev0, n_rep=plan["b_nrep"], hist=hist,
            max_env_steps=PH_B[1] - 1 - env.i)
        if B_emb is None and PH_B[1] - 1 - env.i >= 24:
            B_emb, bq, bs2 = R.r1_motion_probe(     # retry: more, smaller
                env, r1_ctl, dev0, n_rep=2, dm=0.9, hist=hist,
                max_env_steps=PH_B[1] - 1 - env.i)
            for kk in bspend:
                bspend[kk] += bs2.get(kk, 0)
        if B_emb is not None:
            Bn = B_emb / np.maximum(np.linalg.norm(B_emb, axis=0,
                                                   keepdims=True), 1e-12)
            if np.linalg.cond(Bn) > 4.0:
                B_emb = None                  # degenerate basis: unusable
    # burn remaining phase-B steps
    while env.i < PH_B[1] - 1:
        env.step({}, read=False)

    # ---------------- phase D: tracking (before C: scan starts on-target)
    track_log = dict(t=[], err=[], locked_read=[], spend_reads=0,
                     spend_motion=0.0)
    track_start_i = env.i + 1
    n_track = PH_D[1] - 1 - env.i
    if B_emb is not None and r2 is not None and plan["D_duty"] > 0 \
            and n_track > 0:
        track_log = R.r3_track(env, r1_ctl, r2, B_emb, dev0,
                               n_steps=n_track, duty=plan["D_duty"],
                               hist=hist)
    while env.i < PH_D[1] - 1:
        env.step({}, read=False)

    # ---------------- phase C: size scan (device parked where D left it)
    scan = dict(ok=False, why="skipped")
    if plan["do_C"] and r1_ctl.get("ok") and r2 is not None:
        scan = R.r2_size_scan(env, r1_ctl, r2, dev0, max_wait=plan["C_wait"])
    while env.i < PH_C[1] - 1:
        env.step({}, read=False)

    # ---------------- phase R: dead-reckon home (agent-side action ledger)
    # The agent knows only its own ACCEPTED move commands (env._move_ledger,
    # written by the pipelines). Net command sum in control units is exactly
    # invertible because motion is a fixed linear basis — no secrets used.
    dev = env.devices[dev0]
    home = np.array(env.dev_center_log[0][dev0])
    a_net = (np.sum(env._move_ledger, axis=0) if env._move_ledger
             else np.zeros(2))
    while env.i < PH_E[0] - 1:
        stepv = np.clip(-a_net, -MAX_STEP, MAX_STEP)
        act = {}
        if np.abs(stepv).sum() > 1e-9:
            act = {dev0: dict(move=tuple(stepv))}
        step = env.i + 1
        obs = env.step(act, read=(step in plan["E"]))
        if step in plan["E"]:
            hist.add(obs)
        if act and not obs["rejected"]:
            a_net += stepv
    home_err = float(np.hypot(*((dev.center - home + env.L / 2) % env.L
                                - env.L / 2)))

    # ---------------- phase E: contract window
    anchor_hist_idx = {}
    while env.i < N_STEPS:
        step = env.i + 1
        obs = env.step({}, read=(step in plan["E"]))
        if step in plan["E"]:
            hist.add(obs)
        if step in P1_ANCHOR_STEPS:
            anchor_hist_idx[step] = len(hist.t)

    # ======== scoring (evaluator side, full-rate truth from cache) =========
    port_perm = env.port_perm
    truth = env.truth()
    na, nc = cached.meta["na"], cached.meta["nc"]

    # ---- R1 truth comparison
    res["r1"] = score_r1(r1, env.devices[dev0], plan, bq, B_emb,
                         bspend, r1_dev=dev0)
    if r1b is not None:
        res["r1_devB"] = score_r1(r1b, env.devices[devB], plan, 0.0, None,
                                  None, r1_dev=devB)

    # ---- R2
    res["r2"] = score_r2(r2, scan, cached, env, dev0, port_perm, na)

    # ---- R3 tracking
    res["r3"] = score_r3(track_log, env, dev0, cached, track_start_i, na,
                         port_perm, r2)
    res["home_err"] = home_err

    # ---- P1
    res["p1"] = score_p1(hist, env, dev0, cached, anchor_hist_idx, r1_ctl,
                         track_log, port_perm)

    # ---- P2
    res["p2"] = score_p2(hist, env, dev0, cached, port_perm)

    # ---- P3
    res["p3"] = score_p3(env, cached, brz, br_meta, g, cfgs, wk, tier,
                         devB, hist, r1 if roster_name == "r1" else
                         (r1b or r1))

    res["spend"] = {k: round(v, 1) for k, v in env.spent.items()}
    res["budget"] = {k: round(v, 1) for k, v in budgets.items()}
    res["wall_s"] = round(time.time() - t0w, 1)
    if verbose:
        print(f"[cell] {world} s{seed} {roster_name} {tier_name}: "
              f"done in {res['wall_s']}s", flush=True)
    return res


# ------------------------------------------------------------- score helpers
def procrustes_corr(P, X):
    Pc = P - P.mean(0)
    Xc = X - X.mean(0)
    U, S, Vt = np.linalg.svd(Pc.T @ Xc)
    Rt = U @ Vt
    s = S.sum() / max((Pc ** 2).sum(), 1e-12)
    fit = s * Pc @ Rt
    num = (fit * Xc).sum()
    den = np.sqrt((fit ** 2).sum() * (Xc ** 2).sum())
    return float(num / max(den, 1e-12)), s, Rt


def score_r1(r1, dev, plan, bq, B_emb, bspend, r1_dev=0):
    out = dict(ok=bool(r1.get("ok")), n_reads_A=len(plan["A"]))
    if not r1.get("ok"):
        out["why"] = r1.get("why")
        return out
    P = dev.offs[dev.node_perm] * dev.base_ds
    adj_true = D.true_adjacency(dev.lattice, dev.offs)[
        np.ix_(dev.node_perm, dev.node_perm)]
    A = r1["adj"]
    tp = int((A & adj_true).sum())
    f1 = 2 * tp / max(int(A.sum()) + int(adj_true.sum()), 1)
    corr, s, Rt = procrustes_corr(P, r1["X"])
    out.update(lattice_est=r1["lattice"], lattice_true=dev.lattice,
               lattice_correct=bool(r1["lattice"] == dev.lattice),
               adj_f1=round(float(f1), 4),
               embed_corr=round(corr, 4),
               snapped=bool("assign" in r1),
               snap_cost=(round(r1["snap_cost"], 3)
                          if "snap_cost" in r1 else None),
               center_correct=bool(r1["center"]
                                   == list(dev.node_perm).index(0)))
    if B_emb is not None:
        B_true = s * Rt.T @ dev.Rm.T @ dev.Bm
        angs, scls = [], []
        for c in range(2):
            v1, v2 = B_emb[:, c], B_true[:, c]
            ca = v1 @ v2 / max(np.linalg.norm(v1) * np.linalg.norm(v2), 1e-12)
            angs.append(float(np.degrees(np.arccos(np.clip(ca, -1, 1)))))
            scls.append(float(np.linalg.norm(v1) / np.linalg.norm(v2)))
        out.update(motion_ok=True, motion_angle_err=[round(a, 1)
                   for a in angs], motion_scale_ratio=[round(x, 2)
                   for x in scls], motion_qual=round(bq, 3),
                   motion_spend=bspend)
    else:
        out.update(motion_ok=False)
    return out


def score_r2(r2, scan, cached, env, dev0, port_perm, na):
    if r2 is None:
        return dict(ok=False, why="insufficient reads")
    out = dict(ok=True, particulate=bool(r2["particulate"]),
               bim_max=round(float(r2["bim"].max()), 3),
               fano=round(float(r2["fano"]), 2),
               p_event=int(r2["p_event"]),
               p_event_field=int(port_perm[r2["p_event"]]),
               center_passes=int(r2["center_passes"]))
    out["scan_ok"] = bool(scan.get("ok"))
    if scan.get("ok"):
        dev = env.devices[dev0]
        r_est = scan["r_est_ds"] * dev.base_ds
        # truth radius: median blob radius of matched act (or all acts) over
        # phase C frames
        fi = int(port_perm[scan.get("port", r2["p_event"])])
        acts = [fi] if fi < na else list(range(na))
        rads = []
        for i in range(PH_C[0], PH_C[1]):
            for a in acts:
                for b in cached.blobs[i][a]:
                    rads.append(np.sqrt(b[2] / np.pi))
        r_true = float(np.median(rads)) if rads else np.nan
        out.update(r_est=round(float(r_est), 2),
                   r_true=round(r_true, 2),
                   r_ratio=(round(float(r_est / r_true), 2)
                            if np.isfinite(r_true) and r_true > 0 else None),
                   scan_spend=scan["spend"])
    else:
        out["scan_why"] = scan.get("why")
    return out


def score_r3(track_log, env, dev0, cached, i_start, na, port_perm, r2):
    if not track_log["t"]:
        return dict(ok=False, why="tracking skipped")
    L = env.L
    p_trk = track_log.get("port", r2["p_event"] if r2 else 0)
    fi = int(port_perm[p_trk])
    acts = [fi] if fi < na else list(range(na))
    # device centers during tracking, from truth log
    n = len(track_log["t"])
    centers = np.array([env.dev_center_log[i][dev0]
                        for i in range(i_start, i_start + n)])
    # nearest-blob distance per step + adaptive lock radius (blob scale)
    dists, radii = [], []
    for j, i_ctrl in enumerate(range(i_start, i_start + n)):
        best, br = np.inf, np.nan
        for a in acts:
            for b in cached.blobs[i_ctrl][a]:
                d = np.hypot(*((np.array(b[:2]) - centers[j] + L / 2) % L
                               - L / 2))
                if d < best:
                    best, br = d, np.sqrt(b[2] / np.pi)
        dists.append(best)
        radii.append(br)
    dists = np.array(dists)
    r_med = float(np.nanmedian(radii)) if len(radii) else LOCK_RADIUS
    lock_r = max(LOCK_RADIUS, r_med)
    # same-blob retention: anchor at FIRST close approach, follow that blob
    ret = []
    trace = {}
    j0 = next((j for j, d in enumerate(dists) if d <= lock_r), None)
    if j0 is not None:
        trace = truth_blob_track(cached.blobs, i_start + j0, centers[j0],
                                 acts, L)
        for j in range(j0, n):
            i_ctrl = i_start + j
            if i_ctrl in trace:
                d = np.hypot(*((trace[i_ctrl] - centers[j] + L / 2) % L
                               - L / 2))
                ret.append(d <= lock_r)
    n_trk = sum(1 for s_ in track_log.get("state", []) if s_ == "track")
    hold = dists[j0:] if j0 is not None else np.array([])
    return dict(ok=True, lock_radius=round(lock_r, 1),
                acquired=bool(j0 is not None),
                t_first_lock=(round(j0 * CTRL_TU, 1)
                              if j0 is not None else None),
                pct_locked_nearest=round(float((dists <= lock_r).mean())
                                         * 100, 1),
                pct_hold=round(float((hold <= lock_r).mean()) * 100, 1)
                if len(hold) else None,
                pct_locked_same=round(float(np.mean(ret)) * 100, 1)
                if ret else None,
                trace_len=len(trace),
                mean_dist=round(float(dists.mean()), 2),
                port=int(p_trk), field=fi,
                pct_in_track_state=round(100.0 * n_trk /
                                         max(len(track_log["t"]), 1), 1),
                spend_reads=track_log["spend_reads"],
                spend_motion=round(track_log["spend_motion"], 1))


def score_p1(hist, env, dev0, cached, anchor_hist_idx, r1, track_log,
             port_perm):
    """CRPS per variant x horizon, averaged over anchors and channels."""
    out = {f"H{int(H)}": {} for H in P1_HORIZONS}
    dev = env.devices[dev0]
    nf = env.nf
    if len(hist.t) < 3:
        return dict(ok=False, why="no reads")
    crps_acc = {(v, H): [] for v in ("persistence", "ar2", "informed",
                                     "climatology") for H in P1_HORIZONS}
    for a_step in P1_ANCHOR_STEPS:
        if a_step not in anchor_hist_idx:
            continue
        n_h = anchor_hist_idx[a_step]
        sub = R.History()
        sub.t = hist.t[:n_h]
        sub.streams = hist.streams[:n_h]
        sub.glob = hist.glob[:n_h]
        if len(sub.t) < 3:
            continue
        pers = R.p1_persistence(sub, dev0, P1_HORIZONS)
        ar2 = R.p1_ar2(sub, dev0, P1_HORIZONS)
        inf = R.p1_informed(sub, dev0, P1_HORIZONS, r1, track_log)
        M = sub.mat(dev0).reshape(len(sub.t), -1)
        clim_mu, clim_sig = M.mean(0), M.std(0) + 1e-3
        for H in P1_HORIZONS:
            i_tgt = a_step + int(round(H / CTRL_TU))
            if i_tgt > N_STEPS:
                continue
            y = sample_truth(cached, i_tgt, dev, port_perm).reshape(-1)
            crps_acc[("persistence", H)].append(
                R.gauss_crps(*pers[H], y).mean())
            crps_acc[("ar2", H)].append(R.gauss_crps(*ar2[H], y).mean())
            crps_acc[("informed", H)].append(R.gauss_crps(*inf[H], y).mean())
            crps_acc[("climatology", H)].append(
                R.gauss_crps(clim_mu, clim_sig, y).mean())
    for H in P1_HORIZONS:
        for v in ("persistence", "ar2", "informed", "climatology"):
            vals = crps_acc[(v, H)]
            out[f"H{int(H)}"][v] = (round(float(np.mean(vals)), 5)
                                    if vals else None)
    out["ok"] = True
    return out


def score_p2(hist, env, dev0, cached, port_perm):
    """Event-rate forecast over (T0, 2500] in 50tu windows. The harness
    announces (port, thr) picked from FULL-rate pre-T0 truth."""
    dev = env.devices[dev0]
    nf = env.nf
    i0 = int(round(T0 / CTRL_TU))
    # harness-side port/threshold: most bimodal port on full pre-T0 streams
    # at the device's HOME position (parked from T0 on)
    full = np.stack([sample_truth(cached, i, dev, port_perm)
                     for i in range(1, i0)])          # (T, nf, k)
    # harness announces (port, thr, direction): the sparse-excursion port
    # with the HIGHEST pre-T0 crossing rate (a contract on a quantity that
    # is identically zero is trivial — E1/E2 home-anchor lesson)
    best, p_ev, sign, thr = -1e9, 0, 1.0, 0.0
    for p in range(nf):
        A_ = full[:, p, :]
        if A_.std() < 1e-9:
            continue
        z = (A_ - A_.mean()) / A_.std()
        sg = 1.0 if float(np.mean(z ** 3)) >= 0 else -1.0
        As = A_ * sg
        lo, hi = np.percentile(As, [5, 99])
        th = 0.5 * (lo + hi)
        of = float((As > th).mean())
        if of <= 1e-4 or of > 0.55:
            continue
        x_ = As > th
        rate = float((~x_[:-1] & x_[1:]).sum()) / max(len(As) - 1, 1)
        sc = rate + 0.01 * R.bimodality_coeff(A_)
        if sc > best:
            best, p_ev, sign, thr = sc, p, sg, th
    A = full[:, p_ev, :] * sign
    # truth rates in the contract window
    fut = np.stack([sample_truth(cached, i, dev, port_perm)
                    for i in range(i0, N_STEPS + 1)])
    xf = fut[:, p_ev, :] * sign > thr
    up = (~xf[:-1] & xf[1:]).sum(1)
    fpw = int(round(P2_WIN / CTRL_TU))
    n_win = len(up) // fpw
    true_rates = np.array([up[j * fpw:(j + 1) * fpw].sum()
                           for j in range(n_win)], float)
    # forecast issued AT T0: only pre-T0 reads are usable
    pre = R.History()
    for tt, ss, gg_ in zip(hist.t, hist.streams, hist.glob):
        if tt <= T0 + 1e-9:
            pre.t.append(tt)
            pre.streams.append(ss)
            pre.glob.append(gg_)
    if len(pre.t) < 4:
        return dict(ok=False, why="no pre-T0 reads")
    preds = R.p2_forecast(pre, dev0, p_ev, thr, P2_WIN, n_win,
                          duty=1.0, sign=sign)
    out = dict(ok=True, p_event=p_ev, sign=sign, thr=round(float(thr), 4),
               degenerate=bool(np.abs(true_rates).max() < 0.5),
               true_rates=true_rates.tolist())
    for v, pr in preds.items():
        mae = float(np.abs(np.asarray(pr) - true_rates).mean())
        out[f"mae_{v}"] = round(mae, 3)
    out["mae_zero"] = round(float(np.abs(true_rates).mean()), 3)
    return out


def score_p3(env, cached, brz, br_meta, g, cfgs, wk, tier, devB, hist, r1B):
    """Announced injection at dev0 home anchor; response scored on dev B
    (parked at its home) over the branch window, full-rate truth."""
    dx = cached.meta["dx"]
    nf = env.nf
    port_perm = env.port_perm
    n_fr = int(round(T_BRANCH / CTRL_TU)) + 1
    # a PARKED copy of device B (its home pose; dilation 1)
    sec = D.world_secrets(wk, nf, cfgs, env.L)
    ds = sec["devices"][devB]
    cfg = cfgs[devB]
    devBp = D.ProbeDevice(devB, cfg["lattice"], cfg["n_rings"],
                          cfg["base_ds"], ds["center"], env.L,
                          ds["secret_rot"], ds["reflect"],
                          ds["motion_theta"], ds["motion_reflect"],
                          ds["node_perm"])
    def branch_streams(name):
        fr = brz[name]
        out = np.empty((n_fr, nf, devBp.k), np.float32)
        for i in range(n_fr):
            out[i] = devBp.sample(fr[i].astype(np.float32)[port_perm], dx)
        return out
    truth_ann = branch_streams("announced")
    ctrl = branch_streams("control")
    # detectability of the true response
    resp_true = truth_ann - ctrl
    noise = np.stack([sample_truth(cached, i, devBp, port_perm)
                      for i in range(int(round(T0 / CTRL_TU)) - 40,
                                     int(round(T0 / CTRL_TU)))])
    nfloor = np.median(np.abs(np.diff(noise, axis=0))) + 1e-9
    z_resp = float(np.abs(resp_true).max() / nfloor)
    # ---- pipeline predictions (duty-limited reads)
    duty = tier["duty"]
    every = max(int(round(1.0 / max(duty, 1e-6))), 1)
    read_idx = list(range(0, n_fr, every))
    # baseline persistence: last pre-T0 read at B
    base = None
    for s_ in reversed(hist.streams):
        if devB in s_ and np.isfinite(s_[devB]).all():
            base = np.asarray(s_[devB], float)
            break
    if base is None:
        base = ctrl[0]
    y = truth_ann.reshape(n_fr, -1)
    scores = {}
    sig0 = np.abs(np.diff(noise, axis=0)).std(axis=0).reshape(-1) + 1e-3
    mu_p = np.tile(base.reshape(1, -1), (n_fr, 1))
    scores["persistence"] = float(np.mean(
        [R.gauss_crps(mu_p[i], sig0, y[i]).mean() for i in range(n_fr)]))
    # AR2 on pre-T0 device-B history
    Mb = np.stack([s_[devB] for s_ in hist.streams
                   if devB in s_ and np.isfinite(s_[devB]).all()])
    if len(Mb) >= 10:
        S = Mb.reshape(len(Mb), -1)
        mu_a = []
        for i in range(n_fr):
            mu_a.append(R._ar2_forecast(S, i + 1))
        mu_a = np.stack(mu_a)
    else:
        mu_a = mu_p
    scores["ar2"] = float(np.mean(
        [R.gauss_crps(mu_a[i], sig0, y[i]).mean() for i in range(n_fr)]))
    # informed: control reads + calib template scaling
    calib_resps = []
    inj_spend = 0.0
    for a in tier["calib"]:
        cost = a * ANN_DUR
        if inj_spend + cost > tier["injection"] + 1e-9:
            continue
        inj_spend += cost
        fr = branch_streams(f"calib{a:g}")
        resp = np.full_like(fr, np.nan)
        resp[read_idx] = fr[read_idx] - ctrl[read_idx]
        calib_resps.append(dict(amp=a, dur=ANN_DUR, resp=resp))
    tmpl = R.p3_template_predict(calib_resps, dict(amp=ANN_AMP, dur=ANN_DUR),
                                 n_fr, devBp.k, nf)
    if tmpl is not None:
        ctrl_est = np.full_like(ctrl, np.nan)
        ctrl_est[read_idx] = ctrl[read_idx]
        idx = np.asarray(read_idx)
        for i in range(n_fr):
            if i not in read_idx:
                j = idx[np.abs(idx - i).argmin()]
                ctrl_est[i] = ctrl_est[j]
        mu_i = (ctrl_est + tmpl).reshape(n_fr, -1)
        # sigma: calib-residual scale + noise floor
        sig_i = sig0
        scores["informed"] = float(np.mean(
            [R.gauss_crps(mu_i[i], sig_i, y[i]).mean()
             for i in range(n_fr)]))
    else:
        scores["informed"] = None
    # P3 runs on branched replicas: report its costs separately (the branch
    # reads are extra episode segments, not part of the main sensor ledger)
    n_read_frames = len(read_idx) * (len(calib_resps) + 1)
    return dict(ok=True, z_response=round(z_resp, 2),
                resp_max=round(float(np.abs(resp_true).max()), 4),
                noise_floor=round(float(nfloor), 5),
                n_calib=len(calib_resps),
                sensor_cost=round(n_read_frames * devBp.k * CTRL_TU, 1),
                injection_cost=round(inj_spend, 1),
                crps={k: (round(v, 5) if v is not None else None)
                      for k, v in scores.items()})


# ================================================================ aggregate
def _collect_rows():
    rows = []
    for fn in sorted(os.listdir(RESULTS)):
        if fn.endswith(".json") and fn != "aggregate.json":
            rows.append(json.load(open(os.path.join(RESULTS, fn))))
    return rows


def _crps_skill(cell, H, variant):
    """Skill vs climatology: 1 - CRPS_v/CRPS_clim (higher better, 0 = no
    better than climatology)."""
    p1 = cell.get("p1", {})
    hh = p1.get(f"H{int(H)}", {})
    v = hh.get(variant)
    c = hh.get("climatology")
    if v is None or c is None or c <= 0:
        return None
    return 1.0 - v / c


def aggregate(make_plots=True):
    rows = _collect_rows()
    if not rows:
        print("no results yet")
        return
    E_of = {v: k for k, v in WORLDS.items()}
    # ---------------- verdict table rows
    table = {}
    for r in rows:
        key = (E_of[r["world"]], r["roster"], r["tier"])
        table.setdefault(key, []).append(r)
    agg = {}
    for key, cells in sorted(table.items()):
        def m(path, default=None):
            vals = []
            for c in cells:
                v = c
                try:
                    for p in path:
                        v = v[p]
                except (KeyError, TypeError):
                    v = None
                if v is not None and not (isinstance(v, float)
                                          and not np.isfinite(v)):
                    vals.append(v)
            if not vals:
                return default
            if isinstance(vals[0], bool):
                return float(np.mean([bool(x) for x in vals]))
            try:
                return float(np.mean([float(x) for x in vals]))
            except (TypeError, ValueError):
                return vals[0]
        skills = {}
        for H in P1_HORIZONS:
            for v in ("persistence", "ar2", "informed"):
                sk = [
                    s for s in (_crps_skill(c, H, v) for c in cells)
                    if s is not None]
                skills[f"p1_H{int(H)}_{v}"] = (round(float(np.mean(sk)), 4)
                                               if sk else None)
        p2m = {}
        for v in ("persistence", "mean", "informed", "zero"):
            p2m[f"p2_mae_{v}"] = m(["p2", f"mae_{v}"])
        agg["|".join(key)] = dict(
            n_seeds=len(cells),
            r1_lattice_acc=m(["r1", "lattice_correct"]),
            r1_adj_f1=m(["r1", "adj_f1"]),
            r1_embed_corr=m(["r1", "embed_corr"]),
            r1_motion_ok=m(["r1", "motion_ok"]),
            r1_motion_qual=m(["r1", "motion_qual"]),
            r1_motion_angerr=m(["r1", "motion_angle_err", 0]),
            r2_particulate=m(["r2", "particulate"]),
            r2_scan_ok=m(["r2", "scan_ok"]),
            r2_r_ratio=m(["r2", "r_ratio"]),
            r3_acquired=m(["r3", "acquired"]),
            r3_pct_locked=m(["r3", "pct_locked_nearest"]),
            r3_pct_hold=m(["r3", "pct_hold"]),
            r3_pct_same=m(["r3", "pct_locked_same"]),
            r3_mean_dist=m(["r3", "mean_dist"]),
            home_err=m(["home_err"]),
            p3_z=m(["p3", "z_response"]),
            p3_crps_pers=m(["p3", "crps", "persistence"]),
            p3_crps_ar2=m(["p3", "crps", "ar2"]),
            p3_crps_inf=m(["p3", "crps", "informed"]),
            **skills, **p2m)
    outp = os.path.join(RESULTS, "aggregate.json")
    with open(outp, "w") as f:
        json.dump(agg, f, indent=1)
    print(f"[aggregate] {len(rows)} cells -> {outp}")
    if make_plots:
        make_adequacy_plots(agg)
    return agg


TIER_X = dict(q4=0.25, x1=1.0, x4=4.0)


def make_adequacy_plots(agg):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    figdir = os.path.join(HERE, "figs")
    os.makedirs(figdir, exist_ok=True)
    worlds = ["E1", "E2", "E3"]
    rosters = ["r1", "r2"]
    tiers = ["q4", "x1", "x4"]

    panels = [
        ("R1 lattice acc", "r1_lattice_acc", (0, 1.05)),
        ("R1 adj F1", "r1_adj_f1", (0, 1.05)),
        ("R3 % hold after lock", "r3_pct_hold", (0, 105)),
        ("P1 skill H50 (informed)", "p1_H50_informed", None),
        ("P1 skill H200 (informed)", "p1_H200_informed", None),
        ("P2 MAE informed/zero", None, None),          # custom
        ("P3 CRPS informed/pers", None, None),         # custom
        ("R2 size ratio", "r2_r_ratio", (0, 3.0)),
    ]
    fig, axes = plt.subplots(2, 4, figsize=(19, 8.5))
    colors = dict(E1="tab:green", E2="tab:orange", E3="tab:red")
    ls = dict(r1="-", r2="--")
    for ax, (title, key, ylim) in zip(axes.ravel(), panels):
        for w in worlds:
            for ro in rosters:
                xs, ys = [], []
                for t in tiers:
                    cell = agg.get(f"{w}|{ro}|{t}")
                    if not cell:
                        continue
                    if key:
                        v = cell.get(key)
                    elif "P2" in title:
                        a, b = cell.get("p2_mae_informed"), cell.get(
                            "p2_mae_zero")
                        v = (a / b) if (a is not None and b) else None
                    else:
                        a, b = cell.get("p3_crps_inf"), cell.get(
                            "p3_crps_pers")
                        v = (a / b) if (a is not None and b) else None
                    if v is None:
                        continue
                    xs.append(TIER_X[t])
                    ys.append(v)
                if xs:
                    ax.plot(xs, ys, marker="o", ls=ls[ro], color=colors[w],
                            label=f"{w} {ro}", lw=1.8, ms=5, alpha=0.85)
        ax.set_xscale("log")
        ax.set_xticks([0.25, 1, 4])
        ax.set_xticklabels(["1/4x", "1x", "4x"])
        ax.minorticks_off()
        ax.set_title(title, fontsize=11)
        ax.grid(alpha=0.25)
        if ylim:
            ax.set_ylim(*ylim)
        if "ratio" in title.lower() or "/" in title:
            ax.axhline(1.0, color="k", lw=0.8, alpha=0.5)
        if "skill" in title:
            ax.axhline(0.0, color="k", lw=0.8, alpha=0.5)
    axes[0, 0].legend(fontsize=8, ncol=2)
    fig.suptitle("A0 adequacy: reference-pipeline scores vs sensor budget "
                 "(x = budget tier)", fontsize=13)
    fig.tight_layout()
    p = os.path.join(figdir, "adequacy_curves.png")
    fig.savefig(p, dpi=130)
    plt.close(fig)
    print(f"[plots] {p}")


# ================================================================== drivers
def evalgroup(world, seed):
    os.makedirs(RESULTS, exist_ok=True)
    main_path, br_path = cache_paths(world, seed)
    cached = D.CachedRun(main_path)
    brz = np.load(br_path, allow_pickle=False)
    for roster in ROSTERS:
        for tier in TIERS:
            outp = os.path.join(RESULTS,
                                f"{world}_s{seed}_{roster}_{tier}.json")
            if os.path.exists(outp):
                print(f"[skip] {outp}")
                continue
            res = run_cell(world, seed, roster, tier, cached=cached, brz=brz)
            with open(outp, "w") as f:
                json.dump(res, f, indent=1, default=str)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["cache", "evalgroup", "cell",
                                    "aggregate"])
    ap.add_argument("--world", default="p4g2_044")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--roster", default="r1")
    ap.add_argument("--tier", default="x1")
    ap.add_argument("--workers", type=int, default=3)
    args = ap.parse_args()
    seed = args.seed if args.seed is not None else BASE_SEEDS[args.world]
    if args.cmd == "cache":
        build_cache(args.world, seed, workers=args.workers)
    elif args.cmd == "evalgroup":
        evalgroup(args.world, seed)
    elif args.cmd == "cell":
        res = run_cell(args.world, seed, args.roster, args.tier)
        print(json.dumps(res, indent=1, default=str))
    elif args.cmd == "aggregate":
        aggregate()


if __name__ == "__main__":
    main()
