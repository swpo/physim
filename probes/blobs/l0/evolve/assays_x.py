"""assays_x.py — A4 CROSS assay on the lib stack (l0-evolver extension).

LOCKED convention (port of evolve/metrics.py v1.1/v1.2 A4 to lib primitives,
amendment v1.3 documented in evolve/metrics.py): for genomes with >= 2
persisting acts, poke act a0 at (L/2-d0/2, L/2) and act a1 at (L/2+d0/2, L/2),
d0=10, T=800, L=64. Each act's channels dressed per its A1 winning variant
(0.0 bare / 0.6 dressed); a0's dressing SHIFTED 0.5 px in -y = kick (90deg,
0.5) M1 convention (angular symmetry breaking; certified rotor self-starts
but round-off takes unbounded time — deterministic kick is the screening
protocol). Classes: blowup, replicate, die, merge_x (either act ncomp!=1 ...
we keep 'odd'), rotor (|revs|>=0.75 AND sep plateau std<0.15), cross_bond
(plateau, no rotation), repel (sep_end > min(d0+6,24)), drift.
"""
import numpy as np
import genome as G

D0_X = 10.0
T_X = 800.0
L_X = 64.0
KICK_D = 0.5


def a4_cross(g, a0, a1, dress0=0.0, dress1=0.0, d0=D0_X, T=T_X, L=L_X, dx=0.5):
    N = int(round(L / dx))
    F = G.state_vacuum(g, N)
    na = len(g["acts"])
    W = np.asarray(g["W"], float)
    x0, x1 = L / 2 - d0 / 2, L / 2 + d0 / 2
    for (act, xx, dress, kick) in ((a0, x0, dress0, True), (a1, x1, dress1, False)):
        base = F[act].copy()
        F = G.poke(F, g, act, xx, L / 2, 2.0, 3.0, dx)
        if dress > 0:
            bump = F[act] - base
            if kick:
                bump = G.fshift(bump, -KICK_D / dx, 0.0)   # shift -y px
            for c, ch in enumerate(g["chans"]):
                if ch["g"] == "id" and W[c, act] != 0.0:
                    F[na + c] += dress * W[c, act] * bump
    r = G.run_genome(g, F=F, T=T, dx=dx, L=L, rec_tu=5.0,
                     track_acts=[a0, a1], stop_explode_n=4,
                     ref_pos={a0: [(x0, L / 2)], a1: [(x1, L / 2)]})
    if r["status"] == "blowup":
        return dict(cls="blowup", d0=d0)
    if r["status"] == "replicated":
        return dict(cls="replicate", d0=d0)
    nc0, nc1 = r[f"ncomp{a0}"], r[f"ncomp{a1}"]
    if r["status"] == "died" or nc0[-1] == 0 or nc1[-1] == 0:
        return dict(cls="die", d0=d0)
    if nc0[-1] != 1 or nc1[-1] != 1:
        return dict(cls="odd", d0=d0)
    ts, p0s, p1s = [], [], []
    for k in range(len(r["t"])):
        if nc0[k] == 1 and nc1[k] == 1 and len(r[f"pos{a0}"][k]) and len(r[f"pos{a1}"][k]):
            ts.append(r["t"][k])
            p0s.append(r[f"pos{a0}"][k][0])
            p1s.append(r[f"pos{a1}"][k][0])
    if len(ts) < 12:
        return dict(cls="odd", d0=d0)
    d = np.array([G.min_image(np.array(b) - np.array(a), L)
                  for a, b in zip(p0s, p1s)])
    ang = np.unwrap(np.arctan2(d[:, 0], d[:, 1]))
    sep = np.hypot(d[:, 0], d[:, 1])
    ts = np.array(ts)
    i0 = len(ts) // 2
    revs = float((ang[-1] - ang[0]) / (2 * np.pi))
    omega = float(np.polyfit(ts[i0:], ang[i0:], 1)[0])
    sep_m, sep_s = float(sep[i0:].mean()), float(sep[i0:].std())
    out = dict(d0=d0, revs=revs, omega=omega, sep_mean=sep_m, sep_std=sep_s,
               sep_end=float(sep[-1]), wall_s=round(r["wall_s"], 2))
    plateau = sep_s < 0.15 and 3.0 < sep_m < 24.0
    if abs(revs) >= 0.75 and plateau:
        out["cls"] = "rotor"
    elif plateau:
        out["cls"] = "cross_bond"
    elif sep_m > min(d0 + 6.0, 24.0):
        out["cls"] = "repel"
    else:
        out["cls"] = "drift"
    return out
