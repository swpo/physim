"""python dipole.py seed T : run the fed-vortex world (WORLD_P from env) and print, every 50 t, the centroid, sign and
area (|omega| > 0.06) of each vortex body; writes dipole_seed<k>.json"""
import sys, os, json, importlib.util, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife')
from scipy import ndimage
spec = importlib.util.spec_from_file_location('w', 'world.py'); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
seed, T = int(sys.argv[1]), float(sys.argv[2]); s = W.init(seed, W.META['size']); dt = s['par']['dt']; rec = []
H, Wd = W.META['size']
for i in range(int(T / dt) + 1):
    if i % int(50 / dt) == 0:
        bodies = []
        for sg in (1, -1):
            m = sg * s['om'] > 0.06
            lab, n = ndimage.label(m)
            for j in range(1, n + 1):
                yy, xx = np.nonzero(lab == j)
                cy = (np.angle(np.exp(2j * np.pi * yy / H).mean()) / (2 * np.pi) * H) % H
                cx = (np.angle(np.exp(2j * np.pi * xx / Wd).mean()) / (2 * np.pi) * Wd) % Wd
                bodies.append({'sign': sg, 'cy': round(float(cy), 1), 'cx': round(float(cx), 1), 'area': int(len(yy))})
        rec.append({'t': round(s['t']), 'bodies': bodies})
        print(round(s['t']), [(b['sign'], b['cy'], b['cx'], b['area']) for b in bodies])
    s = W.step(s)
json.dump(rec, open(f'dipole_seed{seed}.json', 'w'))
