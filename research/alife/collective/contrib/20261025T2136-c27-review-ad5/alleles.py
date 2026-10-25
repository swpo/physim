"""(c27) Droplets per dominant allele over time from labkit frames.npz (render frames), world vs neutral twin.
Droplet = 8-connected component of phi > 0 (periodic merge ignored; >= 12 px); allele = argmax of summed a_i in it."""
import sys, json, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
runs = sys.argv[1:]
fig, axs = plt.subplots(1, len(runs), figsize=(4.5 * len(runs), 3.4), squeeze=False)
out = {}
for ax, r in zip(axs[0], runs):
    z = np.load(r + "/frames.npz"); F = z["render"].astype(float); fr = z["render_f"]
    ser = []
    for i in range(len(F)):
        lab, n = ndimage.label(F[i, 0] > 0, structure=np.ones((3, 3)))
        cnt = [0, 0, 0, 0]
        for k in range(1, n + 1):
            m = lab == k
            if m.sum() < 12: continue
            cnt[int(np.argmax([F[i, 2 + j][m].sum() for j in range(4)]))] += 1
        ser.append(cnt)
    S = np.array(ser); t = fr * 100.0  # 200 steps x dt 0.5 per frame
    for j in range(4): ax.plot(t, S[:, j], label=f"allele {j} (k={[0.10,0.12,0.14,0.16][j] if 'neutral' not in r else 0.13})")
    ax.set_title(r, fontsize=8); ax.legend(fontsize=6); ax.set_xlabel("t")
    out[r] = {"t": t[::12].tolist(), "droplets_per_allele": S[::12].tolist(), "final": S[-1].tolist()}
    print(r, "final droplets per allele", S[-1].tolist(), "max", S.max(0).tolist())
fig.tight_layout(); fig.savefig("alleles_c27.png", dpi=70)
json.dump(out, open("alleles_c27.json", "w"))
