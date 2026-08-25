"""tests/gate_parity.py — Gate PARITY runner: GPU soup runs for the locked assay.

On the pod: python tests/gate_parity.py run   -> runs 7 worlds x seeds 1-3
  (f32, noise 2e-3, T=5000, L=128, protocol verbatim via soup_sim_v2.init_soup
  + GPU batched stepping in ONE tensor of 21 worlds) and saves
  results/parity_runs/gpu_<world>_s<seed>.npz (soup_sim.save_run format).

Locally: python tests/gate_parity.py score  -> scores the npz runs with the
  LOCKED metrics_v1 (sys.path -> l0/complexity, untouched) and applies the
  band gate from GATES.md against v1_scores_all.json.
"""
import glob, json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
GPU = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, GPU)
RUNS = os.path.join(GPU, "results", "parity_runs")
CPLX = os.path.normpath(os.path.join(GPU, "..", "l0", "complexity"))

from tests.gt_worlds import world as gt_world, KICKS, NAMES   # noqa: E402

SEEDS = (1, 2, 3)


def run():
    import blobgpu.soup as BS
    import soup_sim
    os.makedirs(RUNS, exist_ok=True)
    jobs, meta = [], []
    for name in NAMES:
        for seed in SEEDS:
            g = gt_world(name)
            jobs.append((g, seed))
            meta.append((name, seed, g["id"]))
    t0 = time.time()
    SS = BS.init_soup_gpu_batch(jobs, L=128.0, dtype="f32",
                                kicks_map=KICKS)
    for S in SS["worlds"]:
        S["snap_t"] = sorted({0.0, 250.0, 2500.0, 5000.0})
    BS.advance_gpu_batch(SS, 5000.0,
                         progress=lambda t: print(f"t={t:.0f}", flush=True))
    wall = time.time() - t0
    print(f"batch of {len(jobs)} worlds T=5000 done in {wall:.0f}s", flush=True)
    for (name, seed, gid), S in zip(meta, SS["worlds"]):
        rec = BS.snapshot_rec_gpu(S)
        pth = os.path.join(RUNS, f"gpu_{name}_s{seed}.npz")
        soup_sim.save_run(rec, pth)
        print(f"saved {pth} status={rec['status']} T={rec['T']}", flush=True)
    json.dump(dict(wall_s=wall, n=len(jobs),
                   ts=time.strftime("%Y-%m-%d %H:%M:%S")),
              open(os.path.join(RUNS, "run_meta.json"), "w"), indent=1)


def score():
    sys.path.insert(0, CPLX)
    import soup_sim
    import metrics_v1 as M
    ref = json.load(open(os.path.join(CPLX, "v1_scores_all.json")))
    got, rows = {}, []
    for pth in sorted(glob.glob(os.path.join(RUNS, "gpu_*_s*.npz"))):
        rec = soup_sim.load_run(pth)
        out = M.full_battery(rec)
        base = os.path.basename(pth)[4:-4]          # <world>_s<seed>
        name, seed = base.rsplit("_s", 1)
        got[f"gt_{name}_s{seed}"] = out["interest"]
        rows.append(dict(world=name, seed=int(seed),
                         interest=round(out["interest"], 2),
                         C={k: round(v, 3) for k, v in out["C"].items()}))
        print(base, round(out["interest"], 2), flush=True)

    # band gate (GATES.md)
    verdicts = {}
    drifts = []
    order_cpu, order_gpu = [], []
    for name in NAMES:
        cpu = [ref[f"gt_{name}_s{s}"]["interest"] for s in SEEDS]
        gpu = [got.get(f"gt_{name}_s{s}") for s in SEEDS]
        if any(v is None for v in gpu):
            verdicts[name] = dict(P1=False, P2=False, missing=True)
            continue
        lo, hi = min(cpu), max(cpu)
        wid = max(0.25 * (hi - lo), 1.0)
        band = (lo - wid, hi + wid)
        mean_gpu = float(np.mean(gpu))
        P1 = band[0] <= mean_gpu <= band[1]
        P2 = sum(band[0] <= v <= band[1] for v in gpu) >= 2
        drifts.append(mean_gpu - float(np.mean(cpu)))
        order_cpu.append(float(np.mean(cpu)))
        order_gpu.append(mean_gpu)
        verdicts[name] = dict(cpu=cpu, gpu=[round(v, 2) for v in gpu],
                              band=[round(band[0], 2), round(band[1], 2)],
                              mean_gpu=round(mean_gpu, 2), P1=P1, P2=P2)
        print(f"{name:5s} cpu={[round(c,1) for c in cpu]} "
              f"gpu={[round(v,1) for v in gpu]} band={verdicts[name]['band']}"
              f" P1={P1} P2={P2}", flush=True)
    # P3: rank of means where CPU bands are disjoint
    P3 = True
    for i, ni in enumerate(NAMES):
        for j, nj in enumerate(NAMES):
            if i >= j or ni not in verdicts or nj not in verdicts:
                continue
            ci = verdicts[ni].get("cpu"); cj = verdicts[nj].get("cpu")
            if ci is None or cj is None:
                continue
            if max(ci) < min(cj):        # disjoint, i strictly below j
                if not verdicts[ni]["mean_gpu"] < verdicts[nj]["mean_gpu"]:
                    P3 = False
                    print(f"P3 violated: {ni} !< {nj}")
    P4 = abs(float(np.mean(drifts))) <= 2.0 if drifts else False
    P1a = all(v.get("P1") for v in verdicts.values())
    P2a = all(v.get("P2") for v in verdicts.values())
    verdict = "PASS" if (P1a and P2a and P3 and P4) else "FAIL"
    out = dict(kind="gate_parity", ts=time.strftime("%Y-%m-%d %H:%M:%S"),
               rows=rows, verdicts=verdicts,
               P1=P1a, P2=P2a, P3=P3, P4=P4,
               mean_drift=round(float(np.mean(drifts)), 3) if drifts else None,
               verdict=verdict)
    pth = os.path.join(GPU, "results", "gate_parity.json")
    hist = json.load(open(pth)) if os.path.exists(pth) else []
    hist.append(out)
    json.dump(hist, open(pth, "w"), indent=1)
    print("GATE-PARITY:", verdict, "drift:", out["mean_drift"])
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "score"
    if mode == "run":
        run()
    else:
        raise SystemExit(score())
