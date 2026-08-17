
import sys, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
from hier_metrics import save_strip
d = np.load(sys.argv[1])
ts = d["ts"]
pre = sys.argv[2]
for f, cm, vmx in (("V","magma",None), ("S","inferno",None), ("R","viridis",1.0)):
    save_strip([d["%s_%d" % (f, t)] for t in ts], "%s_%s.png" % (pre, f),
               titles=["%s t=%d" % (f, t) for t in ts], cmap=cm, vmax=vmx)
print("saved", pre)
