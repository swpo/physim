"""Plot mu and neutral-tag trajectories from motile_trait run logs (JSON lines).
python mtplot.py OUT.png LOG [LOG ...]  (log names contain the kd value: mt6_<kd>_<seed>.log)"""
import sys, json, os, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(10, 3.6), sharey=True)
for f in sys.argv[2:]:
    rows = [json.loads(l) for l in open(f) if l.startswith("{")]
    kd = os.path.basename(f).split("_")[1]
    a = ax[0] if float(kd) == 0 else ax[1]
    t = [r["t"] for r in rows]
    a.plot(t, [r["mu"] for r in rows], color="tab:red", lw=1.4)
    a.plot(t, [r["tag"] for r in rows], color="0.5", lw=1.0, ls="--")
for a, ttl in zip(ax, ("no toxin (kd=0)", "toxic waste (kd=0.02)")):
    a.set_title(ttl); a.set_xlabel("time"); a.axhline(1.5, color="k", lw=0.5)
ax[0].set_ylabel("population mean trait")
ax[0].plot([], [], color="tab:red", label="phoretic mobility mu"); ax[0].plot([], [], color="0.5", ls="--", label="neutral tag (same mutation)")
ax[0].legend(fontsize=8)
fig.tight_layout(); fig.savefig(sys.argv[1], dpi=80)
