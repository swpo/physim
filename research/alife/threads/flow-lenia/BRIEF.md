# Thread brief: flow-lenia

**Family:** mass-conserving Lenia (Flow-Lenia, Plantec et al. 2023) and parameter
localization.

**Why this thread.** In Flow-Lenia the growth field does not create matter; it moves
matter along a flow, so total mass is conserved. That rules out explosive growth, makes
individuals compete for matter, and gives sharp, durable creatures. With parameter
localization, each parcel of matter carries its own update-rule parameters, which are
advected and mixed with it. Several species can then live in one world, and inheritance
happens in situ. This is our most direct path to L7 (heredity with selection).

**Start from.** The Flow-Lenia section of `LITERATURE.md` (affinity, flow
`F = (1-alpha) grad U - alpha grad A_sum`, alpha from local mass, reintegration tracking).
Validate that mass is conserved to round-off and that a known creature persists and moves.

**First sprint, suggested.**
1. Implement and validate Flow-Lenia (single species, then multi-channel).
2. Implement parameter localization: a parameter field carried with matter by the same
   reintegration step. Seed 2-4 species from random parameters and run until they
   interact. Who wins, coexists, or mixes?
3. Add heritable variation: small parameter mutations when matter splits or at a low rate.
   Look for lineages (labkit lineage.png), and plot per-species mass over time.

**Mutation ideas.** Different mixing rules for parameters at collisions (winner-takes-all,
mass-weighted, stochastic sampling); a food or energy field that is converted to
matter (an open system with a conserved total); hybrid growth that is partly local.

**Targets.** L2-L4b motile creatures from random init; L5 species interactions;
L6 division; L7 differential success of heritable variants.
