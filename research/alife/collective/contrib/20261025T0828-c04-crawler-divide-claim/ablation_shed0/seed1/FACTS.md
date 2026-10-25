# Evidence pack: crawler (seed 1)

- world: `../../crawler.py`, family `phase-field`
- parent: None; mutation: Ziebert-Aranson crawling cell, body-wise area constraint
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 199s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/crawler.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/cr/C --seeds 0 1 --frames 240 --threshold 0.25 --no-movie`
- segmentation: matter > 0.26 of robust range [-0.0, 0.9689], min area 6 px

## Measurements
- components: final 25, mean 17.0, max 25; occupancy final 0.22
- tracks: 138; persistent (alive >= 50% of run): 25; longest 161 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.54 (1 = constant size)
- enclosures: components with a hole mean 0.15, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 25, 25], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 50, default): splits 52, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 32, merge/split ratio 0.615, nucleations 0
- channel total drift (end/start - 1): [3.7955, 0.8347, None, -0.7611]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 92 at frame 161: holes 0, rim-vs-core 0.33, rim-vs-outside 0.22, heterogeneity 0.06; core [0.709, 0.133, 0.002, 0.039] rim [0.382, 0.159, 0.001, 0.044]
  - track 93 at frame 161: holes 0, rim-vs-core 0.29, rim-vs-outside 0.17, heterogeneity 0.05; core [0.636, 0.133, 0.0, 0.047] rim [0.348, 0.152, 0.0, 0.05]
  - track 98 at frame 161: holes 0, rim-vs-core 0.21, rim-vs-outside 0.25, heterogeneity 0.05; core [0.641, 0.125, 0.0, 0.045] rim [0.436, 0.147, 0.0, 0.048]
  - track 128 at frame 165: holes 0, rim-vs-core 0.28, rim-vs-outside 0.17, heterogeneity 0.05; core [0.625, 0.133, 0.0, 0.051] rim [0.346, 0.154, 0.0, 0.055]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 112 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.758, rim/outside 6.7 (aggregate of 112 individuals; 1/112 membrane-like individually; rim level 0.592)
  - radial |P| (actin polarization): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.48, rim/outside 4.22 (aggregate of 112 individuals; 102/112 membrane-like individually; rim level 0.176)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.872, rim/outside 1.03 (aggregate of 112 individuals; 1/112 membrane-like individually; rim level 0.0421)
  - radial n (nutrient): peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 1.12, rim/outside 0.993 (aggregate of 112 individuals; 0/112 membrane-like individually; rim level 0.0945)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #92 (t=402.5, R_eq 14.94): ['|P| (actin polarization)']; #93 (t=402.5, R_eq 13.27): ['|P| (actin polarization)']; #98 (t=402.5, R_eq 13.06): ['|P| (actin polarization)']; #128 (t=412.5, R_eq 13.04): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 112 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 1 of 112 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
