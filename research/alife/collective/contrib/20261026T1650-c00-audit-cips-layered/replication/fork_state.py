"""Fork arms from a saved state of the claim's world (same arm definitions as the claim's fork.py and c40's cut.py,
but starting from a state saved by wrapworld.py instead of re-running from t=0).
Arms: fed; fork (kF=0 everywhere); fork_d0 (kF=0 and d=0); fed_d0 (fuel kept, enzyme turnover d=0);
cut (kF=0 only in a disk of FR x nearest-neighbour distance around the most isolated body).
usage: python fork_state.py STATE.npz SEED OUTPREFIX T_SHORT T_LONG FR"""
import sys, os, json, copy, importlib.util
import numpy as np
from scipy import ndimage
sys.path.insert(0, "/home/user/physim/research/alife")
spec = importlib.util.spec_from_file_location("w", "/home/user/physim/research/alife/collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py")
w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
st, seed, out, tshort, tlong, FR = sys.argv[1], int(sys.argv[2]), sys.argv[3], float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6])
Z = np.load(st)
s = w.init(seed, w.META["size"]); H, W = s["shape"]
for k in "epFs": s[k] = Z[k].copy()
s["t"] = float(Z["t"]); tf = s["t"]


def bodies(e):
    E = np.pad(e, 24, mode="wrap"); lab, n = ndimage.label(E > 0.5, structure=np.ones((3, 3)))
    res = []
    for i in range(1, n + 1):
        b = lab == i; cy, cx = ndimage.center_of_mass(b)
        if 24 <= cy < 24 + H and 24 <= cx < 24 + W:
            res.append((cy - 24, cx - 24, int(b.sum())))
    return res


def pd(a, b):
    dy = abs(a[0] - b[0]); dy = min(dy, H - dy); dx = abs(a[1] - b[1]); dx = min(dx, W - dx); return (dy * dy + dx * dx) ** 0.5


bs = bodies(s["e"])
nn = [min(pd(c, d) for d in bs if d is not c) for c in bs]
i = int(np.argmax(nn)); tgt = bs[i]; R = max(14.0, FR * nn[i])
yy, xx = np.mgrid[0:H, 0:W]
dy = (yy - tgt[0] + H / 2) % H - H / 2; dx = (xx - tgt[1] + W / 2) % W - W / 2
disk = dy * dy + dx * dx <= R * R
arms = {"fed": ({}, tlong), "fork": ({"fork_t": tf}, tshort), "fork_d0": ({"fork_t": tf, "fork_d": 0.0}, tshort),
        "fed_d0": ({"d": 0.0}, tlong), "cut": ({"cut_t": tf, "cut_r": R, "cut_y": tgt[0], "cut_x": tgt[1]}, tlong)}
res, snaps = {}, {}
for name, (mod, ta) in arms.items():
    a = copy.deepcopy(s); a["par"] = dict(s["par"], **mod)
    log, sn, k = [], [], 0
    while a["t"] <= tf + ta + 1e-9:
        if k % 250 == 0:
            b = bodies(a["e"])
            inn = [x for x in b if pd(x, tgt) <= R]
            outb = [x for x in b if pd(x, tgt) > R]
            cat = a["par"]["kc"] * a["F"] * np.clip(a["e"], 0, None) ** a["par"]["n"] * (1 - a["p"])
            log.append({"t": round(a["t"] - tf, 1), "bodies": len(b), "areas": sorted(x[2] for x in b),
                        "body_area_px": int((a["e"] > 0.5).sum()), "mean_F": float(a["F"].mean()), "max_e": float(a["e"].max()),
                        "e_total": float(a["e"].sum()), "cat_body_share": float(cat[a["e"] > 0.5].sum() / max(cat.sum(), 1e-300)),
                        "target_px": int(((a["e"] > 0.5) & disk).sum()), "F_in_disk": float(a["F"][disk].mean()),
                        "bodies_outside_disk": len(outb), "outside_area": int(sum(x[2] for x in outb))})
        if k % 1000 == 0:
            sn.append((round(a["t"] - tf), a["e"].copy(), a["F"].copy()))
        w.step(a); k += 1
    res[name] = log; snaps[name] = sn
    print(name, log[0]["bodies"], log[0]["body_area_px"], "->", log[-1]["bodies"], log[-1]["body_area_px"],
          "target", log[0]["target_px"], "->", log[-1]["target_px"], "outside", log[0]["bodies_outside_disk"], "->", log[-1]["bodies_outside_disk"], flush=True)
json.dump({"seed": seed, "t_fork": tf, "target": tgt, "nn_dist": nn[i], "cut_radius": R, "arms": res}, open(out + ".json", "w"))
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
names = list(arms); nc = max(len(snaps[n]) for n in names)
fig, ax = plt.subplots(len(names) + 1, nc, figsize=(1.7 * nc, 1.8 * (len(names) + 1)), squeeze=False)
th = np.linspace(0, 2 * np.pi, 100)
for r, name in enumerate(names + ["cutF"]):
    nm = "cut" if name == "cutF" else name
    for j in range(nc):
        ax[r, j].axis("off")
        if j < len(snaps[nm]):
            t, e, F = snaps[nm][j]
            img = F if name == "cutF" else e
            ax[r, j].imshow(img, cmap="viridis" if name == "cutF" else "magma", vmin=0, vmax=1)
            if nm == "cut":
                ax[r, j].plot((tgt[1] + R * np.cos(th)) % W, (tgt[0] + R * np.sin(th)) % H, "w.", ms=0.5)
            ax[r, j].set_title(f"{name} t=+{t}", fontsize=6)
fig.suptitle(f"seed {seed}: arms from the state at t={tf:.0f} (e; last row: fuel F in the cut arm; dotted: cut disk r={R:.0f})", fontsize=7)
fig.tight_layout(); fig.savefig(out + ".png", dpi=75)
