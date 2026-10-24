# REPORT r2: fisim-beyond-laplacian

## 0. Corrections to r1 (accepted from the committee; verified in code)

- **xcell-turn retracted.** Its waste was gated by the **cargo** channel (`muts.py:62`,
  `perm [6, 3, β]`), not by the membrane. My world init also dressed every body-driven
  channel, so every founder started with planted waste (q=1.2), cargo and global values. The
  "die-off then 4-6 generations" was poisoned founders, not turnover.
- xcell-div / xcell-her: founders are planted, so the max generation of 2 is **one counted generation**.
- Fixes: `xgenome` `perm`/`taxis` take channel **names** (`["c","m",5]`); world inits plant only the
  body plus its v/w dress (`mkworld --dress`). Blobkit parity is unchanged (3.8e-14).

## 1. Headline

**I ran the committee's selection experiment and it came out negative, for a reason that is
itself a finding. Once nothing is planted, these membrane cells (m4 dissipative solitons)
essentially never die. Three intrinsic turnover routes all froze at 12-21 cells. With imposed
chemostat dilution I got births and deaths in most windows, and new marker kinds arising in
every arm. But divisions run at about 1 per cell per 1000 t, so an arisen on-kind never
divided (0 on→on+on in 6 runs), and S and N are indistinguishable (final on-cells 1/0/2 vs
1/1/0).** No rung is gained this sprint. The r1 overclaims are corrected (§0).

## 2. Claims

| world | claimed level | strongest evidence | known weaknesses |
|---|---|---|---|
| `xcell-evo2-S` / `xcell-evo2-N` | **L7 Contradicted** (variation present, no selection); L6 not supported in-run for arisen kinds | `packs/xcell-evo2-{S,N}/seed{0,1,2}/kinds.json`, `kinds.png`. Kicks give in-run gains S 3/1/2, N 1/2/0. On-cells persist (S0 sheet: white cell t≈790→2000). on→on+on = 0 in every run. Splits/deaths per 200 t window mostly 0-4 each | Turnover is imposed (disk erasure), not intrinsic. Selection is wch=0.15, above the suggested range, and still invisible. Only 1 division per cell per 1000 t |
| `xcell-her` (r1) | L6 Weak (one counted generation); heredity of planted kinds Supported (committee) | r1 packs, unchanged | Planted kinds; kb −10% gives switches (committee) |
| `xcell-a` (r1) | L4b[L3] (committee: medium) | r1 packs | Passive compartment (K=0) |
| `xcell-turn` (r1) | **Retracted** | §0 | Waste gated by cargo and planted |

Heredity-window control (committee arm L, partial): with no gate on h and Dh=0.02, every
planted on-marker is lost by t=100 at kb 0.225, 0.25 and 0.275 (`screens/log.txt`, "Lgrid").
So at that Dh, low diffusion does not replace the gate. Dh 0.05/0.1 were not run.

## 3. Mechanisms learned

- **These membrane cells do not die on their own.** Once planting was removed, none of three
  intrinsic turnover routes produced deaths: unplanted membrane-gated waste (K=0.15), slow
  global food (τ=200-300), and the old cell-pop cap. Populations freeze at 12-21 cells. An
  m4 spot is a robust dissipative soliton. Turnover needs an explicit cost that grows with age or size; a
  concentration-type waste can't provide one, because division doesn't dilute it.
- **Kicks are a clean mutation operator for a bistable marker.** A σ=1.5 h-disk that lands
  inside a body flips it on, and the gate keeps it on. One that lands outside decays,
  because the off-state is favoured off-body (k1=-0.2). Rate 0.02 per time unit gave 4 gains
  among ~11 lineages in 1000 t, all of which persisted.
- **Ungated marker (L arm), Dh=0.02:** every planted on-marker was lost by t=100 at
  kb 0.225/0.25/0.275, while the gated marker holds (r1: 46 divisions, 0 mixed; committee
  re-run: no gate → all on-lineages lost). At this one Dh, the gate is not replaceable by low
  diffusion. Dh 0.05/0.1 were not run (CPU).

- **Why selection was invisible (prediction for the next attempt).** Each S on-cell makes
  ~15% more cargo. But under a global cap, division needs both free space and the slow cargo
  build-up. Measured: 9-13 divisions and 6-11 deaths per 2000-t run among ~11 cells, so a
  lineage divides about once per 1000 t, and an arisen on-cell gets 0-1 divisions before
  dilution removes it. Selection needs ≥5-10
  divisions per lineage lifetime: higher division rates (larger kc, weaker cap) with faster dilution,
  or a much bigger box.

## 4. Negative results

- Unplanted membrane-gated waste (kw 0.15): no deaths in 1000 t.
- Slow global food (τ 200/300, K 1.5/1.0): monotone growth to 20-21 cells, then frozen. No overshoot.
- Slow local food (D=5, τ=100, K=1.5): starves all cells by t≈50. With D=20: crash to 2 cells, then a frozen lattice.
- xcell-evo packs started before the review (planted h and waste): stopped, not used.
- **Main S/N experiment**: no selection signal (above); 0 in-run on→on+on.
- My first `kinds.py` window counter crashed on int64 (fixed). No labkit bug this sprint.

## 5. Next sprint

1. **Get division rate up before testing selection**: screen kc 0.35-0.5 with a stronger
   global cap K so cells divide every ~100 t at steady state, plus dilution at the same rate.
   Accept the L7 test only when an arisen on-kind divides ≥3 times in N.
2. **Intrinsic death**: an age-like cost that division resets. One candidate is a conserved
   (CH-type) waste that splits between daughters at division. A relaxing channel can't do it.
3. Finish arm L (Dh 0.05/0.1 × kb ±10%, 3 seeds) and the β_h=0 / kb±10% packs the committee
   asked for. The gated marker is still the thread's one supported mechanism.
4. Movie: `packs/xcell-div/seed0/movie.mp4` (membrane cells pinching) is the thread's
   best-looking run. No new movie this sprint.
