"""runjob.py — one machine job per invocation; appends to results.json, saves npz.

Usage: runjob.py '<json job spec>'
Job spec fields:
  id, kind (label), tau, eps, profile (flat|tri|saw|const), frac, n_teeth, bconst,
  L, dx, T, blobs [[x, y, kick], ...] (kick = null | [ang_deg, kick_d]),
  init_from, add_blobs, ref_pos [[x,y],...], noise, seed, rec_tu, snap_times,
  save_state_as (basename -> data/<name>.npz with u,v,w).
Light per-run metrics inline (net_x per identity, area tails, ncomp accounting);
machine-cycle certification metrics live in metrics.py (locked separately).
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

kind_prof = job.get("profile", "flat")
eps = job.get("eps", 0.0)
bconst = job.get("bconst", None)

kw = dict(tau=job.get("tau", 5.7), eps=eps, kind=kind_prof,
          frac=job.get("frac", 0.85), n_teeth=job.get("n_teeth", 1),
          chan_eps=job.get("chan_eps", 0.0), chan_cap=job.get("chan_cap", 24.0),
          L=job.get("L", 96.0), dx=job.get("dx", 0.5), T=job.get("T", 1500.0),
          blobs=blobs, add_blobs=add_blobs,
          init_from=job.get("init_from"),
          noise=job.get("noise", 0.0), seed=job.get("seed", 0),
          rec_tu=job.get("rec_tu", 5.0),
          snap_times=tuple(job.get("snap_times", ())),
          p_over=job.get("p_over"), allow_empty=job.get("allow_empty", False))
if job.get("ref_pos"):
    kw["ref_pos"] = [tuple(r) for r in job["ref_pos"]]

if bconst is not None:
    # constant-offset world: implement via p_over on k1,k4 (iso-displacement point)
    p_over = dict(kw.get("p_over") or {})
    u0 = sim.uniform_state(2.0, -0.7, 1.0, 1.5)
    p_over["k1"] = sim.M0["k1"] + u0 * bconst
    p_over["k4"] = sim.M0["k4"] + bconst
    kw["p_over"] = p_over
    kw["kind"] = "flat"; kw["eps"] = 0.0

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

# pad pos/area to (nrec, MAXN, ...) for npz; identities valid while ncomp const
if nrec:
    maxn = max(len(p) for p in r["pos"])
    P = np.full((nrec, maxn, 2), np.nan)
    A = np.full((nrec, maxn), np.nan)
    for i, (pp, aa) in enumerate(zip(r["pos"], r["area"])):
        if len(pp):
            P[i, :len(pp)] = pp
            A[i, :len(aa)] = aa
    # per-identity net displacement over the longest constant-ncomp tail
    same = ncomp == ncomp[0]
    const_all = bool(same.all())
    rec["ncomp_const"] = const_all
    net = []
    for k in range(maxn):
        xk = P[:, k, 1]
        ok = np.isfinite(xk)
        net.append(round(float(xk[ok][-1] - xk[ok][0]), 3) if ok.sum() >= 2 else None)
    rec["net_x"] = net
    rec["x_end"] = [round(float(P[-1, k, 1]), 2) if np.isfinite(P[-1, k, 1]) else None
                    for k in range(maxn)]
    rec["area_end"] = [round(float(A[-1, k]), 2) if np.isfinite(A[-1, k]) else None
                       for k in range(maxn)]
    # inline quick metrics (exploration reads; cert metrics live in metrics.py)
    WIN = 300.0
    if const_all and nrec >= 8:
        tail = t >= (t[-1] - WIN)
        qm = {}
        for k in range(maxn):
            xk = P[:, k, 1]
            ok = tail & np.isfinite(xk)
            if ok.sum() >= 4:
                qm[f"v_x_{k}"] = round(float(np.polyfit(t[ok], xk[ok], 1)[0]), 6)
        if ncomp[0] == 2:
            d = P[:, 0] - P[:, 1]
            sep = np.hypot(d[:, 0], d[:, 1])
            ok = tail & np.isfinite(sep)
            if ok.sum() >= 4:
                qm["sep_mean"] = round(float(sep[ok].mean()), 3)
                qm["sep_std"] = round(float(sep[ok].std()), 4)
            com = P.mean(axis=1)
            ok = tail & np.isfinite(com[:, 1])
            if ok.sum() >= 4:
                qm["v_com_x"] = round(float(np.polyfit(t[ok], com[ok, 1], 1)[0]), 6)
                qm["v_com_y"] = round(float(np.polyfit(t[ok], com[ok, 0], 1)[0]), 6)
        rec["quick"] = qm
    np.savez_compressed(os.path.join(BASE, "data", f"{jid}.npz"),
                        t=t, pos=P, area=A, ncomp=ncomp, b=r["b"],
                        **({f"snap_{k}": v.astype(np.float32)
                            for k, v in r["snaps"].items()}))

if job.get("save_state_as") and r["fields"] is not None:
    u, v, w = r["fields"]
    sim.save_state(job["save_state_as"], u, v, w)
    rec["state_saved"] = job["save_state_as"]

sim.append_result(rec)
print(json.dumps({k: rec[k] for k in ("id", "status", "ncomp0", "ncomp_end",
                                      "ncomp_max", "net_x", "x_end", "area_end",
                                      "wall_s", "tu_per_s") if k in rec}))
