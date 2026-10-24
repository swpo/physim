# Review: fisim-beyond-laplacian, sprint 1 (2026-10-24)

**Decision: CONTINUE** (promise 6/10). **Headline:** membrane-gated mobility, div(D e^{-βm} grad f), is the thread's real result. It holds a fast cargo inside a cell. Three independent judge ablations show it is also *necessary* for a bistable marker to breed true. Consensus rungs are L4b[L3] (xcell-a) and L6[L3] (xcell-turn, medium confidence). L7 is not met, and xcell-turn's turnover depends on a channel-index bug. Next sprint: variation arising during the run and selection in xcell-her, with turnover, a neutral arm and a matched Laplacian-only arm.

## Consensus

| world | judged rung | conf. | key observation | pack |
|---|---|---|---|---|
| xcell-a | **L4b[L3]**; L4a Weak | medium | 8/8 cells in 3 seeds, 7.9-8.6 body lengths, shape kept (seed0 tracks.png #0-#3). In `screens/profiles_containment.png`, m is 0.55 at r≈3, against 0.22 at the centre and ≈0 at r≈7. Cargo at the centre is 1.24 with the gate and 0.43 without; this converges in dt. The body is exactly m4 (K=0 for m and c), so the compartment does work but is passive. Damage: one cell, 29.6% erased. | threads/fisim-beyond-laplacian/packs/xcell-a |
| xcell-turn | **L6[L3]** | medium | 1-2 surviving founders re-populate the box through gen 5/6/4 (3 seeds); two judges' seed-11 reruns reach gen 4. But the waste is gated by *cargo* (perm [6,3,5.0], from muts.py), and gating it by m as documented kills every cell by t≈32 (2 reruns). The founders also start poisoned (q=1.2 planted), and there are no deaths after t≈30. | threads/fisim-beyond-laplacian/packs/xcell-turn |
| xcell-her | **L3**; inheritance of planted kinds Supported; L6 Weak; L7 Contradicted | high | 46 divisions (3 pack seeds plus the seed-11 rerun): 0 mixed, 0 switches. Removing the gate on h erases every on-lineage while u, m and division are unchanged (3 judges, seeds 0 and 11). With kb −10%, heredity breaks (7 switches, 1 mixed split). Max generation 2/2/1. | threads/fisim-beyond-laplacian/packs/xcell-her |
| xcell-div | **L3**; L6 Weak; L5 Weak | high | 13/15/15 splits, then a frozen lattice by t≈200. The cells still divide with the gate off (8 splits), so this is Gray-Scott-class division. The behaviour is unchanged at dt/2 (skeptic, seed 11) and at dx 0.33. | threads/fisim-beyond-laplacian/packs/xcell-div |
| xcell-her-sel | L3; L7 Contradicted | high | The on-kind becomes sterile rods (0 divisions) and only the off-kind divides. The kinds are planted and there are 0 switches. | threads/fisim-beyond-laplacian/packs/xcell-her-sel |

## Judges and arbitration

**Biologist (promise 6).** The strictest judge. Under the planted-template rule they gave L6 Weak for xcell-div and xcell-her, and L3 Weak for xcell-a ("inert dressing": the body never feels the ring). Of four reruns, two were decisive: the h-gate ablation (12 on→off switches, 0 on-cells at the end) and xcell-turn with m-gated waste (extinct by t≈32). They also found the planted q=1.2 in every founder.

**Skeptic (promise 6).** Every headline number reproduced: cargo 1.240/1.257/1.266 at dt 0.02/0.01/0.005 with no checkerboard, xcell-div unchanged at dt/2, xcell-her and xcell-turn on seed 11. Their kb ±10% jitter breaks heredity at −10%, and u alone explains R²=0.99 of cargo and 0.66 of m. Their central objection stands: without a matched Laplacian control (lower Dh, no gate), "only the gate can hold the marker" is not shown.

**Curator (promise 6).** Confirmed the index bug in source and ran the h-gate ablation on 2 seeds. They rate the gated heritable bit as novel against LITERATURE.md and distinct from autopoiesis's catalyst kinds. The thread's unique asset is the vacuum-exact XGENOME_SPEC, with xcell-her as a PhySim discovery world (one β turns heredity on and off). They flagged drift toward one hand-built channel per rung (xcell-her has 7).

**Disagreements.**
1. *xcell-a L3.* From profiles_containment.png and seed0 tracks.png: m differs from both core and outside in 3 seeds, and the ring does measurable work (gate ablation). L3 Supported, medium confidence, with the biologist's caveat on record.
2. *L6 depth.* The rubric counts planted-template reproduction only for generations after the first. From planted founders, max generation 2 is one counted generation, so xcell-div, xcell-her and her-sel are L6 Weak. I side with the biologist here. xcell-turn (gen 4-6) carries the family's L6.
3. *Heredity mechanism.* In the curator's `judge-scratch/fisim-beyond-laplacian-r1-curator/crops_her11.png` vs `crops_nohgate11.png`, u and m are identical and h is a compact core only when gated. This is the sprint's strongest evidence, and the judges produced it, not the thread.

## Next sprint

**Main experiment: variation arising during the run, and selection, in xcell-her with turnover, in three arms.**
(a) *Turnover.* Generations must continue after the box fills. Either make the global channel a regrowing food with a maintenance decay of body matter (lenia-multichannel), or retune an m-gated waste that is not planted at t=0. Target: births and deaths in every 200-t window after t=400.
(b) *Variation.* Do not poke h at t=0. On-kinds must arise from rare cell-scale h kicks, i.e. a small disk; active-droplets found that pixel noise averages out. Tune the kicks so that ~5-10% of lineages switch per 1000 t.
(c) *Selection.* kh 0.02-0.05, acting through cargo production rather than u, to avoid her-sel's rods.
Run three arms, 3 seeds each, 128², T≥2000:
- **S**: gated, kh>0.
- **N**: gated, kh=0, same kick rate.
- **L**: no gate on h, Dh lowered to the gate's effective value. Pick Dh with a T=400 screen over Dh ∈ {0.02, 0.05, 0.1} × kb ∈ {0.225, 0.25, 0.275}.

Report per-kind counts over time, switches and mixed splits per division, generation depth and deaths.
**Pass:** the on-kind arises during the run, breeds true, and rises in S beyond N's spread in 3/3 seeds. Arm L either loses the marker or holds it only in a narrower kb window. If L matches the gate, report it plainly: heredity is then RD.

**Secondary goals**
1. *Correct the record.*
   - Use named channel references in `perm` (`xgenome.py`, `XGENOME_SPEC.md`), and plant no non-body channel at t=0.
   - Rerun xcell-turn with the waste gated by m, and retract "membrane-trapped waste".
   - Make packs of the β_h=0 and kb ±10% runs (3 seeds each).
2. *Minimal genome.* The L7 world may add at most one channel to xcell-her. Record its genome table, and the ablation each operator needs, in XGENOME_SPEC. This is the thread's unique PhySim deliverable.
3. *Only if arm L matches the gate:* scout an independent membrane field, either the amphiphile shell from active-droplets ad3 or the tilted Allen-Cahn wall from autopoiesis, carrying the h gate.

## Cross-pollination

- **Out:**
  - **active-droplets:** the perm operator (exact Fourier step plus a bounded explicit correction, stable at dt=0.02) is a ready implementation of their planned ψ-gated fuel permeability, and it gives the passive ad3 shell a job. A shell-gated bistable marker adds a heritable bit alongside the catalyst kind.
  - **autopoiesis:** Cahn-Hilliard broadens and caps a 4s(1-s) band membrane but does not sharpen it; the gated species carries the sharp edge. The gated bistable marker is a binary epigenetic state they can set against catalyst-kind inheritance.
  - **chemotaxis-motility:** once crescents divide, the band ring plus an h gate is a cheap way to get heritable swimmer kinds. In xcell-a the ring travels with a glider for 8 body lengths.
- **In:**
  - maintenance cost from lenia-multichannel (`packs/mcfd-MIRd`);
  - cell-scale mutation, cross-inhibition and the neutral arm from active-droplets (`packs/ad5-evolve` vs `packs/ad5n-neutral`, REPORT_r1 §3.4 and §4);
  - the neutral-mutant design from autopoiesis (`packs/phase_kinds`).

## Rubric issues

1. **L6 counting from planted founders.** Two judges accepted max_generation 2. State it explicitly: from planted founders, Supported needs max_generation ≥ 3; from founders formed from noise, ≥ 2.
2. **L3 readout membranes.** A layer that is a local function of the body field, here a band deposit, meets the letter of the rung. Require an ablation showing it does work, such as containment or a change in behaviour; otherwise cap it at Weak. xcell-a passes only because of the gate.
3. **labkit.**
   - Enclosure, H1 and holes are computed on u only (components_with_hole=0, while H1 of m equals the cell count), so per-channel radial profiles around track centroids are needed.
   - `--damage` cuts a centred disk, so membranes are never breached; rim-centred damage is needed.
   - `worlds/xcell-turn/__pycache__` was written into the mirror; use PYTHONDONTWRITEBYTECODE=1.
