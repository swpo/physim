"""(c45) Pooled selection regression over seeds: relative descendants (within-run relative fitness) on traits standardized
within run, with a run fixed effect. usage: pooled_sel.py label1 label2 ..."""
import sys, json, numpy as np
Z, W = [], []
for lab in sys.argv[1:]:
    d = json.load(open(f"/tmp/claude-0/se/sel_{lab}.json")); X = np.array(d["X"], float); Y = np.array(d["Y"], float)
    if len(Y) < 3: continue
    Z.append((X - X.mean(0)) / X.std(0)); W.append(Y / max(Y.mean(), 1e-9))
Z = np.vstack(Z); W = np.concatenate(W); A = np.c_[np.ones(len(Z)), Z]
b = np.linalg.lstsq(A, W, rcond=None)[0]
rng = np.random.default_rng(0); bs = [np.linalg.lstsq(A[i], W[i], rcond=None)[0] for i in (rng.integers(0, len(W), len(W)) for _ in range(4000))]
lo, hi = np.percentile(bs, [2.5, 97.5], axis=0)
print(" + ".join(sys.argv[1:]), f"n={len(W)}: " + "; ".join(f"{nm} {b[k+1]:+.3f} [{lo[k+1]:+.3f}, {hi[k+1]:+.3f}]" for k, nm in enumerate(["D", "speed", "straightness"])))
