"""Run an allele world and audit heredity: allele fraction, division inheritance, conversions vs mutations.

python audit_alleles.py world.py OUT_PREFIX STEPS SIZE SEED [KEY=VAL ...]
Samples every 50 steps. Cells = A0 > 0.3 components (area >= 20). Matching by overlap between samples.
  division: a previous cell overlaps >= 2 current cells (each overlap >= 20% of the child): does every child
            carry the parent's majority allele?
  conversion: a 1-to-1 matched cell whose majority allele changed with no mutation event at that cell
            in the interval.
Writes OUT_PREFIX.json (series + audit) and OUT_PREFIX.png (strip: allele 1 red, allele 0 cyan, food green).
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from labkit.world import load_world  # noqa: E402

W = load_world(sys.argv[1]); pre = sys.argv[2]; steps = int(sys.argv[3]); size = int(sys.argv[4]); seed = int(sys.argv[5])
for kv in sys.argv[6:]:
    k, v = kv.split("=", 1); setattr(W, k, eval(v, dict(vars(W)) | {"np": np}))
s = W.init(seed, (size, size))
EVERY = 50


def cells(s):
    M = s["A"].sum(0)
    lab, n = ndimage.label(s["A"][0] > 0.3)
    out = []
    for i in range(1, n + 1):
        m = lab == i
        if m.sum() < 20:
            continue
        mm = ndimage.binary_dilation(m, iterations=3)
        al = float((s["a"][mm] * M[mm]).sum() / max(M[mm].sum(), 1e-9))
        out.append(dict(mask=m, allele=int(al > 0.5), purity=max(al, 1 - al),
                        cy=float(ndimage.center_of_mass(m)[0]), cx=float(ndimage.center_of_mass(m)[1])))
    return out


prev, series, tiles = None, [], []
aud = dict(divisions=0, true_divisions=0, divisions1=0, true_divisions1=0, conversions=0, mutations=0, impure_cells=0, cell_samples=0)
nmut_seen = 0
for t in range(steps + 1):
    if t % EVERY == 0:
        cur = cells(s)
        M = s["A"].sum(0)
        frac = float((M * s["a"]).sum() / max(M.sum(), 1e-9))
        series.append(dict(t=t, n=len(cur), n1=sum(c["allele"] for c in cur), frac1=frac, F=float(s["F"].mean())))
        aud["cell_samples"] += len(cur)
        aud["impure_cells"] += sum(c["purity"] < 0.9 for c in cur)
        new_muts = s["mut_log"][nmut_seen:]
        nmut_seen = len(s["mut_log"])
        if prev is not None:
            for p in prev:
                kids = [c for c in cur if (p["mask"] & c["mask"]).sum() >= 0.2 * c["mask"].sum()]
                if len(kids) >= 2:
                    aud["divisions"] += 1
                    aud["true_divisions"] += all(k["allele"] == p["allele"] for k in kids)
                    if p["allele"] == 1:
                        aud["divisions1"] += 1
                        aud["true_divisions1"] += all(k["allele"] == 1 for k in kids)
                elif len(kids) == 1:
                    k = kids[0]
                    owners = [q for q in prev if (q["mask"] & k["mask"]).sum() >= 0.2 * k["mask"].sum()]
                    if len(owners) == 1 and k["allele"] != p["allele"]:
                        mutated = any(abs(((my - k["cy"] + size / 2) % size) - size / 2) < 25 and
                                      abs(((mx - k["cx"] + size / 2) % size) - size / 2) < 25 for _, my, mx, _ in new_muts)
                        if not mutated:
                            aud["conversions"] += 1
        prev = cur
        if t % (steps // 12) == 0:
            Mc = np.clip(M, 0, 1); a = s["a"]
            rgb = np.stack([Mc * a + 0.1 * Mc, 0.35 * np.clip(s["F"], 0, 1) * (1 - Mc) + 0.6 * Mc * (1 - a), Mc * (1 - a)], -1)
            tiles.append(np.pad((255 * np.clip(rgb, 0, 1)).astype(np.uint8), ((2, 2), (2, 2), (0, 0)), constant_values=60))
    if t < steps:
        s = W.step(s)
aud["mutations"] = len(s["mut_log"])
aud["mut_log"] = s["mut_log"]
Image.fromarray(np.concatenate(tiles, 1)).save(pre + ".png")
json.dump(dict(series=series, audit=aud), open(pre + ".json", "w"))
print(json.dumps({k: v for k, v in aud.items() if k != "mut_log"}), "final frac1 %.2f n1 %d/%d" % (series[-1]["frac1"], series[-1]["n1"], series[-1]["n"]))
