"""pilot1: engine sanity. (a) eps=0 reproduces M3 (A area 169, B area 25, pinned).
(b) base relax with tri eps: does the no-blob world stay quiescent? (c) small-eps
drift sign/speed both species, tri profile, blob seeded mid-branch (x=24)."""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sim

out = {}

# (a) eps=0 control: A blob and B blob separately, T=400
for spn, exp_area in (("A", 169.0), ("B", 25.0)):
    r = sim.run(eps=0.0, kind="flat", T=400.0, spots=((spn, 48.0, 48.0),), rec_tu=10.0)
    tr = r["tracks"][0]
    out[f"ctrl_{spn}"] = dict(status=r["status"], area_final=tr["area"][-1],
                              nc_final=tr["nc"][-1],
                              x0=tr["x"][0], x_final=tr["x"][-1],
                              y_final=tr["y"][-1], peak=round(tr["peak"][-1], 3),
                              expected_area=exp_area, tu_per_s=round(r["tu_per_s"], 1))
    print("ctrl", spn, out[f"ctrl_{spn}"], flush=True)

# (b) base quiescence under tri eps: relax, then run NO blob for 300 tu, check nothing nucleates
for eps in (0.002, 0.005, 0.01):
    r = sim.run(eps=eps, kind="tri", T=300.0, spots=(), rec_tu=25.0)
    out[f"quiesce_eps{eps}"] = dict(status=r["status"],
                                    n1=max(r["glob"]["n1"]), n2=max(r["glob"]["n2"]),
                                    a1=max(r["glob"]["a1"]), a2=max(r["glob"]["a2"]),
                                    b_range=[float(r["b"].min()), float(r["b"].max())])
    print("quiesce", eps, out[f"quiesce_eps{eps}"], flush=True)

# (c) drift pilot: eps=0.005, both species, seeded at x=24 (mid rising branch), T=1200
for spn in ("A", "B"):
    r = sim.run(eps=0.005, kind="tri", T=1200.0, spots=((spn, 24.0, 48.0),), rec_tu=10.0)
    tr = r["tracks"][0]
    xs = np.array(tr["x"]); ts = np.array(r["t"])
    out[f"drift_{spn}"] = dict(status=r["status"], x0=float(xs[0]), x_end=float(xs[-1]),
                               net=float(xs[-1] - xs[0]), area_end=tr["area"][-1],
                               nc_max=max(tr["nc"]), tu_per_s=round(r["tu_per_s"], 1),
                               x_series=[round(float(v), 3) for v in xs[::12]])
    print("drift", spn, out[f"drift_{spn}"], flush=True)

json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pilot1.json"), "w"), indent=1)
print("DONE")
