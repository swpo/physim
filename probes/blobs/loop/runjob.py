"""runjob.py — one factory job per invocation; appends to results.json, saves npz.

Usage: runjob.py '<json job spec>'
rotor/runjob.py fields verbatim, plus:
  bfield2       — per-species-2 isok field (else bfield shared)
  eta12/eta21   — scalar OR etafield spec dict (see sim.build_etafield)
  roller        — {"cen":[sp,id], "cargo":[sp,id]}: azimuthal advection metrics
                  of cargo about cen: r(t), unwrapped phi(t), v_tan, net stats.
  pairs         — [[spA,idA,spB,idB,"name"],...]: separation series stats.
Light inline metrics (exploration); certification metrics live in metrics.py.
"""
import sys, os, json
import numpy as np
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import sim

job = json.loads(sys.argv[1])
jid = job["id"]

def _kick(k):
    return None if k is None else (float(k[0]), float(k[1]))

def _blobs(key):
    return [(float(b[0]), float(b[1]), _kick(b[2])) for b in job.get(key, [])]

kw = dict(tau1=job.get("tau1", 5.7), tau2=job.get("tau2", 2.5),
          eta12=job.get("eta12", 0.0), eta21=job.get("eta21", 0.0),
          L=job.get("L", 96.0), dx=job.get("dx", 0.5), dt=job.get("dt", 0.02),
          T=job.get("T", 1500.0),
          blobs1=_blobs("blobs1"), blobs2=_blobs("blobs2"),
          add_blobs1=_blobs("add_blobs1"), add_blobs2=_blobs("add_blobs2"),
          init_from=job.get("init_from"),
          noise=job.get("noise", 0.0), seed=job.get("seed", 0),
          rec_tu=job.get("rec_tu", 5.0),
          snap_times=tuple(job.get("snap_times", ())),
          p_over=job.get("p_over"), stop_split=job.get("stop_split", True),
          bfield=job.get("bfield"), bfield2=job.get("bfield2"))

r = sim.run(**kw)
rec = dict(id=jid, kind=job.get("kind", "free"), job=job, status=r["status"],
           dt=r["dt"], wall_s=round(r["wall_s"], 1),
           tu_per_s=round(r["tu_per_s"], 2) if r["tu_per_s"] else None)

t = r["t"]; nrec = len(t)
rec["T_end"] = float(t[-1]) if nrec else 0.0
for sp in (1, 2):
    nc = r[f"ncomp{sp}"]
    if len(nc):
        rec[f"nc{sp}_end"] = int(nc[-1]); rec[f"nc{sp}_max"] = int(nc.max())

L = r["L"]

def get_pos(sp, k):
    def g(i):
        P = r[f"pos{sp}"][i]
        return P[k] if len(P) > k else None
    return g

def series_pair(getA, getB):
    ts, seps, angs, coms = [], [], [], []
    for i in range(nrec):
        a = getA(i); b = getB(i)
        if a is None or b is None:
            continue
        d = a - b
        ts.append(t[i]); seps.append(float(np.hypot(*d)))
        angs.append(float(np.arctan2(d[0], d[1])))
        coms.append((a + b) / 2)
    ts = np.array(ts); seps = np.array(seps)
    angs = np.unwrap(np.array(angs)) if len(angs) else np.array([])
    coms = np.array(coms) if len(coms) else np.zeros((0, 2))
    return ts, seps, angs, coms

def tail_stats(ts, seps, angs, coms, W=300.0):
    if len(ts) < 6:
        return {}
    m = ts >= ts[-1] - W
    out = dict(sep_mean=round(float(seps[m].mean()), 3),
               sep_std=round(float(seps[m].std()), 4),
               sep_end=round(float(seps[-1]), 3))
    if m.sum() >= 3:
        om = np.polyfit(ts[m], angs[m], 1)[0]
        out["omega_last"] = round(float(om), 6)
        out["rev_total"] = round(float((angs[-1] - angs[0]) / (2 * np.pi)), 3)
        d = np.diff(coms[m], axis=0); dts = np.diff(ts[m])
        sp = np.hypot(d[:, 0], d[:, 1]) / dts
        out["c_com_last"] = round(float(np.median(sp)), 6)
    return out

if job.get("rotor_verdict"):
    import metrics as MET
    rv = MET.rotor_verdict(t, r["pos1"], r["pos2"], r["ncomp1"], r["ncomp2"],
                           rec["T_end"])
    rec["rotor"] = {k: (round(v, 6) if isinstance(v, float) else v)
                    for k, v in rv.items()}

# ---- roller advection metrics: cargo about a (near-)static center identity
if job.get("roller"):
    cen_sp, cen_id = job["roller"]["cen"]
    car_sp, car_id = job["roller"]["cargo"]
    ts, rr, ph, _ = series_pair(get_pos(car_sp, car_id), get_pos(cen_sp, cen_id))
    RO = {}
    if len(ts) >= 6:
        RO["n"] = int(len(ts))
        RO["r0"] = round(float(rr[0]), 3); RO["r_end"] = round(float(rr[-1]), 3)
        RO["r_min"] = round(float(rr.min()), 3); RO["r_max"] = round(float(rr.max()), 3)
        RO["dphi_net"] = round(float(ph[-1] - ph[0]), 4)
        RO["arc_net"] = round(float((ph[-1] - ph[0]) * rr.mean()), 3)
        W = 500.0
        m = ts >= ts[-1] - W
        if m.sum() >= 3:
            om = float(np.polyfit(ts[m], ph[m], 1)[0])
            RO["omega_last"] = round(om, 6)
            RO["vtan_last"] = round(om * float(rr[m].mean()), 5)
        # whole-track secular rate (robust to graze oscillation)
        om_all = float(np.polyfit(ts, ph, 1)[0])
        RO["omega_all"] = round(om_all, 6)
        RO["vtan_all"] = round(om_all * float(rr.mean()), 5)
    rec["roller"] = RO

if job.get("pairs"):
    PR = {}
    for (sa, ia, sb, ib, name) in job["pairs"]:
        ts, seps, angs, coms = series_pair(get_pos(sa, ia), get_pos(sb, ib))
        PR[name] = tail_stats(ts, seps, angs, coms)
        if len(ts) >= 2:
            PR[name]["sep0"] = round(float(seps[0]), 3)
            PR[name]["sep_min"] = round(float(seps.min()), 3)
            PR[name]["sep_max"] = round(float(seps.max()), 3)
    rec["pairs"] = PR

# per-identity net displacement + end positions/areas
for sp in (1, 2):
    P = r[f"pos{sp}"]; A = r[f"area{sp}"]
    if nrec and len(P[0]):
        nid = len(P[0])
        net, endp, enda = [], [], []
        for k in range(nid):
            tr = [P[i][k] for i in range(nrec) if len(P[i]) > k]
            if len(tr) >= 2:
                net.append(round(float(np.hypot(*(tr[-1] - tr[0]))), 2))
                endp.append([round(float(x), 2) for x in tr[-1]])
            aa = [A[i][k] for i in range(nrec) if len(A[i]) > k]
            enda.append(round(aa[-1], 2) if aa else None)
        rec[f"net{sp}"] = net; rec[f"end{sp}"] = endp; rec[f"area{sp}_end"] = enda

if job.get("save_state_as") and r["fields"] is not None:
    sim.save_state(job["save_state_as"], r["fields"])
    rec["state_saved"] = job["save_state_as"]

if job.get("save_track_as") and nrec:
    mx1 = max((len(p) for p in r["pos1"]), default=0)
    mx2 = max((len(p) for p in r["pos2"]), default=0)
    T1 = np.full((nrec, max(mx1, 1), 2), np.nan)
    T2 = np.full((nrec, max(mx2, 1), 2), np.nan)
    for i in range(nrec):
        if len(r["pos1"][i]): T1[i, :len(r["pos1"][i])] = r["pos1"][i]
        if len(r["pos2"][i]): T2[i, :len(r["pos2"][i])] = r["pos2"][i]
    A1 = np.full((nrec, max(mx1, 1)), np.nan)
    A2 = np.full((nrec, max(mx2, 1)), np.nan)
    for i in range(nrec):
        if len(r["area1"][i]): A1[i, :len(r["area1"][i])] = r["area1"][i]
        if len(r["area2"][i]): A2[i, :len(r["area2"][i])] = r["area2"][i]
    np.savez_compressed(os.path.join(BASE, "data", job["save_track_as"] + ".npz"),
                        t=t, pos1=T1, pos2=T2, area1=A1, area2=A2,
                        ncomp1=r["ncomp1"], ncomp2=r["ncomp2"])
    rec["track_saved"] = job["save_track_as"]

if job.get("save_snaps_as") and r["snaps"]:
    sn = r["snaps"]
    times = sorted(sn.keys())
    np.savez_compressed(os.path.join(BASE, "data", job["save_snaps_as"] + ".npz"),
                        times=np.array(times),
                        u1=np.stack([sn[k][0] for k in times]).astype(np.float32),
                        u2=np.stack([sn[k][1] for k in times]).astype(np.float32))
    rec["snaps_saved"] = job["save_snaps_as"]

n = sim.append_result(rec)
print(json.dumps({k: v for k, v in rec.items() if k != "job"}, default=str))
print(f"[{jid}] appended as record {n}")
