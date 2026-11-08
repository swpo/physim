"""combine4 -- F vs M (same layout, same keys, same platform): paired comparisons, the identity-event split,
feature groups (objects), chaos curves; collects the job's headline numbers.

usage: python -B combine4.py   -> $W4_OUT/combine.json
Needs $W4_WORK/FM.npz, FM.json and closure_{F,M}_{coarse,objects}_items.npz (with predictions).
Bootstrap: 400 resamples of the trajectory index j, applied to F and M together (pairs share keys).
Event flag of an item at horizon h: some replicate (base continuation or branch) has a tracker identity
event (birth, death, fusion or fission counter change) in (t, t + h].
"""
import json
import math
import os
import time

import numpy as np

import w4

w4.setup_paths()
import wr  # noqa: E402

WD = wr.WD
WORK, OUT = w4.work_dir(), w4.out_dir()
NC, K, NF = WD.NC, WD.K_SLOTS, WD.NF
T0 = time.time()
FEATS = ("present", "mass", "frac_c1", "x_cos", "x_sin", "y_cos", "y_sin", "rg", "q1", "q2", "vx", "vy")
GROUPS = {"identity(present,mass,frac_c1)": ("present", "mass", "frac_c1"),
          "position(4)": ("x_cos", "x_sin", "y_cos", "y_sin"), "shape(rg,q1,q2)": ("rg", "q1", "q2"),
          "velocity(2)": ("vx", "vy")}


def log(*a):
    w4.progress(f"[combine4 {time.time() - T0:6.1f}s] " + " ".join(str(x) for x in a))


def jsonable(o):
    if isinstance(o, dict):
        return {str(k): jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, np.ndarray):
        return jsonable(o.tolist())
    if isinstance(o, np.floating):
        return None if not math.isfinite(float(o)) else float(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, float) and not math.isfinite(o):
        return None
    return o


def load_items(S, view):
    fn = f"{WORK}/closure_{S}_{view}_items.npz"
    if not os.path.exists(fn):
        return None
    z = np.load(fn)
    names = [str(x) for x in z["names"]]
    return {"names": names, "err": {nm: z["err"][k].astype(float) for k, nm in enumerate(names)},
            "orac": z["orac"].astype(float), "items": z["items"], "item_j": z["item_j"],
            "orac_common": z["orac_common"].astype(float), "vbest_common": z["vbest_common"].astype(float),
            "v0_common": z["v0_common"].astype(float), "preds": z["preds"], "FUT": z["FUT"], "eff": z["eff"],
            "sd": z["sd"]}


def ceiling_of(d, idx, names=None):
    names = d["names"] if names is None else names
    V = np.stack([d["err"][nm][idx].mean(0) for nm in names])
    V0, Vu = d["err"]["mean"][idx].mean(0), d["orac"][idx].mean(0)
    return (V0 - V.min(0)) / (V0 - Vu)


def boot_idx(item_j, pick):
    return np.concatenate([np.flatnonzero(item_j == q) for q in pick])


def event_flags(meta, z, S, items, HZ):
    """(n, nH) bool: an identity event in some replicate within (t, t + h]."""
    J = meta["J"]
    off = 0 if S == "F" else J
    TAB, BG = z["TAB"], z["BG"]
    fl = np.zeros((len(items), len(HZ)), bool)
    for a, (jj, i, t) in enumerate(items):
        g0 = TAB[off + jj, t, -4:]
        for hi, h in enumerate(HZ):
            ev = np.any(TAB[off + jj, t + h, -4:] != g0)
            ev = ev or np.any(BG[off + jj, i, :, h - 1, 1:] != g0[None])
            fl[a, hi] = ev
    return fl


def chaos(meta, z, S, view, eff, sd):
    """Oracle variance (standardised) vs horizon 1..TX from the branches at the first test tick + base."""
    J, t0, TX = meta["J"], meta["test_ticks"][0], meta["TX"]
    off = 0 if S == "F" else J
    sl = slice(0, NC) if view == "coarse" else slice(NC, None)
    Y = z["Y"][off:off + J][..., sl][..., eff].astype(float) / sd[eff]
    X = z["X"][off:off + J][..., sl][..., eff].astype(float) / sd[eff]
    G = np.concatenate([Y[:, t0 + 1:t0 + TX + 1][:, None], X], 1)          # (J, R, TX, q)
    R, q = G.shape[1], G.shape[-1]
    var = ((G - G.mean(1, keepdims=True)) ** 2).sum((1, 3)) / (R - 1) / q   # (J, TX)
    curve = var.mean(0)
    nat = float(Y.reshape(-1, q).var(0).mean())

    def crossing(c, level):
        idx = np.flatnonzero(c >= level)
        if idx.size == 0:
            return None
        i = int(idx[0])
        if i == 0:
            return 1.0
        a, b = np.log(c[i - 1]), np.log(c[i])
        return float(i + (np.log(level) - a) / (b - a))
    return {"curve_mean": curve, "curve_se": var.std(0, ddof=1) / math.sqrt(J), "natural_uncond": nat,
            "cross_half_natural": crossing(curve, 0.5 * nat), "cross_0.9_natural": crossing(curve, 0.9 * nat),
            "per_traj": var}


def group_errors(d, view, best_names):
    """objects: per item and horizon, oracle / mean / best errors restricted to each feature group."""
    if view != "objects":
        return None
    eidx = np.flatnonzero(d["eff"])
    feat = np.array([FEATS[q % NF] for q in eidx])
    FUT, P = d["FUT"].astype(float), d["preds"].astype(float)
    R = FUT.shape[1]
    out = {}
    for g, fs in GROUPS.items():
        sel = np.isin(feat, fs)
        og = ((FUT[..., sel] - FUT[..., sel].mean(1, keepdims=True)) ** 2).sum((1, 3)) / (R - 1) / sel.sum()
        e = {}
        for nm in ("mean",) + tuple(sorted(set(best_names))):
            k = d["names"].index(nm)
            e[nm] = ((FUT[..., sel] - P[k][:, None][..., sel]) ** 2).sum(3).mean(1) / sel.sum()
        best = np.stack([e[best_names[hi]][:, hi] for hi in range(len(best_names))], 1)
        out[g] = {"oracle": og, "mean": e["mean"], "best": best, "n_coords": int(sel.sum())}
    return out


def contrast(view, SF, SM, meta, z, HZ, with_chaos=True):
    """F vs M for one pair of sets in one view -> dict (None if the items are missing)."""
    nH = len(HZ)
    F, M = load_items(SF, view), load_items(SM, view)
    if F is None or M is None:
        log("missing items for", SF, SM, view)
        return None
    assert np.array_equal(F["items"], M["items"])
    item_j = F["item_j"]
    uj = np.unique(item_j)
    all_idx = np.arange(len(item_j))
    cF, cM = ceiling_of(F, all_idx), ceiling_of(M, all_idx)
    bF = [F["names"][k] for k in np.stack([F["err"][nm].mean(0) for nm in F["names"]]).argmin(0)]
    bM = [M["names"][k] for k in np.stack([M["err"][nm].mean(0) for nm in M["names"]]).argmin(0)]
    flF = event_flags(meta, z, "F", F["items"], HZ)
    flM = event_flags(meta, z, "M", M["items"], HZ)
    gF, gM = group_errors(F, view, bF), group_errors(M, view, bM)
    rng = np.random.default_rng(11)
    bs = {"dceil": [], "dVor_c": [], "dVbest_c": [], "dceil_noevent": []}
    bsg = {g: [] for g in (gF or {})}

    def noevent_ceiling(d, fl, idx):
        out = np.full(nH, np.nan)
        for hi in range(nH):
            ii = idx[~fl[idx, hi]]
            if len(ii) < 4:
                continue
            V = np.stack([d["err"][nm][ii, hi].mean() for nm in d["names"]])
            v0, vu = d["err"]["mean"][ii, hi].mean(), d["orac"][ii, hi].mean()
            out[hi] = (v0 - V.min()) / (v0 - vu)
        return out

    def gceil(g, idx):
        r = {}
        for lab, G_ in (("F", gF), ("M", gM)):
            e = G_[g]
            v0, vu, vb = e["mean"][idx].mean(0), e["oracle"][idx].mean(0), e["best"][idx].mean(0)
            r[lab] = (v0 - vb) / (v0 - vu)
        return r["F"] - r["M"]
    neF, neM = noevent_ceiling(F, flF, all_idx), noevent_ceiling(M, flM, all_idx)
    for b in range(400):
        pick = rng.choice(uj, uj.size, replace=True)
        idx = boot_idx(item_j, pick)
        bs["dceil"].append(ceiling_of(F, idx) - ceiling_of(M, idx))
        bs["dVor_c"].append(F["orac_common"][idx].mean(0) - M["orac_common"][idx].mean(0))
        bs["dVbest_c"].append(F["vbest_common"][idx].mean(0) - M["vbest_common"][idx].mean(0))
        bs["dceil_noevent"].append(noevent_ceiling(F, flF, idx) - noevent_ceiling(M, flM, idx))
        for g in bsg:
            bsg[g].append(gceil(g, idx))
    sd = {k: np.nanstd(np.array(v), 0) for k, v in bs.items()}
    dceil = cF - cM
    dVor = F["orac_common"].mean(0) - M["orac_common"].mean(0)
    dVb = F["vbest_common"].mean(0) - M["vbest_common"].mean(0)
    r = {"sets": [SF, SM], "n_items": int(len(item_j)), "ceiling_F": cF, "ceiling_M": cM, "best_F": bF, "best_M": bM,
         "dceiling_F_minus_M": dceil, "dceiling_se": sd["dceil"], "dceiling_z": dceil / sd["dceil"],
         "common_scale": {"V_oracle_F": F["orac_common"].mean(0), "V_oracle_M": M["orac_common"].mean(0),
                          "dV_oracle": dVor, "dV_oracle_se": sd["dVor_c"],
                          "V_best_F": F["vbest_common"].mean(0), "V_best_M": M["vbest_common"].mean(0),
                          "dV_best": dVb, "dV_best_se": sd["dVbest_c"],
                          "dV_best_over_Vbest_M": dVb / M["vbest_common"].mean(0),
                          "dV_oracle_over_Vbest_M": dVor / M["vbest_common"].mean(0),
                          "V0_F": F["v0_common"].mean(0), "V0_M": M["v0_common"].mean(0)},
         "event_split": {"share_items_with_event_F": flF.mean(0), "share_items_with_event_M": flM.mean(0),
                         "ceiling_noevent_F": neF, "ceiling_noevent_M": neM, "dceiling_noevent": neF - neM,
                         "dceiling_noevent_se": sd["dceil_noevent"]}}
    if gF is not None:
        r["feature_groups"] = {}
        for g in gF:
            cg = {}
            for lab, G_ in (("F", gF), ("M", gM)):
                e = G_[g]
                v0, vu, vb = e["mean"].mean(0), e["oracle"].mean(0), e["best"].mean(0)
                cg[lab] = {"V0": v0, "V_oracle": vu, "V_best": vb, "ceiling": (v0 - vb) / (v0 - vu)}
            d = cg["F"]["ceiling"] - cg["M"]["ceiling"]
            r["feature_groups"][g] = {"F": cg["F"], "M": cg["M"], "dceiling": d,
                                      "dceiling_se": np.std(bsg[g], 0), "n_coords": gF[g]["n_coords"]}
    if with_chaos:
        for S, d in (("F", F), ("M", M)):
            ch = chaos(meta, z, S, view, d["eff"], d["sd"])
            ch.pop("per_traj")
            r[f"chaos_{S}"] = ch
    log(SF, SM, view, "ceiling F", np.round(cF, 3).tolist(), "M", np.round(cM, 3).tolist(), "F-M",
        np.round(dceil, 3).tolist(), "se", np.round(sd["dceil"], 3).tolist())
    return r


def main():
    meta = json.load(open(f"{WORK}/FM.json"))
    z = np.load(f"{WORK}/FM.npz")
    HZ = w4.HZ_FM
    res = {"note": __doc__, "platform": meta["platform"], "sim_seconds": meta["seconds"],
           "member_ticks": meta["member_ticks"], "member_ticks_per_s": meta["member_ticks_per_s"], "views": {}}
    for view in ("coarse", "objects"):
        r = contrast(view, "F", "M", meta, z, HZ)
        if r is not None:
            res["views"][view] = r
    if os.path.exists(f"{WORK}/FM2.json"):
        meta2 = json.load(open(f"{WORK}/FM2.json"))
        z2 = np.load(f"{WORK}/FM2.npz")
        r2 = contrast("objects", "F2", "M2", meta2, z2, HZ, with_chaos=False)
        if r2 is not None:
            res["objects_pair2"] = r2
            r1 = res["views"].get("objects")
            if r1 is not None:
                pooled = {}
                for k, ks in (("dceiling_F_minus_M", "dceiling_se"),):
                    d = (np.asarray(r1[k]) + np.asarray(r2[k])) / 2
                    se = np.sqrt(np.asarray(r1[ks]) ** 2 + np.asarray(r2[ks]) ** 2) / 2
                    pooled[k], pooled[ks], pooled["dceiling_z"] = d, se, d / se
                for k in ("dV_oracle", "dV_best"):
                    d = (np.asarray(r1["common_scale"][k]) + np.asarray(r2["common_scale"][k])) / 2
                    se = np.sqrt(np.asarray(r1["common_scale"][k + "_se"]) ** 2 + np.asarray(r2["common_scale"][k + "_se"]) ** 2) / 2
                    pooled[k], pooled[k + "_se"] = d, se
                d = (np.asarray(r1["event_split"]["dceiling_noevent"]) + np.asarray(r2["event_split"]["dceiling_noevent"])) / 2
                se = np.sqrt(np.asarray(r1["event_split"]["dceiling_noevent_se"]) ** 2 +
                             np.asarray(r2["event_split"]["dceiling_noevent_se"]) ** 2) / 2
                pooled["dceiling_noevent"], pooled["dceiling_noevent_se"] = d, se
                if "feature_groups" in r1 and "feature_groups" in r2:
                    pooled["feature_groups"] = {}
                    for g in r1["feature_groups"]:
                        a, b = r1["feature_groups"][g], r2["feature_groups"][g]
                        d = (np.asarray(a["dceiling"]) + np.asarray(b["dceiling"])) / 2
                        se = np.sqrt(np.asarray(a["dceiling_se"]) ** 2 + np.asarray(b["dceiling_se"]) ** 2) / 2
                        pooled["feature_groups"][g] = {"dceiling": d, "dceiling_se": se}
                pooled["note"] = ("mean of the two independent F - M differences at the 36-trajectory layout; "
                                  "SE = sqrt(se1^2 + se2^2) / 2")
                res["objects_pooled_pairs"] = pooled
                log("objects pooled F-M", np.round(pooled["dceiling_F_minus_M"], 3).tolist(), "se",
                    np.round(pooled["dceiling_se"], 3).tolist())
    json.dump(jsonable(res), open(f"{OUT}/combine.json", "w"), indent=1)
    log("saved", f"{OUT}/combine.json")


if __name__ == "__main__":
    main()
