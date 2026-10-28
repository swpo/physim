import json, numpy as np
from scipy import ndimage
D = "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/"
# (1) recompute energy-score ratios from the saved ensembles (independent implementation)
def es(F, y):
    return np.mean(np.linalg.norm(F - y, axis=1)) - 0.5 * np.mean(np.linalg.norm(F[:, None] - F[None], axis=2))
for tag, arms in (("B0.003", ["adv0", "fork", "dthalf"]), ("B0.01", ["adv0", "fork"])):
    E = {a: np.load(D + f"out/ens_s0_{tag}_{a}.npy") for a in ["native", "truth"] + arms}
    nat = E["native"]; sc = nat.reshape(-1, nat.shape[2]).std(0) + 1e-6
    for w in (30, 100, 300):
        nt = w // 2
        Z = {a: (X[:, :nt] / sc).reshape(8, -1) for a, X in E.items()}
        base = np.mean([es(Z["native"], y) for y in Z["truth"]])
        print(tag, w, {a: round(np.mean([es(Z["native"], y) for y in Z[a]]) / base, 2) for a in arms})
    # (2) when the probed vortex leaves device0: centre node (index 6) om below 0.06
    for a in ("native", "truth", "dthalf") if "dthalf" in arms else ("native", "truth"):
        X = E[a][:, :, 6]
        tl = [int((np.argmax(x < 0.06) + 1) * 2) if (x < 0.06).any() else None for x in X]
        print(tag, a, "dev0 centre om < 0.06 first at t =", tl)
# (3) body count on a smoothed signed field (sigma 2 px), late half of rendered frames
def count(om, thr=0.06, amin=20):
    k = 0; peaks = []
    for sgn in (1, -1):
        m = sgn * om > thr
        lab, n = ndimage.label(np.tile(m, (3, 3)), structure=np.ones((3, 3)))
        big = np.tile(sgn * om, (3, 3))
        for i, sl in enumerate(ndimage.find_objects(lab)):
            if 128 <= sl[0].start < 256 and 128 <= sl[1].start < 256:
                mk = lab[sl] == i + 1
                if mk.sum() >= amin:
                    k += 1; peaks.append(big[sl][mk].max())
    return k, (np.median(peaks) if peaks else 0.0)
for p in ["A0_s0", "B0.003_s0", "B0.01_s0", "B0.02_s0", "B0.03_s0", "A0.03_s0", "B0.1_s0"]:
    r = np.load(D + f"packs/{p}/frames.npz")["render"].astype(np.float64)
    late = r[len(r) // 2:, 2]
    res = [count(ndimage.gaussian_filter(np.arctanh(np.clip(f, -0.999, 0.999)), 2.0, mode="wrap")) for f in late]
    print(p, "smoothed(sigma2) bodies >=20px: mean", round(np.mean([x[0] for x in res]), 1), "median peak", round(float(np.median([x[1] for x in res])), 3))
