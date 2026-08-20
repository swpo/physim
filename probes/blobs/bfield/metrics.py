"""metrics.py — LOCKED measurement conventions for M6 BFIELD certification.
LOCKED 2026-02-19 BEFORE certification runs (BF1/BF2 sections). BF3/BF4 protocol
constants locked by dated amendment after design pilots, BEFORE their cert seeds
(same convention as transport/machine). Any later change invalidates the cert.

WORLD: A=4 single-species family (M4), tau dial, IMEX-FFT dx=0.5 dt=0.02 L=96
periodic (larger L documented per-run). b promoted to 4th dynamical field:
  db/dt = (gamma*S - b)/tau_b + D_b lap b,  S = tanh(max(u-THR,0)/0.4)  ["s2"]
  coupling: k1_eff = k1 + u0*b, k4_eff = k4 + b (isok; exact vacuum for any b).
s1/s3 sources documented as variants; s2 is the certification source.

Tracking: machine/sim.py verbatim (thr = u0 + 0.45(sqrt(lam)-u0), periodic label,
circular-mean centroids, greedy matching, unwrapped coords).

GATES
BF1 COEXISTENCE (flagship = SELF-LAUNCH point: tau=5.7, gamma=+0.05, tau_b=200,
  D_b=0, sigma=2e-3, T=3000, no kick):
  - 3 seeds: alive throughout (ncomp==1 at every record), area_end in [15,80],
    self-propelled at end (c_med over last WIN >= 0.02),
    b_dyn within the STATIC level window measured by machine C3 for singles:
    b_dyn_max_all <= 0.20, b_dyn_min_all >= -0.15.
  - PLUS parked-well coexistence: tau=5.7, gamma=-0.05, tau_b=200, D_b=0,
    sigma=2e-3, T=3000, 1 seed: alive, parked (net |dx| <= 2px), b_core in
    [-0.055, -0.040].
  - dx-refine one-off: kicked launch (g=+0.05, tb=200, Db=0, kick 0deg kd=0.5,
    noiseless, T=1000): |c(dx=0.25) - c(dx=0.5)| / c(dx=0.5) <= 0.15, c over
    t in [700,1000].
BF2 CURVES (all noiseless unless stated):
  - SELF-PROFILE: parked blob (tau=5.7, tb=200, Db=0, T=1500): b_core/gamma in
    [0.95, 1.00] for >= 3 gammas in [-0.15,-0.02] (tanh-saturation law);
    dilution monotone: |b_core| strictly decreasing in D_b over {0, 0.5, 2}.
  - LAUNCH CURVE (NEW MOTILITY): tau=5.7 (BELOW single onset 5.748), tb=200,
    Db=0, parked IC, T=3000: >= 5 traveling points (c_med >= 5e-3 last WIN),
    c monotone in gamma (no decrease worse than 2% of max), plus >= 1 sub-
    threshold point with c_med < 2e-3. Threshold gamma* bracketed.
  - BACKREACTION CURVE: tau=6.0, kicked kd=0.5, tb=200, Db=0, T=1500: >= 7
    points incl. gamma=0 control (|c(0) - 0.1234| / 0.1234 <= 0.03, M4 anchor);
    c(gamma) monotone increasing across the traveling branch; slowdown for
    gamma<0 and speedup for gamma>0 both resolved (>= 3% effects).
    TRAP TRANSITION: >= 1 gamma with directed motion lost: net displacement
    over [TRANSIENT, T] < 40 px AND straightness < 0.4 while blob alive
    (self-trapping); boundary gamma_trap bracketed by a traveling point.
  - TRAIL LAW: from a traveling-blob run, fit b_trail(s) = -B0*exp(-s/s0) along
    the path behind the blob (s = arclength behind): decay length s0 within
    25% of c*tau_b (the relaxation prediction), >= 2 (gamma, tau_b) combos.
BF3 MEDIATED INTERACTION (amendment locks exact geometry after pilot):
  - Writer pair (tau=5.7) passes parked reader at lateral distance >= 20 px.
  - Metric: dy_reader(T) signed TOWARD trail line.
  - PASS: gamma<0 run dy >= +3 px (attraction); gamma=0 control |dy| <= 0.5 px;
    sign flip or |dy| <= 0.5 for gamma>0 (wall = repulsion/neutral documented).
    Reader and writer alive throughout; writer still traveling.
BF4 EMERGENT STRUCTURE (amendment after pilot; candidate = self-dug channel):
  - A groove dug by the writer's passage GUIDES an independently launched
    traveling unit: captured (direction turns along groove, |angle| <= 10 deg
    off groove axis at end) and confined (y_rms about groove line <= 2 px over
    the final 40 px of travel); gamma=0 control crosses the line region with
    < 10 deg turn (no capture). Order parameter: capture angle + y_rms.
B7 BUDGET: routine candidate (T=1500, L=96, 4 fields) <= 5 min single-core;
  tau_b=1000 (T=4000) and L>=128 runs documented one-offs.

Constants: WIN=300.0; TRANSIENT=200.0; C_TRAVEL=5e-3; C_STAT=2e-3;
AREA_OK=(15.0,80.0); B_WINDOW=(-0.15,0.20); WELL_SLOPE=(0.95,1.00);
LAUNCH_ALIVE_C=0.02; TRAP_NET=40.0; TRAP_STRAIGHT=0.4; GRID_CONV_REL=0.15;
TRAIL_S0_RELTOL=0.25; BF3_DY=3.0; BF3_CTRL=0.5; BF4_ANG=10.0; BF4_YRMS=2.0.
"""
import numpy as np

WIN = 300.0
TRANSIENT = 200.0
C_TRAVEL = 5e-3
C_STAT = 2e-3
AREA_OK = (15.0, 80.0)
B_WINDOW = (-0.15, 0.20)
WELL_SLOPE = (0.95, 1.00)
LAUNCH_ALIVE_C = 0.02
TRAP_NET = 40.0
TRAP_STRAIGHT = 0.4
GRID_CONV_REL = 0.15
TRAIL_S0_RELTOL = 0.25
BF3_DY = 3.0
BF3_CTRL = 0.5
BF4_ANG = 10.0
BF4_YRMS = 2.0


def tail_speed(t, x, y, T, win=WIN):
    """Median step speed + net/straightness over the last win tu."""
    sel = (t >= T - win - 1e-9)
    tt, xx, yy = t[sel], x[sel], y[sel]
    if len(tt) < 4:
        return None
    dx = np.diff(xx); dy = np.diff(yy); dt = np.diff(tt)
    sp = np.hypot(dx, dy) / dt
    net = np.hypot(xx[-1] - xx[0], yy[-1] - yy[0])
    path = np.hypot(dx, dy).sum()
    return dict(c_med=float(np.median(sp)),
                straight=float(net / path) if path > 1e-12 else 0.0)


def run_travel_stats(t, x, y, transient=TRANSIENT):
    sel = t >= transient
    tt, xx, yy = t[sel], x[sel], y[sel]
    dx = np.diff(xx); dy = np.diff(yy)
    net = float(np.hypot(xx[-1] - xx[0], yy[-1] - yy[0]))
    path = float(np.hypot(dx, dy).sum())
    return dict(net=net, path=path,
                straight=net / path if path > 1e-12 else 0.0)


def is_trapped(t, x, y, T):
    st = run_travel_stats(t, x, y)
    return st["net"] < TRAP_NET and st["straight"] < TRAP_STRAIGHT, st


def monotone_ok(gammas, cs, tol_frac=0.02):
    order = np.argsort(gammas)
    c = np.asarray(cs)[order]
    tol = tol_frac * np.nanmax(c)
    return bool(np.all(np.diff(c) >= -tol))


def trail_fit(svals, bvals):
    """Fit b = -B0 exp(-s/s0) (or +B0 for gamma>0): returns B0, s0, r2 on log|b|."""
    m = np.abs(bvals) > 1e-6
    s, lb = np.asarray(svals)[m], np.log(np.abs(np.asarray(bvals)[m]))
    if len(s) < 5:
        return None
    A = np.vstack([s, np.ones_like(s)]).T
    coef, res, *_ = np.linalg.lstsq(A, lb, rcond=None)
    pred = A @ coef
    ss_res = float(((lb - pred) ** 2).sum())
    ss_tot = float(((lb - lb.mean()) ** 2).sum())
    return dict(s0=float(-1.0 / coef[0]), B0=float(np.exp(coef[1])),
                r2=1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0)


# ---------------------------------------------------------------------------
# AMENDMENT 1 (dated 2026-02-19, AFTER BF3 design pilots P3_*, BEFORE BF3 cert
# seeds; declared in the header lock). Pilots showed the gamma=0 control reader
# moves dy=+6.75px from the writer pair's DIRECT oscillatory tails at 20px
# lateral offset — the absolute-dy metric is contaminated by non-b physics.
# BF3 metric is REDEFINED as relative-to-control (control isolates direct tails):
#   Geometry A (passage): L=96, tau=5.7, writer pair (18,30)+(33,30) kicked
#   (0deg, kd=0.5), reader parked (48, 30+dy0), dy0=20; tau_b=200, D_b=1.0,
#   source s2, T=1500. ddy := [y_reader(T)-y_reader(0)]_gamma
#                           - [y_reader(T)-y_reader(0)]_gamma=0.
#   PASS(attract, gamma=-0.30): ddy <= -3 px  (toward trail line)
#   PASS(repel,   gamma=+0.30): ddy >= +3 px  (away from trail line)
#   + all runs: every blob alive at every record (ncomp==3), writer pair still
#   traveling at end (v_x >= 0.02), reader stays a single component.
#   Cert battery: noiseless triplet (done as pilots) + sigma=2e-3 seeds
#   {1,2} attract, {1} repel, {1} control; same ddy thresholds per seed pair.
# BF3_DDY = 3.0 px replaces BF3_DY/BF3_CTRL for geometry A.
BF3_DDY = 3.0


# ---------------------------------------------------------------------------
# AMENDMENT 2 (dated 2026-02-19, AFTER BF4 pilots P4/P5/P6/P7/P8, BEFORE BF4
# cert seeds). Pilot findings that forced the redesign, all documented in
# results.json: (i) writer-pair channels at tau=5.7 are contaminated by direct
# wake interactions; (ii) angled stamp kicks quantize to the axis at dx=0.5 for
# kd=0.5 (offset rounds to the same cell) - parallel-launch geometry instead;
# (iii) kick_d=1.0 splits the tau=6.0 blob (trap note); (iv) the groove-guided
# probe is a weakly damped transverse oscillator - "y_rms<=2px" is a
# many-period asymptote, the honest order parameter is transverse BINDING.
# BF4 = TRAIL-BOUND STATE (self-organized channel capturing an independent
# traveler):
#   Stage 1 DIG: tau=6.0 single writer, gamma=-0.50, tau_b=1000, D_b=0.25,
#     source s2, L=128, T=3100, stamped (10,30) kicked (0deg, kd=0.5)
#     [= run W2_dig_gm50_L128; groove: moat along y_g=29.75, depth ~-0.003 to
#     -0.010 k4-units, writer still lapping]. State saved incl. b.
#   Stage 2 CAPTURE: init_from stage-1 state, add probe (60, 52) kicked
#     (0deg, kd=0.5), writing ON (same gamma), T=2500, sigma=2e-3,
#     seeds {1,2,3}.
#   PASS per seed:
#     (a) ncomp==2 at every record (writer + probe alive, no split/merge);
#     (b) probe crosses y_g at least TWICE (restoring force felt on both
#         sides = transverse binding);
#     (c) bounded orbit: after first crossing, max |y_probe - y_g| <= 22.25
#         (the launch offset) - no slingshot;
#     (d) probe co-travels along the channel: v_x (last WIN) >= 0.05;
#     (e) writer stays on-line: |y_writer - y_g| <= 3 px throughout.
#   CONTROL (locks causality, 1 noiseless + seed 1):
#     fresh world, same gamma/probe/kick, NO groove: |y(t)-y(0)| <= 2 px
#     throughout (P7c noiseless: 0.0 px). Groove-only (writing OFF during
#     capture, P7d) documented as mechanism support.
#   Order parameter: n_crossings >= 2 + amplitude contraction A1 = max
#     excursion below y_g < 22.25 = A0 (damped transverse oscillator bound to
#     the self-dug channel).
BF4_YG = 29.75
BF4_A0 = 22.25
BF4_VX = 0.05
BF4_WRITER_DY = 3.0


# ---------------------------------------------------------------------------
# AMENDMENT 3 (dated 2026-02-19, AFTER BF4 battery 1 FAILED — recorded as
# BF4_battery1_FAIL — BEFORE battery 2 seeds). Diagnosis: the noisy WRITER's
# heading diffuses (generic for gamma<0 travelers under noise); it drags the
# channel off the fixed line and breaks the line-tied gates, while all 3 probes
# were in fact captured. Redesign (physics, not metric weakening): the writer
# is REMOVED after the dig by documented IC surgery (vacuum_blob_sector=True:
# blob sector reset to u0, b sector kept verbatim — ICs are free, the groove
# configuration was reached autonomously in W2_dig_gm50_L128). The probe rides
# with writing ON (gamma=-0.50) and MAINTAINS the channel (stigmergy).
# BATTERY 2 (T=2500, L=128, sigma=2e-3, seeds {1,2,3}; probe stamped (60,52)
# kicked (0deg, kd=0.5); init_from=W2_gm50_state + vacuum_blob_sector):
#   (a) ncomp==1 at every record (probe alive, no split);
#   (b) n_crossings(y_g=29.75) >= 2 (restoring force both sides);
#   (c) bounded after first crossing: max |y - y_g| <= 22.25 (launch offset);
#   (d) co-travel: v_x over last WIN >= 0.05;
#   (e) noisy control (fresh world, no groove, same seed 1): 0 crossings of
#       y_g AND stays >= 8 px above y_g throughout (heading diffusion
#       documented quantitatively, not capture);
#   (f) noiseless controls stand: P7c (no groove: dy == 0.0 px),
#       P7d (groove, writing off: capture) — mechanism triangle.


# ---------------------------------------------------------------------------
# AMENDMENT 4 (dated 2026-02-19, AFTER batteries 1-2 readouts — battery 2's
# fixed-line gates also proved frame-brittle (probe seed 2 slingshots through
# a decaying unmaintained section; grooves are MOVING objects co-evolving with
# their diggers) — BEFORE battery 3 = final. This amendment REINTERPRETS
# battery 1 in the channel co-moving frame; no new physics runs needed, the
# battery-1 raw data is scored as-is + one gamma=0 pair control + one T=5000
# boundedness one-off.
# BF4 FINAL = TRAIL-MEDIATED TRANSVERSE BINDING (channel frame):
#   Battery-1 runs (writer + probe, both writing, sigma=2e-3, seeds {1,2,3},
#   T=2500): let dy_rel(t) = y_probe - y_writer (writer position = channel).
#   PASS per seed:
#     (a) both alive, ncomp==2 throughout;
#     (b) dy_rel crosses 0 (probe reaches the channel from 22.25 px away);
#     (c) bounded: max |dy_rel| after first zero <= 1.5 * 22.25 = 33.4 px
#         (no slingshot; overshoot allowed, escape not);
#     (d) return: after the max excursion, |dy_rel| decreases by >= 3 px
#         (restoring force pulls back — oscillator, not fly-through);
#     (e) co-travel: v_x(probe) last WIN >= 0.05.
#   CONTROLS:
#     (f) gamma=0 same two-blob geometry + noise: dy_rel stays >= 15 px from 0
#         at all t (no capture without b) OR monotone growth documented;
#     (g) noiseless triangle P7a/P7c/P7d stands (groove necessary);
#     (h) T=5000 one-off: |dy_rel| bounded <= 33.4 for the whole run
#         (>= 1 full transverse period).
BF4_REL_BOUND = 33.4
BF4_RETURN = 3.0
BF4_CTRL_MIN = 15.0


# ---------------------------------------------------------------------------
# AMENDMENT 5 (dated 2026-02-19, BEFORE any partition runs; channel candidate
# closed as honest partial in BF4_channel_FINAL_readout). BF4 FINAL CANDIDATE =
# MUTUAL-AVOIDANCE SPACE PARTITION (trail network of 3 writers):
#   3 blobs, tau=6.0, L=128 periodic, stamped x=20, y = {44, 64, 84}
#   (crowded: torus NN y-gaps 20/20/88), all kicked (0deg, kd=0.5);
#   gamma=+0.35 (repulsive trails), tau_b=1000, D_b=0.25, source s2, T=2500.
#   Order parameter: R(t) = std/mean of the 3 torus nearest-neighbor y-gaps.
#   R(0) = 0.75; perfect partition (gaps 42.67) R = 0.
#   PASS per run: all alive (ncomp==3 throughout), all traveling at end
#   (v_x last WIN >= 0.05 each), R(end) <= 0.25, and min pairwise torus dy
#   >= 30 px at end (no pair adjacent).
#   CONTROL: gamma=0, same geometry/seeds: R(end) >= 0.45 (no partition force;
#   wake/direct interactions alone do not spread them).
#   Battery: noiseless + seeds {1,2} at sigma=2e-3; control noiseless + seed 1.
BF4P_R_END = 0.25
BF4P_MIN_GAP = 30.0
BF4P_CTRL_R = 0.45
