"""(c54) Paired summary for Q:marangoni-distance-pays. Arms: dep (birth-site depletion, ladder 20/40/60), twin (same, MARS 40/40/40),
glob (DEP=2: the same supply loss spread over the whole domain, ladder), E (c50's sink-disc world without depletion, ladder).
Per run, from spread_stats.py's json: trait mean (ladder value of pure living bodies) averaged over t >= 1000 and at the end;
mar-60 and mar-20 shares late; M-gate passers (3 own rod lengths, rear tip >= 2/3) among dividing rods; median D (own rod
lengths per cycle) and cycle; the selection gradient of relative descendants (two median cycles after birth) on standardized D;
Spearman of path speed vs cycle. usage: pool.py anadir outpng seed [seed ...]"""
import sys, json, numpy as np
from scipy import stats
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
A = sys.argv[1]; png = sys.argv[2]; seeds = [int(x) for x in sys.argv[3:]]
ARMS = ["dep", "twin", "glob", "E"]
COL = {"dep": "C0", "twin": "0.5", "glob": "C2", "E": "C1"}
res = {}
fig, ax = plt.subplots(1, len(seeds) + 1, figsize=(4.2 * (len(seeds) + 1), 3.4))
print("seed arm   trait_late trait_end k2_late k0_late  pass     medD  cycle  Dgrad   rho(v,cycle)  bodies_late  pass(born<1000 / >=1000)")
for j, s in enumerate(seeds):
    for a in ARMS:
        fn = f"{A}/{'dep07' if a == 'dep' else a}_s{s}.json"
        try: J = json.load(open(fn))
        except FileNotFoundError: continue
        tr = np.array([x[:7] for x in J["traj"]], float); t = tr[:, 0] * 5; n = tr[:, 2:5].sum(1); ok = n >= 3
        late = ok & (t >= 1000)
        tl = np.nanmean(tr[late, 5]) if late.any() else np.nan
        te = tr[ok, 5][-1] if ok.any() else np.nan
        k2 = np.mean(tr[late, 4] / n[late]) if late.any() else np.nan
        k0 = np.mean(tr[late, 2] / n[late]) if late.any() else np.nan
        D = J["div"]; Dv = np.array([d["D"] for d in D]); pa = sum(d["pass_rl"] for d in D)
        cyc = np.array([d["cycle"] for d in D]); vp = np.array([d["vpath"] for d in D]); de = None
        g = np.nan
        ok2 = np.array([d["desc2"] is not None for d in D], bool)
        if ok2.sum() > 3:
            dv, dd = Dv[ok2], np.array([d["desc2"] for d in D if d["desc2"] is not None], float)
            if dd.mean() > 0 and dv.std() > 0:
                g = np.polyfit((dv - dv.mean()) / dv.std(), dd / dd.mean(), 1)[0]
        e1 = [d for d in D if d["start"] * 5 < 1000]; l1 = [d for d in D if d["start"] * 5 >= 1000]
        pe, pl = sum(d["pass_rl"] for d in e1), sum(d["pass_rl"] for d in l1)
        rho = stats.spearmanr(vp, cyc)[0] if len(D) > 3 else np.nan
        res[(s, a)] = dict(tl=tl, te=te, k2=k2, k0=k0, pa=pa, n=len(D), medD=float(np.median(Dv)) if len(D) else np.nan, g=g)
        print(f"{s} {a:5s} {tl:9.1f} {te:9.1f} {k2:7.2f} {k0:7.2f}  {pa:2d}/{len(D):<3d} {np.median(Dv) if len(D) else np.nan:6.2f} {np.median(cyc) if len(D) else np.nan:6.0f} {g:+6.2f}   {rho:+.2f}   {np.mean(tr[late,1]) if late.any() else 0:.1f}   early {pe}/{len(e1)} late {pl}/{len(l1)}")
        ax[j].plot(t[ok], tr[ok, 5], color=COL[a], lw=1.2, label=f"{a} (M {pa}/{len(D)})")
    ax[j].axhline(40, ls=":", c="k"); ax[j].set_ylim(18, 62); ax[j].set_title(f"seed {s}: trait mean"); ax[j].set_xlabel("time"); ax[j].legend(fontsize=7)
xs = np.arange(len(ARMS))
for s in seeds:
    y = [res[(s, a)]["pa"] / max(res[(s, a)]["n"], 1) if (s, a) in res else np.nan for a in ARMS]
    ax[-1].plot(xs, y, "o-", label=str(s))
ax[-1].set_xticks(xs); ax[-1].set_xticklabels(ARMS); ax[-1].set_title("share of dividing rods passing M gate"); ax[-1].legend(fontsize=7)
fig.suptitle("c54 Q:marangoni-distance-pays: birth-site depletion (dep) vs twin, global-loss control (glob), sink discs only (E)")
fig.tight_layout(); fig.savefig(png, dpi=90)
for a in ["twin", "glob", "E"]:
    d = [(res[(s, "dep")]["tl"] - res[(s, a)]["tl"], res[(s, "dep")]["pa"] / max(res[(s, "dep")]["n"], 1) - res[(s, a)]["pa"] / max(res[(s, a)]["n"], 1)) for s in seeds if (s, "dep") in res and (s, a) in res]
    if d:
        d = np.array(d); print(f"dep minus {a}: trait_late {' '.join(f'{x:+.1f}' for x in d[:,0])}; pass share {' '.join(f'{x:+.2f}' for x in d[:,1])}; seeds dep>{a}: trait {int((d[:,0]>0).sum())}/{len(d)}, pass {int((d[:,1]>0).sum())}/{len(d)}")
