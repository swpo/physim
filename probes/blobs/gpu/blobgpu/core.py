"""blobgpu/core.py — JAX stepper for the L0 genome simulator (batched, padded).

Numerics contract (mirrors probes/blobs/l0/complexity/soup_sim_v2.advance,
the LOCKED CPU kernel). One step, in this order:
  1. explicit reaction with OLD u:  R_u = lam*u - u^3 + k1 - K@x (- bilin)
                                    R_x = (drive(z) - x) / tau,  z = u - u0
  2. F += dt * R
  3. optional activator noise (amplitude noise*sqrt(dt))
  4. exact diffusion in k-space:    F <- irfft2( rfft2(F) * exp(-D k^2 dt) )

Batch layout: F is ONE tensor (B, nf_max, N, N); worlds are padded to a common
(na_max, nc_max). Padded slots are inert BY PARAMETER CONSTRUCTION (packing.py;
verified exactly in tests/test_padding.py). There is NO cross-world coupling:
reactions are per-world einsums over the field axis, FFTs are per-field 2D
transforms. A NaN blowup in one world cannot contaminate another.

RNG: per-world jax threefry keys, folded with the ABSOLUTE step index, so
(a) chunked continuation reproduces a single long run exactly, and
(b) a world's noise stream does not depend on what else is in the batch.
This is a different stream than the CPU numpy PCG64 stream — same law
(N(0,1)*noise*sqrt(dt) on activators), different realization. Trajectory
parity is therefore gated at noise=0 (f64 rel-L2) and, with noise, at the
descriptor level (locked metrics_v1 battery). See GATES.md.

f32 default; f64 via JAX_ENABLE_X64=1 (or core.enable_x64() first thing).
einsums pinned to Precision.HIGHEST: on A100 the default would let XLA use
TF32 tensor cores for f32 contractions — a silent 1e-3-level numerics change.
"""
import numpy as np
import jax
import jax.numpy as jnp
from functools import partial

HI = jax.lax.Precision.HIGHEST


def enable_x64():
    jax.config.update("jax_enable_x64", True)


# ----------------------------------------------------------------- k-space
def k2_grid(N, dx):
    kf = 2 * np.pi * np.fft.fftfreq(N, d=dx)
    kr = 2 * np.pi * np.fft.rfftfreq(N, d=dx)
    return kf[:, None] ** 2 + kr[None, :] ** 2          # (N, N//2+1), f64


def diffusion_E(D, N, dx, dt, dtype=np.float32):
    """exp(-D k^2 dt): computed in f64, cast to dtype (CPU convention).
    D: (B, nf) -> E: (B, nf, N, N//2+1) real."""
    k2 = k2_grid(N, dx)
    E = np.exp(-np.asarray(D, np.float64)[..., None, None] * k2[None, None] * dt)
    return jnp.asarray(E.astype(dtype))


def batch_keys(seeds):
    """Per-world PRNG keys from integer seeds -> (B, 2) uint32."""
    return jnp.stack([jax.random.PRNGKey(int(s)) for s in seeds])


# ----------------------------------------------------------------- stepper
def make_stepper(struct, N, dx, dt, noise=0.0, precompute_E=True, unfused=False):
    """Build the jitted chunk stepper for a packed batch.

    struct: static ints/tuples from packing.pack_genomes().
    Returns step_chunk(F, params, keys, step0, nsteps) -> F
      F      (B, nf_max, N, N) device array            [donated]
      params dict of device arrays (packing) + "E" (precompute_E)
             or "D"(B,nf) + "k2"(N,N//2+1)             (on-the-fly)
      keys   (B, 2) uint32 per-world PRNG keys (batch_keys)
      step0  int32 absolute step index of F            [traced]
      nsteps int                                       [static]
    """
    na = struct["na_max"]
    tanh_slots = tuple(struct["tanh_slots"])
    nb = struct["nb_max"] if struct["has_bilin"] else 0
    use_noise = noise > 0.0
    nsig64 = float(noise) * float(np.sqrt(dt))

    def reaction(F, p):
        U = F[:, :na]
        X = F[:, na:]
        Z = U - p["u0"][:, :, None, None]
        RU = (p["lam"][:, :, None, None] * U - U ** 3
              + p["k1"][:, :, None, None]
              - jnp.einsum("bic,bcyx->biyx", p["K"], X, precision=HI))
        for k in range(nb):
            idx_c = p["bi_c"][:, k][:, None, None, None]
            idx_c2 = p["bi_c2"][:, k][:, None, None, None]
            xc = jnp.take_along_axis(X, idx_c, axis=1)[:, 0]
            xc2 = jnp.take_along_axis(X, idx_c2, axis=1)[:, 0]
            oh = jax.nn.one_hot(p["bi_i"][:, k], na, dtype=F.dtype)  # (B, na)
            RU = RU - (p["bi_coef"][:, k][:, None] * oh)[:, :, None, None] \
                      * (xc * xc2)[:, None]
        drive = jnp.einsum("bca,bayx->bcyx", p["Wid"], Z, precision=HI)
        for c in tanh_slots:
            tz = jnp.tanh(jnp.clip(Z - p["thr"][:, c][:, None, None, None],
                                   0.0, None)
                          / p["sc"][:, c][:, None, None, None])
            drive = drive.at[:, c].add(
                jnp.einsum("ba,bayx->byx", p["Wtanh"][:, c], tz, precision=HI))
        RX = (drive - X) * p["inv_tau"][:, :, None, None]
        return jnp.concatenate([RU, RX], axis=1)

    def diffuse(F, p):
        Fh = jnp.fft.rfft2(F)
        if precompute_E:
            Fh = Fh * p["E"]
        else:
            E = jnp.exp(-p["D"][:, :, None, None] * p["k2"][None, None] * dt
                        ).astype(F.dtype)
            Fh = Fh * E
        return jnp.fft.irfft2(Fh, s=(N, N))

    def body_factory(params, keys):
        def body(i, F):
            R = reaction(F, params)
            if unfused:                    # bench-only: force R to materialize
                R = jax.lax.optimization_barrier(R)
            F = F + jnp.asarray(dt, F.dtype) * R
            if use_noise:
                # key layout: fold (step, field) into each world key so a
                # world's noise stream is independent of batch shape/padding
                kk = jax.vmap(lambda k: jax.random.fold_in(k, i))(keys)
                def world_noise(k):
                    def field_noise(a):
                        return jax.random.normal(jax.random.fold_in(k, a),
                                                 (N, N), dtype=F.dtype)
                    return jax.vmap(field_noise)(jnp.arange(na))
                xi = jax.vmap(world_noise)(kk)
                F = F.at[:, :na].add(jnp.asarray(nsig64, F.dtype)
                                     * params["act_mask"][:, :, None, None] * xi)
            return diffuse(F, params)
        return body

    @partial(jax.jit, static_argnums=(4,), donate_argnums=(0,))
    def step_chunk(F, params, keys, step0, nsteps):
        body = body_factory(params, keys)
        return jax.lax.fori_loop(step0, step0 + nsteps, body, F)

    return step_chunk


def make_single_step(struct, N, dx, dt, noise=0.0, donate=True):
    """One jitted step (python-loop mode; bench baseline for launch overhead).
    Same math as make_stepper with nsteps=1, but without the fori_loop."""
    chunk = make_stepper(struct, N, dx, dt, noise=noise)

    def step(F, params, keys, step0):
        return chunk(F, params, keys, step0, 1)

    return step
