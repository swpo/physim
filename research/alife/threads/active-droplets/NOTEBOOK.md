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
