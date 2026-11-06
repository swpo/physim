"""Oracle branches: R-1 fresh-noise replicates from each saved test state (h0, m) of the base runs.

usage: python run_branches.py WORLD J0 J1 NREP TMAX
Replicate r of state (j, i) uses noise seed (77, 202, j, i, r) (independent of the base trajectory,
which serves as replicate 0). Records level-1 vectors of both Phi at every tick 1..TMAX."""
import os
import sys
import time

import numpy as np

import lenia_world as LW
vw = LW.vw


def main():
    name, j0, j1, nrep, tmax = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    specs, parts = LW.make_specs(name)
    coarse = parts["phi_coarse"]
    w = vw.VectorWorld(specs["objects"], world_seed=0)
    for j in range(j0, j1):
        out = f"data/{name}/branch_{j:03d}.npz"
        if os.path.exists(out):
            continue
        t_start = time.time()
        d = np.load(f"data/{name}/base_{j:03d}.npz")
        Yo = np.zeros((len(d["st_tick"]), nrep - 1, tmax, w.spec.n1))
        Yc = np.zeros((len(d["st_tick"]), nrep - 1, tmax, coarse(d["st_h0"][:1]).shape[1]))
        for i in range(len(d["st_tick"])):
            for r in range(1, nrep):
                ens = vw.Ensemble(w, d["st_h0"][i][None], d["st_m"][i][None], (77, 202, j, i, r), [0],
                                  int(d["st_tick"][i]))
                for s in range(tmax):
                    ens.step(None)
                    Yo[i, r - 1, s] = ens.h1()[0]
                    Yc[i, r - 1, s] = coarse(ens.h0)[0]
        np.savez_compressed(out, Yo=Yo, Yc=Yc)
        print(name, j, "done", round(time.time() - t_start, 1), "s", flush=True)


if __name__ == "__main__":
    main()
