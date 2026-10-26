"""Run the world headless and save its event logs: python simulate.py MODE LO T OUTDIR SEEDS..."""
import sys, os, time, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import world
mode, lo, T, out = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
os.makedirs(out, exist_ok=True)
for s in map(int, sys.argv[5:]):
    t0 = time.time(); S = world.init(s, p=dict(mode=mode, lo=lo, maxev=max(1_000_000, 420 * T)))
    for _ in range(T): world.step(S)
    L = world.logs(S); np.savez_compressed(f"{out}/m{mode}_lo{lo}_s{s}.npz", **L)
    print(out, s, f"{time.time()-t0:.0f}s pop={L['pop'][-1]} reps={len(L['rep_t'])} uniq={len(np.unique(L['rep_k']))} overflow={L['overflow']}", flush=True)
