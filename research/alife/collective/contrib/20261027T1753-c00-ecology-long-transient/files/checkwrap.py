"""check that the WORKERS=1 wrapper reproduces the original world (WORKERS=2) bit for bit over 12000 steps at 64^2 (t=2400, past predator injection)"""
import sys, importlib.util, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife')
from labkit import ops
def load(p, name):
    spec = importlib.util.spec_from_file_location(name, p); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
orig = load('/home/user/physim/research/alife/collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py', 'o')
res = {}
for wk in (2, 1):
    ops.WORKERS = wk
    s = orig.init(90, (64, 64))
    for _ in range(12000): s = orig.step(s)
    res[wk] = orig.fields(s)
print('max abs diff WORKERS 2 vs 1:', float(np.abs(res[2] - res[1]).max()), 'max c_b', float(res[1][1].max()))
