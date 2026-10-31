"""CIPS-iso prepared state: the variant from init(SEED) at zero noise to T_PREP (dt 0.1), then the 250 t window
at zero noise with e snapshots every 12.5 t (5 tu; float16, for pictures), and a check that e, p, F equal the
cips_rotation world_iso.py (both drifts isotropic) after 300 steps from the same init (the amphiphile is
one-way coupled)."""
import json, sys, time, importlib.util, os
sys.path.insert(0, "/home/user/evalwork/pm_cips_eval/scripts")
from common import PC, E, LW, EVALPILOT, OUT
import numpy as np
from pathlib import Path
SEED, T_PREP, N = int(sys.argv[1]), float(sys.argv[2]), 192
D = Path(OUT) / "cips_prep"; D.mkdir(parents=True, exist_ok=True)
w = PC.cips_world(0.0)
m = PC.native_module(w)
# equality check against world_iso.py
spec = importlib.util.spec_from_file_location("wiso", f"{EVALPILOT}/cips_rotation/world_iso.py")
wi = importlib.util.module_from_spec(spec); spec.loader.exec_module(wi); wi.ops.WORKERS = 1
a, b = m.init(SEED, (N, N)), wi.init(SEED, (N, N))
for _ in range(300):
    a, b = m.step(a), wi.step(b)
chk = {f: float(np.abs(a[f] - b[f]).max()) for f in PC.CIPS_FIELDS}
print("vs world_iso after 300 steps", chk, flush=True)
t0 = time.process_time()
s = m.init(SEED, (N, N))
nsteps = int(round(T_PREP / 0.1))
for i in range(nsteps):
    s = m.step(s)
cpu = time.process_time() - t0
np.savez_compressed(D / f"prep_s{SEED}_t{int(T_PREP)}.npz", t=s["t"], **{f: s[f] for f in PC.CIPS_FIELDS})
snaps = {}
for k in range(21):
    snaps[f"e_{k * 5}tu"] = s["e"].astype(np.float16)
    snaps[f"s_{k * 5}tu"] = s["s"].astype(np.float16)
    snaps[f"F_{k * 5}tu"] = s["F"].astype(np.float16)
    if k < 20:
        for _ in range(125):
            s = m.step(s)
np.savez_compressed(D / f"window_s{SEED}_t{int(T_PREP)}.npz", **snaps)
json.dump(dict(seed=SEED, t_prep=T_PREP, cpu_prep_s=cpu, cpu_total_s=time.process_time() - t0, vs_world_iso_300=chk),
          open(D / f"prep_s{SEED}_t{int(T_PREP)}.json", "w"), indent=1)
print("done", cpu, flush=True)
