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

## Slow-motion segments (2026-08-31, one A100-40GB pod, ~11 min GPU wall, pod terminated after)

`jobs_slomo.json` re-simulates 3 champions with dense in-window snapshots:
every 5tu (REC grid, 101 frames) over one 500tu window each, riding ONE
tensor to the latest window end (t_start feature in film_job.py; advance to
window start records cheap activator-only pulls, no full snaps):

* p6g8_033 t=10,000-10,500 (mature rotor core; count pinned at 31)
* p3g9_022 t=19,500-20,000 (cap-crossing boom; count 148-162, ends 151 = assay)
* p4g3_033 t= 5,000- 5,500 (rotor storm peak growth; count 136->165)

Render: render_film.py --fps 8 --crf 27 --zoom-pop (window-local population
panel) -> v2_<cand>_slomo.mp4, 12.6s each, 0.17/0.59/0.47 MB.
40tu/s of sim time vs the originals' ~900tu/s: ~12x finer time resolution.
Decorrelation check (species-1 full field): consecutive 25tu frames corr
r=0.98 (p6g8) / 0.23 (p3g9) / 0.94 (p4g3); at 5tu those become
1.00 / 0.86 / 0.99 — the fast movers were strobing on the 25tu grid.
