"""O measure for C:open-ended: shadow-calibrated cohort novelty plus replacement (c30).

Why: raw cumulative novelty and cumulative Bedau new activity both keep growing in Hash Chemistry for
20000 steps while its adaptive novelty stopped by t~2000 (20261026T0009-c30-hash-chemistry-o-calibration).
What to report for a world claiming O:
  1. cohort new activity: kinds BORN in window w whose activity (replications or copy-censuses)
     within Lc of birth reaches a*, where a* is calibrated on a neutral reference (q-th percentile of the
     same early activity in an in-world neutral twin or a Rechtsteiner-Bedau shadow of the run);
  2. the same count on the neutral reference; O needs real > reference in LATE windows, sustained;
  3. replacement: share of each window's top-k kinds already top-k in the first window (must decay),
     and share vs the previous window (turnover keeps happening).
Inputs are either replication logs (arrays t, kind) or censuses (list of {kind: count}).

API
  early_activity(t, k, Lc)                     -> (birth_time, early_activity) per kind
  calibrate_astar(t_ref, k_ref, Lc, q, t0, t1) -> a* from a neutral reference log
  cohort(t, k, T, astar, Lc, win)              -> dict(sig, births) per window
  top_overlap(t, k, T, win, topk)              -> dict(first, prev)
  rb_shadow(birth_t, innov, death_t, n0, seed) -> (t, k) replication log of a neutral shadow
  census_shadow(rows, seed), census_stats(rows, astar, Lc, win, topk)
  report(t, k, t_ref, k_ref, T, ...)           -> everything above in one dict, with late totals
Self-test: python o_measure.py --selftest  (synthetic Moran process: neutral vs recurrent sweeps)
"""
import numpy as np


def _running(t, k):
    o = np.argsort(t, kind="stable"); t = np.asarray(t)[o].astype(np.int64); k = np.asarray(k)[o]
    u, fi, inv = np.unique(k, return_index=True, return_inverse=True)
    return t, k, inv, t[fi]


def early_activity(t, k, Lc):
    t, k, inv, birth = _running(t, k)
    ok = (t - birth[inv]) <= Lc
    return birth, np.bincount(inv[ok], minlength=len(birth))


def calibrate_astar(t_ref, k_ref, Lc, q=99.9, t0=0, t1=None):
    b, a = early_activity(t_ref, k_ref, Lc)
    t1 = b.max() - Lc if t1 is None else t1
    sel = (b >= t0) & (b < t1)
    return float(np.percentile(a[sel], q)) if sel.any() else float("inf")


def cohort(t, k, T, astar, Lc, win):
    b, a = early_activity(t, k, Lc); nb = T // win
    hit = (a >= astar) & (b < T - Lc)
    return dict(sig=np.bincount(b[hit] // win, minlength=nb)[:nb].tolist(),
                births=np.bincount(b // win, minlength=nb)[:nb].tolist())


def top_overlap(t, k, T, win, topk=20):
    t = np.asarray(t); k = np.asarray(k); tops = []
    for w in range(T // win):
        s = (t >= w * win) & (t < (w + 1) * win)
        if not s.any(): tops.append(set()); continue
        u, c = np.unique(k[s], return_counts=True); tops.append(set(u[np.argsort(-c)[:topk]].tolist()))
    return dict(first=[len(tops[0] & x) / topk for x in tops],
                prev=[1.0] + [len(tops[i - 1] & tops[i]) / topk for i in range(1, len(tops))])


def rb_shadow(birth_t, innov, death_t, n0, seed=0):
    """Rechtsteiner-Bedau shadow at the kind level. birth_t: times of births; innov: True where the
    newborn's kind differs from its parent's (a mutation); death_t: times of deaths; n0: the initial
    population, either a size (all kinds distinct) or the list of initial kinds (give the real ones). Parents and victims are drawn uniformly from the shadow;
    an innovation gets a fresh label. Returns the shadow's (t, kind) birth log."""
    rng = np.random.default_rng(seed)
    ev = np.r_[np.asarray(birth_t, np.int64), np.asarray(death_t, np.int64)]
    typ = np.r_[np.where(np.asarray(innov, bool), 2, 1), np.zeros(len(death_t), int)]
    o = np.lexsort((rng.random(len(ev)), ev)); ev = ev[o]; typ = typ[o]
    lab = list(range(n0)) if np.isscalar(n0) else [int(x) for x in n0]
    nxt = max(lab) + 1 if lab else 0; out_t = []; out_k = []
    for t, y in zip(ev, typ):
        if y == 0:
            if lab: j = rng.integers(len(lab)); lab[j] = lab[-1]; lab.pop()
        else:
            if y == 2 or not lab:
                kk = nxt; nxt += 1
            else:
                kk = lab[rng.integers(len(lab))]
            lab.append(kk); out_t.append(t); out_k.append(kk)
    return np.array(out_t, np.int64), np.array(out_k, np.int64)


def census_shadow(rows, seed=0, g=1):
    """rows: list of {kind: count}. Shadow census j+1 has the real size; copies of kinds new in the real
    census get fresh labels (same innovation counts); the rest are drawn multinomially from the shadow's
    census j (random parents, no selection). g = Wright-Fisher generations of neutral drift between
    two censuses: g = 1 resamples once per census, which UNDER-states drift when many generations
    pass between censuses (BFF: ~1 WF generation per epoch, 50 epochs per census)."""
    rng = np.random.default_rng(seed); seen = set(); sh = []; prev = None; nxt = 0
    for r in rows:
        N = sum(r.values()); new = [n for g, n in r.items() if g not in seen]; seen |= set(r)
        if prev is None or sum(prev.values()) == 0:
            cur = {("x", g): n for g, n in r.items()}
        else:
            labs = list(prev); p = np.array([prev[l] for l in labs], float); p /= p.sum(); M = max(0, N - sum(new))
            for _ in range(g):
                draw = rng.multinomial(M, p); p = draw / max(1, draw.sum())
            cur = {l: int(n) for l, n in zip(labs, draw) if n > 0}
            for s in new:
                cur[("n", nxt)] = s; nxt += 1
        sh.append(cur); prev = cur
    return sh


def census_stats(rows, astar, Lc, win, topk=5):
    """Census version: activity = summed counts over censuses; Lc and win in census units."""
    act, birth, hit = {}, {}, {}
    for j, r in enumerate(rows):
        for g, n in r.items():
            birth.setdefault(g, j); act[g] = act.get(g, 0) + n
            if act[g] >= astar and g not in hit: hit[g] = j
    nb = (len(rows) + win - 1) // win; coh = np.zeros(nb, int)
    for g, j in hit.items():
        if j - birth[g] <= Lc: coh[birth[g] // win] += 1
    tops = []
    for b in range(0, len(rows), win):
        agg = {}
        for r in rows[b:b + win]:
            for g, n in r.items(): agg[g] = agg.get(g, 0) + n
        tops.append(set(sorted(agg, key=lambda g: -agg[g])[:topk]))
    return dict(cohort_new=coh.tolist(), n_kinds=len(birth),
                top_overlap_first=[len(tops[0] & x) / topk for x in tops],
                top_overlap_prev=[1.0] + [len(tops[i - 1] & tops[i]) / topk for i in range(1, len(tops))])


def report(t, k, t_ref, k_ref, T, Lc=1000, win=1000, q=99.9, late_from=None, topk=20):
    """Cohort novelty of a run against a neutral reference log (twin or shadow), and replacement."""
    late_from = 2 * win if late_from is None else late_from
    astar = calibrate_astar(t_ref, k_ref, Lc, q, t0=win)
    r = cohort(t, k, T, astar, Lc, win); s = cohort(t_ref, k_ref, T, astar, Lc, win); ov = top_overlap(t, k, T, win, topk)
    lw = late_from // win
    return dict(astar=astar, sig=r["sig"], births=r["births"], ref_sig=s["sig"], ref_births=s["births"],
                late_sig=int(sum(r["sig"][lw:])), late_ref_sig=int(sum(s["sig"][lw:])), top_first=ov["first"], top_prev=ov["prev"])


def _moran(seed, T=8000, N=500, mu=0.0005, s_new=0.0):
    """Synthetic Moran process logging births (t, kind). s_new > 0 gives each new mutant a fitness
    advantage over its parent (recurrent sweeps); s_new = 0 is neutral."""
    rng = np.random.default_rng(seed); kind = np.zeros(N, np.int64); fit = np.ones(N); nxt = 1
    bt, bk, inn, dt = [], [], [], []
    for t in range(T):
        for _ in range(N // 10):
            p = rng.choice(N, p=fit / fit.sum()); v = rng.integers(N)
            if rng.random() < mu:
                kind[v] = nxt; fit[v] = fit[p] * (1 + s_new); nxt += 1; inn.append(True)
            else:
                kind[v] = kind[p]; fit[v] = fit[p]; inn.append(False)
            bt.append(t); bk.append(kind[v]); dt.append(t)
        fit /= fit.max()
    return np.array(bt), np.array(bk), np.array(inn), np.array(dt)


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        T = 8000
        for s_new in (0.0, 0.2):
            for ms in (1, 3):
                bt, bk, inn, dt = _moran(ms, T=T, s_new=s_new)
                sh = [rb_shadow(bt, inn, dt, n0=[0] * 500, seed=q) for q in range(8)]
                ast = calibrate_astar(sh[0][0], sh[0][1], 1000, 99.9, t0=1000)
                real = sum(cohort(bt, bk, T, ast, 1000, 1000)["sig"][2:])
                env = [sum(cohort(a, b, T, ast, 1000, 1000)["sig"][2:]) for a, b in sh]
                print(f"Moran s_new={s_new} seed {ms}: a*={ast:.0f}; late significant new kinds real {real}, 8 RB shadows {env}")
