import sys, importlib.util, numpy as np, pickle
from scipy import ndimage
spec = importlib.util.spec_from_file_location("w", sys.argv[1]); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
seed = int(sys.argv[2]); T0 = float(sys.argv[3]); dt = w.P["dt"]
s = w.init(seed, w.META["size"])
for _ in range(int(round(T0 / dt))): s = w.step(s)
pickle.dump(s, open(f"/tmp/claude-0/c09/state_{seed}_{int(T0)}.pkl", "wb"))
u = s["u"] - w.P["u_bg"]; body = u > 0.8
lab, n = ndimage.label(body); far = ~ndimage.binary_dilation(body, iterations=3)
sz = ndimage.sum(body, lab, range(1, n + 1)); per = ndimage.mean(s["c"], lab, range(1, n + 1)) / s["c"][far].mean()
print("n", n, "cout", s["c"][far].mean(), "sizes", sz.astype(int)[:20], "contrast", np.round(per[:20], 1))
