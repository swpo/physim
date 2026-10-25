# Evidence pack: crawler-divide (seed 3)

- world: `../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0908-c04-crawler-divide-confound/world.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 267s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0908-c04-crawler-divide-confound/world.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/ccs/ocsk/seed3 --seeds 3 --frames 240 --no-movie`
- segmentation: matter > 0.25 of robust range [-0.0, 0.9973], min area 6 px

## Measurements
- components: final 1, mean 5.1, max 17; occupancy final 0.01
- tracks: 36; persistent (alive >= 50% of run): 0; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.19, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 3.64/time; max body lengths 2.4
- replication (lineage window K = 20 frames = time 50, default): splits 17, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 1, merge/split ratio 0.059, nucleations 0
- channel total drift (end/start - 1): [-0.8487, -0.9583, None, -0.6816]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 17 at frame 182: holes 0, rim-vs-core 0.43, rim-vs-outside 0.32, heterogeneity 0.07; core [0.86, 0.102, 0.013, 0.069] rim [0.433, 0.145, 0.006, 0.08]
  - track 23 at frame 175: holes 0, rim-vs-core 0.42, rim-vs-outside 0.32, heterogeneity 0.07; core [0.853, 0.1, 0.011, 0.065] rim [0.436, 0.138, 0.006, 0.074]
  - track 25 at frame 157: holes 0, rim-vs-core 0.40, rim-vs-outside 0.25, heterogeneity 0.07; core [0.795, 0.098, 0.007, 0.049] rim [0.392, 0.113, 0.004, 0.054]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 30 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.78, rim/outside 4.91 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.664)
  - radial |P| (actin polarization): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.07, rim/outside 4.98 (aggregate of 30 individuals; 23/30 membrane-like individually; rim level 0.118)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.865, rim/outside 2.14 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.05)
  - radial n (nutrient): peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 1.08, rim/outside 1.08 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.0734)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #17 (t=455, R_eq 21.59): ['|P| (actin polarization)']; #23 (t=437.5, R_eq 20.42): ['|P| (actin polarization)']; #3 (t=167.5, R_eq 144.43): none; #25 (t=392.5, R_eq 17.57): ['|P| (actin polarization)']

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 3 of 30 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
