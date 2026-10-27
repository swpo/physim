import sys, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
runs = sys.argv[2:]; frames = [20, 30, 50, 70, 99]
fig, ax = plt.subplots(len(runs), len(frames), figsize=(2 * len(frames), 2.1 * len(runs)), squeeze=False)
for r, run in enumerate(runs):
    R = np.load(f'comp/{run}/frames.npz')['render'].astype(float)
    for c, f in enumerate(frames):
        F = R[f]; ax[r, c].imshow(np.stack([F[1], F[0] * 0.8, F[5]], -1).clip(0, 1)); ax[r, c].axis('off')
        ax[r, c].set_title(f'{run} t={f*100}', fontsize=7)
plt.suptitle('green prey, red predator kind b, blue predator kind e', fontsize=8); plt.tight_layout(); plt.savefig(sys.argv[1], dpi=80)
