"""Reviewer's own energy score (V-statistic, RMS over coordinates / frozen scale) from the cached ensembles."""
import json, numpy as np
S = "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/cips_runner/out/suite"
suite = json.load(open(f"{S}/suite.json")); sc = suite["calibration"]["scales"]
TIMES = [0, 2, 5, 8, 10, 12, 15, 20, 22, 25, 30, 35, 40, 45, 50]
ST = [2, 5, 8, 10, 12, 15, 20, 25, 30, 35, 40, 45, 50]
SEN = ("device0", "device1", "global"); FL = ("e", "p", "F", "s")
L = lambda p: (lambda z: [z[f"query{i}"] for i in range(3)])(np.load(p))
def es(X, Y):
    d = X.shape[1]
    r = lambda A, B: np.sqrt(((A[:, None] - B[None]) ** 2).sum(-1) / d).mean()
    return r(X, Y) - 0.5 * r(X, X)
def score(pred, tru, W):
    ti = [TIMES.index(t) for t in ST if t <= W]; out = {}
    for qi, s in enumerate(SEN):
        for p, f in enumerate(FL):
            if s == "global":
                X = np.concatenate([pred[qi][:, ti, p, k] / sc[f"global/{f}/{n}"]["scale"] for k, n in ((0, "mean"), (1, "variance"))], 1)
                Y = np.concatenate([tru[qi][:, ti, p, k] / sc[f"global/{f}/{n}"]["scale"] for k, n in ((0, "mean"), (1, "variance"))], 1)
            else:
                X = pred[qi][:, ti, p, :].reshape(len(pred[qi]), -1) / sc[f"{s}/{f}"]["scale"]
                Y = tru[qi][:, ti, p, :].reshape(len(tru[qi]), -1) / sc[f"{s}/{f}"]["scale"]
            out[f"{s}/{f}"] = es(X, Y)
    return out
res = {}
for cid in ("c001", "c002"):
    tru = L(f"{S}/truth/{cid}.npz")
    for W in (10, 50):
        ref = score(L(f"{S}/controls/{cid}/independent_native.npz"), tru, W)
        for n in ("numerical_null", "ablate_kF0", "ablate_d0", "band_native"):
            g = score(L(f"{S}/controls/{cid}/{n}.npz"), tru, W)
            agg = np.mean(list(g.values())) / np.mean(list(ref.values()))
            d0 = np.mean([g[k] for k in g if k.startswith("device0")]) / np.mean([ref[k] for k in ref if k.startswith("device0")])
            res[f"{cid}/{W}tu/{n}"] = (round(float(agg), 2), round(float(d0), 2))
        res[f"{cid}/{W}tu/independent_native_raw"] = round(float(np.mean(list(ref.values()))), 4)
print(json.dumps(res, indent=0))
