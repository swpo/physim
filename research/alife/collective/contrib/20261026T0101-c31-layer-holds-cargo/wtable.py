"""W table: cargo inside/outside (signed distance) for the layer (kappa=10) and its ablation, per seed."""
import json, numpy as np, sys
pairs = [(0, "runs/ck10.json", "runs/c_ablate.json", 12), (1, "runs/koff1.json", "runs/koff1_k0.json", 6), (2, "runs/k10_s2.json", "runs/k0_s2.json", 12)]
print("seed arm  t_range  ratio_min ratio_med rear_min rear_med held_med  frac_frames_ratio>=2")
for seed, a, b, T in pairs:
    for arm, f in (("kappa10", a), ("ablate ", b)):
        try: r = json.load(open(f))
        except Exception: continue
        r = [x for x in r if 1.0 <= x["t"] <= T]
        R = np.array([x["ratio"] for x in r]); Rb = np.array([x["ratio_back"] for x in r]); H = np.array([x["held"] for x in r])
        print(f"{seed}    {arm} 1-{T:<5} {R.min():8.2f} {np.median(R):8.2f} {Rb.min():8.2f} {np.median(Rb):8.2f} {np.median(H):8.2f} {np.mean(R >= 2):8.2f}")
