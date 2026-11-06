"""Input visibility: constrained inputs applied to saved test states, against the no-input twin
(the base trajectory itself: same state, same noise seed and key, so identical noise).

usage: python run_inputs.py WORLD J0 J1 STATE_INDEX TMAX
Placements: random cells; body cells (sources and sinks inside tracked bodies); bite (sources in
bodies, sinks in empty space >= 8 px from any body). Values: half the k coordinates at -b, half at
+b (zero sum). Conditions beyond the default constraint (k > 8 or sum|a| > 4) are designer probes."""
import os
import sys
import time

import numpy as np
import scipy.ndimage as ndi

import lenia_world as LW
vw = LW.vw

CONDS = [
    dict(name="none", place="none", k=0, b=0.0, ticks=1),
    dict(name="rand_k2_b1", place="random", k=2, b=1.0, ticks=1),
    dict(name="rand_k8_b0.5", place="random", k=8, b=0.5, ticks=1),
    dict(name="rand_k32_b1", place="random", k=32, b=1.0, ticks=1),
    dict(name="body_k2_b1", place="body", k=2, b=1.0, ticks=1),
    dict(name="body_k8_b0.125", place="body", k=8, b=0.125, ticks=1),
    dict(name="body_k8_b0.5", place="body", k=8, b=0.5, ticks=1),
    dict(name="body_k8_b1", place="body", k=8, b=1.0, ticks=1),
    dict(name="body_k32_b1", place="body", k=32, b=1.0, ticks=1),
    dict(name="bite_k8_b0.5", place="bite", k=8, b=0.5, ticks=1),
    dict(name="body_k8_b0.5_x8", place="body", k=8, b=0.5, ticks=8),
    dict(name="rand_k8_b0.5_x8", place="random", k=8, b=0.5, ticks=8),
]
TAUS_L0 = (1, 2, 4, 8, 16, 24, 32)


def far_empty(mask, dmin):
    H, W = mask.shape
    tile = np.tile(~mask, (3, 3))
    dist = ndi.distance_transform_edt(tile)[H:2 * H, W:2 * W]
    return np.flatnonzero((dist >= dmin).ravel())


def choose_cells(rng, place, k, h0, m, l0, tr):
    HW = l0.HW
    body = m[:HW] > 0
    S = h0.reshape(l0.C, HW).sum(0)
    if place == "random":
        cells = rng.choice(HW, k, replace=False)
        return cells[: k // 2], cells[k // 2:]
    bc = np.flatnonzero(body & (S > 1e-3))
    if place == "body":
        cells = rng.choice(bc, k, replace=False)
        return cells[: k // 2], cells[k // 2:]
    if place == "bite":
        src = rng.choice(bc, k // 2, replace=False)
        snk = rng.choice(far_empty(body.reshape(l0.H, l0.W), 8.0), k - k // 2, replace=False)
        return src, snk
    raise ValueError(place)


def main():
    name, j0, j1, si, tmax = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    specs, parts = LW.make_specs(name)
    l0, tr, coarse = parts["l0"], parts["tracker"], parts["phi_coarse"]
    w = vw.VectorWorld(specs["objects"], world_seed=0)
    inv = LW.inverse_in_map(w)
    C = w.spec.inputs
    for j in range(j0, j1):
        out = f"data/{name}/inputs_{j:03d}_s{si}.npz"
        if os.path.exists(out):
            continue
        t_start = time.time()
        d = np.load(f"data/{name}/base_{j:03d}.npz")
        keys = [tuple(k) for k in d["l0_keys"]]
        t0 = int(d["st_tick"][si]) - int(d["burn_in"])
        res = {}
        for ci, c in enumerate(CONDS):
            if c["place"] == "none" and j - j0 >= 3:
                continue
            rng = np.random.default_rng([5, j, si, ci])
            ens = vw.Ensemble(w, d["st_h0"][si][None], d["st_m"][si][None], tuple(int(x) for x in d["seed"]), [0],
                              int(d["st_tick"][si]))
            Yo, Yc, l0d, moved, on_matter, admissible, cells_log = [], [], [], [], [], [], []
            for s in range(tmax):
                a = None
                if c["place"] != "none" and s < c["ticks"]:
                    src, snk = choose_cells(rng, c["place"], c["k"], ens.h0[0], ens.m[0], l0, tr)
                    a = np.zeros(w.n_in)
                    a[inv[src]] = -c["b"]
                    a[inv[snk]] = c["b"]
                    adict = {int(i): float(a[i]) for i in np.flatnonzero(a)}
                    admissible.append(not C.violations(adict, 0, None, 0.0))
                    u = np.zeros((1, w.spec.n_u))
                    u[:, w.in_map] = a
                    hk = l0.kick(ens.h0, u)
                    moved.append(0.5 * float(np.abs(hk - ens.h0).sum()))
                    body = ens.m[0, :l0.HW] > 0          # tracked-body pixels
                    on_matter.append([int(body[src].sum()), int(body[snk].sum())])
                    cells_log.append(np.concatenate([src, snk]))
                ens.step(a)
                Yo.append(ens.h1()[0])
                Yc.append(coarse(ens.h0)[0])
                if (t0, s + 1) in keys:
                    ref = d["l0_snap"][keys.index((t0, s + 1))].astype(float)
                    l0d.append(float(np.abs(ens.h0[0] - ref).sum()))
            res[c["name"]] = dict(Yo=np.array(Yo), Yc=np.array(Yc), l0diff=np.array(l0d), moved=np.array(moved),
                                  on_matter=np.array(on_matter), admissible=np.array(admissible),
                                  cells=np.array(cells_log) if cells_log else np.zeros((0, 0)))
        flat = {f"{cn}__{k}": v for cn, r in res.items() for k, v in r.items()}
        np.savez_compressed(out, t0=t0, conds=np.array([c["name"] for c in CONDS]), **flat)
        print(name, j, "done", round(time.time() - t_start, 1), "s", flush=True)


if __name__ == "__main__":
    main()
