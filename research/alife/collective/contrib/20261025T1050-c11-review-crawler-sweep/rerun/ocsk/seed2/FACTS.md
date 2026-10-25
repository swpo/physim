# Evidence pack: crawler-divide (seed 2)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T0908-c04-crawler-divide-confound/world.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 266s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0908-c04-crawler-divide-confound/world.py --out /tmp/claude-0/c11rev13/ocsk --seeds 2 --frames 240 --no-movie`
- segmentation: matter > 0.25 of robust range [-0.0, 0.9991], min area 6 px

## Measurements
- components: final 0, mean 5.2, max 19; occupancy final 0.00
- tracks: 38; persistent (alive >= 50% of run): 0; longest 90 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.18, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 3.77/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 50, default): splits 17, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.059, nucleations 0
- channel total drift (end/start - 1): [-1.0, -1.0, None, -0.7081]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 32 at frame 182: holes 0, rim-vs-core 0.41, rim-vs-outside 0.31, heterogeneity 0.07; core [0.834, 0.109, 0.009, 0.078] rim [0.424, 0.145, 0.005, 0.087]
  - track 26 at frame 169: holes 0, rim-vs-core 0.41, rim-vs-outside 0.31, heterogeneity 0.07; core [0.837, 0.098, 0.009, 0.058] rim [0.429, 0.129, 0.005, 0.066]
  - track 35 at frame 171: holes 0, rim-vs-core 0.40, rim-vs-outside 0.25, heterogeneity 0.07; core [0.786, 0.108, 0.007, 0.065] rim [0.388, 0.125, 0.003, 0.072]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 35 components >= 12 px at frames [40, 81, 121, 159, 200]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.8, rim/outside 3.82 (aggregate of 35 individuals; 1/35 membrane-like individually; rim level 0.644)
  - radial |P| (actin polarization): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.06, rim/outside 3.77 (aggregate of 35 individuals; 26/35 membrane-like individually; rim level 0.11)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.992, rim/outside 2.61 (aggregate of 35 individuals; 2/35 membrane-like individually; rim level 0.0495)
  - radial n (nutrient): peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 1.09, rim/outside 1.09 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.0668)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #32 (t=455, R_eq 19.36): ['|P| (actin polarization)']; #3 (t=162.5, R_eq 144.43): none; #26 (t=422.5, R_eq 19.05): ['|P| (actin polarization)']; #35 (t=427.5, R_eq 17.48): ['|P| (actin polarization)']

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 35 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 2 of 35 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
