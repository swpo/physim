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
