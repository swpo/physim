# active-droplets: sprint 2 report

## 1. Headline

**Membrane thickness evolves toward a predicted optimum.** Dividing droplets make their own amphiphile shell, and the shell gates diffusion: it slows fuel coming in (weak gate) and catalyst leaking out (strong gate). That makes membrane output a heritable trait with an interior fitness optimum.

- **Single-allele landscape (1 seed):** peaks at kp≈0.5 (droplets at t=8000: 4 / 7 / 12 / 11 / 10 / 9 / 6 for kp = 0 / 0.2 / 0.5 / 1 / 1.5 / 2.5 / 4).
- **Mechanism:** each half of the trade-off is removed by its own ablation.
- **Evolution from both sides (3+3 seeds per side, against neutral controls with the same mutation and dilution):**
  - Membrane-less start: the population reaches 23 droplets vs 10 in the neutral control.
  - Thick start: 36 droplets vs 21 in the neutral control. Intermediate alleles hold 25/36 (69%) vs 9/21 (43%) of neutral labels.
- **Caveat from the neutral control:** mutation churn alone redistributes allele labels quickly. The thick ancestor's label falls to 24% even when it is neutral, so ancestor decline is NOT evidence here. The evidence is population size and the intermediate shift.
- **Movie:** `packs/ad7t-thick/seed1/protocells.mp4`. Small red thick-shelled cells are replaced by green and yellow thinner-membrane cells that divide.

Fork recorded in META: fisim-beyond-laplacian's gated diffusion `div(D e^{-βm}∇c)`, applied to the self-made amphiphile shell from ad3.

## 2. Claims

| world | claimed level | strongest evidence | known weaknesses |
|---|---|---|---|
| `ad7-gated` family (`ad7-gated-d4`, `ad7t-thick`, neutral controls `ad7n-neutral-d4`, `ad7tn-neutral`) | **L7[L3], Weak**: heritable *membrane* phenotype under selection | `packs/ad7-gated-d4/alleles.png`, `packs/ad7t-thick/alleles.png` (3 seeds each, t=20000). Membrane-less ancestor: membrane alleles 16/23 vs neutral total 10 droplets. Thick ancestor: kp=4 ancestor falls to 8/36; intermediate kp 0.5 + 1.5 reach 25/36. Neutral thick control (all kp=4): [0,2,2,2], [2,1,3,2], [2,3,1,1] (21 droplets): label churn alone puts the ancestor label at 5/21. Selection vs neutral: intermediate alleles 25/36 vs 9/21; population 36 vs 21. Landscape seed 1: kp 0/0.5/1.5/4 gives 5/12/12/6 droplets (broad peak). Phenotypes visible in single frames (`protocells.png`): kp=0 is a diffuse leaky blob that doesn't divide; kp=0.5 has a thin rim and divides; kp=4 has a thick rim, stays small and doesn't divide. | Mutation and dilution are imposed stochastic events (as in ad5). Populations are small (5-13 droplets per seed). From the thin side, the kp=0.5 vs kp=1.5 optimum is not resolved: alleles 1/2/3 got 7/5/4 of 23 droplets. The mutation rate is high relative to selection (label churn). The signal is modest: 69% vs 43% intermediate. Allele assignment uses argmax over catalyst means. |
| `ad7-gated` (single allele) | L4c + L3: membrane is now **functional** | `screens/ad7_landscape.png` (seed 0; seed 1 agrees: 5/12/12/6). Ablations at t=8000: catalyst gating off (bc=0) at kp=0.5 gives 3 droplets (benefit gone); fuel gating off (bu=0) at kp=4 gives 12 (cost gone). | Ablations use 1 seed. |
| `ad5-evolve` (sprint 1) | L7[L2] (unchanged) | New readable movie: `packs/ad5-evolve/seed0/protocells.mp4`. A mutant appears as half of an ancestral droplet (t=3700), then takes it over. | as before |

## 3. Mechanisms learned

1. **One gating operator gives a two-sided trade-off.** With fuel (small, weakly gated) and catalyst (large, strongly gated) crossing the same shell, more shell means better retention and worse uptake. That is the classic protocell permeability problem, emerging from one term.
   - Prediction confirmed by ablation: no retention gating means the membrane is pure cost; no uptake gating means more membrane is never worse.
   - This is the lab convergence "containment = gated mobility" made heritable: the gate's strength is now genotype-controlled.
2. **Selection needs turnover.** At dil=0.0005, membrane-less ancestors neither divide nor die, so they just persist; the selection signal was weak (ancestor 11/25 vs 9/14 neutral). At dil=0.002, non-dividers get removed and space is re-colonized by dividers.
3. **Division and motility want opposite condensate mobility** (negative, below). Division here needs slow CH mobility (core starvation). Frey-type self-propulsion needs the condensate to be fast compared with substrate diffusion.

## 4. Negative results

- **Self-propulsion, none found:**
  - ad6: Flory-Huggins affinity to fuel, `μ += χ_u u`, χ_u = -1, -3.
  - ad6b: slow self-secreted repellent forked from chemotaxis-motility, `μ += χ_w w`. At χ_w=10 droplets dissolve (the waste is made inside, which raises μ everywhere in the droplet). At χ_w=1, 3 they divide normally.
  - Treadmilling: low Du and low F.
  - Best case was ≤0.8 body lengths (labkit tracking).
- **A screening-metric artifact.** My quick path metric (non-periodic labels) reported "20 body lengths"; it was false.
- **ad7 at low dilution:** weak selection (above).

## 5. Next sprint

1. **Resolve the optimum with bigger populations and a lower mutation rate** (so selection beats label churn).
   - Smaller cells (lower Du), or 192² boxes, with a continuous kp trait (point mutations ±δ) instead of 4 alleles.
   - Measure mean kp(t) from both sides against the landscape peak, and check the prediction that a steeper fuel gate bu moves the optimum to thinner membranes.
2. **Endogenous variation.** Replace imposed mutation patches with copy errors during catalyst replication, at droplet scale.
3. **Motility, if funded.** Let a second component lower the local CH mobility only at the rear, or let an allele control mobility, to test the division/motility conflict directly.
4. **Numerics.** A resolution test (dx=0.5) for ad7.

Tools added: `protocell_movie.py` (readable movies from pack frames), and `allele_plot.py --offset`. No labkit changes.
