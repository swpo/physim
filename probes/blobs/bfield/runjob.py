"""runjob.py — one bfield job per invocation; appends to results.json, saves npz.

Usage: runjob.py '<json job spec>'
Job fields: id, kind, tau, gamma, tau_b, D_b, source (s1|s2|s3),
  eps/profile/frac/n_teeth/chan_eps/chan_cap (static b, optional),
  L, dx, T, blobs [[x,y,kick],...], init_from, add_blobs, ref_pos, noise, seed,
  rec_tu, snap_times, save_state_as.
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

blobs = [(float(b[0]), float(b[1]), _kick(b[2])) for b in job.get("blobs", [])]
add_blobs = [(float(b[0]), float(b[1]), _kick(b[2])) for b in job.get("add_blobs", [])]

kw = dict(tau=job.get("tau", 5.7),
          gamma=job.get("gamma", 0.0), tau_b=job.get("tau_b", 200.0),
          D_b=job.get("D_b", 0.5), source=job.get("source", "s2"),
          eps=job.get("eps", 0.0), kind=job.get("profile", "flat"),
          frac=job.get("frac", 0.85), n_teeth=job.get("n_teeth", 1),
          chan_eps=job.get("chan_eps", 0.0), chan_cap=job.get("chan_cap", 24.0),
          L=job.get("L", 96.0), dx=job.get("dx", 0.5), T=job.get("T", 1500.0),
          blobs=blobs, add_blobs=add_blobs,
          init_from=job.get("init_from"),
          vacuum_blob_sector=job.get("vacuum_blob_sector", False),
          noise=job.get("noise", 0.0), seed=job.get("seed", 0),
          rec_tu=job.get("rec_tu", 5.0),
          snap_times=tuple(job.get("snap_times", ())),
          p_over=job.get("p_over"), allow_empty=job.get("allow_empty", False))
if job.get("ref_pos"):
    kw["ref_pos"] = [tuple(r) for r in job["ref_pos"]]

r = sim.run(**kw)
rec = dict(id=jid, kind=job.get("kind", "free"), job=job, status=r["status"],
           dt=r["dt"], wall_s=round(r["wall_s"], 1),
           tu_per_s=round(r["tu_per_s"], 2) if r["tu_per_s"] else None)

t = r["t"]
nrec = len(t)
ncomp = r["ncomp"]
rec["T_end"] = float(t[-1]) if nrec else 0.0
rec["ncomp0"] = int(ncomp[0]) if nrec else 0
rec["ncomp_end"] = int(ncomp[-1]) if nrec else 0
rec["ncomp_max"] = int(ncomp.max()) if nrec else 0
rec["ncomp_min"] = int(ncomp.min()) if nrec else 0
rec["b_dyn_min_end"] = round(float(r["b_min"][-1]), 5) if nrec else None
rec["b_dyn_max_end"] = round(float(r["b_max"][-1]), 5) if nrec else None
rec["b_dyn_min_all"] = round(float(r["b_min"].min()), 5) if nrec else None
rec["b_dyn_max_all"] = round(float(r["b_max"].max()), 5) if nrec else None

if nrec:
    maxn = max((len(p) for p in r["pos"]), default=0)
    maxn = max(maxn, 1)
    P = np.full((nrec, maxn, 2), np.nan)
    A = np.full((nrec, maxn), np.nan)
    BC = np.full((nrec, maxn), np.nan)
    for i, (pp, aa, bb) in enumerate(zip(r["pos"], r["area"], r["b_at"])):
        if len(pp):
            P[i, :len(pp)] = pp
            A[i, :len(aa)] = aa
            BC[i, :len(bb)] = bb
    same = ncomp == ncomp[0]
    rec["ncomp_const"] = bool(same.all())
    net = []
    for k in range(maxn):
        xk = P[:, k, 1]
        ok = np.isfinite(xk)
        net.append(round(float(xk[ok][-1] - xk[ok][0]), 3) if ok.sum() >= 2 else None)
    rec["net_x"] = net
    rec["x_end"] = [round(float(P[-1, k, 1]), 2) if np.isfinite(P[-1, k, 1]) else None
                    for k in range(maxn)]
    rec["y_end"] = [round(float(P[-1, k, 0]), 2) if np.isfinite(P[-1, k, 0]) else None
                    for k in range(maxn)]
    rec["area_end"] = [round(float(A[-1, k]), 2) if np.isfinite(A[-1, k]) else None
                       for k in range(maxn)]
    rec["b_core_end"] = [round(float(BC[-1, k]), 5) if np.isfinite(BC[-1, k]) else None
                         for k in range(maxn)]
    WIN = 300.0
    if rec["ncomp_const"] and nrec >= 8:
        tail = t >= (t[-1] - WIN)
        qm = {}
        for k in range(maxn):
            xk = P[:, k, 1]; yk = P[:, k, 0]
            ok = tail & np.isfinite(xk)
            if ok.sum() >= 4:
                qm[f"v_x_{k}"] = round(float(np.polyfit(t[ok], xk[ok], 1)[0]), 6)
                qm[f"v_y_{k}"] = round(float(np.polyfit(t[ok], yk[ok], 1)[0]), 6)
        com = np.nanmean(P, axis=1)
        ok = tail & np.isfinite(com[:, 1])
        if ok.sum() >= 4:
            d = np.diff(com[ok], axis=0); dts = np.diff(t[ok])
            sp = np.hypot(d[:, 0], d[:, 1]) / dts
            qm["c_com_med"] = round(float(np.median(sp)), 6)
            qm["v_com_x"] = round(float(np.polyfit(t[ok], com[ok, 1], 1)[0]), 6)
            qm["v_com_y"] = round(float(np.polyfit(t[ok], com[ok, 0], 1)[0]), 6)
        if ncomp[0] == 2:
            d = P[:, 0] - P[:, 1]
            sep = np.hypot(d[:, 0], d[:, 1])
            ok = tail & np.isfinite(sep)
            if ok.sum() >= 4:
                qm["sep_mean"] = round(float(sep[ok].mean()), 3)
                qm["sep_std"] = round(float(sep[ok].std()), 4)
        rec["quick"] = qm
    snaps = {}
    for kk, (usnap, bsnap) in r["snaps"].items():
        snaps[f"usnap_{kk}"] = usnap.astype(np.float32)
        snaps[f"bsnap_{kk}"] = bsnap.astype(np.float32)
    np.savez_compressed(os.path.join(BASE, "data", f"{jid}.npz"),
                        t=t, pos=P, area=A, bcore=BC, ncomp=ncomp,
                        b_min=r["b_min"], b_max=r["b_max"], bstat=r["b"], **snaps)

if job.get("save_state_as") and r["fields"] is not None:
    u, v, w, bdyn = r["fields"]
    sim.save_state(job["save_state_as"], u, v, w, bdyn)
    rec["state_saved"] = job["save_state_as"]

sim.append_result(rec)
out = {k: rec[k] for k in ("id", "status", "ncomp0", "ncomp_end", "ncomp_max",
                           "net_x", "x_end", "area_end", "b_core_end",
                           "b_dyn_min_all", "b_dyn_max_all",
                           "wall_s", "tu_per_s") if k in rec}
if "quick" in rec:
    out["quick"] = rec["quick"]
print(json.dumps(out))
