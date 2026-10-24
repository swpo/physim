# Thread brief: active-droplets

**Family:** phase separation with chemistry: Cahn-Hilliard plus reactions (active
emulsions), multi-phase and amphiphile models.

**Why this thread.** Phase separation produces genuinely sharp interfaces with surface
tension. That gives a real inside and outside, with partition coefficients
controlling what crosses the boundary. Diffusion-only worlds cannot provide this (see
the PhySim boundary problems). Zwicker et al. (2017) showed that chemically active droplets
can suppress Ostwald ripening, grow to a size set by their chemistry, become shape-
unstable and divide: a minimal protocell. Nobody has pushed this to differentiated
interiors, heredity and selection in an open-ended world.

**Start from.** The active-emulsion and Cahn-Hilliard sections of `LITERATURE.md`. Use a
semi-implicit spectral scheme (stiff 4th-order term implicit, nonlinear terms explicit),
`labkit.ops.wavenumbers`. Validate: plain CH coarsens (Ostwald ripening); with reactions,
droplet sizes stabilize; above a critical size, droplets elongate and divide.

**First sprint, suggested.**
1. Reproduce growth and division of active droplets (L6[L2-L3]).
2. Add a second chemical component that partitions into droplets and is produced or
   consumed inside them: differentiated interiors (L3) and metabolism (L4c).
3. Give droplets heritable composition: two catalyst types that partition with the
   droplet and are split at division. Do droplet kinds breed true? Does one outgrow the
   other (L7)?

**Mutation ideas.** Ternary systems with an interfacial (surfactant) component that forms
a membrane-like layer; reactions localized at interfaces; nonlocal (Ohta-Kawasaki)
terms; chemotactic coupling for droplet motility; external fuel gradients.

**Targets.** L6[L3] dividing protocells with differentiated interiors; L7 composition
heredity with selection.
