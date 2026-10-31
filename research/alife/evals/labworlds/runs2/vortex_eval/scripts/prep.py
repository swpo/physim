"""Prepared state: the declared noisy world from init(seed) to t=T (noise seed fixed), saved with module state."""
import argparse, json, pickle, sys, time
import numpy as np
from scipy import ndimage
sys.path.insert(0, "/home/user/evalwork/vortex_eval/scripts")
import common as C
from physim import labworld as LW

ap = argparse.ArgumentParser()
ap.add_argument("--seed", type=int, default=31)
ap.add_argument("--T", type=float, default=600)
ap.add_argument("--noise-seed", type=int, default=7331)
ap.add_argument("--out", default=f"{C.OUT}/prep")
a = ap.parse_args()
w = C.world(actuators=False)
st = LW.LabStepper(w, {})
m = st.module
C.one_worker(m)
s = m.init(a.seed, (128, 128))
rng = np.random.default_rng([a.noise_seed, a.seed])
t0 = time.process_time()
for _ in range(int(round(a.T / w.native_dt))):
    s = st.add_noise(s, rng, w.native_dt)
    s = m.step(s)
om = s["om"]
lab, n = ndimage.label(np.abs(om) > 0.06)
info = dict(seed=a.seed, noise_seed=a.noise_seed, T=a.T, t=float(s["t"]), bodies=int(n), cpu_s=round(time.process_time() - t0, 1),
            noise=dict(intensity=C.INTENSITY, ell=C.ELL), om_range=[float(om.min()), float(om.max())],
            Y_range=[float(s["Y"].min()), float(s["Y"].max())])
import os
os.makedirs(a.out, exist_ok=True)
with open(f"{a.out}/state_s{a.seed}.pkl", "wb") as fh:
    pickle.dump(s, fh)
json.dump(info, open(f"{a.out}/state_s{a.seed}.json", "w"), indent=1)
print(json.dumps(info))
