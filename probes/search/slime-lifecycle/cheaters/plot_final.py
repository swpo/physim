
import sys, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

cb = "/Users/spoho/Documents/prime/test/physim/probes/search/slime-lifecycle/cheaters"
panels = [
    ("M2hi_s0", "tragedy: lam=0.002 (c* -> 0.15)"),
    ("R_jit1", "polymorphism: jittered canonical (c* ~ 0.37)"),
    ("T_mid_hi", "bistable hold: hi-init lam=0.002 mu=0.03 (c* ~ 0.93)"),
    ("glob_nobn", "no assortment (global dispersal): collapse at lam=0.002"),
]
fig, axes = plt.subplots(len(panels), 1, figsize=(9, 2.2*len(panels)), sharex=False)
for ax, (tag, title) in zip(axes, panels):
    d = np.load("%s/series_%s.npz" % (cb, tag))
    t = d["t"]/1000.0
    ax.plot(t, d["cmean"], "b-", lw=1.2, label="<c>")
    ax.fill_between(t, d["cmean"]-d["csd"], d["cmean"]+d["csd"], color="b", alpha=0.15)
    ax.plot(t, d["aggm"], "r-", lw=0.5, alpha=0.5, label="aggm (L3)")
    ax.set_ylim(-0.02, 1.02); ax.set_title(title, fontsize=9)
    ax.set_ylabel("<c>, aggm")
    if ax is axes[0]: ax.legend(fontsize=7, loc="upper right")
axes[-1].set_xlabel("kiloticks")
fig.tight_layout()
fig.savefig("%s/strips/L4_panels.png" % cb, dpi=110)
print("saved L4_panels.png")

# G3 curves figure
fig2, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.2))
lam = [0.002, 0.003, 0.004, 0.008]
th_med = [27725, 9850, 8650, 4200]
th_all = {0.002: [26600, 28850, 37600, 10900], 0.003: [20950, 8250, 9850],
          0.004: [10850, 8650, 8650], 0.008: [4200, 6450, 3650]}
for l, ths in th_all.items():
    a1.plot([l]*len(ths), ths, "k.", alpha=0.4, ms=5)
a1.plot(lam, th_med, "ro-", lw=1.5)
a1.set_xscale("log"); a1.set_yscale("log")
a1.set_xlabel("signal cost lam_c"); a1.set_ylabel("collapse half-time t_half")
a1.set_title("G3a: tragedy speed vs cost (selection regime)", fontsize=9)
mu = [0.001, 0.003, 0.01, 0.03, 0.1]
sd_med = [0.0028, 0.0048, 0.0254, 0.0345, 0.0452]
sd_all = {0.001: [0.0027,0.0028,0.0036], 0.003: [0.0048,0.0519,0.0048],
          0.01: [0.0254,0.0182,0.0631], 0.03: [0.0345,0.0590,0.0205],
          0.1: [0.0498,0.0452,0.0376]}
for m, sds in sd_all.items():
    a2.plot([m]*len(sds), sds, "k.", alpha=0.4, ms=5)
a2.plot(mu, sd_med, "bo-", lw=1.5)
a2.set_xscale("log"); a2.set_yscale("log")
a2.set_xlabel("mutation size mu"); a2.set_ylabel("equilibrium sd(c)*")
a2.set_title("G3b: trait variance vs mutation (balance)", fontsize=9)
fig2.tight_layout()
fig2.savefig("%s/strips/G3_curves.png" % cb, dpi=110)
print("saved G3_curves.png")
