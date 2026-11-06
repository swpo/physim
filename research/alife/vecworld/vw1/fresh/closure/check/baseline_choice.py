"""Checker: which linear baseline (AR(1) or ridge_p2) the residual nets sit on, per horizon, at each
learning-curve fraction (coarse). Same code path as closure_lib.make_patch_extra."""
import json, sys
import numpy as np
sys.path.insert(0, "/home/user/evalwork/vecworld/vw1/fresh/closure/scripts")
import closure_lib as CL
AN = CL.AN
AN.HORIZONS = [1, 2, 4, 8, 16, 32]
D, cat, metas = CL.load_data()
out = {}
for phi in ("coarse", "objects"):
    Y0 = D["Yc"] if phi == "coarse" else D["Yo"]
    allY = np.concatenate(Y0); sd = allY.std(0); eff = sd > 1e-6 * max(sd.max(), 1e-12); sd = np.where(eff, sd, 1.0)
    Ys = [Y[:, eff] / sd[eff] for Y in Y0]
    J = len(Ys)
    for fr in (0.25, 0.5, 1.0):
        ch = []
        for f in range(4):
            tr_j = [jj for jj in range(J) if jj % 4 != f]
            va_j = [jj for jj in tr_j if jj % 4 == (f + 1) % 4]
            fit_all = [jj for jj in tr_j if jj not in va_j]
            fit_j = fit_all[:max(1, int(round(fr * len(fit_all))))]
            mu = np.concatenate([Ys[jj] for jj in fit_j]).mean(0)
            _, ev = CL.linear_baselines(Ys, fit_j, va_j, 32, mu)
            ch.append(["ar1" if a <= b else "ridge_p2" for a, b in zip(ev["ar1"], ev["ridge_p2"])])
        out[f"{phi}_{fr}"] = ch
        print(phi, fr, ch, flush=True)
json.dump(out, open("/home/user/evalwork/vecworld/vw1/fresh/closure/check/baseline_choice.json", "w"), indent=1)
