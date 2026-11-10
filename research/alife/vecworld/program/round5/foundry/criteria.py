"""criteria -- declared world types, gates and the candidate score (numpy; study foundry, round 5).

Inputs are the per-draw measures of screen.measure_one (arrays with leading axis = draw). Every
threshold is a constant below; they were fixed before the GPU screen, from a CPU pilot on prior seed 1
(the GPU screen uses prior seed 2026).

Types (first rule that applies):
  invalid   a non-finite value, a negative cell, or total mass drift above 1e-9
  point     collapsed: participation ratio of the total density below PR_POINT, or a cell above SMAX
  uniform   no structure beyond the noise: cell-level contrast cv_cell below CV_UNIFORM
  frozen    the block view barely changes over 16 ticks: persistence error vp(16) below VP_FROZEN
  noisy     the block view loses half its variance to persistence error within one tick: vp(1) above VP_NOISY
  active    everything else; sub-types by the tracker:
              movers    2 <= bodies <= NB_MAX, body mass share >= BODY_FRAC, net speed >= V_NET
              bodies    2 <= bodies <= NB_MAX, body mass share >= BODY_FRAC (slower than V_NET)
              field     otherwise (waves, labyrinths, crowds, one body)
Gates (declared targets, after track1/DESIGN.md section 3):
  viable       type active
  closure      ceiling c(1) >= C1_MIN, the oracle predicts at 8 ticks (V_orc(8) <= VORC8_MAX) and the cheap
               level-1 predictor leaves an intermediate gap: GAP_MIN <= max_h [V_pred(h) - V_orc(h)] and
               c(32) <= C32_MAX (not closed forever)
  structures   sub-type movers, at least EVENTS_MIN fusions + fissions per 100 ticks and member, no kept
               overflow in the tracker
  sensitive    plug-in loss of a 10% weight neighbour at 4 ticks: PL(4) >= PL_MIN and PL(4) >= V_orc(4)
A candidate passes all four. The score ranks viable worlds (geometric mean of desirabilities in [0, 1]).
"""
from __future__ import annotations

import numpy as np

HZ = (1, 2, 4, 8, 16, 32)
PR_POINT, SMAX = 0.004, 200.0
CV_UNIFORM = 0.25
VP_FROZEN, VP_NOISY = 0.02, 1.0
NB_MIN, NB_MAX, BODY_FRAC, V_NET = 2.0, 20.0, 0.2, 0.05
C1_MIN, VORC8_MAX, GAP_MIN, C32_MAX = 0.8, 0.5, 0.1, 0.9
EVENTS_MIN = 2.0
PL_MIN = 0.01
TYPES = ("invalid", "point", "uniform", "frozen", "noisy", "active:field", "active:bodies", "active:movers")
THRESHOLDS = dict(PR_POINT=PR_POINT, SMAX=SMAX, CV_UNIFORM=CV_UNIFORM, VP_FROZEN=VP_FROZEN, VP_NOISY=VP_NOISY,
                  NB_MIN=NB_MIN, NB_MAX=NB_MAX, BODY_FRAC=BODY_FRAC, V_NET=V_NET, C1_MIN=C1_MIN,
                  VORC8_MAX=VORC8_MAX, GAP_MIN=GAP_MIN, C32_MAX=C32_MAX, EVENTS_MIN=EVENTS_MIN, PL_MIN=PL_MIN)


def _h(i_h):
    return HZ.index(i_h)


def derive(m: dict, T: int) -> dict:
    """Scalar descriptors per draw from the measures (m: dict of arrays, leading axis D)."""
    f = lambda k: np.asarray(m[k], np.float64)
    d = {}
    for k in ("finite", "mass_drift", "xmin", "smax", "pr", "moved", "cv_cell", "cv_block", "wavelength",
              "var_static", "nb_mean", "nb_std", "nb_max", "body_frac", "body_mass", "rg", "v_inst", "v_net",
              "survive", "age_mean", "mean_S", "kind_frac0"):
        d[k] = f(k)
    vc, vo, vp, vs, pl = f("v_clim"), f("v_orc"), f("v_pred"), f("v_pers"), f("pl")
    for i, h in enumerate(HZ[:vc.shape[1]]):
        d[f"vp_main{h}"] = f("vp_main")[:, i]
        d[f"v_orc{h}"], d[f"v_pred{h}"], d[f"v_pers{h}"], d[f"v_clim{h}"] = vo[:, i], vp[:, i], vs[:, i], vc[:, i]
        d[f"ceil{h}"] = f("ceil")[:, i]
        d[f"gap{h}"] = vp[:, i] - vo[:, i]
        d[f"pl{h}"] = pl[:, i]
    gaps = vp - vo
    d["gap_max"] = np.nanmax(gaps, 1)
    d["gap_argmax_h"] = np.asarray(HZ)[np.nanargmax(np.nan_to_num(gaps, nan=-1e9), 1)].astype(float)
    g = f("glob")                                   # next_uid, births, deaths, fusions, fissions over T ticks
    per100 = 100.0 / T
    d["births100"], d["deaths100"] = g[:, 1] * per100, g[:, 2] * per100
    d["fusions100"], d["fissions100"] = g[:, 3] * per100, g[:, 4] * per100
    d["events100"] = (g[:, 3] + g[:, 4]) * per100
    ov = f("ovf")
    d["ovf_raw_ticks"], d["ovf_kept_ticks"], d["raw_peak"] = ov[:, 0], ov[:, 1], ov[:, 2]
    tw = f("twin_v")
    d["twin_v1"], d["twin_v8"], d["twin_v32"] = tw[:, 0], tw[:, 7], tw[:, -1]
    with np.errstate(divide="ignore", invalid="ignore"):
        # doubling time of the replica variance between 2 and 8 ticks (ticks per doubling; inf if not growing)
        r = np.log2(np.maximum(tw[:, 7], 1e-300) / np.maximum(tw[:, 1], 1e-300)) / 6.0
        d["twin_doubling"] = np.where(r > 1e-6, 1.0 / r, np.inf)
    half = tw >= 0.5
    d["twin_half_h"] = np.where(half.any(1), half.argmax(1) + 1.0, np.inf)
    d["twin_l1_1"], d["twin_l1_32"] = f("twin_l1")[:, 0], f("twin_l1")[:, -1]
    d["theta_l1_32"] = f("theta_l1")[:, -1]
    with np.errstate(divide="ignore", invalid="ignore"):
        d["body_speed_len"] = d["v_net"] / np.maximum(2.0 * d["rg"], 1e-9)       # body lengths per tick
    return d


def classify(d: dict) -> np.ndarray:
    """Type index per draw (into TYPES)."""
    n = len(d["finite"])
    t = np.full(n, -1)
    invalid = (d["finite"] < 0.5) | (d["xmin"] < 0) | ~(d["mass_drift"] < 1e-9)
    point = (d["pr"] < PR_POINT) | (d["smax"] > SMAX)
    uniform = d["cv_cell"] < CV_UNIFORM
    frozen = d["vp_main16"] < VP_FROZEN
    noisy = d["vp_main1"] > VP_NOISY
    bodies = (d["nb_mean"] >= NB_MIN) & (d["nb_mean"] <= NB_MAX) & (d["body_frac"] >= BODY_FRAC)
    movers = bodies & (d["v_net"] >= V_NET)
    for i, cond in enumerate([invalid, point, uniform, frozen, noisy]):
        t = np.where((t < 0) & cond, i, t)
    t = np.where((t < 0) & movers, 7, t)
    t = np.where((t < 0) & bodies, 6, t)
    t = np.where(t < 0, 5, t)
    return t


def gates(d: dict, t: np.ndarray) -> dict:
    viable = t >= 5
    closure = ((d["ceil1"] >= C1_MIN) & (d["v_orc8"] <= VORC8_MAX) & (d["gap_max"] >= GAP_MIN)
               & (d["ceil32"] <= C32_MAX))
    structures = (t == 7) & (d["events100"] >= EVENTS_MIN) & (d["ovf_kept_ticks"] == 0)
    sensitive = (d["pl4"] >= PL_MIN) & (d["pl4"] >= d["v_orc4"])
    g = dict(viable=viable, closure=viable & closure, structures=viable & structures, sensitive=viable & sensitive)
    g["candidate"] = g["closure"] & g["structures"] & g["sensitive"]
    return g


def score(d: dict, t: np.ndarray) -> np.ndarray:
    """Rank score in [0, 1] (0 for non-viable worlds)."""
    c = lambda v: np.clip(np.nan_to_num(v, nan=0.0, posinf=1.0, neginf=0.0), 0.0, 1.0)
    d_gap = c(d["gap_max"] / 0.3)
    d_c1 = c((d["ceil1"] - 0.5) / 0.4)
    d_orc = c((0.8 - d["v_orc8"]) / 0.5)
    nb_ok = (d["nb_mean"] >= NB_MIN) & (d["nb_mean"] <= NB_MAX) & (d["ovf_kept_ticks"] == 0)
    d_bod = np.where(nb_ok, 1.0, 0.3) * (0.1 + 0.9 * c(d["body_frac"] / 0.3))
    d_move = 0.1 + 0.9 * c(d["v_net"] / 0.3)
    d_int = 0.1 + 0.9 * c(d["events100"] / 10.0)
    d_sens = 0.1 + 0.9 * c(d["pl4"] / 0.05)
    s = (d_gap * d_c1 * d_orc * d_bod * d_move * d_int * d_sens) ** (1.0 / 7.0)
    return np.where(t >= 5, s, 0.0)
