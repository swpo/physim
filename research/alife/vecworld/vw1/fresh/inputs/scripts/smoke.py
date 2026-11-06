import time
import common as CM
import numpy as np
import jax
w, parts, AW = CM.build_world("both")
d = w.designer
print("n_in", w.n_in, "n_obs", w.n_obs, "card inputs", w.card()["inputs"])
t0 = time.time()
ens = d.ensemble(2, seed=(999,))
print("init+burn 2 members", time.time() - t0)
print(jax.tree_util.tree_structure(ens.carry.mem))
mem = CM.tracker_mem(ens)
print("mem shape", mem.shape)
lab, tab = CM.mem_parts(mem)
print("present", tab[:, :, 0].sum(1), "uids", tab[0, :, 16])
L1 = ens.level(1)
print("L1 shape", L1.shape, "objects part equals table feats:", np.abs(L1[:, 192:].reshape(2, 12, 12) - tab[:, :, :12]).max())
t0 = time.time()
ens2, r = d.rollout(ens, None, T=4, rec=("L1",))
print("rollout T=4 B=2 (incl compile)", time.time() - t0)
t0 = time.time()
ens3, r = d.rollout(ens2, None, T=4, rec=("L1",))
print("rollout T=4 B=2", time.time() - t0, r["L1"].shape)
A = CM.matter(ens.x)
print("matter stats: frac cells S<1e-3", (A < 1e-3).mean(), "S==0", (A == 0).mean(), "min", A.min(), "median", np.median(A))
print("in_map[:5]", w.in_map[:5])
