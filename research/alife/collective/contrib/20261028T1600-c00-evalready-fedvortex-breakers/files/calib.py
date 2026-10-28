"""quick noise calibration: python calib.py <form> <sd...> ; form A = additive om+Y, B = additive om + proportional Y, C = additive om only"""
import sys, os, json, importlib.util, numpy as np
from scipy import ndimage
sys.path.insert(0, '/home/user/physim/research/alife')
D = '/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex'
form = sys.argv[1]
for sd in map(float, sys.argv[2:]):
    wp = {"dyn_noise": sd}
    if form == 'B': wp.update(noise_fields=["om"], mult_fields=["Y"])
    if form == 'C': wp.update(noise_fields=["om"])
    os.environ['WORLD_P'] = json.dumps(wp)
    spec = importlib.util.spec_from_file_location('w', D + '/fv_noise.py'); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
    s = W.init(0, (128, 128)); out = []
    for blk in range(8):
        for i in range(2500): s = W.step(s)
        a = np.abs(s['om']); lab, n = ndimage.label(a > 0.06)
        sizes = np.bincount(lab.ravel())[1:]; nb = int((sizes >= 6).sum())
        out.append(f"t{s['t']:.0f}: n{nb} max|w|{a.max():.3f} Y{s['Y'].mean():.3f} sd(w){s['om'].std():.3f}")
        if not np.isfinite(a).all(): out.append('NONFINITE'); break
    print(form, sd, ' | '.join(out), flush=True)
