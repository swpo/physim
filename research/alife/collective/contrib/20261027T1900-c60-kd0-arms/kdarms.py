"""kd=0 arms for the c52 digestion ecology (the c00 audit's deciding experiment), on the unchanged world.py.
usage: kdarms.py STATE.npz SEED ARM OUT.json [--T 3000]
ARM: ctrl | kdlocal | kdzero | kdlocal_chiF0 | kdzero_chiF0
kdlocal: kd (the digestion-product yield) is 0 in a disk that follows each target pair (tracked predator + the prey it
touches, re-centred every 50 t); eating (k2) is unchanged, so the prey is still consumed at the fed rate.
kdlocal_chiF0: as kdlocal and the written fuel-depletion taxis is also 0 in the same moving disks."""
import sys, os, json, argparse, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from arms_util import w, pdist, label_p, pcentroid, pick_targets
KEYS = ["pa", "pb", "p", "F", "w", "q"]

def dil(m, k=2):
    for _ in range(k): m = m | np.roll(m, 1, 0) | np.roll(m, -1, 0) | np.roll(m, 1, 1) | np.roll(m, -1, 1)
    return m

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("state"); ap.add_argument("seed", type=int); ap.add_argument("arm"); ap.add_argument("out")
    ap.add_argument("--T", type=float, default=3000); ap.add_argument("--every", type=float, default=50)
    a = ap.parse_args()
    s = w.init(a.seed, (128, 128)); d = np.load(a.state)
    for k in KEYS: s[k] = d[k].copy()
    s["t"] = float(d["t"]); s["par"] = dict(s["par"]); H, W = s["shape"]; dt = s["par"]["dt"]
    tg = pick_targets(s); arm = a.arm
    chimask = np.ones((H, W)); kdmap = np.full((H, W), float(s["par"]["kd"]))
    if arm in ("kdlocal", "kdlocal_chiF0"): s["par"]["kd"] = kdmap
    if arm == "kdzero": s["par"]["kd"] = 0.0
    if arm == "k2zero": s["par"]["k2"] = 0.0
    if arm == "kdzero_chiF0": s["par"]["kd"] = 0.0; s["par"]["chiF"] = 0.0
    if arm == "kdlocal_chiF0":
        _o = w.vf_flux_div; w.vf_flux_div = lambda c, f, chi: _o(c, f, chi * chimask)
    F = w.fields(s); Lb, nb = label_p(F[1])
    tmask = [Lb == c["pred"] for c in tg]; alive = [True] * len(tg)
    centers = [(c["cy"], c["cx"], c["R"]) for c in tg]
    rec = []; frames = []; fev = int(round(100.0 / dt)); ev = int(round(a.every / dt)); nsteps = int(round(a.T / dt)); t0 = time.time()
    for i in range(nsteps + 1):
        if i % ev == 0:
            F = w.fields(s); ca, cb = F[0], F[1]; La, na = label_p(ca); Lb, nb = label_p(cb)
            eat = s["par"]["k2"] * ca ** 2 * cb ** 2
            row = dict(t=s["t"], n_prey=na, n_pred=nb, eat_total=float(eat.sum()), q_total=float(F[4].sum()), targets=[])
            for k, c in enumerate(tg):
                tr = {}
                if alive[k]:
                    ov = Lb[tmask[k]]; ov = ov[ov > 0]
                    if ov.size == 0: alive[k] = False; tmask[k] = np.zeros_like(tmask[k])
                    else: tmask[k] = Lb == np.bincount(ov).argmax()
                tr["alive"] = alive[k]; tr["area"] = int(tmask[k].sum())
                if alive[k]:
                    m = tmask[k]; prey = [j for j in np.unique(La[dil(m)]) if j > 0]
                    pm = np.isin(La, prey) if prey else np.zeros_like(m)
                    cy, cx = pcentroid(m | pm); R = float(pdist(H, W, cy, cx)[m | pm].max()) + 4.0
                    centers[k] = (cy, cx, R)
                    tr.update(max_cb=float(cb[m].max()), n_prey_touch=len(prey), prey_area=int(pm.sum()),
                              eat_on_pred=float(eat[dil(m)].sum()), q_max=float(F[4][dil(m)].max()), cy=cy, cx=cx)
                row["targets"].append(tr)
            if arm in ("kdlocal", "kdlocal_chiF0"):
                kdmap[:] = float(w.P["kd"]); chimask[:] = 1.0
                for k in range(len(tg)):
                    if alive[k] or True:
                        cy, cx, R = centers[k]; dsk = pdist(H, W, cy, cx) <= R
                        kdmap[dsk] = 0.0; chimask[dsk] = 0.0
            rec.append(row)
        if i % fev == 0: frames.append(np.asarray(w.fields(s)[[0, 1, 4]], np.float32))
        if i < nsteps: s = w.step(s)
    json.dump(dict(arm=arm, seed=a.seed, t0=float(d["t"]), targets=tg, rows=rec, wall=time.time() - t0), open(a.out, "w"))
    np.savez_compressed(a.out.replace(".json", "_frames.npz"), render=np.array(frames))
    print(arm, a.seed, "done", time.time() - t0)

if __name__ == "__main__":
    main()
