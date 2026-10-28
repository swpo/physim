"""Which field's noise breaks the world? Native world (64^2 or given size), seed 0, noise on ONE field at a time
(additive / proportional / conserved), T time units; reports blow-up time, max |v|, final body count and mean |Q| in
bodies against the noise-free run. usage: fieldnoise.py SIZE T a [a ...]"""
import importlib.util, json, sys
import numpy as np
from pathlib import Path
from scipy import ndimage

D = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("mgn", D / "mg_noise.py")
NZ = importlib.util.module_from_spec(spec); spec.loader.exec_module(NZ)
W = NZ.B
N, T = int(sys.argv[1]), float(sys.argv[2])
amps = [float(x) for x in sys.argv[3:]]
cases = [("none", None, 0.0)]
for a in amps:
    cases += [(f"add:{f}", dict(nfields=[f], mult=[], cons=[]), a) for f in ["phi", "q1", "s", "c"]]
    cases += [("add:q1q2", dict(nfields=["q1", "q2"], mult=[], cons=[]), a),
              ("cons:phi", dict(nfields=[], mult=[], cons=["phi"]), a),
              ("mult:s", dict(nfields=[], mult=["s"], cons=[]), a),
              ("mult:c", dict(nfields=[], mult=["c"], cons=[]), a)]
for name, form, a in cases:
    s = W.init(0, (N, N)); rng = np.random.default_rng([4, 0])
    n = int(T / W.P["dt"]); blow = None; vmax = 0
    for k in range(n):
        if form:
            s = NZ.add_noise(s, a, rng, **form)
        s = W.step(s)
        if k % 20 == 0:
            if not np.isfinite(s["phi"]).all() or not np.isfinite(s["vx"]).all():
                blow = round(k * W.P["dt"], 2); break
            vmax = max(vmax, float(np.hypot(s["vx"], s["vy"]).max()))
    if blow is None:
        lab, nb = ndimage.label(s["phi"] > 0)
        ins = s["phi"] > 0
        r = dict(bodies=int(nb), occ=round(float(ins.mean()), 3), Q_in=round(float(np.hypot(s["q1"], s["q2"])[ins].mean()), 3),
                 s_max=round(float(s["s"].max()), 2), c_in=round(float(s["c"][ins].mean()), 2), c_out=round(float(s["c"][~ins].mean()), 3))
    else:
        r = {}
    print(json.dumps(dict(case=name, a=a, blowup_t=blow, vmax=round(vmax, 3), **r)), flush=True)
