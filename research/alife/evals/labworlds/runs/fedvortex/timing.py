import sys, time, os, json, importlib.util, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife')
D = '/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex'
os.environ['WORLD_P'] = '{}'
spec = importlib.util.spec_from_file_location('w', D + '/fv_noise.py'); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
from labkit import ops; print('workers', ops.WORKERS)
s = W.init(0, (128, 128))
# bitwise check vs base for 200 steps
spec2 = importlib.util.spec_from_file_location('b', W.BASE); Bm = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(Bm)
s2 = Bm.init(0, (128, 128))
for i in range(200): s = W.step(s); s2 = Bm.step(s2)
print('bitwise equal after 200 steps:', np.array_equal(s['om'], s2['om']), np.array_equal(s['Y'], s2['Y']))
t0 = time.time(); n = 2000
for i in range(n): s = W.step(s)
print('ms/step', 1000 * (time.time() - t0) / n, 't', s['t'])
