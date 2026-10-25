"""Deaths of mature cells only (seen in >= MIN snapshots = MIN*50 steps, and not a cell that first 'appeared'
as a remnant), with the cell's yield y and inert marker z as percentiles among the living cells at its last
snapshot. Removes the remnant double counts (small bodies flickering across the 20-particle threshold)."""
import sys, json, numpy as np
d = json.load(open(sys.argv[1])); S = d['series']; MIN = int(sys.argv[2]) if len(sys.argv) > 2 else 100
pos = {}
for a, x in enumerate(S):
    for i, c in enumerate(x['id']): pos.setdefault(c, []).append((a, i))
appeared = {ch[0] for t, ty, p, ch in d['events'] if ty == 'appear' and t > 1000}
def pct(a, i, key):
    x = S[a]; y = x[key][i]; o = np.array([v for j, v in enumerate(x[key]) if j != i])
    return float((np.sum(o < y) + 0.5 * np.sum(o == y)) / len(o))
rows = []
for t, ty, p, ch in d['events']:
    if ty != 'death' or p[0] in appeared: continue
    L = pos[p[0]]
    if len(L) < MIN: continue
    a, i = L[-1]
    rows.append(dict(t=t, life_steps=50 * len(L), np_first=S[L[0][0]]['np'][L[0][1]], y=S[a]['ym'][i], y_pct=round(pct(a, i, 'ym'), 3), z_pct=round(pct(a, i, 'zm'), 3)))
sp = [e for e in d['events'] if e[1] == 'split' and len(e[3]) >= 2]
print(json.dumps(dict(file=sys.argv[1], min_snapshots=MIN, n_mature_deaths=len(rows), mean_y_pct=round(float(np.mean([r['y_pct'] for r in rows])), 3) if rows else None,
      mean_z_pct=round(float(np.mean([r['z_pct'] for r in rows])), 3) if rows else None, deaths=rows, all_deaths=sum(1 for e in d['events'] if e[1] == 'death'), splits=len(sp))))
