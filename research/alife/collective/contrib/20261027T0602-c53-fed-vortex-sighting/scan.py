import sys, os, json, importlib.util, numpy as np
os.environ['WORLD_P'] = sys.argv[1]
sys.path.insert(0, '/home/user/physim/research/alife')
from scipy import ndimage
spec = importlib.util.spec_from_file_location('w', 'world.py'); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
s = W.init(int(sys.argv[2]), W.META['size']); dt = s['par']['dt']; T = float(sys.argv[3]); out = []
for i in range(int(T / dt) + 1):
    if i % int(100 / dt) == 0 and i > 0:
        a = np.abs(s['om']); m = a > 0.05; lab, n = ndimage.label(m)
        sizes = ndimage.sum(m, lab, range(1, n + 1)) if n else []
        npos = ndimage.label(s["om"] > 0.05)[1]; nneg = ndimage.label(s["om"] < -0.05)[1]
        out.append(f"t{s['t']:.0f}:+{npos}-{nneg},occ{m.mean():.2f},n{n},maxA{int(max(sizes)) if n else 0},w{a.max():.2f}")
    s = W.step(s)
    if not np.isfinite(s['om']).all(): out.append('BLOWUP'); break
print(sys.argv[1], ' '.join(out))
