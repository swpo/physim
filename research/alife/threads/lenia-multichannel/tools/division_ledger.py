"""Per-division and conversion ledger for a whole-body branch run (territory tracking every 5 t).

python division_ledger.py world.py STATE.npz OUT.json EFF [STEPS]
Same start as branch_test.py OP=whole. Every 50 steps, territories (see branch_test.territories) are matched
to the previous sample by overlap (>= 20% of the child). For each territory p = allele-1 mass fraction,
kind = 1 if p >= 0.5.
  division : one parent overlaps >= 2 children. True if every child has the parent's kind and is pure
             (p >= 0.9 for kind 1, p <= 0.1 for kind 0).
  conversion: a 1-to-1 match whose kind changes (no mutation in these runs).
  mixed-born: a division child with 0.1 < p < 0.9.
Ledger kept separately for kind-1 and kind-0 parents.
"""
import json
import sys
from pathlib import Path

import numpy as np
from scipy import ndimage

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from branch_test import territories  # noqa: E402
from labkit.world import load_world  # noqa: E402

W = load_world(sys.argv[1]); st = np.load(sys.argv[2]); out = sys.argv[3]; W.EFF = float(sys.argv[4])
steps = int(sys.argv[5]) if len(sys.argv) > 5 else 5000
W.MU_CELL = 0.0
H, Wd = st["F"].shape
s = W.init(0, (H, Wd))
s["A"], s["F"], s["a"] = st["A"].copy(), st["F"].copy(), np.zeros_like(st["a"])
terr, n = territories(s["A"])
best, bestd = 1, -1
for i in range(1, n + 1):
    m = terr == i
    others = (terr > 0) & ~m
    d = ndimage.distance_transform_edt(~m)
    dm = float(d[others].min()) if others.any() else 1e9
    if dm > bestd:
        best, bestd = i, dm
s["a"] = np.where(ndimage.binary_dilation(terr == best, iterations=2), 1.0, 0.0)

L = {k: dict(div=0, true=0, mixed_born=0, conv_to_other=0, deaths=0) for k in (0, 1)}


def snap(s):
    terr, n = territories(s["A"])
    M = s["A"].sum(0)
    cells = []
    for i in range(1, n + 1):
        m = terr == i
        p = float((s["a"][m] * M[m]).sum() / max(M[m].sum(), 1e-9))
        cells.append((m, p))
    return cells


prev = snap(s)
for t in range(1, steps + 1):
    s = W.step(s)
    if t % 50:
        continue
    cur = snap(s)
    for pm, pp in prev:
        kind = int(pp >= 0.5)
        kids = [(cm, cp) for cm, cp in cur if (pm & cm).sum() >= 0.2 * cm.sum()]
        if len(kids) >= 2:
            L[kind]["div"] += 1
            ok = all((cp >= 0.9) if kind else (cp <= 0.1) for _, cp in kids)
            L[kind]["true"] += ok
            L[kind]["mixed_born"] += sum(0.1 < cp < 0.9 for _, cp in kids)
        elif len(kids) == 1:
            cm, cp = kids[0]
            owners = sum((qm & cm).sum() >= 0.2 * cm.sum() for qm, _ in prev)
            if owners == 1 and int(cp >= 0.5) != kind:
                L[kind]["conv_to_other"] += 1
        else:
            L[kind]["deaths"] += 1
    prev = cur
json.dump(dict(state=sys.argv[2], eff=W.EFF, ledger=L), open(out, "w"))
print(json.dumps(L))
