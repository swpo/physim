"""Quick-look helper: run a (x, t, L) stepping function and save a particle contact sheet."""
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from labkit import render as R  # noqa: E402


def sheet(snaps, L, path, title="", ncols=6, size=240, radius=1.0):
    ims, labs = [], []
    for tt, x, t in snaps:
        ims.append(R.particle_canvas(x, t, (0, 0, L, L), size, radius=radius))
        labs.append(f"t={tt:g}")
    R.contact_sheet(ims, labs, ncols=ncols, title=title).save(path)


def run(stepper, state, nsteps, nsnap, dt, L, path, title=""):
    snaps = []
    every = max(1, nsteps // (nsnap - 1))
    t0 = time.time()
    for s in range(nsteps + 1):
        if s % every == 0:
            snaps.append((s * dt, state["x"].copy(), state["t"].copy()))
        if s < nsteps:
            state = stepper(state)
    sheet(snaps, L, path, title)
    np.savez_compressed(str(path).replace("screens/", "scratch/").replace(".png", ".npz"),
                        x=np.stack([s[1] for s in snaps]), t=np.stack([s[2] for s in snaps]))
    print(f"{path}: {time.time() - t0:.1f}s")
    return state, snaps
