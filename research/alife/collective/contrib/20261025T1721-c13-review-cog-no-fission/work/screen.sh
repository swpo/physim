#!/bin/bash
# c13: 5 noise-formed cogs (seed 7, 96^2, t=600) under single-kernel perturbations m x0.9 / x1.1, 400 t each
run() { tag=$1; mod=$2; WORLD_P="{\"N\":96${mod}}" EVERY=5 python ../runsave.py ../world.py scr_$tag 7 400 pre7_ckpt.npz > /dev/null 2>&1
python - "$tag" <<'PY'
import sys, numpy as np
from scipy import ndimage
t=sys.argv[1]; d=np.load(f'scr_{t}_snaps.npz'); X=d['X'].astype(np.float32)
n=[ndimage.label(ndimage.gaussian_filter(x[0],1)>0.3)[1] for x in X]
m=X[:,:2].sum((1,2,3))
print(t, 'cores every 50t', n[::10], 'final', n[-1], 'max', max(n), 'matter end/start %.2f' % (m[-1]/m[0]), flush=True)
PY
}
run base "" 
for k in 0 1 2 3 4 5; do for f in 0.9 1.1; do run k${k}_m$f ",\"mod\":[[$k,\"m\",$f]]" & done; wait; done
