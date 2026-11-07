"""programs -- designer-chosen open-loop programs aimed at a body visible in a saved state.

All programs are fixed from the state at t = 0 (tracker table and slot map), never re-aimed: the
target's path is extrapolated linearly, p(t) = p0 + v0 t. Direction n = the target's left normal
(+90 deg from its velocity). Every program lasts T_IN = 4 ticks with the budget split equally.

wind_aimed(C)     uniform force f n on the 2 x 2 blocks whose centres surround p(t + 1/2), each tick
                  (the group follows the extrapolated path); f = sigma_w sqrt(C / (2 T_IN)).
wind_regional(C)  uniform force f n on the 4 x 4 blocks (64 x 64 px) around the t = 0 group, fixed in
                  space; f = sigma_w sqrt(C / (8 T_IN)).
kick_aimed(L1)    the port's matter kick on the target's flanks: k sources on the -n flank (highest
                  matter, pn < -rg/4) and k sinks on the +n flank (largest pn) of the t = 0 footprint
                  shifted by round(v0 t); per tick sum|a| = L1 / T_IN, k = 4 (L1 <= 16) or 16 (L1 = 64,
                  designer probe beyond Admissible(k=8, total=4)). Its KL against the flow noise is infinite;
                  its budget is its own L1 norm.
"""
from __future__ import annotations

import numpy as np

from wind import G, H, HW, KMAX, NF, NW, W, mi

T_IN = 4
CY, CX, UID = NF, NF + 1, NF + 4


def pick_target(T):
    """run_steer.pick_target (VW-0 rule: mass within [0.5, 1.6] x median, speed >= 0.6 px/tick,
    isolated by rg_s + rg_o + 10 px; fastest wins), with fallbacks so every state has a target:
    (1) fastest non-isolated body passing mass and speed, (2) heaviest present body.
    Returns (slot, tier) with tier 0 / 1 / 2."""
    pres = np.flatnonzero(T[:, 0] > 0.5)
    if pres.size == 0:
        return None, -1
    med = np.median(T[pres, 1])
    best, bs, best1, bs1 = None, 0.0, None, 0.0
    for s in pres:
        sp = np.hypot(T[s, 10], T[s, 11])
        if not (0.5 * med <= T[s, 1] <= 1.6 * med) or sp < 0.6:
            continue
        iso = all(np.hypot(mi(T[o, CY] - T[s, CY], H), mi(T[o, CX] - T[s, CX], W)) >= T[s, 7] + T[o, 7] + 10
                  for o in pres if o != s)
        if iso and sp > bs:
            best, bs = s, sp
        if sp > bs1:
            best1, bs1 = s, sp
    if best is not None:
        return int(best), 0
    if best1 is not None:
        return int(best1), 1
    return int(pres[np.argmax(T[pres, 1])]), 2


def frame(T, s):
    """(p0 (y, x), v0 (vy, vx), n (y, x) unit left normal, speed)."""
    p0 = np.array([T[s, CY], T[s, CX]], float)
    v = np.array([T[s, 11], T[s, 10]], float)
    sp = float(np.hypot(*v))
    u = v / sp if sp > 1e-6 else np.array([0.0, 1.0])
    n = np.array([u[1], -u[0]])          # (y, x): rotate (ux, uy) by +90 deg in the (x, y) plane
    return p0, v, n, sp


def _group(p):
    """Rows and cols of the 2 x 2 blocks whose centres (16 i + 7.5) surround p."""
    b = H // G
    i0 = int(np.floor((p[0] - (b - 1) / 2) / b)) % G
    j0 = int(np.floor((p[1] - (b - 1) / 2) / b)) % G
    return [i0, (i0 + 1) % G], [j0, (j0 + 1) % G]


def wind_aimed(T, s, C, sigma_w, T_in=T_IN):
    p0, v, n, _ = frame(T, s)
    f = sigma_w * np.sqrt(C / (2.0 * T_in))
    U = np.zeros((T_in, 2, G, G))
    for t in range(T_in):
        rows, cols = _group(p0 + v * (t + 0.5))
        for c in range(2):
            U[t, c][np.ix_(rows, cols)] = f * n[c]
    return U.reshape(T_in, NW)


def wind_regional(T, s, C, sigma_w, T_in=T_IN):
    p0, v, n, _ = frame(T, s)
    f = sigma_w * np.sqrt(C / (8.0 * T_in))
    rows, cols = _group(p0)
    rows = [(rows[0] + k) % G for k in (-1, 0, 1, 2)]
    cols = [(cols[0] + k) % G for k in (-1, 0, 1, 2)]
    U = np.zeros((T_in, 2, G, G))
    for t in range(T_in):
        for c in range(2):
            U[t, c][np.ix_(rows, cols)] = f * n[c]
    return U.reshape(T_in, NW)


def kick_aimed(T, s, smap, A, L1, T_in=T_IN):
    """-> (idx (T_in, KMAX) int, val (T_in, KMAX)), commanded L1 per tick, number of cells per side."""
    p0, v, n, _ = frame(T, s)
    S = np.asarray(A).reshape(2, -1).sum(0)
    cells = np.flatnonzero((np.asarray(smap).astype(int) == s + 1) & (S > 1e-3))
    y, x = cells // W, cells % W
    dy, dx = mi(y - p0[0], H), mi(x - p0[1], W)
    pn = dy * n[0] + dx * n[1]
    per = L1 / T_in
    k = 4 if per <= 4 + 1e-9 else 16
    amp = per / (2 * k)
    cand = np.flatnonzero(pn < -0.25 * T[s, 7])
    src = cand[np.argsort(-S[cells[cand]], kind="stable")[:k]]
    snk = np.argsort(-pn, kind="stable")
    snk = np.array([j for j in snk if j not in set(src)][:k], int)
    idx = np.zeros((T_in, KMAX), int)
    val = np.zeros((T_in, KMAX))
    for t in range(T_in):
        sh = np.rint(v * t).astype(int)
        ys, xs = (y + sh[0]) % H, (x + sh[1]) % W
        cs = ys * W + xs
        idx[t, :len(src)] = cs[src]
        val[t, :len(src)] = -amp
        idx[t, len(src):len(src) + len(snk)] = cs[snk]
        val[t, len(src):len(src) + len(snk)] = amp
        # zero sum when the two sides differ in size (rare): rescale the larger side
        neg, pos = -val[t][val[t] < 0].sum(), val[t][val[t] > 0].sum()
        if neg > 0 and pos > 0 and abs(neg - pos) > 1e-12:
            m = min(neg, pos)
            val[t][val[t] < 0] *= m / neg
            val[t][val[t] > 0] *= m / pos
    return idx, val, float(np.abs(val).sum()), (len(src), len(snk))
