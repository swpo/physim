
import sys, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter")
from morpho_sim import simulate
from runner import calibrate_plateaus

# failing jitter case F48 jit=4: Dv=10.87 kap=0.488 eps=2.53e-3
Dv, L, kap, eps = 10.87, 48, 0.488, 2.53e-3
cal = calibrate_plateaus(Dv, L, (4, 5))
S_lo, S_hi = cal[0]["S"], cal[1]["S"]
kstar2 = (1-kap)*S_lo + kap*S_hi
p = dict(ny=8, nx=L, dx=1.0, dt=0.1, a=0.1, b=0.9, Du=1.0, Dv=Dv, Dc=10.0,
         sigma=1.0, mode="auto", eps=eps, kstar2=kstar2, steps=60000,
         meas_every=25, seed=1, k_ref=0.62, C0=1.0, t_on=250.0,
         noise_amp=2e-3, Cmin=0.5, Cmax=1.9)
r = simulate(p)
m = r["t"] >= 1000
t, env, amp, n = r["t"][m], r["envmin"][m], r["amp"][m], r["nz"][m]
med = np.median(env)
print("median envmin=%.3f  p75=%.3f  min=%.3f" % (med, np.percentile(env, 75), env.min()))
thr = 0.5*med
low = env < thr
d = np.diff(low.astype(int))
starts = np.where(d==1)[0]+1; ends = np.where(d==-1)[0]+1
print("raw event count:", low.sum(), "segments:", len(starts))
for s_, e_ in zip(starts[:25], ends[:25]):
    print("  dip t=[%.0f,%.0f] dur=%.1f minenv=%.3f" % (t[s_], t[min(e_,len(t)-1)], t[min(e_,len(t)-1)]-t[s_], env[s_:e_].min() if e_>s_ else -1))
flips = np.where(np.diff(n)!=0)[0]
print("flips at:", [int(t[i]) for i in flips])
