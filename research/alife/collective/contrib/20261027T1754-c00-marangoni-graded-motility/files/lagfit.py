"""Lag test for the ramp loop: per-frame population mean speed m(t) and swimming fraction w(t) (split-born rods), plotted
against mar(t - tau). For each tau the loop is the mean |down - up| over common mar bins (4-unit bins, 22-58); the best
tau is the one that minimizes it. Also: mean rod area and own length on each leg at equal mar (graded size effect?), and
the loop of the first-order relaxation model y' = (f(mar) - y)/tau fitted to both runs.
usage: lagfit.py OUT.json OUT.png rampA/rods.json rampB/rods.json THR"""
import sys, json
sys.path.insert(0, "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/paperexp/marangoni-bistability")
import numpy as np, states as S
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
oj, op, pA, pB, thr = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], float(sys.argv[5])
bins = np.arange(22, 58.01, 4.0)
res = {}
fig, axs = plt.subplots(1, 3, figsize=(16, 4.5))
for lab, p in (("A", pA), ("B", pB)):
    d = json.load(open(p)); R, trk = S.load([p]); mar = np.array(d["mar"]); FT = d["FT"]; T = len(mar)
    f = R["f"].astype(int); nf = np.bincount(f, minlength=T)
    m = np.bincount(f, R["spL"], minlength=T) / np.maximum(nf, 1)
    w = np.bincount(f, (R["spL"] > thr).astype(float), minlength=T) / np.maximum(nf, 1)
    A = np.bincount(f, R["A"], minlength=T) / np.maximum(nf, 1); L = np.bincount(f, R["Lm"], minlength=T) / np.maximum(nf, 1)
    t = np.arange(T) * FT
    ok = (t >= 500) & (nf > 0)
    up = np.gradient(mar) > 0; dn = np.gradient(mar) < 0
    def loop(y, tau):
        k = int(round(tau / FT)); mm = np.interp(t - tau, t, mar)  # mar(t - tau)
        gm = np.gradient(mm); up = gm > 1e-9; dn = gm < -1e-9  # legs of the SHIFTED drive
        out = []
        for a, b in zip(bins[:-1], bins[1:]):
            iu = ok & up & (mm >= a) & (mm < b) & (np.arange(T) >= k); idn = ok & dn & (mm >= a) & (mm < b) & (np.arange(T) >= k)
            if iu.sum() > 5 and idn.sum() > 5: out.append(y[idn].mean() - y[iu].mean())
        return np.array(out)
    taus = np.arange(0, 401, 10)
    Lm_ = [np.mean(np.abs(loop(m, tau))) for tau in taus]; Lw_ = [np.mean(np.abs(loop(w, tau))) for tau in taus]
    Ls_ = [np.mean(loop(m, tau)) for tau in taus]
    best = int(taus[np.argmin(Lm_)])
    res[lab] = dict(zero_cross=float(np.interp(0, -np.array(Ls_), taus)), signed_curve=np.array(Ls_)[:8].round(5).tolist(), loop_meanspeed_tau0=float(Lm_[0]), signed_meanspeed_tau0=float(Ls_[0]), best_tau=best,
                    loop_meanspeed_best=float(np.min(Lm_)), signed_at_best=float(Ls_[int(np.argmin(Lm_))]),
                    loop_frac_tau0=float(Lw_[0]), best_tau_frac=int(taus[np.argmin(Lw_)]), loop_frac_best=float(np.min(Lw_)),
                    area_down_minus_up=loop(A, 0).round(2).tolist(), L_down_minus_up=loop(L, 0).round(3).tolist(),
                    mean_area_up=float(A[ok & up].mean()), mean_area_down=float(A[ok & dn].mean()))
    res[lab]["_curves"] = {"m": m.tolist(), "w": w.tolist(), "ok": ok.tolist(), "mar": mar.tolist(), "t": t.tolist()}
    axs[0].plot(taus, Lm_, label=f"ramp {lab}: mean |down-up| speed"); axs[1].plot(taus, Ls_, label=f"ramp {lab}: signed down-up")
    # smoothed trajectory in the (mar, m) plane
    ks = 20; sm = np.convolve(m, np.ones(ks) / ks, mode="same")
    axs[2].plot(mar[ok], sm[ok], lw=1, label=f"ramp {lab} (100 t running mean)")
axs[0].set_xlabel("tau (t)"); axs[0].set_ylabel("loop size (lengths/t)"); axs[0].legend(fontsize=8); axs[0].set_title("loop size vs assumed lag")
axs[1].axhline(0, color="k", lw=.5); axs[1].set_xlabel("tau (t)"); axs[1].legend(fontsize=8); axs[1].set_title("signed loop (down minus up)")
axs[2].set_xlabel("mar(t)"); axs[2].set_ylabel("mean speed (own lengths/t)"); axs[2].legend(fontsize=8); axs[2].set_title("trajectory: mean speed vs mar")
fig.tight_layout(); fig.savefig(op, dpi=90)
# noise reference: same leg, run A vs run B, binned by mar (tau = 0)
def binned(c, leg):
    m = np.array(c["m"]); w = np.array(c["w"]); ok = np.array(c["ok"]); mar = np.array(c["mar"]); g = np.gradient(mar)
    sel = ok & ((g > 1e-9) if leg == "up" else (g < -1e-9))
    return (np.array([m[sel & (mar >= a) & (mar < b)].mean() for a, b in zip(bins[:-1], bins[1:])]),
            np.array([w[sel & (mar >= a) & (mar < b)].mean() for a, b in zip(bins[:-1], bins[1:])]))
cA, cB = res["A"].pop("_curves"), res["B"].pop("_curves")
ref = {}
for leg in ("up", "down"):
    (ma, wa), (mb, wb) = binned(cA, leg), binned(cB, leg)
    ref[leg] = dict(meanspeed_absdiff=float(np.nanmean(np.abs(ma - mb))), frac_absdiff=float(np.nanmean(np.abs(wa - wb))))
(maU, waU), (maD, waD) = binned(cA, "up"), binned(cA, "down"); (mbU, wbU), (mbD, wbD) = binned(cB, "up"), binned(cB, "down")
res["noise_ref_same_leg_A_vs_B"] = ref
res["pooled_loop_signed"] = dict(meanspeed=float(np.nanmean((maD + mbD) / 2 - (maU + mbU) / 2)), frac=float(np.nanmean((waD + wbD) / 2 - (waU + wbU) / 2)),
                                 meanspeed_by_bin=((maD + mbD) / 2 - (maU + mbU) / 2).round(4).tolist(),
                                 frac_by_bin=((waD + wbD) / 2 - (waU + wbU) / 2).round(3).tolist(), bins=bins.tolist(),
                                 meanspeed_up=((maU + mbU) / 2).round(4).tolist(), meanspeed_down=((maD + mbD) / 2).round(4).tolist())
json.dump(res, open(oj, "w"), indent=1)
for k in ("A", "B"): print(k, {kk: v for kk, v in res[k].items() if not kk.endswith("_minus_up")})
print("noise ref", ref); print("pooled", res["pooled_loop_signed"])
