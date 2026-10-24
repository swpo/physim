# Autopoiesis, sprint 3 report (final sprint)

## 1. Headline

**Arm E passes the committee's L7 test: with the horizontal channel sealed, heritable link yield
is selected through births and deaths against an identical-event twin.**

`worlds/membrane_evo*` uses phase_membrane cells from noise with two catalyst kinds that differ
only in link yield b2 (c2 = c1):
- **Sealed channel:** zero catalyst flux on every boundary face (min face gate) and fast decay of
  catalyst outside bodies.
- **Events:** from t=8000, whole-cell kind flips in both directions, whole-cell neutral-tag
  mutations and random disk deaths, all drawn from one state-independent RNG. Every seed
  therefore has an identical-event twin (b2=b).

Over 10 seeds × 32k t per arm at high turnover (38-75 births per run on ~15-20 cells, about
2.5-4 generations), `screens/membrane_evo_selection.png`:
- **Low-yield K2 (0.7b):** K2 biomass share is below the twin in 9/10 seeds (the 10th ties at 0).
  K2 is purged through deaths (1-14 per run) and missing births (0-5).
- **High-yield K2 (1.3b):** above the twin in 9/10 seeds (the 10th ties at 0). It sweeps to
  85-97% of biomass in 8/10, through K2 births (12-45 vs the twin's 0-14).
- **Hygiene:** first acquisitions 1 in 30 runs, conversions ≤ flips in 30/30 (at most 4),
  off-kind daughters 4 in total (all in the up arm). The neutral tag drifts (0.68-1.53) with the
  same mean in all arms (≈1.0).

**dt/2 check** (`runs/evo_dt/`, 2 seeds, a different event realization): high-yield K2 share
0.93/0.80 vs twin 0.64/0.29, K2 births 37/45 vs 6/17. Conversions ≤ flips, at most 1 first
acquisition.

Pure-culture pre-screen: b=0.035 extinct, 0.05 one cell, 0.065 20 cells, 0.08 6 large cells, so
b matters, and the stop rule does not trigger.

## 2. Claims

| world | claimed | strongest evidence | known weaknesses |
|---|---|---|---|
| `membrane_evo` (twin), `membrane_evo_up`, `membrane_evo_down` | **L7[L3]** against the r2 criteria (first acquisitions ≤1 per run; conversions ≤ flips; share departs from the twin through births and deaths in ≥4/5) | `runs/evo_hi/{down,twin,up}_s0..9.json` (per-seed ledger: births and deaths by kind and cause, flips, conversions, first acquisitions, off-kind daughters, counts, biomass, tag). `screens/membrane_evo_selection.png`. Kind-coloured packs (K1 cyan, K2 orange, L magenta, wall green): `packs/membrane_evo_up` (s4: blue → orange sweep), `packs/membrane_evo_twin` (s4), `packs/membrane_evo_down` (s1). Movie `movies/showcase.mp4` | Variation is a flip operator, not a copying error. Flips hit cells by location, so bigger cells are flipped more often (K2→K1 back-flips up to 6 per run in up, seeds 0-4), which works against the observed sweep. The sealed channel needs b=0.065 for viability. Low turnover (`runs/evo/`, ~1 generation) does not resolve selection: up gives fewer but bigger K2 cells than the twin (5/5), with mixed biomass. Birth strips are not separate: sheet and tracks only (tracks #28 shows a whole-cell K1→K2 flip at t≈20250 that keeps its kind). |
| `phase_membrane` mature damage | L4a for mature cells | `packs/phase_membrane_damage_mature/seed{0,1,2}` (labkit mature-compact target; undamaged twins in `packs/phase_membrane_mature_ctl`). Measured loss 30.3/31.7/31.8%. Area back to 1.04x by +50 t (s0) and 1.0x by +350 t (s2), and both later divide (s2 damage.png: wall and ring resealed by t=6250, division at ~7750). s1 regrows to 1.37x, then is lost to a merge or death at +250 t | 2/3 clean |
| `phase_membrane_chi0` (control) | the ring is not load-bearing | `packs/phase_membrane_chi0` (3 seeds): 42-43 cells, 26-32 persistent splits, gen 2-4, the same as phase_protocell_noise | the L3 claim rests on a self-made, inherited ring, not a necessary one |

## 3. Mechanisms learned

1. **Sealing horizontal transfer takes two operators.** A binary gate with an arithmetic face
   mean leaks (0.5 on every boundary face). The min face mean, plus fast decay of stranded
   catalyst, brings conversions from 8-26 per run (membrane_kinds, r2) to ≤ flips (mostly 0).
2. **Equal growth rates remove the takeover amplifier.** With c2=c1, a trace of the other kind
   does not win inside a cell, and first acquisitions vanish (1 in 30 runs).
3. **Link yield acts on the birth-death balance.** Low yield means walls cannot hold, so cells
   die. High yield gives larger cells that recolonize space cleared by deaths and divide more,
   which is why selection shows only with enough turnover (about 1 generation is not enough).
4. **χ=0 control.** Cells live and divide without the adsorbed ring (more splits than with
   it). The ring is a morphological layer that daughters inherit, not a survival requirement.

## 4. Negative results

- Low turnover (p_death 0.003, ~1 generation per run): selection on b2 not resolved.
- The mature-damage target in s1 was lost (merge or death) after regrowth.

## 5. Status

Final sprint. See FINAL.md (thread summary, consensus rungs, showcase caption) and
`movies/showcase.mp4`.
