"""Is the cargo a memory or re-equilibration? Run the claimed world (seed 13) to t=200, branch, delete the solute
inside one body (and, separately, inside every body), and follow that body's contrast vs an untouched twin.
Usage: refill.py seed"""
import sys, copy, importlib.util, numpy as np
from scipy import ndimage
spec = importlib.util.spec_from_file_location("w", "world.py"); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
seed = int(sys.argv[1]); P = w.P; thr = 0.8
s = w.init(seed, (128, 128)); spf = 200
for _ in range(50 * spf): s = w.step(s)  # t=200

def contrast(s, lab_mask):
    body = (s["u"] - P["u_bg"]) > thr
    far = ~ndimage.binary_dilation(body, iterations=3)
    return s["c"][lab_mask].mean() / s["c"][far].mean()

body = (s["u"] - P["u_bg"]) > thr
lab, n = ndimage.label(body)
sizes = ndimage.sum(body, lab, range(1, n + 1)); k = int(np.argmax(sizes)) + 1
one = lab == k
arms = {"twin": copy.deepcopy(s), "one_emptied": copy.deepcopy(s), "all_emptied": copy.deepcopy(s)}
arms["one_emptied"]["c"][ndimage.binary_dilation(one, iterations=1)] = 0
arms["all_emptied"]["c"][ndimage.binary_dilation(body, iterations=1)] = 0
print(f"seed {seed}: {n} bodies at t=200; target body {k}, {int(sizes[k-1])} px")
times = [0, 0.4, 1, 2, 4, 8, 16, 32, 64]
t = 0.0; rows = []
for tt in times:
    while t < tt - 1e-9:
        for a in arms: arms[a] = w.step(arms[a])
        t += P["dt"]
    # follow the target body by its overlap with the original mask
    out = []
    for a in arms:
        b = (arms[a]["u"] - P["u_bg"]) > thr; l2, _ = ndimage.label(b)
        ids = np.unique(l2[one & b]); ids = ids[ids > 0]
        m = np.isin(l2, ids)
        allb = ndimage.mean(arms[a]["c"], l2, range(1, l2.max() + 1)) / arms[a]["c"][~ndimage.binary_dilation(b, iterations=3)].mean()
        out.append(f"{a}: target {contrast(arms[a], m):6.1f}x, bodies>=2x {np.mean(allb >= 2):.2f}")
    print(f"t=200+{tt:5.1f}  " + " | ".join(out), flush=True)
