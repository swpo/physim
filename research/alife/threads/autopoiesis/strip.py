"""Fixed-crop strip from one or more packs (rows), same frames, labkit colours.
python strip.py OUT.png cy cx half f1,f2,... PACK [PACK ...]"""
import sys, numpy as np
sys.path.insert(0, ".")
from labkit import render as R
out, cy, cx, half, fl = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), [int(v) for v in sys.argv[5].split(",")]
rows, labels = [], []
for pack in sys.argv[6:]:
    z = np.load(pack + "/frames.npz"); rend = z["render"].astype(np.float32); rf = list(z["render_f"])
    sc = R.channel_scales(rend)
    for f in fl:
        k = int(np.argmin([abs(x - f) for x in rf]))
        img = R.composite(R.normalize(rend[k], sc))
        crop = R.crop_periodic(img, cy, cx, half)
        rows.append(np.asarray(R.Image.fromarray(crop).resize((128, 128), R.Image.NEAREST)))
        labels.append(f"{pack.rstrip('/').split('/')[-1][-14:]} f{rf[k]}")
R.contact_sheet(rows, labels, ncols=len(fl), title=f"fixed crop centre ({cy:.0f},{cx:.0f}) half {half}").save(out)
