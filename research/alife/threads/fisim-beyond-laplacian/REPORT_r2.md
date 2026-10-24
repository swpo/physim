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

HEADLINE

## 2. Claims

CLAIMS

## 3. Mechanisms learned

- **These membrane cells do not die on their own.** Once planting was removed, none of three
  intrinsic turnover routes produced deaths: unplanted membrane-gated waste (K=0.15), slow
  global food (τ=200-300), and the old cell-pop cap. Populations freeze at 12-21 cells. An
  m4 spot is a robust dissipative soliton. The only death mechanism I found is
  overcrowding at birth. Turnover needs an explicit cost that grows with age or size; a
  concentration-type waste can't provide one, because division doesn't dilute it.
- **Kicks are a clean mutation operator for a bistable marker.** A σ=1.5 h-disk that lands
  inside a body flips it on, and the gate keeps it on. One that lands outside decays,
  because the off-state is favoured off-body (k1=-0.2). Rate 0.02 per time unit gave 4 gains
  among ~11 lineages in 1000 t, all of which persisted.
- **Ungated marker (L arm), Dh=0.02:** every planted on-marker was lost by t=100 at
  kb 0.225/0.25/0.275, while the gated marker holds (r1: 46 divisions, 0 mixed; committee
  re-run: no gate → all on-lineages lost). At this one Dh, the gate is not replaceable by low
  diffusion. Dh 0.05/0.1 were not run (CPU).

MECH_SEL

## 4. Negative results

- Unplanted membrane-gated waste (kw 0.15): no deaths in 1000 t.
- Slow global food (τ 200/300, K 1.5/1.0): monotone growth to 20-21 cells, then frozen. No overshoot.
- Slow local food (D=5, τ=100, K=1.5): starves all cells by t≈50. With D=20: crash to 2 cells, then a frozen lattice.
- xcell-evo packs started before the review (planted h and waste): stopped, not used.
NEG_MORE

## 5. Next sprint

NEXT
