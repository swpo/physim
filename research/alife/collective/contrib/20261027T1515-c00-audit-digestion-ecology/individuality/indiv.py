"""Auditor (individuality lens): per-track, merge-aware measurements of predators, prey and prey-predator composites
from a labkit frames.npz of c52's digestion world.
usage: indiv.py pack/seedN out.json
Tracking: labkit's own per-species functions (render channel, labkit robust-range normalisation, threshold 0.35, min area 6,
periodic), as c52's predlineage.py and c55's coinc.py/partners.py. Gap to prey: periodic Euclidean distance transform of the
labkit prey mask (3x3 tiling), min over the predator's pixels; attached = gap <= 2 px (c56's freepred.py rule).
"""
import sys, json, numpy as np, importlib.util
from collections import Counter, defaultdict
from scipy import ndimage
sys.path.insert(0, '/home/user/physim/research/alife')
from labkit import run as LR, metrics as M

pack, out = sys.argv[1], sys.argv[2]
WORLD = '/home/user/physim/research/alife/collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py'
spec = importlib.util.spec_from_file_location('w', WORLD); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
R = np.load(pack + '/frames.npz')['render'].astype(np.float32); T = len(R); H, W = R.shape[2:]; shape = (H, W)
K = 20; DTF = 100.0


def trk(ch):
    mn, thr, lo, hi = LR._normalize_matter(R[:, ch], w.META, True)
    comps, links = LR._segment_frames(mn, thr, 6, True, keep_labels=True)
    tracks, events = M.track(comps, links, shape, True)
    lin = M.lineage_stats(tracks, events, T, DTF, shape, True, K=K)
    return comps, tracks, events, lin, (lo + thr * (hi - lo))


pc, pt, pe, pl, pthr = trk(0)   # prey
qc, qt, qe, ql, qthr = trk(1)   # predator
print('prey thr (render units, before blur)', pthr, 'pred thr', qthr)
print('prey tracks', len(pt), 'persistent splits', len(pl['persistent_splits']), 'gen', pl['max_generation'],
      '| pred tracks', len(qt), 'persistent splits', len(ql['persistent_splits']), 'gen', ql['max_generation'])

# ---- periodic distance to prey, per frame
def edt_to(mask):
    big = np.tile(~mask, (3, 3)); d = ndimage.distance_transform_edt(big); return d[H:2 * H, W:2 * W]
DP = [edt_to(pc[f]['lab'] > 0) for f in range(T)]
def dil(m, it=2):
    return ndimage.binary_dilation(np.tile(m, (3, 3)), iterations=it)[H:2 * H, W:2 * W]

# prey track id per (frame, comp)
ptid = {}
for t in pt:
    for k, ci in enumerate(t['comp']): ptid[(t['start'] + k, ci)] = t['id']
qtid = {}
for t in qt:
    for k, ci in enumerate(t['comp']): qtid[(t['start'] + k, ci)] = t['id']

# prey lineage root: follow split parents only (a merge child gets a new root = itself)
def prey_root(i):
    while pt[i]['birth'] == 'split' and pt[i]['parents']:
        i = pt[i]['parents'][0]
    return i
def prey_anc(i):
    s = {i}; st = [i]
    while st:
        j = st.pop()
        for p in pt[j]['parents']:
            if p not in s: s.add(p); st.append(p)
    return s

def qmask(f, ci): return qc[f]['lab'] == ci + 1
def pmask(f, ci): return pc[f]['lab'] == ci + 1

def prey_touched(f, m):
    ls = np.unique(pc[f]['lab'][dil(m, 2)]); return sorted({ptid[(f, l - 1)] for l in ls if l > 0 and (f, l - 1) in ptid})

# ---- per predator track measurements
F0 = 25  # predator noise at t=2000 (frame 20); bodies exist from frame ~21
rows = []
for t in qt:
    if t['start'] < 21: continue
    span = t['end'] - t['start'] + 1
    gaps = []; partners = []; areas = []
    for k, ci in enumerate(t['comp']):
        f = t['start'] + k; m = qmask(f, ci)
        gaps.append(float(DP[f][m].min())); areas.append(float(m.sum()))
        for i in prey_touched(f, m):
            if i not in partners: partners.append(i)
    # unrelated partners (neither in the other's ancestry, merges included as c55)
    roots = []
    for i in partners:
        a = prey_anc(i)
        if not any(r in a or i in prey_anc(r) for r in roots): roots.append(i)
    # end kind
    if t['end'] >= T - 1: endk = 'alive_end'
    elif not t['children']: endk = 'dissolved'
    else:
        kinds = {qt[c]['birth'] for c in t['children']}
        endk = 'split' if 'split' in kinds else 'merge'
    # formation: frames from start to first frame with area >= 0.5 * median area of the track
    med = np.median(areas); form = next(k for k, a in enumerate(areas) if a >= 0.5 * med)
    rows.append(dict(id=t['id'], start=t['start'], end=t['end'], span=span, birth=t['birth'], endk=endk,
                     frac_attached=float(np.mean(np.array(gaps) <= 2)), max_gap=float(max(gaps)),
                     n_prey_tracks=len(partners), n_unrelated_prey=len(roots),
                     area_min=float(min(areas)), area_med=float(med), area_max=float(max(areas)), formation_frames=int(form)))

def summ(sel, name):
    if not sel: return {name: 'none'}
    a = lambda k: np.array([r[k] for r in sel])
    return {name: dict(n=len(sel), span_median_t=float(np.median(a('span'))) * DTF, span_max_t=float(a('span').max()) * DTF,
                       frac_attached_median=float(np.median(a('frac_attached'))), frac_attached_mean=float(a('frac_attached').mean()),
                       always_attached=int((a('frac_attached') == 1).sum()), ever_free=int((a('frac_attached') < 1).sum()),
                       one_prey_lineage=int((a('n_unrelated_prey') <= 1).sum()), ge2_unrelated_prey=int((a('n_unrelated_prey') >= 2).sum()),
                       zero_prey=int((a('n_prey_tracks') == 0).sum()),
                       area_med_median=float(np.median(a('area_med'))), area_max_max=float(a('area_max').max()),
                       area_max_over_min_median=float(np.median(a('area_max') / a('area_min'))),
                       area_max_over_med_p95=float(np.percentile(a('area_max') / a('area_med'), 95)),
                       formation_frames_median=float(np.median(a('formation_frames'))),
                       births=dict(Counter(a('birth').tolist())), ends=dict(Counter(a('endk').tolist())))}

res = {'pack': pack, 'T': T, 'thr_prey': float(pthr), 'thr_pred': float(qthr),
       'prey': {'tracks': len(pt), 'persistent_splits': len(pl['persistent_splits']), 'max_gen': pl['max_generation'],
                'splits': sum(e['type'] == 'split' for e in pe), 'merges': sum(e['type'] == 'merge' for e in pe)},
       'pred': {'tracks': len(qt), 'persistent_splits': len(ql['persistent_splits']), 'max_gen': ql['max_generation'],
                'splits': sum(e['type'] == 'split' for e in qe), 'merges': sum(e['type'] == 'merge' for e in qe)}}
res.update(summ([r for r in rows if r['span'] >= 10], 'pred_tracks_ge10'))
res.update(summ([r for r in rows if r['span'] >= 20], 'pred_tracks_ge20'))
res.update(summ([r for r in rows if r['span'] >= 60], 'pred_tracks_ge60'))
# births after the founders: nucleation vs split, among tracks that reach >= 10 frames
late = [r for r in rows if r['start'] >= 30]
res['pred_births_after_t3000'] = {k: dict(all=sum(r['birth'] == k for r in late), reach10=sum(r['birth'] == k and r['span'] >= 10 for r in late))
                                  for k in ('nucleation', 'split', 'merge')}
# where do late-nucleated predator bodies appear? attached at birth?
nuc = [r for r in late if r['birth'] == 'nucleation' and r['span'] >= 10]
res['late_nucleations_reach10_attached_frac_median'] = float(np.median([r['frac_attached'] for r in nuc])) if nuc else None

# late nucleations of predators (>= 10 frames): de novo condensation from the bath, or a body that flickered below threshold?
Rb = R[:, 1]
nucl = []
for r in nuc:
    t = qt[r['id']]; f = t['start']; m = qmask(f, t['comp'][0]); md = dil(m, 2)
    prev_max = float(Rb[f - 1][md].max()); prev_comp = bool((qc[f - 1]['lab'][dil(m, 3)] > 0).any())
    pr = prey_touched(f, m)
    # did the touched prey carry another predator body in the previous frame?
    prey_had_pred = False
    for i in pr:
        tr = pt[i]
        if tr['start'] <= f - 1 <= tr['end']:
            pmk = pmask(f - 1, tr['comp'][f - 1 - tr['start']])
            if (qc[f - 1]['lab'][dil(pmk, 2)] > 0).any(): prey_had_pred = True
    # where did the prey come from: a prey split within the last 10 frames?
    prey_recent_split = any(pt[i]['birth'] == 'split' and f - pt[i]['start'] <= 10 for i in pr)
    nucl.append(dict(f=f, area=r['area_med'], prev_max_cb=prev_max, prev_pred_comp_within3=prev_comp, prey_had_pred=prey_had_pred,
                     prey_recent_split=prey_recent_split, on_prey=bool(pr)))
res['late_nucleations_reach10'] = dict(n=len(nucl), prev_pred_comp_within3=sum(x['prev_pred_comp_within3'] for x in nucl),
                                       prev_max_cb_median=float(np.median([x['prev_max_cb'] for x in nucl])) if nucl else None,
                                       de_novo_prev_max_lt_0p25=sum(x['prev_max_cb'] < 0.25 for x in nucl),
                                       on_prey=sum(x['on_prey'] for x in nucl), on_prey_that_had_pred=sum(x['prey_had_pred'] for x in nucl),
                                       on_prey_from_split_le1000t=sum(x['prey_recent_split'] for x in nucl))
res['bath_cb_median_t6000'] = float(np.median(Rb[60][qc[60]['lab'] == 0]))
# predator deaths (dissolved) among tracks >= 10 frames: attached at the end? did its prey survive the next frame?
deaths = []
for r in rows:
    if r['span'] < 10 or r['endk'] != 'dissolved': continue
    t = qt[r['id']]; f = t['end']; m = qmask(f, t['comp'][-1]); pr = prey_touched(f, m)
    prey_alive = any(pt[i]['end'] > f or any(pt[c]['start'] == f + 1 for c in pt[i]['children']) for i in pr)
    a = t['area']; trend = float(a[-1] / max(a[max(0, len(a) - 6)], 1))
    deaths.append(dict(f=f, gap=float(DP[f][m].min()), n_prey=len(pr), prey_survives=prey_alive, area_last=float(a[-1]), area_ratio_last_vs_5before=trend))
res['pred_deaths_dissolved_ge10'] = dict(n=len(deaths), attached_at_end=sum(d['gap'] <= 2 for d in deaths),
                                         its_prey_survives=sum(d['prey_survives'] for d in deaths), free_at_end=sum(d['gap'] > 2 for d in deaths),
                                         area_last_median=float(np.median([d['area_last'] for d in deaths])) if deaths else None)
# prey births after t=3000 by kind (tracks reaching >= 10 frames)
res['prey_births_after_t3000'] = {k: dict(all=sum(t['birth'] == k and t['start'] >= 30 for t in pt),
                                          reach10=sum(t['birth'] == k and t['start'] >= 30 and t['end'] - t['start'] + 1 >= 10 for t in pt))
                                  for k in ('nucleation', 'split', 'merge')}

# ---- per-frame contact structure (composite body plan)
deg_prey = Counter(); deg_pred = Counter(); frac_free = []
for f in range(30, T, 2):
    lq, nq = qc[f]['lab'], qc[f]['n']; lp, np_ = pc[f]['lab'], pc[f]['n']
    preds_of_prey = defaultdict(set); prey_of_pred = {}
    for j in range(nq):
        m = lq == j + 1; ls = np.unique(lp[dil(m, 2)]); ls = [l - 1 for l in ls if l > 0]
        prey_of_pred[j] = ls
        for l in ls: preds_of_prey[l].add(j)
    for i in range(np_): deg_prey[min(len(preds_of_prey[i]), 3)] += 1
    for j in range(nq): deg_pred[min(len(prey_of_pred[j]), 3)] += 1
    frac_free.append(np.mean([len(v) == 0 for v in prey_of_pred.values()]) if nq else 0)
tot = lambda c: {str(k): round(v / sum(c.values()), 3) for k, v in sorted(c.items())}
res['contact_t3000plus'] = {'predators_per_prey(0,1,2,3+)': tot(deg_prey), 'prey_per_predator(0,1,2,3+)': tot(deg_pred),
                            'pred_free_frac_mean': float(np.mean(frac_free))}

# ---- persistent predator splits: classification and daughter follow-up
prey_split_ev = [e for e in pe if e['type'] == 'split']
def lineage_alive(c, f):
    """largest-area descendant of track c (through splits only) alive at frame f, or None"""
    best = None; st = [c]
    while st:
        i = st.pop(); tr = qt[i]
        if tr['start'] <= f <= tr['end']:
            a = tr['area'][f - tr['start']]
            if best is None or a > best[1]: best = (i, a)
        for ch in tr['children']:
            if qt[ch]['birth'] == 'split': st.append(ch)
    return best
def desc_all(c):
    return M.descendants(qt, c)
splits = []
for e in ql['persistent_splits']:
    f = e['frame']; par = qt[e['parent']]; kids = e['surviving_children']
    pm = qmask(f - 1, par['comp'][-1]); P_par = prey_touched(f - 1, pm)
    kid_prey = [prey_touched(f, qmask(f, qt[c]['comp'][0])) for c in kids]
    kid_gap = [float(DP[f][qmask(f, qt[c]['comp'][0])].min()) for c in kids]
    # prey split near in time whose parent was touched by the predator parent or whose child is touched by a predator daughter
    touched = set(P_par) | {i for kp in kid_prey for i in kp}
    ps = [pe_ for pe_ in prey_split_ev if f - 2 <= pe_['frame'] <= f + 2 and (pe_['parent'] in touched or any(c in touched for c in pe_['children']))]
    # map kid prey to lineage roots at the split frame
    kroots = [set(prey_root(i) for i in kp) for kp in kid_prey]
    A0 = set(kid_prey[0]); A1 = set(kid_prey[1]) if len(kid_prey) > 1 else set()
    lag = None
    if ps: cls = 'pinched_with_dividing_prey(+-2 frames)'
    elif A0 and A1 and not (A0 & A1):
        # torn between two prey bodies: are they sisters from a recent prey split? lag = f - frame of the most recent common split
        best = None
        for a in A0:
            for b in A1:
                C = prey_anc(a) & prey_anc(b)
                if C:
                    mrca_end = max(pt[c]['end'] for c in C)
                    if best is None or mrca_end > best: best = mrca_end
        if best is not None and f - (best + 1) <= 20:
            lag = int(f - (best + 1)); cls = 'torn_between_sister_prey(prey split <=2000t before)'
        else:
            cls = 'torn_between_unrelated_prey'
    elif A0 and A1 and (A0 & A1):
        cls = 'pinched_on_one_prey_no_prey_split'
    else:
        cls = 'other(daughter_free)'
    # follow daughters
    fol = {}
    for dtf in (5, 10, 20):
        g = f + dtf
        if g >= T: continue
        st = []
        for c in kids:
            la = lineage_alive(c, g)
            if la is None: st.append(None); continue
            i, a = la; m = qmask(g, qt[i]['comp'][g - qt[i]['start']])
            pr = prey_touched(g, m)
            st.append(dict(area=float(a), gap=float(DP[g][m].min()), prey_roots=sorted({prey_root(x) for x in pr}), prey_tracks=pr))
        fol[dtf] = st
    # re-merge of daughters' descendants at any time to the end
    d0, d1 = desc_all(kids[0]), desc_all(kids[1]) if len(kids) > 1 else set()
    remerge = sorted(d0 & d1)
    remerge_f = min(qt[i]['start'] for i in remerge) if remerge else None
    splits.append(dict(frame=f, t=f * DTF, parent=e['parent'], parent_area=float(pm.sum()), parent_prey=len(P_par),
                       parent_gap=float(DP[f - 1][pm].min()), kids=kids, kid_areas=[float(qt[c]['area'][0]) for c in kids],
                       kid_gap=kid_gap, kid_prey_roots=[sorted(k) for k in kroots], cls=cls, prey_split_near=len(ps), sister_lag_frames=lag,
                       follow=fol, remerge_frame=remerge_f))
res['pred_persistent_split_classes'] = dict(Counter(s['cls'] for s in splits))
res['pred_split_sister_lags_frames'] = sorted(s['sister_lag_frames'] for s in splits if s['sister_lag_frames'] is not None)
res['pred_persistent_split_frames'] = [s['frame'] for s in splits]
def fstat(dtf):
    ok = [s for s in splits if dtf in s['follow']]
    both_alive = [s for s in ok if all(x is not None for x in s['follow'][dtf])]
    both_att = [s for s in both_alive if all(x['gap'] <= 2 for x in s['follow'][dtf])]
    diff_prey = [s for s in both_att if len(s['follow'][dtf]) >= 2 and not (set(s['follow'][dtf][0]['prey_tracks']) & set(s['follow'][dtf][1]['prey_tracks']))]
    diff_lin = [s for s in both_att if len(s['follow'][dtf]) >= 2 and not (set(s['follow'][dtf][0]['prey_roots']) & set(s['follow'][dtf][1]['prey_roots']))]
    return dict(n=len(ok), both_alive=len(both_alive), both_attached=len(both_att), attached_to_different_prey_bodies=len(diff_prey),
                attached_to_unrelated_prey_lineages=len(diff_lin))
res['pred_split_followup'] = {f'+{d * 100}t': fstat(d) for d in (5, 10, 20)}
res['pred_split_remerged_ever'] = sum(s['remerge_frame'] is not None for s in splits)
res['pred_split_parent_free'] = sum(s['parent_gap'] > 2 for s in splits)
res['pred_split_kid_area_over_parent_median'] = float(np.median([min(s['kid_areas']) / s['parent_area'] for s in splits])) if splits else None
res['pred_splits'] = splits

# ---- prey persistent splits: is a predator the cutter?
qsplit_ev = [e for e in qe if e['type'] == 'split']
psr = []
for e in pl['persistent_splits']:
    f = e['frame']; par = pt[e['parent']]; kids = e['surviving_children']
    pm = pmask(f - 1, par['comp'][-1])
    km = np.zeros_like(pm)
    for c in pt[e['parent']]['children']:
        km |= pmask(f, pt[c]['comp'][0])
    neck = pm & ~dil(km, 1)          # parent pixels not near any daughter at f
    predf = qc[f]['lab'] > 0
    neck_pred = float(predf[neck].mean()) if neck.any() else None
    # one predator body touching >= 2 daughters at f (bridge)
    kms = [dil(pmask(f, pt[c]['comp'][0]), 2) for c in kids]
    bridge = False
    for j in np.unique(qc[f]['lab'][predf]):
        mj = qc[f]['lab'] == j
        if sum(bool((mj & k).any()) for k in kms) >= 2: bridge = True; break
    near_pred = bool((predf & dil(pm, 6)).any())
    coinc = any(abs(q['frame'] - f) <= 1 and any(bool((dil(qmask(q['frame'], qt[c]['comp'][0]), 6) & dil(pm, 2)).any()) for c in q['children']) for q in qsplit_ev)
    fol = {}
    for dtf in (10, 20):
        g = f + dtf
        if g >= T: continue
        st = []
        for c in kids:
            best = None; stck = [c]
            while stck:
                i = stck.pop(); tr = pt[i]
                if tr['start'] <= g <= tr['end']:
                    a = tr['area'][g - tr['start']]
                    if best is None or a > best[1]: best = (i, a)
                stck += [ch for ch in tr['children'] if pt[ch]['birth'] == 'split']
            if best is None: st.append(None); continue
            i, a = best; m = pmask(g, pt[i]['comp'][g - pt[i]['start']])
            npred = len({l for l in np.unique(qc[g]['lab'][dil(m, 2)]) if l > 0})
            st.append(dict(area=float(a), n_pred=npred))
        fol[dtf] = st
    psr.append(dict(frame=f, parent_area=float(pm.sum()), kid_areas=[float(pt[c]['area'][0]) for c in kids],
                    neck_px=int(neck.sum()), neck_pred_frac=neck_pred, bridge=bridge, pred_within6=near_pred, coinc_pred_split=coinc, follow=fol))
res['prey_split_summary'] = dict(n=len(psr), pred_within6=sum(p['pred_within6'] for p in psr), bridge_pred_touching_both_daughters=sum(p['bridge'] for p in psr),
                                 neck_pred_frac_median=float(np.median([p['neck_pred_frac'] for p in psr if p['neck_pred_frac'] is not None])) if psr else None,
                                 neck_mostly_pred=sum((p['neck_pred_frac'] or 0) >= 0.5 for p in psr), coinc_pred_split=sum(p['coinc_pred_split'] for p in psr),
                                 kid_area_over_parent_median=float(np.median([min(p['kid_areas']) / p['parent_area'] for p in psr])) if psr else None)
def pf(dtf):
    ok = [p for p in psr if dtf in p['follow'] and all(x is not None for x in p['follow'][dtf])]
    grow = [max(x['area'] for x in p['follow'][dtf]) / p['parent_area'] for p in ok]
    two_pairs = sum(all(x['n_pred'] >= 1 for x in p['follow'][dtf]) for p in ok)
    return dict(n_both_alive=len(ok), largest_kid_area_over_parent_median=float(np.median(grow)) if grow else None,
                both_kids_carry_predator=two_pairs)
res['prey_split_followup'] = {f'+{d * 100}t': pf(d) for d in (10, 20)}
res['prey_splits'] = psr

# ---- composite (prey U predator) tracking: does the pair keep one body plan and divide into two pairs?
U = np.stack([((pc[f]['lab'] > 0) | (qc[f]['lab'] > 0)).astype(np.float32) for f in range(T)])
comps, links = LR._segment_frames(U, 0.5, 6, True, keep_labels=True)
ct, ce = M.track(comps, links, shape, True)
cl = M.lineage_stats(ct, ce, T, DTF, shape, True, K=K)
csp = sum(e['type'] == 'split' for e in ce); cme = sum(e['type'] == 'merge' for e in ce)
# body plan per composite after t=3000: (n prey comps, n pred comps)
plan = Counter()
for f in range(30, T, 2):
    lab = comps[f]['lab']
    for j in range(comps[f]['n']):
        m = lab == j + 1
        npy = len(np.unique(pc[f]['lab'][m & (pc[f]['lab'] > 0)])); npd = len(np.unique(qc[f]['lab'][m & (qc[f]['lab'] > 0)]))
        plan[f'{min(npy, 3)}prey_{min(npd, 3)}pred'] += 1
tp = sum(plan.values())
# composite persistent splits: do both daughters carry 1 prey + >=1 predator at +K?
def cplan(f, ci):
    m = comps[f]['lab'] == ci + 1
    return (len(np.unique(pc[f]['lab'][m & (pc[f]['lab'] > 0)])), len(np.unique(qc[f]['lab'][m & (qc[f]['lab'] > 0)])))
cps = []
for e in cl['persistent_splits']:
    f = e['frame']; par = ct[e['parent']]
    pp = cplan(f - 1, par['comp'][-1]); kp = [cplan(f, ct[c]['comp'][0]) for c in e['surviving_children']]
    cps.append(dict(frame=f, parent_plan=pp, kid_plans=kp, parent_birth=par['birth']))
res['composite'] = dict(tracks=len(ct), splits=csp, merges=cme, merge_split=round(cme / csp, 3) if csp else None,
                        persistent_splits=len(cl['persistent_splits']), max_gen=cl['max_generation'],
                        persistent_tracks_ge60=int(sum(t['end'] - t['start'] + 1 >= 60 for t in ct)),
                        body_plans_t3000plus={k: round(v / tp, 3) for k, v in plan.most_common(8)},
                        persistent_split_kids_both_1prey_ge1pred=sum(all(k[0] == 1 and k[1] >= 1 for k in s['kid_plans']) for s in cps),
                        persistent_split_parent_plans=dict(Counter(f"{min(s['parent_plan'][0],3)}p{min(s['parent_plan'][1],3)}q" for s in cps)),
                        persistent_split_parent_born_by=dict(Counter(s['parent_birth'] for s in cps)))
# composite track lifetimes vs formation (frames) after t=3000
cl_l = [t['end'] - t['start'] + 1 for t in ct if t['start'] >= 30]
res['composite']['span_median_t_after3000'] = float(np.median(cl_l)) * DTF if cl_l else None

json.dump(res, open(out, 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
print(json.dumps({k: v for k, v in res.items() if k not in ('pred_splits', 'prey_splits')}, indent=1, default=str))
