"""(c45) base vs each setting: pooled over seeds 70+71, Mann-Whitney U on D of dividing tracks and bootstrap 95% CI of the
difference in medians (4000 resamples within each seed). usage: compare.py"""
import json, numpy as np
from scipy import stats
rng = np.random.default_rng(1)
def D(n, s): return np.array([r["disp_rl"] for r in json.load(open(f"{n}{s}.json"))["rows"] if r["dividing"]])
for n in ["mar60", "mar80", "phib065"]:
    b = [D("base", s) for s in (70, 71)]; x = [D(n, s) for s in (70, 71)]
    u = stats.mannwhitneyu(np.concatenate(x), np.concatenate(b), alternative="greater")
    bs = []
    for _ in range(4000):
        bs.append(np.median(np.concatenate([rng.choice(a, len(a)) for a in x])) - np.median(np.concatenate([rng.choice(a, len(a)) for a in b])))
    lo, hi = np.percentile(bs, [2.5, 97.5])
    print(f"{n}: n {sum(map(len,x))} vs base {sum(map(len,b))}; median D {np.median(np.concatenate(x)):.2f} vs {np.median(np.concatenate(b)):.2f}; "
          f"diff 95% CI [{lo:+.2f}, {hi:+.2f}]; Mann-Whitney one-sided p = {u.pvalue:.4f}")
