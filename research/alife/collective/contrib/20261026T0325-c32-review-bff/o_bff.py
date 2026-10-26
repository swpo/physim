"""O measure on BFF seeded-soup censuses (exact 64-byte tapes with >= 3 copies, every 50 epochs).
python o_bff.py CENSUS.json.gz OUT.json [PNG]
Early activity of a kind = sum of its census counts over the Lc censuses after its first census.
a* = 99.9th percentile of the same in 8 census shadows (o_measure.census_shadow: same census sizes
and innovation counts, random parents). Also: replacement (top-20 overlap), Hamming distance of the
commonest kind from the planted ancestor, and whether the commonest kinds still self-replicate."""
import sys, os, json, gzip, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from o_measure import census_shadow
from seeded import planted
from bff import _exec


def early(rows, Lc):
    birth, act = {}, {}
    for j, r in enumerate(rows):
        for g, n in r.items():
            b = birth.setdefault(g, j)
            if j - b <= Lc: act[g] = act.get(g, 0) + n
    return birth, act


def sig_per_window(birth, act, astar, win, nb, Lc, J):
    s = np.zeros(nb, int)
    for g, a in act.items():
        if a >= astar and birth[g] + Lc < J and birth[g] >= 1: s[birth[g] // win] += 1
    return s


def replicates(hexs, trials=20, seed=0):
    rng = np.random.default_rng(seed); out = []
    for h in hexs:
        P = np.frombuffer(bytes.fromhex(h), np.uint8); ok = 0
        for _ in range(trials):
            t = np.r_[P, rng.integers(0, 256, 64).astype(np.uint8)]; k = np.zeros(128, np.uint32)
            _exec(t, k, 8192); ok += int((t[64:] == P).all())
        out.append(ok / trials)
    return out


if __name__ == "__main__":
    cens = json.load(gzip.open(sys.argv[1], "rt")); rows = [c["census"] for c in cens]; ts = [c["t"] for c in cens]
    J = len(rows); Lc = 20; win = 20; nb = (J + win - 1) // win
    br, ar = early(rows, Lc)
    G = int(os.environ.get('SHADOW_G', '50'))
    shs = [early(census_shadow(rows, q, g=G), Lc) for q in range(8)]
    pool = np.concatenate([[a for g, a in A.items() if B[g] >= 1 and B[g] + Lc < J] for B, A in shs])
    astar = float(np.percentile(pool, 99.9))
    real = sig_per_window(br, ar, astar, win, nb, Lc, J)
    env = np.array([sig_per_window(B, A, astar, win, nb, Lc, J) for B, A in shs])
    tops = []
    for b in range(nb):
        agg = {}
        for r in rows[b * win:(b + 1) * win]:
            for g, n in r.items(): agg[g] = agg.get(g, 0) + n
        tops.append(sorted(agg, key=lambda g: -agg[g])[:20])
    P0 = planted()
    ham = [int((np.frombuffer(bytes.fromhex(t[0]), np.uint8) != P0).sum()) if t else -1 for t in tops]
    rep = [replicates(t[:5]) for t in tops]
    res = dict(shadow_g=G, epochs_per_census=ts[1] - ts[0], Lc_censuses=Lc, win_censuses=win, astar=astar, sig=real.tolist(),
               shadow_sig_mean=env.mean(0).round(2).tolist(), shadow_sig_max=env.max(0).tolist(),
               top20_overlap_first=[len(set(tops[0]) & set(x)) / 20 for x in tops],
               top20_overlap_prev=[1.0] + [len(set(tops[i - 1]) & set(tops[i])) / 20 for i in range(1, nb)],
               hamming_top1_from_ancestor=ham, top5_replication_fraction=rep, kinds_total=len(br),
               in_repeated_kinds=[sum(r.values()) for r in rows[::win]])
    json.dump(res, open(sys.argv[2], "w"), indent=1)
    print("a*", astar); print("sig", res["sig"]); print("shadow mean", res["shadow_sig_mean"]); print("shadow max", res["shadow_sig_max"])
    print("ov first", np.round(res["top20_overlap_first"], 2).tolist()); print("ov prev", np.round(res["top20_overlap_prev"], 2).tolist())
    print("hamming", ham); print("rep top5", [np.round(np.mean(x), 2) for x in rep])
