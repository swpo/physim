# Evidence pack: nrch (seed 4)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T1054-c08-nrch-chemostat-crystal/world.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 241 frames x 500 steps x dt 0.05 = time 6000; grid [192, 192]; wall 734s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1054-c08-nrch-chemostat-crystal/world.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/rev17/k5 --seeds 4 --frames 240 --spf 500 --lineage-k 40 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.9191, 0.9128], min area 6 px

## Measurements
- components: final 16, mean 18.6, max 38; occupancy final 0.21
- tracks: 214; persistent (alive >= 50% of run): 16; longest 219 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.40 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [0, 0, 0]
- motion: 25 long-lived tracks moved >= 1 body length; max speed 0.274/time; max body lengths 59.0
- replication (lineage window K = 40 frames = time 1000, --lineage-k): splits 35, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 1, merges 17, merge/split ratio 0.486, nucleations 129
- channel total drift (end/start - 1): [-0.076, 25.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 114 at frame 131: holes 0, rim-vs-core 0.23, rim-vs-outside 0.44, heterogeneity 0.20; core [0.938, 0.384] rim [0.712, 0.396]
  - track 132 at frame 135: holes 0, rim-vs-core 0.22, rim-vs-outside 0.44, heterogeneity 0.19; core [0.925, 0.341] rim [0.705, 0.387]
  - track 166 at frame 141: holes 0, rim-vs-core 0.25, rim-vs-outside 0.43, heterogeneity 0.20; core [0.945, 0.372] rim [0.699, 0.378]
  - track 182 at frame 149: holes 0, rim-vs-core 0.22, rim-vs-outside 0.45, heterogeneity 0.20; core [0.94, 0.38] rim [0.721, 0.386]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 110 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.79, rim/outside 6.44 (aggregate of 110 individuals; 0/110 membrane-like individually; rim level 0.752)
  - radial psi: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.32, rim/outside 0.945 (aggregate of 110 individuals; 0/110 membrane-like individually; rim level 0.526)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #114 (t=3275, R_eq 14.76): none; #132 (t=3375, R_eq 14.45): none; #166 (t=3525, R_eq 14.07): none; #182 (t=3725, R_eq 14.53): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
