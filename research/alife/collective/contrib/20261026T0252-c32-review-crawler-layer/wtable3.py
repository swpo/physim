"""W table for world3 (SRC=rho): cargo in/out by signed distance with the layer (kappa=10) vs the
kappa=0 ablation. The ablation arm is numerically the same world: s and c do not feed back on
phi or rho, and with kappa=0 the cargo does not see s (runs from world2 with kappa=0)."""
import json, numpy as np
pairs = [(0, "runs/srho.json", "runs/c_ablate.json", 8), (1, "runs/r3k10_s1.json", "runs/koff1_k0.json", 6),
         (1, "runs/r3k10_s1.json", None, 12), (2, "runs/r3k10_s2.json", "runs/k0_s2.json", 12)]
print("seed arm      t_range  ratio_min ratio_med rear_min rear_med held_med  frac_frames_ratio>=2")
for seed, a, b, T in pairs:
    for arm, f in (("kappa10", a), ("kappa0 ", b)):
        if f is None: continue
        r = [x for x in json.load(open(f)) if 1.0 <= x["t"] <= T]
        R = np.array([x["ratio"] for x in r]); Rb = np.array([x["ratio_back"] for x in r]); H = np.array([x["held"] for x in r])
        print(f"{seed}    {arm}  1-{T:<5} {R.min():8.2f} {np.median(R):8.2f} {Rb.min():8.2f} {np.median(Rb):8.2f} {np.median(H):8.2f} {np.mean(R >= 2):8.2f}")
