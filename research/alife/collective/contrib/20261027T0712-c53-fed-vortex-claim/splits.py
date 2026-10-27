"""python splits.py <pack_seed_dir> [out.png] : labkit's own segmentation, tracker and lineage (merge-aware, K=20 frames) on
|omega|; every track's sign read from the rendered signed-vorticity channel at a rendered frame inside its life. Reports, for
persistent splits, whether the daughters have the parent's sign; for merges, whether same-sign or opposite-sign bodies
merged; the generation of each split; and draws |omega| crops of up to 4 randomly chosen persistent splits at the deepest
two generations (parent 6 frames before the split to daughters 6 frames after). Writes splits.json next to frames.npz."""
import sys, json, importlib.util, os, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife')
from labkit import run as R, metrics as M
pack = sys.argv[1]
spec = importlib.util.spec_from_file_location('w', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'world.py')); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
F = np.load(f'{pack}/frames.npz'); mat = F['matter'].astype(np.float32); RR = F['render'].astype(np.float32); rf = list(F['render_f'])
m = json.load(open(f'{pack}/metrics.json')); dtf = m['steps_per_frame'] * m['dt']
mn, thr, lo, hi = R._normalize_matter(mat, W.META, True, W.META.get('threshold')); H, Wd = mn.shape[1:]
comps, links = R._segment_frames(mn, thr, R._default_min_area(H, Wd), True, keep_labels=True)
tracks, events = M.track(comps, links, (H, Wd), True)
lin = M.lineage_stats(tracks, events, len(mn), dtf, (H, Wd), True, 20)
def sign(tid):
    t = tracks[tid]
    for k, ci in enumerate(t['comp']):
        f = t['start'] + k
        if f in rf:
            mask = comps[f]['lab'] == ci + 1
            return int(np.sign(RR[rf.index(f), 2][mask].sum()))
    return 0
ps = lin['persistent_splits']; same = diff = unk = 0; rows = []
gen = lin.get('generation', {})
for e in ps:
    sp = sign(e['parent']); sc = [sign(c) for c in e['surviving_children']]
    if sp == 0 or 0 in sc: unk += 1
    elif all(x == sp for x in sc): same += 1
    else: diff += 1
    rows.append({'frame': e['frame'], 't': e['frame'] * dtf, 'parent': e['parent'], 'children': e['surviving_children'], 'sign_parent': sp, 'sign_children': sc,
                 'generation': max([gen.get(c, gen.get(str(c), 0)) for c in e['surviving_children']] or [0])})
mg_same = mg_opp = mg_unk = 0
for ev in events:
    if ev.get('type') != 'merge': continue
    ss = [sign(p) for p in ev.get('parents', [])]
    if 0 in ss or len(ss) < 2: mg_unk += 1
    elif len(set(ss)) == 1: mg_same += 1
    else: mg_opp += 1
out = {'pack': pack, 'persistent_splits': len(ps), 'daughters_same_sign': same, 'daughters_other_sign': diff, 'sign_unknown': unk,
       'merges_same_sign': mg_same, 'merges_opposite_sign': mg_opp, 'merges_unknown': mg_unk,
       'max_generation': max([r['generation'] for r in rows] or [0]), 'splits': rows}
json.dump(out, open(f'{pack}/splits.json', 'w'), indent=0)
print({k: v for k, v in out.items() if k != 'splits'})
if len(sys.argv) > 2:
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    rng = np.random.default_rng(0); gmax = out['max_generation']
    pool = [r for r in rows if r['generation'] >= gmax - 1]; pick = [pool[i] for i in sorted(rng.choice(len(pool), min(4, len(pool)), replace=False))]
    offs = [-6, -3, 0, 3, 6, 12]
    fig, ax = plt.subplots(len(pick), len(offs), figsize=(1.6 * len(offs), 1.7 * len(pick)), squeeze=False)
    for i, r in enumerate(pick):
        p = tracks[r['parent']]; cy, cx = p['cy'][-1], p['cx'][-1]
        for j, o in enumerate(offs):
            f = min(max(r['frame'] + o, 0), len(mat) - 1)
            img = np.roll(np.roll(mat[f], int(H / 2 - cy), 0), int(Wd / 2 - cx), 1)[H // 2 - 20:H // 2 + 20, Wd // 2 - 20:Wd // 2 + 20]
            ax[i, j].imshow(img, origin='lower', cmap='magma', vmin=0, vmax=0.25); ax[i, j].set_xticks([]); ax[i, j].set_yticks([])
            ax[i, j].set_title(f't={f * dtf:.0f}', fontsize=7)
        ax[i, 0].set_ylabel(f"gen {r['generation']}\nsign {r['sign_parent']:+d}->{r['sign_children']}", fontsize=7)
    fig.suptitle(f'{pack}: randomly chosen persistent splits at generation >= {gmax - 1} (|omega|, crops 40 px)', fontsize=8)
    plt.tight_layout(); plt.savefig(sys.argv[2], dpi=80)
