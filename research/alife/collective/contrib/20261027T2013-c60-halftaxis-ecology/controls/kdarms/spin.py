"""Run the unchanged c52 world (128^2, defaults) to t=T and dump its state. usage: spin.py SEED T OUT.npz"""
import sys, os, time
sys.path.insert(0, '/home/user/physim/research/alife')
sys.path.insert(0, '/home/user/physim/research/alife/collective/contrib/20261027T2013-c60-halftaxis-ecology')
import numpy as np, world as w
KEYS = ["pa", "pb", "p", "F", "w", "q"]
seed, T, out = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
s = w.init(seed, (128, 128)); t0 = time.time()
n = int(round(T / s["par"]["dt"]))
for i in range(n): s = w.step(s)
np.savez(out, t=s["t"], **{k: s[k] for k in KEYS})
print(seed, s["t"], time.time() - t0)
