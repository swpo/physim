"""(a) blind input visibility and (d) late differences, through the VW-1 InputPort and designer API.

usage: python -B visibility.py S0 S1 [R]      -> results/vis/state_XXX.npz (float32 level-1 records)

For each saved test state s (results/states.npz, fresh designer ensemble), one MapWorld rollout call
holds, with R noise keys k_r (member keys make_key(4242, s) folded with r):
  twin_r        no input, key k_r       (the R twins are also the fresh-noise oracle replicates)
  <cond>_r      open-loop program <cond>, key k_r (identical noise to twin_r)
  null          no input, key k_0       (must equal twin_0 exactly: the twin-validity check)
Conditions (agent coordinates; cells <-> coordinates through the hidden in_map, designer side):
  rand_x1       Admissible.sample (default constraint) at t = 0
  rand_x8       Designer.random_program(rate=1) over t = 0..7 (default constraint)
  body_x1       4 sources -0.5 / 4 sinks +0.5 on tracked-body cells (run_inputs.py 'body'), t = 0
  body_x8same   the same body input at t = 0..7
  k32_x1        16 sources -1 / 16 sinks +1 on body cells (designer probe: k = 32, sum|a| = 32), t = 0
  empty_x1      4 sources -0.5 / 4 sinks +0.5 on empty cells (A_sum < 1e-4, >= 8 px from any body), t = 0
Default-constraint programs go through Designer.program_dense(validate=True) (the port's checks and
canonicalisation); the k32 probe is densified unvalidated and flagged inadmissible.
Records L1 = <Phi_coarse (192), Phi_objects (144)> at t = 0..32, and the moved matter per input tick
(from the level-0 state before each kick; numpy transcription of the JAX kick)."""
import os
import sys
import time

import common as CM
import jax
import jax.numpy as jnp
import numpy as np
import scipy.ndimage as ndi

from vw.world import make_key, member_keys
import aworld as AW

S0, S1 = int(sys.argv[1]), int(sys.argv[2])
R = int(sys.argv[3]) if len(sys.argv) > 3 else 6
TMAX, TIN, CH = 32, 8, 8
CONDS = ["rand_x1", "rand_x8", "body_x1", "body_x8same", "k32_x1", "empty_x1"]
OUT = f"{CM.RES}/vis"
os.makedirs(OUT, exist_ok=True)

w, parts, _ = CM.build_world("both")
d = w.designer
C = w.inport.admissible
inv = AW.inverse_in_map(w)
st = np.load(f"{CM.RES}/states.npz")
X, M = st["x"], st["m"]


def far_empty(mask, dmin):
    tile = np.tile(~mask, (3, 3))
    dist = ndi.distance_transform_edt(tile)[CM.H:2 * CM.H, CM.W:2 * CM.W]
    return dist >= dmin


def to_dict(src, snk, b):
    a = {int(inv[c]): -b for c in src}
    a.update({int(inv[c]): b for c in snk})
    return a


def programs(s, rng):
    S = X[s].sum(0).ravel()
    lab, _ = CM.mem_parts(M[s][None])
    body = lab[0] > 0
    bc = np.flatnonzero(body & (S > 1e-3))
    emp = np.flatnonzero(far_empty(body.reshape(CM.H, CM.W), 8.0).ravel() & (S < 1e-4))
    out = {}
    out["rand_x1"] = [(0, C.sample(rng, w.n_in))]
    out["rand_x8"] = d.random_program(rng, TIN, rate=1.0)
    c = rng.choice(bc, 8, replace=False)
    out["body_x1"] = [(0, to_dict(c[:4], c[4:], 0.5))]
    c = rng.choice(bc, 8, replace=False)
    a = to_dict(c[:4], c[4:], 0.5)
    out["body_x8same"] = [(t, dict(a)) for t in range(TIN)]
    c = rng.choice(bc, 32, replace=False)
    out["k32_x1"] = [(0, to_dict(c[:16], c[16:], 1.0))]
    c = rng.choice(emp, 8, replace=False)
    out["empty_x1"] = [(0, to_dict(c[:4], c[4:], 0.5))]
    meta = {"n_body_cells": int(bc.size), "n_empty_cells": int(emp.size)}
    return out, meta, body, S


t_all = time.time()
for s in range(S0, S1):
    fn = f"{OUT}/state_{s:03d}.npz"
    if os.path.exists(fn):
        continue
    t0 = time.time()
    rng = np.random.default_rng([2026, 11, 6, s])
    progs, meta, body, S = programs(s, rng)
    adm, dense = {}, {}
    for cn, pr in progs.items():
        adm[cn] = all(not C.violations(a) for _, a in pr)
        dense[cn] = d.program_dense(pr, TIN, validate=adm[cn])        # (TIN, n_in) agent coordinates
    names = [f"twin_{r}" for r in range(R)] + [f"{cn}_{r}" for cn in CONDS for r in range(R)] + ["null"]
    kidx = [r for r in range(R)] + [r for cn in CONDS for r in range(R)] + [0]
    B = len(names)
    P = np.zeros((B, TIN, w.n_in))
    for i, nm in enumerate(names):
        cn = nm.rsplit("_", 1)[0]
        if cn in dense:
            P[i] = dense[cn]
    keysR = member_keys(make_key(4242, s), R)
    keys = keysR[jnp.asarray(kidx)]
    xb = jnp.asarray(np.repeat(X[s][None], B, 0))
    mb = (((), jnp.asarray(np.repeat(M[s][None], B, 0))),)
    ens = d.from_states(xb, mem=mb, keys=keys)
    ens, r1 = d.rollout(ens, P, T=CH, rec=("L1", "x"))
    Ys, xs = [r1["L1"]], r1["x"]                                        # x: (B, CH+1, 32768)
    # moved matter per input tick, and where the sources / sinks sit (state before the kick)
    moved = np.zeros((B, TIN))
    for i, nm in enumerate(names):
        for t in range(TIN):
            if P[i, t].any():
                u = np.zeros(CM.HW)
                u[w.in_map] = P[i, t]
                moved[i, t] = CM.moved_matter(xs[i, t], u)
    null_x = float(np.abs(xs[names.index("null")] - xs[0]).max())
    del xs, r1
    done = CH
    while done < TMAX:
        ens, r = d.rollout(ens, None, T=CH, rec=("L1",))
        Ys.append(r["L1"][:, 1:])
        done += CH
    Y = np.concatenate(Ys, 1)                                          # (B, TMAX+1, 336)
    null_y = float(np.abs(Y[names.index("null")] - Y[0]).max())
    site = {}
    for cn, pr in progs.items():
        a = pr[0][1]
        cells = w.in_map[np.array(sorted(a))]
        vals = np.array([a[j] for j in sorted(a)])
        site[cn] = np.stack([cells, vals, S[cells], body[cells]], 1)
    # random admissible commands at this state: matter moved and site occupancy (numpy kick only)
    nsamp = 200
    mv, empt, inb, srce = [], [], [], []
    for _ in range(nsamp):
        a = C.sample(rng, w.n_in)
        u = np.zeros(CM.HW)
        cells = w.in_map[np.array(list(a))]
        u[cells] = np.array(list(a.values()))
        mv.append(CM.moved_matter(X[s].reshape(2, -1), u))
        empt.append(float((S[cells] < 1e-3).mean()))
        inb.append(float(body[cells].mean()))
        sc = cells[u[cells] < 0]
        srce.append(float((S[sc] < 1e-3).mean()))
    np.savez_compressed(fn, Y=Y.astype(np.float32), names=np.array(names), moved=moved,
                        adm=np.array([adm[c] for c in CONDS]), conds=np.array(CONDS),
                        null_x=null_x, null_y=null_y, n_body=meta["n_body_cells"], n_empty=meta["n_empty_cells"],
                        rand_moved=np.array(mv), rand_empty_frac=np.array(empt), rand_body_frac=np.array(inb),
                        rand_src_empty_frac=np.array(srce),
                        **{f"site_{c}": v for c, v in site.items()})
    print(f"state {s} B={B} null_x={null_x:.3g} null_y={null_y:.3g} moved(median per cond)=" +
          " ".join(f"{c}:{np.median(moved[[i for i, n in enumerate(names) if n.startswith(c)]].sum(1)):.3g}"
                   for c in CONDS) + f"  {time.time() - t0:.0f}s (total {time.time() - t_all:.0f}s)", flush=True)
