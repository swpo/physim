"""c59: novelty measures on trait3.py output (traits_by_frame: every 30 t, the 3-component trait of every labelled vortex).
Class = round(theta/dm), dm 0.4. Per run, against time:
  n          number of labelled vortices
  div        mean pairwise trait distance (diversity)
  cen        distance of the population trait centroid from the ancestor (0)
  rms        rms distance of vortices from the ancestor
  new_act    Bedau-Packard style: classes whose cumulative activity (vortex-samples) first reaches A0=5, per 1000 t
  age_mean   activity-weighted mean age (t - first appearance of the class) of the vortices present now
  surv       of the classes that ever reached A0 by time t-1000, the share still present at t
python novelty2.py out.png label1=a.json label2=b.json ..."""
import sys, json, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
DM, A0 = 0.4, 5
def measure(path):
    d = json.load(open(path)); tb = d['traits_by_frame']
    T = []; N = []; DIV = []; CEN = []; RMS = []; AGE = []; first = {}; act = {}; crossed = []; present = []
    for t, th in tb:
        x = np.array(th).reshape(-1, 3); T.append(t); N.append(len(x))
        if len(x) >= 2:
            dd = np.sqrt(((x[:, None] - x[None]) ** 2).sum(-1)); DIV.append(dd[np.triu_indices(len(x), 1)].mean())
        else: DIV.append(np.nan)
        CEN.append(np.linalg.norm(x.mean(0)) if len(x) else np.nan); RMS.append(np.sqrt((x ** 2).sum(1).mean()) if len(x) else np.nan)
        cl = [tuple(int(round(v / DM)) for v in r) for r in x]
        for c in cl:
            first.setdefault(c, t); act[c] = act.get(c, 0) + 1
            if act[c] == A0: crossed.append(t)
        AGE.append(np.mean([t - first[c] for c in cl]) if cl else np.nan); present.append(set(cl))
    T = np.array(T); crossed = np.array(crossed)
    surv = []
    for i, t in enumerate(T):
        j = np.searchsorted(T, t - 1000)
        if t - 1000 < T[0]: surv.append(np.nan); continue
        # classes that reached A0 by t-1000
        old = set(); a2 = {}
        for k in range(j + 1):
            for r in tb[k][1]:
                c = tuple(int(round(v / DM)) for v in r); a2[c] = a2.get(c, 0) + 1
        old = {c for c, v in a2.items() if v >= A0}
        surv.append(len(old & present[i]) / len(old) if old else np.nan)
    C = np.array([np.array(th).reshape(-1, 3).mean(0) if len(th) else [np.nan] * 3 for _, th in tb]); lags = np.arange(1, len(T) // 2); taus = lags * (T[1] - T[0])
    msd = np.array([np.nanmean(((C[l:] - C[:-l]) ** 2).sum(1)) for l in lags])
    return dict(msd=(taus, msd), T=T, n=np.array(N), div=np.array(DIV), cen=np.array(CEN), rms=np.array(RMS), age=np.array(AGE), crossed=crossed, surv=np.array(surv), Tend=d['T'])
def window_rate(ev, Tend, w=1000):
    edges = np.arange(0, Tend + 1, w); return edges[1:], np.histogram(ev, edges)[0]
if __name__ == '__main__':
    out = sys.argv[1]; runs = [a.split('=', 1) for a in sys.argv[2:]]
    fig, ax = plt.subplots(2, 4, figsize=(17, 7)); ax = ax.ravel(); summ = {}
    for lab, p in runs:
        m = measure(p); ls = '-' if 'spec' in lab else '--'
        ax[0].plot(m['T'], np.arange(1, 1) if False else np.searchsorted(np.sort(m['crossed']), m['T'], side='right'), ls, label=lab)
        e, r = window_rate(m['crossed'], m['Tend']); ax[1].step(e, r, ls, where='pre', label=lab)
        sm = lambda y: np.convolve(np.nan_to_num(y), np.ones(9) / 9, 'same') / np.convolve(np.ones(len(y)), np.ones(9) / 9, 'same')
        ax[2].plot(m['T'], sm(m['age']), ls, label=lab); ax[3].plot(m['T'], sm(m['div']), ls, label=lab)
        ax[4].plot(m['T'], sm(m['cen']), ls, label=lab); ax[5].plot(m['T'], m['surv'], ls, label=lab)
        taus, msd = m['msd']; ax[6].loglog(taus, msd, ls, label=lab); ax[7].plot(m['T'], sm(m['rms']), ls, label=lab)
        late = m['T'] >= m['Tend'] / 2
        summ[lab] = {'classes_reaching_A0': int(len(m['crossed'])), 'new_per_1000t_by_window': r.tolist(),
                     'age_mean_late': float(np.nanmean(m['age'][late])), 'age_end': float(np.nanmean(m['age'][-10:])),
                     'div_late': float(np.nanmean(m['div'][late])), 'centroid_end': float(np.nanmean(m['cen'][-10:])), 'rms_end': float(np.nanmean(m['rms'][-10:])),
                     'centroid_msd_tau_1000_4000': [float(np.interp(1000, *m['msd'])), float(np.interp(4000, *m['msd']))], 'surv_1000_late': float(np.nanmean(m['surv'][late])), 'n_mean': float(np.nanmean(m['n']))}
    for a, ttl in zip(ax, [f'classes reaching activity {A0} (cumulative)', 'new classes per 1000 t', 'mean class age of present vortices (t)',
                          'trait diversity (mean pairwise distance)', 'population centroid |theta| from ancestor', 'share of classes alive 1000 t ago still present', 'centroid MSD vs lag (t)', 'rms |theta| of vortices from ancestor']):
        a.set_title(ttl, fontsize=9); a.set_xlabel('t')
    ax[0].legend(fontsize=7); fig.tight_layout(); fig.savefig(out, dpi=80)
    json.dump(summ, open(out.replace('.png', '.json'), 'w'), indent=1)
    for k, v in summ.items(): print(k, v)
