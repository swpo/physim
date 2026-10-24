# active-droplets: final summary (3 sprints)

## 1. Best worlds and committee consensus rungs

| world | consensus rung (committee) | what it is |
|---|---|---|
| `ad7-gated` family (`ad7-gated-d4`, `ad7t-thick`, `ad9-ledger`) | **L6[L3] medium**; L7[L3] Weak; single allele L3 + L4c Weak | Fuel-fed Cahn-Hilliard droplets make their own amphiphile shell. The shell gates diffusion: fuel in weakly, catalyst out strongly. That gives membrane-bounded, dividing protocells whose heritable membrane output trades permeability against retention. |
| `ad5-evolve` | **L7[L2] low** (the lab's first L7 that survived a contagion audit) | The same droplets carry 4 catalyst alleles. Mutants arise, take over droplets, breed true, and faster alleles out-multiply the ancestor (6+6 seeds, p≈0.001 on a2+a3). |
| `ad1-fuel` | **L6[L2] high** | Core starvation plus slow interior transport divides droplets, via ring break-up or dumbbell fission. Converged at dt/2 and dx=0.5. |
| `ad3-membrane` / `ad3s-soup` | L6[L3] low (superseded by ad7) | Self-made ψ shell that wraps every daughter. It was inert until ad7 gave it a job. |

SPRINT3_SUMMARY

## 2. Mechanisms that worked (with the ablation that shows it)

1. **Division in 2D by core starvation.** Fuel enters from outside. Production `k u c²` is cooperative, so the dilute phase is stable.
   - With slow interior transport (CH mobility M=0.03), the core decays: the droplet becomes a ring that breaks up, or a dumbbell that pinches.
   - Ablations: M=1 gives no division at any Du; n=1 (linear production) nucleates the background.
   - Caveat from the judges: in ad1, replacing CH by linear diffusion at D=M still divides. ad1 is "Gray-Scott mitosis in a CH body". In the gated world ad7, the same swap stopped division (5 vs 12 droplets, 1 seed): there the double well does work.
2. **Self-made membranes from one coupling.** The by-product ψ drifts up `|∇φ|²` (`χ ψ |∇φ|²` free energy) and lines every interface, including fresh ones after division or wounding. Ablation: χ=0 gives no shell.
3. **A gated shell gives a protocell trade-off** (fork of fisim's `div(D e^{-βm}∇c)`). A single-peaked fitness landscape in membrane output kp, peaking at kp≈0.5-1.5. Ablations:
   - catalyst gate off: the membrane is pure cost (3 droplets vs 12);
   - fuel gate off: thick is as good as optimal (12 vs 6).
4. **Heredity from compartments.** Droplet-confined, replicating catalysts are split with the material at division.
   - Within-droplet competition decides whether innovation is possible: with β=1.5, 31/31 mutant patches were lost; with β=1.1, mutants can fix.
5. **Selection needs turnover.** Without deaths, every run froze into a static lattice and "selection" was a one-shot colonization race. Dilution gives turnover: random disks in ad5/ad7, Moran-coupled killing in ad9.

## 3. Mechanisms that failed

- **Zwicker linear chemistry in 2D:** dumbbells that never pinch (no Rayleigh-Plateau instability in 2D).
- **Uniform or noisy starts:** extinct. A uniform soup burns the fuel before slow phase separation can concentrate material.
- **Pixel-white demographic noise:** no flips; it averages out over a droplet.
- **Surfactant back-reaction** `κ - 2sψ`: no effect, then blow-up at s=0.3.
- **Self-propulsion, none in 6 attempts.** Variants: fuel affinity χ_u; a self-secreted repellent (forked from chemotaxis); treadmilling. Our division regime needs slow condensate mobility; Frey-type swimming needs fast mobility.
- **ad7 evolution with r=5 mutation patches:** label churn as large as selection. The neutral control matched the "selected" ancestor decline (22 vs 24%). A first-sprint-2 counting error (9/21) was caught by the committee; the correct figure is 12/21.

## 4. What transfers to PhySim worlds

- **Gated diffusion `div(D e^{-βψ}∇c)` with ψ made by the body itself.** It is a cheap, stable operator: implicit with ungated D, plus an explicit correction, using harmonic face means. One field then gives containment, a permeability/retention trade-off, and a heritable "membrane thickness" knob. It is a good hidden law for an agent to discover: the landscape has an interior optimum and a two-ablation signature.
- **Interface-seeking by-products** (drift up `|∇φ|²`) give membranes for free in any phase-separating world.
- **Compartment heredity:** any confined autocatalyst plus a dividing body gives breeding-true kinds; turnover must be designed in.
- **Readable rendering:** colour by kind, membrane as a white rim, fuel as background (`protocell_movie.py`). It reads far better than channel composites.

## 5. What a next lab should try

- Endogenous turnover: deaths that come from fuel competition at a moderate maintenance cost, not imposed dilution. Then a continuous kp trait in 192²+ boxes.
- Resolve the division/motility conflict: let a second component or an allele set local CH mobility, giving swimmers that switch to dividers.
- A membrane that matters mechanically: a saturating surfactant back-reaction (bounded κ_eff) so that membrane composition sets division geometry.
- Parasites and cheats with the gated membrane: does retention gating protect against parasitic replicators (the autopoiesis thread found a threshold)?

## 6. Showcase movie

`movies/showcase.mp4` (sheet: `movies/showcase_sheet.png`).

Caption: World `ad7t-thick`, seed 1, 128x128 periodic box, t = 0-20000, 120 frames, whole box, fixed colour scales (rendered by `protocell_movie.py` from the evidence-pack frames). Background brightness = fuel (dark = depleted around consumers); cell body colour = dominant catalyst allele; white rim = the amphiphile shell each cell makes for itself. Six planted cells all carry the thick-membrane allele kp=4 (red: small, bright thick shell, fuel-starved, rarely divide). Mutation patches (imposed stochastic events, visible as two-coloured cells) introduce kp=0 (blue: no shell, leaky, a blurred catalyst halo, does not divide), kp=0.5 (green, thin shell) and kp=1.5 (yellow). Green and yellow cells grow and divide by dumbbell fission, and random dilution disks (also imposed) clear space that they recolonize. By t=20000 the box is mostly thin- and medium-membrane cells. Caveat: the neutral control (all kp=4) also relabels most cells through mutation churn; what differs is population size (36 vs 21 over 3 seeds) and the fact that only green/yellow cells divide repeatedly.
