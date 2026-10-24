# active-droplets: sprint 1 report

## 1. Headline

**Fuel-fed Cahn-Hilliard droplets divide in 2D when interior transport is slow compared with the chemistry. If they also carry replicating, droplet-confined catalyst alleles, mutant alleles that arise during the run take over droplets, breed true through division, and the faster allele is selected.**

- Fastest-allele share at t=20000: 19/34 droplets with selection vs 3/30 in the neutral control (3 seeds each).
- Ancestor share at t=20000: 5/34 vs 19/30.
- In a membrane variant, each droplet makes its own amphiphile, which forms a shell on every interface. The shell re-forms on the cut faces after damage.

## 2. Claims

| world | claimed level | strongest evidence | known weaknesses |
|---|---|---|---|
| `ad1-fuel` | **L6[L2]** + **L4c** | `packs/ad1-fuel/seed*/sheet.png`, `lineage.png`. Planted disks hollow into rings, which break into 3-4 daughters (t≈2000-4400). Daughters then divide by dumbbell pinch-off (t≈8700-11300). 12-16 persistent splits, generations 2-4, all 3 seeds. Ablation F=0 (no fuel feed): all droplets dissolve by t≈6000 (`screens/abl_ad1_nofuelfeed.png`). | Starts from 2 planted disks; a uniform start goes extinct. Division stops once the box is full: the end state is a static lattice. dt halving changes nothing (`screens/num_ad1_dt*.png`), but resolution was not tested. φ overshoots the binodal (max ≈1.3). |
| `ad3-membrane` / `ad3s-soup` | **L6[L3]**, **L4a** weak | Amphiphile shell on every droplet for the whole run (`packs/ad3-membrane/seed1/tracks.png`; ψ rim 0.50-0.69, core 0.17-0.20, outside ≈0). The shell lines both faces of the hollow-ring stage and wraps each daughter through fission (sheet t=12100-17300). Ablation χ=0: no shell; ψ fills the body (`screens/abl_ad3_chi0.png`). Damage (`packs/ad3-membrane-damage`, 50% of a droplet erased): the two fragments each close a full shell within ~2 frames, and area is back to control in 5 frames (`screens/ad3_damage_vs_ctrl.png`). `ad3s-soup`: same behaviour from 8 random irregular blobs, no planted disks (`packs/ad3s-soup`, 3 seeds: 8-12 persistent splits, generations 2-3, 15-18 cells; ψ rim 0.69-0.73 vs core 0.18). | The membrane is passive: with back-reaction s=0 it does no work, and s≥0.3 blows up. It is a surfactant coating made by the droplet's own reaction, not a bilayer. The repair test produced two healed cells, not the original one. All divisions happen before t≈5000; after that the population is static. Damage was tested on one seed only. |
| `ad5-evolve` (+ `ad5n-neutral` control) | **L7[L2]** | `packs/ad5-evolve/alleles.png`: 3 selection seeds vs 3 neutral seeds. End counts [a0..a3]: selection [0,2,1,9], [4,1,2,4], [1,1,3,6]; neutral [7,0,0,2], [8,1,1,0], [4,4,2,1]. `seed0/sheet.png`: an a3 (blue) mutant appears inside an ancestral droplet at t≈3000, takes it over, then divides blue→blue+blue repeatedly. Ancestral droplets stay small and mostly stop dividing. Without dilution, selection persists (`screens/abl_ad5_nodil*.txt`). | Mutation is an imposed stochastic event: a 5-px disk is converted to another allele at rate 0.002. Kinds are coloured channels. Their phenotype (droplet size and division rate) differs visibly, but they were seeded as a designed repertoire of 4, not open-ended. Populations are about 10 droplets at 128², so seed 1 is noisy. Allele assignment uses argmax of the mean catalyst. Selection acts mainly during colonization; there is no ongoing turnover, because the static lattice comes back. |
| `ad4-protocell` | L6[L3] with 2 kinds; L7 **not** claimed | `packs/ad4-protocell`: membrane + catalyst kinds, which stay pure through division. | Selection signal is weak (A 3→6 vs B 3→5). The 5-channel sheet is hard to read. |
| `ad0-zwicker` | L1/L2 (validation) | `screens/ad0_base.png`: arrested coarsening. | No division in 2D (see negatives). |

## 3. Mechanisms learned (with ablations)

1. **Division in 2D needs core starvation plus slow interior transport.** Production `k u c²` needs fuel u, which enters from outside. Its penetration length √(Du/k) ≈ 4.5 px is smaller than the droplet radius, so the core decays.
   - With CH mobility M=1, interior chemical-potential flow (D_eff ≈ 2M) heals the core, giving stable round droplets at every Du from 0.5 to 4 (ablation).
   - With M=0.03 the core empties. The droplet becomes a ring, and the ring breaks up. Elongated droplets pinch at the starved waist.
   - Prediction: division needs the CH healing time R²/2M to exceed the decay time 1/kd. Both regimes fit this.
2. **Cooperative production (c², not c) keeps the dilute phase stable.** With n=1 the background nucleates and target-like rings appear (`screens/ad1_early.png`). n=2 gives discrete individuals.
3. **A membrane from the χ ψ |∇φ|² coupling.** It puts the droplet's own by-product exactly on its interfaces, including new interfaces made by division or wounding. With χ=0 there is no shell.
4. **Within-droplet competition controls whether innovation is possible (multi-level selection).**
   - With strong cross-inhibition (β=1.5), 31/31 mutant patches were lost: the bistable majority always wins.
   - With β=1.1, patches can take over a droplet. After that, between-droplet selection on growth rate decides which allele spreads.
5. **Heredity comes for free from phase separation.** Catalysts confined by the droplet are partitioned between daughters at division. Every division we saw kept the parent's kind.

## 4. Negative results

- **Zwicker linear chemistry, 2D:** droplets elongate into dumbbells that never pinch (no Rayleigh-Plateau instability in 2D). Raising the supersaturation only nucleates the background (`screens/ad0_*`).
- **Uniform or noisy start:** extinct in all 4 tested (φ0 from -0.7 to 0). A uniform soup burns the fuel globally before slow phase separation can concentrate material. The same slow M that enables division blocks nucleation.
- **Dense soup** (40 blobs): fills the box at once into a static lattice, with no room to divide.
- **Pixel-white demographic noise** on catalysts (σ up to 0.15): no flips and no catalyst loss. The noise averages out over a droplet.
- **Amphiphile back-reaction** κ_eff = κ − 2sψ: no effect at s=0.1; blow-up at s=0.3.
- **Low fuel** (F=0.002): the only regime with some droplet death and turnover, but it is slow (a few events per 40k steps).

## 5. Next sprint

1. **Make variation and turnover endogenous.**
   - Mutation as stochastic replication errors at droplet scale, e.g. copy noise applied to the per-droplet catalyst totals, instead of imposed patches.
   - Death from fuel competition (low-F regime) instead of a static lattice. Larger boxes (192-256²) with longer runs to get more than 50 droplets and repeated sweeps. This needs ~5 min per run, so some care with the compute budget.
2. **Give the membrane a function and make it heritable.**
   - Amphiphile gates fuel permeability (Du_eff = Du/(1+γψ), done implicitly so it stays stable), so membrane thickness sets metabolism and division rate.
   - Alleles that differ in amphiphile output then give **L7[L3]**: organized, membrane-bounded protocells under selection.
3. **Spontaneity and numerics.**
   - Sparse soup for ad5.
   - A resolution test (dx=0.5 with κ rescaled).
   - A saturating surfactant back-reaction.
4. **Motility.** A Frey-type χ coupling of fuel or product to φ (LITERATURE §2.4.3) for self-propelled protocells (L4b) that would compete by chemotaxis.

Tools in the thread dir (not labkit):
- `screen.py`: quick strips.
- `kinds.py`: two-kind counts.
- `alleles.py`: per-allele counts.
- `allele_plot.py`: per-allele curves computed from pack frames.

No labkit changes.
