# Evidence pack: neural-field-dep-fork (seed 1)

- world: `../../world_fork.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 9s; status ok
- command: `python -m labkit.run /tmp/c20nfe/world_fork.py --out /tmp/c20nfe/cut_half --seeds 0 1 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 12, mean 30.4, max 70; occupancy final 0.05
- tracks: 619; persistent (alive >= 50% of run): 0; longest 83 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 12], H1 [0, 0, 0]
- motion: 86 long-lived tracks moved >= 1 body length; max speed 0.569/time; max body lengths 37.8
- replication (lineage window K = 20 frames = time 100, default): splits 242, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 3, merges 60, merge/split ratio 0.248, nucleations 6
- channel total drift (end/start - 1): [1.0, None, -0.7661, -0.2712]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 568 at frame 160: holes 0, rim-vs-core 0.28, rim-vs-outside 0.84, heterogeneity 0.16; core [0.893, 0.576, 1.0, 0.349] rim [0.662, 0.487, 0.871, 0.384]
  - track 365 at frame 87: holes 0, rim-vs-core 0.25, rim-vs-outside 0.90, heterogeneity 0.15; core [0.911, 0.454, 1.0, 0.368] rim [0.682, 0.396, 0.93, 0.42]
  - track 554 at frame 145: holes 0, rim-vs-core 0.25, rim-vs-outside 0.87, heterogeneity 0.15; core [0.93, 0.615, 1.0, 0.469] rim [0.707, 0.516, 0.934, 0.498]
  - track 603 at frame 176: holes 0, rim-vs-core 0.29, rim-vs-outside 0.87, heterogeneity 0.16; core [0.94, 0.625, 1.0, 0.505] rim [0.681, 0.53, 0.927, 0.558]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 155 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.778, rim/outside 2.92 (aggregate of 155 individuals; 0/155 membrane-like individually; rim level 0.701)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.88, rim/outside 1.91 (aggregate of 155 individuals; 3/155 membrane-like individually; rim level 0.541)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.821, rim/outside 26.4 (aggregate of 155 individuals; 0/155 membrane-like individually; rim level 0.791)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.2, rim/outside 0.915 (aggregate of 155 individuals; 1/155 membrane-like individually; rim level 0.534)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #568 (t=800, R_eq 2.93): ['adaptation a']; #365 (t=435, R_eq 2.93): none; #554 (t=725, R_eq 3.57): none; #603 (t=880, R_eq 3.19): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 155 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
