# L0 SAMPLER — stage-1 SUMMARY (2026-02-19)

## What was built (deliverables 1-4)
- lib/genome.py — deviation-form genome (acts/chans/W/K/bilin/provenance),
  generic n-field IMEX-FFT simulator (composite/rotor numerics verbatim,
  batched rfft2), tracking verbatim, results-IO with fcntl lock.
  FOUR reference genomes: M0, VVW (MAXC pair), XV (rotor), BFIELD (M6, exact
  via one bilinear vertex -x_b*x_w + tanh channel).
- parity.py — ALL 5 GATES PASS:
  * P-M0: area 28.0 @ dx=0.5, 2000 tu, ncomp==1 throughout.
  * P-XV: omega=0.011062 vs certified audit 0.011062 (5-digit match), sep 8.437.
  * P-VVW-B: B blob 1000 tu, area 30.
  * P-BF0: gamma=0 parked, |c| ~ 5e-12.
  * P-BF5: c=0.0758 vs law 0.0752 (+0.8%) — after 2 honest protocol fixes
    (D_b=0 is the certified point; kicked kd=0.5 speed-law test because the
    symmetric paste sits on the unstable symmetric branch).
- lib/funnel.py — G0b (fold discriminant), G0a (full (na+nc)-field dispersion
  margin over k in [0,3], all-root enumeration helper), G0c (self-block tail
  polynomial in s=mu^2 with A_c=tau_c*D_c poles).
  G0c VALIDATED: M0 wl=10.77, M4 wl=10.84 vs certified 10.9 shell (0.5%);
  M4 cert shell spacing 25.68-14.78=10.90 exact.
- lib/assays.py + metrics.py (LOCKED v2 before batch) — A1 poke PANEL
  (bare, then dressed 0.6*W channel bumps — M1-trap-aware), A2 pair
  d0 in {8,12,16,20} with rate-based bond/repel/merge classes, A3 tau+-20%
  dial, descriptor -> MAP-Elites archive.json (shared with l0-evolver).
- sample.py — per-candidate pipeline with SAVE-AS-YOU-GO (append after every
  candidate), atomic archive updates, per-stage timing.

## Stage-1 batch: tag s1v3, 200 candidates (100 uniform + 100 jitter), seeds 3000-3199
(two earlier batches ABORTED and kept in results.json: s1 26 rows — bare-poke
protocol missed all tau=5.7 refs; s1v2 32 rows — jitter lost bistability ~50%.
Both aborts produced locked protocol upgrades BEFORE the real batch.)

## YIELD CURVES (primary deliverable; data/yield_s1v3.json)
UNIFORM (n=100):            JITTER sigma=0.15/fold-log 0.4 (n=100):
  G0b pass       87%          G0b pass       100%
  G0a pass       87%          G0a pass        97%
  osc tails      24%          osc tails       97%
  chem box        3%          chem box        76%
  excitable shelf 10%         excitable shelf 23%
  A1/100: die 58, domain 27,  A1/100: die 31, persist 49, multi 5,
          persist 2                   replicate 5, domain 7
  ALIVE/100:      2           ALIVE/100:      49
  bond/100:       1           bond/100:      14 (+ repel 19, replicate-on-pair 12)
  motility onset: 0           motility onset: 0
Wall-clock: funnel ~2.3 ms/cand (BOTH strategies); assay median 31 s, mean 130 s
(alive candidates cost 300-1000 s: full pair batteries dominate).
Throughput: 30 cand/hour/core mean; 200 cands = 121 min on 4 local cores.
Uniform candidates are 5x cheaper (mean 40 s vs 199 s) because dead worlds
early-exit; a CPU-pod hour buys ~90 uniform or ~18 jitter candidates/core.

## Jitter yield by reference (n / alive / bond)
  VVW 23/74%/12   XV 17/76%/8   M0 16/38%/5   BFIELD 22/36%/2   M4 22/23%/2
  (M4/BFIELD sit at tau=5.7 near the pair-drift edge: jitters fall off the
  blob island more often — consistent with M4's mapped replication ceiling.)

## Theory validation on NEW worlds (headline)
Across 37 real-mover bond outcomes (moved>1px): d*/wl_G0c clusters at
  1.348 +- 0.075 (n=30 first shell) — M4's certified ratio is 14.76/10.9=1.354.
  Higher shells at ~1.8-2.0 (n=4) and ~2.8 (n=3) = 1.35+0.5, 1.35+1.5 (half-
  wavelength ladder, consistent with tail-lock shells).
=> G0c tail wavelength PREDICTS bond separations to ~5% across jittered
   equation space: the funnel's "chemistry" coordinate is real physics.

## Novel worlds from UNIFORM RANDOM (2/100 alive — both outside known families)
- s1v3_uni_3050: 1 act + 2 TANH channels + 1 id channel, K has an EXCITING
  entry (-1.11); persists (area 28), pairs MERGE at d0<=12 and repel to ~24
  at d0>=16 (strips/uni3050_tanh_world.png). First stable world with
  saturating-deposit channels as core physics, not as b-field add-on.
- s1v3_uni_3034: NO oscillatory linear tails (G0c-invisible), yet pair
  converges two-sidedly to d*=27.9 from d0 in {12,16,20} (bond basin wider
  than any known family; strips/uni3034_monotail_bond.png). Fold distance
  0.556 — far from the fold, unlike ALL certified refs (0.027-0.03).
  => binding without oscillatory tails exists = beyond-G0c binding channel.

## Honest negatives / caveats
- NO travel and NO motility onset in 200 candidates (A3 +-20% tau dial too
  coarse, or drift windows too narrow: M4's window is (5.636,5.748) = +-1%).
  Stage-2 should dial tau adaptively (e.g. 5 points, +-5%) on alive cands.
- chem_box as specced has a recall problem: its osc-dominance clause
  (|Re osc| <= 2|Re mono|) rejects ALL 15 alive VVW-family jitters (12 bond).
  Wavelength+|Re| box alone would keep them. Uniform side: chem_box 3% with
  0/3 alive (n too small to score precision).
- A2 'bond' class has a wrap artifact: co-traveling/scattered pairs on the
  torus can register sep~L*k stable (3057 d0=8 -> 131.9px). Filterable
  post-hoc (d* < 30 AND moved < 40), kept raw in results.json.
- domain class (area>=150) = 27% of uniform candidates: spreading-phase
  worlds (labyrinth caveat class), not blobs. The blob/domain boundary is
  THE discriminator uniform sampling must learn (fold distance correlates:
  alive uniforms at 0.038/0.556 both, domain median fold-dist much larger —
  not yet a clean predictor, n too small).
- Uniform G0b pass 87% matches the designed 87% (|k1|<1.15*k1max window).
- Funnel cost is NEGLIGIBLE (2 ms): G0 is not the bottleneck; the assay is.
  Pod planning should budget ~40 core-s/uniform and ~200 core-s/jitter.

## Files
results.json (append-per-candidate, 258 candidate rows total incl. aborted
batches, all parity/funnel-check/ref-assay rows), archive.json (108 cells,
shared with l0-evolver), data/yield_s1v3.json, strips/*.png, NOTES.md
(protocol ledger), metrics.py (LOCKED v2), parity.py, sample.py,
yield_curves.py, lib/{genome,funnel,assays,sampler}.py.
