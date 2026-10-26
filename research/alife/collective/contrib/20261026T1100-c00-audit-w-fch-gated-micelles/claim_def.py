"""The claim's own cargo definition (cargo_contrast.py: body = (u+1.6) > 0.8, per-body mean c over
the whole body / mean c beyond a 3-px dilation of all bodies), applied to EVERY frame >= 5 instead
of the 11 frames the claim script prints. Usage: claim_def.py <pack_dir>"""
import sys, json
import numpy as np
from scipy import ndimage

d = sys.argv[1]
F = np.load(d + "/frames.npz")
R, rf = F["render"].astype(np.float32), list(F["render_f"])
per_all, late = [], []
for i, f in enumerate(rf):
    if f < 5:
        continue
    u, c = R[i, 0], R[i, 1]
    body = u > 0.8
    lab, n = ndimage.label(body)
    far = ~ndimage.binary_dilation(body, iterations=3)
    if n == 0 or not far.any():
        continue
    cout = c[far].mean()
    per = ndimage.mean(c, lab, range(1, n + 1)) / max(cout, 1e-12)
    per_all += list(per)
    if f >= 30:
        late += list(per)
per_all, late = np.array(per_all), np.array(late)
out = {"claim_def_body_frames": int(len(per_all)), "claim_def_median": float(np.median(per_all)),
       "claim_def_share_ge2": float(np.mean(per_all >= 2)), "claim_def_late_median": float(np.median(late)),
       "claim_def_late_share_ge2": float(np.mean(late >= 2))}
json.dump(out, open(d + "/claim_def.json", "w"), indent=1)
print(d, out)
