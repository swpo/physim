"""Figures and results.json for the Hash Chemistry O calibration.
usage: python make_figs.py RUNDIR  (RUNDIR holds short/ and long/ from simulate.py)"""
import sys, os, json, glob, gzip
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import o_measure as om

RD = sys.argv[1]; HERE = os.path.dirname(os.path.abspath(__file__))
C = {"m0_lo0.0": ("C0", "hash (consistent)"), "m1_lo0.2": ("C3", "random f~U[0.2,1]"), "m2_lo0.0": ("C2", "additive (singleton hash mean)"), "m1_lo0.0": ("C7", "random f~U[0,1]")}
res = {}

def load(p):
    return {k: v for k, v in np.load(p).items()}

def analyse(sub, T, win, Lc):
    out = {}
    for p in sorted(glob.glob(f"{RD}/{sub}/*.npz")):
        tag = os.path.basename(p)[:-4]; L = load(p)
        if L["pop"][-1] == 0:
            out[tag] = dict(extinct_at=int(np.argmax(L["pop"] == 0)), reps=int(len(L["rep_t"]))); continue
        S = L | {}; sh = om.shadow(L, seed=1)
        sh["mut_n"] = L["mut_n"]
        a = om.stats(L, T, win=win, Lc=Lc); b = om.stats(sh | {"mut_n": L["mut_n"]}, T, win=win, Lc=Lc)
        out[tag] = dict(real=a, shadow=b, pop=L["pop"])
        print(sub, tag, "unique", a["cum_unique"][-1], "shadow", b["cum_unique"][-1], "cohort", a["cohort_new"].tolist()[:8], "sh", b["cohort_new"].tolist()[:8], flush=True)
    return out

short = analyse("short", 2000, 200, 1000)
long_ = analyse("long", 20000, 1000, 1000)

def j(x):
    if isinstance(x, np.ndarray): return x.tolist()
    if isinstance(x, (np.integer,)): return int(x)
    if isinstance(x, (np.floating,)): return float(x)
    return x

summary = {}
for name, D_, T in (("short", short, 2000), ("long", long_, 20000)):
    for tag, d in D_.items():
        if "extinct_at" in d:
            summary[f"{name}/{tag}"] = d; continue
        r, s = d["real"], d["shadow"]
        summary[f"{name}/{tag}"] = dict(unique_k2=int(r["cum_unique"][-1]), shadow_unique_k2=int(s["cum_unique"][-1]),
            cohort_new=j(r["cohort_new"]), shadow_cohort_new=j(s["cohort_new"]), bedau_new=j(r["bedau_new"]), shadow_bedau_new=j(s["bedau_new"]),
            median_age_at_crossing=r["age_at_cross"], top20_overlap_with_first_window=[round(v, 2) for v in r["top_overlap_first"]],
            mean_size=[round(float(v), 2) for v in r["mean_size"]], pop_end=int(d["pop"][-1]))

# ---- figure 1: 2000-step calibration
fig, ax = plt.subplots(1, 4, figsize=(20, 4.6))
for tag, d in short.items():
    key = tag.rsplit("_s", 1)[0]; c = C[key][0]
    if "extinct_at" in d:
        continue
    r, s = d["real"], d["shadow"]; tb = np.arange(len(r["cohort_new"])) * 200 + 100
    ax[0].plot(r["cum_unique"], c=c); ax[0].plot(s["cum_unique"], c=c, ls=":", lw=1)
    ax[1].plot(tb, np.cumsum(r["bedau_new"]), c=c); ax[1].plot(tb, np.cumsum(s["bedau_new"]), c=c, ls=":", lw=1)
    ax[2].plot(tb, r["cohort_new"], c=c, marker="o", ms=3); ax[2].plot(tb, s["cohort_new"], c=c, ls=":", lw=1)
    ax[3].plot(tb, r["mean_size"], c=c)
for k, (c, l) in C.items(): ax[0].plot([], [], c=c, label=l)
ax[0].plot([], [], c="k", ls=":", label="RB neutral shadow of each run"); ax[0].legend(fontsize=8)
ax[0].set_title("raw novelty: distinct replicated multisets (k>=2)\nhash is LOWEST (Sayama: about 1/3 of the biased control)")
ax[1].set_title("Bedau new activity: components reaching a*=50\n(cumulative)")
ax[2].set_title("cohort new activity: components born in a 200-step\nwindow that reach a*=50 within 1000 steps")
ax[3].set_title("mean size of replicated multisets")
for a in ax: a.set_xlabel("step")
plt.tight_layout(); plt.savefig(f"{HERE}/o_calibration_2000.png", dpi=72); plt.close()

# ---- figure 2: 20000-step runs
fig, ax = plt.subplots(1, 4, figsize=(20, 4.6))
for tag, d in long_.items():
    key = tag.rsplit("_s", 1)[0]; c = C[key][0]
    if "extinct_at" in d:
        continue
    r, s = d["real"], d["shadow"]; tb = np.arange(len(r["cohort_new"])) * 1000 + 500
    ax[0].plot(tb, np.cumsum(r["bedau_new"]), c=c); ax[0].plot(tb, np.cumsum(s["bedau_new"]), c=c, ls=":", lw=1)
    ax[1].plot(tb, r["cohort_new"], c=c, marker="o", ms=3); ax[1].plot(tb, s["cohort_new"], c=c, ls=":", lw=1)
    ax[2].plot(tb, r["top_overlap_first"], c=c)
    ax[3].plot(tb, [a if a is not None else np.nan for a in r["age_at_cross"]], c=c)
ax[0].set_title("Bedau new activity (a*=50), 20000 steps: keeps rising\nsolid real, dotted RB shadow; blue hash x9, red random x3")
ax[1].set_title("cohort new activity per 1000-step birth window\n(born there, reach a*=50 within 1000 steps)"); ax[1].set_yscale("symlog")
ax[2].set_title("share of the window's top-20 multisets that were\nalready top-20 in steps 0-1000 (replacement test)")
ax[3].set_title("median age of components when they cross a*\n(late Bedau 'new activity' = old components)")
for a in ax: a.set_xlabel("step")
plt.tight_layout(); plt.savefig(f"{HERE}/o_long_20000.png", dpi=72); plt.close()

# ---- figure 3: evoloop census (c16) with the same cohort/replacement measure and a census shadow
EV = os.path.join(HERE, "..", "20261025T1457-c16-evoloop-not-open-ended", "census")
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2)); ev = {}
for s_, c in ((1, "C0"), (2, "C1"), (3, "C2")):
    d = json.load(gzip.open(f"{EV}/geno_s{s_}.json.gz"))
    rows = [c_["full"] for c_ in d["census"]]; t = np.array([c_["t"] for c_ in d["census"]])
    win = 25
    r = om.census_stats(rows, 200, 25, win)
    shs = [om.census_stats(om.census_shadow(rows, q), 200, 25, win)["cohort_new"] for q in range(20)]
    tb = (np.arange(len(r["cohort_new"])) + 0.5) * win * 2000
    ax[0].plot(tb, r["cohort_new"], c=c, marker="o", label=f"seed {s_}"); ax[0].plot(tb, np.mean(shs, 0), c=c, ls=":")
    ax[0].fill_between(tb, np.percentile(shs, 5, 0), np.percentile(shs, 95, 0), color=c, alpha=0.12)
    ax[1].plot(tb, r["top_overlap_first"], c=c, marker="o")
    ev[f"s{s_}"] = dict(cohort_new=j(r["cohort_new"]), shadow_mean=j(np.mean(shs, 0)), shadow_p95=j(np.percentile(shs, 95, 0)),
                        top5_overlap_first=r["top_overlap_first"], top5_overlap_prev=r["top_overlap_prev"], genotypes=r["n_components"])
ax[0].set_title("evoloop (c16 census): genotypes born per 50k-step window\nreaching 200 loop-censuses within 50k steps; dotted/band = census shadow")
ax[0].legend(); ax[1].set_title("evoloop: top-5 genotypes overlap with first window")
for a in ax: a.set_xlabel("step")
plt.tight_layout(); plt.savefig(f"{HERE}/o_evoloop.png", dpi=72); plt.close()
summary["evoloop_census"] = ev
json.dump(summary, open(f"{HERE}/results.json", "w"), indent=1, default=j)
print("written")
