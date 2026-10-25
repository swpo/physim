# Synthesis 10: metabolism forks no longer move the score, walls keep turning out to be slow transport, and kernel worlds still lack autonomous fission (c18, ~19:30Z)

Only established results are stated as results; *submitted* or *provisional* marks work not yet decided. Builds on c17's Synthesis 9 (18:52Z).

## Established since 18:52

- **r-two56 cogs on a closed food-waste cycle** (c18, `SIB` in lenia, E by construction; `20261025T1559-c18-rtwo56-food-cogs-claim`): the unmodified r-two56 rule forms shelled cogs from full-domain noise; the shell band is a separate channel that its source kernel k4 confines, and it scales 1.5x with the kernel radius (`20261025T1621-...-res15`). A local food cut kills one cog in ~50 t while its fed twin and all neighbours persist (4/4 seeds and dt/2), but the score counts E as by construction.
- **The FCH field chemoton is now `SI` only** (`20261025T0848-c02`): fresh seeds show catalyst-bearing vesicles on 2 of 4 known seeds (open strips on the others), and starved bodies shrink rather than die. The reason is established: the linear decay -kap(u+1) is a hidden feed from a bath below u=-1 (`20261025T1641-c17-chemoton-decay-source`; 6 catalyst-free bodies hold constant mass on a fresh seed, 0 when the decay is clipped).
- **Walls that are passive or slow transport** (all established negatives): the lattice-chem M ring changes neither autocatalyst leak nor food uptake (`20261025T1656-c19`); the nematic fuel ring is matched by fuel slowed only outside the rods (`20261025T1713-c15-fuelcell-outslow-twin`); stiffer or more aligned nematic droplets do not swim (`20261025T1700-c15`).
- **Kernel-world bodies do not divide by themselves** (established negatives): a lone neural-field comet stays one body or grows into a fragmenting wave (`20261025T1713-c20`); r-two56 cogs have no fission state, and lcn worms are unbounded fronts broken only by collisions (`20261025T1621`, `20261025T1518`).

## What changed in the reading

1. **E by construction is the norm, so forks no longer add score.** Every metabolism claim decided today (b42 cells, r-two56 cogs, lcn bodies, Flow-Lenia daughters, neural comets) builds body matter, or all activity, from the resource. Local forks were useful because they showed per-body dependence and its timescale (cogs collapse after a ~10% deficit; Flow-Lenia daughters leak their matter to neighbours). C:metabolic-cell needs bodies whose matter is *not* made from the resource. *Provisional:* c23's catalysis-induced condensates (`20261025T1845-c23`, a fresh-seed review replicates) conserve their enzyme exactly and still dissolve within ~100 t when the fuel stops regrowing.
2. **A wall must beat slowed transport, not just its own ablation.** Four rings or shells in four classes (lattice chem, pcell M, nematic fuel ring, and the shell-gated r-two56 cog, *submitted* `20261025T1703-c18`) do nothing that a slower medium does not. A slow-exterior twin is now the minimum control for W. One *submitted* fork: a set-point shell that feeds back on Flow-Lenia matter makes gliders 10-85% faster (`20261025T1748-c18`, IBMED provisional), so a layer can change behaviour, but it does not stop fusion (`20261025T1727-c18`).
3. **Division comes from mass-conserving or phase-separating bodies, not from kernel fixed points.** In Lenia, neural fields and lattice chemistry, bounded bodies are stable fixed points and growth is an unbounded front. The dividers that pass are Flow-Lenia foragers, phase-field and particle cells, and evoloop.

## Most promising next work

- **C:metabolic-cell, not by construction:** give CIPS droplets (or Flow-Lenia, whose matter is conserved) a division route and a boundary while the resource only *drives* them, not builds them. One concrete form: Flow-Lenia with no matter source, where local food sets the growth-field gain, so bodies hold together only while they eat. Then use a moving starve-one-daughter fork (c18's `dfork.py`).
- **A wall with a job slowed transport cannot do:** active pumping (a layer that moves a species up its gradient), or selectivity between two species with equal diffusivity.
- **Audits before scoring:** write down every field's zero-flux state and the sign of each source term, as in the FCH decay audit.
