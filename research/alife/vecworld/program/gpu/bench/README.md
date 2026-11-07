# GPU benchmark vw1-bench-001 (7 Nov 2026)

One A100-SXM4-80GB (datacrunch, $2.35/h, billed $0.19), JAX 0.12.0.1 with CUDA 12, float64 (jax_enable_x64).
Script: `../../../vw1/port/bench_gpu.py`; raw results: `vw1-bench-001_results.json` (copied from
`origin/gpu-jobs:jobs/vw1-bench-001/out/`).

| gliders world, vw.World with vmap | B = 1 | 8 | 64 | 256 |
|---|---|---|---|---|
| 'both' (block view + JAX tracker), member-ticks/s | 229 | 1,015 | 1,486 | 1,599 |
| 'coarse' (block view only), member-ticks/s | 331 | 1,175 | 1,607 | 1,707 |

- One tick is 20 Flow-Lenia substeps on 2 x 128 x 128. CPU reference: 0.13-0.16 s per member-tick per core (about 7
  member-ticks/s), so one A100 at B >= 64 is worth about 220-240 CPU cores. Peak memory at B = 256: 2.9 GB.
- First rollout including compilation: 1-5 s; ensemble init with the 50-tick burn-in: 8-23 s.
- JAX object tracker alone: about 19,900 member-updates/s at B = 256 (13 ms per batch), a few % of a tick.
- Conv autoencoder training step, float32, 2 x 128 x 128 inputs: 107 steps/s at batch 64, 27 at batch 256
  (about 6,800 samples/s either way).
- GPU vs CPU: members initialised and burnt in on each device separately already differ completely after the 50-tick
  burn-in (level 0 max abs difference 2.7), because chaos amplifies rounding differences between the GPU and CPU
  kernels. So runs are not bit-reproducible across platforms. Frozen truths must name the platform that made them. A
  one-tick comparison from one shared state (the numerical agreement proper) was not run; it goes in the next job.
- Provisioning took about 28 minutes (queue to running); the run itself about 4 minutes.

Implication for estimates: the 47k member-tick closure study is about 30 s of A100 time; 1M member-ticks about
10 minutes (about $0.40 at this rate).

## Agreement from one shared state: vw1-agree-001 (7 Nov 2026)

A100 80GB, billed $0.08. Two members built once on the CPU (init and burn-in), copied to the GPU, then advanced
in step on both, with zero input (`agree_gpu.py`; raw results `vw1-agree-001_agreement.json`).

- One Flow-Lenia substep: level-0 max abs difference 4e-15, growing to 1e-13 over 5 substeps; block view 1e-16 to
  8e-16. That is the float64 rounding floor, so the GPU arithmetic agrees with the CPU.
- Full ticks (20 substeps): level-0 max abs difference 5.6e-11, 1.4e-7, 1.7e-4, 0.26 and 1.2 at ticks 1-5 (about
  x2,500 per tick), after which the maximum saturates at 1-2.7. The field-wide RMS difference keeps growing slowly:
  1.0e-2 at tick 5 and 7.8e-2 at tick 20, against a field RMS of 0.18. The divergence is local first and global
  over tens of ticks, consistent with the closure study's divergence curve.
- Object view: at tick 1 it differs by at most 6e-13 (rounding passed through continuously, not a discrete
  flip). Discrete tracker differences (slot assignment or presence) first appear around tick 9 (max abs 2.0) and
  tick 17 (93), once the bodies themselves differ.
- Consequence: GPU and CPU runs are statistically the same world but not bit-reproducible beyond a few ticks, so
  frozen truths and certificates must record the platform that produced them.
