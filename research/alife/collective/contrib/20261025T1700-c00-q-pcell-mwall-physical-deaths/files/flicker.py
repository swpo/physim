"""Are genealogy 'deaths' real disappearances or MINP / threshold flicker? For each death of a mature
cell (>= 20 snapshots, t > 1000), look for an 'appear' event within WIN steps after it, within RAD px of
the dying cell's last position (periodic). Also: first-snapshot size and yield rank of 'appear' cells.
usage: python flicker.py snaps.pkl gen.json [H=128]"""
import sys, json, pickle, numpy as np
pk, gj = sys.argv[1], sys.argv[2]; H = int(sys.argv[3]) if len(sys.argv) > 3 else 128
snaps = pickle.load(open(pk, 'rb'))['snaps']; d = json.load(open(gj)); S = d['series']; E = d['events']
pos = {}
for a, x in enumerate(S):
    for i, c in enumerate(x['id']): pos.setdefault(c, []).append((a, i))
def xy(c, last):
    a, i = pos[c][-1] if last else pos[c][0]; C = snaps[a][1][i]; return C['cy'], C['cx'], snaps[a][0]
def dist(p, q):
    dy = abs(p[0] - q[0]) % H; dx = abs(p[1] - q[1]) % H
    return np.hypot(min(dy, H - dy), min(dx, H - dx))
appear = [(e[0], e[3][0]) for e in E if e[1] == 'appear']
res = {}
for WIN, RAD in ((2000, 6), (5000, 8)):
    n = hit = 0
    for e in E:
        if e[1] != 'death' or e[0] <= 1000: continue
        c = e[2][0]
        if len(pos.get(c, [])) < 20: continue
        n += 1; p = xy(c, True)
        for t, a in appear:
            if e[0] <= t <= e[0] + WIN and a in pos and dist(p, xy(a, False)) <= RAD: hit += 1; break
    res[f'deaths_followed_by_appear_within_{WIN}steps_{RAD}px'] = f'{hit}/{n}'
ap = []
for t, a in appear:
    if t <= 1000 or a not in pos: continue
    a0, i0 = pos[a][0]; x = S[a0]; y = x['ym'][i0]; o = np.array([v for j, v in enumerate(x['ym']) if j != i0])
    if len(o): ap.append(((np.sum(o < y) + 0.5 * np.sum(o == y)) / len(o), x['np'][i0], len(pos[a])))
ap = np.array(ap)
res.update(n_appear=len(ap), appear_first_rank_mean=round(float(ap[:, 0].mean()), 3), appear_first_np_median=float(np.median(ap[:, 1])),
           appear_life_snapshots_median=float(np.median(ap[:, 2])))
print(json.dumps(res))
