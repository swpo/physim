"""Determinism check: the same seed, run twice in one process, must give identical logs."""
import sys, os, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, world
def run(seed, T):
    S = world.init(seed, p=dict(maxev=500000))
    for _ in range(T): world.step(S)
    L = world.logs(S); return L["pop"][-1], hashlib.md5(L["rep_k"].tobytes()).hexdigest()[:10]
print([run(s, 300) for s in (0, 0, 3, 3)])
