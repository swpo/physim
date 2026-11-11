"""adv_sim -- simulations for the adversary's form-free repair on the designer's own check (sublevel_second/gvh.py).

    python -B adv_sim.py OUT.npz [lam] [size] [n_lab] [seed] [key=value ...] [H=1]

DESIGN-STAGE CHECK, CPU, tiny size. PILOT values: never to be reused as an exam.

It repeats gvh.py's set-up call for call (same members, programs, Lab episodes, test items, truths, public runs,
in the same order, so the numbers of gvh's result file are reproduced and its H column can be quoted as paired),
keeps the focus view at EVERY tick 0..32 instead of four horizons, and adds what the adversary's recipes need:
public-law runs under TRANSFORMED programs, with common random numbers against a no-input run.

The transformed programs are a filter bank on the command, with no knowledge of the hidden part:
    delay 0, 4, 8, 16 ticks  x  spatial blur none / 3 x 3 bumps (total coefficient kept)
(8 programs; `d0b0` is the program itself). With H=1 the designer's told-the-form grid fit is also run (gvh's H).
"""
import os
import sys
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
SUB = os.path.abspath(os.path.join(HERE, "..", "sublevel_second"))
sys.path.insert(0, SUB)

import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

import sublevel as SL  # noqa: E402
from sublevel import MJ, MW  # noqa: E402
import screen as SC  # noqa: E402
import gvh as GV  # noqa: E402

T0, H, R = GV.T0, GV.H, GV.R
DELAYS, BLURS, RB = (0, 4, 8, 16), (0, 1), 3


def blur_matrix(cfg):
    """(m, m) row-stochastic: each bump's coefficient spread evenly over the 3 x 3 bumps around it (periodic)."""
    cen = MJ.bump_centres(cfg)
    sp = cfg.H / cfg.G
    dy = (cen[:, None, 0] - cen[None, :, 0] + cfg.H / 2) % cfg.H - cfg.H / 2
    dx = (cen[:, None, 1] - cen[None, :, 1] + cfg.W / 2) % cfg.W - cfg.W / 2
    W = ((np.abs(dy) <= sp + 1e-9) & (np.abs(dx) <= sp + 1e-9)).astype(float)
    return W / W.sum(1, keepdims=True)


def transform(P, delay, blur, Wb):
    Q = np.zeros_like(P)
    Q[delay:] = P[:P.shape[0] - delay]
    return Q @ Wb if blur else Q


def main():
    out = sys.argv[1]
    args = sys.argv[2:]
    pos = [a for a in args if "=" not in a]
    kv = {k: float(v) for k, v in (a.split("=", 1) for a in args if "=" in a)}
    do_H = bool(kv.pop("H", 0))
    lam = float(pos[0]) if len(pos) > 0 else 1.0
    size = int(pos[1]) if len(pos) > 1 else 64
    n_lab = int(pos[2]) if len(pos) > 2 else 16
    seed = int(pos[3]) if len(pos) > 3 else 5
    nats, M = 300.0, 16
    truth = dict({"rho": 0.005, "DX": 0.2}, **kv, lam=lam)
    cfg = SL.small_cfg(size)
    t_cpu = time.process_time()
    rng = np.random.default_rng(seed)
    spec_p, parts = SL.build(cfg)
    dp = MW.MapWorld(spec_p, world_seed=1).designer
    spec_h, _ = SL.build(cfg, "pro", hidden=truth)
    wh = MW.MapWorld(spec_h, world_seed=0)
    dh = wh.designer
    wg = MW.MapWorld(spec_h, world_seed=2)
    dg = wg.designer
    K = parts["tracker"].K

    ens = dh.ensemble(M, seed=(78, seed))
    ens, rec0 = dh.rollout(ens, None, T=T0, rec=("L1",))
    x = {k: np.asarray(v) for k, v in ens.x.items()}
    _, tgt = SC.programs(cfg, rec0["L1"][:, -1], K, nats, np.random.default_rng(0))
    ok = [i for i in range(M) if tgt[i]["mass_t0"] > 0]
    lab_m = [i for i in ok if i < 8]
    test_m = [i for i in ok if i >= 8]
    lab = [(lab_m[j % len(lab_m)],) + GV.one_program(cfg, tgt[lab_m[j % len(lab_m)]], rng, nats) for j in range(n_lab)]
    test = [(i,) + GV.one_program(cfg, tgt[i], rng, nats) for i in test_m for _ in range(4)]

    def run(d, items, reps, full, zero=False, progs=None, keys=None):
        """focus view (n_items, reps, H + 1, 2) of `reps` futures per item under its program (or none, or progs)."""
        mem = np.repeat([it[0] for it in items], reps)
        xs = {k: x[k][mem] for k in (x if full else MJ.FIELDS)}
        P = np.repeat(np.stack([it[1] for it in items] if progs is None else progs), reps, axis=0)
        _, r = d.rollout(d.from_states(xs, keys=keys), None if zero else P, T=H, rec=("L1",))
        L1 = r["L1"].reshape(len(items), reps, H + 1, -1)
        return np.stack([SC.focus_view(L1[j], K, tgt[it[0]], size) for j, it in enumerate(items)])

    # --- gvh.py's runs, in gvh.py's order (the world's key counters advance as they do there)
    y_lab = run(dh, lab, 1, True)[:, 0]
    pub_lab, pub0_lab = run(dp, lab, R, False), run(dp, lab, R, False, zero=True)
    Yt = run(dh, test, R, True)
    pub, pub0 = run(dp, test, R, False), run(dp, test, R, False, zero=True)
    cpu_gvh = time.process_time() - t_cpu

    # --- the adversary's filter bank on the public law, common random numbers against a no-input run
    Wb = blur_matrix(cfg)
    kl, kt = dp.w._fresh_keys(len(lab) * RB), dp.w._fresh_keys(len(test) * RB)
    z_lab, z_test = run(dp, lab, RB, False, zero=True, keys=kl), run(dp, test, RB, False, zero=True, keys=kt)
    names, B_lab, B_test = [], [], []
    for dl in DELAYS:
        for bl in BLURS:
            names.append(f"d{dl}b{bl}")
            B_lab.append((run(dp, lab, RB, False, progs=[transform(it[1], dl, bl, Wb) for it in lab], keys=kl) - z_lab).mean(1))
            B_test.append((run(dp, test, RB, False, progs=[transform(it[1], dl, bl, Wb) for it in test], keys=kt) - z_test).mean(1))
    cpu_bank = time.process_time() - t_cpu - cpu_gvh

    extra = {}
    if do_H:                                                 # gvh.py's H, unchanged (27-point grid, least squares)
        sc = Yt[:, :, list(GV.HS)].reshape(-1, len(GV.HS), 2).std(0)
        sc = np.maximum(sc, 0.1 * np.median(sc[sc > 1e-9]))
        base = dict(wh.params)
        fits = []
        for la in GV.GRID["lam"]:
            for rh in GV.GRID["rho"]:
                for dx in GV.GRID["DX"]:
                    wg.params = dict(base, lam=jnp.asarray(la, jnp.float64), rho=jnp.asarray(rh, jnp.float64),
                                     DX=jnp.asarray(dx, jnp.float64))
                    m = run(dg, lab, 3, True).mean(1)[:, list(GV.HS)]
                    fits.append((float((((y_lab[:, list(GV.HS)] - m) / sc) ** 2).sum()), la, rh, dx))
        fits.sort()
        _, la, rh, dx = fits[0]
        wg.params = dict(base, lam=jnp.asarray(la, jnp.float64), rho=jnp.asarray(rh, jnp.float64), DX=jnp.asarray(dx, jnp.float64))
        extra = {"Hh": run(dg, test, R, True), "H_fit": np.array([la, rh, dx])}

    np.savez_compressed(
        out, y_lab=y_lab, pub_lab=pub_lab, pub0_lab=pub0_lab, Yt=Yt, pub=pub, pub0=pub0,
        B_lab=np.stack(B_lab, 1), B_test=np.stack(B_test, 1), names=np.array(names),
        F_lab=np.stack([it[2] for it in lab]), F_test=np.stack([it[2] for it in test]),
        lab_member=np.array([it[0] for it in lab]), test_member=np.array([it[0] for it in test]),
        truth_keys=np.array(sorted(truth)), truth_vals=np.array([truth[k] for k in sorted(truth)]),
        meta=np.array([size, n_lab, seed, R, RB]), cpu=np.array([cpu_gvh, cpu_bank, time.process_time() - t_cpu]), **extra)
    print("saved", out, "cpu_s gvh-part", round(cpu_gvh, 1), "bank", round(cpu_bank, 1), "total", round(time.process_time() - t_cpu, 1))


if __name__ == "__main__":
    main()
