# films/ — v2 champion film pipeline (post 10)

Re-simulates the 5 film candidates + 2 B-roll ancestors from their committed
genomes/seeds and renders the post-10 MP4s (docs/blobs/media/v2/).

Pipeline (2026-08-30, one H100 pod, ~20 min GPU wall, pod terminated after):
1. `film_job.py jobs.json outdir/` on a CUDA pod with blobkit 0.3.4
   (verify_locks must be True; wheel built from probes/blobs/blobkit).
   Groups jobs by horizon T; each group rides ONE batched tensor
   (init_soup_gpu_batch/advance_gpu_batch — the campaign stepper, f32,
   L=128, n_soup=12, default noise, assay seeds). Dense snap_t schedule
   (~40-60 full-field frames on the CREC grid) -> per-world npz
   (float16 activator stacks + REC-grid blob-count series).
2. `render_film.py <npz> <mp4> --title ...` locally: per-activator panels
   (magma/viridis/inferno/cividis, fixed per-film percentile scales),
   timestamp overlay, blob-count cursor panel; ffmpeg libx264 -crf 23,
   2.5 fps.

Horizons: champions at their assay T_used (p6g8_033/p4g3_033/p4g2_044
20000, p5g3_040 5000), p3g9_022 at 40000 = 2x its cap exit (CAP_RIDERS
evidence film), B-rolls (smoke_m0, ds3_014) at 2500.

Captured nblobs_end vs assay: p4g2_044 21/21 exact, p4g3_033 247/241,
p5g3_040 93/92, smoke_m0 12 frozen, ds3_014 80 (delayed onset),
p3g9_022 189 vs 151@20k — GREW past the cap, confirming the rising-at-exit
claim on camera.
