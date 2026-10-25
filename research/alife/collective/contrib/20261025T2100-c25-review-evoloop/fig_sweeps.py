"""Kind fractions (hole side) and loop number over time for the three tracker runs, with the founding time of the
largest side-4 and side-3 clades (origins.py) marked."""
import json, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
runs = [("trk400/trk400_s4.json", "fresh seed 4, 400k steps", {4: 220240, 3: 235400}), ("trk/trk_s6.json", "fresh seed 6, 200k steps", {}),
        ("trk_c16s2/trk_s2.json", "c16's seed 2 re-run, 150k steps", {4: 76840, 3: 114940})]
cols = {2: "#1f4e9c", 3: "#9bbbe3", 4: "#f4a259", 11: "#bbbbbb", 12: "#b5b82a"}
fig, ax = plt.subplots(3, 1, figsize=(10, 9))
for a, (f, name, mk) in zip(ax, runs):
    d = json.load(open(f)); t = np.array([c["t"] for c in d["census"]]); n = np.array([c["n"] for c in d["census"]])
    fr = {k: np.array([dict(zip(c["areas"], c["counts"])).get(k, 0) for c in d["census"]]) / np.maximum(n, 1) for k in cols}
    other = 1 - sum(fr.values()); a.stackplot(t, *[fr[k] for k in cols], other, colors=list(cols.values()) + ["#e6c3d8"], labels=[f"side {k}" for k in cols] + ["other"])
    a2 = a.twinx(); a2.plot(t, n, "k", lw=1); a2.set_ylabel("loops")
    for k, t0 in mk.items(): a.axvline(t0, color="r", ls="--"); a.text(t0, 1.02, f"largest side-{k} clade founded", color="r", fontsize=7)
    a.set_title(name, fontsize=9); a.set_ylim(0, 1); a.set_ylabel("kind fraction")
ax[0].legend(fontsize=7, ncol=6, loc="lower left"); ax[-1].set_xlabel("time step"); plt.tight_layout(); plt.savefig("sweeps.png", dpi=70)
