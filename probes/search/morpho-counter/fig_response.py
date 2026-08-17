
import json
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

g3 = json.load(open("results_g3final.json"))
sig = json.load(open("results_sigma_staircase.json"))
fig, axes = plt.subplots(1, 3, figsize=(13, 3.6))
e = [r["eps"] for r in g3["eps_curve"]]; T = [r["period"] for r in g3["eps_curve"]]
axes[0].loglog(e, T, "o-")
xx = np.array(e); axes[0].loglog(xx, 3.8 / xx, "k--", lw=0.8, label="T = 3.8/eps")
axes[0].set_xlabel("eps (C drive gain)"); axes[0].set_ylabel("counter period T")
axes[0].legend(); axes[0].set_title("G3a: T(eps), monotone, T ~ 1/eps")
k = [r["kappa"] for r in g3["kappa_curve"]]; d = [r["duty"] for r in g3["kappa_curve"]]
axes[1].plot(k, d, "s-")
axes[1].set_xlabel("kappa (setpoint position)"); axes[1].set_ylabel("duty = dwell6/(dwell5+dwell6)")
axes[1].set_title("G3b: duty(kappa), monotone")
s = [r["sigma"] for r in sig]; cj = [r["C_jump_5to6"] for r in sig]
pred = [r["pred_exponent"] for r in sig]
axes[2].plot(s, cj, "d-", label="C_jump(5->6)")
axes[2].plot(s, pred, "x--", label="C_jump^sigma (collapse)")
axes[2].set_xlabel("sigma (wavelength-control exponent)")
axes[2].set_ylabel("C at 5->6 up-jump")
axes[2].legend(); axes[2].set_title("G3c: staircase position(sigma)")
for ax in axes: ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig("strips/response_curves.png", dpi=110)
print("saved response curves")
