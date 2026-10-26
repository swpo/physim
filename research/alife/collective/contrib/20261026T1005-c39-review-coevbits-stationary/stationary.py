"""(c38; c39 copy: local imports, seed from env SEED, data/ in the working directory) Two checks on the 700k-step coevbits run (b10L) and its neutral twin (b10LN), seed 0.
1. Time-shift profile (timeshift.py's matrix, censuses every 10000 steps) in the first and the second half of the run.
2. Revisits: consensus genotype of births per 2000-step window (bitsfig.windows); for each window the smallest Hamming
   distance to any consensus at least 50000 steps earlier.
Needs the npz logs in ../20261026T0735-c38-coevbits-predator-o/data/ (regenerate with its drivebits.py) and, from
../20261026T0821-c38-coevbits-timeshift and ../20261026T0735-c38-coevbits-predator-o, timeshift.py, resync.py, bitsfig.py."""
import sys, os, json, numpy as np
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here); SEED = int(os.environ.get("SEED", 0))
os.environ["DT"] = "10000"; sys.argv = ["timeshift.py", "x"]
exec(open(os.path.join(here, "timeshift.py")).read().split("tag = sys.argv[1]")[0])
import bitsfig as B
out = {}
for tag in ("b10L", "b10LN"):
    M = mats(tag, SEED, 10.0); n = len(M); res = {}
    for name, (a, b) in (("early", (2, n // 2)), ("late", (n // 2, n))):
        res[name] = {L * 10000: round(float(np.nanmean([M[i, i + L] for i in range(a, b) if 2 <= i + L < n])), 4) for L in (-10, -4, -1, 0, 1, 2, 4, 10)}
    out[tag] = res
    o, nb, T = B.windows(tag, SEED)
    for sp, nm in ((0, "prey"), (1, "pred")):
        C = np.round(o[sp]["cons"]); md = np.array([int(np.abs(C[:i - 25] - C[i]).sum(1).min()) for i in range(26, len(C))])
        out[f"{tag}_{nm}_revisit"] = dict(frac_le1=float(np.mean(md <= 1)), frac_le3=float(np.mean(md <= 3)), median=float(np.median(md)))
print(json.dumps(out, indent=1))
