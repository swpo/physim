# Thread brief: fisim-beyond-laplacian

**Family:** the PhySim/blobkit world genome, extended with non-diffusive operators.

**Why this thread.** This thread connects the lab to the benchmark. PhySim worlds use
the blobkit deviation-form genome: cubic activators u_i and linear channels x_c,
each with a Laplacian, and only local couplings. They cannot easily produce sharp boundaries or containment
across boundaries, and one field damping another across a boundary has limited
sharpness. The question is which *minimal* additions to the genome fix this
while keeping its conventions: an exact designated vacuum (u = u0, x = 0 stays a rest
state for any couplings), IMEX-FFT numerics, and interpretable parameters.

**Start from.** `packages/blobkit/blobkit/genome.py` (genome semantics and the IMEX-FFT
stepper), packaged worlds in `packages/blobkit/blobkit/data/worlds/` (`m4`, `bf`, `xv`,
`ds3_014`, ...), `packages/blobkit/README.md`. Write a standalone extended stepper in your
thread (do not modify blobkit) and first check parity with blobkit on a short run of
`m4`. Codex's P7 enclosure world (`p7g2_009`) is only documented by images on branch
`origin/codex/research-update-20261020` (`research/evaluation/2026-10-23.md`); use it as
a visual reference for "enclosure with internal pattern", not as a dependency.

**First sprint, suggested.** Add one operator at a time to an existing world and look
for sharp-bounded individuals and containment:
1. nonlocal kernel couplings (ring-kernel convolution of deviations; vacuum-safe);
2. chemotactic / cross-diffusive flux `div(u_i grad x_c)` (moves an activator as a body);
3. a Cahn-Hilliard term on one channel (sharp interfaces with surface tension);
4. degenerate or density-dependent diffusion (fronts with compact support);
5. advection of all fields by the gradient of one channel.
For each, report what it does to boundary sharpness (profile width), enclosure
persistence, and whether one species can be held inside another's boundary.

**Targets.** L3 individuals with sharp, containing boundaries in a genome that still
works as a PhySim world; a short, implementable spec of the extended genome.
