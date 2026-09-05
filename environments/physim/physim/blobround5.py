"""physim.blobround5 — BLOB round-5 contract system (v2.1: category-anchored
contracts, closed-book reveal). EVALUATOR-SIDE.

Implements probes/blobs/l0/deepsearch/TRACKA_R5_ANCHORS.md (spec v2.1) for
worlds E1 (p4g2_044) + E2 (p6g8_033), difficulty tags BLOB2v2-E1 / BLOB2v2-E2.
BLOB2v2r2-E1/E2 reuse these exact contracts and truths with a separately
versioned resource policy. Legacy v2 ceilings and refusals remain available.
v1 (blobround2.py, tags BLOB2-E1/E2) is FROZEN; nothing here touches it.

The v2 mechanic (spec 2.1): a two-phase episode.
  PHASE A (exploration): the agent sees the SYLLABUS only — per tier the
    payload schema, the ladder rung names, and the instance-sampling DOMAIN
    (ranges, never values). World access is fully open: base-record reads
    over the whole cached span [0, 2500], exploration forks from any grid t,
    adjusts/injections inside forks, free resets. No budgets; silent safety
    caps only (CAPS5, target hit rate exactly 0).
  probe_ready() (agent-triggered, irreversible): reveals the six concrete
    instances and closes every world tool.
  PHASE B (closed book): only probe_status/probe_submit stay; answers come
    from the agent's own artifacts. Unsubmitted instances score -1; an
    episode that never calls probe_ready scores every instance -1.

INSTANCES (spec 2.2): hash-drawn once per (world, seed) from the published
domains, salt "r5_instances_v1" (blobround2 _rng pattern), hidden until the
reveal. Anchors are continuous-uniform in [600, 2300], realized at sim-step
resolution (dt=0.02; off the 5tu read grid with probability 1).

TRUTH (spec 2.6): per instance a fresh replica ensemble forked from the
exact anchor state (deterministic replay of the base realization), each
member running the protocol under an independent salted noise stream:
  member stream seed = sha256("truth|<world>|s<seed>|<instance>|m<m>")
  agent fork seed    = sha256("fork|<rollout nonce>|f<fork counter>")
Frozen-once per (world, seed, instance) under cache/round5/ (r5_ prefix).
Degenerate single-member truths (base realization, replay==live at A0
tolerance): L1 (adjust-only forks do not disturb the world), L2 (horizon
0), undisturbed legs with horizon <= 25tu. n_truth = 16, 24 for the
long-horizon instances (L3E, L3S, and the whole L3F instance, which carries
the H=400 leg) — spec Q3 recommendation.

SCORING (spec PART 3, formula unchanged from round 2):
  skill = clip(1 - CRPS_agent / CRPS_best_rung, -1, +1); unsubmitted = -1;
  reward = mean skill over the 6-instance menu. CRPS_agent = mean over
  truth members of CRPS(agent gaussian, member). Ladder rungs (climatology /
  persistence; AR(2) only on L3F) are recomputed PER INSTANCE from full-rate
  pre-anchor base-record history. Raw CRPS is logged verbatim (Q5a).

METERS (spec 2.7): all silent; logged per rollout, never surfaced, never
priced into reward. Legacy CAPS5/refusals are frozen. CAPS5_R2 has measured
headroom over real rollouts; r2 guard trips stop as unscored resource-limit
errors. Replayable LRU residency is separate from logical fork admission.
"""

from __future__ import annotations

import hashlib
import json
import os
from functools import lru_cache

import numpy as np

from physim import blobcore as B
from physim import blobround2 as R2

# ------------------------------------------------------------------ config
MENUS5 = dict(
    E1=("L1", "L2", "L3F", "L3E", "L4", "L4D"),
    E2=("L1", "L2", "L3F", "L3S", "L4", "L4D"),
)

EPISODES5 = {
    "BLOB2v2-E1": dict(world="p4g2_044", seeds=(928, 929, 930), menu="E1"),
    "BLOB2v2-E2": dict(world="p6g8_033", seeds=(942, 943, 944), menu="E2"),
    "BLOB2v2r2-E1": dict(world="p4g2_044", seeds=(928, 929, 930), menu="E1"),
    "BLOB2v2r2-E2": dict(world="p6g8_033", seeds=(942, 943, 944), menu="E2"),
}

T_BASE = 2500.0                       # full cached span, observable in A
N_STEPS_BASE = 500                    # 5tu grid frames (0..500)
SIM_DT = 0.02                         # sim substep (asserted at build)
SPC = int(round(B.CTRL_TU / SIM_DT))  # substeps per control step (250)

ANCHOR_LO, ANCHOR_HI = 600.0, 2300.0
L3F_H5 = dict(E1=(5.0, 25.0, 100.0, 400.0), E2=(25.0, 100.0, 400.0))
SINGLE_MEMBER_H = 25.0                # degenerate rule (spec 2.6)
L3E_N_WIN, L3E_WIN = 16, 50.0
L3S_EPOCHS5 = (400.0, 800.0)          # windows END at t_a+400 / t_a+800
L3S_WIN5 = 200.0
L4_LAGS5 = (10.0, 25.0, 50.0, 100.0, 175.0, 250.0)
L4D_LAGS5 = (25.0, 75.0, 150.0)
L4_AMP_RANGE = (1.5, 3.0)             # whole domain above AMP_CAP=1.0
L4D_AMP_RANGE = (0.30, 0.90)
DUR_RANGE = (5.0, 20.0)
SEQ_LEN_CHOICES = (1, 2, 3)
KH = R2.KH                            # hidden-sensor slots (13)

N_TRUTH = 16
N_TRUTH_LONG = 24                     # L3E / L3S / L3F (H=400 leg inside)

INSTANCE_SALT = "r5_instances_v1"
ACTIVE_SALT = INSTANCE_SALT   # test hook (reveal-leak gate G-R1)

# silent safety caps (spec 2.7; ~25-33x the v1 budgets; hit rate target 0)
CAPS5 = dict(sensor=1_000_000.0,      # node-tu
             adjust=30_000.0,         # commanded cu
             injection=3_000.0,       # amp-tu at the v1 price fn (meter)
             fork_spawns=400,         # count
             open_forks=8,            # concurrent
             sim_tu=100_000.0)        # live sim tu across all forks

CAP_MSG = "instrument saturated"      # frozen legacy-v2 refusal text

# Resource-policy-only revision, not new physics/contracts/truth. These
# values are PRIVATE runaway guards, not displayed budgets. Actual Fable
# demand reached 400 forks / 15,795 sim-tu / 536,360 sensor node-tu; r2 has
# 250x / 633x / 1,864x headroom on those observations, not a never-hit promise.
LEGACY_POLICY5 = "v2"
RESOURCE_POLICY5 = "v2r2"
CAPS5_R2 = dict(sensor=1_000_000_000.0,
                adjust=10_000_000.0,
                injection=1_000_000.0,
                fork_spawns=100_000,
                open_forks=10_000,       # LOGICAL handles, not resident sims
                sim_tu=10_000_000.0,     # aggregate only; no per-fork deadline
                log_entries=1_000_000)   # persisted op + emission entries
RESIDENT_FORKS5 = 8                      # replayable LRU, not an experiment cap
RESOURCE_STOP_MSG5 = "episode stopped by a safety guard"


def resource_policy5(difficulty: str) -> str:
    """Select an explicit cohort; old tags must never silently opt into r2."""
    if difficulty not in EPISODES5:
        raise ValueError(f"unknown round-5 cohort: {difficulty!r}")
    return (RESOURCE_POLICY5 if difficulty.startswith("BLOB2v2r2-")
            else LEGACY_POLICY5)


def resource_caps5(policy: str) -> dict:
    if policy == LEGACY_POLICY5:
        return CAPS5
    if policy == RESOURCE_POLICY5:
        return CAPS5_R2
    raise ValueError(f"unknown round-5 resource policy: {policy!r}")


def resource_metadata5(policy: str) -> dict:
    """Private host/trace metadata. NEVER include this in tool responses."""
    return dict(id=policy, caps=dict(resource_caps5(policy)),
                resident_forks=RESIDENT_FORKS5 if policy == RESOURCE_POLICY5
                else CAPS5["open_forks"],
                resident_policy="lru-replay" if policy == RESOURCE_POLICY5
                else "legacy-open-limit",
                safety_trip="truncate" if policy == RESOURCE_POLICY5
                else "generic-refusal")

_R5_CACHE_DIR = os.environ.get(
    "PHYSIM_BLOB_R5_CACHE", os.path.join(B.CACHE_DIR, "round5"))


def episode_cfg5(difficulty: str, seed_idx: int) -> dict:
    ep = EPISODES5[difficulty]
    return dict(world=ep["world"], seed=ep["seeds"][seed_idx % 3],
                menu=ep["menu"])


def _seed_from(key: str) -> int:
    return int(hashlib.sha256(key.encode()).hexdigest()[:16], 16)


def _rng5(world: str, seed: int, tag: str) -> np.random.Generator:
    return np.random.default_rng(
        _seed_from(B.world_key(world, seed) + "|" + tag))


def truth_member_seed(world: str, seed: int, iid: str, m: int) -> int:
    """Truth noise streams: build-side salt (domain-separated from forks)."""
    return _seed_from(f"truth|{world}|s{seed}|{iid}|m{m}")


def fork_stream_seed(nonce: str, counter: int) -> int:
    """Agent fork noise streams: rollout nonce + fork counter."""
    return _seed_from(f"fork|{nonce}|f{counter}")


# --------------------------------------------------------------- instances
def _snap_t(t: float) -> tuple[float, int]:
    k = int(round(t / SIM_DT))
    return round(k * SIM_DT, 2), k


def _l1_prefix_ok(seq: np.ndarray) -> bool:
    """Apparatus acceptance for a command sequence from device 0's t=0
    configuration (dilation 1.0): every prefix keeps the dilation strictly
    inside its bounds (margin so the truth walk can never be refused)."""
    dil = 1.0
    for j in range(len(seq)):
        dil = dil * float(np.exp(seq[j, 2]))     # u3 -> dlog (R3-final map)
        if not (0.5 + 1e-6 <= dil <= 3.0 - 1e-6):
            return False
    return True


@lru_cache(maxsize=16)
def instances5(world: str, seed: int, menu: str,
               salt: str = INSTANCE_SALT) -> dict:
    """The hidden instance menu, hash-drawn once per (world, seed) from the
    published domains. NEVER agent-visible before probe_ready. Independent
    draws per family (anchors spread over t statistically)."""
    nf = B.n_ports(world, seed)
    out = {}
    for cid in MENUS5[menu]:
        rng = _rng5(world, seed, f"{salt}|{cid}")
        t_a, k_a = _snap_t(float(rng.uniform(ANCHOR_LO, ANCHOR_HI)))
        inst = dict(id=f"{cid}@i1", family=cid, t_a=t_a, k_a=k_a)
        if cid == "L1":
            while True:
                n = int(rng.integers(1, 4))
                seq = np.round(rng.uniform(-1.0, 1.0, (n, 3)), 4)
                if _l1_prefix_ok(seq):
                    break
            inst["seq"] = [[float(x) for x in u] for u in seq]
        elif cid == "L3F":
            inst["device"] = int(rng.integers(0, 2))
            inst["horizons"] = [float(h) for h in L3F_H5[menu]]
        elif cid == "L3E":
            cc = B.contracts(world, seed)["private"]
            inst.update(port=int(cc["p2_port"]), sign=float(cc["p2_sign"]),
                        thr=float(cc["p2_thr"]), n_windows=L3E_N_WIN,
                        window_tu=L3E_WIN)
        elif cid == "L3S":
            inst.update(epochs=[float(e) for e in L3S_EPOCHS5],
                        window_tu=L3S_WIN5)
        elif cid in ("L4", "L4D"):
            lo, hi = L4_AMP_RANGE if cid == "L4" else L4D_AMP_RANGE
            inst["port"] = int(rng.integers(0, nf))
            inst["amp"] = round(float(rng.uniform(lo, hi)), 4)
            dur, k_dur = _snap_t(float(rng.uniform(*DUR_RANGE)))
            inst.update(dur=dur, k_dur=k_dur,
                        lags=[float(x) for x in
                              (L4_LAGS5 if cid == "L4" else L4D_LAGS5)])
        out[cid] = inst
    return out


def payload_shapes5(world: str, seed: int, menu: str,
                    salt: str = INSTANCE_SALT) -> dict:
    """Required {"mean","sigma"} shapes per instance (post-reveal facts:
    L3F's device axis depends on the drawn device)."""
    cc = B.contracts(world, seed)["private"]
    nf, kA, kB = cc["nf"], cc["kA"], cc["kB"]
    ii = instances5(world, seed, menu, salt)
    k_i = (kA, kB)[ii["L3F"]["device"]]
    shapes = dict(
        L1=(nf, kA),
        L2=(nf, KH),
        L3F=(len(L3F_H5[menu]), nf, k_i),
        L4=(len(L4_LAGS5), nf, kB),
        L4D=(len(L4D_LAGS5), nf, kB),
    )
    if "L3E" in MENUS5[menu]:
        shapes["L3E"] = (L3E_N_WIN,)
    if "L3S" in MENUS5[menu]:
        shapes["L3S"] = (len(L3S_EPOCHS5), nf, 2)
    return shapes


# ---------------------------------------------------------------- syllabus
# Normative Phase-A contract text (spec 2.3, verbatim; <angle> constants are
# category facts per (world, seed) — instance-independent by the reveal-leak
# audit). Published in the system prompt and repeated by probe_status.
_SYLLABUS_HEAD = """SYLLABUS — BLOB2v2-{tag} (the only contract text before the reveal)
This episode has two phases. NOW (exploration): probe_read / probe_wait /
probe_adjust / probe_fork / probe_reset / probe_inject are open on the
base record and on your forks. WHEN YOU CALL probe_ready(): the six
instances below are revealed with concrete values, every world tool
closes for the rest of the episode, and probe_submit opens. Everything
outside the world (your notes, files, code) stays available. Submit
{{"mean","sigma"}} arrays of the stated shape per instance; resubmission
allowed, last accepted wins; unsubmitted instances score -1.
Scoring per instance: skill = 1 - CRPS/CRPS_ref, clipped to [-1, 1],
where CRPS_ref is the best of the stated reference forecasts ("ladder"),
fit to pre-anchor base-record data; reward = mean over the six.
Hidden instance parameters are sampled once per episode from the stated
domains and revealed all at once at probe_ready(). CONTINUOUS means any
real value in the range — do not expect grid values. tu = time units of
the base record, which spans [0, 2500].
 L1  apparatus response. At a hidden anchor a fresh fork is taken and a
     hidden command sequence is applied to device 0 (from its t=0
     configuration); predict device 0's reading right after the final
     command. domain: anchor t_a continuous-uniform in [600, 2300];
     sequence length in {{1, 2, 3}}; each command u in [-1, 1]^3,
     components continuous, one control step each; only sequences the
     apparatus accepts are drawn. payload: [ports][slots of device 0].
     ladder: climatology | persistence.
 L2  hidden-sensor nowcast. One additional fixed sensor cluster of 13
     slots reports the same ports; predict its reading vector at a
     hidden anchor. domain: t_a continuous-uniform in [600, 2300].
     payload: [ports][13]. ladder: global climatology | global
     persistence."""

_SYLLABUS_L3F_E1 = """ L3F forecast. Predict device i's streams (t=0 configuration) at every
     horizon H in {5, 25, 100, 400} tu after a hidden anchor,
     undisturbed. domain: device i uniform over your devices {0, 1};
     t_a continuous-uniform in [600, 2300]. payload:
     [4][ports][slots of device i]. ladder: climatology | persistence
     | AR(2)."""

_SYLLABUS_L3F_E2 = """ L3F forecast. Predict device i's streams (t=0 configuration) at every
     horizon H in {25, 100, 400} tu after a hidden anchor,
     undisturbed. domain: device i uniform over your devices {0, 1};
     t_a continuous-uniform in [600, 2300]. payload:
     [3][ports][slots of device i]. ladder: climatology | persistence
     | AR(2)."""

_SYLLABUS_L3E = """ L3E event rate. Predict the crossing count of the announced event
     (port {p2_port}, sign {p2_sign}, threshold {p2_thr}) in each of 16
     consecutive 50tu windows starting at a hidden anchor, undisturbed;
     windows may extend past the base record. domain: t_a continuous-
     uniform in [600, 2300]. payload: [16]. ladder: zero-rate |
     pre-anchor rate."""

_SYLLABUS_L3S = """ L3S slow observable. Predict the per-port global mean and variance
     (the free aggregate stream) averaged over the 200tu windows ending
     at t_a+400 and t_a+800, undisturbed. domain: t_a continuous-uniform
     in [600, 2300]. payload: [2][ports][2] with [.,.,0]=mean
     [.,.,1]=variance. ladder: windowed climatology | windowed
     persistence."""

_SYLLABUS_TAIL = """ L4  emission response, beyond the apparatus range. At a hidden anchor a
     fresh fork is taken and one hidden emission is driven through the
     same emitter probe_inject uses; predict device 1's streams (t=0
     configuration) at lags {10, 25, 50, 100, 175, 250} tu from emission
     start. domain: t_a continuous-uniform in [600, 2300]; port uniform
     over the ports; amp continuous-uniform in [1.5, 3.0] (your
     apparatus stops at 1.0); dur continuous-uniform in [5, 20] tu.
     payload: [6][ports][slots of device 1]. ladder: climatology |
     persistence.
 L4D emission response, inside the apparatus range. Same protocol shape
     as L4. domain: t_a continuous-uniform in [600, 2300]; port uniform
     over the ports; amp continuous-uniform in [0.30, 0.90]; dur
     continuous-uniform in [5, 20] tu; lags {25, 75, 150} tu. payload:
     [3][ports][slots of device 1]. ladder: climatology | persistence."""


@lru_cache(maxsize=8)
def syllabus5(world: str, seed: int, menu: str,
              resource_policy: str = LEGACY_POLICY5) -> str:
    """Published Phase-A text. Resource revision changes the label ONLY;
    domains/category facts never depend on hidden instances or meters."""
    resource_caps5(resource_policy)  # reject unknown private policy ids
    head = _SYLLABUS_HEAD.format(tag=menu)
    if resource_policy == RESOURCE_POLICY5:
        head = head.replace("BLOB2v2-", "BLOB2v2r2-", 1)
    parts = [head]
    parts.append(_SYLLABUS_L3F_E1 if menu == "E1" else _SYLLABUS_L3F_E2)
    if "L3E" in MENUS5[menu]:
        cc = B.contracts(world, seed)["private"]
        parts.append(_SYLLABUS_L3E.format(
            p2_port=int(cc["p2_port"]), p2_sign=int(cc["p2_sign"]),
            p2_thr=round(float(cc["p2_thr"]), 6)))
    if "L3S" in MENUS5[menu]:
        parts.append(_SYLLABUS_L3S)
    parts.append(_SYLLABUS_TAIL)
    return "\n".join(parts)


def reveal_menu5(world: str, seed: int, menu: str,
                 salt: str = INSTANCE_SALT) -> list:
    """The concrete instance menu returned by probe_ready / post-reveal
    probe_status. ALL values explicit (spec 2.2). Agent-visible."""
    ii = instances5(world, seed, menu, salt)
    shapes = payload_shapes5(world, seed, menu, salt)
    items = []
    for cid in MENUS5[menu]:
        inst = ii[cid]
        d = dict(id=inst["id"], anchor_t=round(inst["t_a"], 2),
                 payload_shape=list(shapes[cid]))
        if cid == "L1":
            d["device"] = 0
            d["sequence"] = [list(u) for u in inst["seq"]]
            d["statistic"] = (
                "a fresh fork is taken at the anchor and the command "
                "sequence is applied to device 0 (from its t=0 "
                "configuration, one control step per command, no "
                "emission); predict its reading right after the final "
                "command")
        elif cid == "L2":
            d["slots"] = KH
            d["statistic"] = (
                "the additional fixed 13-slot sensor cluster's reading "
                "vector at the anchor")
        elif cid == "L3F":
            d["device"] = inst["device"]
            d["horizons"] = [int(h) for h in inst["horizons"]]
            d["statistic"] = (
                "device {}'s streams (t=0 configuration) at each horizon "
                "after the anchor, undisturbed".format(inst["device"]))
        elif cid == "L3E":
            d.update(port=inst["port"], sign=int(inst["sign"]),
                     thr=round(inst["thr"], 6), n_windows=inst["n_windows"],
                     window_tu=int(inst["window_tu"]))
            d["statistic"] = (
                "count of upward crossings of sign*value above thr, summed "
                "over device 0's slots (t=0 configuration), per consecutive "
                "window starting at the anchor, undisturbed")
        elif cid == "L3S":
            d.update(epochs=[int(e) for e in inst["epochs"]],
                     window_tu=int(inst["window_tu"]))
            d["statistic"] = (
                "the per-port global mean and variance (the free aggregate "
                "stream), each averaged over the window ending at the "
                "anchor plus the stated epoch, undisturbed")
        elif cid in ("L4", "L4D"):
            d.update(device=1, port=inst["port"], amp=inst["amp"],
                     dur_tu=inst["dur"], lags=[int(x) for x in inst["lags"]])
            d["statistic"] = (
                "one emission (port, amp, dur) is driven through the fixed "
                "emission channel from the anchor on a fresh fork; predict "
                "device 1's streams (t=0 configuration) at each lag from "
                "emission start")
        items.append(d)
    return items


# ------------------------------------------------------------- truth build
# One deterministic base pass per (world, seed) realizes the exact f32
# anchor states + the degenerate single-member truths; ensemble members are
# then run as independent live replicas (verbatim step_chunk dynamics) with
# salted noise streams. Frozen-once under cache/round5/ (r5_ prefix).

def _anchors_path(world: str, seed: int, cache_dir: str | None = None) -> str:
    d = cache_dir or _R5_CACHE_DIR
    return os.path.join(d, f"r5_{world}_s{seed}_anchors.npz")


def _partial_path(world: str, seed: int, cid: str, m0: int, m1: int,
                  cache_dir: str | None = None) -> str:
    d = cache_dir or _R5_CACHE_DIR
    return os.path.join(d, f"r5_{world}_s{seed}_{cid}_m{m0}-{m1}.npz")


def truth_path(world: str, seed: int, cache_dir: str | None = None) -> str:
    d = cache_dir or _R5_CACHE_DIR
    return os.path.join(d, f"r5_{world}_s{seed}_truth.npz")


def n_truth_of(cid: str) -> int:
    return N_TRUTH_LONG if cid in ("L3F", "L3E", "L3S") else N_TRUTH


def ens_cids(menu: str) -> tuple:
    return tuple(c for c in MENUS5[menu] if c not in ("L1", "L2"))


def _l3f_split(menu: str) -> tuple:
    """([deg horizons], [ensemble horizons]) per the spec-2.6 degenerate
    rule: undisturbed legs with H <= 25tu are single-member."""
    hs = L3F_H5[menu]
    return (tuple(h for h in hs if h <= SINGLE_MEMBER_H + 1e-9),
            tuple(h for h in hs if h > SINGLE_MEMBER_H + 1e-9))


def _walked_device_l1(world: str, seed: int, seq: list):
    """Device 0 after the hidden command sequence (one control step per
    command) from its t=0 configuration. R3-final fixed actuator map."""
    dev = B.make_device(world, seed, B.DEV_A)
    M = B.adjust_mix(B.world_key(world, seed))
    for u in seq:
        d = M @ np.asarray(u, float)
        dev.center = (dev.center + d[:2]) % dev.L
        dev.dilation = float(np.clip(dev.dilation * np.exp(d[2]),
                                     *dev.dil_bounds))
    return dev


@lru_cache(maxsize=8)
def worker_export(world: str, seed: int) -> str:
    """JSON payload that lets a member worker sample devices WITHOUT loading
    the (heavy) frame cache: device secrets, port perm, emitter home, dx/L."""
    c = B.get_cached(world, seed)
    sec = B.get_secrets(world, seed)
    devs = []
    for i, cfg in enumerate(B.ROSTER):
        ds = sec["devices"][i]
        devs.append(dict(lattice=cfg["lattice"], n_rings=cfg["n_rings"],
                         base_ds=cfg["base_ds"], center=ds["center"],
                         secret_rot=ds["secret_rot"], reflect=ds["reflect"],
                         motion_theta=ds["motion_theta"],
                         motion_reflect=ds["motion_reflect"],
                         node_perm=ds["node_perm"]))
    return json.dumps(dict(
        L=c.meta["L"], dx=c.meta["dx"], N=c.meta["N"],
        na=c.meta["na"], nc=c.meta["nc"],
        port_perm=list(sec["port_perm"]),
        inj_yx=list(sec["devices"][B.DEV_A]["center"]),
        devices=devs))


def _device_from_export(exp: dict, idx: int):
    d = exp["devices"][idx]
    return B.agdev.ProbeDevice(
        dev_id=idx, lattice=d["lattice"], n_rings=d["n_rings"],
        base_ds=d["base_ds"], center=d["center"], L=exp["L"],
        secret_rot=d["secret_rot"], reflect=d["reflect"],
        motion_theta=d["motion_theta"], motion_reflect=d["motion_reflect"],
        node_perm=d["node_perm"])


def build_anchors(world: str, seed: int, menu: str,
                  salt: str = INSTANCE_SALT, cache_dir: str | None = None,
                  workers: int = 3, verbose: bool = True) -> dict:
    """Stage 1: ONE deterministic replay of the base realization from t=0
    (verbatim step_chunk, original noise stream), capturing per instance the
    exact f32 anchor state and every degenerate single-member truth.
    Self-checks: SIM_DT, bitwise state equality at the 1700 snapshot, and
    replay==live vs the f16 record at A0 tolerance."""
    from blobkit.soup import sim_cpu
    path = _anchors_path(world, seed, cache_dir)
    if os.path.exists(path):
        return dict(np.load(path, allow_pickle=False))
    ii = instances5(world, seed, menu, salt)
    c = B.get_cached(world, seed)
    g = B.load_genome(world)
    perm = np.asarray(B.get_secrets(world, seed)["port_perm"], int)
    dx = c.meta["dx"]
    S = sim_cpu.init_soup(g, L=c.meta["L"], seed=seed, dtype="f32",
                          workers=workers)
    assert abs(S["dt"] - SIM_DT) < 1e-12, S["dt"]

    # agenda: (substep, kind, cid, extra)
    events = []
    for cid in MENUS5[menu]:
        inst = ii[cid]
        k_a = inst["k_a"]
        if cid == "L1":
            events.append((k_a + len(inst["seq"]) * SPC, "l1", cid, None))
        elif cid == "L2":
            events.append((k_a, "l2", cid, None))
        elif cid == "L3F":
            deg, _ens = _l3f_split(menu)
            for j, H in enumerate(deg):
                events.append((k_a + int(round(H / SIM_DT)), "l3f_deg",
                               cid, j))
            events.append((k_a, "anchor", cid, None))
        else:
            events.append((k_a, "anchor", cid, None))
    # parity checkpoints (grid frames) + the 1700 snapshot check
    for i_chk in (120, 200, 340, 460):
        events.append((i_chk * SPC, "parity", "", i_chk))
    events.sort(key=lambda e: e[0])

    out = {}
    deg_l3f = {}
    parity_max = 0.0
    devA = B.make_device(world, seed, B.DEV_A)
    devB = B.make_device(world, seed, B.DEV_B)
    dev_l1 = _walked_device_l1(world, seed, ii["L1"]["seq"])
    dev_hid = R2.hidden_device(world, seed)
    dev_l3f = (devA, devB)[ii["L3F"]["device"]]
    now = 0
    for k_sub, kind, cid, extra in events:
        if k_sub > now:
            B.agdev.step_chunk(S, k_sub - now)
            now = k_sub
        F = np.asarray(S["F"], np.float32)
        if kind == "anchor":
            out[f"F_{cid}"] = F.copy()
        elif kind == "l1":
            out["L1"] = dev_l1.sample(F[perm], dx)[None]
        elif kind == "l2":
            out["L2"] = dev_hid.sample(F[perm], dx)[None]
        elif kind == "l3f_deg":
            deg_l3f[extra] = dev_l3f.sample(F[perm], dx)
        elif kind == "parity":
            i_chk = extra
            live = devA.sample(F[perm], dx)
            rep = B.sample_at(world, seed, i_chk, devA)
            parity_max = max(parity_max, float(np.abs(live - rep).max()))
            if abs(i_chk * B.CTRL_TU - 1700.0) < 1e-9:
                snapF = c._z["snapF_1700"]
                assert np.array_equal(F, snapF), \
                    "base pass diverged from the cached 1700 snapshot"
    assert parity_max <= 2e-3, f"replay==live parity broke: {parity_max}"
    deg, _ens = _l3f_split(menu)
    if deg:
        out["L3F_deg"] = np.stack([deg_l3f[j] for j in range(len(deg))])
    meta = dict(world=world, seed=seed, menu=menu, salt=salt,
                instances=ii, parity_max=parity_max,
                export=json.loads(worker_export(world, seed)))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp.npz"
    np.savez_compressed(tmp, meta=json.dumps(meta), **out)
    os.replace(tmp, path)
    if verbose:
        print(f"[anchors] {world} s{seed}: parity_max={parity_max:.2e}"
              f" -> {path}")
    return dict(np.load(path, allow_pickle=False))


def _member_state(template: dict, F0: np.ndarray, m_seed: int,
                  k_a: int) -> dict:
    """Shallow-copied live sim state: shared read-only params, own fields +
    own (salted) noise stream. step_chunk only rebinds S["F"]/S["t_step"]
    and draws from S["rng"], so sharing the rest is safe."""
    S = dict(template)
    S["F"] = np.array(F0, np.float32)
    S["rng"] = np.random.default_rng(m_seed)
    S["t_step"] = k_a
    return S


def _run_member(template: dict, exp: dict, inst: dict, F0: np.ndarray,
                m_seed: int, menu: str):
    """One truth member: run the instance protocol live from the anchor
    state under the member's own noise stream; return the sampled truth."""
    cid = inst["family"]
    perm = np.asarray(exp["port_perm"], int)
    dx = exp["dx"]
    S = _member_state(template, F0, m_seed, inst["k_a"])

    def _sample(dev):
        return dev.sample(np.asarray(S["F"], np.float32)[perm], dx)

    if cid == "L3F":
        dev = _device_from_export(exp, inst["device"])
        _deg, ens = _l3f_split(menu)
        marks = {int(round(H / B.CTRL_TU)) for H in ens}
        n_ctrl = max(marks)
        out = {}
        for j in range(1, n_ctrl + 1):
            B.agdev.step_chunk(S, SPC)
            if j in marks:
                out[j] = _sample(dev)
        return np.stack([out[int(round(H / B.CTRL_TU))] for H in ens])

    if cid == "L3E":
        dev = _device_from_export(exp, 0)
        n_ctrl = int(round(L3E_N_WIN * L3E_WIN / B.CTRL_TU))      # 160
        vals = [_sample(dev)[inst["port"]]]
        for _ in range(n_ctrl):
            B.agdev.step_chunk(S, SPC)
            vals.append(_sample(dev)[inst["port"]])
        A = np.stack(vals) * inst["sign"]                          # (161, k)
        up = B._crossings_per_step(A, inst["thr"])                 # (160,)
        fpw = int(round(L3E_WIN / B.CTRL_TU))
        return np.array([up[w * fpw:(w + 1) * fpw].sum()
                         for w in range(L3E_N_WIN)], float)

    if cid == "L3S":
        n_ctrl = int(round(max(L3S_EPOCHS5) / B.CTRL_TU))          # 160
        fpw = int(round(L3S_WIN5 / B.CTRL_TU))                     # 40
        gs = []
        for _ in range(n_ctrl):
            B.agdev.step_chunk(S, SPC)
            f = np.asarray(S["F"], np.float32)[perm]
            gs.append(np.stack([f.mean(axis=(1, 2)), f.var(axis=(1, 2))],
                               axis=1))
        gs = np.stack(gs)                                          # (160,nf,2)
        out = []
        for ep in L3S_EPOCHS5:
            j1 = int(round(ep / B.CTRL_TU))                        # 80/160
            out.append(gs[j1 - fpw:j1].mean(axis=0))
        return np.stack(out)                                       # (2,nf,2)

    if cid in ("L4", "L4D"):
        dev = _device_from_export(exp, 1)
        inj = dict(field=int(perm[inst["port"]]), y=exp["inj_yx"][0],
                   x=exp["inj_yx"][1], amp=float(inst["amp"]))
        k_dur = int(inst["k_dur"])
        marks = {int(round(x / B.CTRL_TU)) for x in inst["lags"]}
        n_ctrl = max(marks)
        out = {}
        for j in range(1, n_ctrl + 1):
            done = (j - 1) * SPC
            act = int(np.clip(k_dur - done, 0, SPC))
            if act > 0:
                B.agdev.step_chunk(S, act, injections=[inj])
            if act < SPC:
                B.agdev.step_chunk(S, SPC - act)
            if j in marks:
                out[j] = _sample(dev)
        return np.stack([out[int(round(x / B.CTRL_TU))]
                         for x in inst["lags"]])
    raise ValueError(cid)


def run_member_chunk(world: str, seed: int, menu: str, cid: str,
                     m0: int, m1: int, salt: str = INSTANCE_SALT,
                     cache_dir: str | None = None, workers: int = 1,
                     verbose: bool = True) -> str:
    """Worker entry: members [m0, m1) of one instance's truth ensemble.
    Loads the stage-1 anchors npz only (never the frame cache)."""
    from blobkit.soup import sim_cpu
    out_path = _partial_path(world, seed, cid, m0, m1, cache_dir)
    if os.path.exists(out_path):
        return out_path
    z = np.load(_anchors_path(world, seed, cache_dir), allow_pickle=False)
    meta = json.loads(str(z["meta"]))
    assert meta["salt"] == salt and meta["menu"] == menu
    exp = meta["export"]
    inst = meta["instances"][cid]
    g = B.load_genome(world)
    template = sim_cpu.init_soup(g, L=exp["L"], seed=seed, dtype="f32",
                                 workers=workers)
    assert abs(template["dt"] - SIM_DT) < 1e-12
    F0 = z[f"F_{cid}"]
    mem = []
    for m in range(m0, m1):
        mem.append(_run_member(template, exp, inst, F0,
                               truth_member_seed(world, seed, inst["id"], m),
                               menu))
        if verbose:
            print(f"[member] {world} s{seed} {cid} m{m} done", flush=True)
    arr = np.stack(mem)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    tmp = out_path + f".tmp{os.getpid()}.npz"
    np.savez_compressed(tmp, members=arr)
    os.replace(tmp, out_path)
    return out_path


def member_jobs(menu: str) -> list:
    """(cid, m0, m1) worker chunks for one (world, seed). 800tu-per-member
    ensembles get smaller chunks so the job queue stays even."""
    jobs = []
    for cid in ens_cids(menu):
        M = n_truth_of(cid)
        chunk = 2 if cid in ("L3E", "L3S") else 4
        for m0 in range(0, M, chunk):
            jobs.append((cid, m0, min(m0 + chunk, M)))
    return jobs


def assemble_truth(world: str, seed: int, menu: str,
                   salt: str = INSTANCE_SALT, cache_dir: str | None = None,
                   keep_partials: bool = False) -> str:
    """Stage 3: gather stage-1 degenerate truths + member partials into the
    frozen truth npz (per-array sha256 manifest for the determinism gate)."""
    path = truth_path(world, seed, cache_dir)
    if os.path.exists(path):
        return path
    z = np.load(_anchors_path(world, seed, cache_dir), allow_pickle=False)
    meta = json.loads(str(z["meta"]))
    assert meta["salt"] == salt and meta["menu"] == menu
    ii = instances5(world, seed, menu, salt)
    assert json.dumps(meta["instances"], sort_keys=True) == \
        json.dumps(ii, sort_keys=True), "instance drift since anchors build"
    arrs = {}
    deg, ens = _l3f_split(menu)
    arrs["L1"] = z["L1"]
    arrs["L2"] = z["L2"]
    for j, H in enumerate(deg):
        arrs[f"L3F_h{int(H)}"] = z["L3F_deg"][j][None]
    for cid in ens_cids(menu):
        M = n_truth_of(cid)
        parts = []
        for c2, m0, m1 in member_jobs(menu):
            if c2 != cid:
                continue
            pp = _partial_path(world, seed, cid, m0, m1, cache_dir)
            assert os.path.exists(pp), f"missing member chunk {pp}"
            parts.append(np.load(pp, allow_pickle=False)["members"])
        full = np.concatenate(parts, axis=0)
        assert len(full) == M, (cid, len(full), M)
        if cid == "L3F":
            for j, H in enumerate(ens):
                arrs[f"L3F_h{int(H)}"] = full[:, j]
        else:
            arrs[cid] = full
    hashes = {k: hashlib.sha256(np.ascontiguousarray(v).tobytes())
              .hexdigest() for k, v in sorted(arrs.items())}
    manifest = dict(world=world, seed=seed, menu=menu, salt=salt,
                    instances=ii, n_truth={c: n_truth_of(c)
                                           for c in ens_cids(menu)},
                    parity_max=meta["parity_max"], hashes=hashes)
    tmp = path + ".tmp.npz"
    np.savez_compressed(tmp, manifest=json.dumps(manifest), **arrs)
    os.replace(tmp, path)
    if not keep_partials:
        for cid, m0, m1 in member_jobs(menu):
            pp = _partial_path(world, seed, cid, m0, m1, cache_dir)
            if os.path.exists(pp):
                os.remove(pp)
    return path


@lru_cache(maxsize=8)
def load_truth(world: str, seed: int, menu: str,
               salt: str = INSTANCE_SALT) -> dict:
    """The frozen truth tensors, keyed (world, seed, instance). Guards
    against instance drift (a redraw after the freeze is a hard error)."""
    path = truth_path(world, seed)
    if not os.path.exists(path):
        raise RuntimeError(
            f"missing round-5 truth cache {path}; build it with "
            f"environments/physim/tools/build_blob5_truth.py")
    z = np.load(path, allow_pickle=False)
    man = json.loads(str(z["manifest"]))
    assert man["salt"] == salt and man["menu"] == menu
    ii = instances5(world, seed, menu, salt)
    assert json.dumps(man["instances"], sort_keys=True) == \
        json.dumps(ii, sort_keys=True), \
        "instance registry drifted after the truth freeze"
    out = {k: z[k] for k in z.files if k != "manifest"}
    out["_manifest"] = man
    return out


def truth_legs(world: str, seed: int, menu: str) -> dict:
    """cid -> list of (leg label, member array (M, ...)) in payload order."""
    tr = load_truth(world, seed, menu)
    legs = dict(
        L1=[("", tr["L1"])],
        L2=[("", tr["L2"])],
        L3F=[(f"h{int(H)}", tr[f"L3F_h{int(H)}"]) for H in L3F_H5[menu]],
        L4=[("", tr["L4"])],
        L4D=[("", tr["L4D"])],
    )
    if "L3E" in MENUS5[menu]:
        legs["L3E"] = [("", tr["L3E"])]
    if "L3S" in MENUS5[menu]:
        legs["L3S"] = [("", tr["L3S"])]
    return legs


# ------------------------------------------------------ ladders + scoring
def _crps_vs_members(mu, sig, members) -> float:
    """Mean over truth members of the mean elementwise gaussian CRPS —
    the unbiased estimate of expected CRPS under the world's own
    predictive distribution (spec PART 3)."""
    return float(np.mean([B.gauss_crps(mu, sig, y).mean()
                          for y in members]))


def _crps_legged(legs, mu_by_leg, sig_by_leg) -> float:
    """Mean over legs of the per-leg member-averaged CRPS. Payload axis 0
    indexes legs for multi-leg instances (L3F); single-leg instances pass
    one leg covering the whole payload."""
    return float(np.mean([
        _crps_vs_members(mu_by_leg[j], sig_by_leg[j], leg_members)
        for j, (_lbl, leg_members) in enumerate(legs)]))


@lru_cache(maxsize=8)
def _hist_dev(world: str, seed: int, dev_idx: int) -> np.ndarray:
    """(T, nf, k) full-span base-record streams of a roster device at its
    t=0 configuration, frames 1..N_STEPS_BASE (the classical record any
    agent could keep)."""
    dev = B.make_device(world, seed, dev_idx)
    return np.stack([B.sample_at(world, seed, i, dev)
                     for i in range(1, N_STEPS_BASE + 1)])


@lru_cache(maxsize=8)
def _hist_glob(world: str, seed: int) -> np.ndarray:
    """(T, nf, 2) free global mean/var stream, frames 1..N_STEPS_BASE."""
    return np.stack([B.global_stats(world, seed, i)
                     for i in range(1, N_STEPS_BASE + 1)])


def _i_hist(t_a: float) -> int:
    """Frames 1..i_hist are pre-anchor history (last 5tu grid read at or
    before the anchor); as an index into the frame-1-based arrays the
    history slice is [:i_hist]."""
    return int(np.floor(t_a / B.CTRL_TU + 1e-9))


@lru_cache(maxsize=8)
def ladders5(world: str, seed: int, menu: str) -> dict:
    """The reference ladder, recomputed PER INSTANCE from full-rate
    pre-anchor base-record history (pose- and instance-ignorant classical
    estimators; v1 rung conventions), evaluated against the frozen truth
    members with the same reduction as agent payloads."""
    ii = instances5(world, seed, menu)
    legs_all = truth_legs(world, seed, menu)
    out = {}

    def clim_pers(hist, legs, extra=None):
        mu_c, sd_c = hist[:-1].mean(0), hist[:-1].std(0) + 1e-6
        last = hist[-1]
        n = len(legs)
        rungs = dict(
            climatology=_crps_legged(legs, [mu_c] * n, [sd_c] * n),
            persistence=_crps_legged(legs, [last] * n, [sd_c] * n))
        if extra:
            rungs.update(extra(mu_c, sd_c, last))
        return rungs

    # L1: device-0 floors (pose-ignorant; the walk is hidden information)
    ih = _i_hist(ii["L1"]["t_a"])
    out["L1"] = clim_pers(_hist_dev(world, seed, 0)[:ih], legs_all["L1"])

    # L2: global-aggregate floors (free stream; no spatial model)
    ih = _i_hist(ii["L2"]["t_a"])
    G = _hist_glob(world, seed)[:ih]
    gm = G[:, :, 0]
    mu_c = np.repeat(gm[:-1].mean(0)[:, None], KH, 1)
    sd_c = np.repeat((np.sqrt(G[:-1, :, 1].mean(0) + gm[:-1].var(0))
                      + 1e-6)[:, None], KH, 1)
    mu_p = np.repeat(gm[-1][:, None], KH, 1)
    sd_p = np.repeat((np.sqrt(G[-1, :, 1]) + 1e-6)[:, None], KH, 1)
    out["L2"] = dict(
        climatology=_crps_vs_members(mu_c, sd_c, legs_all["L2"][0][1]),
        persistence=_crps_vs_members(mu_p, sd_p, legs_all["L2"][0][1]))

    # L3F: climatology / persistence / AR(2), per revealed device
    inst = ii["L3F"]
    ih = _i_hist(inst["t_a"])
    A = _hist_dev(world, seed, inst["device"])[:ih]
    mu_c, sd_c = A[:-1].mean(0), A[:-1].std(0) + 1e-6
    last = A[-1]
    Sa = A.reshape(len(A), -1)
    legs = legs_all["L3F"]
    cl, pe, ar = [], [], []
    for j, H in enumerate(L3F_H5[menu]):
        members = legs[j][1]
        # forecast steps from the LAST pre-anchor grid read to the exact
        # (off-grid) truth time t_a + H
        n = max(int(round((inst["t_a"] + H) / B.CTRL_TU)) - ih, 1)
        cl.append(_crps_vs_members(mu_c, sd_c, members))
        pe.append(_crps_vs_members(last, sd_c, members))
        mu_a, sig_a = R2._ar2_mu_sig(Sa, n)
        ar.append(_crps_vs_members(mu_a.reshape(A.shape[1:]),
                                   sig_a.reshape(A.shape[1:]), members))
    out["L3F"] = dict(climatology=float(np.mean(cl)),
                      persistence=float(np.mean(pe)),
                      ar2=float(np.mean(ar)))

    if "L3E" in MENUS5[menu]:
        inst = ii["L3E"]
        ih = _i_hist(inst["t_a"])
        A = _hist_dev(world, seed, 0)[:ih, inst["port"], :] * inst["sign"]
        up = B._crossings_per_step(A, inst["thr"])
        fpw = int(round(L3E_WIN / B.CTRL_TU))
        n_pre = len(up) // fpw
        pre = np.array([up[w * fpw:(w + 1) * fpw].sum()
                        for w in range(n_pre)], float)
        sig_ev = pre.std() + 0.5
        rate = pre.mean()
        members = legs_all["L3E"][0][1]
        zero = np.zeros(L3E_N_WIN)
        out["L3E"] = dict(
            zero=_crps_vs_members(zero, np.full(L3E_N_WIN, sig_ev), members),
            pre_rate=_crps_vs_members(np.full(L3E_N_WIN, rate),
                                      np.full(L3E_N_WIN, sig_ev), members))

    if "L3S" in MENUS5[menu]:
        inst = ii["L3S"]
        ih = _i_hist(inst["t_a"])
        G = _hist_glob(world, seed)[:ih]
        fpw = int(round(L3S_WIN5 / B.CTRL_TU))
        mu_p = G[-fpw:].mean(0)
        mu_cl = G.mean(0)
        n_bl = len(G) // fpw
        blocks = np.stack([G[w * fpw:(w + 1) * fpw].mean(0)
                           for w in range(n_bl)])
        sd_bl = blocks.std(0) + 1e-6
        n_ep = len(L3S_EPOCHS5)
        members = legs_all["L3S"][0][1]
        out["L3S"] = dict(
            climatology=_crps_vs_members(np.tile(mu_cl, (n_ep, 1, 1)),
                                         np.tile(sd_bl, (n_ep, 1, 1)),
                                         members),
            persistence=_crps_vs_members(np.tile(mu_p, (n_ep, 1, 1)),
                                         np.tile(sd_bl, (n_ep, 1, 1)),
                                         members))

    for cid in ("L4", "L4D"):
        ih = _i_hist(ii[cid]["t_a"])
        Bh = _hist_dev(world, seed, 1)[:ih]
        mu_c, sd_c = Bh[:-1].mean(0), Bh[:-1].std(0) + 1e-6
        last = Bh[-1]
        legs = legs_all[cid]
        n = len(ii[cid]["lags"])
        members = legs[0][1]
        out[cid] = dict(
            climatology=_crps_vs_members(np.tile(mu_c, (n, 1, 1)),
                                         np.tile(sd_c, (n, 1, 1)), members),
            persistence=_crps_vs_members(np.tile(last, (n, 1, 1)),
                                         np.tile(sd_c, (n, 1, 1)), members))
    return out


def score_episode5(world: str, seed: int, menu: str, subs: dict) -> dict:
    """subs: instance family (or id) -> payload JSON. Returns the mean-skill
    reward (unsubmitted = -1), per-instance skill + raw CRPS (logged
    verbatim, Q5a), the ladder table, and the revealed instance parameters
    (post-episode report data)."""
    shapes = payload_shapes5(world, seed, menu)
    ladder = ladders5(world, seed, menu)
    legs_all = truth_legs(world, seed, menu)
    ii = instances5(world, seed, menu)
    detail = dict(
        ladders={k: {kk: round(vv, 6) for kk, vv in v.items()}
                 for k, v in ladder.items()},
        instances=json.loads(json.dumps(ii)),
    )
    skills = {}
    for cid in MENUS5[menu]:
        js = (subs.get(cid, "") or subs.get(f"{cid}@i1", "")) or ""
        if not js:
            skills[cid] = -1.0
            detail[f"{cid.lower()}_error"] = "not submitted"
            continue
        parsed, why = B._parse_payload(js, shapes[cid])
        if parsed is None:
            skills[cid] = -1.0
            detail[f"{cid.lower()}_error"] = why
            continue
        mu, sig = parsed
        legs = legs_all[cid]
        if len(legs) > 1:
            crps = _crps_legged(legs, mu, sig)
            detail[f"{cid.lower()}_crps_per_leg"] = {
                lbl: round(_crps_vs_members(mu[j], sig[j], mem), 6)
                for j, (lbl, mem) in enumerate(legs)}
        else:
            crps = _crps_vs_members(mu, sig, legs[0][1])
        best = min(ladder[cid].values())
        skills[cid] = float(np.clip(1.0 - crps / max(best, 1e-12),
                                    -1.0, 1.0))
        detail[f"{cid.lower()}_crps"] = round(crps, 6)
        detail[f"{cid.lower()}_ratio_vs_ref"] = round(
            crps / max(best, 1e-12), 4)
    reward = float(np.mean([skills[c] for c in MENUS5[menu]]))
    detail["skills"] = {k: round(v, 4) for k, v in skills.items()}
    return dict(reward_skill=reward, skills=skills, detail=detail)


def ladder_member_sensitivity(world: str, seed: int, menu: str) -> dict:
    """Q3 build-time variance check: relative move of the best-rung CRPS
    when each ensemble is halved (report-only; raise n_truth if > ~0.02)."""
    ii = instances5(world, seed, menu)
    legs_all = truth_legs(world, seed, menu)
    ladder_full = ladders5(world, seed, menu)
    out = {}
    for cid in ens_cids(menu):
        legs = legs_all[cid]
        halves = [(lbl, mem[:max(len(mem) // 2, 1)]) for lbl, mem in legs]
        # rebuild the best rung on halved members via the same estimators:
        # cheap proxy — rescore the BEST full-rung mu/sig is not stored, so
        # compare best-rung CRPS by re-running ladders on a halved view is
        # heavy; instead report the member-mean CRPS shift of a fixed
        # climatology forecast (dominant noise term is the member draw).
        ih = _i_hist(ii[cid]["t_a"])
        dev_idx = ii[cid].get("device", 1 if cid in ("L4", "L4D") else 0)
        if cid == "L3S":
            G = _hist_glob(world, seed)[:ih]
            mu_c = np.tile(G.mean(0), (len(L3S_EPOCHS5), 1, 1))
            sd_c = np.tile(G.std(0) + 1e-6, (len(L3S_EPOCHS5), 1, 1))
        elif cid == "L3E":
            mu_c = np.zeros(L3E_N_WIN)
            sd_c = np.full(L3E_N_WIN, 1.0)
        else:
            H = _hist_dev(world, seed, dev_idx)[:ih]
            n = len(legs) if cid == "L3F" else len(ii[cid]["lags"])
            mu1, sd1 = H[:-1].mean(0), H[:-1].std(0) + 1e-6
            if cid == "L3F":
                mu_c, sd_c = [mu1] * n, [sd1] * n
            else:
                mu_c = np.tile(mu1, (n, 1, 1))
                sd_c = np.tile(sd1, (n, 1, 1))
        if cid == "L3F":
            full = _crps_legged(legs, mu_c, sd_c)
            half = _crps_legged(halves, mu_c, sd_c)
        else:
            full = _crps_vs_members(mu_c, sd_c, legs[0][1])
            half = _crps_vs_members(mu_c, sd_c, halves[0][1])
        out[cid] = dict(full=round(full, 6), half=round(half, 6),
                        rel_move=round(abs(half - full) / max(full, 1e-12),
                                       4))
    _ = ladder_full
    return out
