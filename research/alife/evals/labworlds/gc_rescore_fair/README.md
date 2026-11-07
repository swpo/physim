# Grand-challenge suites re-scored with the fair estimator (8 Nov 2026)

All 12 suites behind the grand-challenge showcase (vortex main/formation/long2; phase_membrane, cips and rods main
iteration 1, main iteration 2 and formation) re-scored from their saved control forecasts with `estimator="plugin"`
(reproduces every stored score bit for bit) and `estimator="fair"`. An independent check recomputed four control
tables and nine specificity figures and corrected four prose statements (see `results/summary.json`, block `checker`).

- 4-member independent-native references drop 19.5-22.3% per suite; persistence is unchanged (zero spread); mechanism
  controls drop 0-10.5%. No ordering between persistence, mechanism controls, naive controls and the native reference
  changes in aggregate.
- Page tags that change: phase_membrane `probe_wide` (formation, S) from "at the probe" to "whole-world", so
  phase_membrane "Singled out" goes from S I BD to I BD; cips `steer_p` (formation, S) from "specific" to "at the
  probe". Separation flags that change: the cips iteration-2 dt-halved null now separates from the native band; the
  cips formation wrong-probe-geometry control no longer does.
- Old and new values for every page number: `results/page_numbers.json` and `results/summary.json` (`page.cards`).

Scripts use absolute paths in the cloud build container (`/home/user/evalwork/gc_suites`); per-forecast outputs are not
committed.
