# Direction: TROPHIC TOWER (3-level food chain)

Build a resource -> grazer -> predator lattice-field world.

Physics sketch (adapt freely): R regenerates logistically; grazer H eats R
(Holling type-II uptake: h*H*R/(1+s*R)); predator P eats H similarly; both
have death rates and diffusion; all continuous fields, torus, small noise.

Target hierarchy:
  L1 (fast): local eating/diffusion fronts, patch boundaries
  L2 (medium): patch populations, pursuit waves (P chasing H chasing R)
  L3 (slow, TOP): global predator-prey OSCILLATOR (lynx-hare cycles) or
      boom-bust relaxation cycles. Top variable: mean H (or P) over the map.

Theory coordinates to sweep: uptake/death ratio per level, timescale ratio
between levels (grazer vs predator rates), Holling saturation, diffusion
ratio (pursuit needs D_P >= D_H). Literature says spatial LV systems damp to
steady state in mean-field but SUSTAIN cycles with the right saturation +
space (de Roos et al) — find that region. The prize: period responds to a
price (G3) like "predator efficiency".

Real-world analogue: lynx-hare, plankton blooms. Films would be spectacular
(three-color pursuit).

Name your dir probes/search/trophic-tower/.
