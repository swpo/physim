"""Fraction of the 6 targets (seeds 61, 62) alive with their prey present, against the held kd fraction, step vs 1000 t ramp."""
import json, os, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'runs'))
def fate(f, tmax):
    d = json.load(open(f)); r = d['rows']; alive = sup = 0
    for k in range(len(d['targets'])):
        tr = [(x['t'] - d['t0'], x['targets'][k]) for x in r if x['t'] - d['t0'] <= tmax + 1]
        al = [x['alive'] for _, x in tr]
        if False in al:
            i = al.index(False); sup += tr[i - 1][1]['prey_area'] > 0
        else: alive += 1
    return alive, sup
fr = [0, 0.05, 0.1, 0.25, 0.5]; fig, ax = plt.subplots(figsize=(5, 3.4))
for r, mk, lab in ((0, 'o-', 'abrupt step'), (1000, 's--', 'ramp over 1000 t')):
    xs, ys = [], []
    for f in fr:
        n = 0; a = 0
        for s in (61, 62):
            name = f'hold_f{f}_r{r}_s{s}.json' if f else f'hold_f0_r1000_s{s}.json'
            if f == 0 and r == 0: continue
            if not os.path.exists(name): continue
            al, _ = fate(name, 3000); a += al; n += 3
        if n: xs.append(f); ys.append(a / n)
    ax.plot(xs, ys, mk, label=lab)
ax.plot([0], [0], 'ko', ms=4, label='step to 0 (claim kdarms, 0/6)')
a = sum(fate(f'ctrl_T5000_s{s}.json', 3000)[0] for s in (61, 62)); ax.axhline(a / 6, color='g', lw=1, label='fed twin (losses only after prey eaten out)')
ax.set_xlabel('held kd / fed kd (inside the disk following each predator)'); ax.set_ylabel('targets alive at +3000'); ax.legend(fontsize=7); ax.set_ylim(-0.05, 1.05)
plt.tight_layout(); plt.savefig('../threshold.png', dpi=100)
