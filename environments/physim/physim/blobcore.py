"""physim.blobcore — BLOB difficulty family core (Track A round 1). EVALUATOR-SIDE.

Episode registry, cache access, contract construction, truth sampling, and
scoring for the probe-device environment on evolved worlds. Nothing in this
module is agent-visible; the agent surface is physim.servers.blob (MCP tools)
plus the prompts in physim.taskset (BLOB branch).

Design (settled in probes/blobs/l0/deepsearch/TRACKA_AGENTENV_SPEC.md and
probes/blobs/agentenv/ADEQUACY.md; round-1 config = the A0 recommendation):

  EPISODE on (world, seed) = the A0 layout, agent-driven:
    main timeline t: 0 -> T0=1700tu, 5tu control cadence, PASSIVE cache
    replay (sensors do not disturb the field; replay==live was gated at
    4.6e-4 f16 tolerance in A0 W1). Injection is NOT allowed on the main
    line. The line HARD-STOPS at T0: the contract windows (T0, 2500] are
    never agent-observable.

    REPLICAS: each inject() call forks the world from the T0 f32+RNG
    snapshot and runs LIVE for up to 250tu with the agent's injection
    (port, amp<=1.0, dur) delivered at the fixed emitter (device A's
    initial position — the same anchor as the announced protocol and the
    cached A0 branches). Replica reads are priced normally. The first
    inject() LOCKS P1'/P2 submissions (they are forecasts issued at T0
    from pre-T0 information, exactly the A0 information structure).

  CONTRACTS (fixed per (world, seed); all sensor-observable, barrier b3):
    P1' forecast — device A streams at T0+{5,15,25}tu (A0 finding F3:
        H=50-200 is skill-free; round 1 respecs to H<=25tu), no-injection
        conditioning, truth = the main cache. CRPS.
    P2 events — upward-crossing counts per 50tu window over (T0, 2500]
        (16 windows) on device A at its starting pose, (port, thr, sign)
        announced by the A0 rule (highest pre-T0 crossing rate).
        MAE vs truth (CRPS-graded reward).
    P3 response (flagship) — the announced injection (amp 3.0, 10tu,
        announced port) runs from T0; predict device B streams at 13
        announced lags over (T0, T0+250]. Truth = the cached A0
        "announced" branch sampled at device B's home pose. CRPS.

  BUDGETS (2x A0 baseline tier; the F1 steep region is 1x-4x):
    sensor 40000 node-tu (duty ~0.5 of full for the 32-node pair),
    motion 1200 cu, injection 120 amp-tu at STEEP pricing:
        price(amp) = amp * (1 + 4*max(0, amp-0.5))   per tu
    (the A0 pricing note: at amp 3 the response is a free beacon, z~600+;
    the cap amp<=1.0 + convex pricing makes response calibration a real
    extrapolation problem).

  Scoring rewards skill over scripted baselines computed HERE at score
  time from the same caches (persistence/climatology for P1'/P3; the
  better of zero / pre-T0-mean-rate for P2).
  accuracy = 0.5*P3 + 0.3*P2 + 0.2*P1".

Cache + agentenv reuse: this module imports probes/blobs/agentenv/device.py
(ProbeDevice, CachedRun, step_chunk, world_secrets — NOT reimplemented) via a
sys.path bootstrap, and reads the A0 caches (11 GB, gitignored, built by
adequacy.py). Round 1 runs from a repo checkout with subprocess runtimes.
Env overrides: PHYSIM_AGENTENV_DIR (agentenv module dir), PHYSIM_BLOB_CACHE
(cache dir).
"""

from __future__ import annotations

import json
import os
import sys
from functools import lru_cache

import numpy as np

# --------------------------------------------------------------- bootstrap
_HERE = os.path.dirname(os.path.abspath(__file__))


def _find_agentenv() -> str:
    cand = os.environ.get("PHYSIM_AGENTENV_DIR")
    if cand and os.path.exists(os.path.join(cand, "device.py")):
        return cand
    # installed editable from a repo checkout: environments/physim/physim
    up = os.path.normpath(os.path.join(_HERE, "..", "..", ".."))
    cand = os.path.join(up, "probes", "blobs", "agentenv")
    if os.path.exists(os.path.join(cand, "device.py")):
        return cand
    raise RuntimeError(
        "BLOB family needs probes/blobs/agentenv (device.py) from the physim "
        "repo checkout; set PHYSIM_AGENTENV_DIR")


AGENTENV = _find_agentenv()
if AGENTENV not in sys.path:
    sys.path.insert(0, AGENTENV)

import device as agdev  # noqa: E402  (agentenv module, path-injected above)

CTRL_TU = agdev.CTRL_TU               # 5.0
MAX_STEP = agdev.MAX_STEP             # 1.5

CACHE_DIR = os.environ.get(
    "PHYSIM_BLOB_CACHE", os.path.join(AGENTENV, "cache"))
BLOBDATA = os.path.join(_HERE, "blobdata")

# ---------------------------------------------------------------- registry
# Roster ORDER + world_key MUST match adequacy.py (ROSTERS["r2"], world_key)
# so device secrets and the cached injection branches are reused verbatim:
# dev0 = square-13 (device A: contract anchor + emitter home),
# dev1 = hex-19    (device B: the stronger instrument, P3 witness).
ROSTER = [dict(lattice="square", n_rings=3, base_ds=3.5),
          dict(lattice="hex", n_rings=3, base_ds=3.0)]
DEV_A, DEV_B = 0, 1

T_EP = 2500.0
T0 = 1700.0
T_REPLICA = 250.0
N_STEPS_MAIN = int(round(T0 / CTRL_TU))          # 340
N_STEPS_EP = int(round(T_EP / CTRL_TU))          # 500
ANN_AMP, ANN_DUR = 3.0, 10.0
P1_HORIZONS = (5.0, 15.0, 25.0)
P2_WIN = 50.0
P3_LAGS = (5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0,
           75.0, 100.0, 150.0, 200.0, 250.0)
AMP_CAP = 1.0
AMP_MIN = 0.05
DUR_CAP = 50.0
MAX_REPLICAS = 12
SIGMA_MIN = 1e-4

EPISODES = {
    "BLOB-E1r3": dict(world="p4g2_044", seeds=(928, 929, 930), gated=False),
    "BLOB-E1r2": dict(world="p4g2_044", seeds=(928, 929, 930), gated=True,
                      why="superseded by BLOB-E1r3 (mixed-control variant, "
                          "retired before any scored rollouts were kept)"),
    "BLOB-E1": dict(world="p4g2_044", seeds=(928, 929, 930), gated=True,
                    why="superseded (R2/R3 control-surface revisions: "
                        "probe_adjust replaces move/dilate)"),
    "BLOB-E2": dict(world="p6g8_033", seeds=(942, 943, 944), gated=True,
                    why="A0 verdict: E2 contracts need the round-2 respec"),
    "BLOB-E3": dict(world="p3g9_022", seeds=(921, 922, 923), gated=True,
                    why="A0 verdict: E3 contracts need the round-2 respec"),
}

# R2 (TRACKA_R2_CONTROLS.md): 'adjust' = the merged motion+dilation pool
# (round 1 already funded both from motion's 1200; the merge keeps the total).
BUDGETS = dict(sensor=40000.0, adjust=1200.0, injection=120.0)

W_P1, W_P2, W_P3 = 0.2, 0.3, 0.5


def inj_price(amp: float) -> float:
    """Steep injection pricing (amp-tu per tu of duration)."""
    a = abs(float(amp))
    return a * (1.0 + 4.0 * max(0.0, a - 0.5))


def episode_cfg(difficulty: str, seed_idx: int) -> dict:
    ep = EPISODES[difficulty]
    if ep["gated"]:
        raise ValueError(
            f"{difficulty} is registered but GATED "
            f"({ep.get('why', 'no reason recorded')})")
    seed = ep["seeds"][seed_idx % len(ep["seeds"])]
    return dict(world=ep["world"], seed=seed)


def world_key(world: str, seed: int) -> str:
    return f"{world}|s{seed}|A0"        # MUST match adequacy.py


# ------------------------------------------------------------------ caches
def load_genome(world: str) -> dict:
    return json.load(open(os.path.join(BLOBDATA, world + ".json")))["genome"]


def cache_paths(world: str, seed: int):
    base = os.path.join(CACHE_DIR, f"{world}_s{seed}")
    return base + ".npz", base + "_branches.npz"


@lru_cache(maxsize=3)
def get_cached(world: str, seed: int) -> agdev.CachedRun:
    main, _ = cache_paths(world, seed)
    if not os.path.exists(main):
        raise RuntimeError(
            f"missing A0 cache {main}; build it with "
            f"probes/blobs/agentenv/adequacy.py cache --world {world} "
            f"--seed {seed}")
    return agdev.CachedRun(main)


@lru_cache(maxsize=3)
def get_branches(world: str, seed: int):
    _, br = cache_paths(world, seed)
    z = np.load(br, allow_pickle=False)
    return z, json.loads(str(z["meta"]))


def adjust_mix(wk: str) -> np.ndarray:
    """R3 secret actuator map (TRACKA_R2_CONTROLS.md + R3 revision): per-
    WORLD fixed 3x3 map with PURE effects — M = P @ diag(s) up to signs,
    i.e. each anonymous channel u_i drives exactly ONE of (dy, dx,
    dlog_spacing) with a secret sign and scale; WHICH one is a secret
    permutation. No cross-mixing (R2's mixed map was retired: difficulty
    without depth). Per adjust step the pose delta is M @ u.

    Scales: translation channels in [1.0, 1.5] (the old MAX_STEP range),
    the dilation channel in [0.6, 1.0] (the old gain range). Deterministic
    in world_key via a salted hash (fresh salt: r3), independent of the A0
    secret stream."""
    import hashlib
    h = int(hashlib.sha256((wk + "|adjust_pure_v3").encode())
            .hexdigest()[:16], 16)
    rng = np.random.default_rng(h)
    perm = rng.permutation(3)           # effect row -> channel column
    signs = rng.choice([-1.0, 1.0], size=3)
    scales = np.array([rng.uniform(1.0, 1.5), rng.uniform(1.0, 1.5),
                       rng.uniform(0.6, 1.0)])  # rows: dy, dx, dlog
    M = np.zeros((3, 3))
    for row in range(3):                # row = effect, perm[row] = channel
        M[row, perm[row]] = signs[row] * scales[row]
    return M


@lru_cache(maxsize=6)
def get_secrets(world: str, seed: int) -> dict:
    c = get_cached(world, seed)
    nf = c.meta["na"] + c.meta["nc"]
    wk = world_key(world, seed)
    sec = agdev.world_secrets(wk, nf, ROSTER, c.meta["L"])
    sec["adjust_mix"] = adjust_mix(wk).tolist()   # R2 control surface
    return sec


def n_ports(world: str, seed: int) -> int:
    c = get_cached(world, seed)
    return c.meta["na"] + c.meta["nc"]


def make_device(world: str, seed: int, idx: int,
                center=None, dilation: float = 1.0) -> agdev.ProbeDevice:
    """A ProbeDevice with the cached secrets; pose overridable (agent state)."""
    c = get_cached(world, seed)
    ds = get_secrets(world, seed)["devices"][idx]
    cfg = ROSTER[idx]
    dev = agdev.ProbeDevice(
        dev_id=idx, lattice=cfg["lattice"], n_rings=cfg["n_rings"],
        base_ds=cfg["base_ds"], center=ds["center"], L=c.meta["L"],
        secret_rot=ds["secret_rot"], reflect=ds["reflect"],
        motion_theta=ds["motion_theta"], motion_reflect=ds["motion_reflect"],
        node_perm=ds["node_perm"])
    if center is not None:
        dev.center = np.asarray(center, float)
    dev.dilation = float(dilation)
    return dev


def sample_at(world: str, seed: int, i_ctrl: int,
              dev: agdev.ProbeDevice) -> np.ndarray:
    """Truth streams (nf, k) at cached frame i, stream order, port order."""
    c = get_cached(world, seed)
    perm = np.asarray(get_secrets(world, seed)["port_perm"], int)
    return dev.sample(c.fields_at(i_ctrl)[perm], c.meta["dx"])


def global_stats(world: str, seed: int, i_ctrl: int) -> np.ndarray:
    c = get_cached(world, seed)
    perm = np.asarray(get_secrets(world, seed)["port_perm"], int)
    f = c.fields_at(i_ctrl)[perm]
    return np.stack([f.mean(axis=(1, 2)), f.var(axis=(1, 2))], axis=1)


def _bimodality(x: np.ndarray) -> float:
    v = np.asarray(x, float).ravel()
    v = v - v.mean()
    s = v.std()
    if s < 1e-12:
        return 0.0
    z = v / s
    m3 = float(np.mean(z ** 3))
    m4 = float(np.mean(z ** 4))
    n = len(v)
    return (m3 ** 2 + 1) / (m4 + 3 * (n - 1) ** 2 / ((n - 2) * (n - 3) + 1e-9))


# --------------------------------------------------------------- contracts
def _crossings_per_step(A: np.ndarray, thr: float) -> np.ndarray:
    """Upward crossings summed over slots, per frame step. A: (T, k)."""
    x = A > thr
    return (~x[:-1] & x[1:]).sum(axis=1)


@lru_cache(maxsize=6)
def contracts(world: str, seed: int) -> dict:
    """Announced contract parameters, fixed per (world, seed).

    public: safe to show agents (indices, thresholds, times, counts).
    private: evaluator-only extras. Announce rule for P2 = the A0 score_p2
    rule (sparse-excursion port with the highest pre-T0 crossing rate at
    device A's home pose; skew-oriented sign).
    """
    nf = n_ports(world, seed)
    devA = make_device(world, seed, DEV_A)
    i0 = N_STEPS_MAIN
    full = np.stack([sample_at(world, seed, i, devA)
                     for i in range(1, i0)])           # (T, nf, k) pre-T0
    best, p_ev, sign, thr = -1e9, 0, 1.0, 0.0
    for pt in range(nf):
        A = full[:, pt, :]
        if A.std() < 1e-9:
            continue
        z = (A - A.mean()) / A.std()
        sg = 1.0 if float(np.mean(z ** 3)) >= 0 else -1.0
        As = A * sg
        lo, hi = np.percentile(As, [5, 99])
        th = 0.5 * (lo + hi)
        of = float((As > th).mean())
        if of <= 1e-4 or of > 0.55:
            continue
        rate = _crossings_per_step(As, th).sum() / max(len(As) - 1, 1)
        sc = rate + 0.01 * _bimodality(A)
        if sc > best:
            best, p_ev, sign, thr = sc, pt, sg, th
    # P3 announced port = the anonymous port mapping to field 0 (the cached
    # branches inject field 0; adequacy build_cache does the same).
    perm = np.asarray(get_secrets(world, seed)["port_perm"], int)
    ann_port = int(np.where(perm == 0)[0][0])
    kA = devA.k
    kB = make_device(world, seed, DEV_B).k
    n_win = int(round((T_EP - T0) / P2_WIN))
    return dict(
        public=dict(
            P1=dict(device=0, horizons=[int(h) for h in P1_HORIZONS],
                    ports=nf, slots=kA,
                    statistic="stream values with the device at its t=0 "
                              "configuration, no injection, at each horizon "
                              "after the exploration span ends"),
            P2=dict(device=0, port=p_ev, thr=float(round(float(thr), 6)),
                    sign=int(sign), window_tu=int(P2_WIN), n_windows=n_win,
                    statistic="count of upward crossings of sign*value "
                              "above thr, summed over the slots of the "
                              "device at its t=0 configuration, per "
                              "consecutive window after the span ends, "
                              "no injection"),
            P3=dict(device=1, port=ann_port, amp=ANN_AMP,
                    dur_tu=int(ANN_DUR),
                    lags=[int(x) for x in P3_LAGS], ports=nf, slots=kB,
                    statistic="stream values with the device at its t=0 "
                              "configuration at each lag after the announced "
                              "emission (amp, dur on the announced port) "
                              "starts at the end of the span"),
        ),
        private=dict(p2_port=p_ev, p2_sign=float(sign), p2_thr=float(thr),
                     ann_field=0, ann_port=ann_port, kA=kA, kB=kB, nf=nf),
    )


# ------------------------------------------------------------------- truth
@lru_cache(maxsize=6)
def truth_p1(world: str, seed: int) -> np.ndarray:
    """(n_horizons, nf, kA) truth streams at device A home."""
    devA = make_device(world, seed, DEV_A)
    out = []
    for H in P1_HORIZONS:
        i = N_STEPS_MAIN + int(round(H / CTRL_TU))
        out.append(sample_at(world, seed, i, devA))
    return np.stack(out)


@lru_cache(maxsize=6)
def truth_p2(world: str, seed: int) -> np.ndarray:
    """(n_windows,) upward-crossing counts per window over (T0, T_EP]."""
    cc = contracts(world, seed)["private"]
    devA = make_device(world, seed, DEV_A)
    fut = np.stack([sample_at(world, seed, i, devA)
                    for i in range(N_STEPS_MAIN, N_STEPS_EP + 1)])
    A = fut[:, cc["p2_port"], :] * cc["p2_sign"]
    up = _crossings_per_step(A, cc["p2_thr"])          # (160,)
    fpw = int(round(P2_WIN / CTRL_TU))
    n_win = len(up) // fpw
    return np.array([up[j * fpw:(j + 1) * fpw].sum()
                     for j in range(n_win)], float)


@lru_cache(maxsize=6)
def truth_p3(world: str, seed: int) -> np.ndarray:
    """(n_lags, nf, kB) announced-branch truth at device B home."""
    brz, _ = get_branches(world, seed)
    perm = np.asarray(get_secrets(world, seed)["port_perm"], int)
    devB = make_device(world, seed, DEV_B)
    c = get_cached(world, seed)
    fr = brz["announced"]
    out = []
    for lag in P3_LAGS:
        i = int(round(lag / CTRL_TU))
        out.append(devB.sample(fr[i].astype(np.float32)[perm], c.meta["dx"]))
    return np.stack(out)


def replica_frames(world: str, seed: int, port: int, amp: float, dur: float,
                   n_ctrl: int, workers: int = 3) -> np.ndarray:
    # workers=3 matters: it reproduces the A0 branch builds bitwise (FFT
    # op order depends on the worker split; gated in test_blob_server T2).
    """LIVE replica: fork the T0 snapshot, inject (port, amp) for dur tu at
    device A's home center, return (n_ctrl+1, nf, N, N) f32 fields.
    amp=0 reproduces the cached control branch bit-path (same RNG stream)."""
    c = get_cached(world, seed)
    g = load_genome(world)
    sec = get_secrets(world, seed)
    perm = np.asarray(sec["port_perm"], int)
    inj_yx = np.asarray(sec["devices"][DEV_A]["center"], float)
    S = c.snapshot_state(g, T0, workers=workers)
    steps_per = int(round(CTRL_TU / S["dt"]))
    nf = S["na"] + S["nc"]
    N = S["N"]
    frames = np.empty((n_ctrl + 1, nf, N, N), np.float32)
    frames[0] = np.asarray(S["F"], np.float32)
    field = int(perm[int(port)])
    for i in range(1, n_ctrl + 1):
        t_rel = (i - 1) * CTRL_TU
        injs = []
        if amp > 0 and t_rel < dur - 1e-9:
            injs = [dict(field=field, y=inj_yx[0], x=inj_yx[1], amp=amp)]
        agdev.step_chunk(S, steps_per, injections=injs)
        frames[i] = np.asarray(S["F"], np.float32)
    return frames


# --------------------------------------------------------------- baselines
def gauss_crps(mu, sig, y):
    """CRPS of N(mu, sig^2) vs observation y (elementwise). sig=0 -> |err|."""
    from scipy.special import ndtr
    mu = np.asarray(mu, float)
    y = np.asarray(y, float)
    sig = np.maximum(np.asarray(sig, float), 0.0)
    err = y - mu
    out = np.abs(err).astype(float)
    pos = sig > 0
    if np.any(pos):
        zp = err[pos] / sig[pos]
        phi = np.exp(-0.5 * zp ** 2) / np.sqrt(2 * np.pi)
        out[pos] = sig[pos] * (zp * (2 * ndtr(zp) - 1) + 2 * phi
                               - 1 / np.sqrt(np.pi))
    return out


@lru_cache(maxsize=6)
def _preT0_stats_A(world: str, seed: int):
    devA = make_device(world, seed, DEV_A)
    full = np.stack([sample_at(world, seed, i, devA)
                     for i in range(1, N_STEPS_MAIN)])
    return full.mean(0), full.std(0) + 1e-6, sample_at(
        world, seed, N_STEPS_MAIN, devA)


@lru_cache(maxsize=6)
def _preT0_stats_B(world: str, seed: int):
    devB = make_device(world, seed, DEV_B)
    full = np.stack([sample_at(world, seed, i, devB)
                     for i in range(1, N_STEPS_MAIN)])
    return full.mean(0), full.std(0) + 1e-6, sample_at(
        world, seed, N_STEPS_MAIN, devB)


@lru_cache(maxsize=6)
def baselines(world: str, seed: int) -> dict:
    """Reference CRPS/MAE per contract (evaluator-side scripted nulls).
    P1/P3 ref = the better of persistence (last pre-T0 value, climatology
    sigma) and climatology (pre-T0 mean/sd). P2 ref = the better of the
    zero forecast and the constant pre-T0-rate forecast (MAE)."""
    mu_c, sd_c, last = _preT0_stats_A(world, seed)
    y1 = truth_p1(world, seed)
    p1_pers = float(np.mean([gauss_crps(last, sd_c, y1[j]).mean()
                             for j in range(len(P1_HORIZONS))]))
    p1_clim = float(np.mean([gauss_crps(mu_c, sd_c, y1[j]).mean()
                             for j in range(len(P1_HORIZONS))]))
    y2 = truth_p2(world, seed)
    cc = contracts(world, seed)["private"]
    devA = make_device(world, seed, DEV_A)
    pre = np.stack([sample_at(world, seed, i, devA)
                    for i in range(1, N_STEPS_MAIN)])
    A = pre[:, cc["p2_port"], :] * cc["p2_sign"]
    rate = _crossings_per_step(A, cc["p2_thr"]).sum() / max(len(A) - 1, 1)
    fpw = int(round(P2_WIN / CTRL_TU))
    p2_zero = float(np.abs(y2).mean())
    p2_rate = float(np.abs(y2 - rate * fpw).mean())
    mu_cB, sd_cB, lastB = _preT0_stats_B(world, seed)
    y3 = truth_p3(world, seed)
    p3_pers = float(np.mean([gauss_crps(lastB, sd_cB, y3[j]).mean()
                             for j in range(len(P3_LAGS))]))
    p3_clim = float(np.mean([gauss_crps(mu_cB, sd_cB, y3[j]).mean()
                             for j in range(len(P3_LAGS))]))
    return dict(p1_ref=min(p1_pers, p1_clim), p1_persistence=p1_pers,
                p1_climatology=p1_clim,
                p2_ref=min(p2_zero, p2_rate), p2_zero=p2_zero,
                p2_rate=p2_rate, p2_pre_rate_per_win=float(rate * fpw),
                p3_ref=min(p3_pers, p3_clim), p3_persistence=p3_pers,
                p3_climatology=p3_clim)


# ----------------------------------------------------------------- scoring
def _parse_payload(js: str, shape: tuple) -> tuple:
    """Payload {"mean": nested list, "sigma": scalar|nested} -> (mu, sig).
    Returns (None, why) on shape/parse failure."""
    try:
        d = json.loads(js)
    except (json.JSONDecodeError, TypeError):
        return None, "unparseable JSON"
    if not isinstance(d, dict) or "mean" not in d:
        return None, "payload must be an object with a 'mean' field"
    try:
        mu = np.asarray(d["mean"], float)
    except (ValueError, TypeError):
        return None, "mean is not numeric"
    if mu.shape != shape:
        return None, f"mean shape {list(mu.shape)} != required {list(shape)}"
    sig = d.get("sigma", 0.0)
    try:
        sig = np.asarray(sig, float)
    except (ValueError, TypeError):
        return None, "sigma is not numeric"
    if sig.ndim == 0:
        sig = np.full(shape, float(sig))
    elif sig.shape != shape:
        return None, f"sigma shape {list(sig.shape)} != required {list(shape)}"
    if not (np.isfinite(mu).all() and np.isfinite(sig).all()):
        return None, "non-finite values"
    return (mu, np.maximum(sig, 0.0)), None


def payload_shapes(world: str, seed: int) -> dict:
    cc = contracts(world, seed)["private"]
    n_win = int(round((T_EP - T0) / P2_WIN))
    return dict(P1=(len(P1_HORIZONS), cc["nf"], cc["kA"]),
                P2=(n_win,),
                P3=(len(P3_LAGS), cc["nf"], cc["kB"]))


def score_episode(world: str, seed: int, p1_json: str, p2_json: str,
                  p3_json: str) -> dict:
    """Final scoring: CRPS (P1/P3) and MAE (P2) vs the cached truths,
    normalized to skill over the scripted reference baselines.
    acc_X = clip01(1 - metric_agent / metric_ref); accuracy = weighted sum."""
    ref = baselines(world, seed)
    shapes = payload_shapes(world, seed)
    detail = dict(baselines={k: round(v, 6) for k, v in ref.items()})
    accs = {}
    # P1
    acc = 0.0
    if p1_json:
        parsed, why = _parse_payload(p1_json, shapes["P1"])
        if parsed is None:
            detail["p1_error"] = why
        else:
            mu, sig = parsed
            y = truth_p1(world, seed)
            crps = float(np.mean([gauss_crps(mu[j], sig[j], y[j]).mean()
                                  for j in range(len(P1_HORIZONS))]))
            acc = float(np.clip(1.0 - crps / max(ref["p1_ref"], 1e-12),
                                0.0, 1.0))
            detail["p1_crps"] = round(crps, 6)
            detail["p1_ratio_vs_ref"] = round(crps / max(ref["p1_ref"],
                                                         1e-12), 4)
    else:
        detail["p1_error"] = "not submitted"
    accs["P1"] = acc
    # P2
    acc = 0.0
    if p2_json:
        parsed, why = _parse_payload(p2_json, shapes["P2"])
        if parsed is None:
            detail["p2_error"] = why
        else:
            mu, sig = parsed
            y = truth_p2(world, seed)
            mae = float(np.abs(mu - y).mean())
            crps = float(gauss_crps(mu, sig, y).mean())
            acc = float(np.clip(1.0 - crps / max(ref["p2_ref"], 1e-12),
                                0.0, 1.0))
            detail["p2_mae"] = round(mae, 4)
            detail["p2_crps"] = round(crps, 4)
            detail["p2_true_total"] = float(y.sum())
            detail["p2_ratio_vs_ref"] = round(crps / max(ref["p2_ref"],
                                                         1e-12), 4)
    else:
        detail["p2_error"] = "not submitted"
    accs["P2"] = acc
    # P3
    acc = 0.0
    if p3_json:
        parsed, why = _parse_payload(p3_json, shapes["P3"])
        if parsed is None:
            detail["p3_error"] = why
        else:
            mu, sig = parsed
            y = truth_p3(world, seed)
            crps = float(np.mean([gauss_crps(mu[j], sig[j], y[j]).mean()
                                  for j in range(len(P3_LAGS))]))
            acc = float(np.clip(1.0 - crps / max(ref["p3_ref"], 1e-12),
                                0.0, 1.0))
            detail["p3_crps"] = round(crps, 6)
            detail["p3_ratio_vs_ref"] = round(crps / max(ref["p3_ref"],
                                                         1e-12), 4)
    else:
        detail["p3_error"] = "not submitted"
    accs["P3"] = acc
    reward = W_P1 * accs["P1"] + W_P2 * accs["P2"] + W_P3 * accs["P3"]
    detail["accs"] = {k: round(v, 4) for k, v in accs.items()}
    return dict(reward_accuracy=float(reward), accs=accs, detail=detail)
