"""python seeded.py SEED EPOCHS N OUTDIR : BFF soup of N tapes with 32 copies of the hand-built replicator
(planted()) placed in random noise; census of exact tapes (>= 3 copies) every 50 epochs, stats every 250."""
import sys, os, json, gzip, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from bff import Soup


def planted():
    """The hand-built BFF self-replicator (64 bytes): clear two food cells, build 64 there with a multiply loop,
    move head1 by 64, copy until the trailing zero, copy the zero, then end on an unmatched bracket."""
    code = b"<[-]<[-]>++++++++[<++++++++>-]<[}-]>>[.>}].["
    return np.frombuffer(code + b"a" * (63 - len(code)) + b"\x00", np.uint8).copy()

if __name__ == "__main__":
    seed, E, N, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    os.makedirs(out, exist_ok=True)
    S = Soup(seed, N=N); P = planted(); S.soup[:32] = P   # 32 planted copies (one copy is often overwritten before it spreads)
    st = open(f"{out}/seeded_stats_s{seed}.jsonl", "w"); cens = []; t0 = time.time()
    for e in range(1, E + 1):
        S.step()
        if e % 50 == 0:
            v = np.ascontiguousarray(S.soup).view(np.dtype((np.void, 64))).reshape(-1)
            u, c = np.unique(v, return_counts=True); keep = c >= 3
            cens.append({"t": e, "n": int(N), "census": {bytes(x).hex(): int(k) for x, k in zip(u[keep], c[keep])}})
        if e % 250 == 0:
            d = S.stats(); d["wall"] = round(time.time() - t0); cc = cens[-1]["census"]
            d["top_copies"] = max(cc.values()) if cc else 0; d["kinds_ge3"] = len(cc); d["in_kinds_ge3"] = sum(cc.values())
            d["exact_P"] = int((S.soup == P).all(1).sum()); st.write(json.dumps(d) + "\n"); st.flush()
        if e % 2000 == 0:
            json.dump(cens, gzip.open(f"{out}/seeded_census_s{seed}.json.gz", "wt"))
    json.dump(cens, gzip.open(f"{out}/seeded_census_s{seed}.json.gz", "wt"))
    np.savez_compressed(f"{out}/seeded_final_s{seed}.npz", soup=S.soup, tok=S.tok)
