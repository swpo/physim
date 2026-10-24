# Autopoiesis, sprint 1 report

## 1. Headline

**Phase protocell: a continuum autopoietic cell whose membrane is an Allen-Cahn domain wall,
held up by links that its own catalyst makes.** Because the wall is a phase boundary, it is
always closed. From smoothed noise, walled cells with a catalyst core and a link-rich shell
self-assemble. They repair a 36% wound, grow, divide by central starvation through ≥ 3-6
generations, and fill the domain (3 seeds; behaviour unchanged at dt/2 and 2x resolution).
Every link of the production loop is necessary: removing mobility gating, removing the
link→phase tilt, or removing the phase each kills all individuals. With two heritable catalyst
kinds and in-run point mutation, a faster mutant lineage sweeps the population in 3/3 seeds. A
link-less "selfish" mutant is purged when its advantage is small (c2 = 0.24). When its advantage
is larger (c2 ≥ 0.27) it drives the population extinct, a parasite threshold.

## 2. Claims

| world | claimed | strongest evidence | known weaknesses |
|---|---|---|---|
| `phase_protocell_noise` | **L6[L3]** (+L4a, L4c) | `packs/phase_protocell_noise/seed{0,1,2}`: from noise, 22-24 transient blobs at t=350 → 11-19 survivors at t=650 → 42-43 cells by t=8000; 28-32 persistent splits, generation 3-4; sheet t=350→8000 | The "membrane" channel is 4φ(1-φ) of the order parameter: a real domain wall with line tension, but it is not a separate molecule. The noise IC has K everywhere and φ noise; the phase nucleates from noise peaks. |
| `phase_protocell` | L6[L3], L4a, L4c | `packs/phase_protocell/seed{0,1,2}` (4 planted blobs, no planted walls): 36-43 cells, 22-33 persistent splits, gen 2-5. Structure: core K 0.88 / S 0.08, rim wall 0.73 with L enriched just inside the wall, outside S 0.44 (FACTS, `screens/pp6_chan.png`). Damage: `packs/phase_protocell_damage` and `screens/damage_strip.png`: a disk removes the wall arc and 36% of a cell at t=1500; both pieces reseal within 100-250 time units and keep dividing; the crop matches the control by t≈2800 | Division is "multiple fission" of a starving disk (horseshoe → 3-4 pieces), close in spirit to Gray-Scott mitosis with a wall around it. Metabolism ablation is via feed only (F ≤ 0.005 → extinction). No motility. |
| `phase_kinds` | **L7[L3] Weak** | `packs/phase_kinds/seed{0,1,2}` + `kinds.png`: K2 (c2 = 0.3 vs 0.2, same link output) arises by ~10 point mutations, its cells breed true and replace all K1 cells (K1 49 → 0, K2 → 28-33) in 3/3 seeds. 47-48 persistent splits, gen 5-6 | Only 2 kinds, and mutation is one-way K1→K2 by a stochastic rule written in. Neutral control (c2 = c1, same mutation rate): no K2 cell ever forms and K1 stays at 52 cells to t=32000 (seed 0; seeds 1 and 2 in NOTEBOOK). No-mutation baseline: 52 cells, stable to t=32000. |
| `phase_kinds_parasite` | L7 (group-level selection), Weak | `packs/phase_kinds_parasite/seed{0,1,2}`: link-less K2 (c2 = 0.3) → infected cells turn pale and die, and the whole population is extinct by t≈25000 in 3/3 seeds. Screens: c2 = 0.24 purged in 3/3 seeds (45-51 cells at t=16-32k); c2 = 0.27 collapses (seed 0 extinct, seed 1 down to 3 cells at t=32k) | The mechanism of collateral death is a hypothesis: infected cells hog substrate before dying. K1 cells fall faster than mutation alone can explain. The no-mutation baseline is stable (52 cells to t=32000), so the decline is caused by K2. |
| `scl_lattice` | L3 Weak (planted), L4a **Contradicted** for large wounds | `packs/scl_lattice/seed{0,1,2}`: a planted 9-px link ring around one catalyst is maintained for 3000 sweeps with continual link decay and splice repair. `packs/scl_lattice_damage` + `screens/scl_damage_strip.png`: after a 30% wound the ring stays open (C-shape) to the end | The ring is planted. Closure holds only 67-76% of the time, and the catalyst sometimes escapes. |

## 3. Mechanisms learned (with ablations)

1. **Topological closure from a phase wall.** In the lattice and polymer-field versions, membranes
   failed by opening: gaps whose ends drift apart, or catalyst and links leaking out. Making the
   boundary the level set of an order parameter removes that failure mode, because a domain wall
   cannot have a hole. Repair is then automatic: curvature flow plus tilt reseal the wound. This
   operator transplants to any RD or Lenia chemistry: add φ, gate the mobilities by φ², and tilt
   φ's double well by an internal product.
2. **Autopoietic tilt (operational closure).**
   `dφ = Dp∇²φ + rφ(1-φ)(φ - ½ + a(L - θ))`: the inside phase survives only where the cell's own
   links exceed θ. Ablation a = 0: every domain shrinks by curvature and dies by t≈350
   (`packs/phase_protocell_notilt`).
3. **Gated mobility keeps the products in.** K and L move with D·φ². Ablations: gate = 0 → all dead
   by t≈350 (`packs/phase_protocell_nogate`); gating L but not K → dead (screen); φ ≡ 1 (no phase)
   → a uniform catalyst sea, no individuals.
4. **Division by central starvation.** Large cells deplete S at the centre, L falls below θ there,
   the tilt flips and the wall pinches through. This predicts that cell size grows with feed F.
   Mean area per cell at t=8000 was 71 / 66 / 88 / 405 px for F = 0.0054 / 0.006 / 0.0066 /
   0.008, which roughly holds. Window: F < 0.005 → extinction, F ≥ 0.01 → sea.
5. **Within-cell vs between-cell selection.** A faster catalyst with equal link output sweeps. A
   faster catalyst that makes no links kills its host (no tilt), so selection acts on cells. The
   population survives only below a parasite-advantage threshold (purged at 0.24, collapse at
   ≥ 0.27).
6. **Numerics:** explicit Euler with consumption capped at 0.5 S per step. dt = 0.5 gives cell
   counts identical to dt = 1 to 3 digits (10/24/36/47 at t = 2k/4k/6k/8k). The 2x-resolution run
   (256², all D x4, dt 0.25) gives 8/10/22/35/49 against 8/10/24/36/47.

## 4. Negative results

- Lattice SCL (numba, McMullin rules + splice): closure fraction is 0.2-0.8 across 24 settings and
  2 seeds. A high single-end extension rate grows internal spurs instead of closing gaps. Separate
  free-link decay did not help.
- scl_divide: flexible bonded links (bond-fluctuation moves), insertion and reconnection fission.
  Moves into holes made the membrane drift **inward**, because production creates holes inside.
  Moves into S let gap ends separate and never re-splice. Reconnection at p = 0.5 shattered cells
  into vesicles. No robust regime found in 16 configurations.
- Gated polymer-field protocell (M forms where |∇L| is large): cells freeze when K is gated and
  die when it is not. Gray-Scott kinetics also die inside any barrier (14 configurations).
- Logistic phase protocell from dense noise: the whole domain becomes one sea, then crashes
  synchronously to extinction (6 configurations). Only sparse nuclei (φ noise mean 0) work.
- labkit: the `--damage` disk sits at the centroid of the largest component, so for walled cells
  it only hits the interior. For a cell wrapped over the periodic edge the mask is misplaced. My
  `damage()` hooks re-find the cell and cut its wall. Suggest an option for a rim-centred disk.

## 5. Next sprint

1. **Make the wall a molecule:** an amphiphile field produced by K that lowers the wall energy, so
   that wall tension depends on supply. Test pearling and budding as division (LITERATURE
   §2.5.5), and get an L3 claim that does not rest on 4φ(1-φ).
2. **Continuous heritable traits:** trait-carrying catalyst fields (c, b) with mutation noise, to
   measure trait trajectories and the cooperation-selfishness balance. Aims at L7 Supported and a
   first L8 probe.
3. **Self-propulsion:** asymmetric link production (a polar cell), in the style of active
   emulsions or Marangoni flow, so walled cells swim (L4b).
4. **Lattice SCL:** add the chain-based bond inhibition that LITERATURE §2.7.1 says is essential,
   and retest repair, as a cheap check that the classic model can reach L4a.

Needs: nothing beyond the current labkit. A rim-centred damage option would help other
membrane threads.
