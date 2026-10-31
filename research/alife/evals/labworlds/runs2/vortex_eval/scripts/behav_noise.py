"""Long behaviour run of the fed vortices under the declared dynamics noise (LabStepper.add_noise before every step).

python behav_noise.py --seed S --T 3000 --intensity 0.003 --out OUT.npz
Records signed vorticity every 3 t (as the claim's packs: 1000 frames at 150 steps) for curation/analyze.py.
"""
import argparse, json, sys, time
import numpy as np
sys.path.insert(0, "/home/user/evalwork/vortex_eval/scripts")
import common as C
from physim import labworld as LW

ap = argparse.ArgumentParser()
ap.add_argument("--seed", type=int, required=True)
ap.add_argument("--T", type=float, default=3000)
ap.add_argument("--intensity", type=float, default=C.INTENSITY)
ap.add_argument("--noise-seed", type=int, default=5150)
ap.add_argument("--out", required=True)
a = ap.parse_args()

w = C.world(intensity=a.intensity, actuators=False)
st = LW.LabStepper(w, {})
m = st.module
C.one_worker(m)
s = m.init(a.seed, (128, 128))
rng = np.random.default_rng([a.noise_seed, a.seed])
fdt, h = 3.0, w.native_dt
spf = int(round(fdt / h))
frames = int(round(a.T / fdt))
rec, snaps = [], {}
t0 = time.process_time()
status = "ok"
for f in range(frames + 1):
    if f:
        for _ in range(spf):
            s = st.add_noise(s, rng, h)
            s = m.step(s)
    om = s["om"]
    if not np.isfinite(om).all():
        status = f"non-finite at frame {f}"
        break
    rec.append(om.astype(np.float32))
    if f in (0, frames // 2, frames) or f % 200 == 0:
        snaps[f"om_{f}"] = om.astype(np.float32)
        snaps[f"Y_{f}"] = s["Y"].astype(np.float32)
cpu = time.process_time() - t0
meta = dict(world="fv", seed=a.seed, N=128, dt=h, T=a.T, rot=0.0, fdt=fdt, spf=spf, frames=frames, overrides={},
            status=status, cpu_s=cpu, noise=dict(intensity=a.intensity, ell=C.ELL, om="additive", Y="proportional",
                                                   noise_seed=a.noise_seed))
np.savez_compressed(a.out, rec=np.stack(rec), meta=json.dumps(meta), census="[]", **snaps)
print(json.dumps(meta), flush=True)
