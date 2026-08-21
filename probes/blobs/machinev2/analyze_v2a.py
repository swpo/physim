"""analyze_v2a.py — locked-metrics analysis of a V2a cert track."""
import os, sys, json
import numpy as np
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import metrics as MET

L = 192.0
X1 = 140.0
LANE = 48.0
FLOOR_DY = 28.0

def analyze(trackname, T_run):
    d = np.load(os.path.join(BASE, "data", trackname + ".npz"))
    t = d["t"]; p1 = d["pos1"]; p2 = d["pos2"]
    a2 = d["area2"]; nc1 = d["ncomp1"]; nc2 = d["ncomp2"]
    carriers = [(p1[:, k, 1], p1[:, k, 0]) for k in range(p1.shape[1])]
    out = dict(track=trackname, census_ok=bool((nc1 == nc1[0]).all() and (nc2 == nc2[0]).all()),
               nc1=[int(nc1[0]), int(nc1[-1])], nc2=[int(nc2[0]), int(nc2[-1])])
    cargo = {}
    picks = {}
    for k, nm in ((1, "c1"), (2, "c2"), (3, "c3")):
        x = p2[:, k, 1]; y = p2[:, k, 0]
        dd = MET.cargo_delivery(t, x, y, X1, L, lane_y=LANE, areas=a2[:, k],
                                carriers=carriers)
        q = MET.queue_integrity(t, x, y, dd["t_pick"])
        f = MET.flyby_immunity(t, x, y, dd["t_sorted"])
        end = (float(x[-1] % L), float(y[-1]))
        cargo[nm] = dict(delivery=dd, queue=q, flyby=f, end_xy=end)
        picks[nm] = dd["t_pick"]
    # plug bookkeeping (infrastructure, not a delivery)
    xp = p2[:, 0, 1]; yp = p2[:, 0, 0]
    plug_pick = MET.picked(t, xp)
    qp = MET.queue_integrity(t, xp, yp, plug_pick)
    cargo["plug"] = dict(t_pick=plug_pick, queue=qp,
                         end_xy=(float(xp[-1] % L), float(yp[-1])))
    delivered = [nm for nm in ("c1", "c2", "c3") if cargo[nm]["delivery"]["delivered"]]
    tp = [v for v in picks.values() if v is not None]
    ts = [cargo[nm]["delivery"]["t_sorted"] for nm in ("c1", "c2", "c3")
          if cargo[nm]["delivery"]["t_sorted"] is not None]
    out["cargo"] = cargo
    out["n_delivered"] = len(delivered)
    out["delivered"] = delivered
    if tp:
        tp = sorted(tp)
        out["cycle_machine"] = [round(tp[i+1]-tp[i], 1) for i in range(len(tp)-1)]
    if ts and tp:
        out["cycle_service"] = [round(s - p, 1) for s, p in zip(sorted(ts), sorted(tp)[:len(ts)])]
    out["throughput_per_1000tu"] = round(len(delivered) / T_run * 1000.0, 3)
    out["queue_ok"] = all(cargo[nm]["queue"]["ok"] for nm in ("c1", "c2", "c3"))
    fl = [cargo[nm]["flyby"]["ok"] for nm in ("c1", "c2", "c3")]
    out["flyby_ok"] = all(f for f in fl if f is not None) and any(f is not None for f in fl)
    out["pass"] = bool(out["n_delivered"] >= 3 and out["queue_ok"] and
                       out["census_ok"] and out["flyby_ok"])
    return out

if __name__ == "__main__":
    import pprint
    name = sys.argv[1]; T = float(sys.argv[2]) if len(sys.argv) > 2 else 5000.0
    r = analyze(name, T)
    pprint.pprint(r, width=100)
