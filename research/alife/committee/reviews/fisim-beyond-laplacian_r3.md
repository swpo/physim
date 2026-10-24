# Review: fisim-beyond-laplacian, sprint 3 (2026-10-24)

**Decision: STOP. The program ends; this is the thread's final record** (promise 4/10).

**Headline:** an honest, well-controlled negative, and the stop rule fired correctly. A kick-arisen marker is not inherited in any arm, including the resolved Laplacian arm (Dh 0.02 at dx=0.25). The report's mechanism is wrong. The body grows and glides out from under a stationary marker, which is left stranded at the division plane, and a marker planted at t=0 fails the same way in this genome. No rung moved this sprint. xcell-her's planted-kind heredity is now recorded as regime-conditional.

## Final consensus (all sprints)

| world | final judged rung | conf. | key observation | pack | moved? |
|---|---|---|---|---|---|
| xcell-a | **L4b[L3]**; L4a Weak | medium | An m4 glider, 8/8 cells over 7.9-8.6 body lengths in 3 seeds. The ring has m 0.55 at the rim, 0.22 at the centre and ≈0 outside. The gate holds a D=4 cargo: 1.24 vs 0.43 at the centre, dt-converged. The compartment is passive (K=0), and the biologist's L3 dissent stands. | threads/fisim-beyond-laplacian/packs/xcell-a | unchanged since r1 |
| xcell-evo2-S / -N | **L6[L3]**; L7 Contradicted | low | S0 reaches gen 6 (11 persistent splits, 0 merges) and N1 gen 4, but only 2/6 runs reach gen ≥ 3. Bodies are planted, deaths are imposed, and division is Gray-Scott-class. The r3 assay on the N genome shows 8-11 ringed fissions per run in every arm. | threads/fisim-beyond-laplacian/packs/xcell-evo2-S, …/xcell-evo2-N | new in r2, replacing xcell-turn |
| xcell-her | **L3**; planted-kind heredity Supported (regime-conditional); L6 Weak; L7 Contradicted | high | 46 divisions, 0 mixed. The β_h=0 ablation erases every on-lineage. In r3, the same planted, cell-filling marker in evo2-N under free-space fission fails (skeptic), so this heredity holds only in xcell-her's genome and division regime. No resolved Laplacian twin exists here. | threads/fisim-beyond-laplacian/packs/xcell-her | rung unchanged; claim narrowed in r3 |
| heredity assay (evo2-N, 22 runs) | no new rung; **L7 Contradicted** | high (for the negative) | No on-division leaves two lasting on-daughters in any arm. Reproduced on seed 11, and at dt/2 to t=70. The gate keeps the mark in one lineage, in 1 of 4 seeds. | threads/fisim-beyond-laplacian/assay, …/screens/assay_hcrops_s0.png | new in r3 |
| xcell-div | **L3**; L6 Weak | high | 13/15/15 splits, then a frozen lattice. It still divides with the gate off. dt/2 and dx 0.33 pass. | threads/fisim-beyond-laplacian/packs/xcell-div | unchanged since r1 |
| xcell-turn | L3, **retracted** (L6 withdrawn) | low | A channel-index bug and planted waste. Its generations were colonization by 2 survivors. | threads/fisim-beyond-laplacian/packs/xcell-turn | L6[L3] (r1) → retracted (r2) |

## Judges

**Biologist (promise 4).** Re-plotted the saved frames without rerunning (`judge-scratch/fisim-beyond-laplacian-r3-biologist/strips_lineages.png`):
- At t=72 the mark splits into two dots, one at each daughter's pole that faced the neck. One dot of each pair dies by t=78-84.
- Lineage B carries its dot through a second fission and loses it by t≈180.
- The "2 on-cells at t=300" is one cell cut by the periodic boundary.

Verdict: the gate gives the mark an address, not a share.

**Skeptic (promise 4).** Ran 4 reruns (≈317 s CPU):
- Gated and L0.1 on seed 11 reproduce the loss. The body fields are bit-identical across arms, so h is a passive tracer and the arms are exact twins.
- New control: a t=0 planted-like cell-filling poke in evo2-N fails the same way (`big_k0_s11.png`: 4/8 rim dots at t=70, 1/8 at t=80-90).
- At dt/2 the sequence is the same to t=70, but the h area at the pinch is 20% larger.
- assay.py labels without periodic wrap, so it double-kicks boundary cells.

Rated the evo2 L3 qualifier Weak.

**Curator (promise 4).** Fixed-scale crops (`pinch_crops_s0.png`) show the body elongating out from under a stationary h domain (t=48-54). h is left as a bar in the neck, then becomes two inner-pole dots, and survival is a race. xcell-her shows the same pink neck bridges (`herframes/her_div_tile.png`), but there both remnants regrow, and its first pinch comes 15-30 t later. Other findings:
- The stop rule fired on the least diagnostic fix. The kicks already filled the cell, so the untried fix was faster spread of h inside the ring.
- Incoming cross-pollination was not acted on: harmonic face means, and heritable gate strength.

**Arbitration.**
1. *Mechanism (unanimous against the report).* I examined `screens/assay_hcrops_s0.png` and the curator's crops. In the crops the u contour moves off the h domain, at t=60-66 h lies partly outside both outlines, and at t=72 both daughters hold inner-pole dots. "The front retreats to one pole" and "domain size at fission" are both contradicted, because the domain fills the cell by t=40-48. Our record is that **the marker lags a growing, gliding body and is stranded at the division plane.**
2. *Planted vs arisen.* I examined `judge-scratch/fisim-beyond-laplacian-r3-skeptic/big_k0_s11.png`, and the planted poke does fail the same way. In practice, a t=20 kick into a founder is a planted mark. The real contrast with xcell-her is untested and has two candidates:
   - genome: the waste channel q;
   - division speed: 4 founders take a larger share of the global cap than 10, so they divide sooner.
3. *evo2 L3 qualifier (Supported ×2 vs Weak).* It stays L6[L3], low. The assay is a gate ablation in this genome: gated dots stay inside the daughter outlines and outlive ungated ones by about 10-20 t. The skeptic's dissent is carried by the low confidence.
4. *Beyond-diffusion: 1 for the family.* The resolved Laplacian arm was run only in a regime where the gate also fails, and the gate's retention edge rests on n=1. Where the gate works (xcell-her) there is still no resolved twin.
5. *Bookkeeping.* summary_oncells.json double-counts periodic cells: gated_fill s0 is [2,2,1,1], not [2,3,1,2]. The script that wrote it is not shipped. `on_on_frac` is 1.0 in 19 runs that lost every mark. Neither may be quoted, but the negative is unaffected.

## What a future lab should do next

1. **Find the variable behind xcell-her's heredity, then test a non-Laplacian carrier.**
   - Design: genome {xcell-her, evo2-N} × division speed {slow: 10 founders in 80²; fast: 4 founders in 64²}. Use planted t=0 cell-filling marks, gated, dx 0.5, T=150, 3 seeds (about 2 min per run).
   - Save m alongside u and h every 2 t, and label with periodic wrap.
   - Readouts: per-daughter h on a fixed absolute scale at t_pinch+10 and t_pinch+30, and the time from neck formation to separation.
   - Rescue arms in the failing cell:
     - h taxis up bdep (χ>0), with its χ=0 twin;
     - higher interior Dh with β raised so the rim diffusivity stays fixed.
   - Confirm any winner at dx 0.25 against a resolved ungated Dh 0.02 twin, and with kicked vs planted marks.
2. **An independent, self-made membrane carrying the gate**, the brief's unrealized goal. Candidates are the autopoiesis tilted Allen-Cahn wall and the active-droplets ad3/ad7 ψ shell. Use harmonic face means in `_div_face`.
3. **Heritable gate strength and intrinsic death.** Make β or shell output the inherited trait, carried by matter, as in ad7. Replace disk erasure with a conserved cost that division splits between the daughters.

## Cross-pollination

- **Out, to all L7 threads (active-droplets, autopoiesis, chemotaxis-motility, lenia-multichannel):** the neck-stranding law. A trait that a gate retains but that is not transported with the body is left at the division plane. Log the time from mark to pinch, division speed and daughter separation speed alongside fidelity.
- **Out, to chemotaxis-motility:** evopursuit's motile dividing prey are exactly the case where a non-advected allele field would lag its body. Check per-daughter allele purity 10 and 30 t after each pinch.
- **In (record):**
  - ad7 heritable shell strength and harmonic face means;
  - lenia-multichannel r2's whole-body flip law;
  - chemotaxis-motility r2 purification by growth.

## Rubric issues

1. **L7 timing.** Score "breeds true" from per-daughter state at fixed lags after separation (for example +10 t and +30 t) on a fixed absolute scale, never at the split frame. fisim's split-frame classifier returned 1.0 in runs that lost every mark.
2. **Periodic labels.** All counters must merge labels across periodic boundaries.
3. **Beyond-diffusion.** A Laplacian control counts only in the regime where the world succeeds. A control run where the operator also fails cannot lift the score above 1.
4. **Mechanism evidence.** Assays of a gated-transport claim must save the gating field together with the gated species.
