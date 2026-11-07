"""Why the closure data are not reproduced with tracker='jax': level-0 rounding depends on the compiled program.

usage: python -B level0_context.py   -> level0_context.json

(a) level 0 after init + burn-in (MapWorld designer ensembles, designer seed 301, world_seed 0), objects
    world with the host tracker vs the JAX tracker: B = 1, 2, 3 members (member keys do not depend on B,
    so a member's level 0 should not either); burn-in of 0, 1, 3 ticks (B = 2).
(b) rollouts from the same given states (4 members, 10 ticks, zero input): host-tracker, JAX-tracker and
    coarse (no tracker) worlds.
(c) compiled init + burn-in program (B = 2, 3 burn-in ticks): where the Flow-Lenia kernel FFT is computed
    and which fusion builds its input; whether the 20-substep loop body is the same in both programs.
(d) the kernel construction itself is rounding-sensitive to compilation: flowlenia_jax.kernel_fft under
    jit vs op by op.
"""
import collections
import json
import os
import re
import sys

sys.path.insert(0, "/home/user/evalwork/vecworld/vw1/port")
import _paths  # noqa: E402,F401
import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

import vw  # noqa: E402
import aworld as AW  # noqa: E402
import flowlenia_jax as FJ  # noqa: E402

OUT = os.path.dirname(os.path.abspath(__file__))
res = {}


def x_after_burnin(kind, B, burn=AW.BURN_TICKS, view="objects"):
    specs, _ = AW.build(tracker=kind, burn_ticks=burn, with_objects=(view != "coarse"))
    w = AW.MapWorld(specs[view], world_seed=0)
    return np.asarray(w.designer.ensemble(B, seed=(301,)).carry.x), w


# (a)
xh1, _ = x_after_burnin("host", 1)
xj1, _ = x_after_burnin("jax", 1)
xh2, _ = x_after_burnin("host", 2)
xj2, _ = x_after_burnin("jax", 2)
res["a_after_50_burnin_ticks"] = {
    "B1_host_vs_jax_max_abs": float(np.abs(xh1 - xj1).max()),
    "B2_host_vs_jax_max_abs": float(np.abs(xh2 - xj2).max()),
    "member0_host_B1_vs_host_B2_max_abs": float(np.abs(xh1[0] - xh2[0]).max())}
xj3, _ = x_after_burnin("jax", 3)
xh3, _ = x_after_burnin("host", 3)
res["a_member0_vs_B1_max_abs"] = {"host_B2": float(np.abs(xh2[0] - xh1[0]).max()),
                                  "host_B3": float(np.abs(xh3[0] - xh1[0]).max()),
                                  "jax_B2": float(np.abs(xj2[0] - xj1[0]).max()),
                                  "jax_B3": float(np.abs(xj3[0] - xj1[0]).max())}
res["a_member1_host_B2_vs_B3_max_abs"] = float(np.abs(xh2[1] - xh3[1]).max())
res["a_member1_jax_B2_vs_B3_max_abs"] = float(np.abs(xj2[1] - xj3[1]).max())
res["a_B2_by_burnin_ticks_host_vs_jax_max_abs"] = {
    str(b): float(np.abs(x_after_burnin("host", 2, b)[0] - x_after_burnin("jax", 2, b)[0]).max()) for b in (0, 1, 3)}
print(res, flush=True)

# (b)
x0 = np.concatenate([xh2, xh2[:, :, ::-1]], 0)
keys = jax.vmap(lambda k: jax.random.fold_in(k, 6))(vw.member_keys(vw.make_key(3, 0, 301), 4))
roll = {}
for view, kind in (("objects", "host"), ("objects", "jax"), ("coarse", "host")):
    specs, _ = AW.build(tracker=kind, with_objects=(view != "coarse"))
    d = AW.MapWorld(specs[view], world_seed=0).designer
    _, r = d.rollout(d.from_states(jnp.asarray(x0), keys=keys), None, T=10, rec=("x",))
    roll[f"{view}:{kind}"] = r["x"]
res["b_rollout_from_given_states_max_abs_vs_objects_host"] = {
    k: float(np.abs(v - roll["objects:host"]).max()) for k, v in roll.items()}
print(res["b_rollout_from_given_states_max_abs_vs_objects_host"], flush=True)


# (c)
def comps(txt):
    out = {}
    for b in re.split(r"\n(?=%?[\w.\-]+ \(.*\) -> .* \{\n|ENTRY )", txt):
        m = re.match(r"%?([\w.\-]+) \(", b)
        if m:
            out[m.group(1)] = b
    return out


def closure_of(C, name, seen=None):
    seen = set() if seen is None else seen
    if name in seen or name not in C:
        return seen
    seen.add(name)
    for callee in re.findall(r"(?:calls=|body=|condition=|to_apply=)%?([\w.\-]+)", C[name]):
        closure_of(C, callee, seen)
    return seen


def norm(b):
    b = "\n".join(b.split("\n")[1:])
    b = re.sub(r", metadata=\{[^}]*\}", "", b)
    b = re.sub(r"%[\w.\-]+", "%v", b)
    b = re.sub(r"\b[\w.\-]+\.\d+\b", "id", b)
    return re.sub(r"backend_config=\{.*?\}\}?", "", b)


prog = {}
for kind in ("host", "jax"):
    specs, _ = AW.build(tracker=kind, burn_ticks=3)
    w = AW.MapWorld(specs["objects"], world_seed=0)
    ki = vw.member_keys(vw.make_key(3, 0, 301), 2)
    kd = jax.vmap(lambda k: jax.random.fold_in(k, 6))(ki)
    txt = w._v_init.lower(w.params, ki, kd).compile().as_text()
    C = comps(txt)
    body = re.search(r"while\([^\n]*body=%?([\w.\-]+)[^\n]*known_trip_count\":\{\"n\":\"20\"", txt).group(1)
    fft = []
    cur = "?"
    for line in txt.split("\n"):
        if re.match(r"^(ENTRY|%?[\w.\-]+ \()", line):
            cur = "ENTRY" if line.startswith("ENTRY") else re.match(r"%?([\w.\-]+)", line).group(1)
        if re.search(r"= c128\[20,128,65\][^\n]* fft\(", line):         # the kernel RFFT
            fft.append(cur)
    kern = re.search(r"%(?:[\w.\-]+) = c128\[20,128,65\][^\n]* fft\(%([\w.\-]+)\)", txt).group(1)
    kline = [ln for ln in txt.split("\n") if re.search(r"%" + re.escape(kern) + r" = ", ln)][0]
    ops = re.findall(r"%([\w.\-]+)", kline.split("fusion(")[1].split(")")[0])
    kinds = []
    for o in ops:
        ln = [x for x in txt.split("\n") if re.search(r"%" + re.escape(o) + r" = ", x)]
        if ln:
            kinds.append(re.search(r"kind=(\w+)", ln[0]).group(1) + ("/ynn" if "__ynn_fusion" in ln[0] else ""))
    prog[kind] = {"kernel_rfft_computed_in": ["program entry (hoisted out of the member loop)" if f == "ENTRY"
                                              else f"loop body {f}" for f in fft],
                  "kernel_rfft_input_fusion_kinds": kinds,
                  "stride_body": collections.Counter(norm(C[c]) for c in closure_of(C, body))}
res["c_compiled_init_program"] = {k: {kk: vv for kk, vv in v.items() if kk != "stride_body"} for k, v in prog.items()}
res["c_compiled_init_program"]["stride_loop_body_identical"] = prog["host"]["stride_body"] == prog["jax"]["stride_body"]
print(res["c_compiled_init_program"], flush=True)

# (d)
lev, cfg, _ = FJ.make_level("A_gliders", 0.5)
a = np.asarray(jax.jit(lambda p: FJ.kernel_fft(cfg, p))(lev.params))
b = np.asarray(FJ.kernel_fft(cfg, lev.params))
res["d_kernel_fft_jit_vs_op_by_op_max_abs"] = float(np.abs(a - b).max())
json.dump(res, open(f"{OUT}/level0_context.json", "w"), indent=1)
print(json.dumps(res, indent=1))
