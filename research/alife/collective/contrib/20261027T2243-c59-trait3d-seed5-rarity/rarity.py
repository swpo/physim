"""c59: does the kind-specific waste act through LOCAL rarity? From trait3.py's 'vort' (every 30 t: trait, centroid, track id),
for every vortex-sample: local similarity S = sum over other vortices within R px (periodic) of exp(-|dtheta|^2/(2 0.4^2)),
and global similarity Sg = the same over all vortices / n. Compares S at the last sample before
  births: parents of persistent splits (labkit lineage),  ends: tracks that end without being a split parent (fade or merge)
with all vortex-samples (permutation p for the difference of means). Also the vortex count of similar neighbours.
python rarity.py R label=run.json ..."""
import sys, json, numpy as np
R = float(sys.argv[1]); SW = 0.4
rng = np.random.default_rng(0)
out = {}
for arg in sys.argv[2:]:
    lab, p = arg.split('=', 1); d = json.load(open(p)); N = d.get('size', 128)
    T = np.array([t for t, _ in d['vort']]); S = {}; SG = {}; allS = []; allSG = []
    for t, vs in d['vort']:
        v = np.array(vs).reshape(-1, 6)
        if len(v) < 2: continue
        th, pos, tid = v[:, :3], v[:, 3:5], v[:, 5].astype(int)
        dp = np.abs(pos[:, None] - pos[None]); dp = np.minimum(dp, N - dp); dist = np.sqrt((dp ** 2).sum(-1))
        G = np.exp(-((th[:, None] - th[None]) ** 2).sum(-1) / (2 * SW ** 2)); np.fill_diagonal(G, 0)
        s = (G * (dist < R)).sum(1); sg = G.sum(1) / (len(v) - 1)
        for k, i in enumerate(tid): S[(t, i)] = s[k]; SG[(t, i)] = sg[k]
        allS += s.tolist(); allSG += sg.tolist()
    def last_sample(tid, tend):
        j = np.searchsorted(T, tend, side='right') - 1
        while j >= 0 and T[j] >= tend - 90:
            if (T[j], tid) in S: return S[(T[j], tid)], SG[(T[j], tid)]
            j -= 1
        return None
    parents = {pp for _, pp, _ in d['splits']}
    par = [last_sample(pp, ft) for ft, pp, _ in d['splits'] if ft > 400]
    ends = [last_sample(k, se[1]) for k, se in enumerate(d['track_span']) if k not in parents and se[1] < d['T'] - 10 and se[1] - se[0] >= 30 and se[0] > 400]
    par = np.array([x for x in par if x is not None]); ends = np.array([x for x in ends if x is not None]); allS = np.array(allS); allSG = np.array(allSG)
    def perm(sub, pool):
        obs = sub.mean() - pool.mean(); null = np.array([rng.choice(pool, len(sub)).mean() - pool.mean() for _ in range(2000)])
        return float(obs), float((np.abs(null) >= abs(obs)).mean())
    out[lab] = {'n_samples': len(allS), 'mean_local_S_all': float(allS.mean()),
                'births': {'n': len(par), 'local': perm(par[:, 0], allS), 'global': perm(par[:, 1], allSG)},
                'ends': {'n': len(ends), 'local': perm(ends[:, 0], allS), 'global': perm(ends[:, 1], allSG)}}
    print(lab, json.dumps(out[lab]))
json.dump(out, open(f'rarity_R{int(R)}.json', 'w'), indent=1)
