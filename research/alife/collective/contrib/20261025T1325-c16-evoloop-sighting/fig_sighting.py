import numpy as np, json, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
COL = np.array([[0,0,0],[0,0,255],[255,0,0],[0,255,0],[255,255,0],[255,0,255],[255,255,255],[0,255,255],[255,128,0]])/255
tag = sys.argv[1]; times = [int(x) for x in sys.argv[2].split(',')]; out = sys.argv[3]
rec = json.load(open(tag + '.json'))
fig = plt.figure(figsize=(4 * len(times), 8.5))
for k, t in enumerate(times):
    ax = fig.add_subplot(2, len(times), k + 1); g = np.load(f'{tag}_g{t}.npy')
    ax.imshow(COL[g], interpolation='nearest'); ax.set_title(f't = {t}'); ax.axis('off')
ax = fig.add_subplot(2, 1, 2)
H = np.array([r['hist'][:16] for r in rec], float); tt = [r['t'] for r in rec]
im = ax.imshow(np.log10(1 + H.T), aspect='auto', origin='lower', extent=[tt[0]-500, tt[-1]+500, -0.5, 15.5], cmap='magma')
ax.set_xlabel('time step'); ax.set_ylabel('loop hole side (kind)'); ax.set_title('loops per hole side over time (log10(1+count)); founder side 11')
plt.colorbar(im, ax=ax, fraction=0.02)
plt.tight_layout(); plt.savefig(out, dpi=70)
