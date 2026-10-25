# Evidence pack: fch-pchemoton-starve-clip (seed 24)

- world: `../../../20261025T1817-c17-chemoton-honest-decay/world_starve_clip.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 672s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1817-c17-chemoton-honest-decay/world_starve_clip.py --out collective/contrib/20261025T2019-c24-review-honest-decay/starve_clip/seed24 --seeds 24 --frames 200 --no-movie`
- segmentation: matter > 0.32 of robust range [-0.0263, 1.9534], min area 6 px

## Measurements
- components: final 3, mean 3.6, max 5; occupancy final 0.01
- tracks: 12; persistent (alive >= 50% of run): 1; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 15.73 (1 = constant size)
- enclosures: components with a hole mean 1.08, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 3, 3], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.3
- replication (lineage window K = 20 frames = time 60, default): splits 3, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 3, merge/split ratio 1, nucleations 3
- channel total drift (end/start - 1): [-1.1059, -0.2955, -0.9872]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.30, rim-vs-outside 0.65, heterogeneity 0.16; core [0.949, 0.0, 0.862] rim [0.719, 0.012, 0.677]
  - track 1 at frame 44: holes 8, rim-vs-core 0.07, rim-vs-outside 0.47, heterogeneity 0.18; core [0.62, 0.802, 0.0] rim [0.667, 0.795, 0.052]
  - track 10 at frame 166: holes 1, rim-vs-core 0.20, rim-vs-outside 0.27, heterogeneity 0.04; core [0.818, 0.399, 0.0] rim [0.614, 0.399, 0.0]
  - track 6 at frame 101: holes 0, rim-vs-core 0.16, rim-vs-outside 0.42, heterogeneity 0.07; core [0.857, 0.832, 0.003] rim [0.696, 0.836, 0.007]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 21 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.987, rim/outside 4.63 (aggregate of 21 individuals; 4/21 membrane-like individually; rim level 0.65)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.16, rim/outside 0.864 (aggregate of 21 individuals; 0/21 membrane-like individually; rim level 0.379)
  - radial catalyst K: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.975, rim/outside 2.87 (aggregate of 21 individuals; 5/21 membrane-like individually; rim level 0.205)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=303, R_eq 11.38): none; #1 (t=132, R_eq 28.26): none; #10 (t=498, R_eq 9.95, ring): ['amphiphile u+1']; #6 (t=303, R_eq 15.03, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 8 of 21 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
