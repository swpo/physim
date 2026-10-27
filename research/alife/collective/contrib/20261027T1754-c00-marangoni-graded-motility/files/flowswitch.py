"""Window-free check of part (c): per-rod body-mean FLOW speed at every frame (2.5 t, no smoothing), split-born rods.
Correlation time (1/e of the within-rod ACF about each rod's own mean, linear interpolation), level-crossing rate of
fixed two-threshold calls (thresholds = 40th / 60th percentiles of the noise-free arm, in own lengths per t and in px per t),
and the Rice-formula expectation for a smooth Gaussian process is NOT assumed: we just report the scaling with eps.
usage: flowswitch.py OUT.json eps=path,path ..."""
import sys, json
sys.path.insert(0, "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/paperexp/marangoni-bistability")
import numpy as np, states as S
FT = 2.5; MIN = 13
arms = [(a.split("=")[0], a.split("=")[1].split(",")) for a in sys.argv[2:]]
def series(paths):
    out = []
    for p in paths:
        d = json.load(open(p))
        for t in d["tracks"]:
            if t["birth"] != "split" or t["n"] < MIN: continue
            U = np.array(t["U"]); L = np.median(t["L4"]); u = np.hypot(U[:, 0], U[:, 1])
            out.append(dict(px=u, L=u / L))
    return out
def tau(xs):
    num = np.zeros(41); den = np.zeros(41)
    for x in xs:
        xo = x - x.mean(); v = xo.var()
        for lag in range(min(41, len(x))):
            num[lag] += (xo[:len(x) - lag] * xo[lag:]).sum(); den[lag] += (len(x) - lag) * v
    a = num / np.maximum(den, 1e-30); i = np.argmax(a < np.exp(-1))
    return float(FT * (i - 1 + (a[i - 1] - np.exp(-1)) / (a[i - 1] - a[i]))), a[:9].round(3).tolist()
base = series(arms[0][1])
th = {k: (np.quantile(np.concatenate([s[k] for s in base]), .4), np.quantile(np.concatenate([s[k] for s in base]), .6)) for k in ("px", "L")}
res = {}
for eps, paths in arms:
    ss = series(paths); r = {"rods": len(ss)}
    for k in ("px", "L"):
        tt, acf = tau([s[k] for s in ss])
        ns = 0; T = 0
        for s in ss:
            st = S.schmitt(s[k], *th[k]); ns += int(np.abs(np.diff(st)).sum()); T += len(s[k]) * FT
        r[k] = dict(tau=tt, acf=acf, switches_per_100t=100 * ns / T, median=float(np.median(np.concatenate([s[k] for s in ss]))),
                    bc=float(S.bimod_coef(np.log10(np.maximum(np.concatenate([s[k] for s in ss]), 1e-5)))))
    res[eps] = r; print(eps, json.dumps(r))
json.dump(dict(thresholds={k: list(map(float, v)) for k, v in th.items()}, arms=res), open(sys.argv[1], "w"), indent=1)
