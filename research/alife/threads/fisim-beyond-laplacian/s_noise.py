import sys, json
from screen import *
from scipy import ndimage
import muts
amp = float(sys.argv[1]); sig = float(sys.argv[2]); T = float(sys.argv[3]) if len(sys.argv) > 3 else 300
g = muts.cellpop(Kg=1.0)
N = 128
rng = np.random.default_rng(0)
S = X.make_state(g, N)
F = S["F"]
F[0] += amp * ndimage.gaussian_filter(rng.standard_normal((N, N)), sig, mode="wrap") * sig
sn, ts, w = run(g, N=N, T=T, F=F)
u0 = g["acts"][0]["u0"]
line = f"cellpop noise IC amp{amp} sig{sig}: wall {w:.0f}s blobs {[blobs(s[0], u0)[0] for s in sn]}"
print(line); open("screens/log.txt", "a").write(line + "\n")
strip(sn, ts, ["u", "v", "w", "m (CH)", "cargo", "glob"], f"screens/cellpop_noise_a{amp}_s{sig}.png", line)
