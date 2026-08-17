# Direction: SLIME LIFECYCLE (starvation-triggered multicellularity)

Build a Dictyostelium-inspired world with a full LIFECYCLE as the top law.

Physics sketch: cells V eat resource R (regenerating slowly). When local R
is scarce, cells emit pulses of attractant chemical S (excitable relay: a
cAMP-like wave layer that other starving cells re-emit); cells drift up the
S gradient (advection term on V). Aggregates form (dense V clusters), which
SURVIVE starvation better (lower per-capita death when dense) and disperse
again when R has regrown under them (grazed lawns regrow while the swarm
sits elsewhere... or spores disperse).

Target hierarchy:
  L1 (fast): relay waves of S (tick-scale, spiral patterns around aggregation
      centers — the classic film)
  L2 (medium): aggregation — cluster count collapsing from many to few
      (coarsening law), collective motion
  L3 (slow, TOP): the LIFECYCLE oscillator — dispersed-grazing <-> aggregated
      phases alternating with resource regrowth; top variable: aggregation
      index (e.g. spatial variance of V or max cluster mass) oscillating.

Theory coordinates: starvation threshold vs R regen time, chemotaxis
strength vs diffusion (Keller-Segel collapse boundary — stay below blowup;
CLIP or saturate the advection), relay excitability, density-protection
strength. G2 top model: oscillator (n_cycles >= 5) on aggregation index.
G3: lifecycle period vs R regen rate response curve.

Real-world analogue: slime mold aggregation, quorum behaviors. The most
cinematic candidate if the spirals + swarming work — save strips generously.
Numerical care: advection stability (upwind or clipped velocities, small dt).

Name your dir probes/search/slime-lifecycle/.
