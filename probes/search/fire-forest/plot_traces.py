
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, sys
WD = "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest"
tags = sys.argv[1:]
fig, axes = plt.subplots(len(tags), 1, figsize=(12, 2*len(tags)), sharex=True)
axes = np.atleast_1d(axes)
for ax, tag in zip(axes, tags):
    mb = np.load(f"{WD}/logs/mB_{tag}.npy")
    t = np.arange(len(mb)) * 5
    ax.plot(t, mb, lw=0.7)
    ax.set_ylabel(tag, fontsize=8)
axes[-1].set_xlabel("tick")
fig.tight_layout()
fig.savefig(f"{WD}/logs/traces.png", dpi=100)
