"""python run.py SEED EPOCHS OUTDIR : BFF soup with stats (every 256) and tape censuses (every 128)."""
import sys, os, json, gzip, time, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bff import Soup
seed, E, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
os.makedirs(out, exist_ok=True)
S = Soup(seed); st = open(f"{out}/stats_s{seed}.jsonl", "w"); cens = []; t0 = time.time()
for e in range(1, E + 1):
    S.step()
    if e % 128 == 0:
        v = np.ascontiguousarray(S.soup).view(np.dtype((np.void, 64))).reshape(-1)
        u, c = np.unique(v, return_counts=True); keep = c >= 5
        cens.append({"t": e, "n": int(S.N), "census": {bytes(x).hex(): int(k) for x, k in zip(u[keep], c[keep])}})
    if e % 256 == 0:
        d = S.stats(); d["wall"] = round(time.time() - t0); d["top_copies"] = max(cens[-1]["census"].values()) if cens[-1]["census"] else 1
        d["kinds_ge5"] = len(cens[-1]["census"]); st.write(json.dumps(d) + "\n"); st.flush()
    if e % 2048 == 0:
        json.dump(cens, gzip.open(f"{out}/census_s{seed}.json.gz", "wt"))
json.dump(cens, gzip.open(f"{out}/census_s{seed}.json.gz", "wt"))
np.savez_compressed(f"{out}/final_s{seed}.npz", soup=S.soup, tok=S.tok)
