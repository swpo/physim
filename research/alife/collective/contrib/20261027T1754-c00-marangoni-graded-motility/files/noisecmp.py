"""Part (c): rods' state statistics against surfactant noise strength eps, with thresholds fixed from the noise-free arm.
usage: noisecmp.py OUT.json OUT.png LO HI THR  eps=path1,path2 [eps=path1,path2 ...]
Per arm (seeds pooled; per seed in brackets): rods, swimming fraction (rod-frames with speed > THR own lengths/t),
two-threshold switches per rod per 100 t, mean complete dwell in each state, within-rod speed autocorrelation time,
dividing tracks, median D, D >= 3 count, mother-daughter D (both dividing) and parent D vs daughter mean speed."""
import sys, json
import numpy as np
from scipy import stats
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/paperexp/marangoni-bistability")
import states as S

oj, op, LO, HI, THR = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
arms = [(float(a.split("=")[0]), a.split("=")[1].split(",")) for a in sys.argv[6:]]
FT = 2.5
rng = np.random.default_rng(1)


def boot_r(x, y, nb=2000):
    x, y = np.asarray(x), np.asarray(y)
    if len(x) < 4: return np.nan, (np.nan, np.nan)
    r = stats.pearsonr(x, y)[0]; bs = []
    for _ in range(nb):
        i = rng.integers(0, len(x), len(x))
        if np.std(x[i]) > 0 and np.std(y[i]) > 0: bs.append(np.corrcoef(x[i], y[i])[0, 1])
    return float(r), (float(np.quantile(bs, .025)), float(np.quantile(bs, .975)))


def arm_stats(paths):
    R, trk = S.load(paths)
    o = {}
    o["rods"] = len(trk); o["rodframes"] = int(len(R["spL"]))
    o["frac_swim"] = float(np.mean(R["spL"] > THR))
    o["frac_swim_per_seed"] = [float(np.mean(R["spL"][R["run"] == i] > THR)) for i in range(len(paths))]
    o["median_spL"] = float(np.median(R["spL"])); o["median_sp_px"] = float(np.median(R["sp"])); o["q90_sp_px"] = float(np.quantile(R["sp"], .9))
    o["median_Lm"] = float(np.median([t["Lm"] for t in trk])); o["frac_swim_px"] = float(np.mean(R["sp"] > THR * 13.7))
    pr = np.log10([max(np.mean(t["spL"]), 1e-4) for t in trk]); o["bc_perrod"] = float(S.bimod_coef(pr))
    o["bc_inst"] = float(S.bimod_coef(np.log10(np.maximum(R["spL"], 1e-4))))
    o["kde_modes_inst"] = len(S.kde_modes(np.log10(np.maximum(R["spL"], 1e-4)), np.linspace(-3, 0, 301))[1])
    tid = R["tid"].astype(int); ls = np.log10(np.maximum(R["spL"], 1e-4)); gm = np.bincount(tid, ls) / np.maximum(np.bincount(tid), 1)
    o["share_between_rods"] = float(np.var(gm[tid]) / np.var(ls))
    comp, cens, nsw, ttot, never, nrod = S.dwells(trk, "spL", LO, HI, FT)
    o["switches_per_rod_100t"] = 100 * nsw / ttot
    o["switches_per_seed"] = []
    for i in range(len(paths)):
        _, _, n_, t_, _, _ = S.dwells([t for t in trk if t["run"] == i], "spL", LO, HI, FT)
        o["switches_per_seed"].append(100 * n_ / t_)
    o["dwell_rest_mean"] = float(np.mean(comp[0])) if comp[0] else None
    o["dwell_swim_mean"] = float(np.mean(comp[1])) if comp[1] else None
    o["dwell_n"] = [len(comp[0]), len(comp[1])]
    o["dwell_cv"] = [float(np.std(comp[k]) / np.mean(comp[k])) if len(comp[k]) > 3 else None for k in (0, 1)]
    pac, oac, nac = S.acf_within(trk)
    o["tau_own"] = float(FT * (np.argmax(oac < np.exp(-1)) if (oac < np.exp(-1)).any() else len(oac)))
    o["tau_pooled"] = float(FT * (np.argmax(pac < np.exp(-1)) if (pac < np.exp(-1)).any() else len(pac)))
    # dividing tracks: D over the WHOLE track (need all frames: recompute from rods.json)
    divD, pairs, pv = [], [], []
    for i, p in enumerate(paths):
        d = json.load(open(p)); tb = {t["id"]: t for t in d["tracks"]}
        def Dof(t):
            Lm = np.median(t["L4"]); return float(np.hypot(t["y"][-1] - t["y"][0], t["x"][-1] - t["x"][0]) / Lm)
        def vmean(t):
            Lm = np.median(t["L4"]); n = t["n"]
            return float(np.hypot(t["y"][-1] - t["y"][0], t["x"][-1] - t["x"][0]) / Lm / max(n - 1, 1) / FT) if n > 1 else np.nan
        for t in d["tracks"]:
            if not t["dividing"]: continue
            divD.append(Dof(t))
            for c in t["lasting"]:
                ct = tb[c]
                if ct["dividing"]: pairs.append((Dof(t), Dof(ct)))
                if ct["n"] >= 2 * 4 + 1: pv.append((Dof(t), np.mean(np.hypot(np.diff(ct["y"]), np.diff(ct["x"]))) / np.median(ct["L4"]) / FT))
    divD = np.array(divD)
    o["dividing"] = int(len(divD)); o["median_D"] = float(np.median(divD)) if len(divD) else None
    o["D_ge3"] = int((divD >= 3).sum()); o["D_q90"] = float(np.quantile(divD, .9)) if len(divD) else None
    o["md_pairs"] = len(pairs)
    o["md_r"], o["md_ci"] = boot_r([a for a, b in pairs], [b for a, b in pairs]) if len(pairs) >= 4 else (None, None)
    o["pD_dpath_n"] = len(pv)
    o["pD_dpath_r"], o["pD_dpath_ci"] = boot_r([a for a, b in pv], [b for a, b in pv]) if len(pv) >= 4 else (None, None)
    o["_D"] = divD.tolist(); o["_R"] = R
    return o


res = {}
for eps, paths in arms:
    res[eps] = arm_stats(paths)
fig, axs = plt.subplots(1, 4, figsize=(18, 4.3))
E = sorted(res); xs = [max(e, 3e-3) for e in E]
lab = [f"{e:g}" for e in E]
axs[0].plot(xs, [res[e]["frac_swim"] for e in E], "o-", label="pooled")
for i in range(2):
    axs[0].plot(xs, [res[e]["frac_swim_per_seed"][i] if len(res[e]["frac_swim_per_seed"]) > i else np.nan for e in E], "x--", label=f"seed index {i}")
axs[0].set_ylabel(f"fraction of rod-frames swimming (> {THR:.3f} L/t)")
axs[1].plot(xs, [res[e]["switches_per_rod_100t"] for e in E], "o-", label="pooled")
for i in range(2):
    axs[1].plot(xs, [res[e]["switches_per_seed"][i] if len(res[e]["switches_per_seed"]) > i else np.nan for e in E], "x--")
axs[1].set_ylabel("state switches per rod per 100 t"); axs[1].set_ylim(bottom=0)
for e in E:
    v = res[e]["_R"]["spL"]
    axs[2].hist(np.log10(np.maximum(v, 1e-4)), np.linspace(-3, -0.5, 51), density=True, histtype="step", lw=1.6, label=f"eps {e:g}")
axs[2].set_xlabel("log10 speed (own lengths per t)"); axs[2].legend(fontsize=8)
axs[3].boxplot([res[e]["_D"] for e in E], tick_labels=lab); axs[3].axhline(3, color="C3", ls=":")
axs[3].set_xlabel("eps"); axs[3].set_ylabel("D of dividing rods (own lengths)")
for a in axs[:2]:
    a.set_xscale("log"); a.set_xlabel("eps (0 plotted at 0.003)"); a.legend(fontsize=7)
axs[0].set_title("swimming fraction"); axs[1].set_title("switching rate"); axs[2].set_title("speed distributions"); axs[3].set_title("per-cycle distance")
fig.tight_layout(); fig.savefig(op, dpi=90)
for e in res:
    res[e].pop("_R")
json.dump({str(k): v for k, v in res.items()}, open(oj, "w"), indent=1)
for e in E:
    r = res[e]; print(e, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items() if k != "_D"})
