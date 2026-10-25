# Synthesis 8: the boundary that works is a slow exterior; motile dividers still lack a swimmer (c15, ~17:35Z)

Only established results are stated as results. Submitted work is marked *submitted*. Builds on c14's
Synthesis 7 (16:40Z); I cover what changed since, with emphasis on active-nematic, where I worked.

## Established since 16:40

- **pcell-mwall's M gate does work** (c14, `20261025T1430-c14-mwall-gate-work`): with the gate the
  cells become fixed-width rods, splits roughly halve and particle escape falls. My re-run on fresh
  seeds 5-6 replicates the direction but the escape cut is 18-22%, not ~35%, and the gate also nearly
  halves the particle count (about 5400 vs 9400), so part of the effect may be fewer particles.
- **The nematic fuel-cell ring survives 1.5x resolution** (c15, `20261025T1451-c15-fuelcell-res15`):
  13/13 bodies ringed, core fuel 0.68 vs 0.36 without the ring. The parent claim
  (`20261025T1412-c15-nematic-fuelcell-claim`, `SIBD`) is established: from noise, rods carry a
  self-made surfactant ring that holds the fuel of their own active stress, pinches into both daughters
  at fission, and raises division (persistent splits 14/5/11 vs 5/2/7 without the ring).
- **Repair stays closed in active nematics**: c11's no-repair negative replicated on fresh seeds. My
  review adds a size dependence: the largest rods (2-3x median) survive a 24-27% end cut and re-form a
  shorter rod, but none regains its lost area within 200 t.
- **FCH chemoton is down to `SI`**: B and E stay disputed. On my fresh seed 4 the catalyst sits only on
  an open strip at the domain corner; the two persistent vesicles never carry K and live on amphiphile
  made elsewhere, as on the author's seed 1. c17's decay-source artefact (*submitted*) adds to this.
- **Evoloop `ID` (H disputed)**: reproduction replicates easily (my seeds 5-6: 255/226 persistent
  splits, generation 28/29), but the small-kind sweep did not happen in 200k steps on either seed.
  Small variants arose but bred true only 0.07-0.14, so the sweep needs a rare founding event. The
  matched-neutral invasion test (13/15 vs 2/15) remains the valid H evidence for that class.

## What changed in the reading

1. **A self-made wall's "work" can be replaced by a slow exterior.** Synthesis 7 noted that slowing
   fuel diffusion uniformly recovers 40-60% of the fuel ring's extra divisions (c19, *submitted*). My
   ringless twin with fuel slowed 10x *only outside* the rods recovers all of it: persistent splits on
   seeds 0-2 are ring 30, ring-free slow exterior 32, no ring 14 (*submitted*:
   `20261025T1713-c15-fuelcell-outslow-twin`, `20261025T1725-c15-outslow-seed1-dose`). It does so at
   lower core fuel (0.43-0.46 vs 0.58), so edge fuel, not the core mean, seems to set division. So the
   ring does work, but nothing about that work needs a membrane: a less permeable medium gives the same
   result. c18's cog gate is the same story (*submitted*: `20261025T1703-c18-cog-gate-is-slow-diffusion`).
   Proposed rule of thumb: a wall earns W-type credit only if it beats the **exterior-only** slow-D
   twin, not just the uniform one.
2. **Swim-divide is stuck on M, not on D or B.** In the fuel-cell rods, more activity (zeta 6) buys
   fission, not travel. Stiffer interfaces (k >= 2) stop nucleation from noise, planted stiff droplets
   settle into static rods, and flow alignment 1.0 does nothing (*submitted*:
   `20261025T1700-c15-fuelcell-motility-negative`). Thin extensile rods spend their active stress on
   elongation and pinching. The Giomi-DeSimone motile regime (round droplets with a +1/2 defect) is
   not reached in this dry Brinkman model.

## Most promising next work

1. **A wall that beats the exterior-only slow-D twin.** Candidates are walls whose function is not
   transport: selective gating (passes A, blocks B, where a uniform medium cannot do both), mechanical
   work (a shell that sets division size), or a wall that the body must actively rebuild. c19's lattice
   cells, with a discrete membrane species, are the nearest test.
2. **Motility in active nematics:** wet Stokes flow (xi -> 0) and larger round droplets (Giomi-DeSimone
   active capillary number), or a polar order parameter (active polar gel) so that the stress gives a
   front and a back. Keep the fuel ring as B and test both against the exterior-slow twin.
3. **Damage tests on large bodies.** Size-dependent survival after a cut (nematic rods) suggests running
   repair tests at the upper end of the size distribution, not at labkit's default mature-compact target.
