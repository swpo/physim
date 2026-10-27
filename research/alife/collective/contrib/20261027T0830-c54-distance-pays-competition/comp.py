"""(c54) Competition assay for Q:marangoni-distance-pays: founders half mar-40 (k1), half mar-60 (k2) in 16 px blocks, mutation off.
Arms: cdep (birth-site depletion, ladder), cdeptwin (depletion, MARS 40/40/40: k2 is a neutral label), cE (sink discs only, ladder),
cEtwin (sink discs only, neutral labels). The selection on mar 60 in an environment is its share in the ladder arm minus its share
(as a label) in that environment's twin, from the same initial field. Per run: k2 share among pure bodies over time, averaged
over t >= 1000 and at the end; per kind among dividing rods, M passers and median D. usage: comp.py anadir outpng seed [seed ...]"""
import sys, json, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
A, png = sys.argv[1], sys.argv[2]; seeds = [int(x) for x in sys.argv[3:]]
ARMS = ["cdep", "cdeptwin", "cE", "cEtwin"]; COL = {"cdep": "C0", "cdeptwin": "C0", "cE": "C1", "cEtwin": "C1"}
fig, ax = plt.subplots(1, len(seeds), figsize=(5 * len(seeds), 3.6), squeeze=False); ax = ax[0]
R = {}
print("seed arm       k2_share t<500  t>=1000  end   bodies_late  dividers k1: pass medD | k2: pass medD")
for j, s in enumerate(seeds):
    for a in ARMS:
        try: J = json.load(open(f"{A}/{a}_s{s}.json"))
        except FileNotFoundError: continue
        tr = np.array([x[:7] for x in J["traj"]], float); t = tr[:, 0] * 5; n = tr[:, 2:5].sum(1); ok = n >= 2
        sh = np.where(ok, tr[:, 4] / np.maximum(n, 1), np.nan)
        e, l = ok & (t < 500), ok & (t >= 1000)
        R[(s, a)] = (np.nanmean(sh[e]), np.nanmean(sh[l]), sh[ok][-1])
        D = J["div"]; per = []
        for k in (1, 2):
            dk = [d for d in D if d["kind"] == k]
            per.append(f"{sum(d['pass_rl'] for d in dk)}/{len(dk)} {np.median([d['D'] for d in dk]) if dk else np.nan:.2f}")
        print(f"{s} {a:9s} {R[(s,a)][0]:9.2f} {R[(s,a)][1]:8.2f} {R[(s,a)][2]:5.2f}   {np.mean(tr[l,1]):5.1f}        {per[0]} | {per[1]}")
        ax[j].plot(t[ok], sh[ok], color=COL[a], ls="-" if "twin" not in a else ":", label=a)
    ax[j].set_ylim(0, 1); ax[j].set_title(f"seed {s}: mar-60 share (twin: neutral label)"); ax[j].set_xlabel("time"); ax[j].legend(fontsize=7)
fig.tight_layout(); fig.savefig(png, dpi=90)
print("selection on mar 60 = ladder share - twin share (t>=1000 / end):")
for s in seeds:
    try:
        sd = (R[(s, "cdep")][1] - R[(s, "cdeptwin")][1], R[(s, "cdep")][2] - R[(s, "cdeptwin")][2])
        se = (R[(s, "cE")][1] - R[(s, "cEtwin")][1], R[(s, "cE")][2] - R[(s, "cEtwin")][2])
        print(f"  {s}: depletion {sd[0]:+.2f} / {sd[1]:+.2f}   sink discs only {se[0]:+.2f} / {se[1]:+.2f}")
    except KeyError: pass
