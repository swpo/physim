"""runjob.py — one transport job per invocation; appends to results.json, saves track npz.

Usage: runjob.py '<json job spec>'
Job kinds:
  drift   : single blob in tri gradient; measures drift_speed (locked metrics).
  exist   : single blob, existence/persistence check (eps=0 or given), reports area tail.
  scatter : drifting cargo vs static obstacle chain; scatter_geometry.
  channel : cargo between two chains along x; channel_metrics (+ paired no-wall control flag).
  ratchet : sawtooth + noise; ratchet_speed / final displacement.
Common fields: id, kind, eps, profile(tri|saw|flat), dx, stepper, T, spots, noise, seed,
  rec_tu, params(overrides), stop_leave, frac, n_teeth, L.
"""
import sys, os, json
import numpy as np
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import sim, metrics

job = json.loads(sys.argv[1])
jid = job["id"]

kw = dict(eps=job.get("eps", 0.0), kind=job.get("profile", "tri"),
          frac=job.get("frac", 0.75), n_teeth=job.get("n_teeth", 4),
          L=job.get("L", 96.0), dx=job.get("dx", 0.5),
          stepper=job.get("stepper", "imexfft"), T=job.get("T", 900.0),
          spots=tuple(tuple(s) for s in job["spots"]),
          noise=job.get("noise", 0.0), seed=job.get("seed", 0),
          rec_tu=job.get("rec_tu", 10.0), p=job.get("params"),
          couple=tuple(job.get("couple", (1.0, 1.0))))
if job.get("stop_leave"):
    kw["stop_leave"] = tuple(job["stop_leave"])
if job.get("init_from"):
    src = np.load(os.path.join(BASE, "data", job["init_from"] + ".npz"))
    kw["init_F"] = src["Ffinal"].astype(float)
if job.get("track_seeds"):
    kw["track_seeds"] = [tuple(s) for s in job["track_seeds"]]

r = sim.run(**kw)
rec = dict(id=jid, kind=job["kind"], job=job, status=r["status"],
           dt=r["dt"], T_end=r["T_end"], wall_s=round(r["wall_s"], 1),
           tu_per_s=round(r["tu_per_s"], 2) if r["tu_per_s"] else None)

if r["status"] in ("no_base",):
    sim.append_result(rec)
    print(json.dumps(rec)); sys.exit()

t = r["t"]
trk = r["tracks"]
np.savez_compressed(os.path.join(BASE, "data", f"{jid}.npz"),
                    t=t, b=r["b"], base1d=r["base1d"],
                    **{f"trk{k}_{key}": np.array(trk[k][key])
                       for k in range(len(trk)) for key in ("x", "y", "area", "nc", "peak")},
                    Ffinal=r["F"].astype(np.float32))

kdef = job.get("cargo_idx", 0)
tr = trk[kdef]
if job["kind"] in ("drift", "exist"):
    x0 = (job["spots"][kdef][1] if job.get("spots")
          else job["track_seeds"][kdef][1])
    m = metrics.drift_speed(t, tr["x"], tr["y"], tr["area"], x0,
                            lone_area=job.get("lone_area"))
    rec["drift"] = m
    rec["area_tail"] = tr["area"][-5:]
    rec["nc_max"] = int(max(tr["nc"])) if tr["nc"] else 0
    rec["net_full"] = (round(float(np.nanmax(tr["x"]) - tr["x"][0]), 3)
                       if len(tr["x"]) else None)
elif job["kind"] == "scatter":
    m = metrics.scatter_geometry(t, tr["x"], tr["y"], tr["area"],
                                 x_obs=job["x_obs"], y0=job["spots"][kdef][2])
    rec["scatter"] = m
    rec["cargo_area_tail"] = tr["area"][-3:]
    # obstacle integrity: all other tracks
    rec["obstacle_final"] = [dict(x=round(trk[k]["x"][-1], 2), y=round(trk[k]["y"][-1], 2),
                                  area=trk[k]["area"][-1])
                             for k in range(len(trk)) if k != kdef]
elif job["kind"] == "channel":
    m = metrics.channel_metrics(t, tr["x"], tr["y"], tr["area"],
                                y_center=job["y_center"])
    rec["channel"] = m
    rec["obstacle_final"] = [dict(x=round(trk[k]["x"][-1], 2), y=round(trk[k]["y"][-1], 2),
                                  area=trk[k]["area"][-1])
                             for k in range(len(trk)) if k != kdef]
elif job["kind"] == "ratchet":
    m = metrics.ratchet_speed(t, tr["x"], tr["area"])
    rec["ratchet"] = m
    rec["x_final"] = round(float(tr["x"][-1]), 3) if len(tr["x"]) else None
    rec["y_final"] = round(float(tr["y"][-1]), 3) if len(tr["y"]) else None
    rec["area_tail"] = tr["area"][-3:]

n = sim.append_result(rec)
print(json.dumps(dict(id=jid, n=n, status=r["status"],
                      key=rec.get("drift") or rec.get("scatter")
                          or rec.get("channel") or rec.get("ratchet"))))
