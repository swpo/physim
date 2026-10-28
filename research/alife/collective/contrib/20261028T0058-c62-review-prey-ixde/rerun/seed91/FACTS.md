# Evidence pack: digestion-driven-predators (seed 91)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1791s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/rv2/rerun/seed91 --seeds 91 --size 256 256 --frames 120 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1571, 1.7935], min area 6 px

## Measurements
- components: final 191, mean 174.1, max 201; occupancy final 0.20
- tracks: 751; persistent (alive >= 50% of run): 82; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [195, 188, 167], H1 [0, 0, 0]
- motion: 298 long-lived tracks moved >= 1 body length; max speed 0.00865/time; max body lengths 8.9
- replication (lineage window K = 20 frames = time 2000, default): splits 137, persistent splits 48 (0 more failed only because the siblings re-merged within K), max generation 5, merges 161, merge/split ratio 1.18, nucleations 317
- channel total drift (end/start - 1): [-0.055, None, -0.6128, -0.6023, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 62: holes 0, rim-vs-core 0.54, rim-vs-outside 0.19, heterogeneity 0.25; core [0.408, 0.563, 0.149, 0.455, 0.429] rim [0.368, 0.153, 0.163, 0.396, 0.088]
  - track 24 at frame 62: holes 0, rim-vs-core 0.20, rim-vs-outside 0.39, heterogeneity 0.24; core [0.498, 0.396, 0.155, 0.562, 0.271] rim [0.374, 0.349, 0.171, 0.421, 0.25]
  - track 40 at frame 62: holes 0, rim-vs-core 0.46, rim-vs-outside 0.17, heterogeneity 0.21; core [0.391, 0.544, 0.167, 0.435, 0.312] rim [0.337, 0.159, 0.178, 0.368, 0.082]
  - track 621 at frame 110: holes 0, rim-vs-core 0.39, rim-vs-outside 0.13, heterogeneity 0.16; core [0.265, 0.555, 0.199, 0.29, 0.211] rim [0.252, 0.202, 0.205, 0.269, 0.061]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1103 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.984, rim/outside 3.95 (aggregate of 1103 individuals; 159/1103 membrane-like individually; rim level 0.454)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.35, rim/outside 6.29 (aggregate of 1103 individuals; 12/1103 membrane-like individually; rim level 0.236)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.42, rim/outside 0.855 (aggregate of 1103 individuals; 0/1103 membrane-like individually; rim level 0.175)
  - radial product p: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.955, rim/outside 4.02 (aggregate of 1103 individuals; 97/1103 membrane-like individually; rim level 0.471)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.297, rim/outside 12.4 (aggregate of 1103 individuals; 22/1103 membrane-like individually; rim level 0.147)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #18 (t=6200, R_eq 4.51): ['prey a']; #24 (t=6200, R_eq 4.07): none; #40 (t=6200, R_eq 3.91): ['prey a', 'product p']; #621 (t=11000, R_eq 4.48): none
- species `prey` (channels ['prey a'], own threshold): components final 182, mean 173.4, max 197; tracks 715, persistent 99; splits 139, persistent splits 72 (K=20), max generation 6, merges 64, merge/split 0.46; moving tracks 317
- species `predator` (channels ['predator b'], own threshold): components final 192, mean 145.6, max 193; tracks 606, persistent 82; splits 81, persistent splits 52 (K=20), max generation 5, merges 25, merge/split 0.309; moving tracks 302

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 1103 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
