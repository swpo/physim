import numpy as np, json, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from swarm import step, random_recipe
seed0, k, N, T, out, box = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], float(sys.argv[6])
rng = np.random.default_rng(seed0 * 1000 + k); rec = random_recipe(rng, 3)
if len(sys.argv) > 7: rng = np.random.default_rng(int(sys.argv[7]))
sp = np.repeat(np.arange(3), N // 3); x = rng.uniform(0, box, (N, 2)); v = rng.uniform(-1, 1, (N, 2))
cols = np.array(['tab:red', 'tab:blue', 'tab:green'])
snaps = np.linspace(0, T, 8).astype(int); fig, ax = plt.subplots(1, 8, figsize=(24, 3.3)); j = 0
for t in range(T + 1):
    if t == snaps[j]:
        a = ax[j]; a.scatter(x[:, 0], x[:, 1], c=cols[sp], s=3); a.set_xlim(0, box); a.set_ylim(0, box); a.set_aspect('equal'); a.set_xticks([]); a.set_yticks([]); a.set_title(f't={t}', fontsize=8); j += 1
        if j == len(snaps): break
    x, v = step(x, v, sp, rec, box, rng)
fig.suptitle(f'swarm chemistry 3-species recipe {seed0}/{k}: ' + json.dumps(rec.round(2).tolist()), fontsize=7)
plt.tight_layout(); plt.savefig(out, dpi=60)
