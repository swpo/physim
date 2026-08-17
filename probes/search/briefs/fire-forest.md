# Direction: FIRE FOREST (separated-timescale excitable + SOC statistics)

Build a fuel-fire world: biomass B grows SLOWLY (logistic, tau ~ thousands of
ticks); fire F is FAST excitable spread (ignites where B high + neighbor
fire or rare lightning; burns B down over ~10 ticks; extinguishes).
Continuous fields preferred (F as fast activator with B as its fuel/slow
inhibitor — an FHN cousin where the recovery variable is GROWN, not relaxed).

Target hierarchy:
  L1 (fast): fire fronts (tick-scale spread)
  L2 (medium): fire events/avalanches with BROAD size distribution
      (powerlaw_tail: report decades honestly; Drossel-Schwabl SOC regime
      needs growth << spark << spread — find the separation in theory coords)
  L3 (slow, TOP): global biomass SAWTOOTH / relaxation oscillator (grow,
      burn, grow) — or, in other regions, spiral-wave "fire ecology".

Theory coordinates: growth/spark/spread rate RATIOS (SOC wants f/p -> 0 with
p/growth -> 0), ignition threshold vs biomass, burn efficiency.
G3 response curve: mean fire return interval (top clock) vs growth rate.

Real-world analogue: forest-fire model (Drossel-Schwabl), chaparral fire
return intervals. Beware: pure CA is fine numerically but keep fields
continuous-ish so it fits the engine template later.

Name your dir probes/search/fire-forest/.
