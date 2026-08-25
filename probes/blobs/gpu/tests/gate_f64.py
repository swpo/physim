"""tests/gate_f64.py — CORRECTNESS GATE 1: f64 trajectory parity at T=100tu.

For each of the 7 ground-truth worlds: run the locked CPU kernel (soup_sim_v2,
f64, noise=0) and the GPU kernel (blobgpu, f64, noise=0) from the SAME
init_soup state (bit-identical ICs, same numpy RNG), T=100tu, L=128.
Gate: relative L2 field error < 1e-5 per world. Also runs the same with the
worlds batched into ONE padded tensor (the production shape).

Writes results/gate_f64.json. Run on any backend; the pod run is the record.
"""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..")))
import blobgpu.soup as BS
import soup_sim_v2 as V2
from tests.gt_worlds import world as gt_world, KICKS, NAMES as GT_NAMES

OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "results", "gate_f64.json"))
T_GATE = 100.0
NAMES = GT_NAMES


def main():
    import jax
    rows, fails = [], []
    # --- single-world path
    cpu_final = {}
    for name in NAMES:
        g = gt_world(name)
        kicks = KICKS.get(g["id"])
        t0 = time.time()
        Sc = V2.init_soup(g, L=128.0, seed=1, dtype="f64", noise=0.0,
                          kicks=kicks, workers=4)
        V2.advance(Sc, T_GATE)
        cpu_s = time.time() - t0
        cpu_final[name] = np.asarray(Sc["F"], np.float64)

        t0 = time.time()
        Sg = BS.init_soup_gpu(g, L=128.0, seed=1, dtype="f64", noise=0.0,
                              kicks=kicks)
        BS.advance_gpu(Sg, T_GATE)
        gpu_s = time.time() - t0
        a = np.asarray(Sg["F"], np.float64)
        rel = float(np.linalg.norm(a - cpu_final[name])
                    / np.linalg.norm(cpu_final[name]))
        ok = rel < 1e-5
        rows.append(dict(world=name, mode="single", relL2=rel,
                         cpu_s=round(cpu_s, 1), gpu_s=round(gpu_s, 1),
                         gate="PASS" if ok else "FAIL"))
        print(f"{name:5s} single relL2={rel:.3e} [{rows[-1]['gate']}]",
              flush=True)
        if not ok:
            fails.append((name, "single", rel))

    # --- batched path (all 7 in one tensor)
    jobs = [(gt_world(n), 1) for n in NAMES]
    SS = BS.init_soup_gpu_batch(jobs, L=128.0, dtype="f64", noise=0.0,
                                kicks_map=KICKS)
    BS.advance_gpu_batch(SS, T_GATE)
    for name, S in zip(NAMES, SS["worlds"]):
        a = np.asarray(S["F"], np.float64)
        rel = float(np.linalg.norm(a - cpu_final[name])
                    / np.linalg.norm(cpu_final[name]))
        ok = rel < 1e-5
        rows.append(dict(world=name, mode="batched7", relL2=rel,
                         gate="PASS" if ok else "FAIL"))
        print(f"{name:5s} batch7 relL2={rel:.3e} [{rows[-1]['gate']}]",
              flush=True)
        if not ok:
            fails.append((name, "batch", rel))

    out = dict(kind="gate_f64", T=T_GATE, L=128.0, noise=0.0,
               backend=str(jax.devices()[0]),
               ts=time.strftime("%Y-%m-%d %H:%M:%S"),
               rows=rows, verdict="PASS" if not fails else "FAIL")
    hist = []
    if os.path.exists(OUT):
        hist = json.load(open(OUT))
    hist.append(out)
    json.dump(hist, open(OUT, "w"), indent=1)
    print("GATE-F64:", out["verdict"])
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
