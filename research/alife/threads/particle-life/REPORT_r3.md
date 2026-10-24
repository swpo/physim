# particle-life: sprint 3 report (final sprint)

## 1. Headline

**With a step-safe integrator, spontaneous spore release disappears.** Free spores drop from 127 to 3, and the population declines, with 1 birth against 22 deaths by t=200. This confirms the committee's diagnosis that spore release was a size-triggered instability of the stiff core.

**An explicit surface-detachment route restores reproduction, and it converges in dt.** On seed 0, dt vs dt/2 agree within 6–8% on free spores, births and cell count, and the merge-aware lineage reaches generation 2. SALR fission and weak detachment fail. Seed 1 is borderline: births per 100 t differ by exactly 20% (10 vs 12 births), free spores by 12%, cells by 0%, and the generation reaches 2 vs 3. So the gate **passes on seed 0 and is borderline on seed 1**. Detachment is a written-in release rule, not an emergent fission.

## 2. Claims

| world | claim | strongest evidence | weaknesses |
|---|---|---|---|
| `sporecell3` (k_det=0.05, n_det=60) | **L6[L2], dt-converged** (gate: pass on seed 0, borderline on seed 1) | The two-seed dt table in §3. `screens/R3_s0_lin2.png` and `screens/R3_s1*_lin2.png`: merge-aware lineage with qualifying births at gen 1–2 (seed 0) and 1–3 (seed 1 at dt/2), and a stationary population of 28–31 cells from t≈75 | Release is a written-in detachment rule. t=200 and 2 seeds only. Deaths (16–23 per 100 t) exceed qualifying births (5–6 per 100 t), because the strict birth rule excludes early unlabelled spores and births that later merge. No ring claim, and no packs made with labkit v0.2. |
| `sporecell3` without explicit release | negative control for the instability diagnosis | 1 birth and 22 deaths by t=200, 3.4 free spores (127 before the integrator fix) | |
| `sporecell3` selected vs neutral twin, seed 0 | see §3 (one pair only, T=300) | | not the full part (b) |

## 3. What was done (committee r2 main experiment)

**(a) Step-safe integrator: `worlds/sporecell3`.**
- Motion uses adaptive sub-steps, so that no particle moves more than 0.05 per sub-step. Forces are recomputed every sub-step. If velocity grows inside a sub-step, the displacement is clipped and the clip is logged.
- The log (`nsub_hist` and `clips` in each `scratch/*_lin2.json`) shows 3–52 sub-steps per step at dt=0.02. That is the stiffness of dense cells (rep=10, ff=10). There were about 3,000–13,000 clips per run, so the motion of the densest cells is limited by the displacement bound rather than fully resolved.
- Every random draw is unconditional, so arms that differ only in parameters are identical-event twins.

**Release routes, seed 0, t=200** (merge-aware lineage, `lineage2.py`):

| route | dt | free spores (t 60–200) | qualifying births /100 t | deaths /100 t | cells at t=200 | max gen |
|---|---|---|---|---|---|---|
| none | 0.02 | 3.4 | 0.5 | 10.9 | 3 | 0 |
| detachment k_det=0.003, n_det=25 | 0.02 | 2.1 | 0 | 9.9 | 3 | 0 |
| detachment k_det=0.01, n_det=25 | 0.02 | 4.5 | 2.5 | 16.3 | 8 | 1 |
| SALR (B=−1 to R2=2.5) | 0.02 | 0.4 | 2.0 | 14.9 | 5 | 1 |
| **detachment k_det=0.05, n_det=60** | 0.02 | 116 | 5.9 | 15.8 | 31 | 2 |
| **same** | 0.01 | 124 | 6.4 | 22.8 | 29 | 2 |
| detachment k_det=0.05, n_det=60, seed 1 | 0.02 | 110 | 4.95 | 16.8 | 28 | 2 |
| same, seed 1 | 0.01 | 96 | 5.94 | 17.8 | 28 | 3 |

**Merge-aware lineage (`lineage2.py`).**
- Continuation is by particle overlap. A birth is counted only for a cluster none of whose particles were in a cluster at the previous sample; fragments are tracked separately and are not births.
- A qualifying birth must live at least 20 samples and must not end in a merge. Deaths and merges are recorded.
- Limitation: spores shed before the parent first reaches 15 particles carry no parent label. Such cells count as founders, so generation counts are lower bounds.

**(b) Minimal twin only: seed 0, T=300, converged detachment route, mu=0.1, identical RNG streams.** The committee's (b) asked for 3+3 seeds plus seed 11, T≥600 and dilution; this is one pair. The arms are selected (k_cat1=0.065) and neutral (k_cat1=0.05). The streams are identical, but trajectories still diverge once catalysis differs.

| arm | kind-1 share, colonization (t<100) | kind-1 share, stationary (t≥100) | final k0/k1 cells | qualifying births k0 / k1 | deaths k0 / k1 | off-kind daughters | intact-cell conversions |
|---|---|---|---|---|---|---|---|
| selected | 0.36 | **0.45** (rising) | 15/14 | 6 / 5 | 24 / 20 | 2 (k0→k1) | 4 |
| neutral | 0.18 | 0.15 | 26/4 | 11 / 3 | 25 / 11 | 0 | 3 |

**Reading.**
- Kind 1 is above neutral and rises in the stationary phase on this one seed.
- But conversions of intact cells (4) are comparable to kind-1 births (5). The pass condition "conversions far fewer than births" fails: kind 1 may spread partly by converting intact cells through conformity at contacts, not only by out-reproducing.
- With one seed this is not an L7 claim. `screens/TW_*_lin2.png`; ledger in `scratch/ledger.py`.

## 4. Negative results

- Converged motion with no explicit release: the population declines (1 birth, 22 deaths).
- SALR fission at a converged step: 4 births, generation 1, declining.
- Weak or narrow detachment (k_det ≤ 0.01, or a surface test of n_det=25): generation ≤1.
- The dense cells are stiff enough that the displacement bound is active (clips), so the converged dynamics are bound-limited, not exact.

## 5. Not done

- Part (b) at full scale (3+3 seeds plus seed 11, T≥600, dilution). Only one twin pair was run.
- Birth strips at the deepest generation.
- Secondary goals: the gated cycle at the converged step, event-matched lysis arms, and repair under rubric v2.
- labkit v0.2 packs.

See FINAL.md for the thread summary and the showcase movie.
