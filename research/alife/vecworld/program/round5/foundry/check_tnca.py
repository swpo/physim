"""check_tnca -- numerical checks of the foundry family on this platform (CPU: about 2 minutes).

    python -B check_tnca.py [--out results/checks.json] [--seed 1]

1. conservation and positivity: N worlds from the prior (seed + 1000), T ticks with random wind commands:
   relative drift of the total mass, of each kind when kappa = 0, the smallest cell.
2. symmetry of the law (noise-free substep): translations and the 8 lattice symmetries commute with it.
3. vw integration: the world as a vw.Level inside a vw.World with a block-view coarse-graining, one short
   agent episode with a wind command; vw.invariant_drift.
4. wind channel: the realised coefficients have the declared law; vw.nats.kl_check of a 3-tick program;
   delivery (centre-of-mass shift of each kind under a uniform command against a no-command twin on the
   same noise, in px per tick and per unit command, against the hidden coupling wq).
5. weight statistics: the growth factor of the fastest mode of the linear symbol against a direct
   noise-free simulation of that mode.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

import tnca as TN  # noqa: E402
import vw  # noqa: E402
from vw.core import Noise  # noqa: E402
from vw.nats import NatsBudget, kl_check, shift_llr  # noqa: E402


def dev(t):
    return {k: jnp.asarray(v) for k, v in t.items()}


def check_conservation(seed, n=8, T=100):
    fam = TN.FAM
    ths = TN.draw_thetas(seed + 1000, range(n))
    keys = jax.random.split(jax.random.key(seed), n)
    rng = np.random.default_rng(seed)
    U = jnp.asarray(rng.normal(size=(n, T, fam.NW)) * 0.5)            # about 256 nats per tick

    def one(th, key, U):
        x0 = TN.init(th, jax.random.fold_in(key, 1))

        def body(x, tu):
            t, u = tu
            xn = TN.tick(th, x, Noise(key, t), u)
            return xn, (xn.sum((1, 2)), xn.min(), xn.max())
        x, (m, mn, mx) = jax.lax.scan(body, x0, (jnp.arange(T), U))
        return x0.sum((1, 2)), m, mn, mx
    m0, m, mn, mx = [np.asarray(a) for a in jax.jit(jax.vmap(one))(dev(ths), keys, U)]
    k0 = ths["kappa"] == 0
    tot = np.abs(m.sum(-1) - m0.sum(-1)[:, None]).max(1) / m0.sum(-1)
    kind = (np.abs(m - m0[:, None]) / m0[:, None]).max((1, 2))
    return dict(n_worlds=n, ticks=T, substeps=T * fam.NSUB, with_wind_commands=True,
                total_mass_rel_drift_max=float(tot.max()), n_kappa0=int(k0.sum()),
                kind_mass_rel_drift_max_kappa0=float(kind[k0].max()) if k0.any() else None,
                kind_mass_rel_change_max_kappa_pos=float(kind[~k0].max()) if (~k0).any() else None,
                min_cell=float(mn.min()), max_cell=float(mx.max()),
                ok=bool(tot.max() < 1e-10 and mn.min() >= 0 and (not k0.any() or kind[k0].max() < 1e-10)))


def check_symmetry(seed, n=4):
    fam = TN.FAM
    ths = TN.draw_thetas(seed + 1000, range(n))
    zx, zw = jnp.zeros((fam.C, 4, fam.H, fam.W)), jnp.zeros((2, fam.H, fam.W))
    f = jax.jit(lambda th, x: TN.substep(th, x, zx, zw))
    worst = {}
    for i in range(n):
        th = dev({k: v[i] for k, v in ths.items()})
        x = TN.init(th, jax.random.key(seed + i))
        for _ in range(3):
            x = f(th, x)
        y = f(th, x)
        ops = {"shift(5,-9)": lambda a: jnp.roll(a, (5, -9), (-2, -1)), "rot90": lambda a: jnp.rot90(a, 1, (-2, -1)),
               "rot180": lambda a: jnp.rot90(a, 2, (-2, -1)), "flip_y": lambda a: jnp.flip(a, -2),
               "flip_x": lambda a: jnp.flip(a, -1), "transpose": lambda a: jnp.swapaxes(a, -2, -1)}
        for name, g in ops.items():
            e = float(jnp.abs(f(th, g(x)) - g(y)).max() / jnp.abs(y).max())
            worst[name] = max(worst.get(name, 0.0), e)
    return dict(n_worlds=n, rel_error_max=worst, ok=bool(max(worst.values()) < 1e-9))


def check_vw(seed):
    fam = TN.FAM
    th = TN.draw_theta(seed + 1000, 0)
    lev = TN.make_level(th)
    phi = vw.CoarseGrain.of(lambda x: TN.block_view(x).reshape(-1), name="Phi_coarse8")
    nq = (fam.C + 1) * 64
    spec = vw.WorldSpec(base=lev, chain=(phi,), inport=vw.InputPort(admissible=vw.Admissible(lo=-2.0, hi=2.0),
                                                                 in_map=tuple(range(fam.NW))),
                        outport=vw.ObservePort(quantum=1e-4, out_map=tuple(range(nq))), burn_in=5,
                        name="foundry/tnca-check")
    w = vw.World(spec, world_seed=0)
    o0 = np.asarray(w.reset(0))
    u = np.zeros(fam.NW)
    u[fam.GW * fam.GW:] = 0.5
    obs = [np.asarray(w.step({i: float(v) for i, v in enumerate(u) if v != 0.0})) for _ in range(3)]
    drift = vw.invariant_drift(w, T=20, B=4)
    budget = NatsBudget.isotropic(fam.NW, fam.sigma_w)
    return dict(level=lev.name, observation_dim=int(o0.shape[-1]), steps=len(obs),
                obs_finite=bool(np.isfinite(np.stack(obs)).all()), invariant_drift_abs=drift,
                charge_of_command_nats=budget.cost(u), tnca_nats=TN.nats(u),
                ok=bool(np.isfinite(np.stack(obs)).all() and abs(budget.cost(u) - TN.nats(u)) < 1e-9
                        and max(drift.values()) < 1e-9))


def check_wind(seed, n_paths=4000):
    fam = TN.FAM
    key = jax.random.key(seed + 7)
    keys = jax.random.split(key, n_paths)
    rng = np.random.default_rng(seed)
    prog = np.zeros((3, fam.NW))
    prog[0, [3, 70]] = [1.5 * fam.sigma_w, -1.5 * fam.sigma_w]
    prog[1, 17] = 4 * fam.sigma_w
    prog[2, rng.choice(fam.NW, 8, replace=False)] = rng.normal(size=8) * fam.sigma_w
    P = jnp.asarray(prog)
    draw = jax.jit(jax.vmap(lambda k: jax.vmap(lambda t, u: TN.wind_coeff(Noise(k, t), u))(jnp.arange(3), P)))
    a = np.asarray(draw(keys))                                        # (paths, 3, NW) under P_u
    eta = a - prog[None]
    llr = shift_llr(a, prog, fam.sigma_w ** 2 * np.eye(fam.NW))
    klc = kl_check(llr, TN.nats(prog))
    # delivery: uniform +x command against the twin on the same noise
    out = dict(noise_mean_abs_max=float(np.abs(eta.mean((0, 1))).max()), noise_std=float(eta.std()),
               sigma_w=fam.sigma_w, kl_check=klc, embedding_dc_gain=float(np.asarray(
                   TN.wind_field(jnp.ones((fam.NW,)))).mean()))
    th_np = TN.draw_theta(seed + 1000, 3)
    th_np = dict(th_np, beta=np.float64(0.0), gam=np.float64(0.0), kappa=np.float64(0.0))   # passive matter
    th = dev(th_np)
    mu_ = float(th_np["mu"])
    u1 = np.zeros(fam.NW)
    u1[fam.GW * fam.GW:] = 1.0                                         # x-component, every block
    X = jnp.arange(fam.W)

    def com_x(x):                                                     # circular mean of column index, per kind
        ang = 2 * jnp.pi * X[None, None, :] / fam.W
        return jnp.arctan2((x * jnp.sin(ang)).sum((1, 2)), (x * jnp.cos(ang)).sum((1, 2))) * fam.W / (2 * jnp.pi)

    def run(k, u):
        x = TN.init(th, jax.random.fold_in(k, 1))
        # one dense patch per kind so that a centre of mass exists
        bump = jnp.exp(-((X[None, :] - 16.0) ** 2 + (X[:, None] - 32.0) ** 2) / 50.0)   # centre column 16
        x = x * 0.2 + bump[None] * th["dens"][:, None, None] * 5

        def body(x, t):
            return TN.tick(th, x, Noise(k, t), u), None
        x1, _ = jax.lax.scan(body, x, jnp.arange(4))
        return com_x(x), com_x(x1), x1
    runj = jax.jit(jax.vmap(run, in_axes=(0, None)))
    ks = jax.random.split(jax.random.key(seed + 9), 8)
    c0, c1, xa = runj(ks, jnp.asarray(u1))
    _, c1z, xz = runj(ks, jnp.zeros(fam.NW))
    _, c1z2, xz2 = runj(ks, jnp.zeros(fam.NW))
    shift = np.asarray(c1 - c1z).mean(0) / 4.0                        # px per tick per unit command
    out["delivery"] = dict(command="x-component 1.0 on all 64 blocks, 4 ticks", nats_per_tick=TN.nats(u1),
                           passive_world="beta = gam = kappa = 0", mu=float(th_np["mu"]),
                           wq=[float(v) for v in th_np["wq"]], shift_px_per_tick=[float(v) for v in shift],
                           shift_over_wq=[float(s / q) for s, q in zip(shift, th_np["wq"])],
                           expected_noise_free=[float(fam.NSUB * 0.25 * mu_ * 2 * np.sinh(q) / (
                               1 - mu_ + 0.25 * mu_ * (2 + 2 * np.cosh(q)))) for q in th_np["wq"]],
                           twin_same_key_identical=bool((np.asarray(xz) == np.asarray(xz2)).all()))
    out["ok"] = bool(abs(klc["z"]) < 4 and abs(out["noise_std"] / fam.sigma_w - 1) < 0.01
                     and abs(out["embedding_dc_gain"] - 1) < 1e-12
                     and all(0.5 < s / e < 2.0 for s, e in zip(shift, out["delivery"]["expected_noise_free"])))
    return out


def check_linear(seed, n_try=40):
    """Growth of the fastest linear mode: symbol against a direct noise-free simulation (small amplitude)."""
    fam = TN.FAM
    ths = TN.draw_thetas(seed + 1000, range(n_try))
    sym = jax.jit(lambda th: TN.linear_symbol(th))
    zx, zw = jnp.zeros((fam.C, 4, fam.H, fam.W)), jnp.zeros((2, fam.H, fam.W))
    f = jax.jit(lambda th, x: TN.substep(th, x, zx, zw))
    rows = []
    for i in range(n_try):
        th = dev({k: v[i] for k, v in ths.items()})
        s = sym(th)
        lam = np.asarray(s["lam"])
        mod = np.abs(lam)
        mod[0, 0] = 0
        iy, ix, j = np.unravel_index(np.argmax(mod), mod.shape)
        g = float(mod[iy, ix, j])
        if not (1.02 < g < 1.6) or abs(np.angle(lam[iy, ix, j])) > 1e-6:
            continue
        # eigenvector of the symbol at that wavevector, from a fresh jvp
        xbar = np.asarray(s["xbar"])
        x0 = jnp.broadcast_to(jnp.asarray(xbar)[:, None, None], (fam.C, fam.H, fam.W))
        yy, xx = np.meshgrid(np.arange(fam.H), np.arange(fam.W), indexing="ij")
        wave = np.cos(2 * np.pi * (np.fft.fftfreq(fam.H)[iy] * yy + np.fft.fftfreq(fam.W)[ix] * xx))
        J = np.zeros((fam.C, fam.C))
        for c in range(fam.C):
            d = np.zeros((fam.C, fam.H, fam.W))
            d[c] = wave
            r = np.asarray(jax.jvp(lambda x: f(th, x), (x0,), (jnp.asarray(d),))[1])
            J[:, c] = (r * wave[None]).sum((1, 2)) / (wave ** 2).sum()
        ev, evec = np.linalg.eig(J)
        k = int(np.argmax(np.abs(ev)))
        v = np.real(evec[:, k])
        amp = 1e-7 * xbar.min()
        x = x0 + amp * jnp.asarray(v[:, None, None] * wave[None])
        a0 = amp
        n = 6
        for _ in range(n):
            x = f(th, x)
        proj = np.asarray(((x - x0) * jnp.asarray(wave)[None]).sum((1, 2)) / (wave ** 2).sum())
        a1 = float(np.linalg.norm(proj) / np.linalg.norm(v))
        rows.append(dict(draw=i, symbol_growth=g, jvp_growth=float(np.abs(ev[k])), simulated_growth=(a1 / a0) ** (1 / n),
                         wavelength_px=float(1 / np.hypot(np.fft.fftfreq(fam.H)[iy], np.fft.fftfreq(fam.W)[ix]))))
        if len(rows) >= 3:
            break
    err = max((abs(r["simulated_growth"] / r["symbol_growth"] - 1) for r in rows), default=None)
    return dict(worlds=rows, rel_error_max=err, ok=bool(rows and err < 1e-3))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "results", "checks.json"))
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--quick", action="store_true")
    a = ap.parse_args()
    res = dict(platform=dict(jax=jax.__version__, numpy=np.__version__, backend=jax.default_backend(),
                             devices=[str(d) for d in jax.devices()], dtype="float64"),
               family=vars(TN.FAM), seed=a.seed)
    checks = [("conservation", lambda: check_conservation(a.seed, *((4, 20) if a.quick else (8, 100)))),
              ("symmetry", lambda: check_symmetry(a.seed, 2 if a.quick else 4)),
              ("vw", lambda: check_vw(a.seed)),
              ("wind", lambda: check_wind(a.seed, 500 if a.quick else 4000)),
              ("linear", lambda: check_linear(a.seed))]
    for name, fn in checks:
        t = time.time()
        res[name] = fn()
        res[name]["seconds"] = round(time.time() - t, 1)
        print(name, json.dumps(res[name], default=float)[:1500], flush=True)
    res["ok"] = all(res[k]["ok"] for k, _ in checks)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w") as f:
        json.dump(res, f, indent=1, default=float)
    print("checks ok:", res["ok"])
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
