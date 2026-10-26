"""(c45) Are consumer condensates separate individuals or bands on prey droplets? For every 10th rendered frame:
consumer components (q > qthr, >= 4 px) and the share that touch a prey droplet (c_a > 0.5) within 2 px (periodic),
and the share of the consumer's own area that overlaps prey (c_a > 0.5). usage: contact.py frames.npz [qthr=0.5]"""
import sys, numpy as np
from scipy import ndimage
z = np.load(sys.argv[1]); R = z["render"]; qthr = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
tot = touch = 0; ov = []
print("frame n_consumer touching_prey mean_overlap_with_prey")
for i in range(5, len(R), 10):
    ca, q = R[i, 0], R[i, 1]
    prey = ca > 0.5
    preyd = ndimage.binary_dilation(np.pad(prey, 3, mode="wrap"), iterations=2)[3:-3, 3:-3]
    lab, n = ndimage.label(q > qthr)
    k = t = 0; o = []
    for j in range(1, n + 1):
        m = lab == j
        if m.sum() < 4: continue
        k += 1; t += bool((m & preyd).any()); o.append((m & prey).sum() / m.sum())
    tot += k; touch += t; ov += o
    print(i, k, t, round(float(np.mean(o)) if o else float("nan"), 2))
print(f"all: {touch} of {tot} consumer bodies touch a prey droplet ({touch / max(tot, 1):.2f}); mean own-area overlap with prey {np.mean(ov):.2f}")
