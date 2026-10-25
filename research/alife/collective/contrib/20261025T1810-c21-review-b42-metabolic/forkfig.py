"""(c21) Fed vs starved twin of pcell-mwall-b42 on one seed from two labkit frames.npz (identical until the cut):
RGB = M wall material (red), wall phi-membrane (green), catalyst particles K (blue); also counts cells
(components of the membrane-channel-filled body: K channel > 0.1, >= 12 px) per frame.
usage: forkfig.py fed/frames.npz starved/frames.npz out.png"""
import sys, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
A, B = np.load(sys.argv[1]), np.load(sys.argv[2])
want = [118, 120, 121, 122, 123, 124, 128, 140, 200]  # frames x 500 = time
def rgb(R, f):
    x = R[f]; c = lambda k: np.clip(x[k] / max(float(np.percentile(R[:, k], 99.5)), 1e-9), 0, 1)
    return np.dstack([c(5), c(3), c(1)])
fig, ax = plt.subplots(2, len(want), figsize=(2 * len(want), 4.6))
for r, (F, name) in enumerate(((A, "fed"), (B, "starved"))):
    rf = list(F["render_f"]); R = F["render"]
    for c, w in enumerate(want):
        f = int(np.argmin([abs(v - w) for v in rf]))
        ax[r, c].imshow(rgb(R, f)); ax[r, c].axis("off")
        n = sum(1 for k in range(1, ndimage.label(R[f, 1] > 0.1)[1] + 1) if (ndimage.label(R[f, 1] > 0.1)[0] == k).sum() >= 12)
        ax[r, c].set_title("%s t=%d, %d bodies" % (name, rf[f] * 500, n), fontsize=7)
fig.suptitle("seed 8: substrate feed cut at t=60000 (bottom) vs fed twin (top); red = M wall material, green = wall, blue = catalyst", fontsize=8)
fig.tight_layout(); fig.savefig(sys.argv[3], dpi=80)
