"""Global fuel forks for the fuel-powered-turnover CIPS world (c48). Runs world.py (seed, WORLD_P) to T_FORK, then
branches: fed (unchanged), fork (kF=0 from T_FORK, fuel-dependent reactivation kept), fork_const (kF=0 and the
reactivation switched to the fuel-independent r*Fs*i at T_FORK, so the enzyme's re-making no longer needs fuel).
Logs the number of bodies (e>0.5, >=10 px), body area, mean F, total e and i every 25 t.
usage: python fork.py SEED T_FORK T_AFTER OUT"""
import sys, os, json, copy, importlib.util, numpy as np
from scipy import ndimage
seed, tf, ta, out = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
spec = importlib.util.spec_from_file_location("w", os.path.join(os.path.dirname(os.path.abspath(__file__)), "world.py"))
w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(seed, w.META["size"])
while s["t"] < tf - 1e-9: w.step(s)
def nb(e):
    lab, n = ndimage.label(e > 0.5); sz = ndimage.sum(np.ones_like(e), lab, range(1, n + 1)); return int((sz >= 10).sum())
q = s["par"]; body = s["e"] > 0.5
react = q["r"] * s["F"] * s["i"]; cat = q["kc"] * s["F"] * np.clip(s["e"], 0, None) ** q["n"] * (1 - s["p"]); inact = q["d"] * s["e"]
diag = {"t": s["t"], "body_area_frac": float(body.mean()), "F_body": float(s["F"][body].mean()), "F_bath": float(s["F"][~body].mean()),
        "i_body": float(s["i"][body].mean()), "i_bath": float(s["i"][~body].mean()),
        "react_share_in_bodies": float(react[body].sum() / react.sum()), "inact_share_in_bodies": float(inact[body].sum() / inact.sum()),
        "fuel_use_react_over_cat": float(q["y_r"] * react.sum() / (q["y"] * cat.sum())), "e_total_mean": float(s["e"].mean()), "i_total_mean": float(s["i"].mean())}
print(diag, flush=True)
arms = {"fed": {}, "fork": {"fork_t": tf}, "fork_const": {"fork_t": tf, "react_const_t": tf}}
res, snaps = {"diag_at_fork": diag}, {}
for name, mod in arms.items():
    a = copy.deepcopy(s); a["par"] = dict(s["par"], **mod); log = []; k = 0
    while a["t"] <= tf + ta + 1e-9:
        if k % 250 == 0:
            e = a["e"]; log.append({"t": round(a["t"], 1), "n_bodies": nb(e), "area": int((e > 0.5).sum()), "F": float(a["F"].mean()),
                                    "e_tot": float(e.mean()), "i_tot": float(a["i"].mean())})
        if k % 1000 == 0: snaps.setdefault(name, []).append((round(a["t"]), a["e"].copy()))
        w.step(a); k += 1
    res[name] = log; print(name, log[0], log[-1], flush=True)
json.dump(res, open(out + ".json", "w"), indent=0)
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
names = list(snaps); nc = len(snaps["fed"])
fig, ax = plt.subplots(len(names), nc, figsize=(1.8 * nc, 1.9 * len(names)))
for r, n in enumerate(names):
    for j in range(nc):
        t, e = snaps[n][j]; ax[r, j].imshow(e, cmap="magma", vmin=0, vmax=1); ax[r, j].axis("off"); ax[r, j].set_title(f"{n} t={t}", fontsize=7)
fig.suptitle(f"seed {seed}: global fuel fork at t={tf:.0f} (e shown)", fontsize=8)
fig.tight_layout(); fig.savefig(out + ".png", dpi=65)
