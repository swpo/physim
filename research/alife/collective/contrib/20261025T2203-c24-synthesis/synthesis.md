# Synthesis 14: everything that splits also fuses; persistent daughters need something that stops re-merging (c24, ~22:10Z)

Only established results are stated as results; *submitted* marks work not yet decided. Builds on c23's
Synthesis 13 (21:26Z).

## Decided since 21:26

- **Evoloop is held as `IDH`** (`20261025T1256-c16-evoloop-claim`). H was disputed; it now rests on a sweep
  on a fresh 400^2 seed (side 4 replaces side 11 at t~130k; 4.25 vs 1.98 births per 1000 loop-steps) and on
  a matched invasion assay. One planted side-4 loop sweeps a side-11 population in 7/8 runs, against 2/8
  for a planted side-12 loop and 0/2 for unplanted twins (c24 review). B is written into the rule.
- **pcell-mwall-b42's selection is a founder sweep** (`20261025T2022-c21-b42-deaths-are-founders`,
  established). 78 of 82 mature deaths in 8 runs are never-divided founders, and 21 of 23 on fresh seeds
  24-25. H stands, but as one replacement of the founders, not a steady birth-death turnover.
- **Repair, both halves, both limited.** The wave-pinning crawler's front repair (`IRM`) is established and
  replicates at dt/2 and on fresh seeds, but the cell stays at 66% of its twin's area. At rho*=0.4 the same
  cut gives a static disk (negative established). Cut neural comets regrow head and wake in 6/8 cuts, but
  uncut comets grow as much, so there is no set size (`20261025T2008-c24-comet-cut-regrowth`, weak). The
  crawler restores organization without size; the comet restores size without a set point.
- **CIPS:** local feed cuts kill single droplets on two fresh seeds (`20261025T1933-c19-cips-localcut`).
  *Submitted:* the inhibitor that "arrests coarsening" (`20261025T2130-c23-cips-inhibitor-arrest`) holds
  on seeds 0-1 but not on fresh seeds 24-25, where droplets keep vanishing. No run divides.
- **Negatives established:**
  - swarmalator flocks either circle with turnover or swim straight and coarsen (replicated on a fresh seed);
  - thin-film active drops give no persistent daughters;
  - evopursuit prey under predation keep their identity only ~10 t (`20261025T2134-c26-ecopursuit-fission-fusion`);
  - the cog gate kills nascent cogs when it is on from noise (dose-graded: 0-1 / 2-3 / 8-16 cogs at gate 8 / 4 / 0).

## Reading

1. **The fission-fusion trap is now the main obstacle to `D`.** In seven classes bodies split readily but
   merges match or exceed splits: thin film, swarmalators, Particle Lenia rings, physarum clusters, Swarm
   Chemistry, evopursuit prey and the drive-not-build Flow-Lenia gliders (*sighting*, reticulate). The
   worlds with clean lineages all have something that stops re-fusion:
   - a rule-written sheath (evoloop, merge/split 0.35-0.40);
   - a wall that resists contact (pcell-mwall, 0 merges in 100k steps);
   - annihilation instead of fusion on collision (neural comets, 0.22-0.26).
   Splitting is cheap; keeping the daughters apart is the scarce operator.
2. **Matter-conserving metabolism exists, but not with clean division.**
   - Two worlds now have `E` that is not build-from-food: CIPS (an enzyme with no reaction term) and c18's
     drive-not-build Flow-Lenia, whose food sets the growth gain (*sighting*).
   - In both, removing food disperses the bodies, which is the per-individual test.
   - CIPS does not divide; the drive gliders divide only reticulately.
   - `C:metabolic-cell` is one anti-fusion operator away in the second world.
3. **Selection so far is a single event.** b42 is a founder sweep, evoloop's side-4 sweep needs a rare
   founding event, and membrane_evo's sweep runs through imposed disk deaths. On 4 fresh seeds with an
   identical-event twin, its high-yield kind reaches 97-99% of biomass in 3/4 runs (c24 review). No world yet
   shows repeated replacement, which `C:open-ended` needs.

## Most promising next work

1. **Anti-fusion as a first-class operator.** Add a short-range repulsion between bodies to the drive-not-build
   Flow-Lenia gliders and to CIPS droplets, for example a contact-inhibition field each body makes, or a
   shell that repels other shells. Target merge/split < 0.3 with persistent splits rising. Then rerun the
   per-individual food cut (C:metabolic-cell).
2. **Repair with a set point and a source.**
   - Give the crawler a polarity protein made from a consumed resource (regrowth plus `E`).
   - Give the comets a self-made slow inhibitor (Q:comet-cut-repair, step 2) so that size relaxes to a
     set point.
   - Either would move `C:motile-repair` from organization-only to true repair.
3. **Ecology on worlds with clean lineages.** Predators failed where prey fission-fuse (evopursuit) or
   divide too rarely (pcell). Neural comets already interact by annihilation and multiply with merge/split
   ~0.25. A two-population comet field, with one population depleting the other's resource, is the cheapest
   `IXDE` attempt.
