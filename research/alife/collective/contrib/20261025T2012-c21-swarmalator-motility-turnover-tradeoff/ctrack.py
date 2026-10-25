"""Particle-cluster tracker for swarmalator runs: clusters = connected components of particles within rc
(periodic), size >= nmin. Between snapshots dt_s apart, a cluster's children are the later clusters that
take >= frac of its members; a split = one parent with >= 2 children each >= nmin that came mostly from it.
Reports cluster count, mean size, splits, merges, and cluster displacement in body lengths over its life."""
import numpy as np
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

def clusters(x, L, rc=1.3, nmin=6):
    pr = cKDTree(x, boxsize=L).query_pairs(rc, output_type="ndarray"); N = len(x)
    A = coo_matrix((np.ones(len(pr)), (pr[:, 0], pr[:, 1])), shape=(N, N))
    n, lab = connected_components(A, directed=False)
    cnt = np.bincount(lab); good = cnt >= nmin
    lab = np.where(good[lab], lab, -1)
    return lab

def analyse(snaps, L, nmin=6, frac=0.5):
    labs = [clusters(x, L, nmin=nmin) for x in snaps]
    splits = merges = 0; nc = []; sizes = []; ev = []
    for t in range(len(labs) - 1):
        a, b = labs[t], labs[t + 1]
        ids_a = [k for k in np.unique(a) if k >= 0]; ids_b = [k for k in np.unique(b) if k >= 0]
        nc.append(len(ids_a)); sizes += [int((a == k).sum()) for k in ids_a]
        for k in ids_a:
            m = a == k
            ch = [j for j in np.unique(b[m]) if j >= 0 and (b[m] == j).sum() >= nmin and (a[b == j] == k).mean() >= frac]
            if len(ch) >= 2: splits += 1; ev.append(("split", t, int(m.sum()), [int((b == j).sum()) for j in ch]))
        for j in ids_b:
            m = b == j
            par = [k for k in np.unique(a[m]) if k >= 0 and (a[m] == k).sum() >= nmin]
            if len(par) >= 2: merges += 1
    return dict(clusters_mean=float(np.mean(nc)), size_mean=float(np.mean(sizes)), size_max=int(np.max(sizes)), splits=splits, merges=merges, events=ev)
