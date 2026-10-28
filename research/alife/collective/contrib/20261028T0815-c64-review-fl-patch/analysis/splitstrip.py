"""Strips of the clean predator splits found by fltrack.py. usage: splitstrip.py TRACK.json FRAMES.npz OUT.png [max_rows]
Rows: clean splits (both daughters' tracks last >= 100 t, or split again cleanly after >= 25 t); columns: t-20 ... t+100,
crop 48 px centred on the parent's centroid. Red: prey matter, green: predator matter (both clipped at 1)."""
import sys, json, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
d = json.load(open(sys.argv[1])); F = np.load(sys.argv[2]); fr, ft = F['f'].astype(np.float32), F['t']; out = sys.argv[3]
mx = int(sys.argv[4]) if len(sys.argv) > 4 else 10
tr = d['tracks']
def clean(k):
    x = tr[k]; return (x['end'] - x['start'] >= 100) or (x['fate'] == 'split' and x['end'] - x['start'] >= 25)
ev = [e for e in d['events'] if e['kind'] == 'split' and sum(clean(k) for k in e['kids']) >= 2][:mx]
offs = [-20, 0, 10, 30, 60, 100]; C = 24; N = fr.shape[-1]
fig, ax = plt.subplots(max(1, len(ev)), len(offs), figsize=(1.6 * len(offs), 1.6 * max(1, len(ev))), squeeze=False)
for r, e in enumerate(ev):
    cy, cx = int(round(e['c'][0])), int(round(e['c'][1]))
    for j, o in enumerate(offs):
        i = int(np.argmin(np.abs(ft - (e['t'] + o)))); f = fr[i]
        img = np.stack([np.clip(f[0], 0, 1), np.clip(f[1], 0, 1), np.zeros_like(f[0])], -1)
        img = np.roll(np.roll(img, N // 2 - cy, 0), N // 2 - cx, 1)[N // 2 - C:N // 2 + C, N // 2 - C:N // 2 + C]
        a = ax[r, j]; a.imshow(img, interpolation='nearest'); a.set_xticks([]); a.set_yticks([])
        a.set_title(f"t={ft[i]:.0f}", fontsize=7)
        if j == 0: a.set_ylabel(f"split t={e['t']:.0f}\nparent {'free' if e['free'] else 'on prey'}", fontsize=7)
plt.tight_layout(); plt.savefig(out, dpi=80); print(len(ev), 'clean splits drawn')
