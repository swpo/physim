"""c63: re-simulate the claim world (claim_world.py, defaults) and save prey and predator matter sums every 5 t (25 steps,
as labkit's frames) for predstrip.py. usage: record.py SEED N T OUT.npz"""
import sys, os, importlib.util, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife')
here = os.path.dirname(os.path.abspath(__file__))
sp = importlib.util.spec_from_file_location('w', os.path.join(here, '..', 'claim_world.py')); w = importlib.util.module_from_spec(sp); sp.loader.exec_module(w)
seed, N, T, out = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
s = w.init(seed, (N, N)); n = int(round(T / w.CFG['dt'])); A, B = [], []
for i in range(n + 1):
    if i % 25 == 0: A.append(s['A'].sum(0).astype(np.float16)); B.append(s['B'].sum(0).astype(np.float16))
    if i < n: s = w.step(s)
np.savez_compressed(out, A=np.array(A), B=np.array(B))
