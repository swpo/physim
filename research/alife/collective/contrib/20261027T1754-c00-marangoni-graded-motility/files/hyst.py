"""Part (b): swimming fraction and speed of the rods against mar(t) on the up and down legs of two opposite-order ramps.
usage: hyst.py OUT.png OUT.json THR_SWIM_L_per_t rampA/rods.json rampB/rods.json [fixed mar runs: label=path ...]
A rod-frame is 'swimming' when its speed (own lengths per t, 10 t window) exceeds THR. Loop area is the mean
difference (down minus up) of each quantity over common mar bins; the sign is compared between the two runs:
same sign in both (down above up, whatever came first in time) = hysteresis; opposite sign = drift with run time."""
import sys, json
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/paperexp/marangoni-bistability")
import states as S

out_png, out_json, thr = sys.argv[1], sys.argv[2], float(sys.argv[3])
ramps = sys.argv[4:6]; fixed = [a.split("=", 1) for a in sys.argv[6:]]
bins = np.arange(20, 60.01, 4.0); cb = 0.5 * (bins[1:] + bins[:-1])
res = {"thr": thr, "bins": cb.tolist(), "runs": {}}
fig, axs = plt.subplots(1, 4, figsize=(19, 4.6))
cols = {"A": ("C0", "C1"), "B": ("C2", "C3")}
for lab, p in zip("AB", ramps):
    d = json.load(open(p)); R, trk = S.load([p]); mar = np.array(d["mar"]); FT = d["FT"]
    t = R["t"]; f = R["f"].astype(int)
    dm = np.gradient(mar)  # per frame
    leg = np.where(dm[f] > 1e-9, "up", np.where(dm[f] < -1e-9, "down", "hold"))
    rr = {}
    for lg, col in zip(("up", "down"), cols[lab]):
        m = leg == lg
        v = R["spL"][m]; mm = R["mar"][m]; fr = R["f"][m]
        mean_v, frac, nn, ring = [], [], [], []
        for a, b in zip(bins[:-1], bins[1:]):
            k = (mm >= a) & (mm < b)
            # per-frame fraction, then mean over frames in the bin (each frame weighs equally)
            fs = [np.mean(v[k & (fr == q)] > thr) for q in np.unique(fr[k])]
            mean_v.append(float(np.mean(v[k])) if k.any() else np.nan); frac.append(float(np.mean(fs)) if fs else np.nan)
            nn.append(int(k.sum())); ring.append(float(np.median(-R["ring"][m][k])) if k.any() else np.nan)
        rr[lg] = dict(mean_spL=mean_v, frac_swim=frac, n=nn, ring_rear=ring)
        order = "first" if (lab == "A") == (lg == "up") else "second"
        axs[0].plot(cb, frac, "-o", color=col, label=f"ramp {lab} {lg} ({order} leg)")
        axs[1].plot(cb, mean_v, "-o", color=col, label=f"ramp {lab} {lg}")
        axs[2].plot(cb, ring, "-o", color=col, label=f"ramp {lab} {lg}")
    dfrac = np.nanmean(np.array(rr["down"]["frac_swim"]) - np.array(rr["up"]["frac_swim"]))
    dv = np.nanmean(np.array(rr["down"]["mean_spL"]) - np.array(rr["up"]["mean_spL"]))
    rr["loop_down_minus_up"] = dict(frac_swim=float(dfrac), mean_spL=float(dv))
    # time series of the number of rods and mean speed
    nfr = np.bincount(f, minlength=len(mar)); sv = np.bincount(f, R["spL"], minlength=len(mar)) / np.maximum(nfr, 1)
    tt = np.arange(len(mar)) * FT
    axs[3].plot(tt, d["ncomp"], color=cols[lab][0], lw=1, label=f"ramp {lab}: bodies")
    ax2 = axs[3]
    rr["ncomp_q"] = [int(np.median(d["ncomp"][i:i + 40])) for i in range(0, len(mar), 80)]
    res["runs"][lab] = rr
for lab, p in fixed:
    R, trk = S.load([p]); d = json.load(open(p)); mar = d["mar"][0]
    late = R["t"] >= 500
    fr = R["f"][late]; v = R["spL"][late]
    fs = [np.mean(v[fr == q] > thr) for q in np.unique(fr)]
    res.setdefault("fixed", {})[lab] = dict(mar=mar, frac_swim=float(np.mean(fs)), mean_spL=float(np.mean(v)))
    axs[0].plot([mar], [np.mean(fs)], "k*", ms=14, label=f"fixed mar {mar:g} ({lab}, t >= 500)")
    axs[1].plot([mar], [np.mean(v)], "k*", ms=14)
axs[0].set_xlabel("mar"); axs[0].set_ylabel(f"fraction of rods swimming (> {thr:.3f} lengths/t)"); axs[0].legend(fontsize=7)
axs[1].set_xlabel("mar"); axs[1].set_ylabel("mean speed (own lengths per t)"); axs[1].legend(fontsize=7)
axs[2].set_xlabel("mar"); axs[2].set_ylabel("ring rear-loading (median, lengths)"); axs[2].legend(fontsize=7)
axs[3].set_xlabel("t"); axs[3].set_ylabel("bodies"); axs[3].legend(fontsize=7)
axs[0].set_title("swimming fraction: up vs down legs"); axs[1].set_title("mean speed"); axs[2].set_title("ring polarity")
axs[3].set_title("population size over the ramps")
fig.tight_layout(); fig.savefig(out_png, dpi=90)
json.dump(res, open(out_json, "w"), indent=1)
print(json.dumps({k: v["loop_down_minus_up"] for k, v in res["runs"].items()}, indent=1), res.get("fixed"))
