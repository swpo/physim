"""Independent recompute of the sbi OES numbers from r4-sbi-002 scores.npz (own code, not vw.scoring):
item bootstrap, two-stage truth-cluster bootstrap and truth-level t for each paired gap.
usage: python -B recheck_oes.py [job_dir] > results/recheck_oes.json"""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
JOB = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "sbi", "results", "job")
z = np.load(os.path.join(JOB, "scores.npz"))
T = sorted({int(k.split("|")[0][1:]) for k in z.files})
names = sorted({k.split("|", 1)[1] for k in z.files if k.startswith("t0|")} - {"classes"})
S = {k: np.stack([z[f"t{i}|{k}"] for i in T]) for k in names}       # (8, 64, 7)
nT, nI, nC = S["oracle"].shape
assert not any(np.isnan(v).any() for v in S.values()), "nan"


def oes_from(means):                       # means: name -> (..., c)
    den = means["climatology"] - means["oracle"]
    return {k: ((means["climatology"] - means[k]) / den).mean(-1) for k in means}


# validity: denominator significant (clim - oracle > 3 se, own estimate)
d = (S["climatology"] - S["oracle"]).reshape(-1, nC)
zc = d.mean(0) / (d.std(0, ddof=1) / np.sqrt(len(d)))
pt = oes_from({k: v.reshape(-1, nC).mean(0) for k, v in S.items()})
rng = np.random.default_rng(12345)
B = 4000
# (1) item bootstrap over the pooled 512 items (as the study)
idx = rng.integers(0, nT * nI, (B, nT * nI))
bi = oes_from({k: v.reshape(-1, nC)[idx].mean(1) for k, v in S.items()})
# (2) two-stage cluster bootstrap: resample truths, then items within each
ti = rng.integers(0, nT, (B, nT))
ii = rng.integers(0, nI, (B, nT, nI))
bc = oes_from({k: v[ti[:, :, None], ii].reshape(B, -1, nC).mean(1) for k, v in S.items()})
# per-truth OES
per = {k: np.array([oes_from({kk: vv[i].mean(0) for kk, vv in S.items()})[k] for i in range(nT)]) for k in names}


def gap(a, b):
    g = pt[a] - pt[b]
    se_i = (bi[a] - bi[b]).std(ddof=1)
    se_c = (bc[a] - bc[b]).std(ddof=1)
    dt = per[a] - per[b]
    se_t = dt.std(ddof=1) / np.sqrt(nT)
    return {"gap": round(float(g), 4), "z_items": round(float(g / se_i), 2), "z_cluster": round(float(g / se_c), 2),
            "truth_mean": round(float(dt.mean()), 4), "t_truths": round(float(dt.mean() / se_t), 2),
            "n_truths_pos": int((dt > 0).sum())}


out = {"cells_z_den": np.round(zc, 1).tolist(), "oes": {k: round(float(pt[k]), 4) for k in names},
       "se_items": {k: round(float(bi[k].std(ddof=1)), 4) for k in names}, "gaps": {}}
pairs = []
for cl in ("net", "ridge"):
    for n in (2, 8, 32, 128, 512):
        pairs += [(f"{cl}|post@{n}", f"{cl}|real@{n}"), (f"{cl}|true", f"{cl}|post@{n}")]
    pairs += [(f"{cl}|true", f"{cl}|prior_pred"), (f"{cl}|true", f"{cl}|prior_mean"),
              (f"{cl}|prior_pred", f"{cl}|prior_mean"), (f"{cl}|real@512", f"{cl}|prior_pred")]
pairs += [("amort|true", "amort|prior_pred"), ("amort|true", "amort|prior_mean"), ("amort|prior_pred", "amort|prior_mean"),
          ("amort|true", "net|true")] + [(f"amort|post@{n}", f"net|post@{n}") for n in (2, 8, 32, 128, 512)]
pairs += [("net|post@2", "net|real@512"), ("ridge|real@32", "net|real@128"), ("net|prior_pred", "net|real@128"),
          ("ridge|real@128", "net|real@128"), ("ridge|real@512", "ridge|prior_pred")]
for a, b in pairs:
    out["gaps"][f"{a} - {b}"] = gap(a, b)
out["per_truth"] = {k: np.round(per[k], 3).tolist() for k in ("net|true", "net|prior_mean", "net|prior_pred",
                                                             "ridge|true", "ridge|post@2", "amort|true")}
# best-of-class envelope per budget
env = {}
for n in (2, 8, 32, 128, 512):
    env[n] = {"best_real": max(pt[f"net|real@{n}"], pt[f"ridge|real@{n}"]),
              "best_post": max(pt[f"net|post@{n}"], pt[f"ridge|post@{n}"], pt[f"amort|post@{n}"])}
out["envelope"] = {n: {k: round(float(v), 4) for k, v in e.items()} for n, e in env.items()}
print(json.dumps(out, indent=1))
