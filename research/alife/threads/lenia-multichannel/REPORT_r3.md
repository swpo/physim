# lenia-multichannel: Sprint 3 report (final sprint)

## 1. Headline

**With a whole-body mutation operator, a 15%-yield allele that starts in one cell spreads in the
food-limited MIRd+ population, and the neutral label does not. But heredity leaks: only 47% of
allele-1 divisions give two pure daughters, so L7 fails the committee's ≥90% bar.** Branch-point test, committee r2
design: 12 mature isolated cells from 2 neutral-arm runs (192², decay 0.03, mutation off), each
flipped whole and continued for 500 t under S and N from the identical state.
- S beats N in 10/12 paired branch points. In the other 2 the allele was lost in both arms.
- S ends at allele-1 mass fraction 0.40-0.72 with 8-22 pure allele-1 cells, from a 1-12% start.
- N drifts: 0 in 5/12, ≤0.24 in 6/12, 0.56 once.
- The sprint-2 operator (A0 component + 4 px, 50-79% of the body) is lost in 4/6 S and 5/6 N
  branches. Partial flips erode, which explains the sprint-2 negative.
- The division ledger (3 branch points × S/N) shows contact leakage: 47% of allele-1 divisions
  are pure in both arms. Kind conversions without division are rare (0-8 per run).

## 2. Claims

| world | claimed rung | strongest evidence | known weaknesses |
|---|---|---|---|
| `mca-MIRd` (whole-body branch test) | **L7 not met (heredity leaks)**; selection on a whole-body allele Supported as differential spread (S>N 10/12) | `screens/branch_test.png`, `screen_data/branch_rows.json` (12 points × S/N). Division ledger: `screen_data/ledger/*.json` (LEDGER_SUMMARY). Pack with allele colour in the sheet: `packs/mca-MIRd-branch` (3 branch states, S arm) | Mutation is imposed (one flip per run, not arising during the run). The pass criterion asks for the full S/N mutation test with the fixed operator at ≥5 seeds per arm, which was not run (no time). 12 points come from 2 runs. Mixed territories in contact zones |
| `mca-MIRd` old operator | operator failure explained | old: lost 4/6 S, 5/6 N; S>N 2/6 | 6 points, one seed run |
| `rf-two56-mu0.01` / `mu0.03` | L3 from noise survives a build-from-food metabolism; **L4c not shown** | `screens/rf-two56_food_decay.png`: shelled cells form and persist on food with decay 0.01 (7/3/2 cells to t=300); decay 0.03 leaves 1/1/0 | Mean food 0.99: consumption is barely measurable; no no-food ablation |

**LEDGER_SUMMARY** (`tools/division_ledger.py`, territories every 5 t, 3 branch points × S/N):
| branch | arm | allele-1 parent divisions | both daughters pure (p>=0.9) | mixed daughters | allele-1 kind changes without division | allele-0 divisions pure |
|---|---|---|---|---|---|---|
| s0_t6000 | S | 56 | 28 | 28 | 3 | 126/134 |
| s0_t6000 | N | 13 | 6 | 5 | 0 | 125/133 |
| s0_t8000 | S | 76 | 34 | 33 | 4 | 100/120 |
| s0_t8000 | N | 30 | 17 | 7 | 2 | 92/120 |
| s1_t4000 | S | 79 | 37 | 44 | 7 | 55/79 |
| s1_t4000 | N | 14 | 4 | 9 | 1 | 115/128 |

**Strict heredity fails:** allele-1 divisions with both daughters pure are 99/211 (47%) in S and
27/57 (47%) in N, far below the 90% bar. Allele-0 divisions are 77-94% pure. Kind changes of living
cells without division are rare (0-8 per run vs 56-134 divisions), so cells mostly keep their
majority allele while impure. The impurity is contact leakage at the expanding allele-1 front:
daughters born touching the other kind take part of their matter from the neighbour's halo. The
allele spreads under selection, but it does not breed true by the committee's criterion. Leakage is
the decisive result here.

## 3. Mechanisms learned

- **A mutation must replace a whole body, or the body's own periphery erases it.** Inheritance is
  majority-by-mass over the 3-px neighbourhood. A cell whose core is flipped but whose surrounding
  matter is not rebuilds its periphery with the old allele, and the majority then flips back. This is
  the same "multilevel" lesson active-droplets found (a patch must win inside its body first).
- **With whole-body variants, selection on yield is visible within 500 t at 192².** At s=0.15 and
  N≈20 cells the fixation advantage is large enough to beat drift in 10/12 pairs.
- **Contact zones leak.** Mixed territories are 22-35% of allele-bearing samples in S. These are
  cells in contact with the other kind, where majority inheritance over the neighbours' halos
  mixes. Per-body confinement (majority over the cell's own core) is the obvious next fix.

## 4. Negative results

- Old operator: allele lost in 9/12 branch runs.
- r-two56 with decay 0.03: at most 1 cell survives.
- Not done: the Jensen control, the dt/2 and 256² runs of the N arm, and the full S/N mutation rerun
  with the fixed operator.

## 5. If the lab continued

1. Run the full S/N test with the whole-body operator (mutation arising during the run), ≥5 seeds per
   arm at 192-256², with a per-kind birth/death/conversion ledger.
2. **First**, restrict majority inheritance to the cell's own body (territory) to stop contact
   leakage. The committee's stop rule says: try per-body confinement once, then stop L7 on MIRd+.
3. Make r-two56 cells measurably dependent on food: higher yield cost, or a no-food ablation after
   formation.
