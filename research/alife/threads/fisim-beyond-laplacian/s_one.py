import sys, json
from screen import *
import muts
name = sys.argv[1]; args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
T = float(sys.argv[3]) if len(sys.argv) > 3 else 200
g = getattr(muts, name)(**args)
sn, ts, w = run(g, N=128, T=T, seed=0)
u0 = g["acts"][0]["u0"]
tag = name + "_" + "_".join(f"{k}{v}" for k, v in args.items())
nb = [blobs(s[0], u0)[0] for s in sn]; occ = blobs(sn[-1][0], u0)[1]
fw = front_width(sn[-1][0], u0)
line = f"{tag}: wall {w:.0f}s blobs {nb} occ {occ:.3f} width {fw:.2f} finite {np.isfinite(sn[-1]).all()}"
print(line); open("screens/log.txt", "a").write(line + "\n")
strip(sn, ts, ["u"] + [f"x{c}" for c in range(len(g["chans"]))], f"screens/{tag}.png", tag)
