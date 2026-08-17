import sys, time
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from hier_metrics import *
from guild_econ import *
import numpy as np

tc = dict(rho=2.0, yW=0.8, leak=0.5, margin=3.0, sig_mut=0.05, over=0.3)
p = theory_to_raw(tc)
rng = np.random.default_rng(0)
state = init_state(p, rng)
step = make_stepper(p, rng)
T1 = 20000
fr_ss = []
blocks = []
for t in range(T1):
    step(state)
    if t % 25 == 0:
        fr_ss.append(macro(state)["fr_b"])
    if t >= T1 - 8000 and t % 20 == 0:
        blocks.append(block_series(state, p["L"]))
bt = block_tau(blocks, 20)
m0 = macro(state)
print(f"settled: fr_b={m0['fr_b']:.3f} ncell={m0['ncell']} btau={bt}")
# steady-state ACF tau of fr_b
x = np.array(fr_ss[-240:]) # last 6000 ticks
x = x - x.mean()
acf = np.correlate(x, x, "full")[len(x)-1:]
acf /= acf[0]
below = np.where(acf < 1/np.e)[0]
print("steady-state fr_b ACF tau:", below[0]*25 if len(below) else ">6000", "ticks; sd:", np.array(fr_ss[-240:]).std())

# L1 impulse
t0=time.time()
tauR = impulse_tau(p, state, "R", 0)
tauW = impulse_tau(p, state, "W", 0)
print(f"L1 taus: R={tauR} W={tauW} ({time.time()-t0:.0f}s)")

# KICK: kill 70% of recycler cells
V, E, R, W, A = state
rec = (A < 0.5) & (V > 0.05)
kill = rec & (rng.random(V.shape) < 0.70)
print(f"killing {kill.sum()} of {rec.sum()} recycler cells")
V[kill] = 0; E[kill] = 0
T2 = 20000
rec_t, rec_fr = [], []
for t in range(T2):
    step(state)
    if t % 25 == 0:
        m = macro(state)
        rec_t.append(t); rec_fr.append(m["fr_b"])
rec_fr = np.array(rec_fr)
print("recovery fr_b: start=%.3f end=%.3f (pre-kick %.3f)" % (rec_fr[0], rec_fr[-1], m0["fr_b"]))
fit = compact_top_fit(rec_fr, dt=25)
print("compact_top_fit:", fit["model"], fit["r2"], fit["params"])
print("trajectory:", [round(float(v),3) for v in rec_fr[::40]])
