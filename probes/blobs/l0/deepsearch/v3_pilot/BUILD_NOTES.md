# v3 pilot bundle build (controller-inline after 4 child setup-deaths)
Base: make_bundle(gpu_batch) 0.3.4 + overlay:
- lib/: metrics_v3, assay_v3, operators_v3, worlds_v3 (+ shims metrics_v1/v2,
  soup_sim_v2->sim_cpu, soup_sim->sim_v1, worlds, assay_v2) + v3_postpass
- pod_worker_batch: npz-rescore hook (C9 partial: t9/e9/r9; s9 deferred),
  spatial-class cell-axis append, __ic__ lane routing -> assay_v3 CPU path
- pod_gen: merge_spatial_ic branch (elite x elite/immigrant, ic npz per child)
- seeds: v2 UNION_FINAL top-100 + atlas g0 jobs (cargo_cell, m5_trains, m2_dimer)
SMOKE (local, cpu-jax): smoke_0 75.2 C9=0.42 structured; smoke_1 60.5 C9=0.37
structured; smoke_sic 69.6 C9=0.49 economy — all ok, cells carry spatial axis.

## Workspace policy (2026-09-02, after /tmp GC ate the build venv mid-run)
- NEVER build venvs or long-lived workspaces in /tmp (macOS GC prunes aggressively).
- Local science venv: ~/.venvs/bk3 (py3.9, blobkit -e install, numpy<2, jax 0.4.30 cpu).
- v3 pilot workspace: ~/v3work/{v3bundle,v3smoke} (was /tmp/v3bundle).
- Prefer uv-managed project venvs (physim/.venv) where the project defines deps.

## Pilot-2 perf fix (2026-09-02 late, RED protocol)
Round-1 launch was 10-20x too slow ($150 cap unreachable): (a) __ic__ lanes ran
serially on CPU assay_v3 BEFORE the GPU batch (isl2: 8 lanes = 8.3h; isl1 never
reached its GPU sweep in 9.5h; walls 20min-3h/lane); (b) C9 npz-rescore ran
serially on the worker main thread (~60-90s/lane on pod cores; GPU+battery pool
idle). Fix (blobkit 0.3.5 + pod_worker_batch.py here):
- engine: run_assay_batch job dicts accept "ic" ((na+nc,N,N)); _norm_jobs ->
  init_soup_gpu_batch(ics=...) replaces S["F"] post-init pre-pack (same
  documented data-level hook as assay_v3 ic_override). Shape mismatch =
  ValueError (lane-isolatable), not assert.
- worker: ic lanes ride the GPU tensor when blobkit>=0.3.5 (version-gated;
  CPU-thread fallback kept). C9 for ic lanes now comes from the same partial-
  mode rescore as screens (s9 absent) => ONE scoring currency for
  screens/confirms/ic lanes; interest blend formula unchanged.
- worker: rescore moved to a spawn ProcessPool (rescore_procs, default
  min(6,ncpu)); rows append at drain (idempotency preserved); npz keep/delete
  decided post-rescore as before. Local check: pooled rescore reproduces the
  inline C9 exactly (p2g1_010: C9=0.5204, interest 65.275).
Expected pace after fix: ~1.5h/gen (GPU sweeps ~20min/32 lanes; rescore hidden).
