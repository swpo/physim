"""Branch a crawler at t_cut into an undamaged twin and a damaged arm; record both."""
import sys, json, os, copy, importlib.util
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
spec = importlib.util.spec_from_file_location("w", sys.argv[1]); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
seed, tcut, T, out = int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
os.makedirs(out, exist_ok=True)
P = w.P; dt = P["dt"]; L = P["L"]
s = w.init(seed, w.META["size"])
while s["t"] < tcut - 1e-9: s = w.step(s)
arms = {"twin": copy.deepcopy(s), "cut": w.cut(copy.deepcopy(s))}
arms["twin"]["rng"] = np.random.default_rng(seed + 1000); arms["cut"]["rng"] = np.random.default_rng(seed + 1000)
info = arms["cut"]["cut_info"]
nst = int(round((T - tcut) / dt)); every = max(1, nst // 300); tsn = np.linspace(0, nst, 9).astype(int)
rec = {k: [] for k in arms}; snaps = {k: [] for k in arms}
for i in range(nst + 1):
    for k, a in arms.items():
        if i % every == 0:
            da = a["dx"] ** 2; A = a["phi"].sum() * da
            hi = ((a["rho"] > 0.5) & (a["phi"] > 0.5)).sum() * da
            c, d = w.polarity(a) if A > 1e-3 else (np.zeros(2), np.zeros(2))
            rec[k].append([a["t"], c[0], c[1], A, hi, w.rho_cyt(a) if A > 1e-3 else 0])
        if i in tsn:
            c, _ = w.polarity(a) if a["phi"].sum() > 1 else (np.array([L / 2, L / 2]), 0)
            N = a["phi"].shape[0]; sh = (N // 2 - int(c[1] / a["dx"]), N // 2 - int(c[0] / a["dx"]))
            snaps[k].append((a["t"], np.roll(a["phi"], sh, (0, 1)), np.roll(a["rho"], sh, (0, 1))))
        if i < nst: arms[k] = w.step(a)
import pickle; pickle.dump({"rec": rec, "snaps": snaps, "info": info}, open(f"{out}/raw.pkl", "wb"))
res = {"cut_info": info, "seed": seed, "t_cut": tcut, "P": {k: v for k, v in P.items()}}
fig, ax = plt.subplots(3, 9, figsize=(18, 6.5))
for r, k in enumerate(["twin", "cut"]):
    R = np.array(rec[k]); dc = np.diff(R[:, 1:3], axis=0); dc = (dc + L / 2) % L - L / 2
    path = np.vstack([[0, 0], np.cumsum(dc, 0)]); tt = R[:, 0]
    sp = np.hypot(*np.gradient(path, tt, axis=0).T)
    np.savetxt(f"{out}/track_{k}.txt", np.column_stack([R, path, sp]), header="t cx cy area area_hi rho_cyt ux uy speed", fmt="%.5g")
    alive = R[:, 3] > 0.05
    # first time after the cut with a connected high patch again (area_hi > 0.05)
    reform = tt[(R[:, 4] > 0.05) & (tt > tcut + 0.05)]
    res["arm_" + k] = {"final_area": R[-1, 3], "final_hi": R[-1, 4], "min_hi_after_cut": float(R[1:, 4].min()),
              "t_extinct": float(tt[~alive][0]) if (~alive).any() else None,
              "speed_last_quarter": float(sp[-len(sp) // 4:].mean()), "disp": float(np.hypot(*path[-1])),
              "t_hi_back": float(reform[0]) if len(reform) and R[1:, 4].min() < 0.05 else None}
    for j, (t, ph, rh) in enumerate(snaps[k]):
        a = ax[r, j]; a.imshow(rh * (ph > 0.5), origin="lower", cmap="magma", vmin=0, vmax=1.2)
        a.contour(ph, [0.5], colors="c", linewidths=0.8); a.set_title(f"{k} t={t:.1f}", fontsize=8); a.set_xticks([]); a.set_yticks([])
for a in ax[2]: a.remove()
for col, (idx, lab) in enumerate([(3, "area"), (4, "polarized area (rho>1/2)"), (8, "speed")]):
    a = fig.add_subplot(3, 3, 7 + col)
    for k in ["twin", "cut"]:
        R = np.loadtxt(f"{out}/track_{k}.txt"); a.plot(R[:, 0], R[:, idx], label=k)
    a.axvline(tcut, color="k", lw=0.5); a.set_title(lab, fontsize=8); a.legend(fontsize=7); a.set_xlabel("t")
fig.suptitle(f"seed {seed}, cut {info['mode']} at t={tcut}: area frac {info['area_frac']:.2f}, protein lost {info['protein_lost_frac']:.2f}; P={os.environ.get('WORLD_P','{}')}", fontsize=8)
fig.tight_layout(); fig.savefig(f"{out}/cut.png", dpi=72)
json.dump(res, open(f"{out}/result.json", "w"), indent=1, default=float)
print(json.dumps({"info": info, "twin": res["arm_twin"], "cut": res["arm_cut"]}, default=float))
