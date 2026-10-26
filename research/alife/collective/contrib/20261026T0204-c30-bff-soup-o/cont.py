"""python cont.py SEED E0 E1 OUTDIR : continue a soup from OUTDIR/final_sSEED.npz (epoch E0) to E1 with a fresh RNG stream."""
import sys, os, json, gzip, time, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bff import Soup
seed, E0, E1, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
S = Soup(seed); d = np.load(f"{out}/final_s{seed}.npz"); S.soup[:] = d["soup"]; S.tok[:] = d["tok"]
S.next_tok = int(S.tok.max()) + 1; S.rng = np.random.default_rng(10_000 + seed * 100 + E0 // 1000); S.t = E0
st = open(f"{out}/stats_s{seed}.jsonl", "a"); cf = f"{out}/census_s{seed}.json.gz"
cens = json.load(gzip.open(cf, "rt")) if os.path.exists(cf) else []; t0 = time.time()
for e in range(E0 + 1, E1 + 1):
    S.step()
    if e % 128 == 0:
        v = np.ascontiguousarray(S.soup).view(np.dtype((np.void, 64))).reshape(-1)
        u, c = np.unique(v, return_counts=True); keep = c >= 5
        cens.append({"t": e, "n": int(S.N), "census": {bytes(x).hex(): int(k) for x, k in zip(u[keep], c[keep])}})
    if e % 256 == 0:
        dd = S.stats(); dd["wall"] = round(time.time() - t0); dd["top_copies"] = max(cens[-1]["census"].values()) if cens[-1]["census"] else 1
        dd["kinds_ge5"] = len(cens[-1]["census"]); st.write(json.dumps(dd) + "\n"); st.flush()
    if e % 2048 == 0:
        json.dump(cens, gzip.open(cf, "wt"))
        np.savez_compressed(f"{out}/final_s{seed}.npz", soup=S.soup, tok=S.tok)
json.dump(cens, gzip.open(cf, "wt"))
np.savez_compressed(f"{out}/final_s{seed}.npz", soup=S.soup, tok=S.tok)
