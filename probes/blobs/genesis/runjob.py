"""runjob.py — one genesis job per invocation; appends to results.json, saves npz.

Usage: runjob.py '<json job spec>'
Extra fields over bfield: two, tau2, eta12, eta21, blobs2/add_blobs2/ref_pos2,
binit_from (b-only load), b_scale, freeze_b, vacuum_blob_sector.
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

def _bl(key):
    return [(float(b[0]), float(b[1]), _kick(b[2])) for b in job.get(key, [])]

kw = dict(tau=job.get("tau", 5.7),
          two=job.get("two", False), tau2=job.get("tau2", 2.5),
          eta12=job.get("eta12", 0.0), eta21=job.get("eta21", 0.0),
          gamma=job.get("gamma", 0.0), tau_b=job.get("tau_b", 200.0),
          D_b=job.get("D_b", 0.0), source=job.get("source", "s2"),
          eps=job.get("eps", 0.0), kind=job.get("profile", "flat"),
          frac=job.get("frac", 0.85), n_teeth=job.get("n_teeth", 1),
          chan_eps=job.get("chan_eps", 0.0), chan_cap=job.get("chan_cap", 24.0),
          L=job.get("L", 96.0), dx=job.get("dx", 0.5), T=job.get("T", 1500.0),
          blobs=_bl("blobs"), blobs2=_bl("blobs2"),
          add_blobs=_bl("add_blobs"), add_blobs2=_bl("add_blobs2"),
          init_from=job.get("init_from"), binit_from=job.get("binit_from"),
          freeze_b=job.get("freeze_b", False), b_scale=job.get("b_scale", 1.0),
          vacuum_blob_sector=job.get("vacuum_blob_sector", False),
          noise=job.get("noise", 0.0), seed=job.get("seed", 0),
          rec_tu=job.get("rec_tu", 5.0),
          snap_times=tuple(job.get("snap_times", ())),
          p_over=job.get("p_over"), allow_empty=job.get("allow_empty", False))
if job.get("ref_pos"):
    kw["ref_pos"] = [tuple(r) for r in job["ref_pos"]]
if job.get("ref_pos2"):
    kw["ref_pos2"] = [tuple(r) for r in job["ref_pos2"]]

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
rec["b_dyn_min_end"] = round(float(r["b_min"][-1]), 6) if nrec else None
rec["b_dyn_max_end"] = round(float(r["b_max"][-1]), 6) if nrec else None
rec["b_dyn_min_all"] = round(float(r["b_min"].min()), 6) if nrec else None
rec["b_dyn_max_all"] = round(float(r["b_max"].max()), 6) if nrec else None
rec["umax_dev_max"] = round(float(r["umax_dev"].max()), 6) if nrec else None

def pack(poss, areas, prefix, ncarr):
    out = {}
    maxn = max((len(p) for p in poss), default=0)
    maxn = max(maxn, 1)
    P = np.full((nrec_used, maxn, 2), np.nan)
    A = np.full((nrec_used, maxn), np.nan)
    for i, (pp, aa) in enumerate(zip(poss, areas)):
        if len(pp):
            P[i, :len(pp)] = pp
            A[i, :len(aa)] = aa
    net = []
    for k in range(maxn):
        xk = P[:, k, 1]
        ok = np.isfinite(xk)
        net.append(round(float(xk[ok][-1] - xk[ok][0]), 3) if ok.sum() >= 2 else None)
    out[prefix + "net_x"] = net
    out[prefix + "x_end"] = [round(float(P[-1, k, 1]), 2) if np.isfinite(P[-1, k, 1]) else None
                             for k in range(maxn)]
    out[prefix + "y_end"] = [round(float(P[-1, k, 0]), 2) if np.isfinite(P[-1, k, 0]) else None
                             for k in range(maxn)]
    out[prefix + "area_end"] = [round(float(A[-1, k]), 2) if np.isfinite(A[-1, k]) else None
                                for k in range(maxn)]
    WIN = 300.0
    if nrec_used >= 8 and (ncarr[:nrec_used] == ncarr[0]).all() and ncarr[0] > 0:
        tail = tt_arr >= (tt_arr[-1] - WIN)
        qm = {}
        for k in range(maxn):
            xk = P[:, k, 1]; yk = P[:, k, 0]
            ok = tail & np.isfinite(xk)
            if ok.sum() >= 4:
                qm[prefix + f"v_x_{k}"] = round(float(np.polyfit(tt_arr[ok], xk[ok], 1)[0]), 6)
                qm[prefix + f"v_y_{k}"] = round(float(np.polyfit(tt_arr[ok], yk[ok], 1)[0]), 6)
        out[prefix + "quick"] = qm
    return out, P, A

nrec_used = nrec
tt_arr = t
if nrec:
    o1, P1, A1_ = pack(r["pos"], r["area"], "", ncomp)
    rec.update(o1)
    rec["ncomp_const"] = bool((ncomp == ncomp[0]).all())
    extra_npz = {}
    if "pos2" in r:
        nc2 = r["ncomp2"]
        o2, P2, A2_ = pack(r["pos2"], r["area2"], "s2_", nc2)
        rec.update(o2)
        rec["ncomp2_end"] = int(nc2[-1]); rec["ncomp2_max"] = int(nc2.max())
        extra_npz["pos2"] = P2; extra_npz["area2"] = A2_; extra_npz["ncomp2"] = nc2
    snaps = {}
    for kk, tup in r["snaps"].items():
        snaps[f"usnap_{kk}"] = tup[0].astype(np.float32)
        snaps[f"bsnap_{kk}"] = tup[1].astype(np.float32)
        if len(tup) > 2:
            snaps[f"u2snap_{kk}"] = tup[2].astype(np.float32)
    np.savez_compressed(os.path.join(BASE, "data", f"{jid}.npz"),
                        t=t, pos=P1, area=A1_, ncomp=ncomp,
                        b_min=r["b_min"], b_max=r["b_max"],
                        umax_dev=r["umax_dev"], **extra_npz, **snaps)

if job.get("save_state_as") and r["fields"] is not None:
    f = r["fields"]
    if len(f) == 4:
        sim.save_state(job["save_state_as"], f[0], f[1], f[2], f[3])
    else:
        sim.save_state(job["save_state_as"], f[0], f[1], f[2], f[3],
                       u2=f[4], v2=f[5], w2=f[6])
    rec["state_saved"] = job["save_state_as"]

sim.append_result(rec)
out = {k: rec[k] for k in ("id", "status", "ncomp0", "ncomp_end", "ncomp_max",
                           "net_x", "x_end", "y_end", "area_end",
                           "b_dyn_min_all", "b_dyn_max_all", "umax_dev_max",
                           "ncomp2_end", "s2_net_x",
                           "wall_s", "tu_per_s") if k in rec}
for kq in ("quick", "s2_quick"):
    if kq in rec:
        out[kq] = rec[kq]
print(json.dumps(out))
