"""physim.blobround2 — BLOB round-2 contract system (clean-slate L1-L4).

EVALUATOR-SIDE. Implements TRACKA_CLEANSLATE_EVAL.md Parts 1-3 for worlds
E1r3 (p4g2_044) + E2 (p6g8_033), difficulty tags BLOB2-E1 / BLOB2-E2:

  L1  pose-targeted prediction (NEW): at span end the harness executes K=3
      announced adjust command sequences on forks, each from device 0's t=0
      configuration; the agent predicts the stream vector reported after the
      final command of each sequence. Prices actuator calibration + local
      spatial modeling without disclosing actuator semantics (commands are
      opaque [u1,u2,u3] lists). Forks are passive (no injection), so truth
      == the cached main line sampled at the walked pose (replay==live was
      A0-gated); sequences are wall-safe by construction.
  L2  hidden-sensor nowcast (NEW): the harness owns ONE additional sensor
      cluster (13 slots, same ports) not among the agent's devices; at span
      end the agent predicts its current reading vector. Prices spatial
      world-modeling. Zero pose language in all announced text.
  L3F multi-horizon forecast: device-0 streams at t=0 configuration,
      H = 5/25/100/400 tu on E1 (predictability transition); E2 swaps the
      H=5 leg out (H = 25/100/400).
  L3E event-rate forecast (E1 menu only): as round-1 P2 (16 x 50tu windows).
  L3S slow-observable forecast (E2 menu only): per-port global mean+var
      averaged over the 200tu windows ending at T0+400 and T0+800.
  L4  injection response: announced amp-3 emission, 6 announced lags
      (slimmed from 13), device-1 streams at t=0 configuration.
  L4D dose-response (NEW): agent submits a response TABLE over an announced
      amp grid (0.30/0.45/0.60/0.75/0.90) at 3 announced lags; scored by
      CRPS at ONE amp drawn secretly from [0.3, 0.9] (linear interpolation
      of the agent's table at the drawn amp). Truth = a live replica at the
      drawn amp (cached per (world, seed) after first computation). Tests
      law-learning vs point-matching.

SKILL SCORING: per contract, an evaluator-side baseline ladder is computed
at scoring time from cached truth (climatology / persistence / AR(2), all
pose-ignorant, full-rate pre-T0 information; sigmas from horizon backtests).
  skill = clip(1 - CRPS_agent / CRPS_best_baseline, -1, +1)
Unsubmitted contracts score -1 (unpriced capabilities go unexercised).
Rollout reward = mean skill over the world's menu. The per-world baseline
table is published in the results json (agents never see it; reports do).

MENUS (world-adaptive, Part 2): E1 = L1 L2 L3F L3E L4 L4D;
E2 = L1 L2 L3F(no H5) L3S L4 L4D (blob-identity/event contracts off-menu
per the A0 caveats). Menu selection uses evaluator-side phenomenology only.
"""

from __future__ import annotations

import hashlib
import json
from functools import lru_cache

import numpy as np

from physim import blobcore as B

# ------------------------------------------------------------------ config
MENUS = dict(
    E1=("L1", "L2", "L3F", "L3E", "L4", "L4D"),
    E2=("L1", "L2", "L3F", "L3S", "L4", "L4D"),
)
LOCK_AT_INJECT = ("L1", "L2", "L3F", "L3E", "L3S")   # forecasts issued at T0

L3F_H = dict(E1=(5.0, 25.0, 100.0, 400.0), E2=(25.0, 100.0, 400.0))
L3S_EPOCHS = (400.0, 800.0)          # windows END at T0+400 / T0+800
L3S_WIN = 200.0
L4_LAGS = (10.0, 25.0, 50.0, 100.0, 175.0, 250.0)
L4D_AMPS = (0.30, 0.45, 0.60, 0.75, 0.90)
L4D_LAGS = (25.0, 75.0, 150.0)
K_SEQ = 3
KH = 13                               # hidden-sensor slots (square-13)

EPISODES2 = {
    "BLOB2-E1": dict(world="p4g2_044", seeds=(928, 929, 930), menu="E1"),
    "BLOB2-E2": dict(world="p6g8_033", seeds=(942, 943, 944), menu="E2"),
}


def episode_cfg2(difficulty: str, seed_idx: int) -> dict:
    ep = EPISODES2[difficulty]
    return dict(world=ep["world"], seed=ep["seeds"][seed_idx % 3],
                menu=ep["menu"])


def _rng(wk: str, salt: str) -> np.random.Generator:
    h = int(hashlib.sha256((wk + "|" + salt).encode()).hexdigest()[:16], 16)
    return np.random.default_rng(h)


# ------------------------------------------------------- round-2 secrets
@lru_cache(maxsize=8)
def l1_sequences(world: str, seed: int) -> tuple:
    """K=3 announced command sequences (each: one u repeated n steps).
    Wall-safe by construction: |dlog| per sequence <= 0.6 from dilation 1.0
    (bounds 0.5..3.0). Returns tuple of dicts(u=[u1,u2,u3], steps=n)."""
    rng = _rng(B.world_key(world, seed), "l1_seq_v1")
    seqs = []
    # seq 0: pure u1; seq 1: pure u2 (magnitudes/signs drawn)
    for ch in (0, 1):
        u = [0.0, 0.0, 0.0]
        u[ch] = float(rng.choice([-1, 1]) * rng.uniform(0.4, 0.8))
        seqs.append(dict(u=[round(x, 3) for x in u],
                         steps=int(rng.integers(2, 4))))
    # seq 2: mixed translation + small dilation component
    n3 = int(rng.integers(2, 4))
    u3 = float(rng.choice([-1, 1]) * rng.uniform(0.1, 0.6 / n3 - 1e-6))
    u = [float(rng.uniform(-0.5, 0.5)), float(rng.uniform(-0.5, 0.5)), u3]
    seqs.append(dict(u=[round(x, 3) for x in u], steps=n3))
    return tuple(seqs)


@lru_cache(maxsize=8)
def hidden_device(world: str, seed: int):
    """The harness-owned nowcast sensor: square-13 at a secret fixed pose
    between the roster devices (torus midpoint + jitter), own secret
    rotation/reflection/node order. NEVER surfaced to agents beyond slot
    and port counts."""
    sec = B.get_secrets(world, seed)
    c = B.get_cached(world, seed)
    L = c.meta["L"]
    a = np.asarray(sec["devices"][B.DEV_A]["center"], float)
    b = np.asarray(sec["devices"][B.DEV_B]["center"], float)
    mid = (a + 0.5 * ((b - a + L / 2) % L - L / 2)) % L
    rng = _rng(B.world_key(world, seed), "hidden_dev_v1")
    ang = rng.uniform(0, 2 * np.pi)
    r = rng.uniform(0, 5.0)
    center = (mid + r * np.array([np.sin(ang), np.cos(ang)])) % L
    dev = B.agdev.ProbeDevice(
        dev_id=99, lattice="square", n_rings=3, base_ds=3.5,
        center=center.tolist(), L=L,
        secret_rot=float(rng.uniform(0, 2 * np.pi)),
        reflect=bool(rng.integers(2)),
        motion_theta=0.0, motion_reflect=False,
        node_perm=rng.permutation(13).tolist())
    return dev


@lru_cache(maxsize=8)
def dose_amp(world: str, seed: int) -> float:
    """The secret scored amplitude, drawn once per (world, seed)."""
    rng = _rng(B.world_key(world, seed), "dose_amp_v1")
    return float(rng.uniform(0.3, 0.9))


# ------------------------------------------------------------------ truths
def _walked_device(world: str, seed: int, seq: dict):
    """Device 0 after executing one announced sequence from its t=0 pose."""
    dev = B.make_device(world, seed, B.DEV_A)
    M = B.adjust_mix(B.world_key(world, seed))
    u = np.asarray(seq["u"], float)
    d = M @ u
    for _ in range(int(seq["steps"])):
        dev.center = (dev.center + d[:2]) % dev.L
        dev.dilation = float(np.clip(dev.dilation * np.exp(d[2]),
                                     *dev.dil_bounds))
    return dev


@lru_cache(maxsize=8)
def truth_l1(world: str, seed: int) -> np.ndarray:
    """(K, nf, kA): device-0 streams at T0+steps after each sequence.
    Forks are passive => truth from the cached main-line... but the fork
    starts AT T0 (the span end). The sequence takes `steps` control steps,
    so the read lands at frame N_STEPS_MAIN + steps."""
    out = []
    for seq in l1_sequences(world, seed):
        dev = _walked_device(world, seed, seq)
        i = B.N_STEPS_MAIN + int(seq["steps"])
        out.append(B.sample_at(world, seed, i, dev))
    return np.stack(out)


@lru_cache(maxsize=8)
def truth_l2(world: str, seed: int) -> np.ndarray:
    """(nf, KH): hidden-sensor reading vector at T0."""
    dev = hidden_device(world, seed)
    return B.sample_at(world, seed, B.N_STEPS_MAIN, dev)


@lru_cache(maxsize=8)
def truth_l3f(world: str, seed: int, menu: str) -> np.ndarray:
    """(nH, nf, kA): device-0 streams at t=0 config, horizons per menu."""
    devA = B.make_device(world, seed, B.DEV_A)
    out = []
    for H in L3F_H[menu]:
        i = B.N_STEPS_MAIN + int(round(H / B.CTRL_TU))
        out.append(B.sample_at(world, seed, i, devA))
    return np.stack(out)


@lru_cache(maxsize=8)
def truth_l3s(world: str, seed: int) -> np.ndarray:
    """(n_epochs, nf, 2): per-port global (mean, var) averaged over the
    200tu window ending at T0+400 and T0+800. Needs cached frames beyond
    2500tu? T0+800 = 2500 exactly: window (2300, 2500] — inside the cache."""
    c = B.get_cached(world, seed)
    perm = np.asarray(B.get_secrets(world, seed)["port_perm"], int)
    fpw = int(round(L3S_WIN / B.CTRL_TU))
    out = []
    for ep in L3S_EPOCHS:
        i1 = B.N_STEPS_MAIN + int(round(ep / B.CTRL_TU))
        i0 = i1 - fpw + 1
        gm, gv = [], []
        for i in range(i0, i1 + 1):
            f = c.fields_at(i)[perm]
            gm.append(f.mean(axis=(1, 2)))
            gv.append(f.var(axis=(1, 2)))
        out.append(np.stack([np.mean(gm, axis=0), np.mean(gv, axis=0)],
                            axis=1))
    return np.stack(out)                       # (2, nf, 2)


@lru_cache(maxsize=8)
def truth_l4(world: str, seed: int) -> np.ndarray:
    """(n_lags, nf, kB): announced-branch truth at the slimmed lag set."""
    brz, _ = B.get_branches(world, seed)
    perm = np.asarray(B.get_secrets(world, seed)["port_perm"], int)
    devB = B.make_device(world, seed, B.DEV_B)
    c = B.get_cached(world, seed)
    fr = brz["announced"]
    out = []
    for lag in L4_LAGS:
        i = int(round(lag / B.CTRL_TU))
        out.append(devB.sample(fr[i].astype(np.float32)[perm], c.meta["dx"]))
    return np.stack(out)


import os as _os

_DOSE_CACHE_DIR = _os.path.join(B.CACHE_DIR, "round2")


def _dose_path(world: str, seed: int) -> str:
    return _os.path.join(_DOSE_CACHE_DIR,
                         f"{world}_s{seed}_dose.npz")


@lru_cache(maxsize=8)
def truth_l4d(world: str, seed: int) -> np.ndarray:
    """(n_dose_lags, nf, kB): live replica at the secret drawn amp on the
    announced port, sampled at device B (t=0 config). Computed once per
    (world, seed) and cached on disk (~2.5 min live sim per build)."""
    path = _dose_path(world, seed)
    amp = dose_amp(world, seed)
    if _os.path.exists(path):
        z = np.load(path, allow_pickle=False)
        if abs(float(z["amp"]) - amp) < 1e-12:
            return z["truth"]
    cc = B.contracts(world, seed)["private"]
    n_ctrl = int(round(max(L4D_LAGS) / B.CTRL_TU))
    frames = B.replica_frames(world, seed, cc["ann_port"], amp,
                              B.ANN_DUR, n_ctrl)
    perm = np.asarray(B.get_secrets(world, seed)["port_perm"], int)
    devB = B.make_device(world, seed, B.DEV_B)
    dx = B.get_cached(world, seed).meta["dx"]
    out = []
    for lag in L4D_LAGS:
        i = int(round(lag / B.CTRL_TU))
        out.append(devB.sample(frames[i][perm], dx))
    truth = np.stack(out)
    _os.makedirs(_DOSE_CACHE_DIR, exist_ok=True)
    np.savez_compressed(path, truth=truth, amp=amp)
    return truth


# --------------------------------------------------------------- contracts
@lru_cache(maxsize=8)
def contracts2(world: str, seed: int, menu: str) -> dict:
    """Announced round-2 contract set. All text barrier-audited (no pose,
    location, or actuator-semantics language)."""
    cc1 = B.contracts(world, seed)
    nf = cc1["private"]["nf"]
    kA, kB = cc1["private"]["kA"], cc1["private"]["kB"]
    pub = {}
    pub["L1"] = dict(
        device=0, sequences=[dict(u=s["u"], steps=s["steps"])
                             for s in l1_sequences(world, seed)],
        ports=nf, slots=kA,
        statistic=("for each command sequence: the harness starts a fresh "
                   "fork at the end of the span, applies the sequence to "
                   "device 0 (from its t=0 configuration, no emission), "
                   "then reads it once; predict that reading"))
    pub["L2"] = dict(
        ports=nf, slots=KH,
        statistic=("one additional fixed sensor cluster of this many slots "
                   "reports the same ports; predict its reading vector at "
                   "the end of the span (no emission)"))
    pub["L3F"] = dict(
        device=0, horizons=[int(h) for h in L3F_H[menu]], ports=nf,
        slots=kA,
        statistic=("device 0's streams in its t=0 configuration at each "
                   "horizon after the span ends, no emission"))
    if "L3E" in MENUS[menu]:
        pub["L3E"] = dict(cc1["public"]["P2"])
    if "L3S" in MENUS[menu]:
        pub["L3S"] = dict(
            epochs=[int(e) for e in L3S_EPOCHS], window_tu=int(L3S_WIN),
            ports=nf,
            statistic=("the per-port global mean and variance (the free "
                       "aggregate stream), each averaged over the "
                       "window ending at the stated time after the span "
                       "ends, no emission; payload mean shape "
                       "[epochs][ports][2] with [.,.,0]=mean, [.,.,1]="
                       "variance"))
    pub["L4"] = dict(
        device=1, port=cc1["public"]["P3"]["port"], amp=B.ANN_AMP,
        dur_tu=int(B.ANN_DUR), lags=[int(x) for x in L4_LAGS],
        ports=nf, slots=kB,
        statistic=("the announced emission runs from the span end on the "
                   "fixed emission channel; predict device 1's streams in "
                   "its t=0 configuration at each lag"))
    pub["L4D"] = dict(
        device=1, port=cc1["public"]["P3"]["port"],
        amps=[float(a) for a in L4D_AMPS], dur_tu=int(B.ANN_DUR),
        lags=[int(x) for x in L4D_LAGS], ports=nf, slots=kB,
        statistic=("the harness will run ONE more emission at an "
                   "undisclosed amp inside the listed amps' span (same "
                   "port, same dur); submit your predicted response TABLE "
                   "over the listed amps — mean shape [amps][lags][ports]"
                   "[slots] — and it is scored at the drawn amp by "
                   "interpolating your table linearly in amp"))
    return dict(public=dict(menu=list(MENUS[menu]), contracts=pub),
                private=dict(nf=nf, kA=kA, kB=kB))


def payload_shapes2(world: str, seed: int, menu: str) -> dict:
    cc = contracts2(world, seed, menu)["private"]
    nf, kA, kB = cc["nf"], cc["kA"], cc["kB"]
    shapes = dict(
        L1=(K_SEQ, nf, kA),
        L2=(nf, KH),
        L3F=(len(L3F_H[menu]), nf, kA),
        L4=(len(L4_LAGS), nf, kB),
        L4D=(len(L4D_AMPS), len(L4D_LAGS), nf, kB),
    )
    if "L3E" in MENUS[menu]:
        shapes["L3E"] = (int(round((B.T_EP - B.T0) / B.P2_WIN)),)
    if "L3S" in MENUS[menu]:
        shapes["L3S"] = (len(L3S_EPOCHS), nf, 2)
    return shapes


# ---------------------------------------------------------- baseline ladder
def _ar2_mu_sig(S: np.ndarray, nsteps: int, n_origins: int = 24):
    """AR(2) per-channel forecast nsteps ahead from the end of S (T, C),
    with backtested per-channel sigma at that horizon."""
    import refpipes as R
    mu = R._ar2_forecast(S, nsteps)
    errs = []
    T = len(S)
    origins = np.linspace(max(8, T - 120), T - nsteps - 1, n_origins)
    for o in origins.astype(int):
        if o < 8 or o + nsteps >= T:
            continue
        pred = R._ar2_forecast(S[:o], nsteps)
        errs.append(S[o + nsteps - 1] - pred)
    sig = (np.std(np.stack(errs), axis=0) + 1e-3) if errs else \
        (S.std(axis=0) + 1e-3)
    return mu, sig


@lru_cache(maxsize=8)
def _preT0_full_A(world, seed):
    devA = B.make_device(world, seed, B.DEV_A)
    return np.stack([B.sample_at(world, seed, i, devA)
                     for i in range(1, B.N_STEPS_MAIN + 1)])


@lru_cache(maxsize=8)
def _preT0_full_B(world, seed):
    devB = B.make_device(world, seed, B.DEV_B)
    return np.stack([B.sample_at(world, seed, i, devB)
                     for i in range(1, B.N_STEPS_MAIN + 1)])


@lru_cache(maxsize=8)
def _preT0_glob(world, seed):
    """(T, nf, 2) global mean/var stream up to T0 (the free aggregate)."""
    return np.stack([B.global_stats(world, seed, i)
                     for i in range(1, B.N_STEPS_MAIN + 1)])


def _crps_of(mu, sig, y):
    return float(B.gauss_crps(mu, sig, y).mean())


@lru_cache(maxsize=8)
def baselines2(world: str, seed: int, menu: str) -> dict:
    """The published ladder: per contract, CRPS of climatology / persistence
    / AR(2) (where sensible). All pose-ignorant, full-rate pre-T0 info."""
    out = {}
    A = _preT0_full_A(world, seed)               # (T, nf, kA)
    mu_c, sd_c = A[:-1].mean(0), A[:-1].std(0) + 1e-6
    last = A[-1]
    Sa = A.reshape(len(A), -1)

    # L1: pose-ignorant floors (baselines don't know the walk)
    y = truth_l1(world, seed)
    out["L1"] = dict(
        climatology=float(np.mean([_crps_of(mu_c, sd_c, y[j])
                                   for j in range(len(y))])),
        persistence=float(np.mean([_crps_of(last, sd_c, y[j])
                                   for j in range(len(y))])))

    # L2: global-aggregate floors (free stream; no spatial model)
    yh = truth_l2(world, seed)                   # (nf, KH)
    G = _preT0_glob(world, seed)                 # (T, nf, 2)
    gm_t = G[:, :, 0]
    mu_glob_c = gm_t[:-1].mean(0)
    sd_glob_c = np.sqrt(G[:-1, :, 1].mean(0) + gm_t[:-1].var(0)) + 1e-6
    mu_glob_p = gm_t[-1]
    sd_glob_p = np.sqrt(G[-1, :, 1]) + 1e-6
    out["L2"] = dict(
        climatology=_crps_of(np.repeat(mu_glob_c[:, None], KH, 1),
                             np.repeat(sd_glob_c[:, None], KH, 1), yh),
        persistence=_crps_of(np.repeat(mu_glob_p[:, None], KH, 1),
                             np.repeat(sd_glob_p[:, None], KH, 1), yh))

    # L3F: climatology / persistence / AR(2)
    y3 = truth_l3f(world, seed, menu)
    Hs = L3F_H[menu]
    cl, pe, ar = [], [], []
    for j, H in enumerate(Hs):
        n = int(round(H / B.CTRL_TU))
        cl.append(_crps_of(mu_c, sd_c, y3[j]))
        pe.append(_crps_of(last, sd_c, y3[j]))
        mu_a, sig_a = _ar2_mu_sig(Sa, n)
        ar.append(_crps_of(mu_a.reshape(A.shape[1:]),
                           sig_a.reshape(A.shape[1:]), y3[j]))
    out["L3F"] = dict(climatology=float(np.mean(cl)),
                      persistence=float(np.mean(pe)),
                      ar2=float(np.mean(ar)))

    if "L3E" in MENUS[menu]:
        y2 = B.truth_p2(world, seed)
        cc = B.contracts(world, seed)["private"]
        Aev = A[:, cc["p2_port"], :] * cc["p2_sign"]
        up = B._crossings_per_step(Aev, cc["p2_thr"])
        fpw = int(round(B.P2_WIN / B.CTRL_TU))
        n_pre = len(up) // fpw
        pre_counts = np.array([up[j * fpw:(j + 1) * fpw].sum()
                               for j in range(n_pre)], float)
        sig_ev = pre_counts.std() + 0.5
        rate = pre_counts.mean()
        out["L3E"] = dict(
            zero=_crps_of(np.zeros_like(y2), np.full_like(y2, sig_ev), y2),
            pre_rate=_crps_of(np.full_like(y2, rate),
                              np.full_like(y2, sig_ev), y2))

    if "L3S" in MENUS[menu]:
        ys = truth_l3s(world, seed)              # (2, nf, 2)
        fpw = int(round(L3S_WIN / B.CTRL_TU))
        Gw = G                                    # (T, nf, 2)
        # persistence: the 200tu window ending at T0
        mu_p = Gw[-fpw:].mean(0)
        # climatology: all pre-T0 windowed means
        mu_cl = Gw.mean(0)
        # windowed std: std of block means over disjoint pre-T0 windows
        n_bl = len(Gw) // fpw
        blocks = np.stack([Gw[j * fpw:(j + 1) * fpw].mean(0)
                           for j in range(n_bl)])
        sd_bl = blocks.std(0) + 1e-6
        out["L3S"] = dict(
            climatology=float(np.mean([_crps_of(mu_cl, sd_bl, ys[j])
                                       for j in range(len(ys))])),
            persistence=float(np.mean([_crps_of(mu_p, sd_bl, ys[j])
                                       for j in range(len(ys))])))

    # L4 / L4D: device-B floors
    Bb = _preT0_full_B(world, seed)
    mu_cb, sd_cb = Bb[:-1].mean(0), Bb[:-1].std(0) + 1e-6
    lastb = Bb[-1]
    y4 = truth_l4(world, seed)
    out["L4"] = dict(
        climatology=float(np.mean([_crps_of(mu_cb, sd_cb, y4[j])
                                   for j in range(len(y4))])),
        persistence=float(np.mean([_crps_of(lastb, sd_cb, y4[j])
                                   for j in range(len(y4))])))
    y4d = truth_l4d(world, seed)
    out["L4D"] = dict(
        climatology=float(np.mean([_crps_of(mu_cb, sd_cb, y4d[j])
                                   for j in range(len(y4d))])),
        persistence=float(np.mean([_crps_of(lastb, sd_cb, y4d[j])
                                   for j in range(len(y4d))])))
    return out


# ----------------------------------------------------------------- scoring
def _skill(crps_agent: float, ladder: dict) -> float:
    best = min(v for v in ladder.values() if v is not None)
    return float(np.clip(1.0 - crps_agent / max(best, 1e-12), -1.0, 1.0))


def score_episode2(world: str, seed: int, menu: str, subs: dict) -> dict:
    """subs: contract id -> payload JSON string (may be empty).
    Returns reward (mean skill over menu; unsubmitted = -1), per-contract
    skill/CRPS, and the published baseline table."""
    shapes = payload_shapes2(world, seed, menu)
    ladder = baselines2(world, seed, menu)
    detail = dict(baselines={k: {kk: round(vv, 6) for kk, vv in v.items()}
                             for k, v in ladder.items()})
    skills = {}
    for cid in MENUS[menu]:
        js = subs.get(cid, "") or ""
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
        if cid == "L1":
            y = truth_l1(world, seed)
        elif cid == "L2":
            y = truth_l2(world, seed)
        elif cid == "L3F":
            y = truth_l3f(world, seed, menu)
        elif cid == "L3E":
            y = B.truth_p2(world, seed)
        elif cid == "L3S":
            y = truth_l3s(world, seed)
        elif cid == "L4":
            y = truth_l4(world, seed)
        elif cid == "L4D":
            # interpolate the submitted table at the drawn amp
            amp = dose_amp(world, seed)
            grid = np.asarray(L4D_AMPS)
            j = int(np.clip(np.searchsorted(grid, amp) - 1, 0,
                            len(grid) - 2))
            w = (amp - grid[j]) / (grid[j + 1] - grid[j])
            mu = (1 - w) * mu[j] + w * mu[j + 1]
            sig = np.sqrt(((1 - w) * sig[j]) ** 2 + (w * sig[j + 1]) ** 2)
            y = truth_l4d(world, seed)
        crps = _crps_of(mu, sig, y)
        skills[cid] = _skill(crps, ladder[cid]) if cid in ladder else 0.0
        detail[f"{cid.lower()}_crps"] = round(crps, 6)
    reward = float(np.mean([skills[c] for c in MENUS[menu]]))
    detail["skills"] = {k: round(v, 4) for k, v in skills.items()}
    if "L4D" in skills and skills["L4D"] > -1.0:
        detail["l4d_drawn_amp"] = round(dose_amp(world, seed), 4)
    return dict(reward_skill=reward, skills=skills, detail=detail)
