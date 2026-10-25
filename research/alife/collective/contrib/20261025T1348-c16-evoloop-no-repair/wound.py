"""Wounding test (repair). Modes: sheath = remove all sheath cells; core = remove k random core (state-1) cells.
Original doc: Sheath ablation: at time t_a, pick mature loops (closed hole of the given side, no arm activity needed) and set
their sheath cells (state 2 inside the loop's bounding box + 1) to empty; a twin keeps them. After `dt` steps compare:
does the loop's hole survive, how many daughters (new holes within 30 px), and genome-signal cells (3-7) that
escaped beyond the box + 3 (leak). One loop ablated per branch (the rest of the world identical)."""
import sys, os, json, importlib.util, numpy as np
from evo_track import holes
params, seed, L, ta, side, n, dt, out = json.loads(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]), sys.argv[8]
mode = sys.argv[9] if len(sys.argv) > 9 else 'sheath'
kcells = int(sys.argv[10]) if len(sys.argv) > 10 else 8  # core mode: number of random core cells removed
os.environ["WORLD_P"] = json.dumps(params)
spec = importlib.util.spec_from_file_location("w", "world.py"); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(seed, (L, L))
for t in range(ta): w.step(s)
g0 = s["g"].copy(); lab, ids, area = holes(g0)
cand = [h for h in ids if round(np.sqrt(area[h])) == side]
rng = np.random.default_rng(seed); cand = [cand[i] for i in rng.permutation(len(cand))[:n]]
def run_branch(g, steps):
    st = dict(s); st["g"] = g.copy()
    for _ in range(steps): w.step(st)
    return st["g"]
res = []
for h in cand:
    ii, jj = np.nonzero(lab == h)
    if ii.max() - ii.min() > L / 2 or jj.max() - jj.min() > L / 2: continue  # skip loops across the seam
    i0, i1, j0, j1 = ii.min() - 3, ii.max() + 4, jj.min() - 3, jj.max() + 4  # hole bbox + sheath + core + sheath
    box = (slice(max(i0, 0), min(i1, L)), slice(max(j0, 0), min(j1, L)))
    ga = g0.copy(); sub = ga[box]
    if mode == 'sheath': sub[sub == 2] = 0
    elif mode == 'outer':  # outer sheath only: state-2 cells that touch the outside background
        from scipy import ndimage
        bg = (lab[box] != h) & (g0[box] == 0)
        lab_bg, _ = ndimage.label(bg); edge = np.unique(np.r_[lab_bg[0], lab_bg[-1], lab_bg[:, 0], lab_bg[:, -1]]); edge = edge[edge > 0]
        outside = np.isin(lab_bg, edge); touch = ndimage.binary_dilation(outside) & (sub == 2); sub[touch] = 0
    else:
        ci, cj = np.nonzero(sub == 1); k = rng.permutation(len(ci))[:kcells]; sub[ci[k], cj[k]] = 0
    ga[box] = sub
    out_b = {}
    for name, g in (("twin", g0), ("ablated", ga)):
        gf = run_branch(g, dt)
        l2, ids2, a2 = holes(gf)
        alive = bool(np.any(np.isin(l2[ii, jj], ids2)))
        big = (slice(max(i0 - 3, 0), min(i1 + 3, L)), slice(max(j0 - 3, 0), min(j1 + 3, L)))
        m = np.zeros((L, L), bool); m[big] = True
        # leak: signal cells just outside the enlarged box in the first 60 steps is not tracked; count dissolution (8) near the loop
        ci, cj = ii.mean(), jj.mean()
        near = [x for x in ids2 if x not in set(l2[ii, jj].tolist())]
        nk = 0
        for x in near:
            pi, pj = np.nonzero(l2 == x)
            if np.hypot(pi.mean() - ci, pj.mean() - cj) < 30: nk += 1
        out_b[name] = {"hole_alive": alive, "holes_within_30px": nk, "structure_in_box": int((gf[box] > 0).sum())}
    out_b["cells_removed"] = int((g0[box] != ga[box]).sum()); out_b["loop_cells"] = int((g0[box] > 0).sum())
    res.append(out_b); print(out_b, flush=True)
json.dump({"mode": mode, "kcells": kcells, "params": params, "seed": seed, "t_ablate": ta, "side": side, "dt": dt, "loops": res}, open(out, "w"), indent=1)
