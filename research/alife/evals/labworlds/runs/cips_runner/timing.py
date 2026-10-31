import os, sys, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.path.insert(0, "/home/user/physim/research/alife")
import importlib.util
import numpy as np
from labkit import ops
ops.WORKERS = 1
W = "/home/user/physim/research/alife/collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py"
spec = importlib.util.spec_from_file_location("w", W); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for n in (128, 192):
    s = m.init(0, (n, n))
    for _ in range(20): s = m.step(s)
    t0 = time.process_time()
    for _ in range(500): s = m.step(s)
    dt = (time.process_time() - t0) / 500
    rng = np.random.default_rng(0)
    t0 = time.process_time()
    for _ in range(200): rng.standard_normal((n, n))
    nz = (time.process_time() - t0) / 200
    print(n, f"step {dt*1e3:.2f} ms, one normal draw {nz*1e3:.3f} ms")
