"""O measure (C:open-ended) calibrated on Hash Chemistry. Importable; no side effects.

Components are the replicating kinds (Hash Chemistry: multisets of size >= kmin, keyed by world.mkey;
census worlds: genotype strings). Three statistics, each compared with a Rechtsteiner-Bedau neutral
shadow of the same run (ECAL'99: same births, deaths and innovations, uniformly random parents and
victims, so no selection):

1. raw novelty: cumulative number of distinct components (Sayama's Fig. 5 measure).
2. Bedau new activity: components whose cumulative activity (number of replications) reaches a*.
   Over long runs this counts late crossings by OLD, slowly replicating components.
3. cohort new activity (the measure we recommend): components BORN in a window that reach a*
   within L steps of birth. O needs it to stay above the shadow's in late windows, together with
   4. replacement: overlap of the top-k components between windows decays (old kinds lose out).
"""
import numpy as np
from numba import njit
from world import mkey


# ---------- Rechtsteiner-Bedau shadow for event logs ----------
@njit
def _shadow(seed, T, n0, ntypes, rep_t, rep_s, die_t, die_s, mut_n, salt, cap):
    np.random.seed(seed)
    lab = np.empty(cap, np.int64)
    for i in range(n0):
        lab[i] = 1 + np.random.randint(ntypes)
    n = n0
    out_t = np.empty(len(rep_t), np.int32); out_k = np.empty(len(rep_t), np.uint64); out_s = np.empty(len(rep_t), np.int32)
    no = 0; ir = 0; idd = 0
    buf = np.empty(cap, np.int64)
    for t in range(T):
        r0 = ir
        while ir < len(rep_t) and rep_t[ir] == t:
            ir += 1
        d0 = idd
        while idd < len(die_t) and die_t[idd] == t:
            idd += 1
        nr = ir - r0; nd = idd - d0
        ev = np.empty(nr + nd, np.int64)
        for a in range(nr):
            ev[a] = a
        for a in range(nd):
            ev[nr + a] = -(a + 1)
        ev = ev[np.random.permutation(nr + nd)]   # within-step order is not logged: interleave at random
        for e in ev:
            if e >= 0:
                k = rep_s[r0 + e]
                if k > n or n + k > cap:
                    continue
                for a in range(k):
                    b = a + np.random.randint(n - a)
                    tmp = lab[a]; lab[a] = lab[b]; lab[b] = tmp
                    buf[a] = lab[a]
                st = np.sort(buf[:k])
                out_t[no] = t; out_k[no] = mkey(st, salt); out_s[no] = k; no += 1
                for a in range(k):
                    lab[n + a] = buf[a]
                n += k
            else:
                k = min(die_s[d0 + (-e - 1)], n)
                for a in range(k):
                    b = np.random.randint(n)
                    lab[b] = lab[n - 1]; n -= 1
        for a in range(mut_n[t]):
            if n > 0:
                lab[np.random.randint(n)] = 1 + np.random.randint(ntypes)
    return out_t[:no], out_k[:no], out_s[:no]


def shadow(L, seed=1, n0=10, ntypes=1000, salt=12345):
    T = len(L["mut_n"])
    st, sk, ss = _shadow(seed, T, n0, ntypes, L["rep_t"].astype(np.int64), L["rep_s"].astype(np.int64),
                         L["die_t"].astype(np.int64), L["die_s"].astype(np.int64), L["mut_n"].astype(np.int64), salt, 600000)
    return dict(rep_t=st, rep_k=sk, rep_s=ss)


# ---------- statistics on (t, key) replication logs ----------
def _prep(t, k):
    o = np.argsort(t, kind="stable"); t = t[o].astype(np.int64); k = k[o]
    u, fi, inv = np.unique(k, return_index=True, return_inverse=True)
    idx = np.argsort(inv, kind="stable"); g = inv[idx]
    starts = np.r_[0, np.flatnonzero(np.diff(g)) + 1]
    cc = np.empty(len(g), np.int64)
    cc[idx] = np.arange(len(g)) - np.repeat(starts, np.diff(np.r_[starts, len(g)]))
    return t, k, inv, t[fi], cc + 1          # times, keys, component index, birth time per component, running activity


def stats(L, T, kmin=2, astar=50, Lc=1000, win=1000, topk=20):
    m = L["rep_s"] >= kmin
    t, k, inv, birth, run_a = _prep(L["rep_t"][m], L["rep_k"][m])
    nb = T // win
    first = run_a == 1
    cum_unique = np.cumsum(np.bincount(t[first], minlength=T))[:T]
    hit = run_a == astar
    th = t[hit]; bh = birth[inv[hit]]
    bedau_new = np.bincount(th // win, minlength=nb)[:nb]               # crossings per window (any age)
    ok = (th - bh) <= Lc
    cohort_new = np.bincount(bh[ok] // win, minlength=nb)[:nb]        # crossings by components born in the window
    age_at_cross = [float(np.median(th[(th // win) == b] - bh[(th // win) == b])) if np.any((th // win) == b) else None for b in range(nb)]
    tops = []
    for b in range(nb):
        s = (t >= b * win) & (t < (b + 1) * win)
        if not s.any(): tops.append(set()); continue
        u, c = np.unique(k[s], return_counts=True); tops.append(set(u[np.argsort(-c)[:topk]].tolist()))
    ov_first = [len(tops[0] & x) / topk for x in tops]
    ov_prev = [1.0] + [len(tops[i - 1] & tops[i]) / topk for i in range(1, nb)]
    msize = np.bincount(L["rep_t"] // win, weights=L["rep_s"], minlength=nb)[:nb] / np.maximum(1, np.bincount(L["rep_t"] // win, minlength=nb)[:nb])
    return dict(cum_unique=cum_unique, bedau_new=bedau_new, cohort_new=cohort_new, age_at_cross=age_at_cross,
                top_overlap_first=ov_first, top_overlap_prev=ov_prev, mean_size=msize)


# ---------- census version (worlds that log genotype counts, e.g. evoloop) ----------
def census_shadow(rows, seed=0):
    """rows: list of {genotype: count}. Shadow census j+1 has the real size; copies of genotypes new in the
    real census keep fresh labels (same innovation counts); the rest are drawn multinomially from the
    shadow's census j (random parents)."""
    rng = np.random.default_rng(seed)
    seen = set(); sh = []; prev = None; nextlab = 0
    for r in rows:
        N = sum(r.values()); new = [n for g, n in r.items() if g not in seen]; seen |= set(r)
        if prev is None or sum(prev.values()) == 0:
            cur = {("x", g): n for g, n in r.items()}
        else:
            labs = list(prev); p = np.array([prev[l] for l in labs], float); p /= p.sum()
            draw = rng.multinomial(max(0, N - sum(new)), p)
            cur = {l: int(n) for l, n in zip(labs, draw) if n > 0}
            for s in new:
                cur[("n", nextlab)] = s; nextlab += 1
        sh.append(cur); prev = cur
    return sh


def census_stats(rows, astar, Lc, win, topk=5):
    act, birth, hit = {}, {}, {}
    for j, r in enumerate(rows):
        for g, n in r.items():
            birth.setdefault(g, j); act[g] = act.get(g, 0) + n
            if act[g] >= astar and g not in hit: hit[g] = j
    nb = (len(rows) + win - 1) // win
    coh = np.zeros(nb, int); bed = np.zeros(nb, int)
    for g, j in hit.items():
        bed[j // win] += 1
        if j - birth[g] <= Lc: coh[birth[g] // win] += 1
    tops = []
    for b in range(0, len(rows), win):
        agg = {}
        for r in rows[b:b + win]:
            for g, n in r.items(): agg[g] = agg.get(g, 0) + n
        tops.append(set(sorted(agg, key=lambda g: -agg[g])[:topk]))
    return dict(cohort_new=coh, bedau_new=bed, n_components=len(birth),
                top_overlap_first=[len(tops[0] & x) / topk for x in tops],
                top_overlap_prev=[1.0] + [len(tops[i - 1] & tops[i]) / topk for i in range(1, len(tops))])
