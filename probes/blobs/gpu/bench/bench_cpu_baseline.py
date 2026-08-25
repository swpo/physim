"""bench/bench_cpu_baseline.py — measured CPU equivalents for the headline table.
Runs the LOCKED CPU pipeline (soup_sim_v2) for short horizons and reports
ms/step; scaled to worlds/hour for the headline shapes. Local M-series core.
"""
import os, sys, time, json
HERE = os.path.dirname(os.path.abspath(__file__))
GPU = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, GPU)
import numpy as np
from tests.gt_worlds import world, KICKS
sys.path.insert(0, os.path.normpath(os.path.join(GPU, "..", "l0", "complexity")))
sys.path.insert(0, os.path.normpath(os.path.join(GPU, "..", "l0", "stage2", "lib")))
import soup_sim_v2 as V2
from bench.bench_step import append

def cpu_soup(world_name, T=100.0, L=128.0, workers=1):
    g = world(world_name)
    S = V2.init_soup(g, L=L, seed=1, dtype="f32", kicks=KICKS.get(g["id"]),
                     workers=workers)
    t0 = time.time()
    V2.advance(S, T)
    wall = time.time() - t0
    steps = int(round(T / 0.02))
    return wall, wall / steps * 1e3, S

if __name__ == "__main__":
    for name, T, L in (("pred", 100.0, 128.0), ("pred", 100.0, 256.0),
                       ("pred", 50.0, 512.0)):
        for wk in (1, 4):
            wall, ms, S = cpu_soup(name, T, L, workers=wk)
            row = dict(kind="cpu_baseline", world=name, T=T, L=L, N=int(L/0.5),
                       workers=wk, wall_s=round(wall, 1),
                       ms_per_step=round(ms, 3),
                       backend="numpy+scipy.fft M-series core")
            append(row)
            print(json.dumps(row), flush=True)
