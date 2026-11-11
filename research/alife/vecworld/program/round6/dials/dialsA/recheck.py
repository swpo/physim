"""recheck -- study A: the headline numbers once more, in plain numpy without a_stats (seconds).

Reads results/job/scores.npz (axes: eta, truth, seed, half, item, horizon) and recomputes sigma at the zero
point, s and g (point values, picks per truth and seed on half 0, scores on half 1); compares with
results/summary.json [headline]. Writes results/recheck.json.
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
z = np.load(os.path.join(HERE, "results", "job", "scores.npz"))
cl = z["classes"]                                                    # (eta, truth, half, item)
T, S = z["K"].shape[1], z["K"].shape[2]


def L(name, e, half, classes="abcd"):
    """(truth, seed): mean over the items of the classes of the score summed over horizons."""
    a = z[name][e][:, :, half].sum(-1).astype(float)                 # (truth, seed, item)
    out = np.zeros((T, S))
    for t in range(T):
        out[t] = a[t][:, np.isin(cl[e, t, half], list(classes))].mean(-1)
    return out


def pick(a, b, e, classes):
    """Per truth and seed the one of a, b with the lower L on half 0 (all classes); its L on half 1."""
    use_a = L(a, e, 0) <= L(b, e, 0)
    return np.where(use_a, L(a, e, 1, classes), L(b, e, 1, classes))


out = {}
K, C, P0 = L("K", 0, 1), L("Cpub", 0, 1), L("P0", 0, 1)
D = pick("Dnet@32", "Dridge@32", 0, "abcd")
null = D if D.mean() <= P0.mean() else P0
out["sigma_0"] = float((null - C).mean() / (K - C).mean())
for name, cls in (("s_aimed_regional", "cd"), ("g_all", "abcd"), ("g_aimed_regional", "cd")):
    Kc, Pc = L("K", 1, 1, cls), L("P0", 1, 1, cls)
    Cc = pick("Ctrue", "CFT@8", 1, cls)
    G = pick("FT@8", "RES@8", 1, cls)
    out[name] = float((Pc - Cc).mean() / (Kc - Cc).mean()) if name.startswith("s") else float((Pc - G).mean() / (Pc - Cc).mean())
d = (L("P0", 1, 1) - pick("FT@8", "RES@8", 1, "abcd")) - 0.7 * (L("P0", 1, 1) - pick("Ctrue", "CFT@8", 1, "abcd"))
dt = d.mean(1)
se = float(np.sqrt(dt.var(ddof=1) / T + d.mean(0).var(ddof=1) / S))
out["g_contrast_mean_se_upper90"] = [float(dt.mean()), se, float(dt.mean() + 1.415 * se)]
h = json.load(open(os.path.join(HERE, "results", "summary.json")))["headline"]
ref = {"sigma_0": h["sigma_0"]["value"], "s_aimed_regional": h["s"]["value"], "g_all": h["g"]["value"],
       "g_aimed_regional": h["g_secondary_aimed_regional"]["value"],
       "g_contrast_mean_se_upper90": [h["g"]["contrast_d_mean_lower_upper"][0], None, h["g"]["contrast_d_mean_lower_upper"][2]]}
diff = max(abs(out[k] - ref[k]) for k in ("sigma_0", "s_aimed_regional", "g_all", "g_aimed_regional"))
diff = max(diff, abs(out["g_contrast_mean_se_upper90"][0] - ref["g_contrast_mean_se_upper90"][0]),
           abs(out["g_contrast_mean_se_upper90"][2] - ref["g_contrast_mean_se_upper90"][2]))
res = {"what": "plain-numpy recomputation of the headline from results/job/scores.npz (job r6-dialsa-003)",
       "PILOT_NEVER_REUSE_AS_EXAM": True, "recomputed": out, "summary_headline": ref, "max_abs_difference": diff,
       "agrees": bool(diff < 1e-3)}
json.dump(res, open(os.path.join(HERE, "results", "recheck.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
