# Evidence pack: cgle-gain (seed 3)

- world: `../../../20261026T1610-c43-cgle-gain-bigbox/world.py`, family `cgle`
- parent: collective/contrib/20261025T0841-c03-cgle-solitons; mutation: the CGLE linear gain becomes a local gain medium g, depleted by |A|^2 and regrowing toward g0
- run: 201 frames x 500 steps x dt 0.01 = time 1000; grid [192, 192]; wall 648s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1610-c43-cgle-gain-bigbox/world.py --out collective/contrib/20261026T2147-c46-review-cgle-bigbox/eps1.40/seed3 --seeds 3 --size 192 192 --frames 200 --no-movie`
- segmentation: matter > 0.21 of robust range [0.0, 2.349], min area 6 px

## Measurements
- components: final 7, mean 10.1, max 18; occupancy final 0.02
- tracks: 48; persistent (alive >= 50% of run): 8; longest 193 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 30.80 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 7], H1 [1, 1, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.0781/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 100, default): splits 11, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 16, merge/split ratio 1.46, nucleations 0
- channel total drift (end/start - 1): [-0.9677, -0.8294, -0.0661]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 20 at frame 104: holes 0, rim-vs-core 0.45, rim-vs-outside 0.15, heterogeneity 0.20; core [0.723, 0.553, 0.487] rim [0.283, 0.537, 0.592]
  - track 21 at frame 104: holes 0, rim-vs-core 0.47, rim-vs-outside 0.17, heterogeneity 0.16; core [0.725, 0.059, 0.493] rim [0.285, 0.179, 0.598]
  - track 26 at frame 106: holes 0, rim-vs-core 0.24, rim-vs-outside 0.40, heterogeneity 0.17; core [0.707, 0.047, 0.515] rim [0.477, 0.111, 0.563]
  - track 10 at frame 74: holes 0, rim-vs-core 0.49, rim-vs-outside 0.17, heterogeneity 0.17; core [0.741, 0.029, 0.437] rim [0.292, 0.19, 0.537]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 57 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial |A|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.631, rim/outside 21.1 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.578)
  - radial Re A: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.95, rim/outside 1.07 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.417)
  - radial g: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.72, rim/outside 0.867 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.62)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #20 (t=520, R_eq 5.41): ['Re A']; #21 (t=520, R_eq 5.35): none; #26 (t=530, R_eq 5.75): none; #10 (t=370, R_eq 5.81): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
