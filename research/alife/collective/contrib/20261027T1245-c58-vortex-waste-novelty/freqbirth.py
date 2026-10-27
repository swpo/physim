"""c58: are births frequency dependent? For each persistent split (trait.py split_rows: t, parent trait, daughter trait) find the
share of labelled vortices in the parent's class (round(theta/dm)) at the nearest traits_by_frame sample; compare with the
class share seen by a random vortex at the same samples (the expectation if splitting ignores class frequency).
Also reports per-capita births by class rarity: splits per vortex-sample for vortices whose class share is below / above 0.25.
python freqbirth.py run.json [...]"""
import sys, json, numpy as np
dm = 0.4
for f in sys.argv[1:]:
    r = json.load(open(f)); tb = r['traits_by_frame']; ts = np.array([t for t, _ in tb])
    shares = []
    for t, th in tb:
        cl = np.round(np.array(th) / dm).astype(int); u, n = np.unique(cl, return_counts=True); d = dict(zip(u, n / len(cl)))
        shares.append(d)
    rows = np.unique(np.array(r['split_rows'])[:, :2], axis=0)
    ps = []; rs = []
    for t, tp in rows:
        j = int(np.argmin(np.abs(ts - t))); d = shares[j]; c = int(round(tp / dm))
        ps.append(d.get(c, 0.0)); cl = np.round(np.array(tb[j][1]) / dm).astype(int); rs.append(np.mean([d[x] for x in cl]))
    # per-capita: vortex-samples by rarity
    rare = common = 0
    for d, (t, th) in zip(shares, tb):
        for x in th:
            s = d[int(round(x / dm))]; rare += s < 0.25; common += s >= 0.25
    br = int(sum(p < 0.25 for p in ps)); bc = int(sum(p >= 0.25 for p in ps)); rare = int(rare); common = int(common)
    print(json.dumps({'run': f, 'splits': len(rows), 'parent_class_share_mean': round(float(np.mean(ps)), 3), 'random_vortex_class_share_mean': round(float(np.mean(rs)), 3),
                      'births_per_1000_vortex_samples_rare(<0.25)': round(1000 * br / max(rare, 1), 2), 'births_per_1000_vortex_samples_common(>=0.25)': round(1000 * bc / max(common, 1), 2),
                      'rare_samples': rare, 'common_samples': common}))
