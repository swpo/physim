"""e1c_scattermin.py — E1c: root-merging CCL (scatter-min union) in jax.

E1b verdict: sweep+jump alone stalls (unions land at PIXELS and must
re-propagate). Classic GPU label-equivalence (Kalentev/Playne) merges at
ROOTS: for every neighbor pair, scatter-min the neighbor's root into the
pixel's ROOT slot — jnp's .at[].min IS that scatter. Expected O(log)
outer iterations even on serpentine components.

Per outer iter: [jumps x path-compress lab<-lab[lab]] -> neighbor-min of
compressed labels (periodic rolls) -> scatter-min into root slots.
Convergence flag on device (one extra iter must be a no-op).

Grid: outer x jumps on 11 real fields + spiral (diameter ~N^2/8) + E2b
parity rerun on converged labels. Rows -> experiments.jsonl.
"""
import json, os, time
import numpy as np

import jax
import jax.numpy as jnp

from blobkit import worlds as W
from blobkit import genome as G
from blobkit.soup import sim_cpu as SC
from blobkit.soup.sim_v1 import blob_list_fast

OUT = os.path.expanduser("~/perf/results/experiments.jsonl")


def emit(row):
    row["ts"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(OUT, "a") as f:
        f.write(json.dumps(row, default=str) + "\n")
    print("[row]", json.dumps(row, default=str)[:500], flush=True)


def real_fields(L=128.0, T=1000.0):
    out = []
    for name in ("m0", "pred", "coex", "ds3_014"):
        g = W.load(name)
        S = SC.init_soup(g, L=L, seed=1, workers=4)
        SC.advance(S, T)
        for i in range(S["na"]):
            u = np.asarray(S["F"][i], np.float64)
            out.append((f"{name}/a{i}", u, float(S["thr_a"][i])))
    return out


def spiral_mask(N):
    m = np.zeros((N, N), bool)
    for r in range(0, N - 4, 4):
        m[r, 2:N - 2] = True
        if (r // 4) % 2 == 0:
            m[r:r + 5, N - 3] = True
        else:
            m[r:r + 5, 2] = True
    return m


def make_ccl(N, outer, jumps):
    """Root-merging CCL. mask (B,N,N) bool -> labels (B,N,N) int32
    (component = min pixel id), converged (B,) bool."""
    NN = N * N

    @jax.jit
    def ccl(mask):
        B = mask.shape[0]
        idx = jnp.arange(NN, dtype=jnp.int32).reshape(1, N, N)
        BIG = jnp.int32(NN)
        lab0 = jnp.where(mask, jnp.broadcast_to(idx, mask.shape), BIG)
        # flat label table with a background SINK slot at index NN
        labf = jnp.concatenate(
            [lab0.reshape(B, NN), jnp.full((B, 1), BIG, jnp.int32)], axis=1)
        brow = jnp.arange(B)[:, None]

        def compress(labf):
            def jmp(_, lf):
                tgt = jnp.take_along_axis(lf, lf[:, :NN], axis=1)
                return lf.at[:, :NN].set(jnp.minimum(lf[:, :NN], tgt))
            return jax.lax.fori_loop(0, jumps, jmp, labf)

        def outer_body(_, labf):
            labf = compress(labf)
            lab2 = labf[:, :NN].reshape(B, N, N)
            n1 = jnp.roll(lab2, 1, axis=-1)
            n2 = jnp.roll(lab2, -1, axis=-1)
            n3 = jnp.roll(lab2, 1, axis=-2)
            n4 = jnp.roll(lab2, -1, axis=-2)
            nmin = jnp.minimum(jnp.minimum(n1, n2), jnp.minimum(n3, n4))
            nmin = jnp.where(mask, nmin, BIG).reshape(B, NN)
            roots = labf[:, :NN]
            # union at the ROOT slot (the Kalentev merge):
            return labf.at[brow, roots].min(nmin)

        labf = jax.lax.fori_loop(0, outer, outer_body, labf)
        labf = compress(labf)
        # converged <=> one more outer step is a no-op
        probe = outer_body(0, labf)
        probe = compress(probe)
        converged = jnp.all(probe[:, :NN] == labf[:, :NN], axis=1)
        return labf[:, :NN].reshape(B, N, N), converged

    return ccl


def canon_partition_check(lab_np, masks_np):
    ok = True
    for b in range(lab_np.shape[0]):
        ref, k = G.periodic_label(np.asarray(masks_np[b]))
        m = np.asarray(masks_np[b])
        if not m.any():
            continue
        pairs = set(zip(lab_np[b][m].ravel().tolist(),
                        ref[m].ravel().tolist()))
        d2r, r2d = {}, {}
        for d, r in pairs:
            if d2r.setdefault(d, r) != r or r2d.setdefault(r, d) != d:
                ok = False
                break
    return ok


def e1c(masks_np, tag):
    B, N, _ = masks_np.shape
    mask = jnp.asarray(masks_np)
    host_t0 = time.perf_counter()
    for b in range(B):
        G.periodic_label(np.asarray(masks_np[b]))
    host_wall = time.perf_counter() - host_t0
    best = None
    for outer, jumps in ((3, 4), (4, 4), (4, 8), (6, 8), (8, 8), (8, 16)):
        ccl = make_ccl(N, outer, jumps)
        lab, conv = ccl(mask)
        jax.block_until_ready((lab, conv))
        t0 = time.perf_counter()
        reps = 20
        for _ in range(reps):
            lab, conv = ccl(mask)
        jax.block_until_ready((lab, conv))
        wall = (time.perf_counter() - t0) / reps
        conv_np = np.asarray(conv)
        lab_np = np.asarray(lab)
        part_ok = canon_partition_check(lab_np, masks_np) \
            if conv_np.all() else False
        emit(dict(question="E1c scatter-min CCL", tag=tag, B=B, N=N,
                  outer=outer, jumps=jumps,
                  wall_ms=round(1e3 * wall, 3),
                  ms_per_field=round(1e3 * wall / B, 4),
                  host_ms_per_field=round(1e3 * host_wall / B, 3),
                  all_converged=bool(conv_np.all()),
                  n_unconverged=int((~conv_np).sum()),
                  partition_match=bool(part_ok),
                  verdict=("CONVERGED+MATCH" if part_ok else
                           ("CONVERGED, MISMATCH" if conv_np.all()
                            else "UNCONVERGED"))))
        if best is None and conv_np.all() and part_ok:
            best = (outer, jumps)
    return best


def main():
    import e1b_pointerjump as E1B     # reuse stats/parity harness
    print("[e1c] building real states...", flush=True)
    fields = real_fields()
    masks = np.stack([u > t for _, u, t in fields])
    N = masks.shape[-1]
    sp = spiral_mask(N)
    masks_sp = np.concatenate([masks, sp[None]], axis=0)
    print(f"[e1c] {masks_sp.shape[0]} masks (11 real + spiral), N={N}",
          flush=True)
    best = e1c(masks_sp, tag="real+spiral")
    print(f"[e1c] best (outer, jumps): {best}", flush=True)
    if best is None:
        emit(dict(question="E1c verdict", verdict="NO CONFIG CONVERGED"))
        return
    outer, jumps = best
    # E2 rerun on the converged CCL: swap make_pjccl for make_ccl
    E1B.make_pjccl = lambda N_, o_, jumps=jumps: make_ccl(N_, o_, jumps)
    E1B.e2b(fields, tag=f"e1c-o{outer}j{jumps}", outer=outer)


if __name__ == "__main__":
    main()
