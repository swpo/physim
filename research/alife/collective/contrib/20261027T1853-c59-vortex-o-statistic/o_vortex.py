"""c59: c30's shadow-calibrated O statistic (o_measure.py) on the fed-vortex trait runs. Census = class counts of the
labelled vortices every 30 t (class = round(theta/0.4)). Activity of a kind = summed counts over censuses. A kind is
significant when its activity within Lc = 33 censuses (~1000 t) of its birth reaches a*, the maximum (q=100) or 99th
percentile of the same early activity among kinds born after the first window in a neutral reference:
  (a) the in-world kind-blind twin (same ecology, same mutation draws), and
  (b) 3 Rechtsteiner-Bedau census shadows of the selective run itself (o_measure.census_shadow: same sizes and
      innovations, random parents).
Reports significant new kinds per 1000-t window, and top-5 overlap with the first and previous window (replacement).
python o_vortex.py out.json label=spec.json:twin.json ..."""
import sys, json, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife/collective/contrib/20261026T0052-c30-o-measure-tool')
import o_measure as O
DM, LC, WIN = 0.4, 33, 33
def rows(p):
    d = json.load(open(p)); out = []
    for t, th in d['traits_by_frame']:
        r = {}
        for x in th:
            c = tuple(int(round(v / DM)) for v in x); r[c] = r.get(c, 0) + 1
        out.append(r)
    return out, d['traits_by_frame'][0][0]
def early(rs):
    act, birth = {}, {}
    for j, r in enumerate(rs):
        for g, n in r.items():
            b = birth.setdefault(g, j)
            if j - b <= LC: act[g] = act.get(g, 0) + n
    return birth, act
def astar(rs, q):
    b, a = early(rs); v = [a[g] for g in a if WIN <= b[g] < len(rs) - LC]
    return float(np.percentile(v, q)) if v else float('inf')
res = {}
for arg in sys.argv[2:]:
    lab, pp = arg.split('='); ps, pt = pp.split(':')
    S, t0 = rows(ps); Tw, _ = rows(pt); out = {'t0': t0, 'n_census': len(S)}
    for q in (100, 99):
        a = astar(Tw, q); st = O.census_stats(S, a, LC, WIN); tt = O.census_stats(Tw, a, LC, WIN)
        out[f'twin_q{q}'] = {'astar': a, 'spec_new': st['cohort_new'], 'twin_new': tt['cohort_new'],
                             'spec_late': int(sum(st['cohort_new'][3:])), 'twin_late': int(sum(tt['cohort_new'][3:]))}
    sh = [O.census_shadow(S, seed=s) for s in range(3)]
    a = max(astar(x, 100) for x in sh); st = O.census_stats(S, a, LC, WIN)
    out['shadow_max'] = {'astar': a, 'spec_new': st['cohort_new'], 'shadow_new': [O.census_stats(x, a, LC, WIN)['cohort_new'] for x in sh],
                         'spec_late': int(sum(st['cohort_new'][3:])), 'top5_first': st['top_overlap_first'], 'top5_prev': st['top_overlap_prev']}
    out['twin_top5_first'] = O.census_stats(Tw, 1e9, LC, WIN, topk=5)['top_overlap_first']
    res[lab] = out
    print(lab, json.dumps({k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items()}) for k, v in out.items()}))
json.dump(res, open(sys.argv[1], 'w'), indent=1)
