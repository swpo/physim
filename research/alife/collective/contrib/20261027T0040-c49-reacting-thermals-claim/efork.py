"""python efork.py : body counts (labkit series n_comp, 1 t per frame) in the fed run vs the fuel fork at t=400, per seed,
and deaths in the fed run (tracks that end without a split or merge before the last frame). Writes efork.png, efork.json."""
import json, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
out = {}; fig, ax = plt.subplots(1, 2, figsize=(10, 3.2))
for k, s in enumerate((0, 1)):
    fed = json.load(open(f'pack/seed{s}/metrics.json'))['series']['n_comp']
    frk = json.load(open(f'pack_fork/seed{s}/metrics.json'))['series']['n_comp']
    g0 = json.load(open(f'pack_g0/seed{s}/metrics.json'))['series']['n_comp']
    t = np.arange(len(fed))
    ax[k].plot(t, fed, 'r', label='fed (flow)'); ax[k].plot(t, frk, 'k', label='fuel emptied at t=400, no regrowth'); ax[k].plot(t, g0, 'b:', label='g=0 twin (fed)')
    ax[k].axvline(400, color='grey', lw=0.5); ax[k].set_title(f'seed {s}', fontsize=9); ax[k].set_xlabel('t'); ax[k].set_ylabel('bodies')
    zero = next((int(i) for i in t if i > 400 and frk[i] == 0), None)
    out[s] = {'fed_400': fed[400], 'fed_600': fed[-1], 'fork_400': frk[400], 'fork_420': frk[420], 'fork_450': frk[450], 'fork_600': frk[-1], 'fork_first_zero_t': zero}
    print(s, out[s])
ax[0].legend(fontsize=7); plt.tight_layout(); plt.savefig('efork.png', dpi=80); json.dump(out, open('efork.json', 'w'))
