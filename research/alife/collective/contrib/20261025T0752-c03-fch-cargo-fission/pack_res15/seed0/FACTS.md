# Evidence pack: fch-cargo-micelles (seed 0)

- world: `../../world_res15.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0726-c03-fch-protocell/world.py; mutation: micelle-fission regime (eta1=4, eta2=5, amphiphile feed 5e-4) and chi=-3: the self-made solute partitions INTO amphiphile-rich bodies (cargo)
- run: 101 frames x 200 steps x dt 0.02 = time 400; grid [192, 192]; wall 287s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0752-c03-fch-cargo-fission/world_res15.py --out collective/contrib/20261025T0752-c03-fch-cargo-fission/pack_res15/seed0 --seeds 0 --frames 100 --size 192 192 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1166, 2.9912], min area 6 px

## Measurements
- components: final 54, mean 38.5, max 54; occupancy final 0.25
- tracks: 85; persistent (alive >= 50% of run): 30; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.56 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [54, 54, 54], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 80, default): splits 25, persistent splits 19 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 28
- channel total drift (end/start - 1): [0.6651, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 51: holes 0, rim-vs-core 0.54, rim-vs-outside 0.16, heterogeneity 0.28; core [0.703, 0.254] rim [0.227, 0.002]
  - track 9 at frame 51: holes 0, rim-vs-core 0.54, rim-vs-outside 0.16, heterogeneity 0.28; core [0.696, 0.247] rim [0.218, 0.002]
  - track 10 at frame 51: holes 0, rim-vs-core 0.54, rim-vs-outside 0.15, heterogeneity 0.28; core [0.694, 0.249] rim [0.216, 0.002]
  - track 56 at frame 82: holes 0, rim-vs-core 0.53, rim-vs-outside 0.16, heterogeneity 0.26; core [0.705, 0.225] rim [0.227, 0.002]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 242 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.549, rim/outside 14.4 (aggregate of 242 individuals; 3/242 membrane-like individually; rim level 0.515)
  - radial solute c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.046, rim/outside 2.9 (aggregate of 242 individuals; 6/242 membrane-like individually; rim level 0.0224)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=204, R_eq 7.38): none; #9 (t=204, R_eq 7.42): none; #10 (t=204, R_eq 7.46): none; #56 (t=328, R_eq 7.42): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
