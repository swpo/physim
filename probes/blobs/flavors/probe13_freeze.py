"""probe13_freeze.py — freeze classifier constants from clean lone-blob portraits.

Runs lone A and lone B (clean, T=500), computes patch features via metrics.patch_features,
freezes W_HALFWIDTH_STAR and ACT_HALFWIDTH_STAR as geometric-mean midpoints,
writes classifier_calib.json and patches metrics.py constants IN PLACE (pre-lock step).
"""
import sys, os, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/flavors")
from flavors_core import default_params, run
import metrics

UB = -0.86756
def pair_params():
    p = default_params()
    p["k1_1"], p["k4_1"], p["Du_1"] = -1.0, 1.4, 0.65
    p["k1_2"], p["k4_2"], p["Du_2"] = -1.0 + 0.75*UB, 2.15, 0.65
    return p

feats = {}
for sp, tag in ((1, "A"), (2, "B")):
    p = pair_params()
    r = run(p, arch="vvw", T=500.0, spots=((sp, 48, 48, 2.0, 3.0),))
    F, bg = r["F"], r["bg"]
    act = (F[0]-bg["u1"]) + (F[1]-bg["u2"])
    cy, cx = np.unravel_index(np.argmax(act), act.shape)
    f = metrics.patch_features(F, bg, cy, cx)
    feats[tag] = f
    print(tag, {k: round(v,4) for k,v in f.items()}, flush=True)

wstar = float(np.sqrt(feats["A"]["w_halfwidth"] * feats["B"]["w_halfwidth"]))
astar = float(np.sqrt(feats["A"]["act_halfwidth"] * feats["B"]["act_halfwidth"]))
calib = dict(A=feats["A"], B=feats["B"], W_HALFWIDTH_STAR=wstar,
             ACT_HALFWIDTH_STAR=astar,
             note="geometric-mean midpoints; clean lone blobs T=500")
json.dump(calib, open("/Users/spoho/Documents/prime/test/physim/probes/blobs/flavors/classifier_calib.json","w"), indent=1)
print("W*=", wstar, "ACT*=", astar)

# patch metrics.py constants
mp = "/Users/spoho/Documents/prime/test/physim/probes/blobs/flavors/metrics.py"
src = open(mp).read()
src = src.replace("W_HALFWIDTH_STAR = None   # filled by freeze(); stored in classifier_calib.json",
                  f"W_HALFWIDTH_STAR = {wstar:.4f}   # frozen by probe13_freeze.py")
src = src.replace("ACT_HALFWIDTH_STAR = None",
                  f"ACT_HALFWIDTH_STAR = {astar:.4f}   # frozen by probe13_freeze.py")
open(mp, "w").write(src)
print("metrics.py constants frozen")
