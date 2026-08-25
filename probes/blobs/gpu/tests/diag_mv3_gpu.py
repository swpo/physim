"""tests/diag_mv3_gpu.py — GPU mv3 seeds 4-8 (pre-registered extension for the
parity investigation; NOT a re-roll: seeds fixed a priori, all reported)."""
import sys, os, time
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(_HERE, "..")))
import blobgpu.soup as BS
import soup_sim
from tests.gt_worlds import world, KICKS

SEEDS = (4, 5, 6, 7, 8)
RUNS = os.path.join(os.path.normpath(os.path.join(_HERE, "..")), "results",
                    "parity_runs")

jobs = [(world("mv3"), s) for s in SEEDS]
SS = BS.init_soup_gpu_batch(jobs, L=128.0, dtype="f32", kicks_map=KICKS)
for S in SS["worlds"]:
    S["snap_t"] = sorted({0.0, 250.0, 2500.0, 5000.0})
t0 = time.time()
BS.advance_gpu_batch(SS, 5000.0, progress=lambda t: print(f"t={t:.0f}", flush=True))
print("wall", round(time.time() - t0, 1), flush=True)
for s, S in zip(SEEDS, SS["worlds"]):
    rec = BS.snapshot_rec_gpu(S)
    soup_sim.save_run(rec, os.path.join(RUNS, f"gpu_mv3_s{s}.npz"))
    print("saved s%d status=%s" % (s, rec["status"]), flush=True)
