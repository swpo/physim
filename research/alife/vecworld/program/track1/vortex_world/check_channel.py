"""check_channel -- the stirring channel as implemented draws what the NatsBudget charges.

    python check_channel.py

1. Noise law: eta = channel(cfg, Noise(key, t), 0) over n_paths x n_ticks draws -- mean, std against
   sigma_a, largest off-diagonal correlation.
2. KL certificate (EXAM 3.1, vw.nats.kl_check): a 3-tick aimed program u_t (a +-1.5 sigma_a pair, a
   4 sigma_a single push, a 6-coefficient pattern); realised u~ = channel(cfg, noise, u_t) on 4000
   paths under P_u; per-path log-likelihood ratio of u~ against the no-input law; its mean against the
   declared charge sum_t |u_t|^2 / (2 sigma_a^2).
3. Grid independence: the charge lives on the m coefficients, so it does not change with the grid.
   For contrast, the same delivered vorticity field charged against the v1 wrapper's pixel noise
   (additive om, intensity 0.003 per sqrt(time), correlation length 2 px, white draws per native step)
   at 64^2 and 128^2, and a v1-style bump of std 2 px (= the noise length; WORLDS.md section 1).
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
import vortex_jax as VJ
import vortex_world as VW


def v1_pixel_charge(field, cfg: VJ.Config, sd=0.003, ell=2.0):
    """Nats of a vorticity field delivered over one tick against v1's additive om noise: per native
    step sd sqrt(dt) * irfft2(G * rfft2(white)), G = exp(-ell^2 k^2 / 2) (intensity form, dx = 1), summed
    over the tick's n_sub steps: spectral variance per unitary-DFT mode n_sub dt sd^2 G(k)^2."""
    ky = 2 * np.pi * np.fft.fftfreq(cfg.H)[:, None]
    kx = 2 * np.pi * np.fft.fftfreq(cfg.W)[None, :]
    G2 = np.exp(-ell ** 2 * (kx ** 2 + ky ** 2))
    Fh = np.fft.fft2(field, norm="ortho")
    return float(0.5 * np.sum(np.abs(Fh) ** 2 / (cfg.tick_time * sd ** 2 * G2)))


def main():
    cfg = VJ.Config(H=64, W=64, G=4)
    m, sa = cfg.m, cfg.sigma_a
    budget = VW.nats_budget(cfg)
    key = vw.make_key(77, 1)

    # 1. noise law
    n_paths, n_ticks = 2000, 8
    draw = jax.jit(jax.vmap(jax.vmap(lambda k, t, u: VJ.channel(cfg, vw.Noise(k, t), u), in_axes=(None, 0, 0)),
                            in_axes=(0, None, None)))
    keys = vw.member_keys(key, n_paths)
    E = np.asarray(draw(keys, jnp.arange(n_ticks), jnp.zeros((n_ticks, m)))).reshape(-1, m)
    C = np.corrcoef(E.T)
    law = {"n": int(E.shape[0]), "mean_abs_max": float(np.abs(E.mean(0)).max()), "std_mean": float(E.std(0).mean()),
           "std_min": float(E.std(0).min()), "std_max": float(E.std(0).max()), "sigma_a": sa,
           "max_abs_offdiag_corr": float(np.abs(C - np.eye(m)).max())}

    # 2. KL certificate for a 3-tick program
    U = np.zeros((3, m))
    U[0, 5], U[0, 6] = 1.5 * sa, -1.5 * sa
    U[1, 9] = 4 * sa
    U[2, [0, 3, 7, 8, 12, 15]] = sa * np.array([1, -2, 0.5, 1, -1, 2])
    charge = budget.program_cost([(t, U[t]) for t in range(3)])
    keys2 = vw.member_keys(vw.make_key(77, 2), 4000)
    Ut = np.asarray(draw(keys2, jnp.arange(3), jnp.asarray(U)))          # (paths, 3, m) realised under P_u
    llr = shift_llr(Ut, U, sa ** 2 * np.eye(m))
    kl = kl_check(llr, charge)

    # 3. grid independence and the v1 contrast
    contrast = {}
    for H, G in ((64, 4), (128, 8)):
        c = VJ.Config(H=H, W=H, G=G)
        B = VJ.stir_basis(c)
        one = (0.1 * B[0]).reshape(H, H)                       # u_0 = 0.1 delivered over one tick
        yy, xx = np.mgrid[0:H, 0:H]
        d2 = ((yy - H / 2 + H / 2) % H - H / 2) ** 2 + ((xx - H / 2 + H / 2) % H - H / 2) ** 2
        bump2 = 0.1 * np.exp(-d2 / (2 * 2.0 ** 2))                 # v1 INJ_SIGMA = 2 px, same peak
        contrast[f"{H}"] = {"channel_nats_u0.1": float(VW.nats_budget(c).cost(np.eye(c.m)[0] * 0.1)),
                            "v1_pixel_noise_nats_same_field": v1_pixel_charge(one, c),
                            "v1_pixel_noise_nats_bump_std2px": v1_pixel_charge(bump2, c),
                            "bump_peak": float(B[0].max()), "bump_mean_removed": float(-B[0].min())}
    out = {"config": {"H": cfg.H, "G": cfg.G, "m": m, "sigma_a": sa, "stir_w": cfg.stir_w, "tick_time": cfg.tick_time},
           "noise_law": law, "kl_check": kl, "program_charge_nats": charge, "per_tick_charges": [budget.cost(u) for u in U],
           "card_guarantee": vw.nats.card_guarantee(charge), "grid_contrast": contrast,
           "example_costs_nats": {f"u={u:g} on one coefficient": float(budget.cost(np.eye(m)[0] * u))
                                  for u in (0.005, 0.01, 0.02, 0.05, 0.1, 0.2)}}
    json.dump(out, open(os.path.join(_paths.RESULTS, "channel.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
