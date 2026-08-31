"""film_job.py — v2 champion film capture: full activator snapshots on GPU.

Groups jobs by horizon T and rides each group as ONE batched tensor
(init_soup_gpu_batch / advance_gpu_batch — the campaign stepper). Each world
gets a dense snapshot schedule (~40-60 frames) on the CREC grid; full field
snaps land in S["snaps"] via the locked record path. Saves per-world npz.

Usage: python film_job.py <jobs.json> <outdir>
jobs.json: [{"name":..., "genome":{...}, "seed":int, "T":float, "frames":int}]
"""
import json, os, sys, time
import numpy as np
from blobkit.soup import sim_gpu as SG

def snap_schedule(T, frames):
    ts = np.linspace(0.0, T, frames)
    ts = sorted({float(round(t / 25.0) * 25.0) for t in ts} | {0.0, float(T)})
    return ts

def save_world(S, job, outdir):
    g, name = job["genome"], job["name"]
    T = float(job["T"])
    rec = SG.snapshot_rec_gpu(S)
    snaps = rec["snaps"]
    ts_snap = sorted(snaps.keys())
    arr = np.stack([snaps[t] for t in ts_snap]).astype(np.float16)
    ts_rec = np.asarray(rec["t"], float)
    nsteps = len(ts_rec)
    ct = np.zeros(nsteps)
    for i in range(len(g["acts"])):
        bl = rec["blobs"][i]
        for k in range(min(nsteps, len(bl))):
            ct[k] += len(bl[k])
    np.savez_compressed(
        os.path.join(outdir, name + "_film.npz"),
        frames=arr, ts=np.asarray(ts_snap, float),
        rec_ts=ts_rec, rec_ct=ct,
        na=len(g["acts"]), status=rec["status"], T=T, seed=job["seed"],
        genome=json.dumps(g), name=name)
    print(f"[{name}] status={rec['status']} snaps={len(ts_snap)} T={T} "
          f"nblobs_end={ct[-1] if len(ct) else 'na'}", flush=True)

def run_group(group, outdir):
    T = float(group[0]["T"])
    t0 = time.time()
    SS = SG.init_soup_gpu_batch([(j["genome"], j["seed"]) for j in group],
                                L=128.0, dtype="f32")
    for S, j in zip(SS["worlds"], group):
        S["snap_t"] = snap_schedule(T, j.get("frames", 56))
    statuses = SG.advance_gpu_batch(SS, T, overlap=True)
    wall = time.time() - t0
    print(f"group T={T} n={len(group)} statuses={statuses} wall={wall:.1f}s",
          flush=True)
    for S, j in zip(SS["worlds"], group):
        save_world(S, j, outdir)

def main():
    jobs = json.load(open(sys.argv[1]))
    outdir = sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    import blobkit
    lk = blobkit.verify_locks()
    print("verify_locks:", lk["ok"], "n_checked:", lk["n_checked"], flush=True)
    assert lk["ok"], "LOCK DRIFT - abort"
    import jax
    print("jax devices:", jax.devices(), flush=True)
    groups = {}
    for j in jobs:
        groups.setdefault(float(j["T"]), []).append(j)
    for T in sorted(groups):
        run_group(groups[T], outdir)
    print("ALL DONE", flush=True)

if __name__ == "__main__":
    main()
