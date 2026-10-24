# Autopoiesis, sprint 3 report (final sprint)

## 1. Headline

**With the horizontal channel sealed, heritable link yield is selected through births and deaths,
and turnover sets the sign.** Arm E (`worlds/membrane_evo*`) uses phase_membrane cells from noise
with two catalyst kinds that differ only in link yield b2. Catalyst flux is zero on every
boundary face (min face gate), and catalyst decays fast outside bodies. Mutations are whole-cell
flips in both directions, alongside a co-mutated neutral tag and random disk deaths. All events
come from one state-independent RNG, so each seed has an identical-event twin with b2=b.
Over 30 runs × 32k t, first acquisitions are **0/30**, conversions are 0 in 27/30 and never
exceed flips, and off-kind daughters are 0 in 28/30. Results:
- **Low-yield K2 (0.7b) is purged.** It ends extinct in 8/10 seeds against the twin's 0-9 K2
  cells, through K2 deaths (1-8) and missing births (0-3).
- **High-yield K2 (1.3b) depends on turnover.** It loses in a crowded low-turnover world (fewer
  cells than the twin in 5/5) but sweeps in 3/5 seeds when disk deaths are frequent (up to 31
  K2 births, K2:K1 = 15:2).

## 2. Claims

| world | claimed | strongest evidence | known weaknesses |
|---|---|---|---|
| `membrane_evo` (+`_up`, `_down`; identical-event twins) | **L7[L3]**, against the committee's r2 criteria | `runs/evo_hi/*.json`, `runs/evo/*.json` (15+15 runs, ledgers per seed: births, deaths by cause, flips, conversions, first acquisitions, off-kind daughters, counts, biomass, tag). Down arm departs from the twin in 4/5 (high turnover) and 5/5 (low) through deaths and missing births. Packs: `packs/membrane_evo_up` (s4, sweep), `packs/membrane_evo_twin` (s4), `packs/membrane_evo_down` (s1): K1 cyan, K2 orange, L magenta, wall green | About 2-3 replacement generations under high turnover, 1 under low. Flips hit cells by location, so big cells are flipped more often (K2→K1 back-flips 1-6 in the up arm). The up-arm sign depends on turnover (a hypothesis about recolonization is untested). The sealed channel needs b=0.065: b=0.05 leaves 1 cell. Birth strips not made (labkit tracks.png only). |
| `phase_membrane_chi0` (control) | control for phase_membrane L3 | `packs/phase_membrane_chi0` (3 seeds): 42-43 cells, 26-32 persistent splits, gen 2-4. This is the parent noise world, so the ring is not load-bearing | |
| `phase_membrane` mature damage | L4a for mature cells | `packs/phase_membrane_damage_mature/seed{0,1,2}` (new labkit mature-compact target; undamaged twins in `packs/phase_membrane_mature_ctl`). Measured loss 30.3/31.7/31.8%. Area back to 1.04x by +50 t (s0) and 1.0x by +350 t (s2), both later dividing (damage.png s2: resealed wall and ring by t=6250, division at ~7750). s1 regrows to 1.37x, then is lost to a merge or death at +250 t | 2/3 clean recoveries |

## 3. Mechanisms learned

1. **Sealing the channel is two operators, not one.** A face gate built from the arithmetic mean
   still leaks (0.5 on boundary faces). The min face mean, plus fast decay of stranded catalyst,
   brings conversions from 8-26 per run (membrane_kinds, r2) to 0 in 27/30 runs. Transfers to any
   gated-mobility world: use min or harmonic face means for binary gates.
2. **Equal growth rates remove the takeover amplifier.** With c2=c1 a trace of the other kind no
   longer wins inside a cell, so first acquisitions vanish.
3. **The sign of selection on a membrane trait depends on turnover.** Pure-culture pre-screen
   (t=16k): b=0.035 extinct, 0.05 one cell, 0.065 20 cells, 0.08 6 large cells. In a crowd,
   high-yield cells are bigger and divide less. After frequent disk deaths they win, presumably by
   refilling cleared space faster.
4. **χ=0 control and mature damage:** see §3a.

### 3a. phase_membrane χ=0 control and mature damage
With χ=0 (no adsorption) the world is phase_protocell_noise: cells form, divide (26-32
persistent splits vs 9-12 with χ=2) and fill the domain. The ring changes morphology (bigger,
irregular cells with fusions) but life does not depend on it. The L3 claim for phase_membrane
rests on the ring being a self-made, inherited layer, not a load-bearing one.

## 4. Negative results

- Low turnover (p_death 0.003) gives about 1 generation: underpowered (batch 1).
- The high-yield sweep is not robust: 3/5 seeds.

## 5. Status

This is the last sprint. FINAL.md summarizes the thread, and `movies/showcase.mp4` is the
showcase movie.
