"""c55 pairtest: is a 'guest' body (predator, consumer) an individual of its own, or one half of a guest-host pair?
Works on a labkit pack (frames.npz 'render') with two species channels. Both species are segmented and tracked with
labkit's own functions (labkit normalisation, min area 6, periodic, K-frame lineage window), as c52's predlineage.py does.

Measures:
  coincidence   persistent guest splits that happen within +-df frames and r px of any host split (track born by split).
                A guest that divides only because its host pinches scores near 1; a guest that divides on its own near 0.
  touching      share of guest bodies (render > 0.5) touching a host body (render > 0.5, dilated 2 px), every 10th frame.
  partners      for every guest track living >= L frames: how many host tracks it touches over its life, how many of
                those are unrelated by host ancestry, and the share of its frames touching no host.
usage:  python pairtest.py PACK_DIR WORLD.py OUT.json [--host 0] [--guest 1] [--K 20] [--dtf 100] [--L 20]
import: pairtest.run(pack_dir, world_py, host=0, guest=1, K=20, dtf=100.0, L=20) -> dict
"""
import sys, json, importlib.util, argparse
import numpy as np
from scipy import ndimage
sys.path.insert(0, '/home/user/physim/research/alife')
from labkit import run as LR, metrics as M


def _track(R, ch, meta, K, dtf):
    T, shape = len(R), R.shape[2:]
    mn, thr, lo, hi = LR._normalize_matter(R[:, ch], meta, True)
    comps, links = LR._segment_frames(mn, thr, 6, True, keep_labels=True)
    tracks, events = M.track(comps, links, shape, True)
    lin = M.lineage_stats(tracks, events, T, dtf, shape, True, K=K)
    return comps, tracks, lin


def _wd(a, b, L):
    return (a - b + L / 2) % L - L / 2


def run(pack, wpath, host=0, guest=1, K=20, dtf=100.0, L=20, df=1, r=20.0):
    spec = importlib.util.spec_from_file_location('w', wpath); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
    R = np.load(pack + '/frames.npz')['render'].astype(np.float32); T = len(R); H, W = R.shape[2:]
    hc, ht, hl = _track(R, host, w.META, K, dtf); gc, gt, gl = _track(R, guest, w.META, K, dtf)
    res = {'pack': pack, 'K': K, 'guest_persistent_splits': len(gl['persistent_splits']), 'guest_max_gen': gl['max_generation'],
           'host_persistent_splits': len(hl['persistent_splits']), 'host_max_gen': hl['max_generation']}
    hsp = [(t['start'], t['cy'][0], t['cx'][0]) for t in ht if t['birth'] == 'split']
    co = 0
    for e in gl['persistent_splits']:
        f = e['frame']; ch = [gt[c] for c in e['children']]
        cy = np.mean([c['cy'][0] for c in ch]); cx = np.mean([c['cx'][0] for c in ch])
        co += any(abs(fp - f) <= df and np.hypot(_wd(y, cy, H), _wd(x, cx, W)) <= r for fp, y, x in hsp)
    res['guest_splits_coincident_with_host_split'] = co
    tf = []
    for f in range(min(30, T - 1), T, 10):
        lab, n = ndimage.label(R[f, guest] > 0.5); hb = ndimage.binary_dilation(R[f, host] > 0.5, iterations=2)
        if n: tf.append(float(np.mean(ndimage.maximum(hb.astype(int), lab, index=np.arange(1, n + 1)))))
    res['guest_touching_host_frac_median'] = float(np.median(tf)) if tf else None
    tid = {(t['start'] + k, ci): t['id'] for t in ht for k, ci in enumerate(t['comp'])}

    def anc(i):
        s, st = {i}, [i]
        while st:
            for p in ht[st.pop()]['parents']:
                if p not in s: s.add(p); st.append(p)
        return s
    rows = []
    for t in gt:
        if t['end'] - t['start'] < L: continue
        seen, alone = [], 0
        for k, ci in enumerate(t['comp']):
            f = t['start'] + k; m = ndimage.binary_dilation(gc[f]['lab'] == ci + 1, iterations=2)
            ids = {tid[(f, l - 1)] for l in np.unique(hc[f]['lab'][m]) if l > 0 and (f, l - 1) in tid}
            alone += not ids
            seen += [i for i in ids if i not in seen]
        roots = []
        for i in seen:
            a = anc(i)
            if not any(q in a or i in anc(q) for q in roots): roots.append(i)
        rows.append({'id': t['id'], 'life': t['end'] - t['start'], 'hosts': len(seen), 'unrelated_hosts': len(roots), 'frames_alone': alone})
    res['guest_tracks_ge_L'] = len(rows); res['L'] = L
    res['guest_tracks_with_ge2_unrelated_hosts'] = sum(x['unrelated_hosts'] >= 2 for x in rows)
    res['guest_frac_frames_alone_median'] = float(np.median([x['frames_alone'] / x['life'] for x in rows])) if rows else None
    res['rows'] = rows
    return res


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('pack'); ap.add_argument('world'); ap.add_argument('out')
    ap.add_argument('--host', type=int, default=0); ap.add_argument('--guest', type=int, default=1)
    ap.add_argument('--K', type=int, default=20); ap.add_argument('--dtf', type=float, default=100.0); ap.add_argument('--L', type=int, default=20)
    a = ap.parse_args()
    res = run(a.pack, a.world, a.host, a.guest, a.K, a.dtf, a.L)
    json.dump(res, open(a.out, 'w'), indent=0, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
    print({k: v for k, v in res.items() if k != 'rows'})
