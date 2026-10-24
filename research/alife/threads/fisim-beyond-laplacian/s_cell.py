import sys, json
from screen import *
import muts
args = json.loads(sys.argv[1]); T = float(sys.argv[2]) if len(sys.argv) > 2 else 200
fn = args.pop("fn", "cell"); g = getattr(muts, fn)(**args)
sn, ts, w = run(g, N=128, T=T, seed=0)
u0 = g["acts"][0]["u0"]
tag = fn + "_" + "_".join(f"{k}{v}" for k, v in args.items())
F = sn[-1]; z = F[0] - u0; m = F[3]; c = F[4]
body = z > 0.45 * (np.sqrt(2) - u0)
from scipy import ndimage
near = ndimage.binary_dilation(body, iterations=8) & ~ndimage.binary_dilation(body, iterations=3)
far = ~ndimage.binary_dilation(body, iterations=8)
ratio = c[body].mean() / max(abs(c[far].mean()), 1e-6)
line = f"{tag}: wall {w:.0f}s blobs {[blobs(s[0], u0)[0] for s in sn]} width {front_width(F[0], u0):.2f} cargo in/far {c[body].mean():.3f}/{c[far].mean():.4f} ratio {ratio:.1f} m rim {m[near].mean():.3f} m in {m[body].mean():.3f}"
print(line); open("screens/log.txt", "a").write(line + "\n")
strip(sn, ts, ["u", "v", "w", "m (CH)", "cargo", "glob"], f"screens/{tag}.png", tag)
