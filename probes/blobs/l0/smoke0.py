import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
import numpy as np
import genome as G

g = G.ref_M0()
probs = G.validate(g)
print("validate:", probs)
N = int(round(96/0.5))
F = G.state_vacuum(g, N)
F = G.poke(F, g, 0, 48.0, 48.0, 2.0, 3.0, 0.5)
r = G.run_genome(g, F=F, T=200.0, rec_tu=10.0)
a = [x[0] if x else 0.0 for x in r["area0"]]
rec = dict(kind="smoke_parity", genome="ref_M0", T=200.0, status=r["status"],
           ncomp_end=int(r["ncomp0"][-1]), area_end=(a[-1] if a else None),
           area_tail=a[-5:], wall_s=round(r["wall_s"],2), tu_per_s=round(r["tu_per_s"],1))
print(rec)
n = G.append_result(rec)
print("results.json rows:", n)
