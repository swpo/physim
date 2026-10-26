"""Spot and molecule census over time for SH settings. usage: scan.py '<json list of WORLD_P>' nsteps tag"""
import os, sys, json, importlib.util, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy import ndimage as ndi
runs = json.loads(sys.argv[1]); nsteps = int(sys.argv[2]); tag = sys.argv[3]
fig, ax = plt.subplots(len(runs), 5, figsize=(15, 3*len(runs)), squeeze=False)
def count(u, dx):
    sp, ns = ndi.label(ndi.gaussian_filter(u, 1.0) > 0.6)
    mol, nm = ndi.label(ndi.binary_dilation(sp > 0, iterations=max(1, int(round(2.2 / dx)))))
    return ns, nm
for i, wp in enumerate(runs):
    os.environ["WORLD_P"] = json.dumps(wp)
    spec = importlib.util.spec_from_file_location("w%d" % i, "world.py"); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
    s = w.init(wp.get("seed", 0), w.META["size"]); dx = w.P["L"] / w.P["N"]
    T = []; NS = []; NM = []; j = 0
    for k in range(nsteps):
        s = w.step(s)
        if k % 200 == 0:
            ns, nm = count(s["u"], dx); T.append(s["t"]); NS.append(ns); NM.append(nm)
        if k in [int(nsteps * f) - 1 for f in (0.1, 0.4, 0.7, 1.0)]:
            ax[i, j].imshow(s["u"], cmap="magma", vmin=-0.5, vmax=2); ax[i, j].set_title("t=%.0f" % s["t"], fontsize=8); ax[i, j].axis("off"); j += 1
    ax[i, 4].plot(T, NS, label="spots"); ax[i, 4].plot(T, NM, label="molecules"); ax[i, 4].legend(fontsize=7)
    ax[i, 4].set_title(json.dumps({k: v for k, v in wp.items() if k not in ("N", "L")})[:60], fontsize=7)
    ups = int(np.sum(np.diff(NS) > 0)); upm = int(np.sum(np.diff(NM) > 0))
    print(json.dumps(wp), "spots", NS[5], "->", NS[-1], "min", min(NS[5:]), "max", max(NS[5:]), "mol", NM[5], "->", NM[-1], "spot-up events", ups, "mol-up events", upm, flush=True)
plt.tight_layout(); plt.savefig("scan_%s.png" % tag, dpi=65)
