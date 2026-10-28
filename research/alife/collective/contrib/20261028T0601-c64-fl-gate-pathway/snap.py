import sys, os, json, copy, pickle, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import world as w
seed = int(sys.argv[1]); s0 = pickle.load(open(f'/tmp/s{seed}_t1000.pkl', 'rb'))
arms = [('fed, claim world', 'all', True), ('starved, gate all 10', 'all', False), ('starved, gate 9 (kernel 9 free)', [0,1,2,3,4,5,6,7,8], False),
        ('starved, gate 9 (kernel 3 free)', [0,1,2,4,5,6,7,8,9], False), ('starved, gate 7 (3,4,8 free)', [0,1,2,5,6,7,9], False), ('starved, gate 3 (3,4,8)', [3,4,8], False)]
fig, ax = plt.subplots(2, len(arms), figsize=(2.3 * len(arms), 4.8))
for j, (name, S, fed) in enumerate(arms):
    s = copy.deepcopy(s0); w.CFG['gate_k'] = S
    if not fed: s['q'][:] = 0; w.CFG['k_qy'] = 0.0
    for i in range(int(300 / w.CFG['dt'])):
        s = w.step(s)
        if i + 1 == int(100 / w.CFG['dt']): f100 = np.stack([s['A'].sum(0), s['B'].sum(0)])
    w.CFG['k_qy'] = 30.0
    for r, f in enumerate([f100, np.stack([s['A'].sum(0), s['B'].sum(0)])]):
        img = np.stack([np.clip(f[0] / 1.5, 0, 1), np.clip(f[1] / 1.5, 0, 1), np.zeros_like(f[0])], -1)
        a = ax[r, j]; a.imshow(img, interpolation='nearest'); a.set_xticks([]); a.set_yticks([])
        a.set_title(f"{name}\n+{100 if r == 0 else 300} t", fontsize=7)
    print(name, 'done', flush=True)
fig.suptitle(f'seed {seed}: t=1000 state, then 300 t; red prey, green predator; starved = q set 0 and yield 0 everywhere', fontsize=8)
plt.tight_layout(); plt.savefig(f'gates_s{seed}.png', dpi=80)
