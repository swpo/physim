# probes/blobs/gpu — JAX accelerator port (blobgpu)

Post: docs/blobs/accelerating-blobs.html. Gates: GATES.md (locked 2026-02-25).
Everything below was validated on an A100 40GB pod (jax 0.4.38 + cuda12) and
runs identically (slower) on CPU JAX for development.

## Layout
- blobgpu/core.py     jitted stepper: reaction -> +dt*R -> noise -> k-space diffusion
- blobgpu/packing.py  genomes -> padded (B, nf_max, N, N) tensors; padding inert by construction
- blobgpu/soup.py     assay drivers: init_soup_gpu[_batch], advance_gpu[_batch],
                      snapshot_rec_gpu, run_soup_gpu (drop-in soup_sim_v2 contract;
                      reuses V2's IC builder + record functions verbatim)
- blobgpu/anchors.py  bond-anchor pair worlds (A4s/A5 + the A5-dt trap)
- tests/              gates (gate_f64, gate_anchor, gate_parity) + exactness tests
- bench/              step benchmarks, headline battery, roofline model, figures
- data/               frozen gt_worlds.json (== live builders, checked), stamps
- results/            gpu_bench.json (append-only), gate results, parity runs, pod logs

## Env
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python "jax==0.4.38" numpy scipy        # CPU
uv pip install --python .venv/bin/python "jax[cuda12]==0.4.38" numpy scipy # pod

## The numbers (A100 40GB, $1.99/h)
- batched 256^2: 5.0-5.7 us/field-step (CPU 1-core: 440) — 78x/field-step
- pop-96 x T=2500 full assay: 858 s -> 403 worlds/h — 57x per CPU core, $0.005/world
- 512^2 T=10k: 264 s (35x); 1024^2 T=10k: 1171 s (37x)
- bandwidth-bound: AI 2.4-3.3 flop/B, ~25-30% of nominal peak BW (~35-40% as-executed)

## Rules
- Gates run BEFORE benchmarks on any kernel change (gate_f64 + gate_anchor minimum).
- metrics_v1 / soup_sim_v2 are LOCKED (hash-checked) — never edit to make parity pass.
- Do not wire run_soup_gpu into the live v2 campaign; it is the future-swap hook.
