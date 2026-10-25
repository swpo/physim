# Evidence pack: crawler-divide (seed 1)

- world: `../cdiv.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 235s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/cdiv.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/sw_0.15_0.006 --seeds 1 --frames 240 --no-movie`
- segmentation: matter > 0.25 of robust range [-0.0, 0.991], min area 6 px

## Measurements
- components: final 1, mean 1.0, max 2; occupancy final 1.00
- tracks: 4; persistent (alive >= 50% of run): 1; longest 184 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.60 (1 = constant size)
- enclosures: components with a hole mean 0.54, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 28, 12]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 3, 2], H1 [19, 12, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 3.37/time; max body lengths 3.7
- replication (lineage window K = 20 frames = time 50, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio 1, nucleations 0
- channel total drift (end/start - 1): [26.0662, 2.1751, None, -0.7958]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 149: holes 0, rim-vs-core 0.01, rim-vs-outside 0.82, heterogeneity 0.10; core [0.836, 0.089, 0.824, 0.005] rim [0.828, 0.092, 0.816, 0.005]
  - track 0 at frame 24: holes 0, rim-vs-core 0.27, rim-vs-outside 0.75, heterogeneity 0.16; core [0.759, 0.262, 0.088, 0.807] rim [0.668, 0.512, 0.078, 0.835]
  - track 1 at frame 52: holes 0, rim-vs-core 0.22, rim-vs-outside 0.65, heterogeneity 0.18; core [0.699, 0.132, 0.231, 0.534] rim [0.649, 0.343, 0.215, 0.533]
  - track 2 at frame 52: holes 0, rim-vs-core 0.30, rim-vs-outside 0.84, heterogeneity 0.15; core [0.867, 0.317, 0.086, 0.488] rim [0.733, 0.586, 0.073, 0.52]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.1, rim/outside 71.3 (aggregate of 6 individuals; 1/6 membrane-like individually; rim level 0.76)
  - radial |P| (actin polarization): peak at rho=1.35 (in the peak band 0.5-1.5), rim/core 1.2, rim/outside 13.8 (aggregate of 6 individuals; 1/6 membrane-like individually; rim level 0.132)
  - radial V/V0 (body content): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.08, rim/outside 68.6 (aggregate of 6 individuals; 1/6 membrane-like individually; rim level 0.676)
  - radial n (nutrient): peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.04, rim/outside 0.213 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.158)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=372.5, R_eq 144.41): none; #0 (t=60, R_eq 54.96): none; #1 (t=130, R_eq 93.05, ring): none; #2 (t=130, R_eq 47.72, ring): ['u (cell)', '|P| (actin polarization)']

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 6 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 6 of 6 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
