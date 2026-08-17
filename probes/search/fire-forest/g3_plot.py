
import json, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
WD = "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest"
rows = json.load(open(WD + "/g3_curve_w7.json"))
g = np.array([r["g"] for r in rows]); t = np.array([r["tau3_med"] for r in rows])
lo = [min(s["tau3"] for s in r["per_seed"] if s["tau3"]) for r in rows]
hi = [max(s["tau3"] for s in r["per_seed"] if s["tau3"]) for r in rows]
fig, ax = plt.subplots(figsize=(6, 4.2))
ax.errorbar(g, t, yerr=[t - np.array(lo), np.array(hi) - t], fmt="o-", capsize=3)
ax.set_xscale("log"); ax.set_yscale("log")
sl = np.polyfit(np.log(g), np.log(t), 1)
ax.plot(g, np.exp(np.polyval(sl, np.log(g))), "--", color="gray",
        label="tau3 ~ g^%.2f" % sl[0])
ax.set_xlabel("growth rate g (micro price)"); ax.set_ylabel("top clock tau3 (ticks)")
ax.set_title("G3 response: fire-return clock vs regrowth rate\n(absolute spark rate held FIXED)")
ax.legend(); fig.tight_layout()
fig.savefig(WD + "/strips/G3_response_curve.png", dpi=110)
print("saved, slope=%.3f" % sl[0])
