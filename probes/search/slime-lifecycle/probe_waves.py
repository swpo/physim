
import numpy as np, sys
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/slime-lifecycle")
import json
from slime import run
from hier_metrics import save_strip

p = json.load(open("best_c30.json"))
o = run(params=p, T=1400, seed=0, rec=10, snap_every=10)
mov = o["movie"]
# famine starts ~t=60; waves during 200-800. save S frames 400..480 every 10
frames = [(t, S) for (t, V, S) in [(m[0], m[1], m[2]) for m in mov] if 300 <= t <= 400]
save_strip([S for _, S in frames], "strips/waves_S_zoom.png",
           titles=["S t=%d" % t for t, _ in frames], cmap="inferno")
framesV = [(m[0], m[1]) for m in mov if 300 <= m[0] <= 400]
save_strip([V for _, V in framesV], "strips/waves_V_zoom.png",
           titles=["V t=%d" % t for t, _ in framesV], cmap="magma")
# wave speed: cross-correlate S(t) at two points 8 cells apart
import numpy as np
print("saved wave strips")
