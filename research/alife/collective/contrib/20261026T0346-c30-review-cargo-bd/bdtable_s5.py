"""c31's bdtable statistic (t=1-8 medians of in/out by signed distance, rear side, held fraction) on seed 5."""
import json, os, numpy as np
H = os.path.dirname(os.path.abspath(__file__))
rows = [("kappa=10, Dc=0.05 (world)", "runs/k10_s5.json"), ("kappa=0,  Dc=0.05", "runs/k0_s5.json"), ("kappa=0,  Dc=0.0125 (D/4)", "runs/k0D4_s5.json")]
print("arm                         seed  ratio_med  rear_med  rear_min  held_med   (t=1-8)")
for name, f in rows:
    p = os.path.join(H, f)
    if not os.path.exists(p): print(name, "missing"); continue
    r = [x for x in json.load(open(p)) if 1 <= x["t"] <= 8]
    g = lambda k: np.array([x[k] for x in r])
    print(f"{name:28s} 5   {np.median(g('ratio')):7.2f}  {np.median(g('ratio_back')):7.2f}  {g('ratio_back').min():7.2f}  {np.median(g('held')):7.2f}")
