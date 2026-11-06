"""Checker: recompute the closure headline numbers from the saved data with independent code.
-> check/recompute.json"""
import json, sys
import numpy as np
RES = "/home/user/evalwork/vecworld/vw1/fresh/closure/results"
OUT = {}
A, B = np.load(f"{RES}/sim_A.npz"), np.load(f"{RES}/sim_B.npz")
cat = {k: np.concatenate([A[k], B[k]], 0) for k in ("Y", "TAB", "B", "BTAB", "X")}
J, T1, _ = cat["Y"].shape
TEST, HZ, R, K, NF, NX = [40, 100, 160, 220], [1, 2, 4, 8, 16, 32], 6, 12, 12, 5
OUT["shapes"] = {k: list(v.shape) for k, v in cat.items()}
OUT["dtypes"] = {k: str(v.dtype) for k, v in cat.items()}
vw0 = json.load(open("/home/user/evalwork/vecworld/integrate/results/A_gliders_certificates.json"))
fold = np.arange(J) % 4

def view(phi):
    sl = slice(0, 192) if phi == "coarse" else slice(192, None)
    Y = cat["Y"][..., sl].astype(float)
    sd = Y.reshape(-1, Y.shape[-1]).std(0)
    eff = sd > 1e-6 * sd.max()
    sd = np.where(eff, sd, 1.0)
    Z = Y[..., eff] / sd[eff]
    Bz = cat["B"][..., sl][..., eff].astype(float) / sd[eff]
    Xz = cat["X"][..., sl][..., eff].astype(float) / sd[eff]
    return Z, Bz, Xz, eff, sd

for phi in ("coarse", "objects"):
    Z, Bz, Xz, eff, sd = view(phi)
    q = Z.shape[-1]
    it = np.load(f"{RES}/closure_{phi}_items.npz")
    js = json.load(open(f"{RES}/closure_{phi}.json"))
    items = it["items"]
    my_items = np.array([(j, i, t) for j in range(J) for i, t in enumerate(TEST)])
    FUT = np.stack([np.concatenate([Z[j, [t + h for h in HZ]][None], Bz[j, i][:, [h - 1 for h in HZ]]], 0)
                    for j, i, t in my_items])                                   # (n, R, nH, q)
    orac = ((FUT - FUT.mean(1, keepdims=True)) ** 2).sum((1, 3)) / (R - 1) / q
    # own simple predictors: training mean and persistence (folds by trajectory, j % 4)
    Vmean = np.zeros((len(my_items), len(HZ))); Vpers = np.zeros_like(Vmean)
    for f in range(4):
        mu = Z[fold != f].reshape(-1, q).mean(0)
        for n, (j, i, t) in enumerate(my_items):
            if fold[j] != f: continue
            Vmean[n] = ((FUT[n] - mu) ** 2).sum(-1).mean(0) / q
            Vpers[n] = ((FUT[n] - Z[j, t]) ** 2).sum(-1).mean(0) / q
    names = [str(x) for x in it["names"]]
    err = {nm: it["err"][k].astype(float) for k, nm in enumerate(names)}
    o = {"n_items": len(items), "items_equal_mine": bool(np.array_equal(items, my_items)), "n_eff": int(q),
         "orac_maxabs_vs_saved": float(np.abs(orac - it["orac"]).max()),
         "Voracle_mine": orac.mean(0).tolist(), "Voracle_json": js["V_oracle"],
         "Vmean_mine": Vmean.mean(0).tolist(), "Vmean_json": js["V"]["mean"],
         "Vmean_item_maxabs_vs_saved": float(np.abs(Vmean - err["mean"]).max()),
         "Vpers_mine": Vpers.mean(0).tolist(), "Vpers_json": js["V"]["persistence"],
         "Vpers_item_maxabs_vs_saved": float(np.abs(Vpers - err["persistence"]).max())}
    # tau=1 errors from the saved tau-1 predictions
    P1 = it["P1"].astype(float); F1 = it["FUT1"].astype(float)
    o["F1_maxabs_vs_mine"] = float(np.abs(F1 - FUT[:, :, 0]).max())
    o["err_tau1_from_P1_maxabs"] = float(max(np.abs(((F1 - P1[k][:, None]) ** 2).sum(-1).mean(1) / q - err[nm][:, 0]).max()
                                             for k, nm in enumerate(names)))
    if phi == "coarse":
        pl = np.load(f"{RES}/closure_coarse_patchlong_items.npz")
        err["patchnet_long"] = pl["err"].astype(float)
    V = {nm: e.mean(0) for nm, e in err.items()}
    V0, Vu = V["mean"], orac.mean(0)
    def ceil(use, idx=slice(None)):
        Vb = np.min([err[nm][idx].mean(0) for nm in use], 0)
        return (err["mean"][idx].mean(0) - Vb) / (err["mean"][idx].mean(0) - orac[idx].mean(0))
    allnm = list(err)
    old = [nm for nm in allnm if nm not in ("rmlp", "slotnet", "patchnet", "patchnet_long")]
    main = [nm for nm in allnm if nm != "patchnet_long"]
    rng = np.random.default_rng(12345)
    bs = {"all": [], "old": [], "main": []}
    item_j = my_items[:, 0]
    for b in range(1000):
        pick = rng.choice(J, J, replace=True)
        idx = np.concatenate([np.flatnonzero(item_j == jj) for jj in pick])
        for k, use in (("all", allnm), ("old", old), ("main", main)):
            bs[k].append(ceil(use, idx))
    # selection check: choose on random half of trajectories, score on other half
    sel = []
    for s in range(300):
        h = rng.permutation(J)[:J // 2]
        Am = np.isin(item_j, h)
        cs = []
        for tr, te in ((Am, ~Am), (~Am, Am)):
            ch = np.argmin([err[nm][tr].mean(0) for nm in allnm], 0)
            e = np.array([err[allnm[c]][te, hi].mean() for hi, c in enumerate(ch)])
            cs.append((err["mean"][te].mean(0) - e) / (err["mean"][te].mean(0) - orac[te].mean(0)))
        sel.append(np.mean(cs, 0))
    r0 = vw0[f"closure_{phi}"]
    cA, cO = ceil(allnm), ceil(old)
    o.update({"ceiling_all": cA.tolist(), "ceiling_all_se1000": np.std(bs["all"], 0).tolist(),
              "ceiling_main": ceil(main).tolist(), "ceiling_main_se1000": np.std(bs["main"], 0).tolist(),
              "ceiling_oldset": cO.tolist(), "ceiling_oldset_se1000": np.std(bs["old"], 0).tolist(),
              "best_all": [allnm[k] for k in np.argmin([V[nm] for nm in allnm], 0)],
              "best_old": [old[k] for k in np.argmin([V[nm] for nm in old], 0)],
              "Vbest": np.min([V[nm] for nm in allnm], 0).tolist(), "V0": V0.tolist(),
              "selection_checked": np.mean(sel, 0).tolist(),
              "z_oldset_vs_vw0": ((cO - np.array(r0["ceiling"])) / np.hypot(np.std(bs["old"], 0), r0["ceiling_se"])).tolist(),
              "z_all_vs_vw0": ((cA - np.array(r0["ceiling"])) / np.hypot(np.std(bs["all"], 0), r0["ceiling_se"])).tolist()})
    # chaos
    G = np.concatenate([Z[:, None, 41:41 + 96], Xz], 1)                         # (J, R, 96, q)
    vl = ((G - G.mean(1, keepdims=True)) ** 2).sum((1, 3)) / (R - 1) / q          # (J, 96)
    cl = vl.mean(0)
    pb = [vl[rng.choice(J, J, replace=True)].mean(0) for _ in range(1000)]
    o["chaos"] = {"at": {h: float(cl[h - 1]) for h in (1, 8, 16, 32, 64, 96)},
                  "first_h_ge_0.5": int(np.argmax(cl >= 0.5)) + 1, "first_h_ge_0.9": int(np.argmax(cl >= 0.9)) + 1,
                  "max": float(cl.max()), "argmax_h": int(cl.argmax()) + 1,
                  "mean_h60_96": float(cl[59:].mean()), "mean_h60_96_se": float(np.std([p[59:].mean() for p in pb])),
                  "frac_boot_reaching_1": float(np.mean([p.max() >= 1 for p in pb])),
                  "uncond_var_mean": float(Z.reshape(-1, q).var(0).mean())}
    OUT[phi] = o

# ---------------- objects gap at tau = 1, checker's rule (gap_events.py): live = present at t or t+1;
# event = tracker code at t+1 != 0 or presence changed
Z, Bz, Xz, eff, sd = view("objects")
Yo = cat["Y"][..., 192:].astype(float); Bo = cat["B"][..., 192:].astype(float)
it = np.load(f"{RES}/closure_objects_items.npz")
names = [str(x) for x in it["names"]]
items = it["items"]
def full(a):
    o = np.zeros(a.shape[:-1] + (K * NF,)); o[..., eff] = a; return o
F1 = full(it["FUT1"].astype(float)).reshape(len(items), R, K, NF)
EVc = 3
def codes(tab):  # tab (..., K*NX + 5) -> event codes (..., K)
    return tab[..., :K * NX].reshape(tab.shape[:-1] + (K, NX))[..., EVc]
pres_t = np.stack([Yo[j, t].reshape(K, NF)[:, 0] > 0.5 for j, i, t in items])
pres1 = np.stack([np.concatenate([[Yo[j, t + 1].reshape(K, NF)[:, 0] > 0.5],
                                  Bo[j, i, :, 0].reshape(R - 1, K, NF)[..., 0] > 0.5]) for j, i, t in items])
ev1 = np.stack([np.concatenate([[codes(cat["TAB"][j, t + 1])], codes(cat["BTAB"][j, i, :, 0])]) for j, i, t in items])
live = pres_t[:, None] | pres1
event = ((ev1 != 0) | (pres1 != pres_t[:, None])) & live
gap = {"codes_seen": sorted(set(np.unique(ev1).astype(int).tolist()))}
def shares(P, reps, boot=True):
    e = ((F1 - full(P)[:, None].reshape(len(items), 1, K, NF)) ** 2)
    es = e.sum(-1)
    m = np.zeros(R, bool); m[reps] = True
    L = live & m[None, :, None]; E = event & m[None, :, None]
    r = {"share_slot_ticks": float(E.sum() / L.sum()), "share_err": float(es[E].sum() / es[L].sum()),
         "n_event": int(E.sum()), "n_live": int(L.sum()),
         "vel_share_on_eventfree": float(e[L & ~E][:, 10:12].sum() / es[L].sum())}
    if boot:
        rng = np.random.default_rng(7); bt, be = [], []
        for b in range(1000):
            pick = rng.choice(J, J, replace=True)
            idx = np.concatenate([np.flatnonzero(items[:, 0] == jj) for jj in pick])
            bt.append(E[idx].sum() / L[idx].sum()); be.append(es[idx][E[idx]].sum() / es[idx][L[idx]].sum())
        r["share_slot_ticks_se"], r["share_err_se"] = float(np.std(bt)), float(np.std(be))
    return r, e, L, E
for pn in ("slotnet", "ar1"):
    P = it["P1"][names.index(pn)].astype(float)
    gap[f"{pn}_base"], _, _, _ = shares(P, [0])
    gap[f"{pn}_all"], e, L, E = shares(P, list(range(R)))
    if pn == "slotnet":
        loo = (F1.sum(1, keepdims=True) - F1) / (R - 1)
        eo = (((F1 - loo) ** 2) * (R - 1) / R).sum(-1)
        gap["slotnet_per_event_slot_tick"] = float(e.sum(-1)[E].sum() / E.sum())
        gap["oracle_per_event_slot_tick"] = float(eo[E].sum() / E.sum())
# every tick, AR(1) (checker's gap_events.py: rho from all one-tick pairs of the training folds)
Zf = np.zeros(Yo.shape); Zf[..., eff] = Yo[..., eff] / sd[eff]
acc = np.zeros(4); per = []
for f in range(4):
    tr = fold != f
    mu = Zf[tr].reshape(-1, K * NF).mean(0)
    a = (Zf[tr, :-1] - mu).reshape(-1, K * NF); b = (Zf[tr, 1:] - mu).reshape(-1, K * NF)
    rho = (a * b).sum(0) / np.maximum((a * a).sum(0), 1e-12)
    for j in np.flatnonzero(~tr):
        e = ((Zf[j, 1:] - (mu + rho * (Zf[j, :-1] - mu))) ** 2).reshape(-1, K, NF).sum(-1)
        pt = Yo[j, :-1].reshape(-1, K, NF)[..., 0] > 0.5; p1 = Yo[j, 1:].reshape(-1, K, NF)[..., 0] > 0.5
        ev = codes(cat["TAB"][j, 1:])
        Lv = pt | p1; Ev = ((ev != 0) | (pt != p1)) & Lv
        per.append([e[Ev].sum(), e[Lv].sum(), Ev.sum(), Lv.sum()])
per = np.array(per)
rng = np.random.default_rng(8)
bb = [per[rng.choice(J, J, replace=True)].sum(0) for _ in range(1000)]
gap["ar1_every_tick"] = {"n_live": int(per[:, 3].sum()), "share_slot_ticks": float(per[:, 2].sum() / per[:, 3].sum()),
                         "share_slot_ticks_se": float(np.std([x[2] / x[3] for x in bb])),
                         "share_err": float(per[:, 0].sum() / per[:, 1].sum()),
                         "share_err_se": float(np.std([x[0] / x[1] for x in bb]))}
OUT["objects_gap_tau1"] = gap
# objects stats from the base runs
pres = Yo.reshape(J, T1, K, NF)[..., 0] > 0.5
glob = cat["TAB"][..., K * NX:]
OUT["objects_stats"] = {"median_objects": float(np.median(pres.sum(-1))),
                        "events_per_100_ticks(births,deaths,fusions,fissions)": ((glob[:, -1, 1:] - glob[:, 0, 1:]).sum(0) / (J * (T1 - 1)) * 100).tolist()}
json.dump(OUT, open("/home/user/evalwork/vecworld/vw1/fresh/closure/check/recompute.json", "w"), indent=1, default=float)
print(json.dumps(OUT, indent=1, default=float)[:20000])
