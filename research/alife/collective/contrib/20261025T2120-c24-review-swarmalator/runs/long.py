"""Long run + cluster census over time + strip of split events (particles coloured by phase, crop on the parent)."""
import sys, json, os, numpy as np
os.environ["WORLD_P"] = sys.argv[2]; tag = sys.argv[1]; T = float(sys.argv[3]); seed = int(sys.argv[4])
import importlib, ctrack; W = importlib.import_module(os.environ.get("SWW", "world"))
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
s = W.init(seed, None); dt = W.P["dt"]; every = int(round(1.0 / dt)); X = []; TH = []
for k in range(int(T / dt) + 1):
    if k % every == 0: X.append(s["x"].copy()); TH.append(s["th"].copy())
    s = W.step(s)
L = W.P["L"]; np.savez_compressed(f"{tag}.npz", X=np.array(X, np.float32), TH=np.array(TH, np.float32))
nb = 5; out = []
for b in range(nb):
    lo, hi = int(len(X) * b / nb), int(len(X) * (b + 1) / nb)
    r = ctrack.analyse(X[lo:hi], L); out.append((lo, hi, round(r["clusters_mean"], 1), round(r["size_mean"], 1), r["splits"], r["merges"]))
print(tag, sys.argv[2], "seed", seed, "census (t0,t1,clusters,size,splits,merges):", out)
r = ctrack.analyse(X, L); ev = [e for e in r["events"] if e[1] > len(X) // 5 and min(e[3]) >= 10]
rng = np.random.default_rng(1); sel = [ev[i] for i in sorted(rng.choice(len(ev), min(4, len(ev)), replace=False))] if ev else []
labs = {}
fig, ax = plt.subplots(max(len(sel), 1), 8, figsize=(16, 2.1 * max(len(sel), 1)), squeeze=False)
for rr, (_, t, n, ch) in enumerate(sel):
    lab = ctrack.clusters(X[t], L); sizes = np.bincount(lab[lab >= 0]); k = int(np.argmin(abs(sizes - n)))
    c = X[t][lab == k]; ang = 2 * np.pi * c / L; cen = (np.angle(np.exp(1j * ang).mean(0)) % (2 * np.pi)) * L / (2 * np.pi)
    for cc in range(8):
        f = min(max(t - 3 + cc * 2, 0), len(X) - 1); d = X[f] - cen; d -= L * np.round(d / L)
        ax[rr, cc].scatter(d[:, 0], d[:, 1], c=np.mod(TH[f], 2 * np.pi), cmap="hsv", s=4, vmin=0, vmax=2 * np.pi)
        ax[rr, cc].set_xlim(-12, 12); ax[rr, cc].set_ylim(-12, 12); ax[rr, cc].set_aspect(1); ax[rr, cc].set_xticks([]); ax[rr, cc].set_yticks([])
        ax[rr, cc].set_title(f"t={f}" + (f" split {n}->{ch}" if f == t + 1 else ""), fontsize=6)
fig.suptitle(f"{tag} seed {seed}: split events (crop 24x24 on the parent at its split time; colour = phase = heading)", fontsize=8); fig.tight_layout(); fig.savefig(f"{tag}_splits.png", dpi=70)
