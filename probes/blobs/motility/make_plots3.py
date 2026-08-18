
import sys, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
OUT = "/Users/spoho/Documents/prime/test/physim/probes/blobs/motility"
S = OUT + "/strips"
d = np.load(OUT + "/cert8_wall_track.npz")
t, c = d["t"], d["com"]
fig, axs = plt.subplots(1, 2, figsize=(10.5, 4.0))
axs[0].plot(t, c[:,0], "C3", lw=1.5)
axs[0].axhline(96, color="k", lw=2); axs[0].text(20, 96.5, "no-flux wall x=96")
axs[0].set_xlabel("t [tu]"); axs[0].set_ylabel("x position [phys]")
axs[0].set_title("wall reflex (tau=5.4, euler, no-flux): reflection at x~90")
u = d["snap400.0"]
axs[1].imshow(u.T, origin="lower", cmap="magma", extent=[0,96,0,96])
axs[1].plot(c[:,0], c[:,1], "c.", ms=1.5)
axs[1].set_title("u at t=400 (after bounce), cyan: COM track")
fig.tight_layout(); fig.savefig(S + "/wall_reflection.png", dpi=130)
print("saved wall_reflection.png")
