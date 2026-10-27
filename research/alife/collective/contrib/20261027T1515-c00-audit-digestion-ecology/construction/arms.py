"""Audit arms from a saved state of the claimed c52 world (construction lens).
usage: arms.py STATE.npz SEED ARM OUT.json [--T 3000] [--every 50] [--targets targets.json]
ARM: ctrl | k2local | k2zero | chiF0 | preyrm | k2local_chiF0
The world is the claim's world.py, imported unchanged (world_dump.w); arms change only s['par'] entries
(k2 becomes a per-pixel map for k2local) or, for preyrm, delete the prey body under each target predator once.
Targets (predator bodies chosen at the fork time) come from targets.json (made by pick_targets in this file)."""
import sys, os, json, argparse, time
sys.path.insert(0, '/home/user/physim/research/alife'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy import ndimage
import world_dump as WD
w = WD.w

def load(state, seed, size=(128, 128)):
    s = w.init(seed, size); d = np.load(state)
    for k in WD.KEYS: s[k] = d[k].copy()
    s["t"] = float(d["t"]); s["par"] = dict(s["par"]); return s

def pdist(H, W, cy, cx):
    yy, xx = np.mgrid[0:H, 0:W]
    dy = (yy - cy + H / 2) % H - H / 2; dx = (xx - cx + W / 2) % W - W / 2
    return np.sqrt(dy * dy + dx * dx)

def label_p(x, th=0.5, amin=4):
    """periodic connected components of x > th with area >= amin"""
    L, n = ndimage.label(x > th)
    H, W = x.shape
    # merge labels across the periodic boundary
    par = list(range(n + 1))
    def f(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for a, b in list(zip(L[0], L[-1])) + list(zip(L[:, 0], L[:, -1])):
        if a and b: par[f(a)] = f(b)
    lut = np.array([f(i) for i in range(n + 1)]); L = lut[L]
    ids, L = np.unique(L, return_inverse=True); L = L.reshape(x.shape)
    if ids[0] != 0: L = L + 1
    a = np.bincount(L.ravel())
    small = np.where(a < amin)[0]; small = small[small > 0]
    L[np.isin(L, small)] = 0
    ids, L = np.unique(L, return_inverse=True); L = L.reshape(x.shape)
    return L, int(L.max())

def pcentroid(mask):
    H, W = mask.shape; ys, xs = np.nonzero(mask)
    ay = np.angle(np.exp(2j * np.pi * ys / H).mean()) * H / (2 * np.pi) % H
    ax = np.angle(np.exp(2j * np.pi * xs / W).mean()) * W / (2 * np.pi) % W
    return float(ay), float(ax)

def pick_targets(s, n=3, out=None):
    F = w.fields(s); ca, cb = F[0], F[1]
    Lb, nb = label_p(cb); La, na = label_p(ca)
    H, W = cb.shape
    cand = []
    for i in range(1, nb + 1):
        m = Lb == i; a = int(m.sum())
        if a < 10: continue
        near = ndimage.binary_dilation(m, iterations=2, mask=None)
        # periodic dilation: roll-based
        near = m.copy()
        for _ in range(2):
            near = near | np.roll(near, 1, 0) | np.roll(near, -1, 0) | np.roll(near, 1, 1) | np.roll(near, -1, 1)
        prey = [j for j in np.unique(La[near]) if j > 0]
        if len(prey) != 1: continue
        pm = La == prey[0]
        cy, cx = pcentroid(m | pm)
        R = float(pdist(H, W, cy, cx)[m | pm].max()) + 2.0
        cand.append(dict(pred=i, area=a, prey_area=int(pm.sum()), cy=cy, cx=cx, R=R, pcy=pcentroid(m)[0], pcx=pcentroid(m)[1]))
    med = np.median([c["area"] for c in cand])
    for c in cand:
        d4 = pdist(H, W, c["cy"], c["cx"]) <= c["R"] + 4
        c["_coll"] = int(len([j for j in np.unique(Lb[d4]) if j > 0 and j != c["pred"]]))
    cand.sort(key=lambda c: (c["_coll"] > 0, abs(c["area"] - med)))
    chosen = []
    for c in cand:
        if all(pdist(H, W, d["cy"], d["cx"])[int(round(c["cy"])) % H, int(round(c["cx"])) % W] > 40 for d in chosen):
            chosen.append(c)
        if len(chosen) == n: break
    # other predator bodies inside any target disk (collateral)
    for c in chosen:
        disk = pdist(H, W, c["cy"], c["cx"]) <= c["R"]
        c["other_preds_in_disk"] = int(len([j for j in np.unique(Lb[disk]) if j > 0 and j != c["pred"]]))
        disk4 = pdist(H, W, c["cy"], c["cx"]) <= c["R"] + 4
        c["other_preds_in_disk_R4"] = int(len([j for j in np.unique(Lb[disk4]) if j > 0 and j != c["pred"]]))
        c["other_prey_in_disk_R4"] = int(len([j for j in np.unique(La[disk4]) if j > 0]))
    if out: json.dump(dict(t=s["t"], n_pred=nb, n_prey=na, targets=chosen), open(out, "w"), indent=1)
    return chosen

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("state"); ap.add_argument("seed", type=int); ap.add_argument("arm"); ap.add_argument("out")
    ap.add_argument("--T", type=float, default=3000); ap.add_argument("--every", type=float, default=50); ap.add_argument("--targets", default=None)
    ap.add_argument("--snaps", type=float, nargs="*", default=[0, 200, 500, 1000, 2000, 3000])
    a = ap.parse_args()
    s = load(a.state, a.seed); H, W = s["shape"]; dt = s["par"]["dt"]; t0 = s["t"]
    tg = json.load(open(a.targets))["targets"] if a.targets else pick_targets(s)
    KPAD = float(os.environ.get("KPAD", "4"))
    disks = [pdist(H, W, c["cy"], c["cx"]) <= c["R"] + KPAD for c in tg]
    regions = [pdist(H, W, c["cy"], c["cx"]) <= c["R"] + 6 for c in tg]
    far = ~np.any([pdist(H, W, c["cy"], c["cx"]) <= c["R"] + 16 for c in tg], axis=0)
    arm = a.arm
    if arm in ("k2local", "k2local_chiF0"):
        k2map = np.full((H, W), float(s["par"]["k2"]))
        for d in disks: k2map[d] = 0.0
        s["par"]["k2"] = k2map
    if arm in ("k2local_taxoff", "taxoff_local"):
        # the written fuel-depletion taxis switched off inside the same disks only: world.py's vf_flux_div is called
        # with chi = chiF (scalar); the wrapper multiplies chi by a 0/1 map (0 in the disks), all else unchanged
        chimask = np.ones((H, W))
        for d in disks: chimask[d] = 0.0
        _orig = w.vf_flux_div
        w.vf_flux_div = lambda c, f, chi, _o=_orig, _m=chimask: _o(c, f, chi * _m)
    if arm == "k2local_taxoff":
        k2map = np.full((H, W), float(s["par"]["k2"]))
        for d in disks: k2map[d] = 0.0
        s["par"]["k2"] = k2map
    if arm == "k2zero": s["par"]["k2"] = 0.0
    if arm in ("chiF0", "k2local_chiF0"): s["par"]["chiF"] = 0.0
    if arm == "preyrm":
        F = w.fields(s); La, na = label_p(F[0]); Lb, nb = label_p(F[1])
        for c in tg:
            m = Lb == c["pred"]; near = m.copy()
            for _ in range(2): near = near | np.roll(near, 1, 0) | np.roll(near, -1, 0) | np.roll(near, 1, 1) | np.roll(near, -1, 1)
            for j in [j for j in np.unique(La[near]) if j > 0]:
                pm = La == j
                for _ in range(2): pm = pm | np.roll(pm, 1, 0) | np.roll(pm, -1, 0) | np.roll(pm, 1, 1) | np.roll(pm, -1, 1)
                pm &= ~m  # leave the predator body itself untouched
                s["pa"][pm] = -1.0
    # per-target overlap tracking of the predator body
    F = w.fields(s); Lb, nb = label_p(F[1])
    tmask = [Lb == c["pred"] for c in tg]; alive = [True] * len(tg)
    rec = []; snaps = {}; frames = []; fev = int(round(100.0 / dt))
    nsteps = int(round(a.T / dt)); ev = int(round(a.every / dt)); snap_steps = {int(round(x / dt)): x for x in a.snaps}
    wall = time.time()
    for i in range(nsteps + 1):
        if i % ev == 0 or i in snap_steps:
            F = w.fields(s); ca, cb = F[0], F[1]
            La, na = label_p(ca); Lb, nb = label_p(cb)
            row = dict(t=s["t"], n_prey=na, n_pred=nb, mean_cb=float(cb.mean()), mean_ca=float(ca.mean()), targets=[])
            # far-field predator bodies (centroid far from every target)
            nfar_pred = 0; nfar_prey = 0
            for j in range(1, nb + 1):
                cy, cx = pcentroid(Lb == j)
                if far[int(round(cy)) % H, int(round(cx)) % W]: nfar_pred += 1
            for j in range(1, na + 1):
                cy, cx = pcentroid(La == j)
                if far[int(round(cy)) % H, int(round(cx)) % W]: nfar_prey += 1
            row["far_pred"] = nfar_pred; row["far_prey"] = nfar_prey
            for k, c in enumerate(tg):
                reg = regions[k]
                tr = dict(max_cb=float(cb[reg].max()), sum_cb_excess=float(np.clip(cb[reg] - 0.05, 0, None).sum()),
                          n_pred_bodies=int(len([j for j in np.unique(Lb[reg]) if j > 0])), prey_area=int((ca[reg] > 0.5).sum()),
                          q_max=float(F[4][reg].max()))
                if alive[k]:
                    ov = Lb[tmask[k]]; ov = ov[ov > 0]
                    if ov.size == 0: alive[k] = False; tmask[k] = np.zeros_like(tmask[k])
                    else:
                        j = np.bincount(ov).argmax(); tmask[k] = Lb == j
                tr["tracked_alive"] = alive[k]; tr["tracked_area"] = int(tmask[k].sum())
                if alive[k]:
                    cy, cx = pcentroid(tmask[k]); tr["tracked_dist_from_center"] = float(pdist(H, W, c["cy"], c["cx"])[int(round(cy)) % H, int(round(cx)) % W])
                    tr["tracked_max_cb"] = float(cb[tmask[k]].max())
                row["targets"].append(tr)
            rec.append(row)
            if i in snap_steps: snaps[str(snap_steps[i])] = F[[0, 1, 4]].astype(np.float32)
        if i % fev == 0: frames.append(np.asarray(w.fields(s), np.float32))
        if i < nsteps: s = w.step(s)
    json.dump(dict(arm=arm, seed=a.seed, t0=t0, targets=tg, rows=rec, wall=time.time() - wall), open(a.out, "w"))
    np.savez_compressed(a.out.replace(".json", "_snaps.npz"), **snaps)
    np.savez_compressed(a.out.replace(".json", "_frames.npz"), render=np.array(frames))
    print(arm, "done", time.time() - wall)

if __name__ == "__main__":
    main()
