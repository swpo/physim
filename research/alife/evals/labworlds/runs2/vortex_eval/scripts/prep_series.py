"""Re-run the seed-31 preparation, saving om every 2 t from t=500 and full states every 10 t from t=540 (identical stream)."""
import json, pickle, sys, time
import numpy as np
sys.path.insert(0, "/home/user/evalwork/vortex_eval/scripts")
import common as C
from physim import labworld as LW
seed, ns = 31, 7331
w = C.world(actuators=False); st = LW.LabStepper(w, {}); m = st.module; C.one_worker(m)
s = m.init(seed, (128, 128)); rng = np.random.default_rng([ns, seed])
oms = {}
for k in range(1, 30001):
    s = st.add_noise(s, rng, w.native_dt); s = m.step(s)
    t = k * 0.02
    if k % 100 == 0 and t >= 500 - 1e-9:
        oms[f"om_{int(round(t))}"] = s["om"].astype(np.float32)
    if k % 500 == 0 and t >= 540 - 1e-9:
        with open(f"{C.OUT}/prep/state_s31_t{int(round(t))}.pkl", "wb") as fh:
            pickle.dump(s, fh)
np.savez_compressed(f"{C.OUT}/prep/series_s31.npz", **oms)
ref = pickle.load(open(f"{C.OUT}/prep/state_s31.pkl", "rb"))
print("identical to prep:", np.array_equal(ref["om"], s["om"]) and np.array_equal(ref["Y"], s["Y"]))
