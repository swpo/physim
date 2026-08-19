"""anchor2: node-convention anchors at dx=0.5 (imexfft AND euler) + quick drift sanity
both species at eps=0.005 + falling-branch mirror check."""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sim

out = {}
# dx=0.5 anchors: imexfft and euler (to separate stepper vs grid effects on A size)
for spn in ("A", "B"):
    for st in ("imexfft", "euler"):
        r = sim.run(eps=0.0, kind="flat", T=600.0, dx=0.5, stepper=st,
                    spots=((spn, 48.0, 48.0),), rec_tu=50.0)
        tr = r["tracks"][0]
        key = f"anchor_{spn}_dx05_{st}"
        out[key] = dict(area_series=tr["area"], nc=tr["nc"][-1], peak=round(tr["peak"][-1], 4),
                        x=round(tr["x"][-1], 3), dt=r["dt"], tu_per_s=round(r["tu_per_s"], 2))
        print(key, out[key], flush=True)

# drift sanity, node convention, dx=0.5 imex, eps=0.005: A and B rising branch (x=24)
for spn in ("A", "B"):
    r = sim.run(eps=0.005, kind="tri", T=900.0, dx=0.5, stepper="imexfft",
                spots=((spn, 24.0, 48.0),), rec_tu=10.0, stop_leave=(0, 10.0, 38.0))
    tr = r["tracks"][0]
    xs = np.array(tr["x"])
    key = f"drift_{spn}_eps0.005"
    out[key] = dict(status=r["status"], x=[round(float(v),3) for v in xs[::9]],
                    area_end=tr["area"][-1], area_max=max(tr["area"]), nc_max=max(tr["nc"]),
                    T_end=r["T_end"], tu_per_s=round(r["tu_per_s"], 2))
    print(key, out[key], flush=True)

# falling-branch mirror: B seeded at x=72 must drift the OTHER way (local slope -eps)
r = sim.run(eps=0.005, kind="tri", T=900.0, dx=0.5, stepper="imexfft",
            spots=(("B", 72.0, 48.0),), rec_tu=10.0, stop_leave=(0, 58.0, 86.0))
tr = r["tracks"][0]
xs = np.array(tr["x"])
out["mirror_B_x72"] = dict(status=r["status"], net=round(float(xs[-1]-xs[0]), 3),
                           x=[round(float(v),3) for v in xs[::9]])
print("mirror_B_x72", out["mirror_B_x72"], flush=True)

json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "anchor2.json"), "w"), indent=1)
print("DONE")
