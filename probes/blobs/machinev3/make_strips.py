import json, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(HERE, "strips")

# 1) tow lock strip: t_mim_06 (single-cargo blade tow)
d = np.load(os.path.join(S, "t_mim_06.npz"))
fig, axs = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
axs[0].plot(d["t"], d["xe"], label="engine x (unwrapped)")
axs[0].plot(d["t"], d["xc"], label="cargo x")
axs[0].legend(); axs[0].set_ylabel("x [px]")
axs[0].set_title("V3-0 tow lock: mimic eta=0.6, drag=131px, c_lock=0.199")
axs[1].plot(d["t"], d["sep"]); axs[1].set_ylabel("sep [px]"); axs[1].set_xlabel("t [tu]")
axs[1].axhline(4.27, ls="--", c="gray")
fig.savefig(os.path.join(S, "v30_tow_lock.png"), dpi=90, bbox_inches="tight")
plt.close(fig)

# 2) release strip: d_mim06_n1_eta0
d = np.load(os.path.join(S, "d_mim06_n1_eta0.npz"))
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(d["t1"], d["xc1"] % 96, label="cargo x (phase1 tow, mod L)")
ax.plot(d["t1"][-1] + d["t2"], d["xc2"] % 96, label="cargo x (phase2 released)")
ax.plot(d["t1"], d["xe1"] % 96, ".", ms=2, alpha=0.4, label="engine x mod L")
ax.plot(d["t1"][-1] + d["t2"], d["xe2"] % 96, ".", ms=2, alpha=0.4)
ax.axvline(d["t1"][-1], c="k", ls=":", label="coupling cut")
ax.legend(fontsize=7); ax.set_xlabel("t [tu]"); ax.set_ylabel("x mod 96 [px]")
ax.set_title("V3-0 release: eta->0 mid-run parks cargo instantly (drift 7e-15px)")
fig.savefig(os.path.join(S, "v30_release_eta0.png"), dpi=90, bbox_inches="tight")
plt.close(fig)

# 3) assembly final fields
for nm in ("asm3_det_a", "asm3_det_b"):
    p = os.path.join(S, nm + "_final.npz")
    if not os.path.exists(p):
        continue
    d = np.load(p)
    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
    for ax, k, tt in zip(axs, ("u_e", "u_c"), ("engine u", "cargo u")):
        im = ax.imshow(d[k], origin="lower", cmap="magma", extent=[0, 96, 0, 96])
        ax.set_title(f"{nm}: {tt}")
        fig.colorbar(im, ax=ax, shrink=0.75)
    fig.savefig(os.path.join(S, nm + "_final.png"), dpi=90, bbox_inches="tight")
    plt.close(fig)
print("strips done")
