"""offline_calib -- CPU check of the synthetic likelihood's calibration on held-out design points.

From the job's design summaries (results/job/design_features.npz: N box draws x K episodes): refit the
projection and the emulator on 80% of the theta points, then for each held-out theta compute the
posterior from its own first n episodes (n = 1, 2, K) under the flat box prior (held-out points are
uniform on the box, so this prior is the right one for a coverage check), and record the marginal
PITs and the HPD level of the truth. Many more truths than the 8 of the job, but only small n.
usage: python -B offline_calib.py [job_dir] [n_test] -> results/offline_calib.json
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sbi_lib as SL  # noqa: E402

JOB = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "results", "job")
NT = int(sys.argv[2]) if len(sys.argv) > 2 else 300
OUTF = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, "results", "offline_calib.json")
z = np.load(os.path.join(JOB, "design_features.npz"))
U, F = z["u"].astype(float), z["F"].astype(float)
N, K, nf = F.shape
rng = np.random.default_rng(0)
perm = rng.permutation(N)
te, tr = perm[:max(2, N // 5)][:NT], perm[max(2, N // 5):]
proj = SL.Projection().fit(F[tr].reshape(-1, nf), np.repeat(U[tr], K, 0))
em = SL.Emulator().fit(U[tr], proj(F[tr].reshape(-1, nf)).reshape(len(tr), K, -1))


class Flat:
    def logp(self, u):
        return np.zeros(len(np.atleast_2d(u)))


out = {"N_train_theta": int(len(tr)), "N_test_theta": int(len(te)), "K": int(K), "emulator": em.diag,
       "projection_r2": proj.r2, "per_n": {}}
for n in sorted({1, 2, K}):
    pits, hpd, sd = [], [], []
    for j in te:
        sbar = proj(F[j, :n]).mean(0)
        post = SL.posterior(em, Flat(), sbar, n, rng, M=20000, target=1000)
        c = SL.posterior_checks(post, em, Flat(), sbar, n, U[j])
        pits.append(c["pit"])
        hpd.append(c["hpd_level"])
        sd.append(post["sd_u"])
    pits, hpd = np.array(pits), np.array(hpd)
    out["per_n"][str(n)] = {"in50": float(((pits > 0.25) & (pits < 0.75)).mean()),
                            "in90": float(((pits > 0.05) & (pits < 0.95)).mean()),
                            "in50_per_param": ((pits > 0.25) & (pits < 0.75)).mean(0).tolist(),
                            "in90_per_param": ((pits > 0.05) & (pits < 0.95)).mean(0).tolist(),
                            "hpd_le_50": float((hpd <= 0.5).mean()), "hpd_le_90": float((hpd <= 0.9).mean()),
                            "post_sd_over_flat_prior_sd_mean": (np.mean(sd, 0) / (1 / np.sqrt(3))).tolist()}
    print(n, out["per_n"][str(n)], flush=True)
json.dump(out, open(OUTF, "w"), indent=1)
