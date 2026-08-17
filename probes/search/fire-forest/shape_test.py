
import sys, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
from hier_metrics import compact_top_fit

T = 2400; P = 300   # 8 cycles, dt=1
t = np.arange(T)
ph = (t % P) / P

def rep(name, x):
    r = compact_top_fit(x, dt=1.0)
    print("%-34s -> %-10s r2=%.3f  all=%s" % (name, r["model"], r["r2"], r["all"]))

rep("sawtooth (linear rise, reset)", ph.copy())
rep("exp-approach tau=P/4 + reset", 1 - np.exp(-ph / 0.25))
rep("exp-approach tau=P/8 + reset", 1 - np.exp(-ph / 0.125))
# logistic S ramp: crawl a, transit, top dwell
for frac_low, frac_hi in ((0.3, 0.3), (0.2, 0.5), (0.4, 0.4)):
    x = 1 / (1 + np.exp(-(ph - frac_low) / (max(1 - frac_low - frac_hi, .05) / 8)))
    rep("S-ramp low=%.1f hi=%.1f" % (frac_low, frac_hi), x)
rep("sine", np.sin(2 * np.pi * ph))
rep("sine + 20% noise", np.sin(2 * np.pi * ph) + 0.2 * np.random.default_rng(0).normal(size=T))
# square with jittered period (like spark-timed fires)
rng = np.random.default_rng(1)
x = []; lev = 1.0
while len(x) < T:
    d = int(rng.normal(P/2, P/8))
    x += [lev] * max(d, 10); lev = 1.0 - lev
rep("square, 25% jittered dwells", np.array(x[:T], float))
x = []; lev = 1.0
while len(x) < T:
    d = int(rng.normal(P/2, P/4))
    x += [lev] * max(d, 10); lev = 1.0 - lev
rep("square, 50% jittered dwells", np.array(x[:T], float))
# sawtooth with jittered period
x = []; 
while len(x) < T:
    d = int(rng.normal(P, P/4)); d = max(d, 20)
    x += list(np.linspace(0, 1, d))
rep("sawtooth, 25% jittered period", np.array(x[:T], float))
