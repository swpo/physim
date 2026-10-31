"""Markdown tables from out/scores.json and the saved arms (body counts, cpu)."""
import json
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent / "out"
S = json.loads((OUT / "scores.json").read_text())
ORDER = ["native", "dthalf", "mar0", "passive", "kappa0", "chis0", "ignore_actions", "wrong_probe_geometry",
         "initial_persistence"]
for prog, pw in S["results"].items():
    print(f"\n### {prog}: ratio to the independent native predictor (5-95% over 6-of-8 subsets)\n")
    cols = [(w, g) for w in ("10tu", "25tu", "50tu") for g in ("device0", "device1", "global", "mean")]
    print("| predictor | " + " | ".join(f"{w} {g}" for w, g in cols) + " |")
    print("|---" * (len(cols) + 1) + "|")
    for a in ORDER:
        if a not in pw["10tu"]["device0"]:
            continue
        cells = []
        for w, g in cols:
            r = pw[w][g][a]
            cells.append(f"{r['es']:.3f}" if a == "native" else f"{r['ratio']:.2f} [{r['sub90'][0]:.2f}-{r['sub90'][1]:.2f}]")
        print(f"| {a} | " + " | ".join(cells) + " |")
print("\n### bodies (phi>0 components >= 6 px) at t=0 and t=50 tu, mean over members; cpu per arm\n")
print("| file | bodies t0 | bodies t50 (mean, min-max) | cpu s |")
print("|---|---|---|---|")
for f in sorted(OUT.glob("*_*_*.npz")):
    if f.stem.startswith("envelope"):
        continue
    z = np.load(f)
    b = z["bodies"]
    print(f"| {f.stem} | {b[:, 0].mean():.1f} | {b[:, -1].mean():.1f} ({b[:, -1].min()}-{b[:, -1].max()}) | {float(z['cpu']):.0f} |")
