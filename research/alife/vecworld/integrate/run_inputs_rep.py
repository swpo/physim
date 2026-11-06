"""Input visibility as an agent would see it: does a fixed open-loop input program shift the
conditional mean of the level-1 future beyond the intrinsic spread?

usage: python run_inputs_rep.py WORLD J0 J1 STATE_INDEX TMAX
For each saved test state and condition, the same open-loop program (cells fixed from the initial
state) is run under R = 6 noise realisations: r = 0 with the base trajectory's noise (twin = base),
r = 1..5 with the oracle branches' noise seeds (twin = branch r). Records level 1 of both Phi."""
import os
import sys
import time

import numpy as np

import lenia_world as LW
from run_inputs import choose_cells
vw = LW.vw

CONDS = [
    dict(name="body_k8_b0.5", place="body", k=8, b=0.5, ticks=1),
    dict(name="body_k8_b0.5_x8", place="body", k=8, b=0.5, ticks=8),
    dict(name="rand_k8_b0.5_x8", place="random", k=8, b=0.5, ticks=8),
    dict(name="body_k32_b1_x8", place="body", k=32, b=1.0, ticks=8),
]


def main():
    name, j0, j1, si, tmax = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    specs, parts = LW.make_specs(name)
    l0, tr, coarse = parts["l0"], parts["tracker"], parts["phi_coarse"]
    w = vw.VectorWorld(specs["objects"], world_seed=0)
    inv = LW.inverse_in_map(w)
    for j in range(j0, j1):
        out = f"data/{name}/inrep_{j:03d}_s{si}.npz"
        if os.path.exists(out):
            continue
        t_start = time.time()
        d = np.load(f"data/{name}/base_{j:03d}.npz")
        h0, m0, tick = d["st_h0"][si], d["st_m"][si], int(d["st_tick"][si])
        res = {"t0": tick - int(d["burn_in"])}
        for ci, c in enumerate(CONDS):
            rng = np.random.default_rng([9, j, si, ci])
            prog = []
            for s in range(c["ticks"]):
                src, snk = choose_cells(rng, c["place"], c["k"], h0, m0, l0, tr)
                a = np.zeros(w.n_in)
                a[inv[src]] = -c["b"]
                a[inv[snk]] = c["b"]
                prog.append(a)
            Yo = np.zeros((6, tmax, w.spec.n1))
            Yc = np.zeros((6, tmax, coarse(h0[None]).shape[1]))
            for r in range(6):
                seed = tuple(int(x) for x in d["seed"]) if r == 0 else (77, 202, j, si, r)
                ens = vw.Ensemble(w, h0[None], m0[None], seed, [0], tick)
                for s in range(tmax):
                    ens.step(prog[s] if s < len(prog) else None)
                    Yo[r, s] = ens.h1()[0]
                    Yc[r, s] = coarse(ens.h0)[0]
            res[f"{c['name']}__Yo"] = Yo
            res[f"{c['name']}__Yc"] = Yc
        np.savez_compressed(out, conds=np.array([c["name"] for c in CONDS]), **res)
        print(name, j, "done", round(time.time() - t_start, 1), "s", flush=True)


if __name__ == "__main__":
    main()
