"""L-link field at t=6000, same colour scale, for phase_membrane and its uniform-D twins (c01)."""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, ".")
from labkit.world import load_world  # noqa: E402

out = sys.argv[1]
arms = [("phase_membrane (gate, chi=2)", "threads/autopoiesis/worlds/phase_membrane/world.py", {}),
        ("phase_membrane chi=0 (gate kept)", "threads/autopoiesis/worlds/phase_membrane/world.py", {"chi": 0.0}),
        ("twin: uniform D x0.1", sys.argv[2], {"lam": 0.1}),
        ("twin: uniform D x0.001", sys.argv[2], {"lam": 0.001}),
        ("twin: D = 0 (frozen)", sys.argv[2], {"lam": 0.0})]
fig, ax = plt.subplots(2, 5, figsize=(17, 7.2))
for j, (name, w, ov) in enumerate(arms):
    W = load_world(w)
    W.P.update(ov)
    s = W.init(5, W.META["size"])
    for _ in range(6000):
        s = W.step(s)
    ax[0, j].imshow(s["L"], cmap="magma", vmin=0, vmax=0.6)
    ax[0, j].contour(s["phi"], [0.5], colors="c", linewidths=0.6)
    ax[0, j].set_title(name, fontsize=9)
    ax[1, j].imshow(s["L"][32:96, 32:96], cmap="magma", vmin=0, vmax=0.6)
    ax[1, j].contour(s["phi"][32:96, 32:96], [0.5], colors="c", linewidths=0.8)
    for a in ax[:, j]:
        a.set_xticks([]); a.set_yticks([])
fig.suptitle("L link at t=6000, seed 5 (magma 0-0.6; cyan: phi=1/2). Bottom: central 64x64 crop", fontsize=10)
fig.tight_layout()
fig.savefig(out, dpi=80)
