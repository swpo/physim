"""K2 biomass share and K2 cell count vs time, up arm (b2 = 1.3 b) vs identical-event twin (b2 = b), evotrack.py outputs."""
import json, sys, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
d = sys.argv[1]; seeds = [24, 25, 26, 27]
fig, ax = plt.subplots(2, 4, figsize=(15, 6)); rows = []
for j, s in enumerate(seeds):
    for arm, col in (("up", "C1"), ("twin", "k")):
        r = json.load(open(f"{d}/{arm}_s{s}.json")); S = r["series"]; t = [x["t"] for x in S]
        ax[0, j].plot(t, [x["bio2"] / max(1e-9, x["bio1"] + x["bio2"]) for x in S], col, label=arm)
        ax[1, j].plot(t, [x["K2"] for x in S], col); ax[1, j].plot(t, [x["K1"] for x in S], col, ls=":")
        E = r["events"]; f = S[-1]
        rows.append(f"seed {s} {arm}: final K1/K2 cells {f['K1']}/{f['K2']}, K2 biomass share {f['bio2']/(f['bio1']+f['bio2']):.2f}; births K1/K2 {E['birth']['K1']}/{E['birth']['K2']}; deaths (other) {E['death']['K1']}/{E['death']['K2']}; disk deaths {E['death_disk']['K1']}/{E['death_disk']['K2']}; flips K1->K2/K2->K1 {E['flip']['K1->K2']}/{E['flip']['K2->K1']}; conversions {E['conversion']['K1->K2']}/{E['conversion']['K2->K1']}; first acquisitions {E['first_acq']}; off-kind daughters {E['offkind_daughters']}")
    ax[0, j].set_title(f"seed {s}: K2 biomass share", fontsize=9); ax[1, j].set_title("K2 cells (solid), K1 (dotted)", fontsize=9); ax[0, j].set_ylim(0, 1); ax[0, j].legend(fontsize=7)
plt.tight_layout(); plt.savefig(f"{d}/up_vs_twin.png", dpi=70)
open(f"{d}/summary.txt", "w").write("\n".join(rows) + "\n"); print("\n".join(rows))
