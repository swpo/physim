import json, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
L = lambda f: json.load(open(f))
fig, ax = plt.subplots(1, 4, figsize=(18, 4))
for f, c, lab in [("pred", "C0", "with predators"), ("nopred", "C2", "no-predator twin"), ("food", "C3", "food removed at t=1500")]:
    for sd, ls in [(0, "-"), (1, "--")]:
        S = np.array(L(f"led/{f}_s{sd}.json")["series"])
        ax[0].plot(S[:, 0], S[:, 1], ls, color=c, lw=1, label=f"{lab} s{sd}")
        ax[1].plot(S[:, 0], S[:, 3], ls, color=c, lw=1)
ax[0].set_title("prey bodies"); ax[1].set_title("prey mass (sum of A+B)"); ax[0].legend(fontsize=7)
for f, c, lab in [("pred", "C1", "with prey"), ("preyrm", "C4", "prey removed at t=1500")]:
    for sd, ls in [(0, "-"), (1, "--")]:
        S = np.array(L(f"led/{f}_s{sd}.json")["series"])
        ax[2].plot(S[:, 0], S[:, 2], ls, color=c, lw=1, label=f"{lab} s{sd}")
ax[2].set_title("predator bodies"); ax[2].legend(fontsize=7)
for f, c, lab in [("pred_s0", "C0", "with predators"), ("nopred_s0", "C2", "no predators")]:
    d = L(f"led/{f}.json"); tr = d["tracks"]
    b = np.array([t[1] for t in tr]); e = np.array([t[2] for t in tr])
    ages = []
    for t in np.arange(1000, 2400, 50):
        al = (b <= t) & (e >= t); ages += list(t - b[al])
    ax[3].hist(ages, bins=np.logspace(0, 3.4, 30), histtype="step", density=True, color=c, label=f"{lab}: median {np.median(ages):.0f} t")
ax[3].set_xscale("log"); ax[3].axvline(100, ls=":", c="k"); ax[3].set_title("age of prey bodies alive at t=1000-2400\n(identity reset by fission or fusion with a >=25% piece)", fontsize=9)
ax[3].legend(fontsize=7); ax[3].set_xlabel("age (t)")
for a in ax[:3]: a.set_xlabel("t"); a.axvline(1500, ls=":", c="gray")
plt.tight_layout(); plt.savefig("ecology_summary.png", dpi=75)
