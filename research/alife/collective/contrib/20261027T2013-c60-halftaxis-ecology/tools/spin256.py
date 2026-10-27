"""Run this world (256^2) from seed to T and dump the state. usage: spin256.py SEED T OUT.npz"""
import sys, os, time
sys.path.insert(0, '/home/user/physim/research/alife'); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np, world as w
seed, T, out = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
s = w.init(seed, (256, 256)); n = int(round(T / s["par"]["dt"])); t0 = time.time()
for i in range(n): s = w.step(s)
np.savez(out, t=s["t"], **{k: s[k] for k in ["pa", "pb", "p", "F", "w", "q"]}); print(seed, s["t"], time.time() - t0)
