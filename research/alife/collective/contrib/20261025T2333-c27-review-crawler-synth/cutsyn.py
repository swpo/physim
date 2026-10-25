"""Branch at t_cut into an undamaged twin and a cut arm (the crawler's cut()), run both to T; record area,
polarized area, protein total and speed. usage: cutsyn.py seed tcut T out"""
import sys, os, json, copy, importlib.util, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("ws", os.path.join(here, "world.py")); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
seed, tcut, T, out = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]; os.makedirs(out, exist_ok=True)
dt = w.P["dt"]; L = w.P["L"]
s = w.init(seed, w.META["size"])
while s["t"] < tcut - 1e-9: s = w.step(s)
arms = {"twin": copy.deepcopy(s), "cut": w.cut(copy.deepcopy(s))}
for a in arms.values(): a["rng"] = np.random.default_rng(seed + 1000)
info = arms["cut"]["cut_info"]; nst = int(round((T - tcut) / dt)); every = max(1, nst // 300); rec = {k: [] for k in arms}; snaps = {k: [] for k in arms}
tsn = np.linspace(0, nst, 8).astype(int)
for i in range(nst + 1):
    for k, a in arms.items():
        if i % every == 0:
            da = a["dx"] ** 2; A = a["phi"].sum() * da
            c, d = w.polarity(a) if A > 1e-3 else (np.zeros(2), np.zeros(2))
            Ntot = (a["phi"] * (a["rho"] + a["cyt"])).sum() * da
            rec[k].append([a["t"], c[0], c[1], A, ((a["rho"] > 0.5) & (a["phi"] > 0.5)).sum() * da, Ntot, float(np.hypot(*d)), float(a["S"].mean())])
        if i in tsn:
            c, _ = w.polarity(a) if a["phi"].sum() > 1 else (np.array([L / 2, L / 2]), 0)
            N = a["phi"].shape[0]; sh = (N // 2 - int(c[1] / a["dx"]), N // 2 - int(c[0] / a["dx"]))
            snaps[k].append((a["t"], np.roll(a["phi"], sh, (0, 1)), np.roll(a["rho"], sh, (0, 1))))
        if i < nst: arms[k] = w.step(a)
res = {"cut_info": info, "Q": w.Q}
fig, ax = plt.subplots(3, 8, figsize=(17, 6.5))
for r, k in enumerate(["twin", "cut"]):
    R = np.array(rec[k]); dc = (np.diff(R[:, 1:3], axis=0) + L / 2) % L - L / 2; path = np.vstack([[0, 0], np.cumsum(dc, 0)])
    sp = np.hypot(*np.gradient(path, R[:, 0], axis=0).T); np.savetxt(f"{out}/track_{k}.txt", np.column_stack([R, sp]), header="t cx cy area area_hi protein |d| Smean speed", fmt="%.5g")
    res[k] = {"area_end": R[-1, 3], "protein_end": R[-1, 5], "speed_last_quarter": float(sp[-len(sp) // 4:].mean()), "min_area": float(R[:, 3].min())}
    for j, (t, ph, rh) in enumerate(snaps[k]):
        a = ax[r, j]; a.imshow(rh * (ph > 0.5), origin="lower", cmap="magma", vmin=0, vmax=1.2); a.contour(ph, [0.5], colors="c", linewidths=0.8); a.set_title(f"{k} t={t:.1f}", fontsize=8); a.set_xticks([]); a.set_yticks([])
for a in ax[2]: a.remove()
for col, (idx, lab) in enumerate([(3, "area"), (5, "protein total"), (8, "speed")]):
    a = fig.add_subplot(3, 3, 7 + col)
    for k in ["twin", "cut"]:
        R = np.loadtxt(f"{out}/track_{k}.txt"); a.plot(R[:, 0], R[:, idx], label=k)
    a.axvline(tcut, color="k", lw=0.5); a.set_title(lab, fontsize=8); a.legend(fontsize=7); a.set_xlabel("t")
fig.suptitle(f"seed {seed}, cut {info['mode']} at t={tcut}: area frac {info['area_frac']:.2f}, protein lost {info['protein_lost_frac']:.2f}; {os.environ.get('WORLD_P','{}')}", fontsize=8)
fig.tight_layout(); fig.savefig(f"{out}/cut.png", dpi=72); json.dump(res, open(f"{out}/result.json", "w"), indent=1, default=float)
print(json.dumps(res, default=float))
