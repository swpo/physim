"""(heredity2: adds mutation-aware flips and per-kind births/deaths)
python heredity.py out_prefix seed T : runs world.py (WORLD_P honoured), records T, a, b every 1 t, segments and tracks
the caps with labkit's own segmentation and tracker on T, and for every cap (component) computes its label share
s = sum(a)/(sum(a)+sum(b)) over its mask. Reports: label purity of caps after labelling; at every persistent split after
lab_t, the parent's kind (s>0.5) at its last frame and each surviving daughter's kind at its first frame (agreement);
conversions = tracks alive >= 20 t whose kind flips between their first and last 5 frames; kind counts over time."""
import sys, os, json, importlib.util, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife')
from labkit import run as R, metrics as M
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('w', os.path.join(here, 'world_claimed.py')); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
out, seed, Tend = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
N = int(os.environ.get('SIZE', 128)); s = w.init(seed, (N, N)); dt = w.P['dt']; per = int(round(1 / dt)); n = int(Tend / dt)
TT, AA, BB = [], [], []
for i in range(n + 1):
    if i % per == 0:
        TT.append(s['T'].astype(np.float32)); AA.append(s['a'].astype(np.float16)); BB.append(s['b'].astype(np.float16))
    if i < n: s = w.step(s)
mat = np.stack(TT); mn, thr, lo, hi = R._normalize_matter(mat, w.META, True, w.META.get('threshold'))
H, W = mat.shape[1:]
comps, links = R._segment_frames(mn, thr, R._default_min_area(H, W), True, keep_labels=True)
tracks, events = M.track(comps, links, (H, W), True)
lin = M.lineage_stats(tracks, events, len(mn), 1.0, (H, W), True, 20)
lab_t = int(w.P['lab_t'])
def share(f, ci):
    m = comps[f]['lab'] == ci + 1; a = float(AA[f][m].astype(np.float32).sum()); b = float(BB[f][m].astype(np.float32).sum())
    return a / (a + b) if a + b > 1e-6 else np.nan
purity = []; counts = []
for f in range(lab_t + 5, len(mn), 5):
    ss = [share(f, ci) for ci in range(comps[f]['n'])]; ss = [x for x in ss if np.isfinite(x)]
    purity += [max(x, 1 - x) for x in ss]; counts.append((f, sum(x > 0.5 for x in ss), sum(x <= 0.5 for x in ss)))
agree = dis = 0; rows = []
for e in lin['persistent_splits']:
    if e['frame'] <= lab_t + 2: continue
    p = tracks[e['parent']]; sp = share(p['end'], p['comp'][-1])
    for c in e['surviving_children']:
        t = tracks[c]; sc = share(t['start'], t['comp'][0])
        if not (np.isfinite(sp) and np.isfinite(sc)): continue
        ok = (sp > 0.5) == (sc > 0.5); agree += ok; dis += (not ok); rows.append((e['frame'], round(sp, 3), round(sc, 3)))
conv = 0; ntr = 0
for t in tracks:
    if t['start'] <= lab_t + 2 or t['end'] - t['start'] < 20: continue
    a0 = np.nanmean([share(t['start'] + k, t['comp'][k]) for k in range(5)]); a1 = np.nanmean([share(t['end'] - k, t['comp'][-1 - k]) for k in range(5)])
    ntr += 1; conv += (a0 > 0.5) != (a1 > 0.5)
muts = s.get('mutations', [])
def near_mut(f, cy, cx):
    for (tm, my, mx) in muts:
        if -2 <= f - tm <= 15 and np.hypot((cy - my + H / 2) % H - H / 2, (cx - mx + W / 2) % W - W / 2) <= 12: return True
    return False
flips_mut = flips_other = 0
for t in tracks:
    if t['start'] <= lab_t + 2 or t['end'] - t['start'] < 10: continue
    ks = [share(t['start'] + k, ci) for k, ci in enumerate(t['comp'])]
    for k in range(5, len(ks)):
        if np.isfinite(ks[k]) and np.isfinite(ks[k - 5]) and (ks[k] > 0.5) != (ks[k - 5] > 0.5) and all(np.isfinite(ks[j]) and ((ks[j] > 0.5) == (ks[k] > 0.5)) for j in range(k, min(k + 5, len(ks)))):
            f = t['start'] + k
            if near_mut(f, t['cy'][k], t['cx'][k]): flips_mut += 1
            else: flips_other += 1
            break
births = {'a': 0, 'b': 0}; deaths = {'a': 0, 'b': 0}; last = len(mn) - 1
for e in lin['persistent_splits']:
    if e['frame'] <= lab_t + 2: continue
    for c in e['surviving_children']:
        sc = share(tracks[c]['start'], tracks[c]['comp'][0])
        if np.isfinite(sc): births['a' if sc > 0.5 else 'b'] += 1
for t in tracks:
    if t['start'] <= lab_t + 2 or t['children'] or t['end'] >= last - 1 or t['end'] - t['start'] < 10: continue
    sd = share(t['end'], t['comp'][-1])
    if np.isfinite(sd): deaths['a' if sd > 0.5 else 'b'] += 1
res = {'seed': seed, 'WORLD_P': os.environ.get('WORLD_P', '{}'), 'persistent_splits_after_label': agree + dis, 'daughter_agree': agree, 'daughter_disagree': dis,
       'cap_purity_median': float(np.median(purity)) if purity else None, 'cap_purity_p10': float(np.percentile(purity, 10)) if purity else None,
       'tracks_ge20': ntr, 'conversions': conv, 'mutations': len(muts), 'flips_at_mutation': flips_mut, 'flips_elsewhere': flips_other, 'births_by_kind': births, 'deaths_by_kind': deaths, 'kind_counts_a_b': counts[::10] + [counts[-1]], 'kind_counts_all': counts, 'split_rows': rows}
json.dump(res, open(out + '.json', 'w'), indent=0, default=lambda o: o.item())
print({k: v for k, v in res.items() if k not in ('split_rows',)})
