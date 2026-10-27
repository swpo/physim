"""usage: python count.py run:time_per_frame ...  Count prey (c_a>0.5) and predator (c_b>0.5) bodies (>=4 px) and mean prey/predator material per recorded frame."""
import sys, json, numpy as np
from scipy import ndimage
def n(x, th=0.5, amin=4):
    l, k = ndimage.label(x > th)
    if k == 0: return 0
    return int((ndimage.sum(np.ones_like(x), l, range(1, k + 1)) >= amin).sum())
out = {}
for arg in sys.argv[1:]:
    run, tpf = arg.split(":")
    d = np.load(f"rerun/{run}/frames.npz"); R, t = d["render"], d["render_f"] * float(tpf)
    rows = [(float(tt), n(f[0]), n(f[1]), float(f[0].mean()), float(f[1].mean())) for tt, f in zip(t, R)]
    out[run] = rows
    sel = [r for r in rows if r[0] in (2000, 5000, 6000, 6100, 6200, 6300, 6400, 6500, 7000)]
    print(run, " ".join(f"t{r[0]:.0f}:prey{r[1]}/pred{r[2]}/ma{r[3]:.3f}/mb{r[4]:.3f}" for r in sel))
json.dump(out, open("counts.json", "w"))
