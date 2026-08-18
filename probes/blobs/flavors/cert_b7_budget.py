"""cert_b7_budget.py — B7: single-candidate wallclock at working L + dx/2 sanity of the pair."""
import sys, time
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/flavors")
from flavors_core import default_params, run

UB = -0.86756
def pp():
    p = default_params()
    p["k1_1"], p["k4_1"], p["Du_1"] = -1.0, 1.4, 0.65
    p["k1_2"], p["k4_2"], p["Du_2"] = -1.0 + 0.75*UB, 2.15, 0.65
    return p

t0 = time.time()
r = run(pp(), arch="vvw", T=800.0, spots=((1,48,30,2.0,3.0),(2,48,66,2.0,3.0)), noise=2.5e-3, seed=0)
w = time.time()-t0
print(f"standard candidate (800tu pair world, L=96): {w:.1f}s = {800/w:.1f} tu/s -> "
      f"5min budget = {300*800/w:.0f} tu", flush=True)
# dt/2 invariance for both species
for sp in (1,2):
    a = {}
    for dtf in (1.0, 0.5):
        r = run(pp(), arch="vvw", T=300.0, spots=((sp,48,48,2.0,3.0),), dt=0.01*dtf)
        s = r["series"]; a[dtf] = (s[f"a{sp}"][-1], s[f"m{sp}"][-1])
    print(f"species {'AB'[sp-1]}: dt=0.01 -> area,amp={a[1.0]}, dt=0.005 -> {a[0.5]}", flush=True)
