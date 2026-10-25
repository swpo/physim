#!/bin/bash
# fission screen: one cog in 96^2, each kernel parameter perturbed
cd "$(dirname "$0")"
for k in 0 1 2 3 4 5; do for fm in "m 0.9" "m 1.1" "s 0.85" "s 1.15"; do set -- $fm
  tag=k${k}_$1$2; WORLD_P="{\"N\":96,\"mod\":[[${k},\"$1\",$2]]}" EVERY=5 python runsave.py world_res.py scr_$tag 0 400 scr_cog.npz > /dev/null 2>&1
  python - "$tag" <<'PY'
import sys, numpy as np
from scipy import ndimage
t=sys.argv[1]; d=np.load(f'scr_{t}_snaps.npz'); X=d['X'].astype(np.float32)
n=[ndimage.label(ndimage.gaussian_filter(x[0],1)>0.3)[1] for x in X]
m=X[:,:2].sum((1,2,3))
print(t, 'cores', n[::10], 'final', n[-1], 'max', max(n), 'matter end/start %.2f' % (m[-1]/m[0]), flush=True)
PY
done; done
