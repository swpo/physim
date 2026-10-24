"""closure screen: fraction of samples where the membrane encloses >= half its planted area,
catalysts inside, link counts. python sweep.py WORLD steps key=v1,v2 [key2=...] (grid over first key)"""
import sys, itertools, numpy as np
sys.path.insert(0, ".")
from labkit.world import load_world
W = load_world(sys.argv[1]); steps = int(sys.argv[2])
keys = [a.split("=")[0] for a in sys.argv[3:]]
vals = [a.split("=")[1].split(",") for a in sys.argv[3:]]
base = dict(W.P)
for combo in itertools.product(*vals):
    for seed in (0, 1):
        W.P.clear(); W.P.update(base)
        for k, v in zip(keys, combo):
            W.P[k] = v if isinstance(base[k], str) else type(base[k])(eval(v))
        s = W.init(seed, W.META["size"])
        st0 = W.stats(s); enc = []
        for t in range(1, steps + 1):
            s = W.step(s)
            if t % 25 == 0:
                enc.append(W.stats(s))
        closed = np.mean([e["encl"] >= 0.5 * st0["encl"] for e in enc])
        last = enc[-1]
        print(dict(zip(keys, combo)), "seed", seed, f"closed {closed:.2f}", "final", last, flush=True)
