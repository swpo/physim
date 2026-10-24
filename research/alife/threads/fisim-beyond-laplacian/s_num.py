import sys, json
from screen import *
import muts
g = muts.cellpop(Kg=1.0)
mode = sys.argv[1]
if mode == "dt":
    sn, ts, w = run(g, N=128, T=200, seed=0, dt=0.01)
else:  # dx 0.25 on the same physical domain (N=256): finer grid
    sn, ts, w = run(g, N=192, T=200, seed=0, dx=64/192, dt=0.01)
u0 = g["acts"][0]["u0"]
line = f"cellpop numerics {mode}: wall {w:.0f}s blobs {[blobs(s[0], u0)[0] for s in sn]}"
print(line); open("screens/log.txt", "a").write(line + "\n")
strip(sn, ts, ["u", "v", "w", "m (CH)", "cargo", "glob"], f"screens/cellpop_num_{mode}.png", line)
