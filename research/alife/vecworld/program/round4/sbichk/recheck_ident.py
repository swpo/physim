"""Recompute the sbi identification table from the job's saved features (design + Lab) on CPU, and a direct
sim-vs-Lab consistency check (Lab summaries at the true theta vs the emulator built on the agent's simulator).
usage: python -B recheck_ident.py [sbi_dir] [job_dir] > results/recheck_ident.json (about 1 CPU-minute)"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SBI = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "sbi")
JOB = sys.argv[2] if len(sys.argv) > 2 else os.path.join(SBI, "results", "job")
sys.path.insert(0, SBI)
import sbi_lib as SL  # noqa: E402

d = np.load(os.path.join(JOB, "design_features.npz"))
Ud, Fd = d["u"].astype(float), d["F"].astype(float)
N, K, nf = Fd.shape
lab = np.load(os.path.join(JOB, "lab_features.npz"))
FL = lab["F"].astype(float)                                   # (8, 512, nf)
truths = np.array(json.load(open(os.path.join(JOB, "truths.json")))["truths"])
pvj = json.load(open(os.path.join(JOB, "viability_prior.json")))
pv = SL.ViabilityPrior()
pv.w = np.array(pvj["w"])

proj = SL.Projection().fit(Fd.reshape(N * K, nf), np.repeat(Ud, K, 0))
S = proj(Fd.reshape(N * K, nf)).reshape(N, K, -1)
em = SL.Emulator().fit(Ud, S)
rng = np.random.default_rng(4403)
ub = rng.uniform(-1, 1, (200_000, 4))
wb = np.exp(pv.logp(ub))
wb /= wb.sum()
pm = wb @ ub
psd = np.sqrt(wb @ (ub - pm) ** 2)
budgets = [2, 8, 32, 128, 512]
res = {n: [] for n in budgets}
chi = {n: [] for n in budgets}
for i, th in enumerate(truths):
    ut = SL.to_u(th)
    for n in budgets:
        sbar = proj(FL[i, :n]).mean(0)
        post = SL.posterior(em, pv, sbar, n, rng)
        c = SL.posterior_checks(post, em, pv, sbar, n, ut)
        res[n].append({"ratio": post["sd_u"] / psd, "in50": c["in50"], "in90": c["in90"], "hpd": c["hpd_level"]})
        # standardised residual of the Lab mean summary at the true theta (emulator mean, full likelihood cov)
        mu = em.mean(ut[None])[0]
        Sfull = em.cov(ut[None])[0] / n + em.emu_var(ut[None])[0] * em.Sig_mean + em.Bm
        Sdata = em.cov(ut[None])[0] / n
        r = sbar - mu
        chi[n].append([float(r @ np.linalg.solve(Sfull, r)), float(r @ np.linalg.solve(Sdata, r))])
out = {"emulator": em.diag, "projection_r2": proj.r2, "prior_sd_theta": (psd * SL.HW_).tolist(), "per_budget": {}}
for n in budgets:
    rr = res[n]
    out["per_budget"][n] = {
        "ratio_mean": np.round(np.mean([r["ratio"] for r in rr], 0), 3).tolist(),
        "in50": float(np.mean([r["in50"] for r in rr])), "in90": float(np.mean([r["in90"] for r in rr])),
        "hpd_le_90": int(sum(r["hpd"] <= 0.9 for r in rr)), "hpd": np.round([r["hpd"] for r in rr], 3).tolist(),
        "chi2_full_per_truth": np.round([c[0] for c in chi[n]], 2).tolist(),
        "chi2_full_mean": round(float(np.mean([c[0] for c in chi[n]])), 2),
        "chi2_dataonly_mean": round(float(np.mean([c[1] for c in chi[n]])), 2)}
# shrink factor 128 -> 512 per parameter
a, b = np.array(out["per_budget"][128]["ratio_mean"]), np.array(out["per_budget"][512]["ratio_mean"])
out["sd_shrink_128_to_512"] = np.round(b / a, 3).tolist()
# misfit floor: posterior sd / prior sd when n -> infinity is set by emu_var*Sig_mean + Bm (no data term)
print(json.dumps(out, indent=1))
