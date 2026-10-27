"""c58: novelty and turnover from trait.py outputs. A class (round(theta/dm)) is dominant at a sample when it holds the
plurality of labelled vortices; a dominance spell needs >= 3 consecutive samples (90 t). Reports per run: dominance spells,
distinct classes ever dominant, new-dominant events (a class dominant for the first time) per 1000 t in t<3000 and t>=3000,
returns to an earlier dominant class, the range of classes present, and (when traits_by_frame exists) the cumulative
number of classes ever held by >= 3 vortices at once. python novelty.py out.png run1.json [run2.json ...]"""
import sys, json, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
out = sys.argv[1]; fs = sys.argv[2:]
fig, ax = plt.subplots(len(fs), 1, figsize=(10, 2.2 * len(fs)), sharex=True, squeeze=False)
for i, f in enumerate(fs):
    r = json.load(open(f)); p = np.array(r['pop_t_n_mean_std_domclass_domshare_min_max'], float); dm = 0.4
    t, dom = p[:, 0], p[:, 4].astype(int)
    spells = []; k = 0
    while k < len(dom):
        j = k
        while j < len(dom) and dom[j] == dom[k]: j += 1
        if j - k >= 3: spells.append((int(t[k]), int(dom[k]), j - k))
        k = j
    merged = []
    for sp in spells:
        if merged and merged[-1][1] == sp[1]: continue
        merged.append(sp)
    seen = set(); new_ev = []; returns = 0
    for (ts, c, L) in merged:
        if c in seen: returns += 1
        else: seen.add(c); new_ev.append(ts)
    new_ev = np.array(new_ev[1:])
    early = int(((new_ev < 3000)).sum()); late = int((new_ev >= 3000).sum())
    cum = None
    if 'traits_by_frame' in r:
        ever = set(); cum = []
        for tt, th in r['traits_by_frame']:
            cl, cn = np.unique(np.round(np.array(th) / dm).astype(int), return_counts=True) if len(th) else ([], [])
            ever |= {int(c) for c, n in zip(cl, cn) if n >= 3}; cum.append((tt, len(ever)))
        cum = np.array(cum)
        # stacked shares of classes
        cls_all = sorted({int(round(x / dm)) for _, th in r['traits_by_frame'] for x in th})
        S = np.zeros((len(cls_all), len(r['traits_by_frame'])))
        for j, (tt, th) in enumerate(r['traits_by_frame']):
            for x in th: S[cls_all.index(int(round(x / dm))), j] += 1
        S = S / np.maximum(S.sum(0), 1)
        tt = [a for a, _ in r['traits_by_frame']]
        cm = plt.get_cmap('turbo'); lo, hi = -6, 10
        ax[i, 0].stackplot(tt, S, colors=[cm((c - lo) / (hi - lo)) for c in cls_all], lw=0)
        ax[i, 0].set_ylim(0, 1)
    else:
        ax[i, 0].plot(t, dom, 'k', lw=1)
    ax[i, 0].set_title(f"{f}: {r['WORLD_P']}  dominant classes {[c for _, c, _ in merged]}", fontsize=7)
    res = {'run': f, 'spells': len(merged), 'distinct_dominant': len(seen), 'new_dominant_t<3000': early, 'new_dominant_t>=3000': late, 'returns': returns,
           'class_range_end': (int(p[-1, 6]), int(p[-1, 7])), 'class_min_max_ever': (int(p[:, 6].min()), int(p[:, 7].max())),
           'mean_n_vortices': round(float(p[:, 1].mean()), 1), 'final_classes_ge3': (int(cum[-1, 1]) if cum is not None else None)}
    print(json.dumps(res))
ax[-1, 0].set_xlabel('t'); fig.tight_layout(); fig.savefig(out, dpi=80)
