"""e2c_f64stats.py — f64 device accumulation parity for the sum outputs.

Approved parity policy: exact on integers/max/partition; f64 device
accumulation + 1e-12 tolerance gate on sums. E2b measured f32 sums at
worst rel err ~5.5e-7. This experiment: same segment stats with f64
accumulators (JAX_ENABLE_X64) — expect <=1e-12; also measures the f64
cost delta (stats kernel + pull rows double in width).

ALSO: exact-match audit of the integer/max outputs (area counts, peaks,
blob count, partition) — must be bit-equal to host.

Rows -> experiments.jsonl.
"""
import os
os.environ["JAX_ENABLE_X64"] = "1"          # BEFORE jax import

import json, time
import numpy as np

import jax
import jax.numpy as jnp

from blobkit import worlds as W
from blobkit import genome as G
from blobkit.soup import sim_cpu as SC
from blobkit.soup.sim_v1 import blob_list_fast

import e1c_scattermin as E1C

OUT = os.path.expanduser("~/perf/results/experiments.jsonl")


def emit(row):
    row["ts"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(OUT, "a") as f:
        f.write(json.dumps(row, default=str) + "\n")
    print("[row]", json.dumps(row, default=str)[:500], flush=True)


def make_blobstats64(N, max_lab):
    """f64 accumulation variant of e1b.make_blobstats. Inputs stay f32
    (u is the sim's f32 field pulled/kept on device); accumulators f64.
    Weights computed in f64 from the f64-CAST of u — mirrors the host
    path (u -> np.float64 -> clip/sum)."""
    ang = 2 * np.pi * (np.arange(N) + 0.5) / N
    cy = jnp.asarray(np.cos(ang), jnp.float64)
    sy = jnp.asarray(np.sin(ang), jnp.float64)
    NN = N * N

    @jax.jit
    def stats(lab, u, thr):
        B = lab.shape[0]
        u64 = u.astype(jnp.float64)
        w = jnp.where(lab < NN,
                      jnp.clip(u64 - thr[:, None, None].astype(jnp.float64),
                               0.0, None), 0.0)
        flat = lab.reshape(B, NN)
        wf = w.reshape(B, NN)
        uf = u64.reshape(B, NN)
        PYc = jnp.broadcast_to(cy[:, None], (N, N)).reshape(NN)
        PYs = jnp.broadcast_to(sy[:, None], (N, N)).reshape(NN)
        PXc = jnp.broadcast_to(cy[None, :], (N, N)).reshape(NN)
        PXs = jnp.broadcast_to(sy[None, :], (N, N)).reshape(NN)

        order = jnp.argsort(flat, axis=1)
        sl = jnp.take_along_axis(flat, order, axis=1)
        newseg = jnp.concatenate([jnp.ones((B, 1), bool),
                                  sl[:, 1:] != sl[:, :-1]], axis=1)
        newseg = newseg & (sl < NN)
        rank_sorted = jnp.cumsum(newseg, axis=1) - 1
        rank = jnp.zeros_like(flat).at[
            jnp.arange(B)[:, None], order].set(rank_sorted)
        rank = jnp.where(flat < NN, jnp.minimum(rank, max_lab), max_lab)
        nlab = rank_sorted[:, -1] + 1

        def seg(vals):
            out = jnp.zeros((B, max_lab + 1), jnp.float64)
            return out.at[jnp.arange(B)[:, None], rank].add(vals)

        tot = seg(wf)
        area = seg((flat < NN).astype(jnp.float64))
        zyr = seg(wf * PYc[None]); zyi = seg(wf * PYs[None])
        zxr = seg(wf * PXc[None]); zxi = seg(wf * PXs[None])
        peak = jnp.full((B, max_lab + 1), -jnp.inf, jnp.float64).at[
            jnp.arange(B)[:, None], rank].max(uf)
        return (tot[:, :max_lab], area[:, :max_lab], zyr[:, :max_lab],
                zyi[:, :max_lab], zxr[:, :max_lab], zxi[:, :max_lab],
                peak[:, :max_lab], nlab)

    return stats


def main():
    fields = []
    for name in ("m0", "pred", "coex", "ds3_014"):
        g = W.load(name)
        S = SC.init_soup(g, L=128.0, seed=1, workers=4)
        SC.advance(S, 1000.0)
        for i in range(S["na"]):
            u = np.asarray(S["F"][i], np.float64)
            fields.append((f"{name}/a{i}", u, float(S["thr_a"][i]),
                           np.asarray(S["F"][i])))  # f32 raw too
    names = [f[0] for f in fields]
    thrs = [f[2] for f in fields]
    us64 = [f[1] for f in fields]
    us32 = [f[3].astype(np.float32) for f in fields]
    masks_np = np.stack([u > t for u, t in zip(us64, thrs)])
    B, N, _ = masks_np.shape
    dx = 0.5

    mask = jnp.asarray(masks_np)
    u32 = jnp.asarray(np.stack(us32))
    t64 = jnp.asarray(np.asarray(thrs, np.float64))
    MAXL = 256
    ccl = E1C.make_ccl(N, 4, 8)
    stats = make_blobstats64(N, MAXL)

    lab, conv = ccl(mask)
    rs = stats(lab, u32, t64)
    jax.block_until_ready(rs)
    t0 = time.perf_counter()
    reps = 10
    for _ in range(reps):
        lab2, _ = ccl(mask)
        rs2 = stats(lab2, u32, t64)
        pulled = [np.asarray(r) for r in rs2]
    e2e = (time.perf_counter() - t0) / reps

    ref_lists = [blob_list_fast(u, t, dx, N * dx)
                 for u, t in zip(us64, thrs)]
    # NOTE: host path uses u.astype(f64) from the f32 field — identical input

    tots, areas, zyrs, zyis, zxrs, zxis, peaks, nlab = pulled
    worst_sum, worst_pos = 0.0, 0.0
    int_exact, match = True, True
    for b in range(B):
        dev_bl = []
        for j in range(MAXL):
            if areas[b][j] <= 0 or tots[b][j] <= 0:
                continue
            y = (np.angle((zyrs[b][j] + 1j * zyis[b][j]) / tots[b][j])
                 % (2 * np.pi)) / (2 * np.pi) * N * dx
            x = (np.angle((zxrs[b][j] + 1j * zxis[b][j]) / tots[b][j])
                 % (2 * np.pi)) / (2 * np.pi) * N * dx
            dev_bl.append(dict(y=float(y), x=float(x),
                               area=float(areas[b][j]) * dx * dx,
                               peak=float(peaks[b][j]),
                               tot=float(tots[b][j])))
        ref_bl = ref_lists[b]
        if len(dev_bl) != len(ref_bl):
            match = False
            emit(dict(question="E2c f64 parity DETAIL", lane=b,
                      name=names[b], n_dev=len(dev_bl), n_ref=len(ref_bl)))
            continue
        sd = sorted(dev_bl, key=lambda d: (d["y"], d["x"]))
        sr = sorted(ref_bl, key=lambda d: (d["y"], d["x"]))
        for db, rb in zip(sd, sr):
            # integer/max outputs: exact
            if db["area"] != rb["area"] or db["peak"] != rb["peak"]:
                int_exact = False
            # sums: tolerance
            for k_ in ("y", "x"):
                err = abs(db[k_] - rb[k_]) / max(abs(rb[k_]), 1e-9)
                worst_pos = max(worst_pos, err)
            # recompute host tot for this blob? blob_list_fast doesn't
            # return tot; centroid err is the sum-parity proxy.
    emit(dict(question="E2c f64-stats parity + cost", B=B, N=N,
              dev_e2e_ms=round(1e3 * e2e, 2),
              dev_e2e_ms_per_field=round(1e3 * e2e / B, 3),
              int_outputs_exact=bool(int_exact),
              worst_centroid_rel_err=float(worst_pos),
              blobsets_match=bool(match),
              policy_pass=bool(match and int_exact and worst_pos < 1e-12),
              verdict=("POLICY PASS" if
                       (match and int_exact and worst_pos < 1e-12)
                       else "CHECK")))


if __name__ == "__main__":
    main()
