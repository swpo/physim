#!/usr/bin/env python
"""make_prodmix.py — build perf/data/prodmix.json.gz from the deepsearch
final CPU harvest (provenance tool; run ONCE, output is FROZEN).

The T2 'assay-mix' benchmark needs a prod-distribution lane mix: real evolved
genomes with their measured T_used stamps, matching the union joint
(nf_bucket, T) distribution. This script samples that from
l0/deepsearch/final_cpu_harvest/results_evo2-*.json (2516 ds2_eval rows;
2079 assayed with ladder T_used).

Measured joint (n=2079, share %):
  bucket |  2500   5000  10000  20000 | share
    b4   |  318      3      0      0  | 15.4
    b7   |  295     34     14     14  | 17.2
    b10  |  234     43     20     12  | 14.9
    b14  |  588    188    219     97  | 52.5
  T share: 2500 69.0 / 5000 12.9 / 10000 12.2 / 20000 5.9

Output entries: {genome, cand, phase, nf, bucket, T_stamp, interest, seed}.
Sampling: deterministic (seed 20260828), up to CAP_PER_CELL diverse cands per
(bucket, T) cell, preferring higher interest (those are the lanes that shape
prod walls). Cell weights are stored so benchconfigs can build ANY lane count
with largest-remainder allocation.
"""
import collections, glob, gzip, json, os, sys

import numpy as np

HARVEST = os.environ.get(
    "BLOBKIT_HARVEST",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                 "l0", "deepsearch", "final_cpu_harvest"))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "data", "prodmix.json.gz")
LADDER = (2500.0, 5000.0, 10000.0, 20000.0)
BUCKETS = (4, 7, 10, 14)
CAP_PER_CELL = 12
SEED = 20260828


def bucket_of(nf):
    for b in BUCKETS:
        if nf <= b:
            return b
    return int(nf)


def main():
    rows = []
    for p in sorted(glob.glob(os.path.join(HARVEST, "results_evo2-*.json"))):
        rows += json.load(open(p))
    cells = collections.defaultdict(list)
    joint = collections.Counter()
    for r in rows:
        if r.get("kind") != "ds2_eval" or r.get("T_used") not in LADDER:
            continue
        g = r.get("genome")
        if not isinstance(g, dict):
            continue
        nf = len(g["acts"]) + len(g["chans"])
        b = bucket_of(nf)
        T = float(r["T_used"])
        joint[(b, T)] += 1
        cells[(b, T)].append(r)
    rng = np.random.default_rng(SEED)
    sample, weights = [], {}
    for (b, T), rs in sorted(cells.items()):
        weights[f"{b}|{int(T)}"] = len(rs)
        # prefer ok + high interest, then shuffle for diversity
        rs = sorted(rs, key=lambda r: -(r.get("interest") or 0.0))
        top = rs[: max(CAP_PER_CELL * 3, 12)]
        idx = rng.permutation(len(top))[:CAP_PER_CELL]
        seen = set()
        for i in sorted(idx):
            r = top[i]
            gid = r.get("ghash") or r.get("cand")
            if gid in seen:
                continue
            seen.add(gid)
            g = r["genome"]
            sample.append(dict(
                genome=g, cand=r.get("cand"), phase=r.get("phase"),
                nf=len(g["acts"]) + len(g["chans"]), bucket=b,
                T_stamp=T, interest=round(float(r.get("interest") or 0.0), 2),
                status=r.get("status"), seed=int(r.get("seed") or 1)))
    out = dict(
        v=1, seed=SEED, harvest=os.path.abspath(HARVEST),
        n_source_rows=int(sum(joint.values())),
        joint={f"{b}|{int(T)}": int(n) for (b, T), n in sorted(joint.items())},
        entries=sample)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with gzip.open(OUT, "wt") as f:
        json.dump(out, f)
    print(f"wrote {OUT}: {len(sample)} entries, "
          f"{len(out['joint'])} cells, source n={out['n_source_rows']}")


if __name__ == "__main__":
    main()
