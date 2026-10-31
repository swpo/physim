"""Extra scoring variants on the saved detect ensembles: (a) the global sensor with each (time, feature) standardised by the
native ensemble's sd at that time; (b) single global features (variance of c, of s, of |v| components, of phi).
Ratio = ES(native forecast | ablation truth) / ES(native forecast | native truth), averaged over the 8 truth members."""
import json, sys
import numpy as np
sys.path.insert(0, ".")
from apparatus import energy_score, OUT, OBS
pre = "det_s0_phys0.01_w150_"
E = {a: np.load(OUT / f"{pre}{a}.npz")["R"] for a in ["native", "truth", "kappa0", "mar0", "passive"]}
nat = E["native"]; nobs = len(OBS); G = nat.shape[-1] - 2 * nobs
res = {}
def ratio(sel, nt, pertime):
    X = {a: E[a][:, :nt][:, :, sel] for a in E}
    sc = X["native"].std(axis=0, keepdims=True) + 1e-9 if pertime else X["native"].reshape(-1, X["native"].shape[-1]).std(0) + 1e-9
    Fz = (X["native"] / sc).reshape(8, -1)
    base = np.mean([energy_score(Fz, y) for y in (X["truth"] / sc).reshape(8, -1)])
    return {a: round(float(np.mean([energy_score(Fz, y) for y in (X[a] / sc).reshape(8, -1)]) / base), 2) for a in ("kappa0", "mar0", "passive")}
for w in (15, 50, 150):
    nt = int(round(w / 2))
    res[f"global_pertime_scale|w{w}"] = ratio(slice(G, None), nt, True)
    res[f"global_pooled_scale|w{w}"] = ratio(slice(G, None), nt, False)
    for f in ("phi", "s", "c", "vx"):
        i = G + nobs + OBS.index(f)
        res[f"var_{f}_only|w{w}"] = ratio([i], nt, False)
for k, v in res.items():
    print(k, v)
json.dump(res, open(OUT / "score_extra_s0_phys0.01_w150.json", "w"), indent=1)
