"""machinev3/metrics.py — V3 composition-machine metrics. LOCKED 2026-02-22
BEFORE any certification run (smoke + probe variants may precede; gates below
are frozen; any later change = documented amendment row in results.json).

WORLD: block direct-sum of engine_10748 (1 act "E" + v_e,w_e) and s2_128_26
(2 acts: "C"=plateau act0, dead act1 + c0,c1_tanh,c2), one coupling move.
Field order: acts [0=E, 1=C, 2=dead], chans [0=v_e, 1=w_e, 2=c0, 3=c1t, 4=c2].

GATES (V3-0):
  G_ENGINE  lone kicked engine in the COUPLED world travels with c within
            +-20 pct of c_ref (c_ref = same protocol, coupling zeroed, same L)
            AND no cargo nucleation (ncomp_C==0, ncomp_dead==0 all run).
  G_CARGO   lone cargo blob (dress 0.6, no kick) in the COUPLED world:
            net drift < 2 px over T>=800, ncomp_C==1 throughout, alive.
  G_TOW     a lock window exists: contiguous records with ncomp_E==1,
            ncomp_C==n_cargo, sep(E, nearest C) in [1.5, 22] px, cargo COM
            x-speed >= 0.02 px/tu (5-rec smoothed); cargo COM x-displacement
            across the longest window >= 30 px. Direction = engine kick (+x).
V3-0 PASS = G_ENGINE and G_CARGO and G_TOW.

GATES (V3-1, stack delivery):
  G_DELIV   3-stack (spacing 14.0): stack COM +x displacement >= 60 px under
            engine drive, census ncomp_C==3 whole run (no collapse/replicate).
  G_RELEASE after the release event (engine dial-stop phase or in-genome
            dock zone): over the final 400 tu stack COM drift < 2 px, all
            spacings within 14.0 +- 1.0 px, ncomp_C==3, engine either parked
            /dead by its own dial or separated > 30 px. 2 seeds (noise 2e-3).
V3-1 PASS = G_DELIV and G_RELEASE on both seeds.

All positions unwrapped (Tracker convention), speeds by np.gradient on the
record grid, smoothed with a 5-record moving mean.
"""
import numpy as np

V_TOW = 0.02            # px/tu sustained cargo speed = machine action
V_PARK = 0.005          # px/tu parked
SEP_LOCK_MIN = 1.5      # px
SEP_LOCK_MAX = 22.0     # px
DRAG_MIN = 30.0         # px V3-0
DELIVER_MIN = 60.0      # px V3-1
PARK_DRIFT_MAX = 2.0    # px
C_ENGINE_TOL = 0.20     # relative
SPACING_TOL = 1.0       # px around 14.0
POST_RELEASE_WIN = 400.0
SMOOTH = 5


def smooth(v, w=SMOOTH):
    if w > 1 and len(v) > 2 * w:
        return np.convolve(v, np.ones(w) / w, mode="same")
    return np.asarray(v, float)


def com_speed_x(t, x):
    return smooth(np.gradient(np.asarray(x, float), np.asarray(t, float)))


def runs_true(mask):
    """[(i0, i1_inclusive)] of contiguous True runs."""
    out, i0 = [], None
    for i, m in enumerate(mask):
        if m and i0 is None:
            i0 = i
        elif not m and i0 is not None:
            out.append((i0, i - 1)); i0 = None
    if i0 is not None:
        out.append((i0, len(mask) - 1))
    return out


def lock_analysis(t, xe, xc_com, sep, nce, ncc, n_cargo):
    """Locked-tow feature extraction. Returns dict (no class decision)."""
    t = np.asarray(t, float)
    vx = com_speed_x(t, xc_com)
    ok = ((np.asarray(nce) == 1) & (np.asarray(ncc) == n_cargo)
          & (np.asarray(sep) >= SEP_LOCK_MIN) & (np.asarray(sep) <= SEP_LOCK_MAX)
          & (vx >= V_TOW))
    wins = runs_true(ok)
    best, drag = None, 0.0
    for (i0, i1) in wins:
        d = float(xc_com[i1] - xc_com[i0])
        if d > drag:
            drag, best = d, (i0, i1)
    out = dict(drag_px=float(drag), n_lock_windows=len(wins))
    if best:
        i0, i1 = best
        out.update(lock_t0=float(t[i0]), lock_t1=float(t[i1]),
                   lock_dur=float(t[i1] - t[i0]),
                   sep_mean=float(np.mean(sep[i0:i1 + 1])),
                   sep_std=float(np.std(sep[i0:i1 + 1])),
                   c_cargo_lock=float((xc_com[i1] - xc_com[i0]) /
                                      max(t[i1] - t[i0], 1e-9)))
    return out


def park_gate(t, pos_com, win=None):
    """net COM drift over the run (or final win tu)."""
    t = np.asarray(t, float)
    p = np.asarray(pos_com, float)
    m = np.ones(len(t), bool) if win is None else (t >= t[-1] - win)
    seg = p[m]
    net = float(np.hypot(*(seg[-1] - seg[0])))
    return dict(net_px=net, parked=bool(net < PARK_DRIFT_MAX))


def engine_gate(c_coupled, c_ref):
    ok = (c_ref > 0) and abs(c_coupled - c_ref) / c_ref <= C_ENGINE_TOL
    return dict(c=float(c_coupled), c_ref=float(c_ref),
                rel=float(c_coupled / c_ref if c_ref else np.nan), ok=bool(ok))
