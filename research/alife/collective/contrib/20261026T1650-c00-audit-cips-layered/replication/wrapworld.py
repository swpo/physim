"""Audit wrapper around the claim's world.py: the dynamics are the claim's step() called unchanged.
Passive extras (they never write e, p, F or s):
 - two cumulative source-labelled copies of the amphiphile s (tracers), integrated with the world's own s scheme,
   whose sources are ks_s*cat restricted to e>0.5 (body interior) and e>0.2 (interior + interface band).
   The s equation is linear in s for given e and cat, so bath share = s - copy2 (window at t=0 is exact).
   They run in windows (reset to 0 at each window start; valid ~300 t later, s lifetime 50 t).
 - every SAMPLE_DT time: per-body s layer by signed distance (ring.py definitions), body share of catalysis
   by signed distance, per-body catchment share, tracer shares in the rim; saved to AUDIT_LOG (json).
 - full state saved at SAVE_TS to AUDIT_STATE_<t>.npz
Env: AUDIT_LOG (path prefix), AUDIT_WIN (json list of [t0,t1]), AUDIT_SAVE (json list of times), AUDIT_SAMPLE (dt)
"""
import json, os, importlib.util
import numpy as np
from scipy import ndimage

_CLAIM = "/home/user/physim/research/alife/collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py"
_spec = importlib.util.spec_from_file_location("claimworld", _CLAIM)
w = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(w)
from labkit import ops

META = dict(w.META)
P = w.P
LOG = os.environ.get("AUDIT_LOG", "audit")
WIN = json.loads(os.environ.get("AUDIT_WIN", "[[0, 1500]]"))
SAVE = json.loads(os.environ.get("AUDIT_SAVE", "[]"))
SAMPLE = float(os.environ.get("AUDIT_SAMPLE", "100"))
_rows = []


def init(seed, size):
    s = w.init(seed, size)
    s["_tr"] = np.zeros((2,) + tuple(s["shape"]))
    s["_tron"] = False
    s["_next"] = SAMPLE
    s["_saved"] = set()
    s["_seed"] = seed
    return s


def _in_win(t):
    for a, b in WIN:
        if a - 1e-9 <= t < b - 1e-9:
            return (a, b)
    return None


def measure(s):
    e, sv, H, W = s["e"], s["s"], s["shape"][0], s["shape"][1]
    q = s["par"]
    cat = q["kc"] * s["F"] * np.clip(e, 0, None) ** q["n"] * (1 - s["p"])
    pad = 24
    E = np.pad(e, pad, mode="wrap"); S = np.pad(sv, pad, mode="wrap"); C = np.pad(cat, pad, mode="wrap")
    TR = np.pad(s["_tr"], ((0, 0), (pad, pad), (pad, pad)), mode="wrap")
    m = E > 0.5
    din = ndimage.distance_transform_edt(m)
    dout, (iy, ix) = ndimage.distance_transform_edt(~m, return_indices=True)
    lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    near = lab[iy, ix]
    sd = np.where(m, -din, dout)   # signed distance: <0 inside
    ctr = (slice(pad, pad + H), slice(pad, pad + W))
    sdc, cc, ssc = sd[ctr], C[ctr], S[ctr]
    bins = [(-1e9, -3), (-3, 0), (0, 3), (3, 7), (7, 1e9)]
    cat_bins = [float(cc[(sdc > a) & (sdc <= b)].sum() / cc.sum()) for a, b in bins]
    s_bins = [float(ssc[(sdc > a) & (sdc <= b)].sum() / ssc.sum()) for a, b in bins] if ssc.sum() > 0 else None
    bodies = []
    trok = s["_tron"]
    for i in range(1, n + 1):
        b = lab == i
        cy, cx = ndimage.center_of_mass(b)
        if not (pad <= cy < pad + H and pad <= cx < pad + W):
            continue
        core = b & (din >= 3)
        rim = (b & (din <= 1.5)) | ((near == i) & (dout <= 1.5) & ~m)
        outs = (near == i) & (dout >= 4) & (dout <= 7)
        catch = b | ((near == i) & ~m)
        catch10 = b | ((near == i) & ~m & (dout <= 10))
        rec = {"cy": float(cy - pad), "cx": float(cx - pad), "area": int(b.sum()),
               "cat_body_over_catch": float(C[b].sum() / C[catch].sum()),
               "cat_body_over_catch10": float(C[b].sum() / C[catch10].sum()),
               "cat_inrim_over_catch10": float(C[b | ((near == i) & (dout <= 3) & ~m)].sum() / C[catch10].sum())}
        if core.sum() >= 3 and outs.sum() >= 3 and S[core].mean() > 0 and S[outs].mean() > 0:
            rec["rim_core"] = float(S[rim].mean() / S[core].mean())
            rec["rim_out"] = float(S[rim].mean() / S[outs].mean())
        if trok and S[rim].sum() > 0:
            a0, a1, a2 = TR[0][rim].sum(), TR[1][rim].sum(), S[rim].sum()
            tr_rim = [float(a0 / a2), float((a1 - a0) / a2), float((a2 - a1) / a2)]
            rec["s_rim_from"] = tr_rim   # fraction of rim s made in e>0.5, 0.2<e<=0.5, e<=0.2
        bodies.append(rec)
    row = {"t": round(s["t"], 3), "n": len(bodies), "cat_bins": cat_bins, "s_bins": s_bins,
           "cat_body_share": float(cat[e > 0.5].sum() / cat.sum()),
           "F_mean": float(s["F"].mean()), "e_mean": float(e.mean()), "e_max": float(e.max()),
           "tr_on": bool(trok), "bodies": bodies}
    if trok and sv.sum() > 0:
        T0, T1 = s["_tr"][0], s["_tr"][1]
        row["tr_min_bath"] = float((sv - T1).min() / sv.max())   # must be >= ~0 once the window has converged
        row["s_total_from"] = [float(T0.sum() / sv.sum()), float((T1 - T0).sum() / sv.sum()), float((sv - T1).sum() / sv.sum())]
        rimall = (sdc >= -1.5) & (sdc <= 1.5)
        if rimall.any() and sv[rimall].sum() > 0:
            row["s_rimall_from"] = [float(T0[rimall].sum() / sv[rimall].sum()), float((T1 - T0)[rimall].sum() / sv[rimall].sum()),
                                    float((sv - T1)[rimall].sum() / sv[rimall].sum())]
    return row


def step(s):
    q = s["par"]; dt = q["dt"]
    win = _in_win(s["t"])
    if win is not None:
        if not s["_tron"]:
            s["_tr"][:] = 0.0; s["_tron"] = True; s["_trwin"] = win
        e0 = s["e"]
        cat = q["kc"] * s["F"] * np.clip(e0, 0, None) ** q["n"] * (1 - s["p"])
        src = np.stack([cat * (e0 > 0.5), cat * (e0 > 0.2)])   # cumulative: body interior, body+interface band
    else:
        s["_tron"] = False
    s = w.step(s)                       # the claim's dynamics, unchanged
    if win is not None:
        ec = np.clip(s["e"], 0, 1)
        wi = 4 * ec * (1 - ec)
        tr = s["_tr"]
        tv = tr - dt * w.up_flux_div(tr, wi, q["Ds"] * q["chi_s"] * q["Lsc"] ** 2) + dt * q["ks_s"] * src
        s["_tr"] = ops.irfft2(ops.rfft2(tv) * s["Ls"], s["shape"])
    if s["t"] >= s["_next"] - 1e-9:
        s["_next"] += SAMPLE
        _rows.append(measure(s))
        with open(LOG + "_log.json", "w") as fh:
            json.dump({"seed": s["_seed"], "P": {k: v for k, v in s["par"].items()}, "win": WIN, "rows": _rows}, fh)
    for ts in SAVE:
        if ts not in s["_saved"] and s["t"] >= ts - 1e-9:
            s["_saved"].add(ts)
            np.savez(f"{LOG}_state_{int(ts)}.npz", e=s["e"], p=s["p"], F=s["F"], s=s["s"], t=s["t"])
    return s


def fields(s):
    return w.fields(s)


def damage(s, mask):
    return w.damage(s, mask)
