"""c47: where along the flow do bodies split? From labkit frames.npz (render channel 0 = e): a component (e>0.5,
>= 10 px) at frame f-1 overlapping >= 2 components (>= 10 px) at frame f is a split; its parent's x centroid is
recorded (the flow runs along +x; the outlet/inlet strip is x < out_w). Also the fraction of frames with a body
whose x centroid lies in [out_w, out_w+20). usage: python splitx.py frames.npz [out_w=6]"""
import sys, numpy as np
from scipy import ndimage
R = np.load(sys.argv[1])["render"]; ow = float(sys.argv[2]) if len(sys.argv) > 2 else 6.0
def comps(e):
    l, n = ndimage.label(e > 0.5); sz = ndimage.sum(np.ones_like(e), l, range(1, n + 1))
    keep = [i + 1 for i, s in enumerate(sz) if s >= 10]
    return l, keep
xs = []; inlet_frames = 0
for f in range(1, len(R)):
    l0, k0 = comps(R[f - 1][0]); l1, k1 = comps(R[f][0])
    for i in k0:
        m = l0 == i; ch = set(np.unique(l1[m])) & set(k1)
        if len(ch) >= 2: xs.append(float(np.nonzero(m)[1].mean()))
    cx = [np.nonzero(l1 == j)[1].mean() for j in k1]
    inlet_frames += any(ow <= c < ow + 20 for c in cx)
xs = np.array(xs); W = R.shape[-1]
print(f"splits {len(xs)}; parent x in [{ow:.0f},{ow+20:.0f}): {int(((xs>=ow)&(xs<ow+20)).sum())}; x>=40: {int((xs>=40).sum())}; "
      f"frames with a body in the inlet zone: {inlet_frames}/{len(R)-1}; x hist (16 px bins): {np.histogram(xs, bins=np.arange(0, W+1, 16))[0].tolist()}")
