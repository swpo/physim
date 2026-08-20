# NOTES.md — l0-sampler working notes (phase 3, stage 1)

## 2026-02-19 build log
- lib/genome.py: deviation-form genome + generic IMEX-FFT simulator (batched rfft2
  over n_act+n_chan fields; reaction explicit w/ OLD u in channel drives, exact
  diffusion in k-space — composite/rotor numerics verbatim). Tracking verbatim.
- PARITY: P-M0 PASS (area 28.0, 2000tu, ncomp 1). P-XV PASS omega=0.011062
  (cert audit value 0.011062 — 5-digit match), sep 8.437 (cert 8.437-8.439).
  P-VVW-B PASS (B blob 1000tu area 30). P-BF0 PASS (parked, |c|~5e-12 < 5e-3).
  P-BF5 first attempt FAILED honestly: symmetric paste sits on the unstable
  symmetric branch (self-launch in M6 was round-off breaking); re-gated as
  speed-law-under-kick (kd=0.5) — M6's own OWN certificate covers spontaneity.
- FOUR reference genomes written in deviation form. Key deviation-form facts:
  * k1_genome = k1_orig - sum_c K_c * u0 (fold channel baselines into k1).
  * M0/M4/XV vacuum = MIDDLE root of the bare cubic (fu=+0.515>0!). VVW vacuum
    also middle root (fu=-0.258<0 there). => u0 designation is a GENE; the funnel
    respects the stored u0. Best-margin designation would MIS-designate M0 (gives
    the deep outer root, wl=16.3 vs certified 10.9).
  * bfield maps EXACTLY via one bilinear vertex b*(u0-w) = -x_b*x_w (quadratic in
    deviations, vacuum-exact, invisible to linear screens) + tanh channel (thr>0
    => gprime(0)=0 => also linear-dead). G0a margin for BFIELD = -1/tau_b (trivial
    slow-channel eigenvalue) — flagged as heuristic in the excitable-shelf test.
- G0c VALIDATION: M0 wl=10.77, M4(tau=5.7) wl=10.84 vs certified shell 10.9 (0.5%);
  M2/P7s wl=10.93. M4 d*: cert 14.76-15.7 ~ 1.4x wl (shells sit at ~1.4 and ~2.4
  wavelengths; G0c predicts the SPACING between consecutive shells ~10.9: cert
  25.68-14.78=10.90 EXACT). VVW wl=12.4-12.7 (A/B species).
- Funnel restructure after measurement: funnel(g) evaluates AT the genome's u0;
  enumerate_vacua() = sampler helper listing all root combos w/ margins.
- Jitter strategy: plain k1 jitter loses G0b ~50% (M0 sits 3% from the fold
  |k1|=k1max). Fixed: jitter (lam, r=k1/k1max) — fold-distance-preserving.
- A2 'bond' classifier: rate-based (|dsep/dt|<0.002 over last 150tu AND moved).
  M0 pair d0=12: approach at T=400 (still closing at 15.8→, rate -0.0028 — the
  M2 bond at A=5 lives at d*=15.7 but M0 Dv=1 'bonds' are pinned artifacts per
  PROGRAM; classifier honestly says 'approach', consistent with slow dynamics).
- Stage-1 batch: 200 candidates, 4 workers x 50, strategies alternating
  uniform/jitter (seeds 1000-1199), launched 16:52.

## Conventions
- results.json: append-per-candidate via fcntl lock (kind=candidate|parity|
  funnel_check|smoke_*). archive.json: MAP-Elites, key = descriptor join,
  exemplar = most negative g0a margin.
- Assays at L=64 (periodic-image-safe for d0<=20 per M2 audit precedent);
  parity at L=96 (certified geometry). LOCKED in metrics.py.

## Parity FINAL (all gates PASS)
- P-M0 PASS area 28.0 @2000tu; P-XV PASS omega=0.011062 (cert 0.011062, 5-digit
  match), sep 8.437; P-VVW-B PASS; P-BF0 PASS (parked |c|~5e-12);
- P-BF5 PASS c=0.0758 vs law 0.0752 (+0.8%) — after 2 honest failures:
  (1) D_b=0.5 default was wrong (cert points ran D_b=0; BF1 dx-refine protocol),
  (2) symmetric paste sits on the unstable symmetric branch (self-launch = round-
  off breaking); gate re-scoped to BF1's kicked speed-law protocol kd=0.5,
  c over t in [700,1000].

## Batch history (honest ledger)
- s1 (seeds 1000-, 26 rows) ABORTED: bare u-poke misses all tau=5.7 refs
  (M1 trap measured in-geometry: M4/XV/BFIELD die bare, revive dressed 0.6).
- s1v2 (seeds 2000-, 32 rows) ABORTED: jitter G0b fail 11/16 — MEASURED FACT:
  all certified refs sit at fold distance 1-|k1/k1max| ~ 0.027-0.03 (blobs live
  NEAR THE CUBIC FOLD; 15% lam jitter throws |r| past 1). Also VVW's B-act
  k1=-2.15... was mis-snapped by polish_root to a far root (root_lost).
- jitter v3: log-jitter fold distance delta (sigma_d=0.4), snap u0 to nearest
  root. Funnel-only sanity: 39/40 pass. => s1v3 launch (seeds 3000-3199),
  17:34, 4 workers x 50, THE stage-1 batch.

## Fold-proximity finding (candidate for global memory)
1-|r| where r=k1/k1max: M0/M4/XV/BFIELD act: 0.0268; VVW A-act 0.0268 B-act
0.0300. Uniform strategy samples r in +-1.15 uniformly => only ~5% of uniform
candidates land within 2x of the refs' fold margin — the two strategies probe
very different shells of equation space (by design, now quantified).
