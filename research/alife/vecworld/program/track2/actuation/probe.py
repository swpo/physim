"""probe -- open-loop aimed and regional programs from the 40 saved states, wind and kick, vs twins.

usage: python -B probe.py SIGMA_W [S0 S1]     -> results/probe/state_XXX.npz (float32 records)

States: vw1/fresh/inputs/results/states.npz (40 level-0 states of the port world, 60 ticks after
burn-in, with VW-0 tracker memories -> vw.objects memories by appending the zero overflow block).
Target per state: programs.pick_target on the t = 0 tracker table (chosen before any run).
Conditions (one member per condition and noise key; R = 3 keys per state, member_keys(make_key(7777, s), 3);
every condition of replicate r shares key r, so each program has a no-input twin with identical noise):
  wind world, background sigma_w = SIGMA_W:
    twin_w; WA2, WA12.5, WA50 (programs.wind_aimed, C nats); WR2, WR12.5, WR50 (wind_regional)
  port world (sigma_w = 0): twin_0; KA4, KA16, KA64 (programs.kick_aimed, sum |a| over the program)
  scaling check (states < NCHK only), background sigma_w / 4: twin_q; WA50q = the WA50 command itself
    (same physical push; it costs 16 x 50 = 800 nats at that background)
Every program lasts 4 ticks (budget split equally); records y = <Phi_coarse, Phi_objects> (336), the
tracker table and globals at t = 0..16, and the matter each kick moved.
"""
import os
import sys
import time

import jax.numpy as jnp
import numpy as np

import programs as PG
import wind as WD
from vw.world import make_key, member_keys

SIG = float(sys.argv[1])
S0 = int(sys.argv[2]) if len(sys.argv) > 2 else 0
S1 = int(sys.argv[3]) if len(sys.argv) > 3 else 40
R, TH, NCHK = 3, 16, 10
OUT = f"{WD.RES}/probe"
os.makedirs(OUT, exist_ok=True)
WIND_C = (2.0, 12.5, 50.0)
KICK_L1 = (4.0, 16.0, 64.0)


def conditions(chk):
    c = [("twin_w", SIG)] + [(f"WA{C:g}", SIG) for C in WIND_C] + [(f"WR{C:g}", SIG) for C in WIND_C]
    c += [("twin_0", 0.0)] + [(f"KA{L:g}", 0.0) for L in KICK_L1]
    if chk:
        c += [("twin_q", SIG / 4), ("WA50q", SIG / 4)]
    return c


def main():
    st = np.load("/home/user/evalwork/vecworld/vw1/fresh/inputs/results/states.npz")
    X, M = st["x"], WD.host_to_jax_memory(st["m"])
    WW = WD.WindWorld()
    run = WW.make_run(record_moved=True)
    t_all = time.time()
    for s in range(S0, S1):
        fn = f"{OUT}/state_{s:03d}.npz"
        if os.path.exists(fn):
            continue
        t0 = time.time()
        Tb, _ = WW.table(jnp.asarray(M[s]))
        Tb = np.asarray(Tb)
        smap = M[s][:WD.HW]
        tgt, tier = PG.pick_target(Tb)
        p0, v0, n0, sp = PG.frame(Tb, tgt)
        conds = conditions(s < NCHK)
        nc = len(conds)
        B = nc * R
        UW = np.zeros((nc, TH, WD.NW))
        KI = np.zeros((nc, TH, WD.KMAX), int)
        KV = np.zeros((nc, TH, WD.KMAX))
        budget, cmd_l1, sides = np.zeros(nc), np.zeros(nc), np.zeros((nc, 2), int)
        for i, (nm, sw) in enumerate(conds):
            if nm.startswith("WA") or nm.startswith("WR"):
                C = 50.0 if nm == "WA50q" else float(nm[2:])
                f = PG.wind_aimed if nm.startswith("WA") else PG.wind_regional
                U = f(Tb, tgt, C, SIG)                       # the command is built at the main background
                UW[i, :PG.T_IN] = U
                budget[i] = WD.nats(U, sw)                     # charged at the member's own background
            elif nm.startswith("KA"):
                idx, val, l1, sd_ = PG.kick_aimed(Tb, tgt, smap, X[s], float(nm[2:]))
                KI[i, :PG.T_IN], KV[i, :PG.T_IN] = idx, val
                budget[i] = cmd_l1[i] = l1
                sides[i] = sd_
        keys = member_keys(make_key(7777, s), R)
        ci = np.repeat(np.arange(nc), R)                      # member b: condition ci[b], replicate ri[b]
        ri = np.tile(np.arange(R), nc)
        sig = np.array([conds[c][1] for c in ci])
        y, tab, glob, moved, A1, _ = run(WW.params, jnp.asarray(np.repeat(X[s][None], B, 0)),
                                         jnp.asarray(np.repeat(M[s][None], B, 0)), keys[jnp.asarray(ri)],
                                         jnp.zeros((B,), jnp.int64), jnp.asarray(KI[ci]), jnp.asarray(KV[ci]),
                                         jnp.asarray(UW[ci]), jnp.asarray(sig))
        A1 = np.asarray(A1)
        np.savez_compressed(fn, y=np.asarray(y, np.float32), tab=np.asarray(tab, np.float32),
                            glob=np.asarray(glob, np.float32), moved=np.asarray(moved, np.float32),
                            cond=np.array([c[0] for c in conds]), cond_sigma=np.array([c[1] for c in conds]),
                            ci=ci, ri=ri, budget=budget, cmd_l1=cmd_l1, sides=sides, uw=UW[:, :PG.T_IN].astype(np.float32),
                            target=tgt, tier=tier, p0=p0, v0=v0, n0=n0, speed=sp, sigma_main=SIG,
                            mass_drift=np.abs(A1.sum((2, 3)) - X[s].sum((1, 2))[None]).max(),
                            seconds=time.time() - t0)
        print(f"state {s} target {tgt} tier {tier} speed {sp:.2f} members {B} {time.time() - t0:.0f}s "
              f"(total {time.time() - t_all:.0f}s)", flush=True)


if __name__ == "__main__":
    main()
