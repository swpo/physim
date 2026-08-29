"""e1_labelprop.py — E1+E2: device blob-stats feasibility on REAL states.

E1: iterative min-neighbor label propagation (periodic) in jax on real
advanced activator fields: iters to converge + wall/iter, fused (B*na, N, N).
Baseline: G.periodic_label (scipy label + python union-find) on host.
E2: given labels, per-blob mass/area/centroid(circular mean)/peak via
one fused segment pass; wall vs the host bincount path (blob_list_fast).

Appends rows to ~/perf/results/experiments.jsonl.
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
    print("[row]", json.dumps(row, default=str)[:400], flush=True)


# ---------------------------------------------------------- real states
def real_masks(L=128.0, T=1000.0):
    """Advanced states for worlds with rich structure; returns list of
    (name, act_idx, u_f64, thr) — the exact inputs _record hands to
    blob_list_fast."""
    out = []
    for name in ("m0", "pred", "coex", "ds3_014"):
        g = W.load(name)
        S = SC.init_soup(g, L=L, seed=1, workers=4)
        SC.advance(S, T)
        for i in range(S["na"]):
            u = np.asarray(S["F"][i], np.float64)
            out.append((name, i, u, float(S["thr_a"][i])))
    return out


# ------------------------------------------------------------- E1 kernel
def make_labelprop(N, iters):
    """One jitted label-prop sweep block: labels (B, N, N) int32,
    mask (B, N, N) bool. Min-neighbor propagation with PERIODIC rolls.
    Returns (labels, changed_any) after `iters` sweeps."""

    @jax.jit
    def block(lab, mask):
        def body(_, carry):
            lab, _ = carry
            n1 = jnp.roll(lab, 1, axis=-1)
            n2 = jnp.roll(lab, -1, axis=-1)
            n3 = jnp.roll(lab, 1, axis=-2)
            n4 = jnp.roll(lab, -1, axis=-2)
            m = jnp.minimum(jnp.minimum(n1, n2), jnp.minimum(n3, n4))
            new = jnp.where(mask, jnp.minimum(lab, m), lab)
            return new, jnp.any(new != lab)
        lab, changed = jax.lax.fori_loop(0, iters, body, (lab, jnp.array(True)))
        return lab, changed

    return block


def init_labels(mask):
    B, N, _ = mask.shape
    idx = jnp.arange(N * N, dtype=jnp.int32).reshape(N, N)[None]
    BIG = jnp.int32(N * N + 7)
    return jnp.where(mask, idx, BIG)


def e1(masks_np, tag):
    """masks_np: (B, N, N) bool block of REAL masks."""
    B, N, _ = masks_np.shape
    mask = jnp.asarray(masks_np)
    lab0 = init_labels(mask)
    block8 = make_labelprop(N, 8)
    # convergence loop: 8 sweeps per block, check flag between blocks
    lab, _ = block8(lab0, mask)      # compile
    lab.block_until_ready()
    t0 = time.perf_counter()
    lab = lab0
    total_iters = 0
    for k in range(64):              # cap 512 sweeps
        lab, changed = block8(lab, mask)
        total_iters += 8
        if not bool(changed):        # host sync per block (8 sweeps)
            break
    lab.block_until_ready()
    conv_wall = time.perf_counter() - t0

    # steady-state wall/iter at the converged iteration count, no syncs
    blockK = make_labelprop(N, total_iters)
    lab2, _ = blockK(lab0, mask)
    lab2.block_until_ready()
    t0 = time.perf_counter()
    reps = 5
    for _ in range(reps):
        lab2, _ = blockK(lab0, mask)
    lab2.block_until_ready()
    fused_wall = (time.perf_counter() - t0) / reps

    # host baseline: G.periodic_label per field
    t0 = time.perf_counter()
    ks = []
    for b in range(B):
        _, k = G.periodic_label(np.asarray(masks_np[b]))
        ks.append(k)
    host_wall = time.perf_counter() - t0

    # correctness: same component PARTITION as periodic_label?
    lab_np = np.asarray(lab)
    ok = True
    for b in range(B):
        ref, k = G.periodic_label(np.asarray(masks_np[b]))
        dev = lab_np[b]
        # canonicalize: map each device root label to ref label where mask
        m = np.asarray(masks_np[b])
        pairs = set(zip(dev[m].ravel().tolist(), ref[m].ravel().tolist()))
        # bijective <=> same partition
        d2r = {}
        r2d = {}
        good = True
        for d, r in pairs:
            if d2r.setdefault(d, r) != r or r2d.setdefault(r, d) != d:
                good = False
                break
        ok &= good
    emit(dict(question="E1 labelprop feasibility", tag=tag, B=B, N=N,
              iters_to_converge=total_iters,
              conv_wall_ms=round(1e3 * conv_wall, 2),
              fused_wall_ms=round(1e3 * fused_wall, 2),
              fused_ms_per_field=round(1e3 * fused_wall / B, 3),
              host_periodic_label_ms=round(1e3 * host_wall, 2),
              host_ms_per_field=round(1e3 * host_wall / B, 3),
              n_components=ks, partition_match=bool(ok),
              verdict=("FEASIBLE" if ok else "PARTITION MISMATCH")))
    return lab_np, ok


# ------------------------------------------------------------- E2 kernel
def make_blobstats(N, dx, max_lab):
    """Given converged labels (B,N,N) + field u (B,N,N) + thr (B,), compute
    per-label stats via one fused segment pass. Labels are pixel ids
    (0..N*N-1, sparse); we bincount into length max_lab bins after
    compacting via sort-free scatter-add (jnp .at adds).
    Returns arrays (B, max_lab): tot, area, zy_re, zy_im, zx_re, zx_im, peak.
    max_lab: max blobs per field we extract (rows beyond -> dropped;
    counted in overflow)."""
    ang = 2 * np.pi * (np.arange(N) + 0.5) / N
    cy = jnp.asarray(np.cos(ang)); sy = jnp.asarray(np.sin(ang))

    @jax.jit
    def stats(lab, u, thr):
        B = lab.shape[0]
        w = jnp.where(lab < N * N, jnp.clip(u - thr[:, None, None], 0.0,
                                            None), 0.0)
        mask = lab < N * N
        # compact labels: unique-ify via sort of flattened labels
        flat = lab.reshape(B, -1)
        wf = w.reshape(B, -1)
        uf = u.reshape(B, -1)
        PYc = jnp.broadcast_to(cy[:, None], (N, N)).reshape(-1)
        PYs = jnp.broadcast_to(sy[:, None], (N, N)).reshape(-1)
        PXc = jnp.broadcast_to(cy[None, :], (N, N)).reshape(-1)
        PXs = jnp.broadcast_to(sy[None, :], (N, N)).reshape(-1)

        # dense-rank labels per batch row: sort labels, positions where
        # value changes = new rank. O(N^2 log N^2) sort on device.
        order = jnp.argsort(flat, axis=1)
        sorted_lab = jnp.take_along_axis(flat, order, axis=1)
        newseg = jnp.concatenate(
            [jnp.ones((B, 1), bool),
             sorted_lab[:, 1:] != sorted_lab[:, :-1]], axis=1)
        rank_sorted = jnp.cumsum(newseg, axis=1) - 1     # 0-based ranks
        rank = jnp.zeros_like(flat).at[
            jnp.arange(B)[:, None], order].set(rank_sorted)
        rank = jnp.where(flat < N * N, rank, max_lab)    # bg -> overflow bin
        rank = jnp.minimum(rank, max_lab)                # clamp (+1 bin)

        def seg(vals):
            out = jnp.zeros((B, max_lab + 1), vals.dtype)
            return out.at[jnp.arange(B)[:, None], rank].add(vals)

        tot = seg(wf)
        area = seg(mask.reshape(B, -1).astype(jnp.float32))
        zyr = seg(wf * PYc[None]); zyi = seg(wf * PYs[None])
        zxr = seg(wf * PXc[None]); zxi = seg(wf * PXs[None])
        peak = jnp.full((B, max_lab + 1), -jnp.inf, uf.dtype).at[
            jnp.arange(B)[:, None], rank].max(uf)
        nlab = rank_sorted[:, -1] + 1     # includes bg rank... approximate
        return tot[:, :max_lab], area[:, :max_lab], zyr[:, :max_lab], \
            zyi[:, :max_lab], zxr[:, :max_lab], zxi[:, :max_lab], \
            peak[:, :max_lab], nlab

    return stats


def blobs_from_stats(tot, area, zyr, zyi, zxr, zxi, peak, N, dx, thr_np):
    """Host-side: assemble blob dicts from device stat rows (tiny)."""
    out = []
    for j in range(tot.shape[0]):
        if tot[j] <= 0:
            continue
        y = (np.angle((zyr[j] + 1j * zyi[j]) / tot[j]) % (2 * np.pi)) \
            / (2 * np.pi) * N * dx
        x = (np.angle((zxr[j] + 1j * zxi[j]) / tot[j]) % (2 * np.pi)) \
            / (2 * np.pi) * N * dx
        out.append(dict(y=float(y), x=float(x),
                        area=float(area[j]) * dx * dx,
                        peak=float(peak[j])))
    return out


def e2(masks_np, fields, thrs, names, tag, dx=0.5):
    B, N, _ = masks_np.shape
    mask = jnp.asarray(masks_np)
    u = jnp.asarray(np.stack(fields).astype(np.float32))
    thr = jnp.asarray(np.asarray(thrs, np.float32))
    lab0 = init_labels(mask)
    blockK = make_labelprop(N, 64)
    lab, _ = blockK(lab0, mask)
    MAXL = 256
    stats = make_blobstats(N, dx, MAXL)
    rs = stats(lab, u, thr)
    jax.block_until_ready(rs)          # compile
    t0 = time.perf_counter()
    reps = 5
    for _ in range(reps):
        rs = stats(lab, u, thr)
        jax.block_until_ready(rs)
    dev_wall = (time.perf_counter() - t0) / reps

    # end-to-end (label + stats + pull tiny rows)
    t0 = time.perf_counter()
    for _ in range(reps):
        lab2, _ = blockK(lab0, mask)
        rs2 = stats(lab2, u, thr)
        pulled = [np.asarray(r) for r in rs2[:7]]
    dev_e2e = (time.perf_counter() - t0) / reps

    # host baseline: blob_list_fast per field (f64, the real path)
    t0 = time.perf_counter()
    ref_lists = [blob_list_fast(np.asarray(f, np.float64), t_, dx, N * dx)
                 for f, t_ in zip(fields, thrs)]
    host_wall = time.perf_counter() - t0

    # parity: same blob multisets (y, x, area, peak), sorted by (y, x)
    tots, areas, zyrs, zyis, zxrs, zxis, peaks = pulled
    match, worst = True, 0.0
    for b in range(B):
        dev_bl = blobs_from_stats(tots[b], areas[b], zyrs[b], zyis[b],
                                  zxrs[b], zxis[b], peaks[b], N, dx,
                                  thrs[b])
        ref_bl = ref_lists[b]
        if len(dev_bl) != len(ref_bl):
            match = False
            emit(dict(question="E2 parity DETAIL", tag=tag, lane=b,
                      name=names[b], n_dev=len(dev_bl), n_ref=len(ref_bl)))
            continue
        sd = sorted(dev_bl, key=lambda d: (d["y"], d["x"]))
        sr = sorted(ref_bl, key=lambda d: (d["y"], d["x"]))
        for db, rb in zip(sd, sr):
            for k_ in ("y", "x", "area", "peak"):
                err = abs(db[k_] - rb[k_]) / max(abs(rb[k_]), 1e-9)
                worst = max(worst, err)
                if err > 5e-3:
                    match = False
    emit(dict(question="E2 segment reductions + parity", tag=tag, B=B, N=N,
              max_lab=MAXL,
              dev_stats_ms=round(1e3 * dev_wall, 2),
              dev_e2e_ms=round(1e3 * dev_e2e, 2),
              dev_e2e_ms_per_field=round(1e3 * dev_e2e / B, 3),
              host_bloblist_ms=round(1e3 * host_wall, 2),
              host_ms_per_field=round(1e3 * host_wall / B, 3),
              n_blobs_ref=[len(r) for r in ref_lists],
              parity_match=bool(match),
              worst_rel_err=float(worst),
              verdict=("PARITY OK" if match else "PARITY FAIL")))


def main():
    print("[e1] building real states...", flush=True)
    fields = real_masks()
    names = [f"{n}/a{i}" for n, i, _, _ in fields]
    masks = np.stack([u > thr for _, _, u, thr in fields])
    us = [u for _, _, u, _ in fields]
    thrs = [thr for _, _, _, thr in fields]
    print(f"[e1] {len(fields)} real fields: {names}", flush=True)
    lab, ok = e1(masks, tag="real-adv-T1000")
    e2(masks, us, thrs, names, tag="real-adv-T1000")


if __name__ == "__main__":
    main()
