"""Real seeded soup vs its in-world neutral twin, same census (tapes >= 3 copies, every 50 epochs), from E0.
python compare.py REAL_CENSUS TWIN_CENSUS OUT.json OUT.png
Early activity = summed census counts over the Lc = 20 censuses (1000 epochs) after a kind's first census;
a* = 99.9th percentile of twin early activity (kinds born after the first window); significant new kinds
per 1000-epoch birth window in both; replacement; distance of the commonest kind from the ancestor;
self-replication of the 5 commonest kinds per window (20 trials each on random food)."""
import sys, os, json, gzip, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from o_bff import early, sig_per_window, replicates

real = json.load(gzip.open(sys.argv[1], "rt")); tw = json.load(gzip.open(sys.argv[2], "rt"))
E0 = tw["E0"]; rr = [c for c in real if c["t"] >= E0]; tc = tw["census"]
J = min(len(rr), len(tc)); rr = rr[:J]; tc = tc[:J]
R = [c["census"] for c in rr]; T = [c["census"] for c in tc]; Lc = 20; win = 20; nb = (J + win - 1) // win
bR, aR = early(R, Lc); bT, aT = early(T, Lc)
pool = np.array([a for g, a in aT.items() if bT[g] >= win and bT[g] + Lc < J])
astar = float(np.percentile(pool, 99.9))
sR = sig_per_window(bR, aR, astar, win, nb, Lc, J); sT = sig_per_window(bT, aT, astar, win, nb, Lc, J)
newR = np.bincount([b // win for b in bR.values()], minlength=nb); newT = np.bincount([b // win for b in bT.values()], minlength=nb)
P0 = planted()
def tops(rows):
    out = []
    for b in range(nb):
        agg = {}
        for r in rows[b * win:(b + 1) * win]:
            for g, n in r.items(): agg[g] = agg.get(g, 0) + n
        out.append(sorted(agg, key=lambda g: -agg[g])[:20])
    return out
tR, tT = tops(R), tops(T)
ov = lambda tt: ([len(set(tt[0]) & set(x)) / 20 for x in tt], [1.0] + [len(set(tt[i - 1]) & set(tt[i])) / 20 for i in range(1, len(tt))])
ham = lambda tt: [int((np.frombuffer(bytes.fromhex(x[0]), np.uint8) != P0).sum()) if x else -1 for x in tt]
repR = [float(np.mean(replicates(x[:5]))) for x in tR]; repT = [float(np.mean(replicates(x[:5]))) for x in tT]
top1R = [max(r.values()) / 32768 if r else 0 for r in R[::win]]; top1T = [max(r.values()) / 32768 if r else 0 for r in T[::win]]
res = dict(E0=E0, censuses=J, astar=astar, rates=tw["rates"], real_sig=sR.tolist(), twin_sig=sT.tolist(),
           real_new_kinds=newR.tolist(), twin_new_kinds=newT.tolist(), real_overlap_first=ov(tR)[0], real_overlap_prev=ov(tR)[1],
           twin_overlap_first=ov(tT)[0], twin_overlap_prev=ov(tT)[1], real_hamming_top1=ham(tR), twin_hamming_top1=ham(tT),
           real_top5_replicate=repR, twin_top5_replicate=repT, real_top1_share=top1R, twin_top1_share=top1T)
json.dump(res, open(sys.argv[3], "w"), indent=1)
for k in ["astar", "real_sig", "twin_sig", "real_new_kinds", "twin_new_kinds", "real_overlap_prev", "twin_overlap_prev", "real_hamming_top1", "twin_hamming_top1", "real_top5_replicate", "real_top1_share", "twin_top1_share"]:
    v = res[k]; print(k, np.round(v, 2).tolist() if isinstance(v, list) else v)
x = E0 + (np.arange(nb) + 0.5) * win * 50
fig, ax = plt.subplots(1, 4, figsize=(19, 4.2))
ax[0].plot(x[:-1], sR[:-1], "o-", c="C3", label="real BFF soup"); ax[0].plot(x[:-1], sT[:-1], "o--", c="k", label="neutral twin (no code run)")
ax[0].set_title(f"new kinds reaching a*={astar:.0f} copy-censuses within 1000 epochs\n(a* = twin 99.9th percentile)"); ax[0].legend()
ax[1].plot(x, ov(tR)[1], "o-", c="C3"); ax[1].plot(x, ov(tT)[1], "o--", c="k"); ax[1].set_title("top-20 kinds overlap with previous window")
ax[2].plot(x, ham(tR), "o-", c="C3"); ax[2].plot(x, ham(tT), "o--", c="k"); ax[2].set_title("bytes by which the commonest kind differs\nfrom the planted replicator")
ax[3].plot(x, repR, "o-", c="C3", label="real"); ax[3].plot(x, repT, "o--", c="k", label="twin"); ax[3].set_ylim(-0.05, 1.05)
ax[3].set_title("self-replication of the 5 commonest kinds\n(fraction of exact copies on random food)"); ax[3].legend()
for a in ax: a.set_xlabel("epoch")
plt.tight_layout(); plt.savefig(sys.argv[4], dpi=72)
