# Evidence pack: fch-protocell (seed 13)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T0726-c03-fch-protocell/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0745-c03-fch-vesicles/world.py; mutation: add a solute made by the bilayer, excluded from it by chi c u (barrier), decaying everywhere
- run: 251 frames x 400 steps x dt 0.02 = time 2000; grid [128, 128]; wall 599s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0726-c03-fch-protocell/world.py --out /tmp/claude-0/c11rev2/rerun_long --seeds 13 --frames 250 --no-movie`
- segmentation: matter > 0.23 of robust range [0.1068, 1.8269], min area 6 px

## Measurements
- components: final 6, mean 6.1, max 7; occupancy final 0.16
- tracks: 12; persistent (alive >= 50% of run): 6; longest 251 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 63.33 (1 = constant size)
- enclosures: components with a hole mean 1.20, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 5]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 6, 6], H1 [6, 6, 5]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 20 frames = time 160, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio n/a, nucleations 6
- channel total drift (end/start - 1): [0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 126: holes 0, rim-vs-core 0.43, rim-vs-outside 0.30, heterogeneity 0.26; core [0.801, 0.141] rim [0.386, 0.015]
  - track 6 at frame 126: holes 0, rim-vs-core 0.36, rim-vs-outside 0.38, heterogeneity 0.26; core [0.795, 0.156] rim [0.469, 0.012]
  - track 8 at frame 126: holes 0, rim-vs-core 0.44, rim-vs-outside 0.30, heterogeneity 0.25; core [0.801, 0.128] rim [0.38, 0.015]
  - track 9 at frame 126: holes 0, rim-vs-core 0.43, rim-vs-outside 0.30, heterogeneity 0.26; core [0.8, 0.151] rim [0.389, 0.013]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 36 components >= 12 px at frames [42, 84, 126, 166, 208, 250]):
  - radial amphiphile u (u + 1.6): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.84, rim/outside 48.1 (aggregate of 36 individuals; 30/36 membrane-like individually; rim level 0.892)  MEMBRANE-LIKE
  - radial solute c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.426, rim/outside 0.829 (aggregate of 36 individuals; 0/36 membrane-like individually; rim level 0.247)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): amphiphile u (u + 1.6)
- membrane-like channels per top track at mid-life: #0 (t=1008, R_eq 9.13): ['amphiphile u (u + 1.6)']; #6 (t=1008, R_eq 9.1): ['amphiphile u (u + 1.6)']; #8 (t=1008, R_eq 9.08): ['amphiphile u (u + 1.6)']; #9 (t=1008, R_eq 9.17): ['amphiphile u (u + 1.6)']

## Warnings
- radial: 6 of 36 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
