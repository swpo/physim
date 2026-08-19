"""pilot2: (a) settled eps=0 anchors T=1200; (b) dx=0.5 imexfft speed + eps=0 anchor;
(c) B at bigger eps dx=1 (depinning?); (d) B at dx=0.5 eps=0.005 (unpinned drift?)."""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sim

out = {}
# (a) settled anchors dx=1
for spn in ("A", "B"):
    r = sim.run(eps=0.0, kind="flat", T=1200.0, spots=((spn, 48.0, 48.0),), rec_tu=20.0)
    tr = r["tracks"][0]
    out[f"anchor_{spn}_dx1"] = dict(area=tr["area"][-1], nc=tr["nc"][-1],
                                    x=round(tr["x"][-1], 3), tu_per_s=round(r["tu_per_s"], 1))
    print("anchor dx1", spn, out[f"anchor_{spn}_dx1"], flush=True)

# (b) dx=0.5 imex anchor + speed
for spn in ("A", "B"):
    r = sim.run(eps=0.0, kind="flat", T=600.0, dx=0.5, stepper="imexfft",
                spots=((spn, 48.0, 48.0),), rec_tu=20.0)
    tr = r["tracks"][0]
    out[f"anchor_{spn}_dx05"] = dict(area=tr["area"][-1], nc=tr["nc"][-1],
                                     x=round(tr["x"][-1], 3), tu_per_s=round(r["tu_per_s"], 1))
    print("anchor dx05", spn, out[f"anchor_{spn}_dx05"], flush=True)

# (c) B depinning scan at dx=1
for eps in (0.01, 0.02):
    r = sim.run(eps=eps, kind="tri", T=1000.0, spots=(("B", 24.0, 48.0),), rec_tu=10.0)
    tr = r["tracks"][0]
    xs = np.array(tr["x"])
    out[f"B_dx1_eps{eps}"] = dict(status=r["status"], net=round(float(xs[-1] - xs[0]), 4),
                                  area_end=tr["area"][-1], nc_max=max(tr["nc"]))
    print("B dx1", eps, out[f"B_dx1_eps{eps}"], flush=True)

# (d) B at dx=0.5 imex, eps=0.005
r = sim.run(eps=0.005, kind="tri", T=800.0, dx=0.5, stepper="imexfft",
            spots=(("B", 24.0, 48.0),), rec_tu=10.0)
tr = r["tracks"][0]
xs = np.array(tr["x"])
out["B_dx05_eps0.005"] = dict(status=r["status"], net=round(float(xs[-1] - xs[0]), 4),
                              area_end=tr["area"][-1], nc_max=max(tr["nc"]),
                              x_series=[round(float(v), 3) for v in xs[::8]],
                              tu_per_s=round(r["tu_per_s"], 1))
print("B dx05", out["B_dx05_eps0.005"], flush=True)

json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pilot2.json"), "w"), indent=1)
print("DONE")
