# lenia-multichannel: final summary (sprints 1-3)

Thread: multi-channel Lenia (nonlocal ring kernels and growth maps, Chan 2020) plus ingredients Lenia
lacks: a consumed food field, maintenance cost and heritable labels. All worlds are in `worlds/`, packs
in `packs/`, the log is in `NOTEBOOK.md`, reports are `REPORT_r1..r3.md`.

## Best worlds (committee consensus rungs, LEADERBOARD after r2)

| world | rung | what it is | main caveat |
|---|---|---|---|
| `mcf-MIRd` | **L6[L2]+L4c**, high | Chan's planted MIRd+ replicator; matter can only be built from a regrowing, diffusing food field. Colony fronts eat into food. Norefill is extinct 3/3 vs 11-16 survivors with refill | Replication is Chan's. L5 Weak |
| `mcfd-MIRd` | **L6[L2]+L4c+L5**, medium | the same plus maintenance decay 0.03: intermittent boom-bust with fission after troughs. Decay 0/0.01/0.03 gives dormant / static fed / boom-bust | Not a regular cycle; damped at 192²; dt/2 extinct in 1/2 |
| `mcf-fastcell` | **L4b[L3]+L4c**, medium | Chan's shelled glider (A0 shell at r 14-22, empty inside r<8) carving food wakes; dies without refill | Planted; no dt/R test |
| `r-two56` | **L3**, high | one of 2/420 random 2-channel rules: shelled cells (white centre, cyan core, orange cog shell) form from noise and persist; survive dt/2 and R=15-20 | Static fixed points with no turnover. L4a Contradicted (core damage kills) |
| `mca-MIRd` (+ branch test) | L6[L2]; L7 Not tested (r2), **L7[L2] candidate (r3)** | discrete majority-inherited alleles; with whole-body flips a 15%-yield allele spreads from one cell to 40-72% of mass in 10/12 paired branches vs neutral drift | Mutation imposed once per run; full S/N rerun with mutation arising not done; contact zones leak |

## Mechanisms that worked (with the ablation that shows it)

1. **A membrane as a nonlocal distance set point** (r-two56). The shell channel grows only where the
   ring-sensed core density hits a set point (kernel k4). That is a band at a fixed distance from the
   core. Removing k4 gives an orange sea; removing shell→core (k5) or making it constant kills the
   core (mutual dependence); removing the narrow core self-kernel k0 gives endless bilayer worms.
   The constant-k5 test is a cheap check of whether a "second channel" does any work: it does for
   r-two56, and does not for the C-glider r-two-s1-60.
2. **Build-from-food metabolism.** Positive growth is capped by local food (yield Y) and decay
   dissipates. It leaves creature dynamics unchanged wherever food is plentiful, so it can be bolted
   onto any Lenia world without retuning. Gating growth by food (G×F) destroys Chan creatures
   instead (negative). No-refill ablations kill gliders and replicators.
3. **Free dormancy and the turnover law.** A static or confluent Lenia tissue has zero matter
   turnover, so it eats nothing and stops selection. Maintenance decay sets the regime:
   0 gives a dormant lattice, 0.01 a static fed lattice, 0.03 boom-bust with fission after troughs.
   Selection acts only where there is turnover: planted kinds froze at colonization frequencies in
   a lattice (H3), and were sorted by yield in the boom-bust regime (H4).
4. **Heredity by growth.** In Lenia matter is built, not moved. Labels are inherited if built
   matter copies the label of the matter that built it (kernel-weighted majority for discrete
   alleles). Mutations must act on whole bodies: partial flips erode from the cell's own periphery
   (committee skeptic; REPORT_r3).

## What failed

- Spontaneous replicators from random graphs: 0/150. Random 15-kernel graphs are 72% dead.
- Repair: r-two56 regrows 10-20% shell cuts, but any core damage kills.
- Adaptive selection on yield: beneficial mutations push the colony into the static lattice and
  turnover stops (3/3 runs). Not yet separated from the Jensen effect.
- Continuous traits blend at contacts. The first discrete-allele operator hit halo dots.

## What transfers to PhySim

- **Nonlocal set-point membranes:** a second field that grows where a ring-convolved first field
  equals m gives a boundary at a fixed distance, which reaction-diffusion cannot do with one length.
- **Build-from-food plus maintenance decay** as a drop-in metabolism with three measurable regimes
  (dormant, fed-static, boom-bust): a good hidden law for a discovery agent.
- **Turnover as a precondition for selection**, which should be measured before any heredity claim.

## What a next lab should try

1. The whole-body allele test (REPORT_r3) at ≥5 seeds per arm with a per-kind ledger, in the
   boom-bust regime at ≥256², so drift (1/N) is small enough to see s=0.15.
2. Put r-two56 cells on food with decay (spontaneous L3 that must eat), and look for fission
   by weakening the size limiter while food is scarce.
3. Penalize jamming (crowding-dependent decay) so that efficiency cannot switch off turnover.

## Showcase movie

`movies/showcase.mp4`: mcfd-MIRd, seed 2, 128² torus, t = 0-1400 (14000 steps,
every 4 t), full grid with fixed colour scales: A0 cyan, A1 orange, A2 magenta, each on [0, 1]; the
regrowing food field is the green background (black = eaten). One planted MIRd+ cell (Chan's
replicator: white core, orange cap, dotted magenta halo) divides into a colony that eats into the
food. The food crashes, most cells starve, and the survivors divide again into the regrown food:
intermittent boom-bust driven by the build-from-food metabolism with maintenance decay 0.03
(L6[L2]+L4c+L5, committee r1). The label gives time and the number of cells (A0 cores).
