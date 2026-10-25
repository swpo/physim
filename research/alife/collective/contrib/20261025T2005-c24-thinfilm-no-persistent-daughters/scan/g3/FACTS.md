# Evidence pack: thinfilm-active (seed 0)

- world: `../world.py`, family `thin-film`
- parent: None; mutation: new class: active polar thin-film drops (lubrication + wetting + polarization)
- run: 81 frames x 200 steps x dt 0.25 = time 4000; grid [128, 128]; wall 199s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/36294be3-c5a3-5217-ad3a-391925841cf2/scratchpad/tfscan/world.py --out /tmp/claude-0/-home-user-physim/36294be3-c5a3-5217-ad3a-391925841cf2/scratchpad/tfscan/g3 --seeds 0 --frames 80 --no-movie`
- segmentation: matter > 0.12 of robust range [0.041, 3.9117], min area 6 px

## Measurements
- components: final 3, mean 5.2, max 14; occupancy final 0.32
- tracks: 74; persistent (alive >= 50% of run): 0; longest 38 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.20, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 3, 1], H1 [1, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.0298/time; max body lengths 3.4
- replication (lineage window K = 20 frames = time 1000, default): splits 20, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 28, merge/split ratio 1.4, nucleations 0
- channel total drift (end/start - 1): [-0.0, 4.7116, 299.6201, -242.8964]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 61 at frame 57: holes 0, rim-vs-core 0.26, rim-vs-outside 0.22, heterogeneity 0.11; core [0.426, 0.866, 0.504, 0.935] rim [0.199, 0.767, 0.497, 0.868]
  - track 30 at frame 24: holes 0, rim-vs-core 0.27, rim-vs-outside 0.22, heterogeneity 0.12; core [0.454, 0.875, 0.065, 0.333] rim [0.205, 0.792, 0.125, 0.356]
  - track 33 at frame 23: holes 0, rim-vs-core 0.24, rim-vs-outside 0.23, heterogeneity 0.11; core [0.443, 0.898, 0.525, 0.95] rim [0.248, 0.774, 0.532, 0.87]
  - track 28 at frame 22: holes 0, rim-vs-core 0.27, rim-vs-outside 0.21, heterogeneity 0.11; core [0.463, 0.888, 0.643, 0.068] rim [0.213, 0.804, 0.617, 0.122]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 34 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial height above precursor h - ha: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.647, rim/outside 4.31 (aggregate of 34 individuals; 1/34 membrane-like individually; rim level 0.354)
  - radial |p| polar order: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.934, rim/outside 2 (aggregate of 34 individuals; 0/34 membrane-like individually; rim level 0.809)
  - radial p_x: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.996, rim/outside 1.04 (aggregate of 34 individuals; 0/34 membrane-like individually; rim level 0.508)
  - radial p_y: peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 1.02, rim/outside 1.03 (aggregate of 34 individuals; 0/34 membrane-like individually; rim level 0.482)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #61 (t=2850, R_eq 7.8): none; #30 (t=1200, R_eq 8.41): none; #33 (t=1150, R_eq 7.78): none; #28 (t=1100, R_eq 8.41): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 34 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 3 of 34 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
