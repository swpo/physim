"""Base trajectories through the VW-0 machinery (designer ensembles of one member each).

usage: python run_base.py WORLD J0 J1 T [VIDEO_J ...]
For each trajectory j in [J0, J1): reset from the declared initial distribution with designer seed
(NS_DESIGNER, 101, j) (init + burn-in), then T free ticks. Records level-1 vectors of both Phi at
every tick, the tracker's slot table and counters, and privileged states at the test ticks (for
branching) plus float32 level-0 snapshots at test tick + tau (for level-0 divergence)."""
import os
import sys
import time

import numpy as np

import lenia_world as LW
vw = LW.vw

TEST_TICKS = (60, 140, 220)
TAUS_L0 = (1, 2, 4, 8, 16, 24, 32)

def main():
    name, j0, j1, T = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    video = {int(x) for x in sys.argv[5:]}
    specs, parts = LW.make_specs(name)
    tr, coarse, l0 = parts["tracker"], parts["phi_coarse"], parts["l0"]
    w = vw.VectorWorld(specs["objects"], world_seed=0)
    os.makedirs(f"data/{name}", exist_ok=True)
    for j in range(j0, j1):
        out = f"data/{name}/base_{j:03d}.npz"
        if os.path.exists(out):
            continue
        t_start = time.time()
        seed = (vw._NS_DESIGNER, 101, j)
        ens = w._new_ensemble(1, seed)
        TT = tuple(t for t in TEST_TICKS if t <= T)
        Yo, Yc, Tab, Gl, M = [], [], [], [], []
        states = {}
        l0snap = {}
        frames = []
        for t in range(T + 1):
            if t > 0:
                ens.step(None)
            Yo.append(ens.h1()[0])
            Yc.append(coarse(ens.h0)[0])
            tab = tr.table(ens.m)[0]
            Tab.append(tab[:, LW.NF:].copy())
            Gl.append(ens.m[0, -LW.N_GLOBAL:].copy())
            M.append(ens.h0[0].reshape(l0.C, -1).sum(1))
            if t in TT:
                states[t] = (ens.h0[0].copy(), ens.m[0].copy(), ens.tick)
            for t0 in TT:
                if t - t0 in TAUS_L0:
                    l0snap[(t0, t - t0)] = ens.h0[0].astype(np.float32)
            if j in video:
                frames.append(ens.h0[0].reshape(l0.shape).astype(np.float32))
        np.savez_compressed(
            out, Yo=np.array(Yo), Yc=np.array(Yc), tab=np.array(Tab), glob=np.array(Gl), mass=np.array(M),
            seed=np.array(seed), test_ticks=np.array(TT), burn_in=w.spec.burn_in,
            st_h0=np.array([states[t][0] for t in TT]), st_m=np.array([states[t][1] for t in TT]),
            st_tick=np.array([states[t][2] for t in TT]),
            l0_keys=np.array(sorted(l0snap)), l0_snap=np.array([l0snap[k] for k in sorted(l0snap)]))
        if frames:
            np.savez_compressed(f"data/{name}/frames_{j:03d}.npz", A=np.array(frames))
        print(name, j, "done", round(time.time() - t_start, 1), "s", flush=True)


if __name__ == "__main__":
    main()
