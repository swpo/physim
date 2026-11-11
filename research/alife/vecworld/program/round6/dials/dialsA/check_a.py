"""check_a -- study A: CPU checks of the law switch and of the recipes (a few CPU-minutes).

1 tick      xtick with xw = 0 against gworld.tick, one tick with inputs above the trigger: bitwise.
2 family    xlaw.sim_episodes_x (XRunner, eta = 0) against ladder_lib.sim_episodes (VRunner): the same keys,
            classes and programs; observations and programs bitwise equal. With eta = 4 the aimed and
            regional episodes must differ and the input-free ones must not.
3 world     xlaw.build_world_x at xw = 0 against sbi_lib.build_world: a Lab batch (reset, 4 input-free ticks,
            then programs of every class), observations bitwise equal; at xw = 4 they differ.
4 classes   a_nets.program_class recovers the mix class of every simulated program.
5 residual  a_nets.res_fit / res_apply on synthetic blocks: a planted per-class, per-region affine residual
            is recovered (ridge 0.05 x rows shrinks it by 1 / 1.05 at most for a unit-variance design).
Writes results/check_a.json. PILOT values only.
"""
import json
import os
import sys
import time

sys.dont_write_bytecode = True
t00 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import xlaw as X  # noqa: E402
import a_nets as AN  # noqa: E402
import jax  # noqa: E402
import numpy as np  # noqa: E402
from vw.secret import Secret  # noqa: E402
from vw.world import make_key, member_keys  # noqa: E402

LL, SL, GW, PL = X.LL, X.SL, X.GW, X.PL
X.assert_one_checkout()
out = {"what": "CPU checks of study A's law switch and recipes", "PILOT_NEVER_REUSE_AS_EXAM": True,
       "backend": jax.default_backend(), "x64": bool(jax.config.jax_enable_x64)}

out["one_tick"] = X.one_tick_check(B=3, burn=2)
print("1 tick", json.dumps(out["one_tick"]), f"{time.time() - t00:.0f}s", flush=True)

# ---- 2 family
names, lo, hi = LL.box(4)
P, H, BURN, B = 4, 4, 2, 8
rng = np.random.default_rng(3)
th = lo + (hi - lo) * rng.random((B, 4))
cls = np.array(list("abcdabcd"))
keys = member_keys(make_key(77, 0), B)
RN, XR = SL.VRunner(burn=BURN), X.XRunner(burn=BURN)
a = LL.sim_episodes(RN, names, th, keys, 77, P, H, chunk=B, classes=cls)
b = X.sim_episodes_x(XR, names, th, np.zeros(B), keys, 77, P, H, chunk=B, classes=cls)
c = X.sim_episodes_x(XR, names, th, np.full(B, 4.0), keys, 77, P, H, chunk=B, classes=cls)
dmax = np.abs(c["obs"][:, :, :LL.NC].astype(float) - a["obs"][:, :, :LL.NC]).max((1, 2))
out["family"] = {"members": B, "ticks": BURN + P + H, "obs_bitwise_equal_eta0": bool(np.array_equal(a["obs"], b["obs"])),
                 "programs_bitwise_equal_eta0": bool(np.array_equal(a["U"], b["U"])),
                 "max_abs_obs_diff_eta0": float(np.abs(a["obs"].astype(float) - b["obs"]).max()),
                 "max_abs_block_diff_eta4_by_class": {k: float(dmax[cls == k].max()) for k in "abcd"},
                 "nats_by_class": {k: float(a["nats"][cls == k].mean()) for k in "abcd"}}
print("2 family", json.dumps(out["family"]), f"{time.time() - t00:.0f}s", flush=True)

# ---- 4 classes (on the programs just simulated)
got = np.array([AN.program_class(u) for u in a["U"][:, P:].astype(float)])
empty = np.abs(a["U"]).sum((1, 2)) == 0
out["classes"] = {"mix": cls.tolist(), "structural": got.tolist(), "empty_program": empty.tolist(),
                  "agree_or_empty": bool(np.all((got == cls) | (empty & (got == "a"))))}
print("4 classes", json.dumps(out["classes"]), flush=True)

# ---- 3 world
sec = Secret()
n_lab = 4
classes = np.array(list("abcd"))
res = {}
for tag, world in (("public", SL.build_world(GW.theta_to_params(dict(zip(names, th[0]))), burn=BURN)),
                   ("xw0", X.build_world_x(X.xparams(names, th[0], 0.0), burn=BURN)),
                   ("xw4", X.build_world_x(X.xparams(names, th[0], 4.0), burn=BURN))):
    lab = SL.BatchLab(world, sec.child("lab", 0), nats=PL.budget(total=SL.EP_CAP * n_lab), max_ticks=n_lab * (1 + P + H))
    mk = lambda j, hist: LL.CLASSES[classes[j]](np.random.default_rng([5, j]), hist, H, SL.EP_CAP)
    res[tag] = lab.run_batch(list(range(n_lab)), P, H, mk)
d4 = np.abs(res["xw4"]["obs"][:, :, :LL.NC].astype(float) - res["public"]["obs"][:, :, :LL.NC]).max((1, 2))
out["world"] = {"episodes": n_lab, "obs_bitwise_equal_xw0": bool(np.array_equal(res["public"]["obs"], res["xw0"]["obs"])),
                "programs_equal_xw0": bool(np.array_equal(res["public"]["U"], res["xw0"]["U"])),
                "max_abs_block_diff_xw4_by_class": {k: float(d4[classes == k].max()) for k in "abcd"}}
print("3 world", json.dumps(out["world"]), f"{time.time() - t00:.0f}s", flush=True)

# ---- 5 residual
G = X.G
rng = np.random.default_rng(9)
n, nh = 40, 3
z0 = rng.standard_normal((n, 3, G, G))
cl = np.array(list("abcd"))[rng.integers(0, 4, n)]
reg = rng.integers(0, 3, (n, G, G))
Wt = {(c_, ih, k): rng.standard_normal((4, 3)) for c_ in "abcd" for ih in range(nh) for k in range(3)}
f = np.concatenate([z0, np.ones_like(z0[:, :1])], 1).transpose(0, 2, 3, 1)
R = np.zeros((n, nh, G, G, 3))
for i in range(n):
    for ih in range(nh):
        for k in range(3):
            R[i, ih][reg[i] == k] = f[i][reg[i] == k] @ Wt[(cl[i], ih, k)]
W = AN.res_fit(z0, R.transpose(0, 1, 4, 2, 3), reg, cl, lam=1e-9)
corr = AN.res_apply(W, z0, reg, cl, nh).reshape(n, nh, 3, G, G) / AN.SCB
Ws = AN.res_fit(z0, R.transpose(0, 1, 4, 2, 3), reg, cl)
Rn = rng.standard_normal(R.shape).transpose(0, 1, 4, 2, 3)                     # pure noise: nothing to learn
_, ch_signal = AN.res_fit_cv(z0, R.transpose(0, 1, 4, 2, 3) + 0.1 * Rn, reg, cl)
_, ch_noise = AN.res_fit_cv(z0, Rn, reg, cl)
out["residual_cv"] = {"chosen_ridge_planted_signal": {k: str(v) for k, v in ch_signal.items()},
                      "chosen_ridge_pure_noise": {k: str(v) for k, v in ch_noise.items()}}
out["residual"] = {"max_abs_error_apply_no_ridge": float(np.abs(corr - R.transpose(0, 1, 4, 2, 3)).max()),
                   "n_maps": len(W), "ridge_0.05_slope_shrink_median": float(np.median([np.linalg.norm(Ws[k]) / np.linalg.norm(Wt[k]) for k in Ws])),
                   "unseen_class_gets_zero": bool(np.all(AN.res_apply({}, z0[:2], reg[:2], cl[:2], nh) == 0))}
print("5 residual", json.dumps(out["residual"]), flush=True)

out["ok"] = bool(out["one_tick"]["bitwise_xw0_equals_gworld"] and out["family"]["obs_bitwise_equal_eta0"]
                 and out["family"]["programs_bitwise_equal_eta0"] and out["world"]["obs_bitwise_equal_xw0"]
                 and out["classes"]["agree_or_empty"] and out["residual"]["max_abs_error_apply_no_ridge"] < 1e-6
                 and out["one_tick"]["max_abs_xw4_minus_gworld"] > 1e-3)
out["seconds"] = time.time() - t00
os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
json.dump(out, open(os.path.join(HERE, "results", "check_a.json"), "w"), indent=1)
print("ok" if out["ok"] else "FAILED", f"{out['seconds']:.0f}s")
sys.exit(0 if out["ok"] else 1)
