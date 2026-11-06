"""Item 4: composition operators on the real A_gliders world (refine is on a toy: refine_toy.py).

usage: python -B compose_demo.py stack|product|stride|couple   -> results/compose_<part>.json

stack    level 2 = Psi_population o Phi_objects (count, total mass, mean speed, fusion-rate EMA),
         observed instead of level 1; its fusion count, inferred from level 1 only, audited
         against the tracker's own fusion events (a designer-side view of the same memory).
product  A_gliders x A_gliders (two independent glider worlds, noise streams 0 and 1):
         the product level equals the pair pathwise; the default joint port (k = 16, one zero-sum
         over the union, one hidden permutation) and what its cross-block commands do to mass.
stride   S_10(S_20(L)) = S_200(L) pathwise (counter-based noise), burn-in included; the tracker
         is not natural under stride: at stride 200 identities break (note, Prop. 10(e)).
couple   the glider world's coarse level (read by a sensor at the port's resolution) wired into
         the input port of a linear-Gaussian oscillator (vw.lingauss): u = clip(gain * W y),
         W = left-minus-right mass imbalance. Against a zero wire with the same keys the source
         path is unchanged and the destination's response equals sum_s A^(t-s) u(s) (closed form).
"""
import json
import sys
import time

import _paths
import jax
import jax.numpy as jnp
import numpy as np

import vw
import aworld as AW
import phi as PH

part = sys.argv[1]
out = {"part": part}
t_start = time.time()


def mass(x):
    return np.asarray(x).sum((-2, -1))


# ----------------------------------------------------------------------------- stack
if part == "stack":
    specs, parts = AW.build(with_objects=False)
    cfg = parts["cfg"]
    po, tr, LW = PH.phi_objects("A_gliders", audit=True)
    pop, fused_count = PH.population(tr.K, LW.NF, cfg.H, cfg.W)
    lev = parts["level"]
    base1 = vw.WorldSpec(base=lev, chain=(po,), inport=vw.InputPort(admissible=AW.INPUTS), outport=AW.OBS,
                         burn_in=AW.BURN_TICKS * AW.STRIDE, public_notes=AW.NOTE, name="A_gliders/objects+audit")
    s1 = vw.stride(base1, AW.STRIDE)
    s2 = vw.stack(s1, pop)
    w = AW.MapWorld(s2, world_seed=3)
    out["card"] = w.card()
    B, T = 4, 150
    ens = w.designer.ensemble(B, seed=(41,))
    ens, rec = AW.chunked_rollout(w.designer, ens, T, chunk=10, rec=("L1", "L2", "obs"))
    Y1, Y2 = rec["L1"], rec["L2"]                               # (B, T+1, 149), (B, T+1, 4)
    nf = tr.K * LW.NF
    g = Y1[..., nf:]                                             # next uid, births, deaths, fusions, fissions
    true_f = np.diff(g[..., 3], axis=1)                          # tracker: absorbed parents per tick
    true_d = np.diff(g[..., 2], axis=1)
    fc = jax.jit(jax.vmap(jax.vmap(fused_count)))
    inf_f = np.asarray(fc(jnp.asarray(Y1[:, :-1, :nf]), jnp.asarray(Y1[:, 1:, :nf])))
    tp = float(np.minimum(inf_f, true_f).sum())
    out["level2"] = {"names": PH.POP_NAMES, "members": B, "ticks": T,
                     "mean": Y2[:, 1:].mean((0, 1)).tolist(), "sd_over_time": Y2[:, 1:].std(1).mean(0).tolist(),
                     "count_range": [float(Y2[..., 0].min()), float(Y2[..., 0].max())]}
    out["fusion_audit"] = {"tracker_fusions": float(true_f.sum()), "tracker_deaths": float(true_d.sum()),
                           "inferred_fusions": float(inf_f.sum()), "matched": tp,
                           "precision": tp / max(inf_f.sum(), 1), "recall": tp / max(true_f.sum(), 1),
                           "ticks_exact": float((inf_f == true_f).mean()),
                           "tracker_fusion_rate_per_tick": float(true_f.mean()),
                           "level2_ema_rate_mean": float(Y2[:, 20:, 3].mean())}
    out["obs_dim"] = int(rec["obs"].shape[-1])
    out["memory_sizes"] = {"level1": int(tr.n_m), "level2": int(nf + 5 + 2)}

# ----------------------------------------------------------------------------- product
elif part == "product":
    specs, parts = AW.build(with_objects=False)
    sc = specs["coarse"]
    cfg = parts["cfg"]
    sp = vw.product(sc, sc, name="A_gliders x A_gliders")
    # (1) the product level equals the pair, pathwise, at the Level layer
    w1 = AW.MapWorld(sc, world_seed=0)
    e = w1.designer.ensemble(2, seed=(77,))
    xa, xb = e.carry.x[0], e.carry.x[1]
    key = jax.random.key(5)
    Lp, La = sp.base, sc.base
    nu = La.input_dim
    stp = jax.jit(lambda x: Lp.step(Lp.params, x, vw.Noise(key, 3), jnp.zeros(2 * nu)))
    sta = jax.jit(lambda x, i: La.step(La.params, x, vw.Noise(jax.random.fold_in(key, i), 3), jnp.zeros(nu)))
    ya, yb = stp((xa, xb))
    out["pair_equality_max_abs"] = [float(jnp.abs(ya - sta(xa, 0)).max()), float(jnp.abs(yb - sta(xb, 1)).max())]
    # (2) the joint port and cross-block commands
    w = AW.MapWorld(sp, world_seed=11)
    out["card"] = {k: w.card()[k] for k in ("n_in", "n_obs", "inputs")}
    o0 = w.reset(seed=1)
    d = w.designer
    inv = AW.inverse_in_map(w)
    X = d.state()["x"]
    m0 = [mass(X[0]), mass(X[1])]
    SA = np.asarray(X[0]).sum(0).ravel()
    dense_A, empty_A = np.argsort(-SA)[:4], np.argsort(SA)[:4]
    SB = np.asarray(X[1]).sum(0).ravel()
    empty_B = np.argsort(SB)[:4] + nu
    cases = {}
    for nm, srcA in (("sources at dense cells of A", dense_A), ("sources at empty cells of A", empty_A)):
        w.reset(seed=1)
        a = {int(inv[i]): -0.5 for i in srcA}
        a.update({int(inv[i]): 0.5 for i in empty_B})
        w.step(a)                                                 # admissible: k = 8, zero sum, total 4
        X1 = d.state()["x"]
        X0 = X                                                    # the law conserves mass: compare with t = 0
        cases[nm] = {"dmass_A_per_channel": (mass(X1[0]) - mass(X0[0])).tolist(),
                     "dmass_B_per_channel": (mass(X1[1]) - mass(X0[1])).tolist(),
                     "dmass_total": float(mass(X1[0]).sum() + mass(X1[1]).sum() - mass(X0[0]).sum() - mass(X0[1]).sum())}
    out["cross_block_commands"] = cases
    out["note"] = ("both commands pass the product port (k=8 <= 16, sum 0, total 4); each factor's kick sees a non-zero-sum "
                   "command: A removes what is there and the pooled matter is lost, B adds the positive part split equally "
                   "over channels (the VW-0 kick's designer-probe branch)")

# ----------------------------------------------------------------------------- stride
elif part == "stride":
    specs, parts = AW.build(with_objects=False)
    lev, params = parts["level"], parts["level"].params
    w0 = AW.MapWorld(specs["coarse"], world_seed=0)
    x = w0.designer.ensemble(1, seed=(55,)).carry.x[0]
    key = jax.random.key(8)
    S20_10 = vw.stride_level(vw.stride_level(lev, 20), 10)
    S200 = vw.stride_level(lev, 200)
    u0 = jnp.zeros(lev.input_dim)
    a = jax.jit(lambda x: S20_10.step(params, x, vw.Noise(key, 4), u0))(x)
    b = jax.jit(lambda x: S200.step(params, x, vw.Noise(key, 4), u0))(x)
    out["S10_S20_vs_S200_one_tick_max_abs"] = float(jnp.abs(a - b).max())
    # worlds at stride 20 and 200 with the audited tracker: same designer seed -> same level-0 path
    po, tr, LW = PH.phi_objects("A_gliders", audit=True)
    base1 = vw.WorldSpec(base=lev, chain=(po,), inport=vw.InputPort(admissible=AW.INPUTS), outport=AW.OBS,
                         burn_in=AW.BURN_TICKS * AW.STRIDE, name="objects+audit")
    s20 = vw.stride(base1, 20)
    s200 = vw.stride(s20, 10)
    B, T200 = 4, 30
    res = {}
    for nm, spec, T, ch in (("stride20", s20, T200 * 10, 20), ("stride200", s200, T200, 10)):
        w = AW.MapWorld(spec, world_seed=0)
        ens = w.designer.ensemble(B, seed=(57,))
        x_start = np.asarray(ens.carry.x)
        ens, rec = AW.chunked_rollout(w.designer, ens, T, chunk=ch, rec=("L1",))
        Y = rec["L1"]
        nf = tr.K * LW.NF
        S = Y[..., :nf].reshape(B, T + 1, tr.K, LW.NF)
        g = Y[..., nf:]
        ev = g[:, -1, 1:] - g[:, 0, 1:]                       # births, deaths, fusions, fissions
        pres = S[..., 0] > 0.5
        speed = np.hypot(S[..., 10], S[..., 11])[pres]
        res[nm] = {"ticks": T, "substeps_per_tick": 20 if nm == "stride20" else 200, "x_start": x_start,
                   "x_end": np.asarray(ens.carry.x), "events_per_1000_substeps": (ev.sum(0) / (B * T * (20 if nm == "stride20" else 200)) * 1000).tolist(),
                   "mean_objects": float(pres.sum(-1).mean()), "median_speed_px_per_tick": float(np.median(speed)),
                   "uid_issued_per_object": float((g[:, -1, 0] - g[:, 0, 0]).sum() / max(pres.sum(-1).mean() * B, 1))}
        print(nm, {k: v for k, v in res[nm].items() if not k.startswith("x_")}, flush=True)
    out["same_level0_path"] = {"start_max_abs": float(np.abs(res["stride20"]["x_start"] - res["stride200"]["x_start"]).max()),
                               "end_max_abs": float(np.abs(res["stride20"]["x_end"] - res["stride200"]["x_end"]).max())}
    out["tracker"] = {k: {kk: vv for kk, vv in v.items() if not kk.startswith("x_")} for k, v in res.items()}
    out["event_names"] = ["births", "deaths", "fusions", "fissions"]

# ----------------------------------------------------------------------------- couple
elif part == "couple":
    from vw import lingauss as LG
    specs, parts = AW.build(with_objects=False)
    G = AW.G
    th = 2 * np.pi / 12
    Aosc = 0.97 * np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    osc = LG.LinearGaussian(A=Aosc, C=np.eye(2), Q=0.05 * np.eye(2), r=0.05,
                            inputs=vw.Admissible(k=2, lo=-1.0, hi=1.0), name="osc")
    dst = osc.spec()
    left = np.zeros(3 * G * G)
    for c in range(2):                      # channel-0 and channel-1 block means, left minus right half
        for i in range(G):
            for j in range(G):
                left[c * G * G + i * G + j] = 1.0 if j < G // 2 else -1.0
    Wm = jnp.asarray(np.stack([left, np.roll(left.reshape(3, G, G), 0, 1).transpose(0, 2, 1).ravel()]))   # (2, 192)
    gain = 20.0

    def wire(y):
        return gain * (Wm @ y) / (G * G)

    cw = vw.couple(specs["coarse"], dst, wire, readout_noise=0.0)
    cz = vw.couple(specs["coarse"], dst, lambda y: 0.0 * (Wm @ y), readout_noise=0.0)
    w, wz = AW.MapWorld(cw, world_seed=2), AW.MapWorld(cz, world_seed=2)
    out["card"] = {k: w.card()[k] for k in ("n_in", "n_obs", "inputs")}
    B, T = 2, 40
    e, ez = w.designer.ensemble(B, seed=(13,)), wz.designer.ensemble(B, seed=(13,))
    m_start = mass(e.carry.x[0])
    e, rec = AW.chunked_rollout(w.designer, e, T, chunk=10, rec=("L1", "x"))
    ez, recz = AW.chunked_rollout(wz.designer, ez, T, chunk=10, rec=("L1", "x"))
    ng = 3 * G * G
    ys, yd = rec["L1"][..., :ng], rec["L1"][..., ng:]
    ysz, ydz = recz["L1"][..., :ng], recz["L1"][..., ng:]
    q = specs["coarse"].outport.quantum
    U = np.clip(gain * np.einsum("ij,btj->bti", np.asarray(Wm), q * np.round(ys / q)) / (G * G), -1.0, 1.0)
    delta = np.zeros((B, T + 1, 2))
    delta[:, 0] = yd[:, 0] - ydz[:, 0]       # the wire already acted during the shared burn-in
    for t in range(T):                       # linear destination: delta(t+1) = A (delta(t) + u(t))
        delta[:, t + 1] = (delta[:, t] + U[:, t]) @ Aosc.T
    out["src_unaffected_max_abs"] = float(np.abs(ys - ysz).max())
    out["src_mass_rel_change"] = float(np.abs(mass(e.carry.x[0]) / m_start - 1).max())
    out["dst_response_vs_closed_form_max_abs"] = float(np.abs((yd - ydz) - delta).max())
    out["dst_response_rms"] = float(np.sqrt(((yd - ydz) ** 2).mean()))
    out["wire_u_rms"] = float(np.sqrt((U ** 2).mean()))
    out["wire_saturated_frac"] = float((np.abs(U) >= 1.0).mean())
    w.reset(seed=4)
    inv = AW.inverse_in_map(w)
    A = np.asarray(w.designer.state()["x"][0])
    S = A.sum(0).ravel()
    a = {int(inv[i]): -0.5 for i in np.argsort(-S)[:4]}
    a.update({int(inv[i]): 0.5 for i in np.argsort(S)[:4]})
    o1 = w.step(a)
    out["agent_step_on_src_port_ok"] = list(o1.shape)

out["seconds"] = time.time() - t_start
print(json.dumps(vw.jsonable(out), indent=1)[:3000])
json.dump(vw.jsonable(out), open(f"{_paths.RESULTS}/compose_{part}.json", "w"), indent=1)
