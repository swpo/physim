"""viz_final.py — hero visuals for GE1: settle strip + kick relaxation plot."""
import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from hier_metrics import *
from guild_econ import *
from probe_cert import smooth
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

WD = "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy"
GE1 = dict(rho=2.1, yW=0.7, leak=0.65, margin=7.0, sig_mut=0.05, over=1.5,
           r0=0.006, hazard=4.5e-4, DW=0.02, L=96)
p = theory_to_raw(GE1)
rng = np.random.default_rng(0)
state = init_state(p, rng)
step = make_stepper(p, rng)
snap_at = {800, 6000, 20000, 45000}
snaps = {}
ts, fs = [], []
t0 = time.time()
T1 = 45000
for t in range(T1):
    step(state)
    if t % 25 == 0:
        ts.append(t); fs.append(macro(state)["fr_site"])
    if t + 1 in snap_at:
        snaps[t + 1] = [x.copy() for x in state]
print(f"settle {time.time()-t0:.0f}s")
# guild map colormap: producers orange, recyclers blue, empty dark
def guildmap(st):
    V, E, R, W, A = st
    g = np.where(V > 0.05, A, np.nan)
    return g
for tt, st in snaps.items():
    save_strip([st[2], st[3], st[0], guildmap(st)],
               WD + f"/strips/GE1_settle_t{tt}.png",
               titles=[f"R t={tt}", f"W t={tt}", f"V t={tt}", f"alloc a t={tt}"],
               cmap="viridis")
# kick
fork_seed = int(rng.integers(2**31))
st_c = [x.copy() for x in state]; st_k = [x.copy() for x in state]
step_c = make_stepper(p, np.random.default_rng(fork_seed))
step_k = make_stepper(p, np.random.default_rng(fork_seed))
Vk, Ek, Rk, Wk, Ak = st_k
rec = (Ak < 0.5) & (Vk > 0.05)
sel = rec & (np.random.default_rng(999).random(Vk.shape) < 0.8)
Ak[sel] = 1.0 - Ak[sel]
snaps2 = {}
kts, kfs, cfs = [], [], []
for t in range(15000):
    step_c(st_c); step_k(st_k)
    if t % 25 == 0:
        kts.append(t); kfs.append(macro(st_k)["fr_site"]); cfs.append(macro(st_c)["fr_site"])
    if t + 1 in (200, 3000, 12000):
        snaps2[t + 1] = [x.copy() for x in st_k]
for tt, st in snaps2.items():
    save_strip([st[2], st[3], st[0], guildmap(st)],
               WD + f"/strips/GE1_kick_t{tt}.png",
               titles=[f"R +{tt}", f"W +{tt}", f"V +{tt}", f"alloc a +{tt}"],
               cmap="viridis")
# main figure: settle + kick trace with exp fit
kfs = np.array(kfs); cfs = np.array(cfs); kts = np.array(kts)
sm = smooth(kfs, 11)
fit = compact_top_fit(sm, dt=25)
tau = fit["params"]["tau"]
fr_star = float(np.median(cfs[-len(cfs)//3:]))
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
ax1.plot(ts, fs, lw=1, color="k")
ax1.set_title("L3 settle: recycler site share fr(t), GE1 seed0")
ax1.set_xlabel("tick"); ax1.set_ylabel("fr_site")
tt2 = np.array(kts)
ax2.plot(tt2, cfs, lw=1, color="gray", label="control twin")
ax2.plot(tt2, kfs, lw=1, color="C0", label="kicked twin (80% recycler flip)")
c = sm[-max(3, len(sm)//10):].mean()
a = sm[0] - c
ax2.plot(tt2, a*np.exp(-tt2/tau) + c, "r--", lw=1.5,
         label=f"exp fit tau={tau:.0f}, r2={fit['r2']:.3f}")
ax2.axhline(fr_star, color="gray", ls=":", lw=0.8)
ax2.legend(fontsize=8); ax2.set_title("L3 top law: market relaxation after guild cull")
ax2.set_xlabel("tick after kick")
fig.tight_layout()
fig.savefig(WD + "/strips/GE1_toplaw.png", dpi=120)
print("saved GE1_toplaw.png; fit:", fit["model"], fit["r2"], "tau", tau)

# patch-size distribution (honest powerlaw check)
V, E, R, W, A = state
from scipy import ndimage
sizes_all = []
for mask in ((A < 0.5) & (V > 0.05), (A >= 0.5) & (V > 0.05)):
    lab, n = ndimage.label(mask)
    if n:
        sizes_all += list(np.atleast_1d(ndimage.sum(np.ones_like(lab), lab, range(1, n+1))))
pl = powerlaw_tail(sizes_all)
print("patch powerlaw:", pl)
json.dump({"powerlaw_patches": pl}, open(WD + "/powerlaw.json", "w"))
