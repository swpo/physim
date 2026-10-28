"""c61: what the trait novelty of c58's waste vortices is made of, per window, waste arm against its kind-blind twin.
Input: trait3.py / trait3c.py JSONs ('traits_by_frame': every 30 t, the traits of the labelled vortices). Class = round(theta/0.4).
Per window of W t:
  n       mean number of labelled vortices
  R       RMS distance of the vortices' traits from the population centroid (the cloud's radius)
  D0      distance of the window's mean centroid from the ancestor (theta = 0)
  step    distance between this window's mean centroid and the previous window's
  newcls  classes occupied for the first time in the run (per 1000 t)
  novel   share of vortex-samples whose class was first occupied < 1000 t before (the population living on new ground)
  far     share of vortex-samples farther than 0.4 (one class width) from every vortex trait recorded more than 1000 t earlier
c30 cohort statistic (as c59's o_vortex.py, Lc = 33 censuses) with three thresholds taken from twin kinds born after the
first window: raw activity (a*, q100 and q99), activity / total census count in the same Lc censuses (share), and activity x
mean number of occupied classes over those censuses / total (relative to an average class: corrects for standing diversity).
python vnov.py out.json [W=2000] label=spec.json:twin.json ..."""
import sys, json, numpy as np
from scipy.spatial import cKDTree
DM, LC, WIN = 0.4, 33, 33


def load(p):
    d = json.load(open(p)); T = []; X = []
    for t, th in d['traits_by_frame']:
        T.append(t); X.append(np.array(th, float).reshape(-1, 3))
    return np.array(T), X


def census(X):
    out = []
    for x in X:
        r = {}
        for v in x:
            c = tuple(int(round(u / DM)) for u in v); r[c] = r.get(c, 0) + 1
        out.append(r)
    return out


def cohort(C, norm):
    """early activity of each kind (first Lc censuses after its birth), raw or normalised"""
    tot = np.array([sum(r.values()) for r in C], float); ncl = np.array([len(r) for r in C], float)
    birth, act = {}, {}
    for j, r in enumerate(C):
        for g, n in r.items():
            b = birth.setdefault(g, j)
            if j - b <= LC: act[g] = act.get(g, 0) + n
    out = {}
    for g, a in act.items():
        b = birth[g]; sl = slice(b, min(b + LC + 1, len(C)))
        if norm == 'raw': out[g] = a
        elif norm == 'share': out[g] = a / max(tot[sl].sum(), 1)
        else: out[g] = a * ncl[sl].mean() / max(tot[sl].sum(), 1)
    return birth, out


def sig_counts(C, astar, norm, nwin):
    birth, act = cohort(C, norm); cnt = [0] * nwin
    for g, a in act.items():
        b = birth[g]
        if WIN <= b < len(C) - LC and a >= astar: cnt[min(b // WIN, nwin - 1)] += 1
    return cnt


def astar_of(C, norm, q):
    birth, act = cohort(C, norm); v = [act[g] for g in act if WIN <= birth[g] < len(C) - LC]
    return float(np.percentile(v, q)) if v else float('inf')


def windows(T, X, W):
    C = census(X); first = {}; cents = []
    for j, r in enumerate(C):
        for g in r: first.setdefault(g, T[j])
    for x in X: cents.append(x.mean(0) if len(x) else np.full(3, np.nan))
    cents = np.array(cents); t0 = T[0]; rows = []; prev = None
    for a in np.arange(t0, T[-1], W):
        idx = np.flatnonzero((T >= a) & (T < a + W))
        if len(idx) < 3: continue
        n = np.mean([len(X[j]) for j in idx])
        R = np.sqrt(np.nanmean([((X[j] - cents[j]) ** 2).sum(1).mean() for j in idx if len(X[j])]))
        cm = np.nanmean(cents[idx], 0); D0 = float(np.linalg.norm(cm))
        step = float(np.linalg.norm(cm - prev)) if prev is not None else np.nan; prev = cm
        newc = sum(1 for g, tf in first.items() if a <= tf < a + W) * 1000.0 / W
        nov = []; far = []
        oldp = [X[j] for j in range(len(T)) if T[j] < a - 1000 and len(X[j])]
        tree = cKDTree(np.concatenate(oldp)) if oldp else None
        for j in idx:
            for v in X[j]:
                g = tuple(int(round(u / DM)) for u in v); nov.append(T[j] - first[g] < 1000)
            if tree is not None and len(X[j]):
                dd, _ = tree.query(X[j]); far += list(dd > 0.4)
        rows.append(dict(t=float(a), n=float(n), R=float(R), D0=D0, step=step, newcls=newc,
                         novel=float(np.mean(nov)) if nov else np.nan, far=float(np.mean(far)) if far else np.nan))
    return rows, C


if __name__ == '__main__':
    out = sys.argv[1]; args = sys.argv[2:]; W = 2000.0
    if args and args[0].startswith('W='): W = float(args[0][2:]); args = args[1:]
    res = {}
    for arg in args:
        lab, pp = arg.split('='); ps, pt = pp.split(':')
        Ts, Xs = load(ps); Tt, Xt = load(pt)
        rs, Cs = windows(Ts, Xs, W); rt, Ct = windows(Tt, Xt, W)
        nwin = int(np.ceil(len(Cs) / WIN)); o = {'spec': rs, 'twin': rt, 'W': W}
        for norm in ('raw', 'share', 'div'):
            for q in (100, 99):
                a = astar_of(Ct, norm, q)
                o[f'{norm}_q{q}'] = {'astar': a, 'spec': sig_counts(Cs, a, norm, nwin), 'twin': sig_counts(Ct, a, norm, nwin)}
        res[lab] = o
        print(lab)
        for k in ('spec', 'twin'):
            print(' ', k, ' '.join(f"t{r['t']:.0f}:n{r['n']:.0f} R{r['R']:.2f} D0{r['D0']:.2f} st{r['step']:.2f} new{r['newcls']:.1f} nov{r['novel']:.2f} far{r['far']:.2f}" for r in o[k]))
        for norm in ('raw', 'share', 'div'):
            for q in (100, 99):
                x = o[f'{norm}_q{q}']; print(f'  {norm} q{q} a*={x["astar"]:.3g} spec {x["spec"]} twin {x["twin"]}')
    json.dump(res, open(out, 'w'), indent=1)
