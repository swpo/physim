"""Auditor's multilevel (Price-style) decomposition of the change of the particle-weighted mean trait
over consecutive genealogy snapshots (DT = 50 steps), for the yield ym and the inert marker zm.
  ybar(a+1) - ybar(a) = WITHIN + BETWEEN
  WITHIN  = sum_j w'_j (y'_j - y_anc(j))   over cells with a single ancestor at a (continuations, split daughters)
  BETWEEN = the rest: deaths, differential particle-number growth, merges, appearances (composition change)
Also: within-life change of cells that later die vs survive, parent->daughter heritability at
persistent two-way splits, and fates by birth rank (low/high) with off-kind daughters.
usage: python price.py gen.json[.gz] [minlife=20]"""
import sys, json, gzip
import numpy as np
fn = sys.argv[1]
d = json.load(gzip.open(fn) if fn.endswith('.gz') else open(fn)); S = d['series']; E = d['events']
MINLIFE = int(sys.argv[2]) if len(sys.argv) > 2 else 20
parent = {}; efate = {}
for t, ty, p, ch in E:
    if ty == 'death': efate[p[0]] = 'death'
for t, ty, p, ch in E:
    if ty == 'split':
        for c in ch: parent[c] = p[0]
out = {"file": fn}
for key in ('ym', 'zm'):
    W = B = 0.0; tot = 0.0; series = []; BD = [0.0, 0.0, 0.0]
    for a in range(len(S) - 1):
        x0, x1 = S[a], S[a + 1]
        if not x0['n'] or not x1['n']: continue
        n0 = np.array(x0['np'], float); y0 = np.array(x0[key]); m0 = np.average(y0, weights=n0)
        n1 = np.array(x1['np'], float); y1 = np.array(x1[key]); m1 = np.average(y1, weights=n1)
        idx0 = {c: i for i, c in enumerate(x0['id'])}
        w1 = n1 / n1.sum(); wi = 0.0
        for j, c in enumerate(x1['id']):
            anc = c if c in idx0 else parent.get(c)
            if anc is not None and anc in idx0:
                wi += w1[j] * (y1[j] - y0[idx0[anc]])
        # split the between term by the ancestor's eventual fate: (W'_anc - w_anc)(y_anc - m0)
        w0 = n0 / n0.sum(); Wn = np.zeros(len(y0)); bna = 0.0
        for j, c in enumerate(x1['id']):
            anc = c if c in idx0 else parent.get(c)
            if anc is not None and anc in idx0: Wn[idx0[anc]] += w1[j]
            else: bna += w1[j] * (y1[j] - m0)
        for i, c in enumerate(x0['id']):
            ctr = (Wn[i] - w0[i]) * (y0[i] - m0)
            if efate.get(c) == 'death': BD[0] += ctr
            else: BD[1] += ctr
        BD[2] += bna
        W += wi; tot += m1 - m0; B += (m1 - m0) - wi
        series.append((x1['t'], round(tot, 4), round(W, 4), round(B, 4)))
    first = [x for x in S if x['n']][0]; last = [x for x in S if x['n']][-1]
    out[key] = dict(start=round(float(np.average(first[key], weights=first['np'])), 4),
                    end=round(float(np.average(last[key], weights=last['np'])), 4),
                    total_change=round(tot, 4), within_cells=round(W, 4), between_cells=round(B, 4),
                    between_by_fate=dict(cells_that_die=round(BD[0], 4), other_cells=round(BD[1], 4), no_ancestor=round(BD[2], 4)),
                    checkpoints=[series[k] for k in np.linspace(0, len(series) - 1, 6).astype(int)])
# within-life change of mature cells, by fate
pos = {}
for a, x in enumerate(S):
    for i, c in enumerate(x['id']): pos.setdefault(c, []).append((a, i))
fate = {}
for t, ty, p, ch in E:
    if ty == 'death': fate[p[0]] = 'death'
    elif ty == 'split' and len(ch) >= 2: fate[p[0]] = 'split'
life = {'death': [], 'split': [], 'other': []}; lifez = {'death': [], 'split': [], 'other': []}
for c, L in pos.items():
    if len(L) < MINLIFE or S[L[0][0]]['t'] <= 1000: continue
    (a0, i0), (a1, i1) = L[0], L[-1]
    f = fate.get(c, 'other')
    life[f].append(S[a1]['ym'][i1] - S[a0]['ym'][i0]); lifez[f].append(S[a1]['zm'][i1] - S[a0]['zm'][i0])
out['within_life_change_mature'] = {f: dict(n=len(v), dy_mean=round(float(np.mean(v)), 4) if v else None,
                                         dz_mean=round(float(np.mean(lifez[f])), 4) if v else None) for f, v in life.items()}
# heritability at splits: parent (last snapshot before) vs daughter (first snapshot), deviations from the pop mean
def val(c, key, last):
    L = pos.get(c)
    if not L: return None
    a, i = L[-1] if last else L[0]
    x = S[a]; return x[key][i] - np.average(x[key], weights=x['np'])
for key in ('ym', 'zm'):
    P_, D_ = [], []
    for t, ty, p, ch in E:
        if ty == 'split' and len(ch) >= 2:
            pv = val(p[0], key, True)
            for c in ch:
                dv = val(c, key, False)
                if pv is not None and dv is not None and len(pos.get(c, [])) >= 10:
                    P_.append(pv); D_.append(dv)
    P_, D_ = np.array(P_), np.array(D_)
    out['split_heritability_' + key] = dict(n_pairs=len(P_), corr=round(float(np.corrcoef(P_, D_)[0, 1]), 3) if len(P_) > 2 else None,
                                            slope=round(float(np.polyfit(P_, D_, 1)[0]), 3) if len(P_) > 2 else None,
                                            mean_abs_parent_dev=round(float(np.mean(np.abs(P_))), 4) if len(P_) else None,
                                            mean_abs_daughter_minus_parent=round(float(np.mean(np.abs(D_ - P_))), 4) if len(P_) else None)
# fates by birth rank, plus off-kind daughters (daughter's birth-rank class differs from parent's class at the split)
def rank(c, a_i, key='ym'):
    a, i = a_i; x = S[a]; y = x[key][i]; o = np.array([v for j, v in enumerate(x[key]) if j != i])
    return None if not len(o) else (np.sum(o < y) + 0.5 * np.sum(o == y)) / len(o)
for key in ('ym', 'zm'):
    off = 0; npairs = 0
    for t, ty, p, ch in E:
        if ty == 'split' and len(ch) >= 2 and p[0] in pos:
            rp = rank(p[0], pos[p[0]][-1], key)
            for c in ch:
                if c in pos and len(pos[c]) >= 10:
                    rd = rank(c, pos[c][0], key)
                    if rp is not None and rd is not None:
                        npairs += 1; off += int((rp < 0.5) != (rd < 0.5))
    out['off_kind_daughters_' + key] = dict(pairs=npairs, off_kind=off)
print(json.dumps(out))
