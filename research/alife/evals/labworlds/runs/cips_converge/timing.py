"""Per-step cost breakdown at a resolution: world step alone, LabStepper with white and with correlated noise.
usage: timing.py DT N [STEPS]"""
import sys, time
dt, N = float(sys.argv[1]), int(sys.argv[2]); n = int(sys.argv[3]) if len(sys.argv) > 3 else 300
sys.argv = sys.argv[:1]
import numpy as np
import cconv as K
LW, C = K.LW, K.C
st, info = K.prepared(N)
res = {}
w = K.world(dt, N)
m = w.load(); C.one_worker(m)
s = m.init(0, (N, N))
for f in K.FIELDS:
    s[f] = st[f].copy()
for _ in range(20):
    s = m.step(s)
t0 = time.process_time()
for _ in range(n):
    s = m.step(s)
res["world_step_ms"] = (time.process_time() - t0) / n * 1e3
for name, ww in (("stepper_noise0", K.world(dt, N, sd=0.0, ell=0.0)), ("stepper_white", K.world(dt, N, ell=0.0)), ("stepper_corr", w)):
    stp = LW.LabStepper(ww, dict(ww.aux(st), _grid=(N, N))); C.one_worker(stp.module)
    sim = LW.template(ww, st, 3)
    ticks = max(1, n // ww.steps_per_tick)
    stp(sim, 5)
    t0 = time.process_time()
    stp(sim, ticks)
    res[f"{name}_ms_per_native_step"] = (time.process_time() - t0) / (ticks * ww.steps_per_tick) * 1e3
res = {k: round(v, 2) for k, v in res.items()}
res["native_steps_per_50tu"] = int(round(50 / 0.02)) * w.steps_per_tick
res["member_50tu_s_estimate_corr"] = round(res["stepper_corr_ms_per_native_step"] * res["native_steps_per_50tu"] / 1e3, 1)
print(dict(dt=dt, N=N, **res))
