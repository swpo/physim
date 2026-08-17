
"""assay_rates.py — short-horizon L4 rate assays for G3.
A) selection rate: from uniform <c>=0.5 init, slope of <c>(t) over t in [5k,25k]
B) mutation erosion: from monoclonal c=1 init, slope of <c>(t) over [5k,25k]
Usage: assay_rates.py <tag> <json-params>"""
import sys, json, time
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/slime-lifecycle")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/slime-lifecycle/cheaters")
from slime_evo import run

tag = sys.argv[1]
pp = json.loads(sys.argv[2])
T = int(pp.pop("_T", 30000))
seed = int(pp.pop("_seed", 0))
t0 = time.time()
out = run(params=pp, T=T, seed=seed, rec=50)
w = time.time() - t0
ser = out["ser"]
t = ser["t"]; cm = ser["cmean"]; sd = ser["csd"]; agg = ser["aggm"]; hf = ser["hf"]
msk = (t >= 5000) & (t <= 25000)
A = np.vstack([t[msk], np.ones(msk.sum())]).T
(slope, icpt), *_ = np.linalg.lstsq(A, cm[msk], rcond=None)
pred = A @ np.array([slope, icpt])
r2 = 1 - ((cm[msk]-pred)**2).sum()/max(((cm[msk]-cm[msk].mean())**2).sum(), 1e-12)
onsets = int(((hf[:-1] < 0.5) & (hf[1:] >= 0.5)).sum())
res = dict(tag=tag, ok=out["ok"], why=out["why"], slope_per_kt=float(slope*1000),
           r2_lin=float(r2), c_start=float(cm[msk][0]), c_end=float(cm[-1]),
           sd_end=float(sd[-1]), agg_frac=float((agg > 0.5).mean()),
           onsets=onsets, wall=round(w, 1))
print("RESULT " + json.dumps(res), flush=True)
np.savez_compressed("assay_%s.npz" % tag, t=t, cmean=cm, csd=sd, aggm=agg, hf=hf)
