"""check_channel -- the substrate channel as implemented draws what the NatsBudget charges.

    python check_channel.py

1. Noise law: eta = channel(cfg, Noise(key, t), 0) over n_paths x n_ticks draws: mean, std against sigma_a,
   largest off-diagonal correlation.
2. KL certificate (EXAM 3.1, vw.nats.kl_check), run once: a 3-tick aimed program u_t (a +-1.5 sigma_a pair,
   a 4 sigma_a single push, an 8-coefficient pattern); realised u~ = channel(cfg, noise, u_t) on 4000 paths
   under P_u; per-path log-likelihood ratio of u~ against the no-input law; its mean against the declared
   charge sum_t |u_t|^2 / (2 sigma_a^2).
3. Delivery: the substrate a tick actually adds (level-0 S after one tick with u minus the twin with u = 0,
   same key, same state) against sum_j u_j b_j: the channel delivers what it says up to the law's own
   response within the tick.
4. Grid independence: the charge lives on the m coefficients, so it does not change with the grid (64^2 with
   G = 8 and 128^2 with G = 16: same 8 px spacing, same bump). For contrast, the same delivered field charged
   against the v1 suite's S noise (proportional, intensity 0.01 per sqrt(time), ell = 2 px, applied every
   native step) at the local levels S = 0.18 (inside cells) and 0.62 (bath), and a v1-style bump of std 2 px
   (= ell, WORLDS.md section 1).
Writes results/channel.json.
"""
import json
import os

import _paths
import jax
import jax.numpy as jnp
import numpy as np

import vw
from vw.nats import kl_check, shift_llr
import membrane_jax as MJ
import membrane_world as MW


def v1_charge(field, H, tick_time, S_level, s=0.01, ell=2.0, floor=1e-10):
    """Nats of a substrate field delivered over one tick against v1's S noise at a uniform level S_level:
    additive intensity s * S_level, smoothed with unit gain at k = 0 by exp(-ell^2 k^2 / 2): spectral variance
    per unitary-DFT mode tick_time (s S)^2 G(k)^2. Modes with G^2 < floor are dropped: there the smoothed noise
    has (numerically) no power, and the round-off content of any field would get an unbounded charge (with all
    modes kept the 64^2 value is 2.5x the 128^2 one for the same bump, from round-off alone)."""
    ky = 2 * np.pi * np.fft.fftfreq(H)[:, None]
    kx = 2 * np.pi * np.fft.fftfreq(H)[None, :]
    G2 = np.exp(-ell ** 2 * (kx ** 2 + ky ** 2))
    Fh = np.fft.fft2(field, norm="ortho")
    keep = G2 >= floor
    return float(0.5 * np.sum(np.abs(Fh[keep]) ** 2 / (tick_time * (s * S_level) ** 2 * G2[keep])))


def v1_charge_continuum(A, w, tick_time, S_level, s=0.01, ell=2.0):
    """The same charge for a continuum Gaussian bump of peak A and std w: A^2 pi w^4 / (2 T (s S)^2 (w^2 - ell^2)),
    infinite for w <= ell (inputs must be smoother than the noise)."""
    if w <= ell:
        return float("inf")
    return float(A ** 2 * np.pi * w ** 4 / (2 * tick_time * (s * S_level) ** 2 * (w ** 2 - ell ** 2)))


def main():
    cfg = MJ.Config()
    m, sa = cfg.m, cfg.sigma_a
    budget = MW.nats_budget(cfg)
    key = vw.make_key(77, 1)

    # 1. noise law
    n_paths, n_ticks = 1000, 8
    draw = jax.jit(jax.vmap(jax.vmap(lambda k, t, u: MJ.channel(cfg, vw.Noise(k, t), u), in_axes=(None, 0, 0)),
                            in_axes=(0, None, None)))
    E = np.asarray(draw(vw.member_keys(key, n_paths), jnp.arange(n_ticks), jnp.zeros((n_ticks, m)))).reshape(-1, m)
    C = np.corrcoef(E.T)
    law = {"n": int(E.shape[0]), "mean_abs_max": float(np.abs(E.mean(0)).max()), "std_mean": float(E.std(0).mean()),
           "std_min": float(E.std(0).min()), "std_max": float(E.std(0).max()), "sigma_a": sa,
           "max_abs_offdiag_corr": float(np.abs(C - np.eye(m)).max()),
           "expected_max_abs_offdiag_corr_iid": float(np.sqrt(2 * np.log(m * (m - 1) / 2) / E.shape[0]))}

    # 2. KL certificate for a 3-tick program
    U = np.zeros((3, m))
    U[0, 40], U[0, 41] = 1.5 * sa, -1.5 * sa
    U[1, 119] = 4 * sa
    U[2, [0, 17, 34, 51, 68, 85, 102, 255]] = sa * np.array([1, -2, 0.5, 1, -1, 2, 1.5, -0.5])
    charge = budget.program_cost([(t, U[t]) for t in range(3)])
    Ut = np.asarray(draw(vw.member_keys(vw.make_key(77, 2), 4000), jnp.arange(3), jnp.asarray(U)))
    llr = shift_llr(Ut, U, sa ** 2 * np.eye(m))
    kl = kl_check(llr, charge)

    # 3. delivery on a real state: one tick with u vs u = 0 (same key)
    lev = MJ.make_level(cfg)
    q = lev.params
    k = vw.make_key(77, 3)
    x = lev.init(q, k)
    x = jax.jit(lambda x: jax.lax.fori_loop(0, 200, lambda i, xx: lev.step(q, xx, vw.Noise(k, i), jnp.zeros(m)), x))(x)
    B = MJ.bump_basis(cfg)
    u = np.zeros(m)
    u[[119, 120, 135, 136]] = 0.05                          # feed four neighbouring bumps by 0.05 each
    one = jax.jit(lambda x, u: lev.step(q, x, vw.Noise(k, 200), u))
    dS = np.asarray(one(x, jnp.asarray(u))["S"] - one(x, jnp.zeros(m))["S"]).ravel()
    target = u @ B
    deliv = {"u": "0.05 on bumps 119, 120, 135, 136", "charge_nats": budget.cost(u),
             "delivered_total": float(dS.sum()), "target_total": float(target.sum()),
             "rel_l2_diff": float(np.linalg.norm(dS - target) / np.linalg.norm(target)),
             "peak_delivered": float(dS.max()), "peak_target": float(target.max())}

    # 4. grid independence and the v1 contrast
    contrast = {}
    for H, G in ((64, 8), (128, 16)):
        c = MJ.Config(H=H, W=H, G=G)
        one_field = (0.05 * MJ.bump_basis(c)[0]).reshape(H, H)
        yy, xx = np.mgrid[0:H, 0:H]
        d2 = ((yy - 4 + H / 2) % H - H / 2) ** 2 + ((xx - 4 + H / 2) % H - H / 2) ** 2
        bump2 = 0.05 * np.exp(-d2 / (2 * 2.0 ** 2))
        contrast[f"{H}"] = {"channel_nats_u0.05": float(MW.nats_budget(c).cost(np.eye(c.m)[0] * 0.05)),
                            "v1_nats_same_field_S0.18": v1_charge(one_field, H, c.tick_time, 0.18),
                            "v1_nats_same_field_S0.62": v1_charge(one_field, H, c.tick_time, 0.62),
                            "v1_nats_bump_std2px_S0.18": v1_charge(bump2, H, c.tick_time, 0.18),
                            "v1_nats_bump_std2px_S0.62": v1_charge(bump2, H, c.tick_time, 0.62),
                            "note": "v1 charges drop modes where the v1 noise power exp(-ell^2 k^2) < 1e-10"}
    contrast["continuum"] = {f"v1_nats_bump_std{w:g}px_S{lvl}": v1_charge_continuum(0.05, w, cfg.tick_time, lvl)
                             for w in (4.0, 2.0) for lvl in (0.18, 0.62)}
    # v1's S noise projected on one bump (sigma equivalent): KL of a peak-A bump = A^2 / (2 s_eq^2)
    s_eq = {lvl: float(0.05 / np.sqrt(2 * contrast["continuum"][f"v1_nats_bump_std4px_S{lvl}"])) for lvl in ("0.18", "0.62")}
    out = {"config": {"H": cfg.H, "G": cfg.G, "m": m, "sigma_a": sa, "bump_w": cfg.bump_w, "tick_time": cfg.tick_time,
                      "dt": cfg.dt},
           "noise_law": law, "kl_check": kl, "program_charge_nats": charge,
           "per_tick_charges": [budget.cost(v) for v in U], "card_guarantee": vw.nats.card_guarantee(charge),
           "delivery": deliv, "grid_contrast": contrast, "v1_S_noise_sigma_equivalent_per_bump": s_eq,
           "example_costs_nats": {f"u={v:g} on one coefficient": float(budget.cost(np.eye(m)[0] * v))
                                  for v in (0.005, 0.01, 0.02, 0.05, 0.1, 0.2)}}
    json.dump(out, open(os.path.join(_paths.RESULTS, "channel.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
