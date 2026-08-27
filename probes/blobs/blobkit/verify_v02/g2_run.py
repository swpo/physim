"""verify_v02/g2_run.py — G2: driver-refactored sim_gpu vs PRE-refactor copy.
CPU-JAX f64 (no local GPU; refactor-identity only — device gates rerun on next
pod deployment). Compares EXACT record streams (ts/blobs/mass/ct/patches/orgs/
memf/snaps/T/status + final F) for:
  A. single world m4 s1, chunked 250 -> 500 tu   (advance_gpu)
  B. batch [m4 s1, mv3 s1(kicks)], chunked 250 -> 500 tu, overlap=True
     (advance_gpu_batch)
"""
import json, os, sys, time

import numpy as np

sys.path.insert(0, "/tmp/bkpre")               # blobkit_pre (pre-refactor copy)
os.environ.setdefault("BLOBKIT_RESULTS", "")

import blobkit
from blobkit import worlds
import blobkit.soup.sim_gpu as NEW
import blobkit_pre.soup.sim_gpu as PRE

REPORT = {}


def deep_eq(a, b, path="$"):
    """Exact (bitwise for arrays) structural compare; returns list of diffs."""
    diffs = []
    if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
        a2, b2 = np.asarray(a), np.asarray(b)
        if a2.shape != b2.shape or a2.dtype != b2.dtype:
            diffs.append(f"{path}: shape/dtype {a2.shape}/{a2.dtype} vs {b2.shape}/{b2.dtype}")
        elif not np.array_equal(a2, b2, equal_nan=True):
            i = np.argwhere(a2 != b2)
            diffs.append(f"{path}: {len(i)} differing elements, first at {i[0].tolist()}")
        return diffs
    if isinstance(a, dict) and isinstance(b, dict):
        if set(a) != set(b):
            diffs.append(f"{path}: keys {sorted(set(a) ^ set(b))}")
        for k in sorted(set(a) & set(b), key=str):
            diffs += deep_eq(a[k], b[k], f"{path}.{k}")
        return diffs
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        if len(a) != len(b):
            diffs.append(f"{path}: len {len(a)} vs {len(b)}")
        for i, (x, y) in enumerate(zip(a, b)):
            diffs += deep_eq(x, y, f"{path}[{i}]")
        return diffs
    if a != b:
        diffs.append(f"{path}: {a!r} vs {b!r}")
    return diffs


def rec_of(mod, S):
    r = mod.snapshot_rec(S) if hasattr(mod, "snapshot_rec") else mod.snapshot_rec_gpu(S)
    r = dict(r)
    r.pop("wall_s", None)
    return r


def run_single(mod, g, kicks):
    S = mod.init_soup_gpu(g, L=128.0, seed=1, dtype="f64", kicks=kicks)
    for T in (250.0, 500.0):
        st = mod.advance_gpu(S, T)
        if st != "ok":
            break
    r = rec_of(mod, S)
    r["_F"] = np.asarray(S["F"], np.float64)
    r["_t_step"] = S["t_step"]
    return r


def run_batch(mod, jobs, kicks_map):
    SS = mod.init_soup_gpu_batch(jobs, L=128.0, dtype="f64", kicks_map=kicks_map)
    for T in (250.0, 500.0):
        mod.advance_gpu_batch(SS, T, overlap=True)
    out = []
    for S in SS["worlds"]:
        r = rec_of(mod, S)
        r["_t_step"] = S["t_step"]
        out.append(r)
    return out


def main():
    m4 = worlds.WORLDS["m4"]()
    mv3 = worlds.WORLDS["mv3"]()
    kicks_map = dict(worlds.KICKS)

    t0 = time.time()
    a_pre = run_single(PRE, worlds.WORLDS["m4"](), None)
    t1 = time.time()
    a_new = run_single(NEW, worlds.WORLDS["m4"](), None)
    t2 = time.time()
    dA = deep_eq(a_pre, a_new)
    REPORT["A_single_m4_s1_T500_f64"] = dict(
        match=not dA, diffs=dA[:10], T=a_pre["T"], status=a_pre["status"],
        n_ts=len(a_pre["t"]), n_ct=len(a_pre["ct"]),
        wall_pre=round(t1 - t0, 1), wall_new=round(t2 - t1, 1))

    jobs = [(worlds.WORLDS["m4"](), 1), (worlds.WORLDS["mv3"](), 1)]
    t3 = time.time()
    b_pre = run_batch(PRE, [(worlds.WORLDS["m4"](), 1), (worlds.WORLDS["mv3"](), 1)], kicks_map)
    t4 = time.time()
    b_new = run_batch(NEW, [(worlds.WORLDS["m4"](), 1), (worlds.WORLDS["mv3"](), 1)], kicks_map)
    t5 = time.time()
    dB = deep_eq(b_pre, b_new)
    REPORT["B_batch_m4+mv3_T500_f64_overlap"] = dict(
        match=not dB, diffs=dB[:10],
        T=[r["T"] for r in b_pre], status=[r["status"] for r in b_pre],
        wall_pre=round(t4 - t3, 1), wall_new=round(t5 - t4, 1))

    ok = all(v["match"] for v in REPORT.values())
    REPORT["gate"] = "G2"
    REPORT["pass"] = ok
    REPORT["note"] = ("CPU-JAX f64 refactor-identity; GPU-device gates rerun "
                      "on next pod deployment")
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "G2_driver_identity.json")
    json.dump(REPORT, open(out, "w"), indent=1, default=str)
    print(json.dumps(REPORT, indent=1, default=str))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
