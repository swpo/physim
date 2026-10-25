# Evidence pack: cips-inhib (seed 5)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: adds an inhibitor I made by catalysis that slows catalysis (cat / (1 + I/KI)) and decays slowly: core inhibition of large droplets as a size-control route that keeps the enzyme conserved
- run: 601 frames x 100 steps x dt 0.1 = time 6000; grid [128, 128]; wall 120s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/world.py --out /tmp/claude-0/c28ci/inh --seeds 5 6 --frames 600 --size 128 128 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0015, 0.9891], min area 6 px

## Measurements
- components: final 33, mean 32.5, max 43; occupancy final 0.13
- tracks: 55; persistent (alive >= 50% of run): 35; longest 535 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 33, 33], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 11, merge/split ratio n/a, nucleations 44
- channel total drift (end/start - 1): [0.0, -0.5759, 0.3965, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 333: holes 0, rim-vs-core 0.36, rim-vs-outside 0.40, heterogeneity 0.10; core [0.958, 0.902, 0.178, 0.871] rim [0.735, 0.71, 0.326, 0.732]
  - track 1 at frame 338: holes 0, rim-vs-core 0.38, rim-vs-outside 0.41, heterogeneity 0.10; core [0.951, 0.886, 0.217, 0.819] rim [0.699, 0.688, 0.364, 0.683]
  - track 3 at frame 338: holes 0, rim-vs-core 0.21, rim-vs-outside 0.54, heterogeneity 0.10; core [0.953, 0.894, 0.198, 0.836] rim [0.817, 0.784, 0.277, 0.764]
  - track 4 at frame 338: holes 0, rim-vs-core 0.31, rim-vs-outside 0.37, heterogeneity 0.08; core [0.937, 0.837, 0.258, 0.795] rim [0.722, 0.678, 0.368, 0.695]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 223 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.923, rim/outside 29.6 (aggregate of 223 individuals; 0/223 membrane-like individually; rim level 0.907)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.871, rim/outside 4.38 (aggregate of 223 individuals; 0/223 membrane-like individually; rim level 0.817)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.42, rim/outside 0.713 (aggregate of 223 individuals; 0/223 membrane-like individually; rim level 0.517)
  - radial I: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.902, rim/outside 2.21 (aggregate of 223 individuals; 0/223 membrane-like individually; rim level 0.815)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=3330, R_eq 4.51): none; #1 (t=3380, R_eq 4.33): none; #3 (t=3380, R_eq 4.41): none; #4 (t=3380, R_eq 3.7): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
