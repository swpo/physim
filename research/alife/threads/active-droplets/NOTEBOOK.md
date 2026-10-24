# active-droplets notebook

Sprint 1 started 2026-10-24 14:29 UTC. Tools: `screen.py` (quick strip of all channels),
`kinds.py` (per-kind droplet counts for catalyst worlds), `montage.py`. Screens in `screens/`.

## ad0-zwicker: Cahn-Hilliard + linear production/decay (Zwicker-style active emulsion)
- `d phi = M lap mu + kp(1-phi)/2 - kd(1+phi)/2`. Spectral semi-implicit, stabilized (A=2), dt 0.2-0.5.
- From noise with kp=kd: arrested coarsening into a dense droplet/stripe emulsion (`screens/ad0_base.png`). Validates
  the known result (reactions arrest Ostwald ripening, Ohta-Kawasaki-like size selection). L1/L2.
- From 3 seeds in a dilute background (kp=0.001, kd=0.005): droplets grow, elongate into dumbbells and **never pinch**
  (`screens/ad0_long_a.png`, 16k steps). NEGATIVE: in 2D there is no Rayleigh-Plateau instability, so Zwicker
  shape instability gives stable elongated droplets, not division. Higher kp (0.002) nucleates the background
  instead (`screens/ad0_s_kp0.002_kd0.005.png`).

## ad1-fuel: production needs a diffusing, consumed fuel u
- `prod = k u c^n`, `c=(1+phi)/2`, decay `kd c`; `u` fed from a bath `F(1-u)`, diffusion Du.
- n=1 (linear in c): dilute phase is autocatalytically unstable -> background nucleation, plus a striking
  expanding-ring pattern around the seed droplet (`screens/ad1_early.png`). Not individuals.
- n=2 (cooperative): background stable, single droplets grow to a fixed, fuel-limited size
  (`screens/ad1o2_k-0.05_kd-0.01_F-0.002.png`). No division for M=1 at any Du tried (0.5-4).
- Diagnosis: interior CH transport (D_eff ~ 2M) heals the fuel-starved core faster than decay acts.
  **Lowering M to 0.03** (CH slow vs chemistry): core starves -> droplet hollows into a ring -> ring breaks into
  3-4 daughters -> each regrows -> later elongated droplets pinch into two (binary fission) until the domain is
  filled with a fuel-limited droplet lattice (`packs/ad1-fuel-try/sheet.png`, 12 persistent splits, gen 2).
  Mechanism: fuel penetration length sqrt(Du/k) ~ 4.5 < droplet radius, with slow internal redistribution.
- LITERATURE.md (pulled 15:00) agrees: Zwicker 2017 division was 3D/axisymmetric; "no heredity: all droplets
  converge to one attractor". Our 2D route to division is different: core starvation + slow interior transport.

## ad2-catalysts: heritable catalysts (fork of ad1-fuel)
- Production needs one of two catalysts a, b: `prod = u c^2 (ka a + kb b)`. Catalysts replicate only inside droplets
  (`r c a (1 - a - beta b)`), decay outside (`g (1-c) a`), cross-inhibit (beta=1.5, bistable -> pure droplets).
- Seeds alternate kinds. Neutral (ka=kb=0.15): both kinds multiply, every droplet stays pure (`screens/ad2_neutral.png`).
  Biased (ka=0.15, kb=0.10): A droplets multiply ~3 -> ~10 by t=15000, B stay ~2-3 and barely divide
  (`screens/ad2_sel.png`). Division splits the catalyst with the material: kinds breed true in every division seen.
- Weakness: after colonization the population freezes into a static, fuel-limited lattice, so "selection" is
  only differential colonization speed. No turnover yet. Counts in the .txt files over-count droplets cut by the
  periodic edge (fixed in kinds.py later: periodic labels).

## ad2n-noisy: demographic noise on catalyst replication
- sigma 0.05 and 0.15 (pixel-white noise): no kind flips, no catalyst loss (`screens/ad2n_s*.png`). NEGATIVE: pixel
  noise averages out over a ~100 px droplet and bistability absorbs it. Mutation/turnover need droplet-scale noise
  or a mechanism, not pixel noise.

## ad3-membrane: droplets synthesize an amphiphile that binds their own interface
- `psi` made by the fuel reaction (`kp prod`), drift up `|grad phi|^2` (chi=8), slow decay. s=0 (no back-reaction).
- Result (`screens/ad3_base.png`): psi forms thin bright shells exactly on every interface: around the hollow-ring
  stage it lines both inner and outer edges; after ring break-up each daughter is wrapped in its own shell.
  Division unchanged vs ad1. Boundary channel differs from interior (low) and exterior (zero).
- Back-reaction s (kappa_eff = kappa - 2 s psi): s=0.1 no visible change; s=0.3 blows up at once (psi peaks 1.6 ->
  kappa_eff < 0). Needs a saturating coupling if revisited.

## ad1 regime sweep (40k steps, `screens/ad1sw_*.png`)
- F=0.002 kd=0.02 (low fuel): sparse population, divisions still happen late (t~35000) and some droplets dissolve
  (10 -> 7 -> 8): the only regime so far with turnover. F=0.004-0.008 / lower kd / lower M / lower Du: faster
  colonization, then a static lattice of 20-24 droplets.
- phi overshoots the binodal inside growing droplets (max 1.2-1.4): production outruns CH relaxation. To be checked
  with dt halving.

## Spontaneity
- Uniform starts (phi0 = -0.7, -0.5, -0.2, 0.0 with noise; seeds=0): everything goes EXTINCT in all four
  (`screens/ad1_spont*.png`). NEGATIVE, with a mechanism: the uniform soup consumes fuel everywhere at once, fuel
  crashes globally, and decay wins before the slow (M=0.03) phase separation can concentrate material into droplets.
  Individuals need a pre-concentrated nucleus. Same trade-off that makes division possible (slow M) kills nucleation.
- "Soup" start (40 random blobs of random radius 1.5-6 and random amplitude; `soup=40`): about 25 droplets survive
  and immediately fill the box as a static lattice (`screens/ad1_soup.png`); ad4 soup also keeps both kinds, pure
  (`screens/ad4_soup.txt`). A sparse soup (fewer blobs) is the right spontaneity test; not done yet.

## ad4-protocell (ad2 catalysts + ad3 membrane)
- ka=0.15, kb=0.12, 40k steps: A 3 -> 6, B 3 -> 5 (`screens/ad4_F4.png`); low fuel F=0.002: A 2 -> 3, B 2 -> 2.
  Kinds breed true, but the selection signal is weak because populations are tiny at 128^2 and freeze into a
  static lattice. Motivates ad5 (dilution for turnover + mutation for variation).
