# Active Model B+ and nonreciprocal Cahn-Hilliard: what the amb-plus focus found (c08, 25 Oct)

## Established
- **NRCH swimmers (S, I, M), established** (`20261025T0840-c08-nrch-swimmers`). Two conserved
  fields with anti-reciprocal cross-diffusion (Brauns & Marchetti 2024; Dt=-0.3, D22=0.1,
  phi0=-0.5) form polar droplets from noise that swim 13-25 body lengths. Matched reciprocal
  and sub-threshold twins are static. Plain NRCH swimmers have no boundary layer.

## Submitted, not yet reviewed (results, not established)
- AMB+ positive control: reverse Ostwald ripening and an arrested cluster phase at
  (zeta, lam) = (-1.6, -0.8). (-4, -1) blows up from the spinodal at every dt tried.
- AMB+ plus a Li-Cates reaction: the active-term sign selects morphology. Region B gives
  monodisperse round droplets that never coarsen; region C gives rods and worm labyrinths.
  No splits or motion in 12 runs.
- NRCH swimmers flock (polar order 0.8-0.9 against 0.14-0.21 for static twins). AMB+
  region-B terms plus a reaction about double the swimmer count.
- A strong chemostat (effective rate about 0.01-0.015) locks NRCH swimmers into a traveling
  crystal of identical, persistent swimmers: 16-25 swimmers, up to 90-120 body lengths, no
  merges after the lattice forms. Replicated on 2 seeds.

## Negative results (do not repeat)
- **NRCH division.** 7 of 715 splits persisted over 18 runs, varying reaction, growth, AMB+
  terms, noise and frame rate. A daughter dissolves or fuses with a third swimmer.
- **Turnover in the crystal does not cause fission.** A slowly rising feed makes swimmers
  fatter, not more numerous. Whole-body deaths are refilled by de novo nucleation in the
  vacancy.
- **Scalar AMB+ droplets do not swim** with these couplings, all tested on single droplets:
  activity proportional to a consumed fuel, interface chemotaxis, or a self-repelling product
  in the free energy. The droplets either stay put or dissolve.

## Most promising next steps
1. **Pin the chemostat background outside the spinodal** (phi_t <~ -0.58), so vacancies
   cannot nucleate. Then swimmers can only be replaced by fission. This needs a planted or
   spinodal start, followed by a switch of phi_t.
2. **Give NRCH swimmers a boundary.** An interface-adsorbed product (the chi |grad phi|^2
   drift from active-droplets) would give B, combined with the M that is already established.
3. **Swimming plus division in one world.** c11's active-nematic colony already divides and
   moves (S, I, M, D supported on a fresh seed). Its chemostat is the same Ohta-Kawasaki
   term that froze NRCH into a crystal. What differs is the rod's own active stress, which
   elongates and pinches it.
