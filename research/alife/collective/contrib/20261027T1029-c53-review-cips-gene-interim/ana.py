"""c48: kind shares in the cips-gene selection runs. Per run: number of bodies of each kind (kind = the larger of
g1, g2; 'empty' if both < 0.5) every 100 t, washout removals by kind, swap events that hit a body.
usage: python ana.py OUTPNG run1.json run2.json ..."""
import sys, json, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
out, runs = sys.argv[1], sys.argv[2:]
fig, ax = plt.subplots(1, 2, figsize=(11, 3.6)); summ = {}
for r in runs:
    d = json.load(open(r)); t = np.array([x["t"] for x in d["log"]])
    def kinds(b):
        n1 = sum(1 for x in b if x[1] >= 0.5 and x[1] > x[2]); n2 = sum(1 for x in b if x[2] >= 0.5 and x[2] > x[1]); return n1, n2, len(b) - n1 - n2
    K = np.array([kinds(x["bodies"]) for x in d["log"]])
    share = K[:, 1] / np.maximum(1, K[:, 0] + K[:, 1])
    lab = r.split("/")[-1].replace(".json", "")
    ls = "-" if d["par"].get("a2", 0) != 0 else "--"
    ax[0].plot(t, share, ls, label=lab); ax[1].plot(t, K.sum(1), ls, label=lab)
    wl = d.get("wash_log", []); sl = d.get("swap_log", [])
    summ[lab] = {"t_end": int(t[-1]), "n_g1_g2_empty_end": K[-1].tolist(), "g2_share_end": float(share[-1]),
                 "g2_share_mean_last_5000t": float(share[t >= t[-1] - 5000].mean()),
                 "removals": len(wl), "removals_g2": sum(1 for x in wl if len(x) > 3 and x[3] > x[2]),
                 "swap_hits": len(sl), "swap_times": [x[0] for x in sl]}
ax[0].set_ylabel("share of g2 bodies"); ax[0].set_xlabel("t"); ax[1].set_ylabel("bodies"); ax[1].set_xlabel("t")
ax[0].legend(fontsize=7); fig.tight_layout(); fig.savefig(out, dpi=70)
print(json.dumps(summ, indent=1))
