
import sys, time, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/motility")
from sim import run
from metrics import window_metrics

OUT = "/Users/spoho/Documents/prime/test/physim/probes/blobs/motility"
# decisive wall encounter: tau=5.4 (euler steady c~0.11), no-flux, launched at
# (60,48) heading +x (0 deg); wall at x=96 -> contact ~ t=300; watch to 800.
P = dict(k1=-0.7, Dv=0.65, tau=5.4)
t0 = time.time()
r = run(p=P, T=800.0, dx=0.5, stepper="euler", boundary="neumann",
        center=(60.0, 48.0), kick_angle=0.0, snap_times=(0.0,200.0,300.0,400.0,500.0,600.0,800.0))
segs = []
for a in range(0, 800, 80):
    wm = window_metrics(r, a, a+80)
    if wm.get("ok"):
        segs.append(dict(t0=a, c=round(wm["c_med"],4), ang=round(wm["ang"],1),
                         x=round(float(r["com"][np.searchsorted(r["t"], a+40), 0]),1)))
res = dict(status=r["status"], runtime_s=round(time.time()-t0,1), segments=segs,
           end_pos=[round(float(x),2) for x in r["com"][-1]],
           nc_end=int(r["ncomp"][-1]) if len(r["ncomp"]) else -1,
           area_end=float(r["area"][-1]) if len(r["area"]) else 0)
print(json.dumps(res, indent=1), flush=True)
json.dump(res, open(OUT + "/cert8_wall.json", "w"), indent=1)
np.savez_compressed(OUT + "/cert8_wall_track.npz", t=r["t"], com=r["com"],
                    **{f"snap{k}": v for k, v in r["snaps"].items()})
