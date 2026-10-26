# (c26 review) the claim's o_measure.stats on my fresh-seed event logs, against each run's RB shadow
import sys, json, glob, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife/collective/contrib/20261026T0009-c30-hash-chemistry-o-calibration')
import o_measure as om
out = {}
for p, T, win in [(f, 2000, 200) for f in sorted(glob.glob('short/*.npz') + glob.glob('rep/*.npz'))] + [(f, 6000, 1000) for f in sorted(glob.glob('long/*.npz'))]:
    L = {k: v for k, v in np.load(p).items()}
    if L["pop"][-1] == 0:
        out[p] = dict(extinct_at=int(np.argmax(L["pop"] == 0))); print(p, out[p]); continue
    sh = om.shadow(L, seed=1)
    a = om.stats(L, T, win=win, Lc=1000); b = om.stats(sh | {"mut_n": L["mut_n"]}, T, win=win, Lc=1000)
    out[p] = dict(unique=int(a["cum_unique"][-1]), unique_shadow=int(b["cum_unique"][-1]), cohort=a["cohort_new"].tolist(), cohort_shadow=b["cohort_new"].tolist(),
                  bedau_cum=int(a["bedau_new"].sum()), bedau_cum_shadow=int(b["bedau_new"].sum()), top_overlap_first=[round(x, 2) for x in a["top_overlap_first"]],
                  mean_size=round(float(np.mean(a["mean_size"])), 2))
    print(p, json.dumps(out[p]))
json.dump(out, open('review_stats.json', 'w'), indent=1)
