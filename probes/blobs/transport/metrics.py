"""metrics.py — M5-prep TRANSPORT locked measurement module.

LOCKED BEFORE CERTIFICATION (lock stamp below). Post-cert edits invalidate certs.

Conventions:
- Gradient axis = axis 0 = "x". Blob positions in physical px (dx-scaled),
  tracks are UNWRAPPED (periodic-safe).
- eps = local slope of static drive b(x) in k1-units per px (tri profile:
  b = eps*g, slope exactly +eps on the rising branch where blobs are seeded).
- DOWNSTREAM := the direction a free single blob drifts on a +eps branch
  (empirical; sign recorded per species).

Estimators (frozen):
- drift_speed: LSQ slope of x(t) on the analysis window
    t >= SETTLE  and  |x - x0| <= RUNWAY  (constant-slope region guard)
  Needs >= MIN_PTS samples. Returns v_x, v_y, r2 of the x-fit, net
  displacement, and a "moved" verdict: |net_x| > MOVE_MIN px.
  PINNED verdict: not moved AND |v_x| < V_FLOOR.
- scatter_geometry: incoming along +x. Impact parameter b_imp = y0 - y_obs.
  Exit measured on the window x > x_obs + PASS_MARGIN: deflection angle
  theta_out = atan2(vy_out, vx_out) (deg), y-shift = y_end - y0.
  BLOCKED verdict if the cargo never reaches x_obs + PASS_MARGIN.
- channel_metrics: y_rms about channel centerline + net x-advance; compared
  against a no-wall control (same seed/noise).
- ratchet_speed: same LSQ slope, window t >= SETTLE, full track (no runway
  guard; sawtooth is globally periodic). Verdict vs paired flat-b control.
"""
import numpy as np

LOCK = "2026-02-19 pre-certification lock (blob-transport searcher, M5-prep)"

SETTLE = 150.0      # tu; discard stamp-relaxation transient
RUNWAY = 10.0       # px; stay near the b~0 anchor (level drift |b| <= 10*eps)
MIN_PTS = 6
MOVE_MIN = 0.35     # px net displacement to count as "moved"
V_FLOOR = 2.0e-4    # px/tu; below this + not moved => pinned
PASS_MARGIN = 10.0  # px past obstacle x to measure exit velocity
DEAD_AREA = 4.0     # px^2; track area below this = blob dead
GROW_FACTOR = 2.5   # area > GROW_FACTOR*lone_area on window => blob destabilized

# AMENDMENT 2026-02-19 (pre-certification, before any cert run): RUNWAY 12->10,
# V_FLOOR 3.5e-4 -> 2e-4, added GROW_FACTOR area guard + lone_area arg to
# drift_speed after pilot1 showed A-blob area blow-up when it climbs the ramp.


def _fit(t, z):
    A = np.vstack([t, np.ones_like(t)]).T
    coef, res, _, _ = np.linalg.lstsq(A, z, rcond=None)
    zhat = A @ coef
    ss = np.sum((z - z.mean()) ** 2)
    r2 = 1.0 - (np.sum((z - zhat) ** 2) / ss if ss > 0 else 0.0)
    return float(coef[0]), float(r2)


def drift_speed(t, x, y, area, x0, settle=SETTLE, runway=RUNWAY, lone_area=None):
    t = np.asarray(t, float); x = np.asarray(x, float); y = np.asarray(y, float)
    area = np.asarray(area, float)
    alive = area >= DEAD_AREA
    if not alive.any() or not alive[-1]:
        return dict(verdict="died", t_death=float(t[~alive][0]) if (~alive).any() else None)
    m = (t >= settle) & np.isfinite(x) & (np.abs(x - x0) <= runway) & alive
    if m.sum() < MIN_PTS:
        return dict(verdict="too_few_pts", n=int(m.sum()))
    amax = float(area[m].max())
    if lone_area is not None and amax > GROW_FACTOR * lone_area:
        # restrict window to before destabilization
        ok = area <= GROW_FACTOR * lone_area
        m = m & ok
        if m.sum() < MIN_PTS:
            return dict(verdict="grew_unstable", area_max=amax, n=int(m.sum()))
    vx, r2x = _fit(t[m], x[m])
    vy, _ = _fit(t[m], y[m])
    net = float(x[m][-1] - x[m][0])
    moved = abs(net) > MOVE_MIN
    verdict = "drifts" if moved else ("pinned" if abs(vx) < V_FLOOR else "creep")
    return dict(verdict=verdict, v_x=vx, v_y=vy, r2_x=r2x, net_x=net,
                area_max=amax, n=int(m.sum()), t_lo=float(t[m][0]), t_hi=float(t[m][-1]),
                x_lo=float(x[m][0]), x_hi=float(x[m][-1]))


def scatter_geometry(t, x, y, area, x_obs, y0, pass_margin=PASS_MARGIN):
    t = np.asarray(t, float); x = np.asarray(x, float); y = np.asarray(y, float)
    area = np.asarray(area, float)
    alive = area >= DEAD_AREA
    if not alive[-1]:
        return dict(verdict="died")
    past = np.isfinite(x) & (x > x_obs + pass_margin) & alive
    if past.sum() < MIN_PTS:
        xmax = float(np.nanmax(x))
        return dict(verdict="blocked", x_max=xmax, gap_to_obs=float(x_obs - xmax),
                    y_end=float(y[alive][-1]), y_shift=float(y[alive][-1] - y0))
    vx, _ = _fit(t[past], x[past])
    vy, _ = _fit(t[past], y[past])
    theta = float(np.degrees(np.arctan2(vy, vx)))
    return dict(verdict="passed", theta_out_deg=theta,
                y_shift=float(y[past][-1] - y0),
                vx_out=vx, vy_out=vy, t_pass=float(t[past][0]))


def channel_metrics(t, x, y, area, y_center, settle=SETTLE, lone_area=None):
    """AMENDMENT 2026-02-19 (pre-certification, documented): added lone_area
    guard — y statistics are only meaningful while the cargo IS a compact blob;
    samples after area > GROW_FACTOR*lone_area are excluded and t_compact is
    reported. Controls destabilize into stripes; without the guard y_rms
    measures stripe COM, not cargo path."""
    t = np.asarray(t, float); x = np.asarray(x, float); y = np.asarray(y, float)
    area = np.asarray(area, float)
    alive = area >= DEAD_AREA
    m = (t >= settle) & np.isfinite(x) & alive
    if lone_area is not None:
        compact = area <= GROW_FACTOR * lone_area
        m = m & compact
    if m.sum() < MIN_PTS:
        return dict(verdict="too_few_pts")
    dy = y[m] - y_center
    return dict(verdict="ok", y_rms=float(np.sqrt(np.mean(dy ** 2))),
                y_max=float(np.max(np.abs(dy))),
                y_final=float(y[m][-1]),
                net_x=float(x[m][-1] - x[m][0]),
                T_obs=float(t[m][-1] - t[m][0]),
                t_compact=float(t[m][-1]))


def ratchet_speed(t, x, area, settle=SETTLE):
    t = np.asarray(t, float); x = np.asarray(x, float)
    area = np.asarray(area, float)
    alive = area >= DEAD_AREA
    if not alive[-1]:
        return dict(verdict="died")
    m = (t >= settle) & np.isfinite(x) & alive
    if m.sum() < MIN_PTS:
        return dict(verdict="too_few_pts")
    vx, r2 = _fit(t[m], x[m])
    net = float(x[m][-1] - x[m][0])
    return dict(verdict="ok", v_x=vx, net_x=net, r2=r2,
                T_obs=float(t[m][-1] - t[m][0]))
