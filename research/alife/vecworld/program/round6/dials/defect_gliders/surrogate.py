"""surrogate -- a second, stronger history-only surrogate on the saved futures (numpy only, seconds).

screen.py's INC surrogate adds other states' increments to the item's start, so it cannot express a change
that is proportional to what the item's own blocks hold (a conversion). LLR(law) is a small predictor family
that can, trained by simulation under `law` exactly as P0 (law = public) and C (law = true) are:

    for every horizon and every region class (blocks under the program's input / their 8 neighbours / the
    rest), a ridge regression from a block's own three numbers at the start (mean c0, mean c1, m2, and 1) to
    its three numbers at the horizon, fitted on the OTHER states' futures under `law` and the same program
    class; the forecast ensemble for an item is that map applied to the item's own start plus the fitted
    residual fields of the training futures, moved so that the pushed blocks coincide.

No micro-state and no future of the item is used. Reported per candidate and program, pooled over the
horizons present: share = (L(LLR public) - L(LLR true)) / (L(K) - L(LLR true)) with a jackknife SE over
states, the skill of LLR true relative to the oracle, and kept = (L(LLR public) - L(LLR true)) / (L(PLUG) - L(O)),
the fraction of the state-given loss that survives without the state.
Reads fut_<cand>_<eta>_<prog>.npz (screen.py) and fut16_*.npz (views.py) from the scratch directory.
Writes results/surrogate.json. PILOT, design phase.
"""
import glob
import json
import os
import sys

sys.dont_write_bytecode = True
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
GEX = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "track2", "gliders_exam")
SC1 = np.load(os.path.join(GEX, "results", "scales.npz"))["level1"].astype(float)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE)))), "vw1"))
from vw.scoring import energy_fair, energy_loo, _pd  # noqa: E402

SCR = sys.argv[1] if len(sys.argv) > 1 else "/tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/dials_defect_gliders"
G, LAM = 8, 1e-2
SCB = SC1.reshape(3, G, G)


def loo_cross(X, Y):
    Rn = Y.shape[0]
    Dxy, Dxx = _pd(X, Y), _pd(X, X)
    m = Rn - 1
    return float(np.mean([Dxy[np.arange(Rn) != r, r].mean() - Dxx[np.ix_(np.arange(Rn) != r, np.arange(Rn) != r)].sum() / (2.0 * m * (m - 1))
                          for r in range(Rn)]))


def region(U_b):
    """(G, G) int: 0 far, 1 neighbour of a pushed block, 2 pushed (any tick). No input: all 0."""
    on = np.abs(U_b.reshape(-1, 2, G, G)).sum((0, 1)) > 0
    nb = np.zeros_like(on)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            nb |= np.roll(np.roll(on, dy, 0), dx, 1)
    return nb.astype(int) + on.astype(int)


def llr_scores(Ylaw, Yt, U, anc, hs):
    """L(LLR(law)) per (state, horizon). Ylaw, Yt (NS, R, T + 1, 192) unscaled; scaled inside."""
    NS, R = Yt.shape[:2]
    Zl = (Ylaw.reshape(NS, R, -1, 3, G, G) / SCB)
    Zt = (Yt.reshape(NS, R, -1, 3, G, G) / SCB)
    reg = [region(U[b]) for b in range(NS)]
    out = np.zeros((NS, len(hs)))
    for b in range(NS):
        oth = [o for o in range(NS) if o != b]
        for ih, h in enumerate(hs):
            W, resid = {}, []
            feats = lambda z0: np.concatenate([z0, np.ones_like(z0[:1])], 0)           # (4, G, G)
            for k in (0, 1, 2):
                # rows ordered (state, replicate, block) in both X and Y
                X = np.concatenate([np.tile(feats(Zl[o, 0, 0])[:, reg[o] == k].T, (R, 1)) for o in oth])
                Y = np.concatenate([np.concatenate([Zl[o, r, h][:, reg[o] == k].T for r in range(R)]) for o in oth])
                if len(X) == 0:
                    W[k] = None
                    continue
                W[k] = np.linalg.solve(X.T @ X + LAM * len(X) * np.eye(4), X.T @ Y)        # (4, 3)

            def pred(z0, rg):
                P = np.zeros((3, G, G))
                f = feats(z0)
                for k in (0, 1, 2):
                    if W[k] is not None and (rg == k).any():
                        P[:, rg == k] = (f[:, rg == k].T @ W[k]).T
                    elif (rg == k).any():                                                  # class unseen in training
                        P[:, rg == k] = z0[:, rg == k]
                return P
            for o in oth:
                Po = pred(Zl[o, 0, 0], reg[o])
                sh = (anc[b][0] - anc[o][0], anc[b][1] - anc[o][1])
                for r in range(R):
                    resid.append(np.roll(Zl[o, r, h] - Po, sh, axis=(1, 2)))
            ens = (pred(Zt[b, 0, 0], reg[b])[None] + np.stack(resid)).reshape(len(resid), -1)
            out[b, ih] = float(energy_fair(ens, Zt[b, :, h].reshape(R, -1)))
    return out


def res_scores(Xp, Yt, U, anc, hs, n_lab, lam_res=0.05):
    """L(RES(n_lab)) per (state, horizon): the GENERIC residual recipe. LLR(public) as P0, then per region
    class a ridge correction of its block map fitted on n_lab 'Lab episodes' = single true-law futures
    (replicate 0) of n_lab other states under the same program class; ensemble spread from the public fits.
    Nothing about the form of the hidden term is used."""
    NS, R = Yt.shape[:2]
    Zp = (Xp.reshape(NS, R, -1, 3, G, G) / SCB)
    Zt = (Yt.reshape(NS, R, -1, 3, G, G) / SCB)
    reg = [region(U[b]) for b in range(NS)]
    feats = lambda z0: np.concatenate([z0, np.ones_like(z0[:1])], 0)
    out = np.zeros((NS, len(hs)))
    for b in range(NS):
        oth = [o for o in range(NS) if o != b]
        lab = [oth[(b + i) % len(oth)] for i in range(n_lab)]                         # which Lab states: rotates with b
        for ih, h in enumerate(hs):
            W = {}
            for k in (0, 1, 2):
                X = np.concatenate([np.tile(feats(Zp[o, 0, 0])[:, reg[o] == k].T, (R, 1)) for o in oth])
                Y = np.concatenate([np.concatenate([Zp[o, r, h][:, reg[o] == k].T for r in range(R)]) for o in oth])
                if len(X) == 0:
                    W[k] = None
                    continue
                W[k] = np.linalg.solve(X.T @ X + LAM * len(X) * np.eye(4), X.T @ Y)
                Xl = np.concatenate([feats(Zt[o, 0, 0])[:, reg[o] == k].T for o in lab])
                Yl = np.concatenate([Zt[o, 0, h][:, reg[o] == k].T for o in lab])
                if len(Xl):
                    W[k] = W[k] + np.linalg.solve(Xl.T @ Xl + lam_res * len(Xl) * np.eye(4), Xl.T @ (Yl - Xl @ W[k]))

            def pred(z0, rg, Wd):
                P = z0.copy()
                f = feats(z0)
                for k in (0, 1, 2):
                    if Wd[k] is not None and (rg == k).any():
                        P[:, rg == k] = (f[:, rg == k].T @ Wd[k]).T
                return P
            resid = []
            for o in oth:
                Po = pred(Zp[o, 0, 0], reg[o], W)                                      # spread: public futures about the corrected map
                sh = (anc[b][0] - anc[o][0], anc[b][1] - anc[o][1])
                for r in range(R):
                    resid.append(np.roll(Zp[o, r, h] - Po, sh, axis=(1, 2)))
            resid = np.stack(resid)
            resid = resid - resid.mean(0, keepdims=True)                               # the correction moves the mean, not the spread
            ens = (pred(Zt[b, 0, 0], reg[b], W)[None] + resid).reshape(len(resid), -1)
            out[b, ih] = float(energy_fair(ens, Zt[b, :, h].reshape(R, -1)))
    return out


def jack(num, den):
    n = len(num)
    jk = np.array([np.delete(num, b, 0).sum() / np.delete(den, b, 0).sum() for b in range(n)])
    return float(num.sum() / den.sum()), float(np.sqrt((n - 1) / n * ((jk - jk.mean()) ** 2).sum()))


res = {"what": "history-only surrogate LLR (per-block ridge by region class, trained on other states' futures under each law); see surrogate.py docstring",
       "PILOT_NEVER_REUSE_AS_EXAM": True, "ridge": LAM, "rows": []}
files = sorted(glob.glob(os.path.join(SCR, "fut_*.npz")) + glob.glob(os.path.join(SCR, "fut16_*.npz")))
clim = {}
for f in files:
    tag, cand, eta, cls = os.path.basename(f)[:-4].split("_")[:4]
    d = np.load(f)
    Yt, Xp, U, anc = d["Yt"], d["Xp"], d["U"], d["anc"]
    NS, R, T1 = Yt.shape[:3]
    hs = [h for h in (1, 2, 4, 8, 16) if h < T1]
    if "Ya" in d:
        Ya = d["Ya"]
    else:
        fa = os.path.join(SCR, f"fut_{cand}_{eta}_a.npz")
        Ya = np.load(fa)["Yt"]
    Oo = np.array([[float(energy_loo(Yt[b, :, h] / SC1)) for h in hs] for b in range(NS)])
    Pl = np.array([[loo_cross(Xp[b, :, h] / SC1, Yt[b, :, h] / SC1) for h in hs] for b in range(NS)])
    Kk = np.array([[float(energy_fair(np.concatenate([Ya[o, :, h] for o in range(NS) if o != b]) / SC1, Yt[b, :, h] / SC1)) for h in hs]
                   for b in range(NS)])
    Lt, Lp = llr_scores(Yt, Yt, U, anc, hs), llr_scores(Xp, Yt, U, anc, hs)
    share, se = jack(Lp - Lt, Kk - Lt)
    row = {"file": os.path.basename(f), "cand": cand, "eta": float(eta), "program": cls, "horizons": hs, "n_states": int(NS), "R": int(R),
           "share_pooled": share, "share_se_jackknife_states": se,
           "share_per_horizon": ((Lp - Lt).mean(0) / (Kk - Lt).mean(0)).tolist(),
           "skill_LLR_true_vs_O": float((Kk - Lt).sum() / (Kk - Oo).sum()), "skill_LLR_public_vs_O": float((Kk - Lp).sum() / (Kk - Oo).sum()),
           "state_given_screen_pooled": float((Pl - Oo).sum() / (Kk - Oo).sum()),
           "kept_fraction": float((Lp - Lt).sum() / max((Pl - Oo).sum(), 1e-12)) if (Pl - Oo).sum() > 1e-9 else None,
           "L_mean_per_horizon": {"K": Kk.mean(0).tolist(), "O": Oo.mean(0).tolist(), "PLUG": Pl.mean(0).tolist(),
                                  "LLR_true": Lt.mean(0).tolist(), "LLR_public": Lp.mean(0).tolist()}}
    kf = "  n/a" if row["kept_fraction"] is None else f"{row['kept_fraction']:5.2f}"
    print(f"{row['file']:24s} share {share:+.3f} (se {se:.3f}) per h {np.round(row['share_per_horizon'], 3).tolist()}  LLR true {row['skill_LLR_true_vs_O']:.3f} "
          f"public {row['skill_LLR_public_vs_O']:.3f} of O; state-given {row['state_given_screen_pooled']:.3f}; kept {kf}", flush=True)
    if cand in ("XW", "M") and cls != "a":
        row["generic_residual"] = {"what": "RES(n): LLR(public) corrected on n single true-law futures of other states (stand-in for n Lab episodes of this class); closed = (L(LLR public) - L(RES)) / (L(LLR public) - L(LLR true)), LLR true being trained on 25 true-law futures"}
        for n in (1, 2, 3, 5):
            Lr = res_scores(Xp, Yt, U, anc, hs, n)
            cl, cl_se = jack(Lp - Lr, Lp - Lt)
            row["generic_residual"][f"n{n}"] = {"closed_pooled": cl, "closed_se_jackknife_states": cl_se,
                                                "closed_per_horizon": ((Lp - Lr).mean(0) / (Lp - Lt).mean(0)).tolist(),
                                                "share_left": jack(Lr - Lt, Kk - Lt)[0]}
            print(f"      RES({n}): closes {cl:+.2f} (se {cl_se:.2f}) of the gap; per h {np.round(row['generic_residual'][f'n{n}']['closed_per_horizon'], 2).tolist()}; share left {row['generic_residual'][f'n{n}']['share_left']:+.3f}")
    res["rows"].append(row)
json.dump(res, open(os.path.join(HERE, "results", "surrogate.json"), "w"), indent=1)
