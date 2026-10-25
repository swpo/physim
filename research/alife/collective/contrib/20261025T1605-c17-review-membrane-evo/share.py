"""K2 biomass share (sum K2 / sum (K1 + K2)) over time for up and twin arms, from labkit frames.npz (channels K1, K2).
Prints the final share per seed and arm, a sign count, and writes share.png and share.json."""
import json, glob, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
seeds = sorted(int(p.split("seed")[1]) for p in glob.glob("up/seed*") if glob.glob(f"twin/seed{p.split('seed')[1]}/frames.npz") and glob.glob(p + "/frames.npz"))
out = {}
fig, ax = plt.subplots(2, 5, figsize=(13, 5), sharex=True, sharey=True)
for a, s in zip(ax.ravel(), seeds):
    out[s] = {}
    for arm, col in (("up", "tab:orange"), ("twin", "0.4")):
        R = np.load(f"{arm}/seed{s}/frames.npz")["render"].astype(float)
        k1, k2 = R[:, 0].sum((1, 2)), R[:, 1].sum((1, 2))
        sh = k2 / np.maximum(k1 + k2, 1e-9)
        out[s][arm] = {"final_share": round(float(sh[-1]), 3), "mean_last_quarter": round(float(sh[-len(sh) // 4:].mean()), 3), "final_K_total": round(float((k1 + k2)[-1]), 1)}
        a.plot(np.linspace(0, 40000, len(sh)) / 1000, sh, color=col, label=f"{arm} (b2={'1.3b' if arm == 'up' else 'b'})")
    a.set_title(f"seed {s}", fontsize=8)
ax[0, 0].legend(fontsize=7); fig.supxlabel("thousand steps"); fig.supylabel("K2 share of catalyst biomass")
fig.tight_layout(); fig.savefig("share.png", dpi=100)
hi = sum(out[s]["up"]["mean_last_quarter"] > out[s]["twin"]["mean_last_quarter"] for s in out)
json.dump(out, open("share.json", "w"), indent=1)
for s in out: print(s, out[s])
print("up > twin (mean share over the last quarter) on", hi, "of", len(out))
