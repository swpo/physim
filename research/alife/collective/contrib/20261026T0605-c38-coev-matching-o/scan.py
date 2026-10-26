import sys, json, numpy as np, coev
BASE = {"eat": 0.1, "cp": 0.03, "rF": 0.01, "Nq0": 30, "Np0": 1000, "cq": 0.02, "hT": 30, "step_q": 0.6, "Rs": 4, "Ediv_q": 4}
o = json.loads(sys.argv[1]); T = int(sys.argv[2]); prm = dict(BASE); prm.update(o); out = []
for seed in (0, 1, 2):
    st = coev.init(seed, prm); r = coev.run(st, T, rec_every=100, maxlog=1_500_000)
    rec = r["rec"]; z = np.where(rec[:, 2] == 0)[0]
    out.append(int(rec[z[0], 0]) if len(z) else -int(rec[-1, 2]))
print(sys.argv[1], "pred extinction t (neg = alive, final count):", out)
