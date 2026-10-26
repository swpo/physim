"""Neutral-twin-calibrated cohort measure for the complex world.
a* = the 99.9th percentile of early activity (replications within Lc steps of birth) of kinds born in
t in [1000, T-Lc) in the neutral twin of the same seed; count, per 1000-step birth window, kinds whose
early activity reaches a*. The neutral twin gives ~0.1% of its births by construction."""
import sys, os, json, glob, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))

def early(path, Lc=1000):
    d = np.load(path); t = d["rep_t"].astype(np.int64); k = d["rep_k"]
    u, fi, inv = np.unique(k, return_index=True, return_inverse=True); b = t[fi]
    ok = (t - b[inv]) <= Lc
    return b, np.bincount(inv[ok], minlength=len(u))

def measure(tag, seed, T=20000, Lc=1000, win=1000, q=99.9):
    bn, an = early(f"{HERE}/runs/neu_s{seed}.npz", Lc)
    sel = (bn >= 1000) & (bn < T - Lc); astar = float(np.percentile(an[sel], q))
    b, a = early(f"{HERE}/runs/{tag}_s{seed}.npz", Lc)
    nb = T // win; hit = (a >= astar) & (b < T - Lc)
    return dict(astar=astar, sig=np.bincount(b[hit] // win, minlength=nb)[:nb].tolist(),
                births=np.bincount(b // win, minlength=nb)[:nb].tolist(),
                neutral_sig=np.bincount(bn[(an >= astar) & (bn < T - Lc)] // win, minlength=nb)[:nb].tolist())

if __name__ == "__main__":
    out = {}
    for tag in sys.argv[1:]:
        for f in sorted(glob.glob(f"{HERE}/runs/{tag}_s*.npz")):
            s = int(f.rsplit("_s", 1)[1][:-4]); m = measure(tag, s); out[f"{tag}_s{s}"] = m
            print(tag, s, "a*", m["astar"], "sig", m["sig"], "| neutral", m["neutral_sig"][:6], "births/1000", m["births"][5])
    json.dump(out, open(f"{HERE}/calibrated.json", "w"))
