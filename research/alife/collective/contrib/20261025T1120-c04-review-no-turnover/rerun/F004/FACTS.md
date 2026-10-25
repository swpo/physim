# Evidence pack: fch-metabolic-micelles (seed 5)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T1000-c03-metabolic-no-turnover/world_F0.004.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py; mutation: amphiphile no longer fed: made from a fed precursor by a shell-held autocatalyst, and degraded
- run: 151 frames x 800 steps x dt 0.02 = time 2400; grid [128, 128]; wall 1003s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1000-c03-metabolic-no-turnover/world_F0.004.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/rev13/F004 --seeds 5 --frames 150 --spf 800 --no-movie`
- segmentation: matter > 0.15 of robust range [0.0799, 2.8546], min area 6 px

## Measurements
- components: final 25, mean 24.8, max 25; occupancy final 0.09
- tracks: 30; persistent (alive >= 50% of run): 25; longest 151 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 13.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 25, 25], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 320, default): splits 3, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 20
- channel total drift (end/start - 1): [-0.3063, 0.7637, None, -0.7029]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 76: holes 0, rim-vs-core 0.73, rim-vs-outside 0.31, heterogeneity 0.28; core [0.639, 0.568, 0.44, 0.031] rim [0.183, 0.0, 0.474, 0.076]
  - track 3 at frame 76: holes 0, rim-vs-core 0.65, rim-vs-outside 0.32, heterogeneity 0.26; core [0.637, 0.458, 0.45, 0.028] rim [0.183, 0.0, 0.489, 0.065]
  - track 4 at frame 76: holes 0, rim-vs-core 0.41, rim-vs-outside 0.44, heterogeneity 0.28; core [0.633, 0.523, 0.449, 0.035] rim [0.346, 0.23, 0.416, 0.07]
  - track 5 at frame 76: holes 0, rim-vs-core 0.65, rim-vs-outside 0.32, heterogeneity 0.26; core [0.638, 0.456, 0.453, 0.027] rim [0.18, 0.0, 0.483, 0.065]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 150 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.478, rim/outside 26.2 (aggregate of 150 individuals; 0/150 membrane-like individually; rim level 0.464)
  - radial catalyst c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.138, rim/outside 11.5 (aggregate of 150 individuals; 0/150 membrane-like individually; rim level 0.107)
  - radial shell q: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 14.6, rim/outside 8.06 (aggregate of 150 individuals; 150/150 membrane-like individually; rim level 0.93)  MEMBRANE-LIKE
  - radial precursor p: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 9, rim/outside 0.784 (aggregate of 150 individuals; 0/150 membrane-like individually; rim level 0.0932)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): shell q
- membrane-like channels per top track at mid-life: #1 (t=1216, R_eq 4.37): ['shell q']; #3 (t=1216, R_eq 4.37): ['shell q']; #4 (t=1216, R_eq 4.37): ['shell q']; #5 (t=1216, R_eq 4.41): ['shell q']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
