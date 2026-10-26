"""Run one coev world and save its full birth/death log. usage: drive.py tag seed T '{json overrides}'"""
import os, sys, json, time, numpy as np, coevbits as coev
BASE = {"eat": 0.1, "cp": 0.03, "rF": 0.01, "Nq0": 30, "Np0": 1000, "cq": 0.02, "hT": 30, "step_q": 0.6, "Rs": 4, "Ediv_q": 4}
tag, seed, T = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
prm = dict(BASE); prm.update(json.loads(sys.argv[4]) if len(sys.argv) > 4 else {})
st = coev.init(seed, prm); t0 = time.time()
r = coev.run(st, T, rec_every=100, maxlog=int(os.environ.get("MAXLOG", 4_000_000)))
summ = dict(tag=tag, seed=seed, T=T, prm=st["p"], np=r["np"], nq=r["nq"], nlog=len(r["log"]), overflow=bool(r["overflow"]),
            attacks=float(r["attacks"]), mean_success=float(r["mean_success"]), secs=time.time() - t0,
            t_end=float(r["rec"][-1, 0]))
np.savez_compressed(f"data/{tag}_s{seed}.npz", log=r["log"].astype(np.float32), rec=r["rec"])
json.dump(summ, open(f"data/{tag}_s{seed}.json", "w"), indent=1)
print(json.dumps({k: v for k, v in summ.items() if k != "prm"}))
