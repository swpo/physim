"""Independent recomputation of the wind study headline numbers from results/items/*.npz (checker)."""
import json, math, sys
import numpy as np
R = sys.argv[1]
B = 2000
out = {}
def L(S, v):
    z = np.load(f"{R}/items/closure_{S}_{v}_items.npz")
    names = [str(x) for x in z["names"]]
    d = {"names": names, "err": {nm: z["err"][k].astype(float) for k, nm in enumerate(names)},
         "orac": z["orac"].astype(float), "item_j": z["item_j"], "items": z["items"]}
    for k in z.files:
        if k not in ("err", "names", "orac", "item_j", "items"):
            d[k] = z[k]
    return d
def ceil(d, idx):
    V = np.stack([d["err"][nm][idx].mean(0) for nm in d["names"]])
    V0, Vu = d["err"]["mean"][idx].mean(0), d["orac"][idx].mean(0)
    return (V0 - V.min(0)) / (V0 - Vu)
def bidx(item_j, rng):
    uj = np.unique(item_j)
    pick = rng.choice(uj, uj.size, replace=True)
    return np.concatenate([np.flatnonzero(item_j == q) for q in pick])
r4 = lambda a: np.round(np.asarray(a, float), 4).tolist()
D = {}
for S, v in [("F", "coarse"), ("M", "coarse"), ("F", "objects"), ("M", "objects"), ("F2", "objects"), ("M2", "objects")]:
    d = L(S, v); D[(S, v)] = d
    all_ = np.arange(len(d["item_j"]))
    rng = np.random.default_rng(101)
    bs = np.array([ceil(d, bidx(d["item_j"], rng)) for _ in range(B)])
    j = json.load(open(f"{R}/closure_{S}_{v}.json"))
    c = ceil(d, all_)
    out[f"ceiling_{S}_{v}"] = {"mine": r4(c), "se_mine": r4(bs.std(0)), "json": r4(j["ceiling"]), "json_se": r4(j["ceiling_se"]),
                               "max_abs_diff": float(np.abs(c - np.asarray(j["ceiling"])).max())}
# F - M paired
def fm(Fd, Md, seed):
    assert np.array_equal(Fd["items"], Md["items"])
    ij = Fd["item_j"]; rng = np.random.default_rng(seed)
    d0 = ceil(Fd, np.arange(len(ij))) - ceil(Md, np.arange(len(ij)))
    bs = []
    for _ in range(B):
        idx = bidx(ij, rng); bs.append(ceil(Fd, idx) - ceil(Md, idx))
    return d0, np.array(bs).std(0)
for tag, (a, b, v) in {"coarse": ("F", "M", "coarse"), "objects1": ("F", "M", "objects"), "objects2": ("F2", "M2", "objects")}.items():
    d0, se = fm(D[(a, v)], D[(b, v)], 7)
    out[f"FminusM_{tag}"] = {"d": r4(d0), "se": r4(se), "z": r4(d0 / se)}
d1, s1 = np.array(out["FminusM_objects1"]["d"]), np.array(out["FminusM_objects1"]["se"])
d2, s2 = np.array(out["FminusM_objects2"]["d"]), np.array(out["FminusM_objects2"]["se"])
dp, sp = (d1 + d2) / 2, np.sqrt(s1 ** 2 + s2 ** 2) / 2
out["FminusM_objects_pooled"] = {"d": r4(dp), "se": r4(sp), "z": r4(dp / sp), "loss_upper95_one_sided": r4(np.maximum(0, -dp + 1.645 * sp))}
# MW oracle cost
mw = {}
for S, v in [("M", "coarse"), ("M", "objects"), ("M2", "objects")]:
    d = D[(S, v)]
    dV = d["oracW"].astype(float) - d["orac"]
    Vb = np.min(np.stack([d["err"][nm].mean(0) for nm in d["names"]]), 0)
    rng = np.random.default_rng(3)
    bs = np.array([dV[bidx(d["item_j"], rng)].mean(0) for _ in range(B)])
    mw[f"{S}_{v}"] = {"dV_over_Vbest": r4(dV.mean(0) / Vb), "se": r4(bs.std(0) / Vb), "z": r4(dV.mean(0) / bs.std(0))}
a, b = mw["M_objects"], mw["M2_objects"]
pm = (np.array(a["dV_over_Vbest"]) + np.array(b["dV_over_Vbest"])) / 2
ps = np.sqrt(np.array(a["se"]) ** 2 + np.array(b["se"]) ** 2) / 2
mw["objects_pooled_two_pairs"] = {"dV_over_Vbest": r4(pm), "se": r4(ps), "z": r4(pm / ps),
                                  "pair_difference_z": r4((np.array(a["dV_over_Vbest"]) - np.array(b["dV_over_Vbest"])) / (2 * ps))}
out["MW"] = mw
# learning curve
lc = {}
for S, v in [("F", "coarse"), ("M", "coarse"), ("F", "objects"), ("M", "objects")]:
    d = D[(S, v)]
    best = {fr: np.min(d[f"lc_err_{fr}"].astype(float).mean(1), 0) for fr in ("0.25", "0.5", "1.0")}
    lc[f"{S}_{v}"] = {"rel_drop_half_to_all": r4((best["0.5"] - best["1.0"]) / best["0.5"]),
                      "rel_drop_quarter_to_half": r4((best["0.25"] - best["0.5"]) / best["0.25"])}
out["learning_curve"] = lc
# P
def es_pair(dl, sel, n_):
    dl = dl[sel]; d = dl.mean(1); Rr = dl.shape[1]
    sn2 = dl.var(1, ddof=1).mean(0); sb2 = np.maximum(d.var(0, ddof=1) - sn2 / Rr, 0)
    return d.mean(0) / np.sqrt((sb2 + sn2) / n_), d.mean(0) / (d.std(0, ddof=1) / math.sqrt(sel.sum()))
P = {}
for v in ("coarse", "objects"):
    d = L("P", v)
    names, err, kl, crn = d["names"], d["err"], d["klass"], d["crn"].astype(float)
    V = {nm: err[nm].mean(0) for nm in names}
    aware = [nm for nm in names if nm.endswith("+u2") or nm.endswith("+u") or nm == "aware_base"]
    blind = [nm for nm in names if nm not in aware]
    nH = 5
    best_all = [min(names, key=lambda nm: V[nm][h]) for h in range(nH)]
    best_blind = [min(blind, key=lambda nm: V[nm][h]) for h in range(nH)]
    Vb = np.array([V[best_all[h]][h] for h in range(nH)])
    prog = kl != "none"; ar = (kl == "aimed") | (kl == "regional")
    rec = {}
    net, netu = ("slotnet", "slotnet+u") if v == "objects" else ("patchnet", "patchnet+u")
    for a, b in ((net, netu), ("ridge_p2", "ridge_p2+u2")):
        dd = err[a] - err[b]
        rec[f"{a}->{b}"] = {"share_all": r4(dd.mean(0) / crn.mean(0)), "achieved_over_Vbest": r4(dd.mean(0) / Vb),
                            "ratio_V_b_over_bestblind": r4(V[b] / np.array([V[best_blind[h]][h] for h in range(nH)]))}
    es = {nm: d["es"][k].astype(float) for k, nm in enumerate([str(x) for x in d["es_names"]])}
    ESm = {nm: es[nm].mean((0, 1)) for nm in es}
    bea = [min(es, key=lambda nm: ESm[nm][h]) for h in range(nH)]
    beb = [min([n for n in es if n not in aware], key=lambda nm: ESm[nm][h]) for h in range(nH)]
    pick = lambda nms: np.stack([es[nms[h]][:, :, h] for h in range(nH)], 2)
    dl = pick(beb) - pick(bea)
    zz = {}
    for mk, sel in (("all", np.ones(len(kl), bool)), ("aimed_regional", ar)):
        for n_ in (32, 64, 128):
            zz[f"{mk}_z_n{n_}_R1"] = r4(es_pair(dl, sel, n_)[0])
        zz[f"{mk}_z_observed_all_items_6truths"] = r4(es_pair(dl, sel, 64)[1])
    idl = d["es_ideal"].astype(float)
    zi = {f"ideal_all_z_n{n_}_R1": r4(es_pair(idl, np.ones(len(kl), bool), n_)[0]) for n_ in (32, 64, 128)}
    # selection check: choose the best-by-ES on half the trajectories, z (n = 64) on the other half; 200 splits
    uj = np.unique(d["item_j"]); rng = np.random.default_rng(9); zs = []
    for s in range(200):
        half = np.isin(d["item_j"], rng.permutation(uj)[: uj.size // 2])
        for tr, te in ((half, ~half), (~half, half)):
            Ea = {nm: es[nm][tr].mean((0, 1)) for nm in es}
            ba = [min(es, key=lambda nm: Ea[nm][h]) for h in range(nH)]
            bb = [min([n for n in es if n not in aware], key=lambda nm: Ea[nm][h]) for h in range(nH)]
            zs.append(es_pair(pick(bb) - pick(ba), te, 64)[0])
    P[v] = {"best_all": best_all, "best_blind": best_blind, "best_by_es_all": bea, "best_by_es_blind": beb,
            "true_effect_programs_over_Vbest": r4(crn[prog].mean(0) / Vb),
            "true_effect_aimed_regional_over_Vbest": r4(crn[ar].mean(0) / Vb),
            "recovered": rec, "es_best_blind_to_best_all": zz, "es_ideal": zi,
            "es_z64_selection_on_other_half_mean": r4(np.nanmean(np.array(zs), 0))}
out["P"] = P
print(json.dumps(out, indent=1))
