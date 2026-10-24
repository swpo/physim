# Thread brief: chemotaxis-motility

**Family:** advective transport: chemotaxis (Keller-Segel family), cross-diffusion,
self-propelled active matter, predator-prey pursuit.

**Why this thread.** Diffusion can only spread matter, while advection carries it as a
body. Chemotaxis and active stresses produce coherent, self-propelled individuals
that move as units, pursue each other and consume each other. These are the
interaction rungs (L4b, L5) that our reaction-diffusion worlds mostly lack, and they come
with natural ecology.

**Start from.** The chemotaxis and active-matter sections of `LITERATURE.md`,
`labkit.ops.upwind_flux_div` for conservative advection. Keller-Segel blows up without
regularization: use volume filling, logistic growth or a nonlocal (finite-sensing-radius)
gradient, and check that the solution stays bounded.

**First sprint, suggested.**
1. Screen 4-6 mechanisms for self-propelled individuals: autochemotactic spots with a
   delayed or degraded signal, chemorepulsive self-trails, phase-separating droplets
   driven by a polar order field (active model B+ or Toner-Tu coupled to Cahn-Hilliard),
   swimmers that consume a resource ahead of them.
2. Two species with pursuit and evasion (predators chemotax up the prey signal, prey
   away from predator signal). Do populations show sustained predator-prey dynamics
   carried by discrete individuals?
3. Add consumption: individuals that need a resource they deplete (metabolism, L4c).

**Mutation ideas.** Nonlocal sensing kernels instead of gradients; saturating response;
cross-diffusion; finite resources with regrowth; signal relays; alignment between
individuals (flocks of blobs).

**Targets.** L4b swimmers with preserved shape; L5 predation or pursuit with population
dynamics; L4c metabolism.
