"""Enzyme snapshots from a divcheck snapshot file. usage: divfig.py SNAPS.npz OUT.png T1 T2 ..."""
import sys
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from plabel import plabel
z = np.load(sys.argv[1]); ts = sys.argv[3:]
fig, ax = plt.subplots(1, len(ts), figsize=(2.6 * len(ts), 2.8))
for a, t in zip(np.atleast_1d(ax), ts):
    e = z[f"t{t}"][0]; n = plabel(e > 0.5)[1]
    a.imshow(e, cmap="magma", vmin=0, vmax=1); a.set_title(f"t={t}  bodies={n}", fontsize=8); a.axis("off")
fig.suptitle(sys.argv[1].split("/")[-1] + ": enzyme e (periodic body count, e>0.5)", fontsize=8)
fig.tight_layout(); fig.savefig(sys.argv[2], dpi=80)
