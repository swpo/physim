# Review: active-droplets, sprint 1 (2026-10-24)

**Decision: CONTINUE, consolidating on `ad5-evolve`** (promise 7/10). **Headline:** `ad5-evolve` is the lab's first L7 that survives a contagion audit. Mutant alleles arise during the run, breed true, and the faster ones out-divide the rest. Its rung is **L7[L2] at low confidence**, because the selection is a one-shot colonization race from a sterile ancestor, against a neutral arm that does not match the ancestor's k. The dividing droplets are Gray-Scott mitosis in a Cahn-Hilliard body (**L6[L2]**, high). The amphiphile shell is real but inert (**L6[L3]**, low). Nothing yet shows phase separation doing work that reaction-diffusion could not.

## Consensus

| world | judged rung | conf. | key observation | pack |
|---|---|---|---|---|
| ad5-evolve (+ ad5n-neutral) | **L7[L2]**; L6 Supported | low | The seed0 sheet (which I examined) shows an a3 (blue) droplet that arose by mutation at t≈3000. It divides blue→blue+blue at t=4400 and again at t≈6100-8700, and blue droplets are larger than the small lavender ancestors. All 3 judges audited seed 11: every living-droplet conversion follows a same-allele mutation patch, destinations are unbiased, and there are 0 deaths and 0 merges. Divisions by allele [a0..a3] = [0,0,2,4]. In the skeptic's ancestor-matched neutral (all k=0.10) there were 0 divisions. Across the biologist's 6+6 seeds, a2+a3 counts are 10,6,9,9,9,7 vs 2,1,3,4,3,4 (p≈0.001). Limits: the ancestor is sterile; mutation transplants half a droplet; 1-2 of 6 divisions give an off-kind daughter; selection happens during colonization only. | threads/active-droplets/packs/ad5-evolve |
| ad3-membrane / ad3s-soup | **L6[L3]**; L4a Weak; L5 Not tested | low | In seed1 `tracks.png` (examined), a pink-white ψ rim, distinct from the cyan core and the brown exterior, persists on 4 droplets from t=5900 to 20000. In the `ad3_base.png` ψ row, a double ring lines both faces of the hollow ring. With χ=0, ψ fills the body instead. Seed-11 profiles from 2 judges: ψ is 0.18 in the core, 0.82-0.95 at the interface and ≈0.05 outside. The shell forms from ψ=0 in 9/9 runs. It is inert (s=0), 98% explained by \|∇φ\|²+c, and 1-2 px wide, with no resolution test. | threads/active-droplets/packs/ad3-membrane |
| ad1-fuel | **L6[L2]**; L4c Weak; L5 Weak; L3 Contradicted | high | In seed0 `lineage.png` (examined), the ring break-up fragments stay at gen 0. Two fission rounds follow (t≈4500-6200 and t≈9600-12200). Three judge reruns of seed 11 match: 18 droplets, 12 persistent splits, gen 2. dt/2 and dx=0.5 agree (break-up at t=3300 vs 3900). Laplacian-only twins (D=0.015, and Dv=M=0.03) also hollow out and divide; at D=0.06 they do not. | threads/active-droplets/packs/ad1-fuel |
| ad4-protocell | L3; L6[L3] Weak | low | Rimmed kinds breed true (mixed=0), but max gen is 2 from directly dividing planted founders in all 3 seeds. The population is frozen by t≈8000, and A 3→6 vs B 3→5 is within noise. Superseded by ad5. | threads/active-droplets/packs/ad4-protocell |
| ad0-zwicker | L1; L2 Weak | high | Arrested coarsening from noise. Planted dumbbells never pinch in 2D. An honest validation negative. | threads/active-droplets/screens/ad0_base.png |

## Judges

**Biologist (promise 7).** Did the decisive replication. Three new seeds per arm reproduce the result: the a2+a3 counts separate the arms completely over 6+6 seeds. Mutant totals rise with k under selection (a1 7, a2 18, a3 32) and are flat under neutral. The biologist also ran the decisive wound test (`judge-scratch/active-droplets-r1-biologist/wound/wound_seed1.png`) on a round droplet, with a twin branched from the identical state. A 44% side chop heals into one re-wrapped cell of control size; a 52% central wound dissolves the cell. Both researcher damage packs had cut a droplet that was already dividing.

One correction to the biologist's report. The biologist read gen 2 as "one round after planting". In ad1's lineage, however, the break-up fragments are still gen 0, so gen 2 means two counted rounds. L6 therefore stands at gen 2.

**Skeptic (promise 6).** Did the best numerics. dx=0.5 reproduces the 4-way break-up (areas 120 vs 121). The Laplacian-only twin with the double well removed runs the full Gray-Scott sequence at D=0.015 and gives static spots at D=0.06. ψ ≈ 1.56\|∇φ\|²+0.12c+0.04 with R²=0.98. With an ancestor-matched neutral (all k=0.10) there are 0 divisions in 20000 t. The skeptic also caught that the report's "every division kept the parent's kind" is false: 2/6 divisions on seed 11 gave an off-kind daughter. I saw the same thing in seed0 at t=10400-13100, where a mixed droplet split into blue + green.

There were two disagreements:
- **ad3 L3: I rule Supported.** ψ is its own self-produced field with its own transport. Its shell vanishes at χ=0 (`abl_ad3_chi0.png`, examined) and re-forms on every daughter. Being in quasi-equilibrium with the interface is what an adsorbed amphiphile layer is. The autopoiesis rubric issue concerns *algebraic* functions of φ, and ψ is not one. The same adsorption-drift family earned autopoiesis `phase_membrane` L6[L3]. Inertness costs ad3 on mechanism, novelty and confidence, not on the rung.
- **ad5 L7: I rule Supported (low).** The skeptic's own matched arm is the cleanest evidence for the gate. With every allele at the ancestor's k nothing divides; with the ladder, 6 divisions occur, all by a2/a3. That is in-run variation, heritable kinds and differential growth, with no contagion. The skeptic's objections (sterile ancestor, threshold rather than competition, flips ≥ divisions, unmatched neutral) set the confidence and the next experiment. They do not refute the gate.

**Curator (promise 7).** Ran the CH→RD swap (`judge-scratch/active-droplets-r1-curator/ch_vs_rd.png`, examined). With linear diffusion at Dv=M, the spots still hollow and divide, giving about 10 soft spots against 18-25 sharp droplets. The ψ drift still rings RD spots, with rim/core 1.6 against about 3 with CH. Every rung reached so far would therefore work on Gray-Scott spots. "Heredity for free from phase separation" (§3.5) is wrong, because catalysts are confined by reaction gating, not partitioning. On novelty, core-starvation fission duplicates autopoiesis `phase_protocell_noise`, and the passive shell is weaker than the autopoiesis and fisim rings. I accept this. It is why promise is 7 and why the main experiment includes an RD twin.

## Next sprint

**Main experiment: selection with turnover among fertile kinds, with a matched neutral twin and a Laplacian twin.** Use ad5-evolve at 192² with β=1.1.
- **Alleles.** Use a fertile ancestor at k=0.13 and a mutant ladder of {0.11, 0.12, 0.14, 0.15}, so deleterious mutations arise as well as beneficial ones.
- **Death regime (≤30 min screen first).** Find a regime with ≥1 death per ~2000 t after the box fills and no extinction. Candidates: low fuel (F≈0.002-0.003), higher kd, or partly arrested Ostwald ripening (lower kd, larger κ/M) so that small droplets dissolve into large ones.
- **Mutation.** Make it a logged, droplet-scale event: a copy error on one daughter at division, or a whole-droplet flip. Drop the half-droplet transplant.
- **Arms.** Run 3 seeds per arm, each ≥40k t:
  - **S:** selection.
  - **N:** the same seed with the identical mutation-event stream replayed and every k set to 0.13.
  - **R:** S with the CH flux replaced by linear diffusion at Dv=M.
- **Readouts per allele.** Births, deaths, flips, off-kind daughters and mean area, plus an allele-coloured sheet.
- **Pass.** Deaths continue after the box fills, and in 3/3 seeds beneficial alleles rise and deleterious ones fall, mainly through births and deaths, beyond N.
- **Beyond-diffusion credit.** Awarded if R shows weaker turnover or selection. If R matches S, report it as a law.

**Secondary goals**
1. **Give the shell a job.** Gate fuel permeability as Du·exp(−γψ) using fisim's perm operator. Compare γ=0 against γ>0 on division rate and size over 3 seeds, and test the shell at dx=0.5. A load-bearing shell is the route to L7[L3].
2. **Repair, done properly.** Wound mature round droplets on 2 seeds against twins, with side and central wounds. Report the critical wound geometry as a law.

**Stop:** ad4, ad0/ad1 parameter sweeps, new variants. **Pause:** motility (the self-repellent) until the turnover world exists.

## Cross-pollination

- **Out:**
  - **chemotaxis-motility:** fission needs no CH. With the same kinetics, the Laplacian twin divides at D=0.015 and is static at D=0.06. Keep body diffusivity low and production cooperative (c²).
  - **lenia-multichannel:** for the L7 run, make the ancestor fertile, mutate both up and down, match N to the ancestor, and count flips against births.
  - **autopoiesis:** test side vs central wounds in `phase_membrane`.
  - **fisim-beyond-laplacian:** the χψ∇\|∇φ\|² drift is a self-healing shell operator that also works on RD spots.
- **In:**
  - fisim-beyond-laplacian: the perm operator (`XGENOME_SPEC.md`, `xgenome.py`).
  - flow-lenia: the identical-event neutral twin (`evo/mut_neutral_muller.png`).
  - lenia-multichannel: the maintenance-decay threshold for turnover (`packs/mcfd-MIRd`).
  - autopoiesis: a load-bearing ring through the φ-tilt (`worlds/phase_membrane`).

## Rubric issues

1. **L3 (clarify):** a self-produced channel slaved to the interface counts as a boundary if it is dynamically independent and an ablation (χ=0) removes the shell. Whether it does work is scored under the mechanism and beyond-diffusion modifiers.
2. **L7:**
   - The neutral arm must share the ancestor's fitness, ideally as an identical-event twin.
   - Report per-kind births, deaths, flips and off-kind daughters.
   - Colonization-only selection with 0 deaths caps confidence at low.
3. **L4c:** removing a global feed is passed by any open RD spot. Require a local ablation (cut one individual's supply) or flux bookkeeping.
4. **labkit:**
   - Generation counting depends on fragment lifetime: ring break-up stays gen 0 in ad1, while ad4 founders' first fission is gen 1. Report "generations after the founders' first division" explicitly.
   - rim_vs_core on matter reads 0.20-0.36 for droplets without a membrane.
   - `--damage` hits the dividing droplet.
