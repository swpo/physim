"""offline_views -- CPU recomputation of an exam job's simulation-trained policies from its saved arrays, on three
views of every item: the full level-1 history (job 2's features), the last three ticks, and the anchor state only.

    python -B offline_views.py JOB_OUT_DIR [--steps 3000] [--tag A]      -> results/offline_views[_TAG].json

PILOT: the truths are public by design; never to be reused as an exam.

Why. In job 2 (r5-vortexexam-003) the net trained on prior simulations (P0) matched the net given the true
parameters (C): with the full history an item gives its hidden parameters away. This script asks how much of that
is the history: the same families are refitted with the history channels masked beyond the first k lags
(vxnet.lag_mask), k = 8 (all lags, up to 64 ticks), 3 (ticks a, a-1, a-2) and 1 (the state at the anchor).
It is also an independent recomputation of the pod's full-history scores: same design episodes, Lab episodes,
items and replicate truths (from design*.npz, lab.npz, exam.npz, items.npz, posterior_draws.npz; the summaries
are stored as float16), other seeds, CPU float32 nets.

Policies per family (net, ridge) and view: P0 (unconditional, design episodes), C (theta-conditional at the
truth), PM (at the prior mean of the box), S@n (posterior draws from n Lab episodes, level-1 summaries), D@n
(fitted to the first n Lab episodes). The law family (T = law|D@n) uses the anchor state only and is the same in
every view. K and O are read from the job's scores.npz.
sigma = (L(null) - L(C)) / (L(K) - L(C)) per family and view, null = the better of D at the largest budget and P0;
bootstrap over truths.
"""
import argparse
import glob
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import vxlib as VX  # noqa: E402
import vxnet as NN  # noqa: E402

import numpy as np  # noqa: E402

from vw.scoring import energy_fair  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("job")
ap.add_argument("--steps", type=int, default=3000)
ap.add_argument("--tag", default="")
ap.add_argument("--m", type=int, default=64)
args = ap.parse_args()
D = args.job
RES = os.environ.get("VX_RES", os.path.join(HERE, "results"))
MARK = "PILOT_NEVER_REUSE_AS_EXAM"
T0 = time.time()

info = json.load(open(os.path.join(D, "info.json")))
PR = info["prior"]
NAMES = list(PR["names"])
LO, HI = np.array(PR["lo"], float), np.array(PR["hi"], float)
CEN, HW = (LO + HI) / 2, (HI - LO) / 2
D_TH = len(NAMES)
VX.T_EP, VX.PROG_TICKS, VX.C_PROG, VX.HS = int(PR["T_ep"]), tuple(PR["prog_ticks"]), float(PR["c_prog"]), tuple(PR["hs"])
NN.set_const(PR.get("const", {}))
PROG, HS = list(VX.PROG_TICKS), list(VX.HS)
VIEWS = {"full": None, "last3": 3, "state": 1}
m = args.m


def log(msg):
    print(f"[{time.time() - T0:6.0f}s] {msg}", flush=True)


def dense(z):
    U = np.zeros(tuple(int(x) for x in z["U_shape"]), np.float32)
    idx = z["U_idx"]
    U[tuple(idx.T)] = z["U_val"]
    return U


def to_u(theta):
    return (np.asarray(theta, float) - CEN) / HW


def mask(X, k):
    return X if k is None else np.asarray(X, np.float32) * NN.lag_mask(k, np.shape(X)[-1])


def mds(ds, k):
    return ds if k is None else dict(ds, Xtr=mask(ds["Xtr"], k), Xva=mask(ds["Xva"], k))


def es_joint(samples, truths):
    """samples (n, m, nh, 2), truths (n, R, nh, 2) -> (n, nh) fair energy score of level 2 jointly (scaled)."""
    sc = NN.sc2()
    return np.stack([energy_fair(samples[:, :, j] / sc, truths[:, :, j] / sc) for j in range(samples.shape[2])], 1)


# ----------------------------------------------------------------------------- data
dz = np.load(os.path.join(D, "design.npz"))
Sd = np.concatenate([np.load(p)["S"].astype(np.float32) for p in sorted(glob.glob(os.path.join(D, "design_S_*.npz")))])
Ud = dense(dz)
Kd = int(dz["K_d"])
thu = np.repeat(dz["u"].astype(float), Kd, 0)
ok = dz["viable"].reshape(-1).astype(bool)
ez = np.load(os.path.join(D, "exam.npz"))
exS = ez["S"].astype(np.float32)                                  # (nT, J, T+1, 14)
nT, J = exS.shape[:2]
exU = dense(ez).reshape(nT, J, VX.T_EP, -1)
iz = np.load(os.path.join(D, "items.npz"))
Yi, L2a = iz["Y"].astype(float), iz["L2a"].astype(float)          # (nT, nI, R, nh, 2), (nT, nI, 2)
nI = Yi.shape[1]
lz = np.load(os.path.join(D, "lab.npz"))
labS = lz["S"].astype(np.float32)                                 # (nT, nL, T+1, 14)
nL = labS.shape[1]
labU = dense(lz).reshape(nT, nL, VX.T_EP, -1)
truths = np.array(json.load(open(os.path.join(D, "truths.json")))["truths"], float)
pz = np.load(os.path.join(D, "posterior_draws.npz"))
budgets = sorted({int(k.split("_n")[1]) for k in pz.files if k.startswith("L1_")})
sz = np.load(os.path.join(D, "scores.npz"))
PRIM = [0, 3, 6][:len(HS)]                                        # the joint cells of the pod's (nh x 3) layout
LK = sz["K"].astype(float)[:, :, PRIM]                            # (nT, nI, nh)
LO_ = sz["oracle"].astype(float)[:, :, PRIM]
pod = {k: float(sz[k].astype(float)[:, :, PRIM].mean()) for k in sz.files if k != MARK and not k.startswith("mean|")}
log(f"design {int(ok.sum())} viable episodes of {len(ok)}, {nT} truths x {nI} items, Lab {nL} episodes, budgets {budgets}")

ds_p0 = NN.dataset(Sd[ok], Ud[ok], seed=11)
ds_c = NN.dataset(Sd[ok], Ud[ok], theta_u=thu[ok], seed=11)
Xi, Xc = [], []
for i in range(nT):
    X, _, la = NN.features(exS[i], exU[i], PROG)
    Xz, _, _ = NN.features(exS[i], exU[i], PROG, theta_u=np.zeros((J, D_TH)))
    Xi.append(X.reshape(nI, len(HS), -1))
    Xc.append(Xz.reshape(nI, len(HS), -1))
    assert np.abs(la.reshape(nI, 2) - L2a[i]).max() < 0.02, "items.npz does not match exam.npz"
rng = np.random.default_rng(3)
SC = {}                                                           # name -> (nT, nI, nh)


def put(name, per_truth_samples):
    SC[name] = np.stack([es_joint(NN.to_level2(s, L2a[i]), Yi[i]) for i, s in enumerate(per_truth_samples)])


def samples(fam, model, X, seed):
    if fam == "net":
        return NN.net_samples(model, X, m, seed)
    if fam == "ridge":
        return NN.ridge_samples(model, X, m, seed)
    return NN.law_samples(model, X, m, seed)


def fit(fam, dsets, d_theta, steps, seed, tag):
    if fam == "net":
        params, tinfo = NN.train_nets(dsets, steps=steps, seed=seed)
        log(f"  net {tag}: best step {tinfo['best_step']} val {np.round(tinfo['best_val'], 4).tolist()} ({tinfo['seconds']:.0f}s)")
        return params
    if fam == "ridge":
        return [NN.fit_ridge(d, seed=seed) for d in dsets]
    return [NN.fit_law(d, d_theta=d_theta, seed=seed) for d in dsets]


for view, k in VIEWS.items():
    for fam in ("ridge", "net"):
        v = f"{fam}[{view}]"
        mp0 = fit(fam, [mds(ds_p0, k)], 0, args.steps, 300, v + "|P0")[0]
        mc = fit(fam, [mds(ds_c, k)], D_TH, args.steps, 301, v + "|cond")[0]
        put(v + "|P0", [samples(fam, mp0, mask(Xi[i], k), 400 + i) for i in range(nT)])
        put(v + "|C", [samples(fam, mc, mask(NN.with_theta(Xc[i], to_u(truths[i])), k), 410 + i) for i in range(nT)])
        put(v + "|PM", [samples(fam, mc, mask(NN.with_theta(Xc[i], np.zeros(D_TH)), k), 420 + i) for i in range(nT)])
        for n in budgets:
            Xs = []
            for i in range(nT):
                dd = to_u(pz[f"L1_t{i}_n{n}"].astype(float))
                Xs.append(mask(NN.with_theta(Xc[i], dd[rng.choice(len(dd), nI * m)].reshape(nI, m, D_TH)), k))
            put(v + f"|S@{n}", [samples(fam, mc, Xs[i], 440 + n + i) for i in range(nT)])
            dsl = [mds(NN.dataset(labS[i][:n], labU[i][:n], seed=100 + n + i), k) for i in range(nT)]
            md = fit(fam, dsl, 0, min(args.steps, {1: 600, 2: 800, 4: 1000, 8: 1500, 16: 2000}.get(n, 1500)), 500 + n, v + f"|D@{n}")
            put(v + f"|D@{n}", [samples(fam, md[i], mask(Xi[i], k), 600 + n + i) for i in range(nT)])
        log(f"{v}: P0 {SC[v + '|P0'].mean():.4f} C {SC[v + '|C'].mean():.4f} PM {SC[v + '|PM'].mean():.4f} "
            f"D@{budgets[-1]} {SC[v + f'|D@{budgets[-1]}'].mean():.4f} (K {LK.mean():.4f}, O {LO_.mean():.4f})")
for n in budgets:                                                  # T: the law fitted to n Lab episodes
    dsl = [NN.dataset(labS[i][:n], labU[i][:n], seed=100 + n + i) for i in range(nT)]
    md = fit("law", dsl, 0, 0, 500 + n, f"law|D@{n}")
    put(f"law|D@{n}", [samples("law", md[i], Xi[i], 600 + n + i) for i in range(nT)])

# ----------------------------------------------------------------------------- report
Lk, Lo = float(LK.mean()), float(LO_.mean())
boots = np.random.default_rng(0).integers(0, nT, size=(1000, nT))


def skill(name):
    return (Lk - float(SC[name].mean())) / (Lk - Lo)


def share(num_a, num_b, den_a, den_b):
    """(L(a) - L(b)) / (L(c) - L(d)) with a bootstrap over truths; arguments are (nT, nI, nh) arrays."""
    na, da = (num_a - num_b).mean((1, 2)), (den_a - den_b).mean((1, 2))
    bs = np.array([na[q].mean() / da[q].mean() for q in boots])
    return {"value": float(na.mean() / da.mean()), "se_truths": float(bs.std()),
            "p05_p95": [float(np.quantile(bs, 0.05)), float(np.quantile(bs, 0.95))]}


nb = budgets[-1]
out = {MARK: True, "source_dir": os.path.basename(os.path.normpath(D)), "names": NAMES, "n_truths": nT,
       "n_items_per_truth": nI, "budgets": budgets, "steps": args.steps, "m": m, "views": {k: (len(NN.LAGS) if v is None else v) for k, v in VIEWS.items()},
       "lags_ticks": list(NN.LAGS), "L_K": Lk, "L_O": Lo, "skill": {k: skill(k) for k in SC},
       "pod_skill_for_comparison": {k: (Lk - pod[k]) / (Lk - Lo) for k in ("net|P0", "net|C", "net|PM", "ridge|P0", "ridge|C",
                                                                              "ridge|PM", f"net|D@{nb}", f"ridge|D@{nb}",
                                                                              f"law|D@{nb}", f"net|S@{nb}") if k in pod},
       "sigma": {}, "rho": {}, "pm_loss": {}, "history_value": {},
       "note": "skill = (L(K) - L) / (L(K) - L(O)) on the pod's primary cells (level 2 jointly at the horizons), pooled; "
               "sigma = (L(null) - L(C)) / (L(K) - L(C)), null = the better of D at the largest budget and P0, same "
               "family and view; rho = (L(P0) - L(S@n)) / (L(P0) - L(C)); pm_loss = skill(C) - skill(PM); history_value "
               "= skill(P0, full) - skill(P0, view); se = bootstrap over truths"}
for view in VIEWS:
    for fam in ("ridge", "net"):
        v = f"{fam}[{view}]"
        p0, c, dn = SC[v + "|P0"], SC[v + "|C"], SC[v + f"|D@{nb}"]
        null = p0 if p0.mean() <= dn.mean() else dn
        out["sigma"][v] = dict(share(null, c, LK, c), null_is="P0" if p0.mean() <= dn.mean() else "D")
        out["sigma"][v + " (null = P0)"] = share(p0, c, LK, c)
        for n in budgets:
            out["rho"][v + f"@{n}"] = share(p0, SC[v + f"|S@{n}"], p0, c)
        out["pm_loss"][v] = share(SC[v + "|PM"], c, LK, LO_)
        out["history_value"][v] = share(p0, SC[f"{fam}[full]|P0"], LK, LO_)
    # the strongest null of the view against the strongest C of the view (over ridge, net and the law T)
    cands_null = [f"{f}[{view}]|P0" for f in ("ridge", "net")] + [f"{f}[{view}]|D@{nb}" for f in ("ridge", "net")] + [f"law|D@{nb}"]
    cands_c = [f"{f}[{view}]|C" for f in ("ridge", "net")]
    kn, kc = min(cands_null, key=lambda q: SC[q].mean()), min(cands_c, key=lambda q: SC[q].mean())
    out["sigma"][f"best[{view}]"] = dict(share(SC[kn], SC[kc], LK, SC[kc]), null=kn, C=kc)
TAG = args.tag
json.dump(out, open(os.path.join(RES, f"offline_views{'_' + TAG if TAG else ''}.json"), "w"), indent=1)
for view in VIEWS:
    for fam in ("ridge", "net"):
        v = f"{fam}[{view}]"
        s_ = out["sigma"][v]
        print(f"{v:14s} P0 {skill(v + '|P0'):.3f} C {skill(v + '|C'):.3f} PM {skill(v + '|PM'):.3f} S@{nb} {skill(v + f'|S@{nb}'):.3f} "
              f"D@{nb} {skill(v + f'|D@{nb}'):.3f} | sigma {s_['value']:+.3f} +- {s_['se_truths']:.3f} (null {s_['null_is']}) "
              f"rho@{nb} {out['rho'][v + f'@{nb}']['value']:+.2f} +- {out['rho'][v + f'@{nb}']['se_truths']:.2f}")
    b = out["sigma"][f"best[{view}]"]
    print(f"  best[{view}]: sigma {b['value']:+.3f} +- {b['se_truths']:.3f} (null {b['null']}, C {b['C']})")
print("T:", {n: round(skill(f"law|D@{n}"), 3) for n in budgets}, "| pod:", {k: round(v, 3) for k, v in out["pod_skill_for_comparison"].items()})
