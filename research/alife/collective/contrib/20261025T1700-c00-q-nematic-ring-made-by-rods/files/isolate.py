"""Self-propulsion test: does a rod move when its neighbours are removed?
Run the world to frame F0; pick the largest rods; for each, a copy of the state keeps only that rod's
Voronoi cell (phi, q1, q2; elsewhere phi = the bath median, Q = 0) and is evolved alone for NF frames.
The same rods are followed in the unmodified colony for comparison (overlap tracking, phi-weighted centroids).
usage: isolate.py world.py seed F0 NF nrods"""
import sys, importlib.util, copy
import numpy as np
from scipy import ndimage
sys.path.insert(0, "/home/user/physim/research/alife"); sys.dont_write_bytecode = True
from labkit import metrics as M

spec = importlib.util.spec_from_file_location("w", sys.argv[1]); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
seed, F0, NF, nrods = (int(x) for x in sys.argv[2:6])
spf = 100; dtf = spf * W.P["dt"]
st = W.init(seed, W.META["size"]); H, Wd = st["phi"].shape
for _ in range(F0 * spf):
    st = W.step(st)


def comps(phi):
    return M.periodic_label(phi > 0)


def wcentroid(phi, m):
    ys, xs = np.nonzero(m); w = np.maximum(phi[m], 0) + 1e-9
    ay, ax = 2 * np.pi * ys / H, 2 * np.pi * xs / Wd
    cy = (np.arctan2((w * np.sin(ay)).sum(), (w * np.cos(ay)).sum()) % (2 * np.pi)) * H / (2 * np.pi)
    cx = (np.arctan2((w * np.sin(ax)).sum(), (w * np.cos(ax)).sum()) % (2 * np.pi)) * Wd / (2 * np.pi)
    return cy, cx


def length(m, cy, cx):
    ys, xs = np.nonzero(m)
    dy, dx = M._wrap(ys - cy, H), M._wrap(xs - cx, Wd)
    return float(np.sqrt(12 * np.linalg.eigvalsh(np.cov(np.stack([dy, dx]), bias=True))[1]))


def follow(state, mask0, nf):
    """Evolve nf frames, following the component with the largest overlap; returns per-frame (cy, cx, area, L, ncomp_in_lineage)."""
    out = []; m = mask0
    cy, cx = wcentroid(state["phi"], m); out.append((cy, cx, int(m.sum()), length(m, cy, cx), 1))
    for f in range(nf):
        for _ in range(spf):
            state = W.step(state)
        lab, n = comps(state["phi"])
        dil = ndimage.binary_dilation(m, iterations=2)
        dil = dil | np.roll(dil, 0, 0)
        ids, cnt = np.unique(lab[dil & (lab > 0)], return_counts=True)
        if not len(ids):
            out.append(None); break
        m = lab == ids[np.argmax(cnt)]
        cy, cx = wcentroid(state["phi"], m)
        big = [i for i, c in zip(ids, cnt) if (lab == i).sum() >= 12]
        out.append((cy, cx, int(m.sum()), length(m, cy, cx), len(big)))
    return out


def summary(tr):
    tr = [t for t in tr if t is not None]
    cy = np.array([t[0] for t in tr]); cx = np.array([t[1] for t in tr])
    dy, dx = M._wrap(np.diff(cy), H), M._wrap(np.diff(cx), Wd)
    net = float(np.hypot(dy.sum(), dx.sum())); path = float(np.hypot(dy, dx).sum())
    L = float(np.median([t[3] for t in tr])); A = float(np.median([t[2] for t in tr]))
    return net, path, L, A, len(tr) - 1, max(t[4] for t in tr)


phi = st["phi"]; lab, n = comps(phi)
areas = ndimage.sum(np.ones_like(phi), lab, range(1, n + 1))
tile = np.tile(phi > 0, (3, 3)); _, idx = ndimage.distance_transform_edt(~tile, return_indices=True)
sl = (slice(H, 2 * H), slice(Wd, 2 * Wd)); own = np.where(phi > 0, lab, lab[idx[0][sl] % H, idx[1][sl] % Wd])
bath = float(np.median(phi[phi < -0.3]))
pick = [int(j) + 1 for j in np.argsort(areas)[::-1][:nrods]]
print(f"seed {seed}: at frame {F0} (t={F0*dtf:.0f}) {n} rods; bath phi median {bath:.3f}; isolating rods {pick} (areas {[int(areas[j-1]) for j in pick]}) for {NF} frames ({NF*dtf:.0f} t)")
col = {}
# colony: one evolution, follow every picked rod
stc = copy.deepcopy(st); masks = {j: lab == j for j in pick}; trs = {j: [] for j in pick}
for j in pick:
    cy, cx = wcentroid(stc["phi"], masks[j]); trs[j].append((cy, cx, int(masks[j].sum()), length(masks[j], cy, cx), 1))
for f in range(NF):
    for _ in range(spf):
        stc = W.step(stc)
    l2, n2 = comps(stc["phi"])
    for j in pick:
        if trs[j][-1] is None:
            continue
        dil = ndimage.binary_dilation(masks[j], iterations=2)
        ids, cnt = np.unique(l2[dil & (l2 > 0)], return_counts=True)
        if not len(ids):
            trs[j].append(None); continue
        masks[j] = l2 == ids[np.argmax(cnt)]
        cy, cx = wcentroid(stc["phi"], masks[j])
        trs[j].append((cy, cx, int(masks[j].sum()), length(masks[j], cy, cx), len([i for i, c in zip(ids, cnt) if (l2 == i).sum() >= 12])))
for j in pick:
    net, path, L, A, nfr, nc = summary(trs[j])
    print(f"  COLONY rod {j}: {nfr} frames, net {net:.1f} px, path {path:.1f}, persist {net/max(path,1e-9):.2f}, L {L:.1f} px -> {net/L:.2f} L ({net/np.sqrt(A):.2f} sqrtA), speed {net/(nfr*dtf):.4f} px/t, max pieces {nc}")
for j in pick:
    s1 = copy.deepcopy(st); cell = own == j
    s1["phi"] = np.where(cell, st["phi"], bath); s1["q1"] = np.where(cell, st["q1"], 0.0); s1["q2"] = np.where(cell, st["q2"], 0.0)
    tr = follow(s1, lab == j, NF)
    net, path, L, A, nfr, nc = summary(tr)
    lab_end, n_end = comps(s1["phi"]) if False else (None, None)
    print(f"  ALONE  rod {j}: {nfr} frames, net {net:.1f} px, path {path:.1f}, persist {net/max(path,1e-9):.2f}, L {L:.1f} px -> {net/L:.2f} L ({net/np.sqrt(A):.2f} sqrtA), speed {net/(nfr*dtf):.4f} px/t, max pieces {nc}")
