"""Long evoloop run with a genome census every `every` steps: per loop (hole side, full canonical core genome,
canonical cyclic sequence of its signal states 3-7). Writes counts per census."""
import sys, os, json, importlib.util, numpy as np, collections, time
from genome import genomes
params, seed, T, L, every, out = json.loads(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
os.environ["WORLD_P"] = json.dumps(params)
spec = importlib.util.spec_from_file_location("w", "world.py"); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(seed, (L, L)); rec = []; t0 = time.time()
def sigseq(gen):
    sg = [c for c in gen if c in '34567']; x = ''.join(sg)
    return min(x[k:] + x[:k] for k in range(len(x))) if x else ''
for t in range(1, T + 1):
    w.step(s)
    if t % every == 0:
        G = genomes(s["g"])
        full = collections.Counter(f"{x['side']}|{x['genome']}" for x in G)
        sig = collections.Counter(f"{x['side']}|{sigseq(x['genome'])}" for x in G)
        rec.append({"t": t, "n": len(G), "full": dict(full), "sig": dict(sig)})
        if t % 50000 == 0:
            print(t, len(G), len(full), len(sig), sig.most_common(2), round(time.time() - t0), flush=True)
            json.dump({"params": params, "seed": seed, "L": L, "every": every, "census": rec}, open(out, "w"))
json.dump({"params": params, "seed": seed, "L": L, "every": every, "census": rec}, open(out, "w"))
