"""cmp_m3: run flavors_core directly vs transport sim, identical protocol."""
import sys, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/flavors")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/transport")
import flavors_core as fc
import sim

p = dict(fc.default_params())
p.update(k1_1=-1.0, k4_1=1.40, k1_2=-1.65067, k4_2=2.15, Du_1=0.65, Du_2=0.65)

r = fc.run(p, arch="vvw", L=96, T=1200.0, spots=((1, 48, 48, 2.0, 3.0),), rec_every_tu=100.0)
print("flavors_core A: bg u1 =", r["bg"]["u1"])
print("  area series:", r["series"]["a1"])
print("  umax:", r["series"]["m1"][-1])

r2 = sim.run(eps=0.0, kind="flat", T=1200.0, spots=(("A", 48.0, 48.0),), rec_tu=100.0)
tr = r2["tracks"][0]
print("transport sim A: base u1 =", r2["base1d"][0].mean())
print("  area series:", tr["area"])
print("  peak+base:", tr["peak"][-1] + r2["base1d"][0].mean())

# B too
rB = fc.run(p, arch="vvw", L=96, T=1200.0, spots=((2, 48, 48, 2.0, 3.0),), rec_every_tu=100.0)
print("flavors_core B area:", rB["series"]["a2"], "umax", rB["series"]["m2"][-1])
r2B = sim.run(eps=0.0, kind="flat", T=1200.0, spots=(("B", 48.0, 48.0),), rec_tu=100.0)
print("transport sim B area:", r2B["tracks"][0]["area"])
