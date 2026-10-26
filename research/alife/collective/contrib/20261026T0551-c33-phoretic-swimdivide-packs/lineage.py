"""lineage.py <npz> [hold_frames=40]: merge-aware genealogy of A+B clusters by particle identity.
Each cluster at f+1 continues the track of the cluster at f that gave it most of its particles (>= 30%).
When a cluster at f sends >= 20% of itself into each of >= 2 clusters at f+1, and the two largest children
both live >= hold frames without ever sharing a cluster again, the split is persistent: both children get new
track ids with generation = parent generation + 1. Otherwise the largest child keeps the parent's id and
smaller children start new tracks with the parent's generation (fragments). A merge keeps the id and
generation of the largest parent. Founders that condense from the gas have generation 0.
Prints persistent splits per generation, max generation and merges/splits."""
import sys, numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0]); from clusters import clusters
npz = sys.argv[1]; hold = int(sys.argv[2]) if len(sys.argv) > 2 else 40
d = np.load(npz); X, SP, L, dt = d["x"], d["sp"], float(d["L"]), float(d["dt"])
if SP.ndim == 1: SP = np.repeat(SP[None], len(X), 0)
F = len(X); labs = []
for f in range(F):
    kp = SP[f] != 2; lab = -np.ones(len(kp), int); lab[kp], _ = clusters(X[f][kp], L); labs.append(lab)

def children(f, k):
    idx = labs[f] == k; nk = idx.sum(); ch = labs[f + 1][idx]; ch = ch[ch >= 0]
    if not len(ch): return []
    cs, cn = np.unique(ch, return_counts=True); o = np.argsort(-cn)
    return [int(cs[i]) for i in o if cn[i] >= 0.2 * nk]

def persistent(f, c1, c2):
    if f + hold >= F: return False
    m1, m2 = np.nonzero(labs[f + 1] == c1)[0], np.nonzero(labs[f + 1] == c2)[0]
    for g in range(f + 2, f + 1 + hold):
        l1 = labs[g][m1]; l1 = l1[l1 >= 0]; l2 = labs[g][m2]; l2 = l2[l2 >= 0]
        if len(l1) < 0.3 * len(m1) or len(l2) < 0.3 * len(m2): return False
        a, b = np.bincount(l1).argmax(), np.bincount(l2).argmax()
        if a == b: return False
        m1, m2 = np.nonzero(labs[g] == a)[0], np.nonzero(labs[g] == b)[0]
    return True

from clusters import pcentroid
pos = {}  # track id -> list of (frame, centroid, size)
reset = {}  # track id -> frame of its last merge (travel is measured only after it)
def note(f, k, t):
    idx = labs[f] == k; pos.setdefault(t, []).append((f, pcentroid(X[f][idx], L), int(idx.sum())))
def travel(t):
    q = [a for a in pos.get(t, []) if a[0] >= reset.get(t, -1)]
    if len(q) < 2: return 0.0
    c = np.array([a[1] for a in q]); dc = (np.diff(c, axis=0) + L / 2) % L - L / 2
    return float(np.hypot(*dc.sum(0)) / (1.8 * np.sqrt(np.median([a[2] for a in q]) / np.pi)))
tid = {}; gen = {}; nxt = 0; ps_by_gen = {}; nsplit = nmerge = 0; events = []
for k in range(labs[0].max() + 1): tid[(0, k)] = nxt; gen[nxt] = 0; nxt += 1
for f in range(F - 1):
    for k in range(labs[f].max() + 1): note(f, k, tid[(f, k)])
    assigned = {}
    for k in range(labs[f].max() + 1):
        ch = children(f, k); p = tid[(f, k)]
        if len(ch) >= 2:
            nsplit += 1
            if persistent(f, ch[0], ch[1]):
                g = gen[p] + 1; ps_by_gen[g] = ps_by_gen.get(g, 0) + 1
                kids = [np.nonzero(labs[f + 1] == c)[0] for c in ch[:2]]
                events.append((f, int((labs[f] == k).sum()), g, [len(q) for q in kids], [round(float((SP[f + 1][q] == 1).mean()), 2) for q in kids], round(travel(p), 2), p))
                for c in ch[:2]: assigned.setdefault(c, []).append((nxt, g, (labs[f + 1] == c).sum())); gen[nxt] = g; nxt += 1
                for c in ch[2:]: assigned.setdefault(c, []).append((nxt, gen[p], 0)); gen[nxt] = gen[p]; nxt += 1
                continue
        for i, c in enumerate(ch):
            if i == 0: assigned.setdefault(c, []).append((p, gen[p], (labs[f] == k).sum()))
            else: assigned.setdefault(c, []).append((nxt, gen[p], 0)); gen[nxt] = gen[p]; nxt += 1
    for c in range(labs[f + 1].max() + 1):
        if c in assigned:
            cand = sorted(assigned[c], key=lambda q: -q[2]); tid[(f + 1, c)] = cand[0][0]
            if len(cand) >= 2 and cand[1][2] > 0: nmerge += 1; reset[cand[0][0]] = f + 1
        else:
            tid[(f + 1, c)] = nxt; gen[nxt] = 0; nxt += 1
print(npz.split("/")[-1], "t=%.0f" % ((F - 1) * dt), "splits", nsplit, "merges", nmerge, "persistent by generation", dict(sorted(ps_by_gen.items())),
      "max generation", max(ps_by_gen) if ps_by_gen else 0)
import json
fb = [e[4] for e in events]; both = sum(1 for q in fb if min(q) >= 0.05)
print("  persistent splits whose two daughters both carry B (>= 5%):", both, "of", len(events))
tv = [e[5] for e in events]; print("  parents that travelled >= 3 cluster diameters (net) since their birth or last merge, before the split:", sum(v >= 3 for v in tv), "of", len(tv), "; max", max(tv) if tv else None)
for e in sorted(events, key=lambda e: -e[5])[:5]: print("    t=%.0f gen %d parent %d -> %s, B share %s, parent travel %.1f diameters (track %d)" % (e[0] * dt, e[2], e[1], e[3], e[4], e[5], e[6]))
print("  median daughter sizes", np.median([min(e[3]) for e in events]) if events else None, np.median([max(e[3]) for e in events]) if events else None)
if len(sys.argv) > 3:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    from clusters import pcentroid
    gmax = max(e[2] for e in events); deep = [e for e in events if e[2] >= gmax - 2]
    rng = np.random.default_rng(2); pick = [deep[i] for i in rng.choice(len(deep), size=min(4, len(deep)), replace=False)]
    offs = [-10, 0, 4, 10, 20, 40]; fig, ax = plt.subplots(len(pick), len(offs), figsize=(2.4 * len(offs), 2.5 * len(pick)), squeeze=False)
    for r, e in enumerate(pick):
        f = e[0]; par = [k for k in range(labs[f].max() + 1) if (labs[f] == k).sum() == e[1]][0]; c = pcentroid(X[f][labs[f] == par], L)
        for q, o in enumerate(offs):
            g = min(max(f + o, 0), F - 1); x = (X[g] - c + L / 2) % L - L / 2; a = ax[r, q]
            for kk, col, sz in ((2, "0.75", 2), (0, "red", 5), (1, "blue", 5)):
                m = (SP[g] == kk) & (np.abs(x).max(1) < 18); a.scatter(x[m, 0], x[m, 1], s=sz, c=col)
            a.set_xlim(-18, 18); a.set_ylim(-18, 18); a.set_aspect(1); a.set_xticks([]); a.set_yticks([])
            a.set_title(f"t={g * dt:.0f}" + (f" gen {e[2]}: {e[1]}->{e[3]}" if o == 0 else ""), fontsize=7)
    fig.suptitle(f"{npz.split('/')[-1]}: random persistent splits of generation >= {gmax - 2} (A red, B blue, food grey)", fontsize=9)
    fig.tight_layout(); fig.savefig(sys.argv[3], dpi=80); print("strip", sys.argv[3])
import os
if os.environ.get("TRACKFIG"):  # life strip of one dividing track: TRACK=<id> (default: most travelled parent of generation >= 3)
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    ev = [e for e in events if e[2] >= 3] or events
    e = [q for q in events if q[6] == int(os.environ["TRACK"])][0] if os.environ.get("TRACK") else max(ev, key=lambda q: q[5])
    q = [a for a in pos[e[6]] if a[0] >= reset.get(e[6], -1)]; fr = [q[i] for i in np.linspace(0, len(q) - 1, 7).astype(int)] + [(min(e[0] + 20, F - 1), q[-1][1], 0)]
    fig, ax = plt.subplots(1, 9, figsize=(21, 2.8)); c0 = q[0][1]
    for a, (f, c, n) in zip(ax[:8], fr):
        x = (X[f] - c + L / 2) % L - L / 2
        for kk, col, sz in ((2, "0.75", 2), (0, "red", 5), (1, "blue", 5)):
            m = (SP[f] == kk) & (np.abs(x).max(1) < 16); a.scatter(x[m, 0], x[m, 1], s=sz, c=col)
        a.set_xlim(-16, 16); a.set_ylim(-16, 16); a.set_aspect(1); a.set_xticks([]); a.set_yticks([]); a.set_title(f"t={f * dt:.0f} n={n}", fontsize=8)
    cc = np.array([a[1] for a in q]); ax[8].plot(cc[:, 0], cc[:, 1], ".", ms=2); ax[8].set_xlim(0, L); ax[8].set_ylim(0, L); ax[8].set_aspect(1)
    ax[8].set_title(f"track {e[6]}: {e[5]:.1f} diameters", fontsize=8)
    fig.suptitle(f"{npz.split('/')[-1]} track {e[6]} (generation {e[2] - 1}): travels, then splits at t={e[0] * dt:.0f} into {e[3]} (B share {e[4]}); last panel +10 t after the split", fontsize=9)
    fig.tight_layout(); fig.savefig(os.environ["TRACKFIG"], dpi=80); print("trackfig", os.environ["TRACKFIG"])
