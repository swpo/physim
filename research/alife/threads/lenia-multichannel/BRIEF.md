# Thread brief: lenia-multichannel

**Family:** Lenia and its continuous-CA relatives (nonlocal ring kernels + growth maps).

**Why this thread.** A nonlocal kernel lets a pattern sense its own body and its
surroundings at a distance, which gives sharp, self-limiting individuals that reaction-
diffusion struggles to produce. Single-channel Lenia already has hundreds of gliders.
Multi-channel Lenia (Chan 2020) has creatures with differentiated parts and reported
self-replicators. What Lenia lacks is metabolism (nothing is consumed), robust membranes
and heredity.

**Start from.** `examples/lenia_orbium/world.py` (validated Orbium), the Lenia section of
`LITERATURE.md`, `labkit.ops.ring_kernel` / `fft_conv` / `growth_gauss`.

**First sprint, suggested.**
1. Build a multi-channel Lenia world (C channels, kernels = (source, target, R, peaks,
   mu, sigma, weight)) and get at least one known multi-channel creature class working.
2. Screen agent-designed families of channel/kernel graphs at 128² from noise. Look for
   creatures where one channel forms a shell around another (L3), creatures that
   regenerate after `--damage` (L4a), and spontaneous self-replication (L6).
3. Add one non-Lenia ingredient that Lenia lacks: a consumed resource channel (metabolism
   and competition), mass conservation, or an obstacle field. Does it produce bounded
   populations and interaction (L5)?

**Mutation ideas.** Asymmetric or anisotropic kernels; kernels acting on gradients;
two-peaked growth maps; channel-specific time scales; resource coupling; hybrid with a
Laplacian term; cross-channel inhibition that defines a membrane.

**Targets.** L3 creatures (shell + core) that persist; L4a regeneration with a control;
L6 replication of L3 creatures. Report what fraction of random graphs give individuals.
