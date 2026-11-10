"""longrun -- is a world's activity a transient? Windowed descriptors over a long free run (CPU, about a minute per world).

    python -B longrun.py --draws 12,345 [--prior-seed 2026] [--ticks 2000] [--window 250] [--out results/longrun.json]

2 members per world, 50 burn-in ticks, then `ticks` ticks; per window: fraction of matter relocated per tick,
bodies, share of mass in bodies, net body speed over 8 ticks, fusions + fissions per 100 ticks, and the
block view's persistence error at 16 ticks in units of its variance within the window.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

import screen as SC  # noqa: E402
import tnca as TN  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--draws", required=True)
    ap.add_argument("--prior-seed", type=int, default=2026)
    ap.add_argument("--ticks", type=int, default=2000)
    ap.add_argument("--window", type=int, default=250)
    ap.add_argument("--out", default=os.path.join(HERE, "results", "longrun.json"))
    a = ap.parse_args()
    T, Wn = a.ticks, a.window
    sz = SC.Sizes(M=2, M_fit=1, M_trk=2, burn=50, T=T, n_snap=1, R=2, R2=2, HB=1)
    wd = SC.tnca_world()
    fn = jax.jit(lambda th, key: {k: v for k, v in SC.simulate_one(wd, sz, th, th, key).items()
                                  if k in ("y", "moved", "tab", "mass", "mass0", "xmin")})
    out = dict(what=__doc__.split("\n")[0], prior_seed=a.prior_seed, ticks=T, window=Wn, members=2,
               platform=dict(backend=jax.default_backend(), jax=jax.__version__, dtype="float64"), worlds=[])
    P, UID, CY, CX, MS, EV = SC._P, SC._UID, SC._CY, SC._CX, SC._MS, SC._EV
    for i in [int(v) for v in a.draws.split(",")]:
        t0 = time.time()
        th = {k: jnp.asarray(v) for k, v in TN.draw_theta(a.prior_seed, i).items()}
        o = {k: np.asarray(v) for k, v in fn(th, jax.random.key(7000 + i)).items()}
        y, tb = o["y"], o["tab"]                                   # (T + 1, M, Q, G, G), (T + 1, Mt, K, 10)
        rows = []
        for s in range(0, T, Wn):
            e = s + Wn
            yy = y[s:e + 1]
            sd2 = yy.var((0, 1, 3, 4)).mean()
            vp16 = float(((yy[16:] - yy[:-16]) ** 2).mean((0, 1, 3, 4)).mean() / max(sd2, 1e-300)) if Wn > 16 else None
            tt = tb[s:e + 1]
            p = tt[..., P] > 0.5
            L = 8
            same = p[L:] & p[:-L] & (tt[L:, ..., UID] == tt[:-L, ..., UID])
            mi = lambda d, n: d - n * np.round(d / n)
            dist = np.hypot(mi(tt[L:, ..., CY] - tt[:-L, ..., CY], 64), mi(tt[L:, ..., CX] - tt[:-L, ..., CX], 64))
            ev = tt[1:, ..., EV]
            rows.append(dict(ticks=[s, e], moved=float(o["moved"][s:e].mean()), bodies=float(p.sum(-1).mean()),
                             body_frac=float((tt[..., MS] * p).sum(-1).mean() / 4096.0),
                             v_net=float((dist * same).sum() / max(same.sum(), 1) / L),
                             # fusions: one survivor row each; fissions: parent and product rows
                             events100=float(((ev == 3).sum() + (ev == 2).sum() / 2.0) / tt.shape[1] * 100.0 / Wn),
                             vp16=vp16))
        w = dict(draw=i, seconds=round(time.time() - t0, 1), windows=rows,
                 mass_drift=float(np.abs(o["mass"].sum(-1) - o["mass0"][None]).max() / o["mass0"].min()),
                 xmin=float(o["xmin"].min()))
        out["worlds"].append(w)
        print(i, w["seconds"], "s; moved", [round(r["moved"], 3) for r in rows], "v_net", [round(r["v_net"], 3) for r in rows],
              "bodies", [round(r["bodies"], 1) for r in rows], "events", [round(r["events100"], 1) for r in rows], flush=True)
    with open(a.out, "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
