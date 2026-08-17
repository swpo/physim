
import json, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
SD = "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest/succession"
hyst = json.load(open(SD + "/hysteresis.json"))
hlow = json.load(open(SD + "/hysteresis_low.json"))
tup = json.load(open(SD + "/tipping_up.json"))
g3 = json.load(open(SD + "/g3_succession.json"))

fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
# hysteresis loop
gT_up = [r["gT"] for r in hyst] + [r["gT"] for r in tup]
T_up = [r["T_up"] for r in hyst] + [r["T_up"] for r in tup]
o = np.argsort(gT_up); gT_up = np.array(gT_up)[o]; T_up = np.array(T_up)[o]
gT_dn = [r["gT"] for r in hlow] + [r["gT"] for r in hyst]
T_dn = [r["T_dn"] for r in hlow] + [r["T_dn"] for r in hyst]
o = np.argsort(gT_dn); gT_dn = np.array(gT_dn)[o]; T_dn = np.array(T_dn)[o]
ax = axes[0]
ax.plot(gT_up, T_up, "o-", color="peru", label="savanna init (up branch)")
ax.plot(gT_dn, T_dn, "s-", color="forestgreen", label="forest init (down branch)")
ax.set_xscale("log")
ax.set_xlabel("tree growth rate gT (price)"); ax.set_ylabel("tree cover T (end)")
ax.set_title("L4 hysteresis: savanna-forest bistability\nwindow gT in [~2.5e-5, ~3.5e-4] (14x)")
ax.legend(fontsize=8)
# G3 response
ax = axes[1]
gs = [r["gT"] for r in g3]; Ts = [r["Tstar_med"] for r in g3]
lo = [min(r["Tstar_forest"]) for r in g3]; hi = [max(r["Tstar_forest"]) for r in g3]
ax.errorbar(gs, Ts, yerr=[np.array(Ts) - lo, np.array(hi) - Ts], fmt="o-",
            color="forestgreen", capsize=3)
ax.set_xscale("log")
ax.set_xlabel("tree growth rate gT (price)")
ax.set_ylabel("forest-branch equilibrium T*")
ax.set_title("G3: T* responds smoothly+monotonically to gT\n(3 seeds per point; mu, fire params fixed)")
fig.tight_layout()
fig.savefig(SD + "/strips/S1_hysteresis_G3.png", dpi=110)
print("saved")
