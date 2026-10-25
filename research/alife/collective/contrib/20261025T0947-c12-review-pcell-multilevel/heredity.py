"""Parent-daughter yield at persistent splits, and per-kind (high/low vs the median of living cells) births and deaths."""
import sys, json, numpy as np
for fn in sys.argv[1:]:
    d = json.load(open(fn)); S = d['series']; pos = {}
    for a, x in enumerate(S):
        for i, cid in enumerate(x['id']): pos.setdefault(cid, []).append((a, i))
    pairs = []
    for t, ty, p, ch in d['events']:
        if ty != 'split' or len(ch) < 2 or t < 1000: continue
        pa = [(a, i) for a, i in pos[p[0]] if S[a]['t'] < t][-1]
        yp = S[pa[0]]['ym'][pa[1]]
        for c in ch:
            if c in pos:
                a, i = pos[c][0]; pairs.append((yp, S[a]['ym'][i]))
    pairs = np.array(pairs)
    r = float(np.corrcoef(pairs.T)[0, 1]) if len(pairs) > 2 else None
    # spread among living cells at split times for scale
    dd = np.abs(pairs[:, 0] - pairs[:, 1]) if len(pairs) else []
    print(json.dumps(dict(file=fn, n_daughters=len(pairs), parent_daughter_r=round(r, 3) if r else None,
                          mean_abs_diff=round(float(np.mean(dd)), 4) if len(dd) else None,
                          living_sd_mid=round(float(np.std(S[len(S) // 2]['ym'])), 4))))
