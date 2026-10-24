# Thread brief: particle-life

**Family:** particle systems: Particle Lenia (energy-based, Mordvintsev et al. 2022)
and multi-type asymmetric "particle life".

**Why this thread.** Particles give conserved matter, crisp identity and natural
membranes. The reference Particle Lenia run (see `examples/packs/particle_lenia`) already
self-organizes into a ring boundary with spokes and an inner core: one organized cell.
Multi-type asymmetric interactions break symmetry, producing motile cells, chasing and
predation, which field models struggle to get.

**Start from.** `examples/particle_lenia/world.py` (validated N=200 numpy port), the
particle section of `LITERATURE.md`. For N in the thousands, use a periodic box with
cKDTree neighbour queries or numba cell lists. Field worlds measure a raster;
rasterize particle density in `fields()` so labkit can track cells. Add a type column
to `particles()` so sheets colour by type.

**First sprint, suggested.**
1. Periodic multi-cell Particle Lenia (several hundred to a few thousand particles): do
   several cells form, persist and interact? What sets the cell size?
2. Two or three particle types with type-pair kernel parameters: can one type form a
   membrane around another (L3)? Can asymmetry make cells swim (L4b)?
3. Particle chemistry: types that convert based on local environment (differentiation),
   or creation from and decay to a resource pool, so cells can grow. Do grown cells
   divide (L6)?

**Mutation ideas.** Type-dependent kernels; asymmetric (non-reciprocal) forces;
alignment/velocity terms; bonds that form and break; resource particles; types that
change by majority vote of neighbours; local energy budgets.

**Targets.** L3 membrane-bounded multi-type cells; L4b swimmers; L5 predation or
binding; L6 growth-and-division cycles.
