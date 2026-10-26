# Evidence pack: phoretic-colloids (seed 4)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0529-c33-phoretic-swimdivide-claim/world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 1601 frames x 1 steps x dt 0.5 = time 800; grid [128, 128]; wall 383s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0529-c33-phoretic-swimdivide-claim/world.py --out /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/rev8/lk_s4 --seeds 4 --frames 1600 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7906], min area 6 px

## Measurements
- components: final 10, mean 11.0, max 20; occupancy final 0.05
- tracks: 433; persistent (alive >= 50% of run): 0; longest 645 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 14, 7], H1 [0, 0, 0]
- motion: 77 long-lived tracks moved >= 1 body length; max speed 0.559/time; max body lengths 11.2
- replication (lineage window K = 20 frames = time 10, default): splits 38, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 9, merges 56, merge/split ratio 1.47, nucleations 301
- channel total drift (end/start - 1): [0.52, 0.34, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 189 at frame 887: holes 0, rim-vs-core 0.20, rim-vs-outside 0.22, heterogeneity 0.15; core [0.703, 0.26, 0.484] rim [0.526, 0.216, 0.407]
  - track 200 at frame 861: holes 0, rim-vs-core 0.13, rim-vs-outside 0.39, heterogeneity 0.21; core [0.668, 0.425, 0.588] rim [0.565, 0.372, 0.533]
  - track 206 at frame 887: holes 0, rim-vs-core 0.18, rim-vs-outside 0.18, heterogeneity 0.25; core [0.543, 0.481, 0.473] rim [0.396, 0.415, 0.401]
  - track 428 at frame 1587: holes 0, rim-vs-core 0.27, rim-vs-outside 0.25, heterogeneity 0.20; core [0.772, 0.237, 0.595] rim [0.526, 0.233, 0.49]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 62 components >= 12 px at frames [269, 538, 807, 1062, 1331, 1600]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.858, rim/outside 15.2 (aggregate of 62 individuals; 5/62 membrane-like individually; rim level 0.616)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.783, rim/outside 15.4 (aggregate of 62 individuals; 16/62 membrane-like individually; rim level 0.347)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.823, rim/outside 3.11 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.596)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #189 (t=443.5, R_eq 3.57): none; #200 (t=430.5, R_eq 4.65): none; #206 (t=443.5, R_eq 3.57): none; #428 (t=793.5, R_eq 4.11): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
