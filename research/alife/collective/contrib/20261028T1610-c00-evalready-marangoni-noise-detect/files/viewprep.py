import json, sys, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, ".")
from apparatus import lattice, OUT
z = np.load(OUT / "prep_s0.npz"); info = json.loads((OUT / "prep_s0.json").read_text()); S = info["sites"]
fig, ax = plt.subplots(1, 4, figsize=(16, 4.4))
for a, (f, im) in zip(ax, [("phi", z["phi"]), ("|Q|", np.hypot(z["q1"], z["q2"])), ("s", z["s"]), ("c", z["c"])]):
    h = a.imshow(im, cmap="viridis", origin="upper", vmax=(np.percentile(im, 99.5) if f == "c" else None)); a.set_title(f"{f} at t_prep={info['t_prep']}"); plt.colorbar(h, ax=a, fraction=0.046)
    for k, mk in (("centre", "r+"), ("rim", "rx"), ("bath", "w*"), ("other", "c+")):
        a.plot(S[k][1], S[k][0], mk, ms=10, mew=2)
    for c, off, col in ((S["centre"], lattice("square", 3.0), "r"), (S["other"], lattice("hex", 6.0), "c")):
        p = (np.array(c) + off) % 128; a.plot(p[:, 1], p[:, 0], ".", color=col, ms=3)
plt.tight_layout(); plt.savefig("prep_s0.png", dpi=80)
