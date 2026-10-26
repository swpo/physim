"""Beyond-diffusion control for W: plain cargo diffusion (kappa=0) at D, D/4, D/10 vs the layer's exclusion (kappa=10, D)."""
import json, numpy as np, os
rows = [("kappa=10, Dc=0.05 (world)", {0: "runs/srho.json", 2: "runs/r3k10_s2.json"}),
        ("kappa=0,  Dc=0.05", {0: "runs/c_ablate.json", 2: "runs/k0_s2.json"}),
        ("kappa=0,  Dc=0.0125 (D/4)", {0: "runs/bd_D4_s0.json", 2: "runs/bd_D4_s2.json"}),
        ("kappa=0,  Dc=0.005 (D/10)", {0: "runs/bd_D10_s0.json", 2: "runs/bd_D10_s2.json"})]
print("arm                         seed  ratio_med  rear_med  rear_min  held_med   (t=1-8)")
for name, fs in rows:
    for seed, f in fs.items():
        if not os.path.exists(f): continue
        r = [x for x in json.load(open(f)) if 1 <= x["t"] <= 8]
        g = lambda k: np.array([x[k] for x in r])
        print(f"{name:28s} {seed}   {np.median(g('ratio')):7.2f}  {np.median(g('ratio_back')):7.2f}  {g('ratio_back').min():7.2f}  {np.median(g('held')):7.2f}")
