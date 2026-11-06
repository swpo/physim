# port: VW-0 A_gliders in the VW-1 types

Run with the shared venv, from this folder, at most 2 processes (`taskset -c 0,1` or `2,3`):
`../.venv/bin/python -B <script>`. `-B` and `_paths.py` keep VW-0 folders read-only (no bytecode).

| file | what |
|---|---|
| `flowlenia_jax.py` | Flow-Lenia Level (float64, periodic, mass-conserving reintegration, VW-0 zero-sum kick, flow noise), JAX `init_patches` |
| `phi.py` | `phi_coarse` (JAX), `phi_objects` (opaque VW-0 tracker, memory 16593), `pair` (fan-out), `population` (level 2) |
| `aworld.py` | A_gliders WorldSpecs (`vw.stride(., 20)`, VW-0 ports), `MapWorld` (lax.map batching), `chunked_rollout` |
| `check_level0.py` | item 1: one-step and free-running agreement with `level0/flowlenia.py`, mass, timing |
| `check_phi.py` | item 2: Phi_coarse vs VW-0, tracker inside the World vs numpy replay, opacity |
| `check_batching.py` | vmap vs lax.map vs unbatched, pathwise, on the chaotic level |
| `check_world.py` | item 3: card, reset/step/run, violations, exam |
| `repro_closure.py`, `closure_vw0_subsample.py` | item 3: VW-0 closure ceilings through the VW-1 world; matched VW-0 control |
| `compose_demo.py stack/product/stride/couple` | item 4 on the real world |
| `refine_toy.py` | item 4: exact, mean-leaky and variance-leaky refinement of `vw.toys.mass_ring` |
| `fisher_demo.py`, `fisher_lr.py` | item 5: autodiff Fisher bounds, FD check, library check, likelihood-ratio estimator |
| `results/` | JSON outputs, logs, `level0_divergence.png`, `closure_data.npz` (float32) |
