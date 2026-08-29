"""benchconfigs.py — packaged benchmark configurations for blobkit perf work.

RULE (perf governance, IDEAS.md 2026-08-28): any blobkit perf claim requires
evidence from THESE benchmarks. Three tiers, minutes-not-hours, prod-like:

  T1 'kernel'    (~2-5 min)  pure batched stepping: (B, nf_bucket) grid,
                             us/world-step + pull/launch/record microbenches.
  T2 'assay-mix' (~5-15 min) prod-distribution lane mix through the REAL
                             run_assay_batch ladder incl. full battery —
                             THE prod-like worlds/hour number.
  T3 'gen-sim'   (~15-25 min, optional) one synthetic generation end-to-end
                             (screens -> confirm lanes with t0 floors).

Every config is DETERMINISTIC: fixed lanes (frozen prodmix sample or packaged
worlds), fixed seeds, fixed ladders. A config name means the same workload
forever — changed workloads get NEW names (t2_v2, ...), so rows stay
comparable across blobkit versions (bench.py compare joins on the workload
hash). Device is a runtime choice (--device); scale is a config choice:

  prod-scale configs (t2, t3, t1 profile 'gpu'): L=128 grid (N=256), the
    locked prod ladder 2500->20000. Minutes on an H100-class device; hours
    on a laptop — run them on the pod.
  mini configs (t2mini, t2smoke, t3mini, t1 profile 'cpu'): SAME code paths,
    same distribution SHAPE, scaled substrate (L=64 -> N=128, ladder
    1250->5000, lane t0 floors = prod stamps scaled by cap_mini/cap_prod).
    ~2-12 min on laptop CPU-JAX. Mini w/h is comparable ACROSS VERSIONS on
    the same device class, not to prod-scale numbers.

Lane source: perf/data/prodmix.json.gz — 127 evolved genomes sampled from the
deepsearch final CPU harvest (2079 assayed rows) preserving the measured
joint (nf_bucket, T_used) distribution:

    bucket |  2500   5000  10000  20000 | share%
      b4   |  318      3      0      0  | 15.4
      b7   |  295     34     14     14  | 17.2
      b10  |  234     43     20     12  | 14.9
      b14  |  588    188    219     97  | 52.5

(69% of assayed worlds stop at the base rung; 5.9% ride to cap. Confirm
lanes carry a t0 floor = their screen's T_used: 82% of harvest confirms
stopped exactly at the stamp, 18% extended past it, 0% below.)

Grouping/order mirror pod_worker_batch 0.3.2: one call per (L, ladder-class,
nf_bucket), descending expected-T inside a call, lane chunks of bmax.
"""
import gzip
import hashlib
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PRODMIX = os.path.join(HERE, "data", "prodmix.json.gz")

LADDER = (2500.0, 5000.0, 10000.0, 20000.0)
PROD_CAP = 20000.0
BUCKETS = (4, 7, 10, 14)

# packaged-world representatives per nf bucket (worlds.py registry) — T1
# fallback when prodmix lacks a bucket, and smoke material.
BUCKET_WORLDS = {
    4: ["m0", "bf", "m4"],
    7: ["xv", "s2_128_26", "s2_118_41"],
    10: ["pred", "coex", "mv3"],
    14: ["ds3_014", "ds3_017"],
}


# --------------------------------------------------------------- prodmix
def load_prodmix():
    with gzip.open(PRODMIX, "rt") as f:
        return json.load(f)


def bucket_of(nf):
    for b in BUCKETS:
        if nf <= b:
            return b
    return int(nf)


def _cell_entries(pm):
    """{(bucket, T): [entries...]} in frozen file order (deterministic)."""
    cells = {}
    for e in pm["entries"]:
        cells.setdefault((e["bucket"], e["T_stamp"]), []).append(e)
    return cells


def largest_remainder(weights, n):
    """Allocate n slots over weighted cells; deterministic, sum == n."""
    keys = sorted(weights)
    tot = float(sum(weights[k] for k in keys))
    quota = {k: n * weights[k] / tot for k in keys}
    base = {k: int(quota[k]) for k in keys}
    left = n - sum(base.values())
    for k in sorted(keys, key=lambda k: (-(quota[k] - base[k]), str(k))):
        if left <= 0:
            break
        base[k] += 1
        left -= 1
    return base


# ------------------------------------------------------------------- T1
# kernel cells: (name, B, bucket, nsteps) at the profile's grid N.
# nsteps sized so a timed rep is ~1-5 s on the profile's device class
# (us/world-step is nsteps-invariant; median of 3 reps).
T1_PROFILES = {
    "gpu": dict(
        N=256,
        cells=[("b4_B32", 32, 4, 2500), ("b7_B32", 32, 7, 2500),
               ("b10_B32", 32, 10, 2500), ("b14_B32", 32, 14, 2500),
               ("b14_B8", 8, 14, 2500), ("b14_B64", 64, 14, 2500),
               ("b14_B96", 96, 14, 2500)],
        pullcadence=dict(B=32, bucket=14, chunk=250, n_chunks=20),
        launch=dict(B=8, bucket=4, n=200),
        record_worlds=["m0", "pred"], record_reps=50,
    ),
    "cpu": dict(
        N=256,
        cells=[("b4_B1", 1, 4, 1500), ("b4_B4", 4, 4, 500),
               ("b7_B4", 4, 7, 300), ("b10_B4", 4, 10, 250),
               ("b14_B4", 4, 14, 150), ("b14_B8", 8, 14, 80)],
        pullcadence=dict(B=4, bucket=14, chunk=250, n_chunks=4),
        launch=dict(B=4, bucket=4, n=50),
        record_worlds=["m0", "pred"], record_reps=30,
    ),
}


def t1_lanes(bucket, B, pm=None):
    """Deterministic lane genomes for a T1 cell: prodmix entries of that
    bucket (frozen order, highest-T cells first: the expensive prod lanes),
    cycled to B; packaged worlds as fallback."""
    pm = pm or load_prodmix()
    cells = _cell_entries(pm)
    pool = [e["genome"] for T in sorted(LADDER, reverse=True)
            for e in cells.get((bucket, T), [])]
    if not pool:
        from blobkit import worlds
        pool = [worlds.load(n) for n in BUCKET_WORLDS[bucket]]
    return [pool[i % len(pool)] for i in range(B)]


# ------------------------------------------------------------------- T2
# Lane mixes drawn from the prodmix joint (bucket, T) cells by largest
# remainder. Confirm-phase entries keep a t0 floor = their stamp scaled to
# the config ladder (async-confirm contract); screens enter at t0.
T2_CONFIGS = {
    # prod tier: 16 lanes, prod grid + ladder. ~10 min H100-class @0.3.2;
    # DO NOT run on laptop (hours).
    "t2": dict(n_lanes=16, L=128.0, t0=2500.0, cap=20000.0, bmax=16,
               B_pad=None,           # engine default (4, 8, 16, 32)
               note="prod-distribution 16-lane mix, prod ladder, N=256"),
    # local tier: same shape, scaled substrate. ~10 min laptop CPU-JAX.
    "t2mini": dict(n_lanes=6, L=64.0, t0=1250.0, cap=5000.0, bmax=8,
                   B_pad=(1, 2, 3, 4, 6, 8),
                   note="scaled local mix: N=128, ladder 1250->5000"),
    # CI smoke: 2 lanes, one rung, ~2-3 min laptop. Path proof + counters,
    # not a perf tier.
    "t2smoke": dict(n_lanes=2, L=64.0, t0=1250.0, cap=1250.0, bmax=8,
                    B_pad=(1, 2, 3, 4, 6, 8),
                    note="2-lane smoke, cap=t0 (single rung), N=128"),
}


def snap_floor(T_stamp, t0, cap):
    """Scale a prod T_used stamp onto a config ladder: multiply by
    cap/PROD_CAP, snap to the t0*2^k grid, clamp to [t0, cap]."""
    v = float(T_stamp) * float(cap) / PROD_CAP
    k = round(math.log2(max(v, t0) / t0))
    return float(min(max(t0 * 2 ** k, t0), cap))


def build_t2_lanes(config, pm=None):
    """-> list of lane dicts {genome, seed, t0, cap, bucket, cand, phase,
    T_stamp} allocated over the prodmix joint (bucket, T) distribution."""
    cfg = T2_CONFIGS[config]
    pm = pm or load_prodmix()
    cells = _cell_entries(pm)
    weights = {}
    for k, v in pm["joint"].items():
        b, T = k.split("|")
        weights[(int(b), float(T))] = v
    alloc = largest_remainder(weights, cfg["n_lanes"])
    lanes = []
    for key in sorted(alloc, key=lambda k: (-k[1], -k[0])):  # heavy T first
        n = alloc[key]
        pool = cells.get(key) or cells.get((key[0], 2500.0)) or []
        # confirms FIRST (stable): floors are a-priori (t0 stamps), so they
        # exercise multi-rung ladders on ANY substrate; screens with high
        # T_stamp only extend if the (scaled) dynamics happen to fire.
        pool = ([e for e in pool if e["phase"] in ("seed2", "seed3", "lane")]
                + [e for e in pool if e["phase"] not in
                   ("seed2", "seed3", "lane")])
        for i in range(n):
            e = pool[i % len(pool)]
            confirm = e["phase"] in ("seed2", "seed3", "lane")
            t0 = (snap_floor(e["T_stamp"], cfg["t0"], cfg["cap"])
                  if confirm else None)
            lanes.append(dict(
                genome=e["genome"], seed=int(e["seed"]),
                t0=t0, cap=cfg["cap"], bucket=key[0],
                cand=e["cand"], phase=e["phase"], T_stamp=e["T_stamp"]))
    return lanes


def group_lanes(lanes, bmax):
    """pod_worker_batch 0.3.2 grouping: one call per nf_bucket (single L and
    ladder-class inside a config), DESCENDING expected T inside a call,
    chunks of bmax. -> list of lane-index lists (call order)."""
    def expected_T(ln):
        return ln["t0"] or ln.get("T_stamp") or 2500.0
    groups = {}
    for i, ln in enumerate(lanes):
        groups.setdefault(ln["bucket"], []).append(i)
    calls = []
    for b in sorted(groups):
        idx = sorted(groups[b], key=lambda i: -expected_T(lanes[i]))
        for k in range(0, len(idx), bmax):
            calls.append(idx[k:k + bmax])
    return calls


# ------------------------------------------------------------------- T3
T3_CONFIGS = {
    # one synthetic generation, prod scale: 64 screens + top-6 x 2 confirms.
    "t3": dict(n_screen=64, n_confirm=6, L=128.0, t0=2500.0, cap=20000.0,
               bmax=32, B_pad=None, seed=20260829,
               note="synthetic generation, prod scale"),
    # local: 6 screens + top-2 x 2 confirms on the mini substrate.
    "t3mini": dict(n_screen=6, n_confirm=2, L=64.0, t0=1250.0, cap=5000.0,
                   bmax=8, B_pad=(1, 2, 3, 4, 6, 8), seed=20260829,
                   note="scaled local generation"),
}


def build_t3_screens(config, pm=None):
    """Synthetic generation screens: mutate prodmix parents (top interest)
    with the packaged operators. Deterministic per config seed."""
    import numpy as np
    from blobkit import operators as OPS
    cfg = T3_CONFIGS[config]
    pm = pm or load_prodmix()
    parents = sorted(pm["entries"],
                     key=lambda e: (-e["interest"], e["cand"]))[:24]
    rng = np.random.default_rng(cfg["seed"])
    out = []
    for i in range(cfg["n_screen"]):
        p = parents[i % len(parents)]
        g = OPS.mutate(p["genome"], rng)
        g["id"] = f"bench_{config}_{i:03d}"
        nf = len(g["acts"]) + len(g["chans"])
        out.append(dict(genome=g, seed=1, t0=None, cap=cfg["cap"],
                        bucket=bucket_of(nf), cand=g["id"], phase="screen",
                        T_stamp=None))
    return out


# ---------------------------------------------------------------- hashing
def workload_hash(lanes, extra=None):
    """Identity of a benchmark workload: genomes+seeds+ladders(+extra).
    Rows carry it; compare joins on it (same hash = same work)."""
    payload = [(ln["genome"], ln.get("seed"), ln.get("t0"), ln.get("cap"))
               for ln in lanes]
    s = json.dumps(payload, sort_keys=True, default=str)
    if extra:
        s += json.dumps(extra, sort_keys=True, default=str)
    return hashlib.sha256(s.encode()).hexdigest()[:12]
