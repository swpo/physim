import sys, json, os, importlib.util, time
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
spec = importlib.util.spec_from_file_location("w", sys.argv[1]); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
seed, T, out = int(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
os.makedirs(out, exist_ok=True)
s = w.init(seed, w.META["size"]); dt = w.P["dt"]
nsnap = 12; snaps = []; rec = []
nsteps = int(round(T / dt)); every = max(1, nsteps // 200); severy = nsteps // nsnap
t0 = time.time()
for i in range(nsteps + 1):
    if i % every == 0:
        c, d = w.polarity(s); da = s["dx"] ** 2
        hi = ((s["rho"] > 0.5) & (s["phi"] > 0.5)).sum() * da
        rec.append([s["t"], c[0], c[1], s["phi"].sum() * da, hi, w.rho_cyt(s), float(s["rho"][s["phi"] > 0.5].max()) if (s["phi"] > 0.5).any() else 0])
    if i % severy == 0:
        snaps.append((s["t"], s["phi"].copy(), (s["rho"] * (s["phi"] > 0.5)).copy()))
    if i < nsteps: s = w.step(s)
rec = np.array(rec)
L = w.P["L"]
# unwrapped displacement
dc = np.diff(rec[:, 1:3], axis=0); dc = (dc + L / 2) % L - L / 2
path = np.vstack([[0, 0], np.cumsum(dc, 0)])
np.savetxt(out + "/track.txt", np.column_stack([rec, path]), header="t cx cy area area_hi rho_cyt rho_max ux uy", fmt="%.5g")
fig, ax = plt.subplots(3, nsnap // 2 + 1, figsize=(2.2 * (nsnap // 2 + 1), 6.6))
for k, (t, ph, r) in enumerate(snaps[:nsnap]):
    a = ax[(k // (nsnap // 2)) , k % (nsnap // 2)]
    img = np.dstack([r / 1.2, ph * 0.6, ph * 0.6]).clip(0, 1)
    a.imshow(img, origin="lower"); a.set_title(f"t={t:.1f}", fontsize=8); a.axis("off")
for a in ax[:2, -1]: a.axis("off")
gs = ax[2]
for a in gs: a.remove()
a1 = fig.add_subplot(3, 3, 7); a1.plot(path[:, 0], path[:, 1]); a1.set_aspect("equal"); a1.set_title("path (unwrapped)", fontsize=8)
a2 = fig.add_subplot(3, 3, 8); a2.plot(rec[:, 0], rec[:, 3], label="area"); a2.plot(rec[:, 0], rec[:, 4], label="area rho>1/2"); a2.legend(fontsize=7); a2.set_xlabel("t")
sp = np.hypot(*np.gradient(path, rec[:, 0], axis=0).T)
a3 = fig.add_subplot(3, 3, 9); a3.plot(rec[:, 0], sp); a3.set_title("speed", fontsize=8); a3.set_xlabel("t")
fig.suptitle(f"{os.path.basename(sys.argv[1])} seed {seed} P={os.environ.get('WORLD_P','{}')}", fontsize=8)
fig.tight_layout(); fig.savefig(out + "/probe.png", dpi=80)
info = getattr(s, "get", lambda k: None)("cut_info") if isinstance(s, dict) else None
n = len(rec); q = rec[n // 2:]
print(json.dumps({"wall_s": round(time.time() - t0), "final_area": rec[-1, 3], "final_hi": rec[-1, 4], "rho_cyt": rec[-1, 5],
                  "mean_speed_2nd_half": float(sp[n // 2:].mean()), "disp": float(np.hypot(*path[-1])), "cut": s.get("cut_info")}))
