import json, glob, os, importlib.util, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
rows = []
for f in sorted(glob.glob("st/*/segments.json")):
    d = json.load(open(f))["summary"]; n = f.split("/")[1]
    if "ring_all" not in d: continue
    rows.append((n, d["ring_all"], d["ring_swimmers"], d["swimmers_3BL"], d["dividers"], d["swim_divide"], d.get("max_chain", 0)))
print("| config | ring all cells | ring swimmers>=3BL | swimmers>=3BL | dividers | swim-divide | chain |")
for r in rows: print("| %s | %.2f | %.2f | %d | %d | %d | %d |" % r)
os.environ["WORLD_P"] = "{}"
spec = importlib.util.spec_from_file_location("w", "world.py"); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
base = dict(w.P)
cfgs = [("static, chi=2 (mu=0)", {"mu": 0, "chi": 2}), ("slip mu=1.8, chi=2", {"mu": 1.8, "sig": 12, "chi": 2}),
        ("slip mu=2.2, chi=1", {"mu": 2.2, "sig": 12, "chi": 1}), ("slip mu=2.5, chi=2", {"mu": 2.5, "sig": 12, "chi": 2})]
fig, ax = plt.subplots(2, 5, figsize=(22, 9))
for k, (name, p) in enumerate(cfgs):
    w.P.clear(); w.P.update(base); w.P.update(p)
    s = w.init(0, w.META["size"])
    for t in range(4000): s = w.step(s)
    ax[0, k].imshow(s["phi"], cmap="gray", vmin=0, vmax=1)
    ax[0, k].set_title(f"{name}\nphi (inside phase), t=4000, seed 0", fontsize=9)
    ax[1, k].imshow(s["L"], cmap="magma", vmin=0, vmax=0.6)
    ax[1, k].set_title("L (links; ring = bright wall layer)", fontsize=9)
for a in ax[:, :4].flat: a.axis("off")
a = ax[0, 4]; ax[1, 4].axis("off")
for r in rows:
    a.scatter(r[2] if r[3] else np.nan, r[5], s=20 + 3 * r[3], c="C1" if r[5] else "C0")
    if r[3]: a.annotate(r[0], (r[2], r[5]), fontsize=6)
a.axvline(1.5, ls="--", c="k"); a.set_xlabel("median wall/core L of segments swimming >= 3 BL"); a.set_ylabel("swim-divide events (seed 0, T=8000)")
a.set_title("ring vs swim-divide (marker size ~ number of 3-BL swimmers)", fontsize=9)
plt.tight_layout(); plt.savefig("tradeoff.png", dpi=70)
