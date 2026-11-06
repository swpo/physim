"""Checker: constraint enforcement (every family, nothing run or charged on rejection, whole-program
validation, the zero-sum tolerance case) and card leakage on composed worlds.
Run from vw1/check: ../.venv/bin/python -B constraints_card_check.py [--gliders]  -> constraints_card.json"""
import json
import math
import os
import re
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
VW1 = os.path.dirname(HERE)
sys.path.insert(0, VW1)

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

import vw  # noqa: E402
from vw.lingauss import ParamLG, lumpable_level, random_lg, ring  # noqa: E402
from vw.toys import additive_kick, mass_ring  # noqa: E402

out = {"cases": {}}


def snap(w):
    ep = w._ep
    return (ep.t, w.ticks_used, w._spent, w._last_in, np.asarray(vw.flat(ep.carry.x)).tobytes(),
            np.asarray(ep.carry.key == ep.carry.key).tobytes() if False else int(np.asarray(ep.carry.t)[0]))


def expect_reject(w, name, fn, exc=vw.InputViolation):
    before = snap(w)
    try:
        fn()
    except exc as e:
        ok = snap(w) == before
        out["cases"][name] = {"rejected": True, "state_unchanged": ok, "msg": str(e)[:160]}
        assert ok, name
        return
    out["cases"][name] = {"rejected": False}
    raise AssertionError(f"{name}: accepted")


# ---------------------------------------------------------------- A: every constraint family
adm = vw.Admissible(k=4, lo=-1.0, hi=1.0, total=2.0, zero_sum=True, min_interval=2, episode_budget=3.0)
w = vw.World(mass_ring(inputs=adm).replace(max_ticks=60), 1)
w.reset(3)
expect_reject(w, "sparsity", lambda: w.step({0: .1, 1: .1, 2: .1, 3: -.2, 4: -.1}))
expect_reject(w, "bound", lambda: w.step({0: 1.2, 1: -1.2}))
expect_reject(w, "total", lambda: w.step({0: 1, 1: 1, 2: -1, 3: -1}))
expect_reject(w, "zero_sum_2e-9", lambda: w.step({0: 0.45 + 2e-9, 1: -0.45}))
expect_reject(w, "format_key_str", lambda: w.step({"a": 1}))
expect_reject(w, "format_key_bool", lambda: w.step({True: 0.5, 1: -0.5}))
expect_reject(w, "format_range", lambda: w.step({99: 0.5, 1: -0.5}))
expect_reject(w, "format_nan", lambda: w.step({0: float("nan"), 1: 0.0}))
expect_reject(w, "format_dense_shape", lambda: w.step(np.zeros(5)))
w.step({0: 0.5, 1: -0.5})                                            # t=0 accepted, spent 1.0
expect_reject(w, "interval", lambda: w.step({2: 0.3, 3: -0.3}))      # t=1 < 0 + 2
w.step(None)                                                         # t=1 empty tick is fine
w.step({0: 1.0, 1: -1.0})                                            # t=2, spent 3.0 = budget
w.step(None)
expect_reject(w, "episode_budget", lambda: w.step({0: 0.01, 1: -0.01}))
# whole-program validation: a violation late in the program -> nothing runs
w.reset(4)
expect_reject(w, "program_late_bound", lambda: w.run([(0, {0: .5, 1: -.5}), (6, {0: 1.5, 1: -1.5})], [1, 8]))
expect_reject(w, "program_interval", lambda: w.run([(0, {0: .5, 1: -.5}), (1, {0: .5, 1: -.5})], [3]))
expect_reject(w, "program_input_after_last_query", lambda: w.run([(0, {0: .5, 1: -.5}), (9, {0: .5, 1: -.5})], [5]))
expect_reject(w, "program_budget_cumulative", lambda: w.run([(0, {0: 1, 1: -1}), (2, {0: 1, 1: -1})], [4]))
w.run([], [0], seed=None)
expect_reject(w, "max_ticks", lambda: w.run([], [200]), exc=vw.BudgetExhausted)
# continuing-episode program: interval is checked against the agent's last input before run()
w.reset(5)
w.step({0: 0.5, 1: -0.5})
expect_reject(w, "program_interval_vs_prior_step", lambda: w.run([(0, {2: .5, 3: -.5})], [1]))

# quantum + zero sum
wq = vw.World(mass_ring(inputs=vw.Admissible(k=4, lo=-1, hi=1, zero_sum=True, quantum=0.1)), 1)
wq.reset(0)
wq.step({0: 0.1, 1: 0.2, 2: -0.3})
expect_reject(wq, "quantum_integer_sum", lambda: wq.step({0: 0.1, 1: 0.2, 2: -0.2}))
expect_reject(wq, "quantum_not_multiple", lambda: wq.step({0: 0.15, 1: -0.15}))

# ---------------------------------------------------------------- B: zero-sum tolerance case
res = {}
for kick_name, kick in (("additive", additive_kick), ("pooling", None)):
    for noise in (0.0, 0.1):
        kw = {} if kick is None else {"kick": kick}
        spec = mass_ring(**kw).replace(inport=vw.InputPort(admissible=vw.Admissible(k=4, lo=-1, hi=1, total=2.0, zero_sum=True),
                                                           noise=noise))
        wt = vw.World(spec, 2)
        wt.reset(1)
        m0 = float(wt.designer.state()["x_flat"].sum())
        a = {0: 0.45 + 9e-10, 1: -0.45}                              # sum 9e-10, total |a| = 0.9
        assert not wt.inport.admissible.violations(a)
        can = wt.inport.admissible.canonical(a)
        for _ in range(25):
            wt.step(a)
        m1 = float(wt.designer.state()["x_flat"].sum())
        res[f"{kick_name}_actnoise{noise}"] = {"canonical_sum": float(sum(can.values())),
                                               "rel_mass_drift_25_ticks": abs(m1 / m0 - 1)}
        assert abs(m1 / m0 - 1) < 1e-12
        before = snap(wt)
        try:
            wt.step({0: 0.45 + 2e-9, 1: -0.45})
            raise AssertionError("2e-9 accepted")
        except vw.InputViolation:
            assert snap(wt) == before
# what the additive world would gain without canonicalisation (designer path, no checks)
wt = vw.World(mass_ring(kick=additive_kick), 2)
wt.reset(1)
ens = wt.designer.branch()
x0 = ens.x_flat().sum()
u = np.zeros(wt.n_in)
u[0], u[1] = 0.45 + 9e-10, -0.45
for _ in range(25):
    ens = ens.step(u)
res["additive_raw_designer_inputs_mass_gain"] = float(ens.x_flat().sum() - x0)
out["zero_sum_tolerance"] = res

# ---------------------------------------------------------------- C: card leakage
r, rl = ring(), random_lg()
lgf, fine, Psi = lumpable_level(r, eta=0.0)
psi = vw.CoarseGrain.of(lambda x: jnp.asarray(Psi) @ x, name="psi-secret")
ema = vw.CoarseGrain(phi=lambda y, m: jnp.concatenate([vw.flat(y), m]), init_memory=lambda y: vw.flat(y),
                     update_memory=lambda m, y: 0.5 * m + 0.5 * vw.flat(y), name="ema-tracker")
worlds = {
    "ring": r.spec(), "paramLG": ParamLG().spec(), "mass_ring": mass_ring(),
    "stack": vw.stack(r.spec(), ema), "product": vw.product(r.spec(), rl.spec()),
    "product_corr": vw.product(r.spec(), r.spec(), noise=("correlated", 0.5)),
    "stride": vw.stride(r.spec(), 7), "refine": vw.refine(r.spec(), fine, psi),
    "couple": vw.couple(r.spec(), mass_ring(), wire=lambda y: jnp.zeros(32)),
    "deep": vw.stride(vw.stack(vw.product(vw.refine(r.spec(), fine, psi), rl.spec()), ema), 3),
}
generic = {"noise", "replay", "inputs", "total", "level", "world", "phi", "read", "both"}
leaks = {}
for k, s in worlds.items():
    wk = vw.World(s, 0)
    txt = json.dumps(wk.card(), default=str).lower()
    names = {s.name, s.base.name} | {c.name for c in s.chain}
    toks = set()
    for n in names:
        toks |= {t for t in re.split(r"[^a-z0-9]+", n.lower()) if len(t) >= 3 and not t.isdigit()}
    toks -= generic
    toks |= {"stride", "refine", "stack", "product", "couple", "psi", "ema", "tracker", "ring", "lingauss", "secret",
             "correlated", "kick", "pool", "block"}
    hit = sorted(t for t in toks if re.search(rf"\b{t}", txt))
    leaks[k] = {"keys": sorted(wk.card().keys()), "hits": hit}
out["card"] = leaks
out["card_example_stride7"] = vw.World(worlds["stride"], 0).card()
out["card_deep_inputs"] = vw.World(worlds["deep"], 0).card()["inputs"]

# ---------------------------------------------------------------- D: the A_gliders world (optional)
if "--gliders" in sys.argv:
    sys.path.insert(0, os.path.join(VW1, "port"))
    import aworld  # noqa: E402
    specs, parts = aworld.build(with_objects=True)
    for k in ("coarse", "objects", "both"):
        txt = json.dumps(vw.World(specs[k], 0).card(), default=str).lower()
        out["card"][f"A_gliders_{k}"] = {"hits": [t for t in ("glider", "flow", "lenia", "coarse", "object", "stride",
                                                              "tracker", "slot", "a_gliders", "20", "128")
                                                  if t in txt], "notes": vw.World(specs[k], 0).card()["notes"]}
    wg = vw.World(specs["coarse"], 0)
    wg.reset(0)
    inv = aworld.inverse_in_map(wg)
    x = np.asarray(wg.designer.state()["x"])
    S = x.sum(0).ravel()
    dense = np.argsort(-S)[:2]
    empty = np.argsort(S)[:2]
    a = {int(inv[dense[0]]): -0.3, int(inv[dense[1]]): -0.15 + 9e-10, int(inv[empty[0]]): 0.25, int(inv[empty[1]]): 0.2}
    m0 = x.sum((1, 2))
    wg.step(a)
    m1 = np.asarray(wg.designer.state()["x"]).sum((1, 2))
    g = {"accepted_sum": float(sum(a.values())), "rel_channel_mass_change_after_tick": float(np.abs(m1 / m0 - 1).max())}
    before = snap(wg)
    try:
        wg.step({int(inv[dense[0]]): -0.45 - 2e-9, int(inv[empty[0]]): 0.45})
        g["2e-9_rejected"] = False
    except vw.InputViolation as e:
        g["2e-9_rejected"] = True
        g["state_unchanged"] = snap(wg) == before
        g["msg"] = str(e)[:120]
    out["A_gliders_tolerance"] = g

print(json.dumps(out, indent=1, default=str))
json.dump(out, open(os.path.join(HERE, "constraints_card.json"), "w"), indent=1, default=str)
