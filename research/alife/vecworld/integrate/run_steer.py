"""Steering: can sparse, default-admissible inputs (k = 8, values +-0.5, sum|a| = 4, zero sum) steer
one creature? Closed-loop designer programs (cells chosen from h0 every tick), against the no-input
twin (the base trajectory: same state, identical noise).

usage: python run_steer.py WORLD J0 J1 STATE_INDEX NTICKS [VIDEO_J]
Strategies (sign +1 / -1 picks the side n = +-(heading rotated by 90 deg)):
  flank  move matter from the body's -n flank (densest cells) to its +n edge cells
  lead   move matter from the body's rear (densest cells) to a 2x2 patch just ahead of it on +n"""
import os
import sys
import time

import numpy as np

import lenia_world as LW
vw = LW.vw

STRATS = [("flank", 1), ("flank", -1), ("lead", 1), ("lead", -1)]


def mi(d, L):
    return (d + L / 2) % L - L / 2


def pick_target(T, H, W):
    pres = np.flatnonzero(T[:, 0] > 0.5)
    if pres.size < 2:
        return None
    mass = T[pres, 1]
    med = np.median(mass)
    best, bs = None, 0.0
    for s in pres:
        sp = np.hypot(T[s, 10], T[s, 11])
        if not (0.5 * med <= T[s, 1] <= 1.6 * med) or sp < 0.6:
            continue
        ok = True
        for o in pres:
            if o == s:
                continue
            dd = np.hypot(mi(T[o, LW.NF] - T[s, LW.NF], H), mi(T[o, LW.NF + 1] - T[s, LW.NF + 1], W))
            if dd < T[s, 7] + T[o, 7] + 10:
                ok = False
        if ok and sp > bs:
            best, bs = s, sp
    return best


def program(strat, sign, h0, m, s, l0, tr):
    HW, H, W = l0.HW, l0.H, l0.W
    T = tr.table(m[None])[0]
    if T[s, 0] < 0.5:
        return None
    cy, cx, rg = T[s, LW.NF], T[s, LW.NF + 1], T[s, 7]
    v = np.array([T[s, 10], T[s, 11]])
    u = v / max(np.linalg.norm(v), 1e-9)
    n = sign * np.array([-u[1], u[0]])
    S = h0.reshape(l0.C, HW).sum(0)
    cells = np.flatnonzero((m[:HW] == s + 1) & (S > 1e-3))
    y, x = cells // W, cells % W
    dx, dy = mi(x - cx, W), mi(y - cy, H)
    pn, pu = dx * n[0] + dy * n[1], dx * u[0] + dy * u[1]
    if strat == "flank":
        cand = cells[pn < -0.25 * rg]
        src = cand[np.argsort(-S[cand])[:4]]
        snk = cells[np.argsort(-pn)[:4]]
    else:
        cand = cells[pu < 0]
        src = cand[np.argsort(-S[cand])[:4]]
        qx, qy = cx + 1.2 * rg * (0.7 * u[0] + 0.7 * n[0]), cy + 1.2 * rg * (0.7 * u[1] + 0.7 * n[1])
        ix, iy = int(np.floor(qx)), int(np.floor(qy))
        snk = np.array([((iy + a) % H) * W + (ix + b) % W for a in (0, 1) for b in (0, 1)])
    if src.size < 4 or len(set(src) & set(snk)):
        return None
    return src, snk


def main():
    name, j0, j1, si, nt = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    vj = int(sys.argv[6]) if len(sys.argv) > 6 else -1
    specs, parts = LW.make_specs(name)
    l0, tr = parts["l0"], parts["tracker"]
    w = vw.VectorWorld(specs["objects"], world_seed=0)
    inv = LW.inverse_in_map(w)
    C = w.spec.inputs
    for j in range(j0, j1):
        out = f"data/{name}/steer_{j:03d}_s{si}.npz"
        if os.path.exists(out):
            continue
        t_start = time.time()
        d = np.load(f"data/{name}/base_{j:03d}.npz")
        T0 = tr.table(d["st_m"][si][None])[0]
        s = pick_target(T0, l0.H, l0.W)
        if s is None:
            print(name, j, "no isolated moving target", flush=True)
            np.savez_compressed(out, target=-1)
            continue
        res = {"target": s, "t0": int(d["st_tick"][si]) - int(d["burn_in"])}
        runs = STRATS + ([("none", 0)] if j == vj else [])
        for strat, sign in runs:
            ens = vw.Ensemble(w, d["st_h0"][si][None], d["st_m"][si][None], tuple(int(x) for x in d["seed"]), [0],
                              int(d["st_tick"][si]))
            tabs, Yo, frames, cells, ok = [], [], [], [], []
            for k in range(nt):
                a = None
                if strat != "none":
                    pr = program(strat, sign, ens.h0[0], ens.m[0], s, l0, tr)
                    if pr is not None:
                        src, snk = pr
                        a = np.zeros(w.n_in)
                        a[inv[src]] = -0.5
                        a[inv[snk]] = 0.5
                        ok.append(not C.violations({int(i): float(a[i]) for i in np.flatnonzero(a)}, 0, None, 0.0))
                        cells.append(np.concatenate([src, snk]))
                    else:
                        cells.append(-np.ones(8, int))
                if j == vj:
                    frames.append(ens.h0[0].reshape(l0.shape).astype(np.float32))
                ens.step(a)
                tabs.append(tr.table(ens.m)[0].copy())
                Yo.append(ens.h1()[0])
            if j == vj:
                frames.append(ens.h0[0].reshape(l0.shape).astype(np.float32))
            key = f"{strat}{'+' if sign > 0 else '-' if sign < 0 else ''}"
            res[f"{key}__tab"] = np.array(tabs)
            res[f"{key}__Yo"] = np.array(Yo)
            res[f"{key}__cells"] = np.array(cells) if cells else np.zeros((0, 8), int)
            res[f"{key}__admissible"] = np.array(ok)
            if frames:
                res[f"{key}__frames"] = np.array(frames)
        np.savez_compressed(out, **res)
        print(name, j, "target", s, "done", round(time.time() - t_start, 1), "s", flush=True)


if __name__ == "__main__":
    main()
