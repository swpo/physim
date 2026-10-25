# Evidence pack: nrch (seed 4)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0840-c08-nrch-swimmers/world.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 121 frames x 1000 steps x dt 0.05 = time 6000; grid [192, 192]; wall 720s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0840-c08-nrch-swimmers/world.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/rev6/main_s4 --seeds 4 --frames 120 --spf 1000 --no-movie`
- segmentation: matter > 0.49 of robust range [-1.0472, 1.0728], min area 6 px

## Measurements
- components: final 4, mean 5.1, max 12; occupancy final 0.22
- tracks: 66; persistent (alive >= 50% of run): 2; longest 86 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 14.06 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 4], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.17/time; max body lengths 19.0
- replication (lineage window K = 20 frames = time 1000, default): splits 12, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 13, merge/split ratio 1.08, nucleations 30
- channel total drift (end/start - 1): [0.0, 129.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 32 at frame 78: holes 0, rim-vs-core 0.24, rim-vs-outside 0.43, heterogeneity 0.17; core [0.929, 0.336] rim [0.692, 0.349]
  - track 13 at frame 65: holes 0, rim-vs-core 0.26, rim-vs-outside 0.42, heterogeneity 0.18; core [0.94, 0.34] rim [0.685, 0.319]
  - track 52 at frame 95: holes 0, rim-vs-core 0.21, rim-vs-outside 0.43, heterogeneity 0.17; core [0.901, 0.315] rim [0.697, 0.363]
  - track 35 at frame 65: holes 0, rim-vs-core 0.23, rim-vs-outside 0.50, heterogeneity 0.18; core [0.949, 0.388] rim [0.724, 0.367]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 30 components >= 12 px at frames [40, 61, 80, 100, 120]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.856, rim/outside 6.6 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.829)
  - radial psi: peak at rho=1.45 (in the peak band 0.5-1.5), rim/core 1.19, rim/outside 1 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.544)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #32 (t=3900, R_eq 15.99): none; #13 (t=3250, R_eq 17.4): none; #52 (t=4750, R_eq 14.52): none; #35 (t=3250, R_eq 19.09): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
