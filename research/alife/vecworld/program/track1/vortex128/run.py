"""vortex128 -- the fed-vortex world's level-2 selection signal at 128^2, a per-area mutation test at 64^2,
and oracle branches for a rough level-2 closure. Same worlds as ../vortex_world/pilot.py (vortex_world.build,
'kinds' spec, MapWorld, world_seed 0); only the seeds, the mutation interval (area64) and the bookkeeping differ.

    python run.py main   ARM S T SEED            128^2, designer ensemble(S, seed=SEED), T ticks
                                                  -> results/main128_ARM.npz (rewritten every chunk; resumable)
                                                     + level-0 snapshots at SNAP ticks (scratch, float64)
    python run.py branch ARM R HB                 from every saved snapshot of ARM: R fresh-noise replicates of
                                                  every member for HB ticks (keys shared by both arms)
                                                  -> results/branch128_ARM.npz (rewritten after every point)
    python run.py area64 ARM S T SEED MUT_DT     64^2 with mutation interval MUT_DT (200 = the 128^2 rate per
                                                  unit area) -> results/area64_ARM.npz
    python run.py area64x ARM S T SEED MUT_DT M0 TAG   as area64 for members M0..M0+S-1 of ensemble(M0+S, SEED)
                                                  -> results/TAG_ARM.npz (extra seeds, both mutation rates)

ARM: sel (eps = 0.2) or neu (eps = 0); both sigma_a = 0.005. Members of ensemble(S, seed) are fold_in(base(seed), j),
so ensemble(4, seed=0) at 64^2 reproduces the initial conditions and noise keys of ../vortex_world's pilot_H64.
"""
import json
import os
import sys
import time

sys.dont_write_bytecode = True
sys.path.insert(0, "/home/user/evalwork/vecworld/program/track1/vortex_world")
import _paths  # noqa: E402,F401
import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

import vw  # noqa: E402
from vw.world import Ensemble, make_key, member_keys  # noqa: E402
import vortex_jax as VJ  # noqa: E402
import vortex_world as VW  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
SCR = os.environ.get("V128_SCRATCH", "/tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/v128")
os.makedirs(RES, exist_ok=True)
os.makedirs(SCR, exist_ok=True)
CHUNK = 20
SNAP = (100, 200, 300, 400)          # branch points (ticks): t = 500, 1000, 1500, 2000


def make(arm, H, mut_dt=50.0):
    cfg = VJ.Config(H=H, W=H, G=H // 16, mut_dt=mut_dt)
    specs, parts = VW.build(cfg)
    theta = dict(VJ.THETA, eps=0.0 if arm == "neu" else 0.2)
    w = VW.MapWorld(specs["kinds"], world_seed=0, params={k: jnp.asarray(v, jnp.float64) for k, v in theta.items()})
    return w, parts


def save_carry(path, ens):
    leaves = jax.tree_util.tree_leaves(ens.carry)
    arrs = {}
    for i, l in enumerate(leaves):
        if jax.dtypes.issubdtype(l.dtype, jax.dtypes.prng_key):
            arrs[f"k{i}"] = np.asarray(jax.random.key_data(l))
        else:
            arrs[f"a{i}"] = np.asarray(l)
    tmp = path + ".tmp.npz"
    np.savez(tmp, t=ens.t, **arrs)
    os.replace(tmp, path)


def load_carry(path, template):
    leaves, tdef = jax.tree_util.tree_flatten(template.carry)
    D = np.load(path)
    new = [jax.random.wrap_key_data(jnp.asarray(D[f"k{i}"])) if f"k{i}" in D.files else jnp.asarray(D[f"a{i}"])
           for i in range(len(leaves))]
    return Ensemble(template.world, tdef.unflatten(new), int(D["t"]))


def overflow(ens):
    m = ens.carry.mem
    try:
        return np.asarray(m[0][1][:, -4:]).tolist()
    except Exception:
        return None


def run_main(arm, S, T, seed, H=128, mut_dt=50.0, tag=None, m0=0):
    tag = tag or f"main{H}_{arm}"
    out_npz, out_js = os.path.join(RES, f"{tag}.npz"), os.path.join(RES, f"{tag}.json")
    last = os.path.join(SCR, f"{tag}_last.npz")
    w, parts = make(arm, H, mut_dt)
    d = w.designer
    ens = d.ensemble(S, seed=seed) if m0 == 0 else d.ensemble(m0 + S, seed=seed).clone(idx=np.arange(m0, m0 + S))
    L1, L2, cpu_prev = None, None, 0.0
    if os.path.exists(last) and os.path.exists(out_npz):              # resume
        ens = load_carry(last, ens)
        D = np.load(out_npz)
        L1, L2 = D["L1"][:, :ens.t + 1], D["L2"][:, :ens.t + 1]
        cpu_prev = json.load(open(out_js))["cpu_s"]
        print(arm, "resumed at tick", ens.t, flush=True)
    t0 = time.process_time()
    while ens.t < T:
        n = min(CHUNK, T - ens.t)
        ens, r = d.rollout(ens, T=n, rec=("L1", "L2"))
        a1, a2 = r["L1"].astype(np.float32), r["L2"].astype(np.float32)
        L1 = a1 if L1 is None else np.concatenate([L1, a1[:, 1:]], 1)
        L2 = a2 if L2 is None else np.concatenate([L2, a2[:, 1:]], 1)
        if tag.startswith("main") and ens.t in SNAP:
            save_carry(os.path.join(SCR, f"{tag}_snap{ens.t}.npz"), ens)
        save_carry(last, ens)
        cpu = cpu_prev + time.process_time() - t0
        np.savez_compressed(out_npz + ".tmp.npz", L1=L1, L2=L2)
        os.replace(out_npz + ".tmp.npz", out_npz)
        meta = dict(arm=arm, H=H, S=S, first_member=m0, T_target=T, t_done=ens.t, seed=seed, mut_dt=mut_dt, sigma_a=VJ.Config.sigma_a,
                    eps=0.0 if arm == "neu" else 0.2, tick_time=VJ.Config().tick_time, K=parts["tracker"].K,
                    tracker=dict(VW.TRACK, **VW.slots_for(VJ.Config(H=H, W=H))), cpu_s=cpu,
                    member_ticks=S * ens.t, cpu_s_per_member_tick=cpu / (S * ens.t), overflow=overflow(ens),
                    snapshots=[s for s in SNAP if s <= ens.t] if tag.startswith("main") else [])
        json.dump(meta, open(out_js, "w"), indent=1)
        print(arm, H, ens.t, "N", L2[:, -1, 0].astype(int).tolist(), "s_b", np.round(L2[:, -1, 1], 2).tolist(),
              "cpu/mt", round(meta["cpu_s_per_member_tick"], 4), flush=True)


def run_branch(arm, R, HB, H=128):
    tag = f"main{H}_{arm}"
    out_npz, out_js = os.path.join(RES, f"branch{H}_{arm}.npz"), os.path.join(RES, f"branch{H}_{arm}.json")
    w, parts = make(arm, H)
    d = w.designer
    S = json.load(open(os.path.join(RES, f"{tag}.json")))["S"]
    template = d.ensemble(S, seed=0)
    done = dict(np.load(out_npz)) if os.path.exists(out_npz) else {}
    meta = json.load(open(out_js)) if os.path.exists(out_js) else {"cpu_s": 0.0, "points": []}
    for tb in SNAP:
        p = os.path.join(SCR, f"{tag}_snap{tb}.npz")
        if f"p{tb}" in done or not os.path.exists(p):
            continue
        t0 = time.process_time()
        ens = load_carry(p, template)
        assert ens.t == tb
        keys = member_keys(make_key(77, H, tb), S * R)                   # same replicate keys for both arms
        rep = ens.clone(rep=R, keys=keys)
        _, rb = d.rollout(rep, T=HB, rec=("L2",))
        done[f"p{tb}"] = rb["L2"].reshape(S, R, HB + 1, -1).astype(np.float32)
        np.savez_compressed(out_npz + ".tmp.npz", **done)
        os.replace(out_npz + ".tmp.npz", out_npz)
        sec = time.process_time() - t0
        meta["cpu_s"] += sec
        meta["points"].append(tb)
        meta.update(arm=arm, H=H, S=S, R=R, HB=HB, member_ticks=S * R * HB * len(meta["points"]),
                    cpu_s_per_member_tick=meta["cpu_s"] / (S * R * HB * len(meta["points"])),
                    keys=f"member_keys(make_key(77, {H}, tick), S*R), member-major (seed, replicate)")
        json.dump(meta, open(out_js, "w"), indent=1)
        print(arm, "branch", tb, "cpu", round(sec, 1), "L2 end mean", np.round(done[f"p{tb}"][:, :, -1].mean((0, 1)), 3).tolist(), flush=True)


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "main":
        run_main(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
    elif mode == "branch":
        run_branch(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
    elif mode == "area64":
        run_main(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), H=64, mut_dt=float(sys.argv[6]),
                 tag=f"area64_{sys.argv[2]}")
    elif mode == "area64x":                    # area64x ARM S T SEED MUT_DT M0 TAG: members M0..M0+S-1 of ensemble(M0+S, SEED)
        run_main(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), H=64, mut_dt=float(sys.argv[6]),
                 tag=f"{sys.argv[8]}_{sys.argv[2]}", m0=int(sys.argv[7]))
    else:
        raise SystemExit(__doc__)
