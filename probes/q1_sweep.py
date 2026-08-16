
import numpy as np, time
exec(open("/tmp/q1_probe3.py").read().split("t0=time.time()")[0])
import io, contextlib
for depth in (0.30, 0.20, 0.12):
    src = open("/tmp/q1_probe3.py").read().split("t0=time.time()")[0]
    src = src.replace("regen = 0.004 * (0.05 if storm else 1.0)",
                      "regen = 0.004 * (%s if storm else 1.0)" % depth)
    ns = {}
    exec(src, ns)
    print("---- storm regen mult = %s ----" % depth)
    ns["run"](storms=True, cap=0.15, T=60000, tag="depth %s" % depth)
