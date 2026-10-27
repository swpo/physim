# fed-vortices screen (c53), seed 0-3, T=300-1200, 128^2, by eye and scan.py
Defaults now in world.py are the bounded-spot setting (pack_spots/ was run with the same values via WORLD_P).
- nu 0.05-0.1, noise 0.6, e 0.5 (|omega| eating): numerical blow-up by t=4 (initial velocities ~7 px/t, spectral blocking).
- nu 0.2, wi 0.1, e 0.5-2 (omega^2 eating), kY 0.5: same-sign vortex patches grow without bound into domain-filling,
  coarsening 2D turbulence (inverse cascade); the vortex rim eats and the core goes hollow (qa2, qb0, qb1).
- fast fuel (kY 2-4) with noise >= 0.1, or slow fuel (kY 0.05-0.3, kF <= 0.01) at any noise: the initial flash eats the
  fuel and every vortex decays (13 settings).
- kY 1, kF 0.02, e 10, noise 0.06: bounded vortex spots (~100 px, |omega| 0.16) in fuel-depletion halos; seed 0: 3
  same-sign monopoles drifting by mutual induction; seed 1: a +/- dipole that travels, swaps partner, travels on
  (dipole_seed1.json, sighting.png). noise 0.075 seeds 1-3: 2 of 3 extinct after the flash. S is fragile.
