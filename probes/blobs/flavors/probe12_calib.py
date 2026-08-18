
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath("__file__")) if "__file__" not in dir() else os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/flavors")
from flavors_core import default_params, run
from scipy import ndimage

UB = -0.86756
def pair_params():
    p = default_params()
    p["k1_1"], p["k4_1"], p["Du_1"] = -1.0, 1.4, 0.65
    p["k1_2"], p["k4_2"], p["Du_2"] = -1.0 + 0.75*UB, 2.15, 0.65
    return p

out = {}
for sp, tag in ((1, "A"), (2, "B")):
    for noise, ntag in ((0.0, "clean"), (2e-3, "noisy")):
        p = pair_params()
        r = run(p, arch="vvw", T=500.0, spots=((sp, 48, 48, 2.0, 3.0),), noise=noise, seed=7)
        F, bg, thr = r["F"], r["bg"], r["thr"]
        u1b, u2b, wb = bg["u1"], bg["u2"], bg["w"]
        # peak of total activity
        act = (F[0]-u1b) + (F[1]-u2b)
        cy, cx = np.unravel_index(np.argmax(act), act.shape)
        # patch features
        P = np.s_[cy-2:cy+3, cx-2:cx+3]
        du1 = float((F[0][P]-u1b).mean()); du2 = float((F[1][P]-u2b).mean())
        dwc = float((F[4][P]-wb).mean())
        # ring r=5 mean of w
        yy, xx = np.meshgrid(np.arange(96), np.arange(96), indexing="ij")
        rr = np.hypot(((yy-cy+48)%96)-48, ((xx-cx+48)%96)-48)
        ring = (rr > 4.5) & (rr < 6.5)
        wring = float(F[4][ring].mean() - wb)
        sharp = dwc - wring
        # union area in 21x21 window
        m = (F[0] > thr[0]) | (F[1] > thr[1])
        win = (rr <= 10.5)
        area = int((m & win).sum())
        # activity amplitude and sharpness
        actc = float(act[P].mean())
        actring = float(act[ring].mean())
        out[f"{tag}_{ntag}"] = dict(du1=round(du1,4), du2=round(du2,4),
            dw_center=round(dwc,4), w_ring=round(wring,4), w_sharp=round(sharp,4),
            act_center=round(actc,4), act_sharp=round(actc-actring,4),
            area21=area, peak=(int(cy),int(cx)))
        print(tag, ntag, out[f"{tag}_{ntag}"], flush=True)
json.dump(out, open("/Users/spoho/Documents/prime/test/physim/probes/blobs/flavors/calib_portraits.json","w"), indent=1)
