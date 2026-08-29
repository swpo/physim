"""e1b_pointerjump.py — E1b: pointer-jumping CCL (label equivalence) in jax.

E1 found: min-neighbor propagation alone needs O(diameter) sweeps (496 on
real labyrinths, 10.3 ms fused for 11 fields — already ~host speed, but
budget-fragile). Classic GPU CCL fix (label-equivalence, Kalentev et al.):
alternate (a) one neighbor-min SWEEP with (b) POINTER JUMPS lab <- lab[lab]
(path compression over the label graph). Chains compress geometrically:
expected O(log diameter) outer iters.

E1b measures: outer iters to converge on the same real fields + a
pathological single-component SPIRAL (diameter ~N^2/8) + wall; device
convergence flag (one extra sweep + compare, returned per field).
E2b: stats on CONVERGED labels -> parity vs blob_list_fast on all lanes.
E4: tiny-row pull cost measured inside e2e.

Rows -> ~/perf/results/experiments.jsonl.
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
    """Single serpentine component, diameter ~N^2/8: worst-case chain."""
    m = np.zeros((N, N), bool)
    for r in range(0, N - 4, 4):
        m[r, 2:N - 2] = True                     # horizontal bar
        if (r // 4) % 2 == 0:
            m[r:r + 5, N - 3] = True             # connect right
        else:
            m[r:r + 5, 2] = True                 # connect left
    return m


# ------------------------------------------------- pointer-jump CCL kernel
def make_pjccl(N, outer, jumps, sweeps_per_outer=2):
    """Jitted pointer-jumping CCL for (B, N, N) bool masks (periodic).
    Returns (labels(B,N,N) int32 pixel-ids, converged(B,) bool)."""
    NN = N * N

    @jax.jit
    def ccl(mask):
        B = mask.shape[0]
        idx = jnp.arange(NN, dtype=jnp.int32).reshape(1, N, N)
        BIG = jnp.int32(NN)
        lab = jnp.where(mask, jnp.broadcast_to(idx, mask.shape), BIG)

        def sweep(lab):
            n1 = jnp.roll(lab, 1, axis=-1)
            n2 = jnp.roll(lab, -1, axis=-1)
            n3 = jnp.roll(lab, 1, axis=-2)
            n4 = jnp.roll(lab, -1, axis=-2)
            m = jnp.minimum(jnp.minimum(n1, n2), jnp.minimum(n3, n4))
            return jnp.where(mask, jnp.minimum(lab, m), lab)

        def jump(labf):
            src = jnp.clip(labf, 0, NN - 1)
            looked = jnp.take_along_axis(labf, src, axis=1)
            return jnp.where(labf < NN, jnp.minimum(labf, looked), labf)

        def outer_body(_, lab):
            for _s in range(sweeps_per_outer):
                lab = sweep(lab)
            labf = lab.reshape(B, NN)
            labf = jax.lax.fori_loop(0, jumps, lambda j, lf: jump(lf), labf)
            return labf.reshape(B, N, N)

        lab = jax.lax.fori_loop(0, outer, outer_body, lab)
        converged = jnp.all(sweep(lab) == lab, axis=(-2, -1))
        return lab, converged

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


def e1b(masks_np, tag, outer_grid=(2, 3, 4, 6, 8)):
    B, N, _ = masks_np.shape
    mask = jnp.asarray(masks_np)
    host_t0 = time.perf_counter()
    for b in range(B):
        G.periodic_label(np.asarray(masks_np[b]))
    host_wall = time.perf_counter() - host_t0

    best = None
    for outer in outer_grid:
        ccl = make_pjccl(N, outer, jumps=12)
        lab, conv = ccl(mask)
        jax.block_until_ready((lab, conv))       # compile
        t0 = time.perf_counter()
        reps = 10
        for _ in range(reps):
            lab, conv = ccl(mask)
        jax.block_until_ready((lab, conv))
        wall = (time.perf_counter() - t0) / reps
        conv_np = np.asarray(conv)
        lab_np = np.asarray(lab)
        part_ok = canon_partition_check(lab_np, masks_np) if conv_np.all() \
            else False
        emit(dict(question="E1b pointer-jump CCL", tag=tag, B=B, N=N,
                  outer=outer, jumps=12,
                  wall_ms=round(1e3 * wall, 2),
                  ms_per_field=round(1e3 * wall / B, 3),
                  host_ms_per_field=round(1e3 * host_wall / B, 3),
                  all_converged=bool(conv_np.all()),
                  n_unconverged=int((~conv_np).sum()),
                  partition_match=bool(part_ok),
                  verdict=("CONVERGED+MATCH" if part_ok else
                           ("CONVERGED, MISMATCH" if conv_np.all()
                            else "UNCONVERGED"))))
        if best is None and conv_np.all() and part_ok:
            best = outer
    return best


# --------------------------------------------------- E2b stats (fixed)
def make_blobstats(N, max_lab):
    ang = 2 * np.pi * (np.arange(N) + 0.5) / N
    cy = jnp.asarray(np.cos(ang), jnp.float32)
    sy = jnp.asarray(np.sin(ang), jnp.float32)
    NN = N * N

    @jax.jit
    def stats(lab, u, thr):
        B = lab.shape[0]
        w = jnp.where(lab < NN,
                      jnp.clip(u - thr[:, None, None], 0.0, None),
                      0.0).astype(jnp.float32)
        flat = lab.reshape(B, NN)
        wf = w.reshape(B, NN)
        uf = u.reshape(B, NN).astype(jnp.float32)
        PYc = jnp.broadcast_to(cy[:, None], (N, N)).reshape(NN)
        PYs = jnp.broadcast_to(sy[:, None], (N, N)).reshape(NN)
        PXc = jnp.broadcast_to(cy[None, :], (N, N)).reshape(NN)
        PXs = jnp.broadcast_to(sy[None, :], (N, N)).reshape(NN)

        order = jnp.argsort(flat, axis=1)
        sl = jnp.take_along_axis(flat, order, axis=1)
        newseg = jnp.concatenate([jnp.ones((B, 1), bool),
                                  sl[:, 1:] != sl[:, :-1]], axis=1)
        newseg = newseg & (sl < NN)              # bg not a segment
        rank_sorted = jnp.cumsum(newseg, axis=1) - 1
        rank = jnp.zeros_like(flat).at[
            jnp.arange(B)[:, None], order].set(rank_sorted)
        rank = jnp.where(flat < NN, jnp.minimum(rank, max_lab), max_lab)
        nlab = rank_sorted[:, -1] + 1            # per-batch component count
        overflow = nlab > max_lab

        def seg(vals):
            out = jnp.zeros((B, max_lab + 1), jnp.float32)
            return out.at[jnp.arange(B)[:, None], rank].add(vals)

        tot = seg(wf)
        area = seg((flat < NN).astype(jnp.float32))
        zyr = seg(wf * PYc[None]); zyi = seg(wf * PYs[None])
        zxr = seg(wf * PXc[None]); zxi = seg(wf * PXs[None])
        peak = jnp.full((B, max_lab + 1), -jnp.inf, jnp.float32).at[
            jnp.arange(B)[:, None], rank].max(uf)
        return (tot[:, :max_lab], area[:, :max_lab], zyr[:, :max_lab],
                zyi[:, :max_lab], zxr[:, :max_lab], zxi[:, :max_lab],
                peak[:, :max_lab], nlab, overflow)

    return stats


def blobs_from_stats(tot, area, zyr, zyi, zxr, zxi, peak, N, dx):
    out = []
    for j in range(tot.shape[0]):
        if area[j] <= 0:
            continue
        if tot[j] <= 0:
            continue
        y = (np.angle((zyr[j] + 1j * zyi[j]) / tot[j]) % (2 * np.pi)) \
            / (2 * np.pi) * N * dx
        x = (np.angle((zxr[j] + 1j * zxi[j]) / tot[j]) % (2 * np.pi)) \
            / (2 * np.pi) * N * dx
        out.append(dict(y=float(y), x=float(x),
                        area=float(area[j]) * dx * dx, peak=float(peak[j])))
    return out


def e2b(fields, tag, outer, dx=0.5):
    names = [n for n, _, _ in fields]
    us64 = [u for _, u, _ in fields]
    thrs = [t for _, _, t in fields]
    masks_np = np.stack([u > t for u, t in zip(us64, thrs)])
    B, N, _ = masks_np.shape
    mask = jnp.asarray(masks_np)
    u32 = jnp.asarray(np.stack(us64).astype(np.float32))
    thr32 = jnp.asarray(np.asarray(thrs, np.float32))
    MAXL = 256
    ccl = make_pjccl(N, outer, jumps=12)
    stats = make_blobstats(N, MAXL)

    lab, conv = ccl(mask)
    rs = stats(lab, u32, thr32)
    jax.block_until_ready(rs)                    # compile both
    t0 = time.perf_counter()
    reps = 10
    for _ in range(reps):
        lab2, conv2 = ccl(mask)
        rs2 = stats(lab2, u32, thr32)
        pulled = [np.asarray(r) for r in rs2]    # E4: tiny-row pull incl.
    e2e = (time.perf_counter() - t0) / reps

    t0 = time.perf_counter()
    ref_lists = [blob_list_fast(u, t, dx, N * dx)
                 for u, t in zip(us64, thrs)]
    host_wall = time.perf_counter() - t0

    tots, areas, zyrs, zyis, zxrs, zxis, peaks, nlab, ovf = pulled
    match, worst, n_mismatch = True, 0.0, 0
    for b in range(B):
        dev_bl = blobs_from_stats(tots[b], areas[b], zyrs[b], zyis[b],
                                  zxrs[b], zxis[b], peaks[b], N, dx)
        ref_bl = ref_lists[b]
        if len(dev_bl) != len(ref_bl):
            match = False; n_mismatch += 1
            emit(dict(question="E2b parity DETAIL", tag=tag, lane=b,
                      name=names[b], n_dev=len(dev_bl), n_ref=len(ref_bl),
                      nlab=int(nlab[b]), overflow=bool(ovf[b]),
                      converged=bool(np.asarray(conv2)[b])))
            continue
        sd = sorted(dev_bl, key=lambda d: (d["y"], d["x"]))
        sr = sorted(ref_bl, key=lambda d: (d["y"], d["x"]))
        for db, rb in zip(sd, sr):
            for k_ in ("y", "x", "area", "peak"):
                err = abs(db[k_] - rb[k_]) / max(abs(rb[k_]), 1e-9)
                worst = max(worst, err)
                if err > 1e-5:
                    match = False; n_mismatch += 1
    emit(dict(question="E2b converged stats + parity", tag=tag, B=B, N=N,
              outer=outer, max_lab=MAXL,
              dev_e2e_ms=round(1e3 * e2e, 2),
              dev_e2e_ms_per_field=round(1e3 * e2e / B, 3),
              host_bloblist_ms=round(1e3 * host_wall, 2),
              host_ms_per_field=round(1e3 * host_wall / B, 3),
              speedup_per_field=round(host_wall / e2e, 2),
              n_blobs_ref=[len(r) for r in ref_lists],
              parity_match=bool(match), n_mismatch=n_mismatch,
              worst_rel_err=float(worst),
              verdict=("PARITY OK" if match else "PARITY FAIL")))


def main():
    print("[e1b] building real states...", flush=True)
    fields = real_fields()
    masks = np.stack([u > t for _, u, t in fields])
    N = masks.shape[-1]
    # real fields + the pathological spiral as an extra lane
    sp = spiral_mask(N)
    masks_sp = np.concatenate([masks, sp[None]], axis=0)
    print(f"[e1b] {masks_sp.shape[0]} masks (11 real + spiral), N={N}",
          flush=True)
    best = e1b(masks_sp, tag="real+spiral")
    print(f"[e1b] smallest converging outer: {best}", flush=True)
    outer = best or 8
    e2b(fields, tag="real-adv-T1000", outer=outer)


if __name__ == "__main__":
    main()
