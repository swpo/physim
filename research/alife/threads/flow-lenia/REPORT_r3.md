# flow-lenia: sprint 3 report (final sprint)

## 1. Headline

**The level-of-selection audit says the uptake-gene "selection" is not yet selection among
individuals.** Against identical-event neutral twins (same mutation times, location quantiles and
effects on their own RNG stream), the gene still rises more under selection (paired S−N: +0.54, +0.43,
+0.03, +1.32, +0.33; 5/5 positive, sign test p=0.031). The decomposition does not pin this on individuals.
- In S seeds 1 and 3, the rise is mostly within-body: one or two fused giants remain.
- In seeds 0 and 4, the between-body term dominates. But the neutral twins show between-body terms of the same size (+0.24…+0.62), with fusion terms to match, so the "between > within+fusion" test does not separate selection from drift through fusion.
- High-g persistent births never clearly outnumber conversions. Following
the committee's rule, I call this **L5 (infection / within-body takeover), not L7**. The next
step is anti-fusion before any more mutation runs.

The predator-prey world fails on a fresh seed: predators die out on seed 11 (t≈704), as the
skeptic found, so coexistence is **3/4 seeds**. Its matched ablations on seed 11 keep the
expected signs. The showcase movie (`movies/showcase.mp4`) is the 192² predator-prey world.

## 2. Main experiment: is selection carried by bodies or by matter?

`worlds/fl_forager_gene2`, 128², 12000 steps (t=2400). Arms:
- **S:** per-parcel uptake gene.
- **N:** identical-event neutral twin. 52/45/46/51/45 events in both arms of seeds 0-4.
- **S_body:** uptake uses g_eff = blur5(A·g)/blur5(A), so the parcels of one body share one rate.
- **N_body** is bit-identical to N: with the gene off, the body flag has nothing to act on (checked on seed 0).

Seeds: 5 per arm (0-4), not 8 (CPU).

Snapshots every 20 steps were analysed by `scripts/audit_gene.py`:
- Bodies are periodic components of blur1(A) > 0.15. The main parent is the largest overlap.
- The Price split of Δ(body-matter-weighted mean log g) is an exact identity (the terms sum to the total).
- A "persistent" fission needs ≥2 daughters that each continue 1-to-1 for ≥200 steps. Raw split counts are flicker.

| run | Δ total | between | within | fusion | final bodies / high | high persistent births / conversions / flips | max persistent gen | origin of final high bodies |
|---|---|---|---|---|---|---|---|---|
| S_s0 | +0.53 | +0.69 | +0.47 | -0.63 | 18 / 18 | 38 / 51 / 7 | 3 | 18 fusion |
| S_s1 | +0.58 | +0.26 | +0.53 | -0.20 | 1 / 1 | 4 / 11 / 1 | 3 | 1 takeover |
| S_s2 | -0.20 | +0.15 | -0.38 | +0.03 | 13 / 0 | 0 / 0 / 0 | 4 | – |
| S_s3 | +0.99 | +0.51 | +0.73 | -0.26 | 2 / 1 | 3 / 2 / 1 | 3 | 1 conversion |
| S_s4 | +0.08 | +0.44 | -0.02 | -0.34 | 14 / 1 | 0 / 1 / 1 | 4 | 1 born_high_from_low |
| Sb_s0 | +0.56 | -0.23 | +0.51 | +0.27 | 2 / 1 | 7 / 12 / 3 | 4 | 1 takeover |
| Sb_s1 | +0.40 | +0.11 | +0.39 | -0.10 | 2 / 1 | 17 / 19 / 2 | 3 | 1 flip |
| Sb_s2 | -0.06 | +0.35 | -0.31 | -0.10 | 15 / 0 | 0 / 0 / 0 | 5 | – |
| Sb_s3 | -0.50 | +0.34 | -0.58 | -0.27 | 2 / 0 | 0 / 1 / 1 | 2 | – |
| Sb_s4 | +0.10 | +0.82 | -0.25 | -0.47 | 16 / 7 | 12 / 66 / 0 | 5 | 2 born_high_from_low, 3 conversion, 2 fusion |
| N_s0 | -0.01 | -0.23 | +0.03 | +0.20 | 12 / 1 | 21 / 54 / 7 | 6 | 1 takeover |
| N_s1 | +0.15 | -0.01 | +0.08 | +0.07 | 13 / 3 | 13 / 69 / 8 | 6 | 1 born_high_from_low, 2 fusion |
| N_s2 | -0.23 | +0.62 | +0.00 | -0.85 | 12 / 0 | 0 / 1 / 0 | 5 | – |
| N_s3 | -0.33 | +0.44 | -0.34 | -0.44 | 2 / 0 | 2 / 4 / 0 | 2 | – |
| N_s4 | -0.25 | +0.24 | -0.27 | -0.22 | 11 / 0 | 1 / 4 / 1 | 7 | – |

Gene-coloured sheets (cyan = low g, pale = ancestral, orange = high g) are in `evo3/sheet_*.png`:
- `sheet_S_s0.png`: a gradual sweep of small orange gliders through ~20 motile gliders.
- `sheet_S_s1.png`: orange gliders multiply (t≈312-416), grow into giants and fuse, and one giant absorbs the last pale cell (t≈1880).

**Verdict against the committee's pass criteria:**
- (a) between > within+fusion: 4/5 S seeds formally pass, but so do 3/5 neutral twins (N_s2 between +0.62, N_s3 +0.44). The test does not discriminate here.
- High-g persistent births > conversions: only in S seed 3 (3 vs 2). In seed 0, 38 births vs 51 conversions.
- Twins ≈ 0: they are not; the terms reach ±0.8 even though the totals stay in −0.33…+0.15.
- Origins: all 18 final high bodies of S seed 0 trace back to fusion; seeds 1 and 3 end with one giant.
- S_body does not rescue it. S_body − N: +0.57, +0.25, +0.16, −0.17, +0.35 (4/5 positive), a weaker shift than S. Gigantism remains (2 final bodies in 3/5 seeds).
- **Result:** L7 not supported. Uptake selection acts on matter (and on giants that form by fusion), not demonstrably on reproducing individuals.

labkit v0.2 pack (`packs/fl_forager_gene2_S/seed0`, gene-coloured): 1018 tracks, 378 splits,
340 merges (merge/split 0.90), 0 persistent splits at K=20 frames, max generation 0. This
independently shows the same fission-fusion churn. Only one pack was shipped (CPU); the other
arms have gene-coloured sheets in `evo3/sheet_*.png`.

**Why:** fusion is frequent in this world, roughly as frequent as persistent fission. High-g matter makes big bodies, which absorb neighbours, so a gene spreads by fusion and by takeover within the giant. That is infection, not heredity. Persistent generation depth is only 2-4 in S runs (5-7 in N runs, which keep more small bodies).

## 3. Secondary: fl_predator arms, seed 11 (packs/fl_predator*/seed11, 12000 steps, t=2400)

| arm | prey t=0 / min / end | predator t=0 / min / end | extinction |
|---|---|---|---|
| reference | 283 / 283 / 1469 | 277 / 0 / 0 | predators by t≈704 |
| flee = 0 | 283 / 0 / 0 | 277 / 0 / 0 | prey t≈784, predators t≈888 |
| chase = 0 | 283 / 283 / 1478 | 277 / 0 / 0 | predators by t≈376 |
| prey only | 283 / 283 / 1195 | – | – |

Signs are as before: without flee both species die, and without chase the predators starve
sooner. The reference fails on seed 11, so coexistence is 3/4 seeds (0, 1, 2 coexist; 11 does
not). It is a narrow escape, as the committee judged.

Not done for lack of CPU time: 6 seeds per arm, the resolution test, and the first-draw log for fl_predator_gene.

## 4. Showcase

`movies/showcase.mp4`: fl_predator at 192², seed 0, t=0…2400, 301 frames, 3.8 MB. Prey and predators coexist to the end.
- Prey peak at t≈830 and t≈2200.
- Predator matter ranges 11…400, with peaks at t≈630-980, 1220, 1680-1880 and 2140-2340.

This is one seed at 192², so it does not settle robustness. The caption is in FINAL.md.

## 5. What I would do next

Add anti-fusion: a local repulsion between distinct bodies, e.g. a pressure term from blurred
matter of other labels, or a cross-body "alpha" term. This should turn the reticulate lineages
into trees. Only then rerun S/N/S_body with the audit, which is ready
(`scripts/record_gene.py` + `scripts/audit_gene.py`).
