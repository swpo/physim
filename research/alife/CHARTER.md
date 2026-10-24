# ALife agent lab: charter

**Mission.** Find simulated worlds whose own dynamics produce life-like organization,
and learn which kinds of dynamics make that possible. "Life-like" is measured by the
[ladder in RUBRIC.md](RUBRIC.md): individuals, then bounded and differentiated individuals,
then autonomy (self-repair, self-propulsion, metabolism), interaction, reproduction,
heredity with selection, and open-endedness.

The existing PhySim worlds are reaction-diffusion fields: a Laplacian plus local nonlinear
couplings. Their boundaries are soft and containment is hard to get. This lab explicitly
explores **beyond diffusion**: nonlocal kernels (Lenia), mass-conserving flows
(Flow-Lenia), particles (Particle Lenia, particle life), sharp interfaces from
phase separation (Cahn-Hilliard, active emulsions), advection and chemotaxis, membranes
and autopoiesis, and hybrids. Diffusion stays allowed; it is just not the only tool.

## How the lab is organized

- **Researchers** each own a *thread* (a family of dynamics) and work independently on
  their own git branch. You are the mutation operator: change equations, operators,
  couplings, conservation laws and representations, not only parameters. Every
  candidate is a single forkable `world.py` that names its parent and its mutation.
- **Evidence packs** (`python -m labkit.run`) are the common currency. Everyone reads
  the same contact sheets, track biographies, lineage charts and fact sheets.
- **The Program Committee** (the central session) acts as peer review and funding
  agency. Three judges with different lenses score each sprint report against the
  rubric; a director decides continue / pivot / merge / stop, points out what other
  threads found, and publishes a lab leaderboard (`committee/LEADERBOARD.md`).
  Reviews arrive as messages in your session and as files on the main lab branch.

## Norms

1. **Science first.** Spend most of your effort running simulations and looking at them.
   No hash-pinned protocols, frozen configuration documents or provenance ledgers: a
   world file + seed + command line is the provenance. A sprint that only improves tooling
   is a failed sprint.
2. **Breadth before polish.** Screen many mechanisms cheaply (64² to 128², short runs, a
   quick look at a few frames), then promote the best few to full evidence packs
   (128² to 256², 3 seeds). 30 quick screens beat 3 careful runs.
3. **Look at the pictures.** Metrics are screens and can be fooled. Open your sheet.png
   and tracks.png before you claim anything.
4. **Honesty.** Show whole runs and several seeds, not best frames. Say when the
   initial condition plants the structure. Negative results are deliverables:
   record them in a line or two each, because they guide other threads.
5. **Mechanism.** For anything interesting, say *why* it works and which operator is
   responsible (an ablation is the best evidence). Mechanisms are what transfer.
6. **Compute etiquette.** Containers have 4 cores. Keep a single run under ~5 minutes;
   vectorize; use `labkit.ops` FFT helpers (2 threads each). If you use subagents, run
   at most 2 simulations at once.
7. **Shared code.** Do not change `labkit/` for thread-specific needs; copy helpers into
   your world file. Fix genuine labkit bugs in a separate small commit and say so in
   your report.

## Sprint deliverables (in `threads/<thread>/`)

- `NOTEBOOK.md`: append-only log. One entry per idea tried: what you changed, what
  happened, a link to the pack or screen image. Negative results included.
- `worlds/<world_id>/world.py`: every candidate you want anyone to see. `META.parent`
  and `META.mutation` record the lineage, including forks from other threads.
- `packs/<world_id>/`: evidence packs. Commit everything except `frames.npz`
  (git-ignored). Keep each pack under ~2 MB. Use `--seeds 0 1 2` for promoted worlds.
- `screens/`: optional quick-look images from sweeps (small PNGs only).
- `REPORT_r<N>.md` at the end of sprint N, at most about 1.5 pages:
  1. Headline: the single most interesting thing you found.
  2. Claims table: world | claimed ladder level | strongest evidence (pack path,
     time) | weaknesses you know about.
  3. Mechanisms learned, with ablations.
  4. Negative results.
  5. Plan for the next sprint and what you would need.
- Commit and push about every 30-45 minutes and at the end of the sprint, so
  the committee can follow progress.

## Getting started

```sh
cd research/alife && ./setup.sh            # creates .labenv (about a minute)
export PATH=$PWD/.labenv/bin:$PATH
python -m labkit.run examples/lenia_orbium/world.py --out scratch/orbium --frames 150
```

Read `labkit/world.py` for the world contract, `LITERATURE.md` for equations and
reference parameters, and `examples/packs/` for calibrated control packs: Orbium
(motile individuals), Gray-Scott mitosis (replication without structure), Particle Lenia
(one organized particle cell) and smoothed noise (nothing).
