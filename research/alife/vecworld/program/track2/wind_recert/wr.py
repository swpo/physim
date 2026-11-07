"""wr -- shared pieces of the wind recertification (track2/wind_recert).

The wind world is actuation/wind.py (imported, not changed) at background sigma_w; level 1 is
<Phi_coarse (192), Phi_objects (144)> as in vw1/fresh/closure. One run call = one tick per step.

Declared exam program mix (equal shares; every program lasts T_IN = 4 ticks from the episode start,
budget split equally over the 4 ticks; built from the state at the episode start, open loop):
  none      u = 0
  blind     a 2 x 2 block group at a uniformly random block corner (i0, j0) and a uniformly random
            direction, fixed for 4 ticks; force f = sigma_w sqrt(C / (2 T_IN)); C ~ logU[150, 700] nats
            (state-independent: the blind counterpart of 'aimed')
  aimed     actuation/programs.wind_aimed on programs.pick_target (the 2 x 2 group follows the target's
            extrapolated path), C ~ logU[150, 700] nats
  regional  actuation/programs.wind_regional (4 x 4 blocks around the target, fixed), C = 700 nats
            (the per-episode budget, EXAM class (d))
Charges are 0.5 |u|^2 / sigma_w^2 summed over ticks (wind.nats).
"""
from __future__ import annotations

import os
import sys

sys.dont_write_bytecode = True
ACT = "/home/user/evalwork/vecworld/program/track2/actuation"
if ACT not in sys.path:
    sys.path.insert(0, ACT)
import numpy as np  # noqa: E402

import wind as WD  # noqa: E402   (adds port, vw1 paths)
import programs as PG  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
RAW = os.path.join(RES, "raw")
os.makedirs(RAW, exist_ok=True)

SIGMA = 0.05
T_IN = PG.T_IN
CLASSES = ("none", "blind", "aimed", "regional")
C_LO, C_HI, C_REG = 150.0, 700.0, 700.0
HORIZONS = [1, 2, 4, 8, 16]
TB = 16                      # branch length (max horizon)
R_BR = 5                     # fresh-noise branches per test state (+ the base continuation = 6 replicates)
R_TWIN = 3                   # no-input twins per program item (same keys as program branches 0..2)

# free-run set F
F_J, F_T, F_TEST, F_CHUNK = 16, 236, (40, 100, 160, 220), 4
F_SEED = 9101
# program-mix set P
P_J, P_T, P_EP0, P_EPLEN = 16, 200, 8, 16
P_EPISODES = tuple(range(P_EP0, P_T - P_EPLEN + 1, P_EPLEN))       # 8, 24, ..., 184
P_TEST = P_EPISODES[1::2]                                          # 24, 56, ..., 184
P_SEED = 9201
# viability
V_SIGMAS, V_J, V_T, V_SEED = (0.0, 0.05, 0.1), 6, 250, 9002
V_ORACLE_TICKS, V_ORACLE_R, V_ORACLE_SEED = (100, 200), 6, 9003
BATCH = 4                    # trajectories per simulation batch (partial saves)


def log_uniform(rng, lo=C_LO, hi=C_HI):
    return float(np.exp(rng.uniform(np.log(lo), np.log(hi))))


def wind_blind(rng, C, sigma_w=SIGMA, T_in=T_IN):
    G = WD.G
    i0, j0 = (int(v) for v in rng.integers(0, G, 2))
    th = float(rng.uniform(0, 2 * np.pi))
    n = np.array([np.sin(th), np.cos(th)])
    f = sigma_w * np.sqrt(C / (2.0 * T_in))
    rows, cols = [i0, (i0 + 1) % G], [j0, (j0 + 1) % G]
    U = np.zeros((T_in, 2, G, G))
    for t in range(T_in):
        for c in range(2):
            U[t, c][np.ix_(rows, cols)] = f * n[c]
    return U.reshape(T_in, WD.NW), {"i0": i0, "j0": j0, "theta": th}


def build_program(klass, rng, table, sigma_w=SIGMA):
    """-> (U (T_IN, NW), info dict). table: the full tracker table (K, NS) at the episode start."""
    info = {"klass": klass, "C": 0.0, "target": -1, "tier": -1}
    if klass == "none":
        return np.zeros((T_IN, WD.NW)), info
    C = C_REG if klass == "regional" else log_uniform(rng)
    info["C"] = C
    if klass == "blind":
        U, extra = wind_blind(rng, C, sigma_w)
        info.update(extra)
        return U, info
    tgt, tier = PG.pick_target(np.asarray(table, float))
    if tgt is None:              # no body: fall back to a blind program of the same budget
        U, extra = wind_blind(rng, C, sigma_w)
        info.update(extra)
        info["fallback"] = "blind"
        return U, info
    info["target"], info["tier"] = int(tgt), int(tier)
    U = (PG.wind_aimed if klass == "aimed" else PG.wind_regional)(np.asarray(table, float), tgt, C, sigma_w)
    return U, info


def assign_test_classes(n, seed=9204):
    """Balanced quotas (equal shares), shuffled."""
    q = [k for k in CLASSES for _ in range(n // len(CLASSES))]
    q += list(CLASSES[: n - len(q)])
    rng = np.random.default_rng(seed)
    return [q[i] for i in rng.permutation(n)]
