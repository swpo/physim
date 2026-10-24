"""Run the mca-MIRd neutral arm with mutation off and save full states at regular times (branch points).

python branch_states.py world.py OUTDIR SEED STEPS EVERY [SIZE]
"""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from labkit.world import load_world  # noqa: E402

W = load_world(sys.argv[1]); out = Path(sys.argv[2]); seed = int(sys.argv[3]); steps = int(sys.argv[4]); every = int(sys.argv[5])
size = int(sys.argv[6]) if len(sys.argv) > 6 else 192
W.EFF = 0.0; W.MU_CELL = 0.0
s = W.init(seed, (size, size))
out.mkdir(parents=True, exist_ok=True)
for t in range(1, steps + 1):
    s = W.step(s)
    if t % every == 0 and t >= 2000:
        np.savez_compressed(out / f"state_s{seed}_t{t}.npz", A=s["A"], F=s["F"], a=s["a"], t=t)
print("done", seed)
