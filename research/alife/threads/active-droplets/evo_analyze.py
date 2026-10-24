"""Analyze ad9 runs: mean kp(t) S vs N envelope, per-rung event tallies, Price-style split.
python evo_analyze.py runs out.png"""
import json, sys
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
KP = [0.0, 0.25, 0.5, 1.0, 1.5, 2.5, 4.0]
root, out = Path(sys.argv[1]), sys.argv[2]
fig, axs = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
rows = []
for j, anc in enumerate([5, 1]):
    ax = axs[j]
    for arm, col in (("N", "gray"), ("S", "C3")):
        curves = []
        for sd in range(3):
            f = root / f"{arm}_a{anc}_s{sd}" / "ledger.json"
            if not f.exists():
                continue
            d = json.load(open(f)); ser = d["series"]
            t = np.array([x[0] for x in ser]); z = np.array([x[2] for x in ser]); n = np.array([x[1] for x in ser])
            curves.append((t, z))
            if arm == "S":
                ax.plot(t, z, color=col, lw=1.6, label="S (selection)" if sd == 0 else None)
            L = d["ledger"]
            cnt = {k: 0 for k in ("birth", "death", "kill", "mut", "convert", "offkind", "nucleate")}
            dz_mut = dz_conv = 0.0
            nn = np.interp([e[1] for e in L], t, n) if len(t) else []
            for e, ni in zip(L, nn):
                cnt[e[0]] = cnt.get(e[0], 0) + 1
                if e[0] in ("mut", "convert"):
                    dz = (KP[e[3]] - KP[e[2]]) / max(ni, 1)
                    if e[0] == "mut":
                        dz_mut += dz
                    else:
                        dz_conv += dz
            zz = z[np.isfinite(z)]
            dtot = (zz[-1] - zz[0]) if len(zz) else float("nan")
            fin = ser[-1][3]
            rows.append((f"{arm}_a{anc}_s{sd}", cnt, round(dtot, 3), round(dz_mut, 3), round(dz_conv, 3),
                         round(dtot - dz_mut - dz_conv, 3), fin, round(float(zz[-1]), 3) if len(zz) else None))
        if arm == "N" and curves:
            tg = curves[0][0]
            Z = np.array([np.interp(tg, t, np.nan_to_num(z, nan=KP[anc])) for t, z in curves])
            ax.fill_between(tg, Z.min(0), Z.max(0), color="gray", alpha=0.35, label="N envelope (identical events, neutral)")
    ax.axhspan(0.5, 1.5, color="C2", alpha=0.12, label="landscape peak 0.5-1.5")
    ax.set_title(f"ancestor kp={KP[anc]}"); ax.set_xlabel("time"); ax.legend(fontsize=7)
axs[0].set_ylabel("mean kp over droplets (label)")
fig.tight_layout(); fig.savefig(out, dpi=85)
print("run | births deaths kills muts converts offkind nucleate | dz_total dz_mut dz_conv dz_between | final rungs | final mean kp")
for r in rows:
    c = r[1]
    print(r[0], "|", c["birth"], c["death"], c["kill"], c["mut"], c["convert"], c["offkind"], c["nucleate"], "|", r[2], r[3], r[4], r[5], "|", r[6], "|", r[7])
