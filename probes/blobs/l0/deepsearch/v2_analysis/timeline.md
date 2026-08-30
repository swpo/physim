# v2 campaign timeline (reconstructed from result-row timestamps)

| era | dir / file | islands | window (2026) | union checkpoint |
|-----|------------|---------|---------------|------------------|
| era0_local_v1 | results.json (ds*, g0_jit*) | local | <= 08-26 | archive.json (metrics_v1 epoch) |
| era0_local_v2 | results_v2.json (ds2g*, v2g*) | local | ~08-25/26 | archive_v2.json (34 cells) |
| era1_cpu_pods | final_cpu_harvest/results_evo2-{0..5} | pods 0-5 | 08-26 10:25 -> 08-28 10:27 | union4_final_cpu = 182 cells |
| era2_singlemode_gpu | gpu_singlemode_harvest/results_isl{6..11} | isl 6-11 | 08-28 10:52 -> 08-28 13:22 | union5_prebatch = 190 cells |
| era3_b1_pilot | gpu_batched_isl1/results_isl1 | isl 1 (gens 1-3) | 08-29 02:55 -> 08-29 06:32 | gpu_b_union1 = 362 cells |
| era4_final_gpu | final_gpu_harvest/results_isl{1..6} | isl 1-6 batched | 08-29 18:27 -> 08-30 16:53 | UNION_FINAL_v2 = 423 cells |

Candidate names are pod-scoped `p{isl}g{gen}_{k}` and are REUSED across eras
(e.g. `p1g2_070` exists in era1, era3 and era4 with different genomes).
Lineage resolution below is timestamp- and pool-aware:
a parent ref in an era4 row first resolves against earlier era4 rows,
then against the gpu_b_union1 breeding-pool holders, then chronologically
backwards (b1 pilot -> singlemode -> cpu pods -> local v2 -> local v1).
