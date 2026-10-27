# Evidence pack: digestion-driven-predators (seed 33)

- world: `../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1796s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/audit/digestion-ecology/replication/claim256 --seeds 33 --size 256 256 --frames 120 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1569, 1.7947], min area 6 px

## Measurements
- components: final 189, mean 173.8, max 203; occupancy final 0.20
- tracks: 786; persistent (alive >= 50% of run): 73; longest 117 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 24.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [195, 178, 154], H1 [0, 0, 0]
- motion: 311 long-lived tracks moved >= 1 body length; max speed 0.0081/time; max body lengths 9.0
- replication (lineage window K = 20 frames = time 2000, default): splits 153, persistent splits 51 (0 more failed only because the siblings re-merged within K), max generation 4, merges 154, merge/split ratio 1.01, nucleations 327
- channel total drift (end/start - 1): [-0.0516, None, -0.6159, -0.6024, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 61 at frame 63: holes 0, rim-vs-core 0.47, rim-vs-outside 0.13, heterogeneity 0.24; core [0.399, 0.502, 0.155, 0.444, 0.368] rim [0.319, 0.157, 0.175, 0.344, 0.075]
  - track 62 at frame 63: holes 0, rim-vs-core 0.47, rim-vs-outside 0.15, heterogeneity 0.27; core [0.429, 0.48, 0.154, 0.482, 0.359] rim [0.329, 0.153, 0.181, 0.363, 0.067]
  - track 74 at frame 63: holes 0, rim-vs-core 0.49, rim-vs-outside 0.17, heterogeneity 0.27; core [0.494, 0.471, 0.145, 0.559, 0.397] rim [0.345, 0.174, 0.177, 0.385, 0.087]
  - track 655 at frame 105: holes 0, rim-vs-core 0.44, rim-vs-outside 0.13, heterogeneity 0.20; core [0.343, 0.539, 0.147, 0.375, 0.266] rim [0.359, 0.151, 0.154, 0.381, 0.066]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1108 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.981, rim/outside 3.94 (aggregate of 1108 individuals; 136/1108 membrane-like individually; rim level 0.464)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.343, rim/outside 5.97 (aggregate of 1108 individuals; 20/1108 membrane-like individually; rim level 0.228)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.44, rim/outside 0.852 (aggregate of 1108 individuals; 0/1108 membrane-like individually; rim level 0.172)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.953, rim/outside 4.02 (aggregate of 1108 individuals; 71/1108 membrane-like individually; rim level 0.482)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.296, rim/outside 12.3 (aggregate of 1108 individuals; 21/1108 membrane-like individually; rim level 0.145)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #61 (t=6300, R_eq 4.55): none; #62 (t=6300, R_eq 4.89): none; #74 (t=6300, R_eq 4.65): none; #655 (t=10500, R_eq 4.69): ['prey a', 'product p']
- species `prey` (channels ['prey a'], own threshold): components final 187, mean 172.4, max 197; tracks 757, persistent 85; splits 148, persistent splits 68 (K=20), max generation 4, merges 60, merge/split 0.405; moving tracks 319
- species `predator` (channels ['predator b'], own threshold): components final 177, mean 143.5, max 190; tracks 587, persistent 80; splits 73, persistent splits 50 (K=20), max generation 4, merges 19, merge/split 0.26; moving tracks 316

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 1108 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
