"""Audit wrapper (construction lens): the claimed world.py, UNCHANGED, plus two passive tagged copies of s.

e, p, F, s are advanced by the claim's own step() (imported from the claim directory, not copied).
s is linear in itself (production ks_s*cat, upwind drift up grad 4e(1-e), diffusion, decay), so it splits
exactly into source-tagged parts that obey the same operator:
  s_body : s produced where e > 0.5 (inside a body)                      [mask from the pre-step e]
  s_band : s produced in the band 0 < distance <= 3 px outside the e=0.5 contour (the interface/rim side)
  s_far  = s - s_body - s_band : s produced farther than 3 px from any body (the medium)
Masks are refreshed every 10 steps (1 t); bodies move < 0.004 px/t.
Side effects (audit only): every LOG_DT t a per-body source split of the rim s is appended to TAG_LOG,
and the full state is saved at the times in TAG_SAVE (npz) for forks.
"""
import importlib.util
import json
import os

import numpy as np
from scipy import ndimage

from labkit import ops

CLAIM = "/home/user/physim/research/alife/collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py"
_spec = importlib.util.spec_from_file_location("claimworld", CLAIM)
w = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(w)

META = dict(w.META)
META["name"] = "cips-layered-divide-audit-tagged"
META["channels"] = ["e", "p", "F", "s", "s_body", "s_band"]
P = w.P
OUTD = os.environ.get("TAG_DIR", ".")
LOG_DT = float(os.environ.get("TAG_LOG_DT", "250"))
SAVE = [float(x) for x in os.environ.get("TAG_SAVE", "").split(",") if x]


def init(seed, size):
    s = w.init(seed, size)
    H, W = s["shape"]
    s["sx"] = np.zeros((2, H, W))   # [s_body, s_band]
    s["k"] = 0
    s["seed"] = seed
    s["next_log"] = LOG_DT
    s["saved"] = set()
    s["log"] = os.path.join(OUTD, f"tag_s{seed}.jsonl")
    open(s["log"], "w").close()
    return s


def _masks(e):
    m = e > 0.5
    dout = ndimage.distance_transform_edt(~m) if m.any() else np.full(e.shape, 1e9)
    band = (~m) & (dout <= 3.0)
    return m.astype(float), band.astype(float)


def per_body(e, sv, sb, sn, cat):
    H, W = e.shape
    pad = 24
    E = np.pad(e, pad, mode="wrap"); S = np.pad(sv, pad, mode="wrap")
    SB = np.pad(sb, pad, mode="wrap"); SN = np.pad(sn, pad, mode="wrap")
    m = E > 0.5
    din = ndimage.distance_transform_edt(m)
    dout, (iy, ix) = ndimage.distance_transform_edt(~m, return_indices=True)
    lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    near = lab[iy, ix]
    res = []
    for i in range(1, n + 1):
        b = lab == i
        cy, cx = ndimage.center_of_mass(b)
        if not (pad <= cy < pad + H and pad <= cx < pad + W):
            continue
        rim = (b & (din <= 1.5)) | ((near == i) & (dout <= 1.5) & ~m)
        catch = b | ((near == i) & (dout <= 7) & ~m)
        core = b & (din >= 3)
        outs = (near == i) & (dout >= 4) & (dout <= 7)
        tot = S[rim].sum()
        if tot <= 0 or b.sum() < 6:
            continue
        res.append({"cy": float(cy - pad), "cx": float(cx - pad), "area": int(b.sum()),
                    "rim_body": float(SB[rim].sum() / tot), "rim_band": float(SN[rim].sum() / tot),
                    "rim_far": float(1 - (SB[rim].sum() + SN[rim].sum()) / tot),
                    "catch_body": float(SB[catch].sum() / S[catch].sum()),
                    "rim_core": float(S[rim].mean() / max(S[core].mean(), 1e-12)) if core.sum() >= 3 else None,
                    "rim_out": float(S[rim].mean() / max(S[outs].mean(), 1e-12)) if outs.sum() >= 3 else None})
    return res


def step(s):
    q = s["par"]
    dt = q["dt"]
    if s["k"] % 10 == 0:
        mb, mn = _masks(s["e"])
        s["mx"] = np.stack([mb, mn])
    cat = q["kc"] * s["F"] * np.clip(s["e"], 0, None) ** q["n"] * (1 - s["p"])
    w.step(s)  # the claim's own step: e, p, F, s
    ec = np.clip(s["e"], 0, 1)
    wi = 4 * ec * (1 - ec)
    c = q["Ds"] * q["chi_s"] * q["Lsc"] ** 2
    u = s["sx"]
    uv = u - dt * w.up_flux_div(u, wi, c) + dt * q["ks_s"] * cat * s["mx"]
    s["sx"] = ops.irfft2(ops.rfft2(uv) * s["Ls"], s["shape"])
    s["k"] += 1
    t = s["t"]
    if t >= s["next_log"] - 1e-9:
        s["next_log"] += LOG_DT
        m = s["e"] > 0.5
        rec = {"t": round(t, 1), "bodies": per_body(s["e"], s["s"], s["sx"][0], s["sx"][1], cat),
               "cat_share_body": float((cat * s["mx"][0]).sum() / cat.sum()),
               "cat_share_band": float((cat * s["mx"][1]).sum() / cat.sum()),
               "s_total": float(s["s"].sum()), "sb_total": float(s["sx"][0].sum()), "sn_total": float(s["sx"][1].sum()),
               "body_area": int(m.sum()), "mean_e": float(s["e"].mean()), "mean_F": float(s["F"].mean())}
        with open(s["log"], "a") as f:
            f.write(json.dumps(rec) + "\n")
    for ts in SAVE:
        if ts not in s["saved"] and t >= ts - 1e-9:
            s["saved"].add(ts)
            np.savez(os.path.join(OUTD, f"state_s{s['seed']}_t{int(ts)}.npz"), e=s["e"], p=s["p"], F=s["F"],
                     s=s["s"], sx=s["sx"], t=s["t"])
    return s


def fields(s):
    return np.concatenate([np.stack([s["e"], s["p"], s["F"], s["s"]]), s["sx"]])


def damage(s, mask):
    return w.damage(s, mask)
