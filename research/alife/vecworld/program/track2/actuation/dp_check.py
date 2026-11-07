"""dp_check -- the nats accounting seen from level 1, at one state (data processing + efficiency).

usage: python -B dp_check.py SIGMA_W [STATE]     -> results/dp_check.json

At saved state STATE (default 0) and its target (programs.pick_target), R = 32 noise keys; members:
twin (no input) and wind_aimed at C = 2 and 12.5 nats, paired keys, 4 ticks. Statistic: the target's
centroid relative to p0, along n (scalar) and in 2-d, from the tracker table (level 1).
  KL proxy (Gaussian, equal covariance): 0.5 dmu^T S0^-1 dmu, dmu from the paired differences,
  bias-corrected by subtracting the paired-difference variance / R (1-d), S0 from the twins.
  Data processing requires KL(level 1) <= C; the share KL/C is the program's information
  efficiency for that statistic. Also the chi^2 card bound (dmu^2 <= (e^{2C} - 1) Var_0) and the
  linear-Gaussian bound (dmu^2 <= 2 C Var_0).
"""
import json
import sys
import time

import jax.numpy as jnp
import numpy as np

import programs as PG
import wind as WD
from vw.world import make_key, member_keys

SIG = float(sys.argv[1])
S = int(sys.argv[2]) if len(sys.argv) > 2 else 0
R, TH, CS = 32, 4, (2.0, 12.5)
t0 = time.time()
st = np.load("/home/user/evalwork/vecworld/vw1/fresh/inputs/results/states.npz")
X, M = st["x"], WD.host_to_jax_memory(st["m"])
WW = WD.WindWorld()
run = WW.make_run()
Tb = np.asarray(WW.table(jnp.asarray(M[S]))[0])
tgt, tier = PG.pick_target(Tb)
p0, v0, n0, sp = PG.frame(Tb, tgt)
nc = 1 + len(CS)
UW = np.zeros((nc, TH, WD.NW))
for i, C in enumerate(CS):
    UW[i + 1] = PG.wind_aimed(Tb, tgt, C, SIG)
B = nc * R
ci, ri = np.repeat(np.arange(nc), R), np.tile(np.arange(R), nc)
keys = member_keys(make_key(7778, S), R)
y, tab, glob, A1, _ = run(WW.params, jnp.asarray(np.repeat(X[S][None], B, 0)), jnp.asarray(np.repeat(M[S][None], B, 0)),
                          keys[jnp.asarray(ri)], jnp.zeros((B,), jnp.int64), jnp.zeros((B, TH, WD.KMAX), int),
                          jnp.zeros((B, TH, WD.KMAX)), jnp.asarray(UW[ci]), jnp.full((B,), SIG))
tab = np.asarray(tab)
tuid = tab[0, 0, tgt, WD.NF + 4]
pos = np.full((B, TH + 1, 2), np.nan)
for b in range(B):
    for h in range(TH + 1):
        sl = np.flatnonzero((tab[b, h, :, 0] > 0.5) & (tab[b, h, :, WD.NF + 4] == tuid))
        if sl.size:
            pos[b, h] = WD.mi(tab[b, h, sl[0], WD.NF:WD.NF + 2] - p0, 128.0)
out = {"state": S, "target": tgt, "sigma_w": SIG, "R": R, "rows": {}}
for i, C in enumerate(CS):
    rows = {}
    for h in range(1, TH + 1):
        a, b0 = pos[ci == i + 1, h], pos[ci == 0, h]
        ok = ~np.isnan(a).any(1) & ~np.isnan(b0).any(1)
        d = a[ok] - b0[ok]
        n_ok = int(ok.sum())
        lat_d, lat0 = d @ n0, b0[ok] @ n0
        dm, v0_ = lat_d.mean(), lat0.var(ddof=1)
        kl1 = 0.5 * (dm ** 2 - lat_d.var(ddof=1) / n_ok) / v0_
        S0 = np.cov(b0[ok].T)
        dm2 = d.mean(0)
        kl2 = 0.5 * dm2 @ np.linalg.solve(S0, dm2)
        rows[f"h{h}"] = {"n_pairs": n_ok, "lateral_shift_px": float(dm), "lateral_sd_twin_px": float(np.sqrt(v0_)),
                         "kl_proxy_1d_nats": float(kl1), "kl_proxy_2d_nats_plugin": float(kl2),
                         "efficiency_1d": float(kl1 / C), "chi2_ratio_dmu2_over_var": float(dm ** 2 / v0_),
                         "chi2_bound_e2C_minus_1": float(np.expm1(2 * C)), "linear_bound_2C": 2 * C}
    out["rows"][str(C)] = rows
out["seconds"] = time.time() - t0
json.dump(out, open(f"{WD.RES}/dp_check.json", "w"), indent=1)
print(json.dumps(out, indent=1))
