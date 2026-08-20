"""runjob.py — one rotor job per invocation; appends to results.json, saves npz.

Usage: runjob.py '<json job spec>'
Fields: id, kind, tau1, tau2, eta12, eta21, L, dx, T, blobs1, blobs2
        [[x,y,kick],...] kick = null | [ang_deg, kick_d], noise, seed, rec_tu,
        snap_times, init_from, add_blobs1/2, save_state_as, rot_center
        ("S"|"com": angle reference for omega), p_over, stop_split.
Light inline metrics (exploration); certification metrics live in metrics.py
(locked separately before cert).
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
          bfield=job.get("bfield"))

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

def series_pair(getA, getB):
    """t, sep, unwrapped angle, com for records where both identities exist."""
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

def g1(k):
    def g(i):
        P = r["pos1"][i]
        return P[k] if len(P) > k else None
    return g

def g2(k):
    def g(i):
        P = r["pos2"][i]
        return P[k] if len(P) > k else None
    return g

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

# locked rotor verdict (metrics.py) when requested
if job.get("rotor_verdict"):
    import metrics as MET
    rv = MET.rotor_verdict(t, r["pos1"], r["pos2"], r["ncomp1"], r["ncomp2"],
                           rec["T_end"])
    rec["rotor"] = {k: (round(v, 6) if isinstance(v, float) else v)
                    for k, v in rv.items()}

def poly_stats(P, W=300.0):
    """N same-species blobs: rotation about instantaneous centroid."""
    if nrec < 6 or P[0].shape[0] < 2:
        return {}
    nid = P[0].shape[0]
    if any(len(P[i]) != nid for i in range(nrec)):
        return {}
    A = np.array([P[i] for i in range(nrec)])          # (nrec, nid, 2)
    C = A.mean(axis=1, keepdims=True)
    rel = A - C
    ang = np.unwrap(np.arctan2(rel[:, :, 0], rel[:, :, 1]), axis=0)
    R = np.hypot(rel[:, :, 0], rel[:, :, 1])
    m = t >= t[-1] - W
    om = np.mean([np.polyfit(t[m], ang[m, k], 1)[0] for k in range(nid)])
    d = np.diff(C[:, 0, :][m], axis=0); dts = np.diff(t[m])
    cC = float(np.median(np.hypot(d[:, 0], d[:, 1]) / dts))
    return dict(omega_last=round(float(om), 6),
                rev_total=round(float((ang[-1] - ang[0]).mean() / 2 / np.pi), 3),
                R_mean=round(float(R[m].mean()), 3), R_std=round(float(R[m].std()), 4),
                c_com_last=round(cC, 6))

pairing = job.get("pairing", "auto")
n1 = rec.get("nc1_max", 0); n2 = rec.get("nc2_max", 0)
if (pairing == "cross" or (pairing == "auto" and n1 >= 1 and n2 >= 1)):
    ts, seps, angs, coms = series_pair(g1(0), g2(0))
    rec["cross"] = tail_stats(ts, seps, angs, coms)
elif pairing == "auto" and n1 == 2 and n2 == 0:
    ts, seps, angs, coms = series_pair(g1(0), g1(1))
    rec["pair1"] = tail_stats(ts, seps, angs, coms)
if pairing == "poly1" or (n1 >= 3 and n2 == 0):
    rec["poly1"] = poly_stats(r["pos1"])

# per-identity net displacement + end areas
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
    T1 = np.full((nrec, mx1, 2), np.nan); T2 = np.full((nrec, mx2, 2), np.nan)
    for i in range(nrec):
        if len(r["pos1"][i]): T1[i, :len(r["pos1"][i])] = r["pos1"][i]
        if len(r["pos2"][i]): T2[i, :len(r["pos2"][i])] = r["pos2"][i]
    np.savez_compressed(os.path.join(BASE, "data", job["save_track_as"] + ".npz"),
                        t=t, pos1=T1, pos2=T2,
                        ncomp1=r["ncomp1"], ncomp2=r["ncomp2"])
    rec["track_saved"] = job["save_track_as"]

n = sim.append_result(rec)
print(json.dumps({k: v for k, v in rec.items() if k != "job"}, default=str))
print(f"[{jid}] appended as record {n}")
