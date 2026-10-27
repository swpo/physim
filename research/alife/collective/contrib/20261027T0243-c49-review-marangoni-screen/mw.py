"""python mw.py : one-sided Mann-Whitney (mar 60 > base) on per-cycle distance D (extract.py disp_rl) of dividing rods, seeds 72, 73 and pooled."""
import json, numpy as np
from scipy.stats import mannwhitneyu
def D(n, s): return np.array([r['disp_rl'] for r in json.load(open(f'runs/{n}/seed{s}/table.json'))['rows'] if r['dividing']])
for s in (72, 73):
    b, m = D('base', s), D('mar60', s); print(s, 'n', len(m), len(b), 'p=%.3f' % mannwhitneyu(m, b, alternative='greater').pvalue)
b = np.concatenate([D('base', 72), D('base', 73)]); m = np.concatenate([D('mar60', 72), D('mar60', 73)])
print('pooled medD', np.median(m).round(2), np.median(b).round(2), 'p=%.3f' % mannwhitneyu(m, b, alternative='greater').pvalue)
