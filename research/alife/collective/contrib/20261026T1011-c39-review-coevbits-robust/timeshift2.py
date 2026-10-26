"""Time-shift test (coevolution 'time-shift experiments'): mean capture probability exp(-h^2/w^2) of the predator
population alive at census i against the prey population alive at census j, averaged over pairs with the same lag
j - i. A chasing predator does best against past prey (lag < 0) and worst against future prey (lag > 0).
usage: timeshift.py tag seeds...   (env DT census spacing, default 4000; writes d2/<tag>_timeshift.json)"""
import sys, os, json, numpy as np
sys.argv_ = sys.argv; sys.argv = [sys.argv[0], "x", "x"]
import resync as RS
sys.argv = sys.argv_
DT = int(os.environ.get("DT", 4000)); RS.DT = DT
NB = int(os.environ.get("NB", 20)); _x = np.arange(1 << NB, dtype=np.int64); POP = np.zeros(1 << NB, np.int8)
for _b in range(NB): POP += ((_x >> _b) & 1).astype(np.int8)
del _x


def mats(tag, seed, w):
    P = RS.censuses(tag, seed, 1); Q = RS.censuses(tag, seed, 0)
    n = min(len(P), len(Q)); P, Q = P[:n], Q[:n]
    pk = [(np.array(list(r), np.int64), np.array(list(r.values()), float)) for r in P]
    qk = [(np.array(list(r), np.int64), np.array(list(r.values()), float)) for r in Q]
    M = np.full((n, n), np.nan)
    for i in range(n):
        gp, cp = pk[i]
        if cp.sum() == 0: continue
        for j in range(n):
            gq, cq = qk[j]
            if cq.sum() == 0: continue
            h = POP[(gp[:, None] ^ gq[None, :]) & ((1 << NB) - 1)].astype(float)
            M[i, j] = (cp[:, None] * cq[None, :] * np.exp(-h * h / (w * w))).sum() / (cp.sum() * cq.sum())
    return M


tag = sys.argv[1]; out = {}
for seed in map(int, sys.argv[2:]):
    M = mats(tag, seed, float(os.environ.get('W', 10))); n = len(M); lags = np.arange(-(n // 2), n // 2 + 1); prof = []
    for L in lags:
        v = [M[i, i + L] for i in range(5, n) if 5 <= i + L < n]   # skip the first 20k steps
        prof.append(float(np.nanmean(v)) if v else None)
    out[seed] = dict(lags=(lags * DT).tolist(), prof=prof)
    k0 = list(lags).index(0)
    print(tag, seed, "lag -40k/-8k/0/+8k/+40k:", [round(prof[k0 + d], 4) for d in (-10, -2, 0, 2, 10)], flush=True)
json.dump(out, open(f"data/{tag}_timeshift.json", "w"))
