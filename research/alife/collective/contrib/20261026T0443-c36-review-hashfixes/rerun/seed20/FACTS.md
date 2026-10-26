# Evidence pack: hash-chemistry-v2 (seed 20)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0304-c30-hash-fixes/knobs/world.py`, family `hash-chemistry`
- parent: None; mutation: reproduction of Sayama 2019 Hash Chemistry (positive control for O)
- run: 101 frames x 20 steps x dt 1.0 = time 2000; grid [128, 128]; wall 14s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0304-c30-hash-fixes/knobs/world.py --out /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/rev3/lk_s20 --seeds 20 --frames 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 6.0], min area 6 px

## Measurements
- components: final 2, mean 0.6, max 3; occupancy final 0.00
- tracks: 64; persistent (alive >= 50% of run): 0; longest 1 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [75, 20, 2], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 400, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 64
- channel total drift (end/start - 1): [0.107, 245.375, -0.878]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 63 at frame 100: holes 0, rim-vs-core 0.22, rim-vs-outside 0.45, heterogeneity 0.31; core [0.667, 0.611, 0.167] rim [0.756, 0.756, 0.033]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1 components >= 12 px at frames [100]):
  - radial density: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.98, rim/outside 3.92 (aggregate of 1 individuals; 1/1 membrane-like individually; rim level 1)  MEMBRANE-LIKE
  - radial top_type: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.98, rim/outside 4.1 (aggregate of 1 individuals; 1/1 membrane-like individually; rim level 1)  MEMBRANE-LIKE
  - radial other_types: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 26, rim/outside 9.75 (aggregate of 1 individuals; 1/1 membrane-like individually; rim level 0.25)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): density (peak at rho=0.25, outside the peak band), top_type (peak at rho=0.25, outside the peak band), other_types
- membrane-like channels per top track at mid-life: #62 (t=2000, R_eq 1.87): ['other_types']; #63 (t=2000, R_eq 2.59): ['density', 'top_type', 'other_types']; #0 (t=120, R_eq 1.38): none; #1 (t=180, R_eq 1.38): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
