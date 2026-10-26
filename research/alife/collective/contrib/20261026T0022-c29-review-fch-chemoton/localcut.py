"""(c29) L4c local ablation for c02's FCH chemoton: cut the precursor feed F in a disc around ONE vesicle
while every other vesicle keeps its feed, alongside an exact fed twin (deterministic after init).
Run seed to T0; label bodies (u+1 > 0.6, filled so a vesicle's lumen counts with it); pick the largest
body that carries catalyst; disc = its filled mask dilated by MARGIN px. Fork: twin (fed) and cut (F=0 in
the disc, P untouched at the fork). Follow every body by overlap; record the amphiphile mass sum(u+1) in its
filled mask (+2 px) and its catalyst mass, every 1 time unit, to T1.
usage: localcut.py seed T0 T1 out [MARGIN]"""
import sys, os, json, copy, importlib.util
import numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
spec = importlib.util.spec_from_file_location("w", os.path.join(os.path.dirname(os.path.abspath(__file__)), "world.py"))
w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
seed, T0, T1, out = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
MARGIN = int(sys.argv[5]) if len(sys.argv) > 5 else 12
os.makedirs(out, exist_ok=True)
H = Wd = w.META["size"][0]; dt = w.P["dt"]; n0 = int(round(T0 / dt)); n1 = int(round((T1 - T0) / dt)); every = int(round(1.0 / dt))


def plabel(m):
    lab, n = ndimage.label(m)
    for a, b in ((lab[0], lab[-1]), (lab[:, 0], lab[:, -1])):
        for x, y in set(zip(a.tolist(), b.tolist())):
            if x and y and x != y: lab[lab == y] = x
    return lab


def bodies(s):
    m = (s["u"] + 1) > 0.6
    # fill lumens (periodic-safe enough for bodies away from the edge: fill on a rolled copy)
    filled = ndimage.binary_fill_holes(np.pad(m, 1, mode="wrap"))[1:-1, 1:-1]
    return plabel(filled)


# custom step with a local feed mask: copy of world.step's P update with F replaced by F*feed
def step_local(s, feed):
    Fsave = w.P["F"]
    Pc = s["P"].copy()
    s = w.step(s)
    # undo the uniform feed term inside the cut and leave the rest: P_new -= dt*F*(1-P_old)*(1-feed)
    s["P"] -= dt * Fsave * (1 - Pc) * (1 - feed)
    return s


s = w.init(seed, (H, Wd))
for i in range(n0): s = w.step(s)
lab = bodies(s); ids = [k for k in np.unique(lab) if k]
info = []
for k in ids:
    m = lab == k
    info.append((int(m.sum()), float(s["K"][m].sum()), int(k)))
info.sort(reverse=True)
target = next(k for A, Km, k in info if Km > 1.0)
tmask = lab == target
disc = tmask.copy()
for _ in range(MARGIN):
    disc = disc | np.roll(disc, 1, 0) | np.roll(disc, -1, 0) | np.roll(disc, 1, 1) | np.roll(disc, -1, 1)
feed = np.ones((H, Wd)); feed[disc] = 0.0
print("seed", seed, "bodies (area, K, id)", info[:8], "target", target, "disc px", int(disc.sum()), flush=True)
arms = {"twin": copy.deepcopy(s), "cut": copy.deepcopy(s)}
cur = {a: {int(k): (lab == k) for k in ids} for a in arms}
rec = {a: {int(k): [] for k in ids} for a in arms}
snaps = {a: [] for a in arms}
for i in range(n1 + 1):
    if i % every == 0:
        for a, st in arms.items():
            L = bodies(st)
            for k in list(cur[a]):
                ov = L[cur[a][k]]; ov = ov[ov > 0]
                if len(ov) == 0:
                    rec[a][k].append([round(T0 + i * dt, 2), 0, 0.0, 0.0]); cur[a][k] = np.zeros((H, Wd), bool); continue
                mm = L == np.bincount(ov).argmax(); cur[a][k] = mm
                mg = ndimage.binary_dilation(mm, iterations=2)
                rec[a][k].append([round(T0 + i * dt, 2), int(mm.sum()), float((st["u"][mg] + 1).sum()), float(st["K"][mg].sum())])
        if i % (n1 // 5) == 0:
            for a in arms: snaps[a].append((T0 + i * dt, arms[a]["u"] + 1, arms[a]["P"].copy()))
    if i < n1:
        arms["twin"] = w.step(arms["twin"]); arms["cut"] = step_local(arms["cut"], feed)
res = {"seed": seed, "T0": T0, "T1": T1, "target": int(target), "margin": MARGIN, "disc_px": int(disc.sum()), "bodies": {}}
for k in ids:
    tw, cu = rec["twin"][k], rec["cut"][k]
    res["bodies"][int(k)] = {"target": int(k) == int(target), "area0": tw[0][1], "mass0": tw[0][2], "K0": tw[0][3],
                             "twin_end": tw[-1][1:], "cut_end": cu[-1][1:],
                             "twin_mass_ratio_end": tw[-1][2] / max(tw[0][2], 1e-9), "cut_mass_ratio_end": cu[-1][2] / max(cu[0][2], 1e-9),
                             "cut_lost_at": next((r[0] for r in cu if r[1] == 0), None), "twin_lost_at": next((r[0] for r in tw if r[1] == 0), None),
                             "track_twin": tw[::5], "track_cut": cu[::5]}
    b = res["bodies"][int(k)]
    print(k, "TARGET" if b["target"] else "", "area0", b["area0"], "mass twin x%.2f cut x%.2f" % (b["twin_mass_ratio_end"], b["cut_mass_ratio_end"]),
          "K end twin %.1f cut %.1f" % (b["twin_end"][2], b["cut_end"][2]), "lost twin", b["twin_lost_at"], "cut", b["cut_lost_at"], flush=True)
json.dump(res, open(f"{out}/result.json", "w"), indent=1)
fig, axs = plt.subplots(3, 6, figsize=(15, 7.5))
for r, a in enumerate(("twin", "cut")):
    for q in range(6):
        ax = axs[r, q]; ax.set_xticks([]); ax.set_yticks([])
        if q < len(snaps[a]):
            t, u1, Pc = snaps[a][q]; ax.imshow(u1, cmap="magma", vmin=0, vmax=2.2)
            ax.contour(disc, [0.5], colors="c", linewidths=0.6); ax.set_title(f"{a} t={t:.0f}", fontsize=8)
for k in ids:
    tw, cu = np.array(rec["twin"][k]), np.array(rec["cut"][k])
    style = dict(lw=2.2) if k == target else dict(lw=0.8)
    axs[2, 0].plot(tw[:, 0], tw[:, 2], "k", **style); axs[2, 0].plot(cu[:, 0], cu[:, 2], "r", **style)
    axs[2, 1].plot(tw[:, 0], tw[:, 3], "k", **style); axs[2, 1].plot(cu[:, 0], cu[:, 3], "r", **style)
axs[2, 0].set_title("amphiphile mass per body (thick = target; black twin, red cut)", fontsize=7)
axs[2, 1].set_title("catalyst K per body", fontsize=7)
t, _, Pc = snaps["cut"][-1]; axs[2, 2].imshow(Pc, cmap="viridis"); axs[2, 2].set_title(f"cut arm P at t={t:.0f}", fontsize=7)
for q in range(3, 6): axs[2, q].axis("off")
fig.suptitle(f"FCH chemoton seed {seed}: precursor feed cut only in the cyan disc around body {target} at t={T0:.0f}", fontsize=9)
fig.tight_layout(); fig.savefig(f"{out}/localcut.png", dpi=60)
