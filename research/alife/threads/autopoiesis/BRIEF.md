# Thread brief: autopoiesis

**Family:** computational autopoiesis: the SCL model (substrate-catalyst-link; Varela,
Maturana and Uribe 1974; McMullin and Varela 1997) and continuous or particle variants,
plus chemoton-inspired spatial models.

**Why this thread.** Autopoiesis is the classic operational definition of a minimal
living individual: a boundary that the individual's own chemistry produces and repairs,
enclosing the chemistry that makes it. That is L3 and L4a by construction. Historically
the membranes were fragile and growth plus division was never achieved robustly. With
modern compute and agent-driven redesign, this is an open target.

**Start from.** The autopoiesis section of `LITERATURE.md`. A vectorized lattice SCL (with
link bonding and decay, catalyst producing links from two substrates, substrate permeating
the membrane) is a good first build. For labkit, `fields()` can return one-hot channel maps
(substrate, catalyst, free link, bonded link). Consider a continuum version too: a link field
whose bonding is an anisotropic or nonlocal aggregation, so membranes become sharp
interfaces.

**First sprint, suggested.**
1. Implement SCL and reproduce a self-repairing membrane around a catalyst; use
   `--damage` against an undamaged control (L3 + L4a).
2. Explore what makes the membrane robust (bond rules, decay rates, permeability) and
   what makes it grow: more catalysts, link inflow, membrane insertion rules.
3. Aim at division: a grown membrane with two catalysts pinching into two cells (L6).

**Mutation ideas.** Bond angle rules; catalyst replication (template copying inside the
membrane); continuous fields with sharp interfaces; particle-based links; competition
between cells for substrate.

**Targets.** L3+L4a self-repairing cells from simple rules; L6 division; a mechanism
others can transplant into field models.
