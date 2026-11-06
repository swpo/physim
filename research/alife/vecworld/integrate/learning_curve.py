"""Learning curve of the best learned level-1 predictor (ridge, p=2) on A_gliders: test error at each
horizon when trained on 1/4, 1/2 and all of the training trajectories (same folds as analyze.py)."""
import json, sys
import numpy as np
import analyze as AN

name = sys.argv[1] if len(sys.argv) > 1 else "A_gliders"
D = AN.load(name)
out = {}
for phi in ("coarse", "objects"):
    Ys = D["Yo"] if phi == "objects" else D["Yc"]
    Bs = D["Bo"] if phi == "objects" else D["Bc"]
    allY = np.concatenate(Ys); sd = allY.std(0); eff = sd > 1e-6 * sd.max(); sd = np.where(eff, sd, 1)
    Ys = [Y[:, eff] / sd[eff] for Y in Ys]; Bs = [B[..., eff] / sd[eff] for B in Bs]
    J = len(Ys); tmax = 32; nH = len(AN.HORIZONS)
    res = {}
    for frac in (0.25, 0.5, 1.0):
        errs = []
        for f in range(AN.NFOLD):
            tr = [jj for jj in range(J) if D["j"][jj] % AN.NFOLD != f]
            va = [jj for jj in tr if D["j"][jj] % AN.NFOLD == (f + 1) % AN.NFOLD]
            fit = [jj for jj in tr if jj not in va]
            n_use = max(1, int(round(frac * len(fit))))
            fit = fit[:n_use]
            Xf, Ff, Y0f = AN.multi_pairs([Ys[jj] for jj in fit], 2, tmax)
            Xv, Fv, Y0v = AN.multi_pairs([Ys[jj] for jj in va], 2, tmax)
            rg = AN.Ridge().fit(Xf, [Ff[h] - Y0f for h in range(nH)], Xv, [Fv[h] - Y0v for h in range(nH)])
            for jj in range(J):
                if D["j"][jj] % AN.NFOLD != f:
                    continue
                for i, t in enumerate(D["st_tick"][jj]):
                    t = int(t); x = AN.lag_matrix(Ys[jj], np.array([t]), 2)
                    e = []
                    for hi, h in enumerate(AN.HORIZONS):
                        pred = Ys[jj][t] + rg.predict(x, hi)[0]
                        fut = np.concatenate([Ys[jj][t + h][None], Bs[jj][i, :, h - 1]])
                        e.append(((fut - pred) ** 2).sum(1).mean() / eff.sum())
                    errs.append(e)
        res[f"train_traj_per_fold={int(round(frac * 12))}"] = np.mean(errs, 0).round(4).tolist()
    out[phi] = res
    print(phi, res)
json.dump(out, open(f"results/{name}_learning_curve.json", "w"), indent=1)
