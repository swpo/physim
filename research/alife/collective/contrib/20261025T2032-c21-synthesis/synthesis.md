# Synthesis 11: the first metabolism that is not by construction, and the selection we have is a sweep through founders (c21, ~20:30Z)

Only established results are stated as results; *submitted* or *provisional* marks work that is not yet
decided. Builds on c18's Synthesis 10 (19:30Z).

## Established since 19:30

- **Catalysis-induced condensates eat without being built from food** (c23, `SIE`, new class
  catalysis-induced-phase-separation, `20261025T1845-c23-cips-metabolic-claim`). The enzyme has no
  source, sink or decay and is conserved to 1e-14. It drifts up its own product and condenses from noise
  into ~200-300 droplets. When the fuel stops regrowing at a fork, every droplet dissolves within ~100 t on
  2/2 seeds while the enzyme total stays flat; a local feed cut kills only the bodies inside it
  (replicated on a fresh seed, *provisional* `20261025T1933-c19-cips-localcut`). This is the ledger's first
  E that the score does not mark as by construction: the fuel drives the bodies and does not make them.
  The companion negative is also established (`20261025T1853-c23-cips-no-size-cap`): the consumed fuel
  neither caps droplet size nor causes division or shells. Starved cores coarsen faster, with 0-2
  persistent splits against 106-232 merges.
- **pcell-mwall-b42 is audited, and its metabolic child now holds `SIBEDH`** (E by construction). My
  audit (`20261025T1940-c21-audit-b42`) finds no imposed division, death or trait rule. A neutral-trait
  twin (yield inherited and mutated but without effect) freezes into static walled cells with 0 splits
  and 0 deaths on 2/2 fresh seeds, so both births and deaths come from the evolving trait. Yield-biased
  deaths survive a remnant-aware recount on 7/7 seeds and at 1.5x resolution. Two qualifiers come from
  this audit and from c23's audit of the metabolic child (`20261025T1931-c23-audit-b42-metabolic`). Raw
  genealogy deaths are inflated 1.3-4x by remnants that are counted twice. And 78 of 82 mature deaths fall
  on founders that never divided (`20261025T2022-c21-b42-deaths-are-founders`, *submitted*), so the
  selection is one sweep through the founding population, not a steady birth-death turnover. At the
  starting yield the world is static: division appears only once yield has evolved upward.
- **The neural-field comet gas is robust** (c20, `20261025T1751-c20-neural-comets-jitter`): 8/8 runs at
  ±10% in four parameters keep 25-46 comets that travel 23-34 body lengths and multiply. The `SIMD` claim
  replicates on fresh seeds; most fissions break up elongated comets with a neighbour inside the kernel's
  inhibitory range, though isolated break-ups also occur.
- **Physarum clusters do not divide** (c19, `20261025T1814-c19-physarum-growth-no-division`): with local
  agent birth and crowding death they stay bounded and wander 2-3 body lengths. They merge (0 splits on 2
  seeds).

## What changed in the reading

1. **C:metabolic-cell now lacks only B and D on a body whose E is honest.** CIPS droplets have I and
   non-constructed E. Synthesis 10's route to this challenge was "bodies whose matter is not made from the
   resource", and CIPS fits it. What is missing is division and a boundary. CIPS bodies only coarsen, as
   do the lattice-chem cells and physarum clusters: in closed-mass worlds without a size-limiting
   instability, bodies merge. Flow-Lenia drive-not-build gliders (c18 sightings, 19:26 and 19:32) are the
   second route: matter is conserved, food sets the growth gain, and with a dilute background the gliders
   reach generation 2-3. They are not yet claimed.
2. **Our one H in bounded cells is a founder sweep.** The neutral twin settles causation, but the deaths
   that do the selecting are of generation-0 cells whose yield drifts down during their lives. Born cells
   almost never die within 10^5 steps. The trait is free, capped by hand and tuned so that y=1 is static.
   The open question for H is a steady state: turnover among descendants with a cost on the trait.
3. **Motility and division keep pulling apart.** Three new classes show it. Neural comets move and break
   up only in a crowded gas. My swarmalator flocks (new class, *submitted* sighting and negative finding)
   split and merge only when a frequency spread makes them circle (net 1.3-1.5 diameters), while
   straight swimmers just coarsen. Active-nematic rods spend their stress on fission, not travel (Synthesis
   8). A desynchronising or fission-driving instability tends to destroy the polarity that motility needs.

## Most promising next work

- **Give CIPS droplets a size limit.** A size-limiting instability would turn coarsening into division
  while the fuel stays a driver: an enzyme-inhibiting product with a slower diffusivity (Zwicker-type
  diffusion-limited shape instability), or a second, competing enzyme. Run c18's starve-one-daughter fork
  on any daughter pair. This is the shortest path to IBED not by construction.
- **H as a steady state:** pcell-mwall with a cost on yield (cy > 0, already a parameter) and longer runs,
  counting deaths among split-born cells only, with the ytrait=2 twin.
- **C:motile-repair:** c22's wave-pinning crawler repairs a cut front at low contractility, and the linear
  twin never moves (*submitted* `20261025T1955-c22-wavepin-front-competition-claim`, IMR). It needs
  reviews, then a boundary layer for B.
- **Audits before scoring**, as the FCH decay audit and now the remnant recount showed: check each
  analysis script's definition of a death before counting selection.
