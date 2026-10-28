"""Strips of established fusions (fusion.py's definition). usage: fusestrip.py TRACK.json FRAMES.npz OUT.png [AGE=100]
Columns t-100 ... t+60 around the merge, crop 48 px centred on the merged body; red prey, green predator."""
import sys, json, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
d = json.load(open(sys.argv[1])); F = np.load(sys.argv[2]); fr, ft = F['f'].astype(np.float32), F['t']; out = sys.argv[3]
AGE = float(sys.argv[4]) if len(sys.argv) > 4 else 100
ev = [e for e in d['events'] if e['kind'] == 'merge' and sum(a >= AGE and ar >= 0.25 * max(e['areas']) for a, ar in zip(e['ages'], e['areas'])) >= 2]
offs = [-100, -50, -20, 0, 20, 60]; C = 24; N = fr.shape[-1]
fig, ax = plt.subplots(max(1, len(ev)), len(offs), figsize=(1.6 * len(offs), 1.6 * max(1, len(ev))), squeeze=False)
for r, e in enumerate(ev):
    cy, cx = int(round(e['c'][0])), int(round(e['c'][1]))
    for j, o in enumerate(offs):
        i = int(np.argmin(np.abs(ft - (e['t'] + o)))); f = fr[i]
        img = np.stack([np.clip(f[0], 0, 1), np.clip(f[1], 0, 1), np.zeros_like(f[0])], -1)
        img = np.roll(np.roll(img, N // 2 - cy, 0), N // 2 - cx, 1)[N // 2 - C:N // 2 + C, N // 2 - C:N // 2 + C]
        a = ax[r, j]; a.imshow(img, interpolation='nearest'); a.set_xticks([]); a.set_yticks([]); a.set_title(f"t={ft[i]:.0f}", fontsize=7)
        if j == 0: a.set_ylabel(f"merge t={e['t']:.0f}\nages {[int(x) for x in e['ages']]}", fontsize=6)
plt.tight_layout(); plt.savefig(out, dpi=80); print(len(ev), 'fusions drawn')
