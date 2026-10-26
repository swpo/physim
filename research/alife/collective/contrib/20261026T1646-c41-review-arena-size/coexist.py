"""c42's coexistence rule on a labkit frames.npz: predators (channel 1 > 0.5, >= 10 px) present at every frame from
t=6000, prey (channel 0) present at >= 50% of those frames. usage: coexist.py frames.npz [t_per_frame=100]"""
import sys, numpy as np
from scipy import ndimage as ndi
f = np.load(sys.argv[1]); R = f["render"].astype(float); tf = f["render_f"] * (float(sys.argv[2]) if len(sys.argv) > 2 else 100.0)
def n(img):
    lab, k = ndi.label(img > 0.5, structure=np.ones((3, 3))); return int((ndi.sum(np.ones_like(img), lab, range(1, k + 1)) >= 10).sum()) if k else 0
late = [i for i in range(len(tf)) if tf[i] >= 6000]
pred = [n(R[i, 1]) for i in late]; prey = [n(R[i, 0]) for i in late]
last_pred = max([tf[i] for i in range(len(tf)) if n(R[i, 1]) > 0], default=-1)
print(sys.argv[1], "predators present at all late frames:", all(p > 0 for p in pred), "| prey present fraction %.2f" % np.mean([p > 0 for p in prey]),
      "| coexist:", all(p > 0 for p in pred) and np.mean([p > 0 for p in prey]) >= 0.5, "| last predator t", last_pred, "| end prey/pred", prey[-1], pred[-1])
