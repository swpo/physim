"""Checker re-run (writes only to this scratch folder).
    rerun.py repro64 T      : pilot.py's sel/neu worlds at 64^2, designer ensemble member 0 (seed 0), T ticks, R = 0;
                              compare L2 with the saved results/pilot_H64.npz rows.
    rerun.py seed128 T s    : 128^2 sel/neu twins from designer ensemble(1, seed=s), T ticks (an independent seed).
"""
import json, os, sys, time
sys.path.insert(0, "/home/user/evalwork/vecworld/program/track1/vortex_world")
import _paths  # noqa
import jax, jax.numpy as jnp, numpy as np
import vortex_jax as VJ, vortex_world as VW

OUT = os.path.dirname(os.path.abspath(__file__))
mode, T = sys.argv[1], int(sys.argv[2])
H = 64 if mode == "repro64" else 128
seed = 0 if mode == "repro64" else int(sys.argv[3])


def make(arm):
    cfg = VJ.Config(H=H, W=H, G=H // 16)
    specs, parts = VW.build(cfg)
    theta = dict(VJ.THETA, eps=0.0 if arm == "neu" else 0.2)
    return VW.MapWorld(specs["kinds"], world_seed=0, params={k: jnp.asarray(v, jnp.float64) for k, v in theta.items()})


res = {}
for arm in ("sel", "neu"):
    w = make(arm)
    d = w.designer
    t0 = time.process_time()
    ens = d.ensemble(1, seed=seed)
    L2 = []
    chunk = 25 if H == 64 else 20
    while ens.t < T:
        ens, r = d.rollout(ens, T=chunk, rec=("L2",))
        L2.append(r["L2"] if not L2 else r["L2"][:, 1:])
    res[arm] = np.concatenate(L2, 1)[0].astype(np.float32)
    print(arm, "cpu_s", round(time.process_time() - t0, 1), flush=True)
np.savez(os.path.join(OUT, f"{mode}_s{seed}.npz"), **res)
if mode == "repro64":
    D = np.load(os.path.join(_paths.RESULTS, "pilot_H64.npz"))
    for arm in ("sel", "neu"):
        s = D[f"{arm}_L2"][0, :T + 1]
        print(arm, "max |diff| vs saved", float(np.abs(res[arm] - s).max()), "rows", len(s))
else:
    for arm in ("sel", "neu"):
        sb = res[arm][:, 1].astype(float)
        print(arm, "s_b mean t500-1500", round(sb[100:300].mean(), 3), "t>=1500", round(sb[300:].mean(), 3) if T > 300 else None,
              "N mean", round(res[arm][100:, 0].mean(), 2), "share_by_100", np.round(sb[::40], 2).tolist())
