"""c58: who wins a fusion, and who fades? For each labkit merge after labelling whose two largest parents differ in trait by
> dm/2: the 'winner' is the parent whose trait is closer to the fused vortex's trait. Reports how often the winner is the
larger parent and how often it is the parent of the rarer class (class share at the nearest traits_by_frame sample), and the
mean class share of vortices that fade (tracks that end with no children before the end) against the mean class share seen by
a random vortex. python fusion.py run.json ..."""
import sys, json, numpy as np
dm = 0.4
for f in sys.argv[1:]:
    r = json.load(open(f)); tb = r['traits_by_frame']; ts = np.array([t for t, _ in tb])
    shares = []
    for t, th in tb:
        cl = np.round(np.array(th) / dm).astype(int); u, n = np.unique(cl, return_counts=True); shares.append(dict(zip(u.tolist(), (n / len(cl)).tolist())))
    def sh(t, x):
        j = int(np.argmin(np.abs(ts - t))); return shares[j].get(int(round(x / dm)), 0.0)
    nm = big = rare = 0; ties = 0
    for t, tc, pr in r['merge_rows']:
        pr = [p for p in pr if p[0] is not None]
        if tc is None or len(pr) < 2: continue
        pr = sorted(pr, key=lambda p: -p[1])[:2]
        if abs(pr[0][0] - pr[1][0]) <= dm / 2: continue
        win = 0 if abs(tc - pr[0][0]) < abs(tc - pr[1][0]) else 1
        s0, s1 = sh(t, pr[0][0]), sh(t, pr[1][0])
        nm += 1; big += (win == 0)
        if s0 == s1: ties += 1
        else: rare += (win == (0 if s0 < s1 else 1))
    fs = [sh(t, x) for t, x in r['fade_rows']]
    rv = [np.mean([shares[j][int(round(x / dm))] for x in th]) for j, (t, th) in enumerate(tb) if len(th)]
    print(json.dumps({'run': f, 'distinct_trait_merges': nm, 'winner_is_larger': big, 'winner_is_rarer_class': rare, 'equal_share': ties,
                      'fades': len(fs), 'fade_class_share_mean': round(float(np.mean(fs)), 3) if fs else None, 'random_vortex_class_share_mean': round(float(np.mean(rv)), 3)}))
