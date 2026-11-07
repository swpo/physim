# port: VW-0 A_gliders in the VW-1 types

Run with the shared venv, from this folder, at most 2 processes (`taskset -c 0,1` or `2,3`):
`../.venv/bin/python -B <script>`. `-B` and `_paths.py` keep VW-0 folders read-only (no bytecode).

| file | what |
|---|---|
| `flowlenia_jax.py` | Flow-Lenia Level (float64, periodic, mass-conserving reintegration, VW-0 zero-sum kick, flow noise), JAX `init_patches` |
| `phi.py` | `phi_coarse` (JAX), `phi_objects_jax` (the tracker as pure JAX, `vw.objects`, memory 16597), `phi_objects` (the VW-0 tracker through a host callback, memory 16593), `pair` (fan-out), `population` (level 2) |
| `aworld.py` | A_gliders WorldSpecs (`vw.stride(., 20)`, VW-0 ports; `build(tracker='host'|'jax')`), `MapWorld` (lax.map batching), `chunked_rollout` |
| `check_level0.py` | item 1: one-step and free-running agreement with `level0/flowlenia.py`, mass, timing |
| `check_phi.py` | item 2: Phi_coarse vs VW-0, tracker inside the World vs numpy replay, opacity |
| `check_batching.py` | vmap vs lax.map vs unbatched, pathwise, on the chaotic level |
| `check_world.py` | item 3: card, reset/step/run, violations, exam |
| `repro_closure.py`, `closure_vw0_subsample.py` | item 3: VW-0 closure ceilings through the VW-1 world; matched VW-0 control |
| `compose_demo.py stack/product/stride/couple` | item 4 on the real world |
| `refine_toy.py` | item 4: exact, mean-leaky and variance-leaky refinement of `vw.toys.mass_ring` |
| `fisher_demo.py`, `fisher_lr.py` | item 5: autodiff Fisher bounds, FD check, library check, likelihood-ratio estimator |
| `results/` | JSON outputs, logs, `level0_divergence.png`, `closure_data.npz` (float32) |
| `results/jax_tracker/` | verification of the JAX tracker: `lockstep.py`, `replay.py`, `speed.py`, `summary.json` |

## Phi_objects: two implementations

`aworld.build(tracker=...)` chooses the implementation of the object tracker. Both follow the same
declared rules (`vw/objects.py` docstring) and read out the same 144 numbers.

- `'jax'` (**the default**): `vw.objects.BlobTracker` with the same settings (blur 1 px, threshold 0.1,
  K = 12, m_min = 20). The whole world is then one compiled JAX program, `jit`/`vmap`-able, with no
  host callback; `differentiable=False` (the matching is discrete), not opaque. Memory = the host
  layout + 4 overflow entries. Fixed caps: at most 64 raw components before the mass filter and 32
  kept after it; anything beyond a cap is left untracked and the tick is counted in the overflow
  entries (A_gliders peaks at about 13). The host tracker has no caps.
- `'host'` (the reference): `integrate/lenia_world.Tracker` (numpy/scipy) called through
  `jax.pure_callback`; opaque.

Checks (`results/jax_tracker/`, and an independent adversarial check of 133 synthetic sequences:
edges and corners of the torus, rings that pinch apart, equal overlaps and masses, fallback ties,
simultaneous fusion and fission, slot exhaustion). Lockstep, where both trackers read the same
level 0 in one world: every slot map, presence, age, event, uid and global is equal, and so is every
agent observation. Continuous features differ by at most 4e-14, from numpy's AVX-512 `arctan2`;
with that disabled they are bit-identical. The fallback distance uses `jnp.hypot`, which can differ
from `math.hypot` by 1 ulp, so a fallback choice could differ only when two candidate distances, or a
distance and the rg + 4 cutoff, are within 1 ulp; this never occurred. Replaying the hero agent
episode with `'jax'` gives bit-identical observations (the designer-side level 1 differs in the last
bits, at most 5.7e-14).

Reproducing saved data: level-0 rounding depends on the compiled program, and chaos amplifies
last-bit differences over the 50 burn-in ticks. In the init + burn-in program of a multi-member
designer ensemble (`d.ensemble(B >= 2)`), the host-tracker program builds the Flow-Lenia kernels
inside the member loop; the JAX-tracker program hoists them to the program entry, as every program
does for B = 1. So:

- Agent episodes (`reset`/`step`, B = 1) are the same under both trackers, as are rollouts from
  given states.
- Under `'jax'`, a member's level 0 is the same for B = 1, 2 and 3. Under `'host'`, B = 1 differs from
  B >= 2.
- The runs in `../fresh/` were made with `'host'`. Their saved B >= 2 ensembles (for example
  `fresh/closure/results/sim_A.npz`) are reproduced bit for bit only with `build(tracker='host')`
  (or `aworld.TRACKER = 'host'`); with `'jax'` they are re-drawn at the rounding level and are equally
  valid samples of the same declared world.

`results/jax_tracker/level0_context.json` has the evidence.
