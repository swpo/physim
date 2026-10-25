# Evidence pack: membrane-evo (seed 59)

- world: `../../world_twin.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/membrane_kinds (arm E of committee r2); identical-event design from fisim-beyond-laplacian xcell-evo2-S; mutation: kinds differ only in link yield b2; sealed catalyst channel (min face gate, fast outside decay); whole-cell flips + neutral tag + random disk deaths from a state-independent RNG
- run: 161 frames x 250 steps x dt 1.0 = time 40000; grid [128, 128]; wall 93s; status ok
- command: `python -m labkit.run collective/contrib/c17-mevo-wip/world_twin.py --out collective/contrib/c17-mevo-wip/twin/seed59 --seeds 59 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7296], min area 6 px

## Measurements
- components: final 14, mean 12.1, max 20; occupancy final 0.24
- tracks: 99; persistent (alive >= 50% of run): 4; longest 105 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 17.04 (1 = constant size)
- enclosures: components with a hole mean 10.80, final 10; holes at thresholds 0.2/0.35/0.5 final [7, 10, 13]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 14, 14], H1 [14, 13, 8]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.00247/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 5000, default): splits 37, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 3, merges 4, merge/split ratio 0.108, nucleations 0
- channel total drift (end/start - 1): [-0.7386, None, 0.0251, -0.2211]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 43 at frame 98: holes 1, rim-vs-core 0.37, rim-vs-outside 0.65, heterogeneity 0.20; core [0.795, 0.0, 0.656, 0.594] rim [0.444, 0.0, 0.528, 0.623]
  - track 27 at frame 83: holes 0, rim-vs-core 1.05, rim-vs-outside 0.70, heterogeneity 0.25; core [0.942, 0.0, 0.9, 0.522] rim [0.0, 0.0, 0.529, 0.807]
  - track 33 at frame 87: holes 1, rim-vs-core 0.41, rim-vs-outside 0.72, heterogeneity 0.22; core [0.877, 0.0, 0.736, 0.521] rim [0.497, 0.0, 0.594, 0.606]
  - track 61 at frame 118: holes 1, rim-vs-core 0.48, rim-vs-outside 0.68, heterogeneity 0.23; core [0.0, 0.982, 0.69, 0.565] rim [0.0, 0.524, 0.54, 0.614]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 83 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial K1: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.06, rim/outside 10.6 (aggregate of 83 individuals; 13/83 membrane-like individually; rim level 0.546)
  - radial K2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.964, rim/outside 4.04 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.0665)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.34, rim/outside 6.62 (aggregate of 83 individuals; 54/83 membrane-like individually; rim level 0.514)
  - radial membrane (wall): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 4.03, rim/outside 4.79 (aggregate of 83 individuals; 72/83 membrane-like individually; rim level 0.514)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #43 (t=24500, R_eq 10, ring): ['L link', 'membrane (wall)']; #27 (t=20750, R_eq 5.29): ['membrane (wall)']; #33 (t=21750, R_eq 8, ring): ['L link', 'membrane (wall)']; #61 (t=29500, R_eq 9.57, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 64 of 83 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
