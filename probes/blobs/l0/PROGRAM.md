# L0 — equation-space search (bottom-up track)
(phase 3, 2026-02-19. Sibling searchers: l0-sampler builds lib/ + funnel + random/
theory-guided sampling; l0-evolver builds merge/mutate operators and evolves.)

## Canonical genome (deviation form — vacuum-exact BY CONSTRUCTION)
n_act cubic activators u_i, n_chan linear channels x_c (deviations, 0 at vacuum):
  du_i/dt = Du_i lap u_i + lam_i*u_i - u_i^3 + k1_i - sum_c K[i,c]*x_c
  dx_c/dt = ( sum_a W[c,a]*g_c(u_a - u0_a) - x_c )/tau_c + D_c lap x_c
g_c = identity OR tanh saturation tanh(max(z-thr,0)/sc) (bounded deposit channels).
At the vacuum u_i=u0_i (a root of -u^3+lam*u+k1=0), all drives vanish -> x_c=0 exactly,
for ANY weights: the iso-line trick is structural here. Genome = {acts:[{lam,k1,Du}],
chans:[{tau,D,g}], W (n_chan x n_act), K (n_act x n_chan), provenance}.
Known worlds map exactly (M0: 1 act + 2 chans; vvw: 2+3 shared w-row; xv: 2+6 with
cross edges eta in W; bfield: 1+3 incl. one tanh channel) — write these four as the
REFERENCE GENOMES and verify behavior parity first.

## G0 algebraic funnel (microseconds each; order matters)
G0a vacuum exists + temporally stable: pick most-negative real cubic root per act;
    J from genome; require max_k Re eig(J - k^2 D) < 0 (else Turing soup — reject,
    but LOG the margin; near-zero margins are an interesting "excitable" shelf).
G0b each activator locally bistable: cubic -u^3+lam*u+k1 has 3 real roots.
G0c spatial tails: steady-state modes e^{mu*x}, s=mu^2 solve (per activator block)
    Du*s + a - sum_c K_c*W_c/(1 - A_c*s) = 0, A_c = tau_c*D_c  (a = lam-3u0^2).
    Complex mu => oscillatory tails => binding shells at wavelength 2pi/|Im mu|
    (validated: predicts M4 shell spacing 10.9px to 1%). Record (Re mu, Im mu);
    "chemistry candidates" have 3 <= wavelength <= 30 px and |Re mu| in [0.1, 1.5].
THEN nonlinear assays (blob existence is SUBCRITICAL/homoclinic — probes mandatory).

## Assay battery (reuse certified metric ideas; IMEX-FFT dx=0.5 dt=0.02 unless noted)
A1 poke: Gaussian seed -> {die, persist(area,peak), replicate, travel(c)} (60-90s)
A2 pair: d0 in {8,12,16,20} -> {repel, bond(d*), merge}; compare d* to G0c prediction
A3 dial probe: tau of the heaviest channel +-20% -> motility onset? (drift family)
Behavior descriptor: (n_act, tails osc?, poke class, motility class, bond?, period?)
MAP-Elites archive keyed on descriptor; keep best-by-margin genome per cell.
results.json append-per-candidate; archive.json updated atomically.

## Honesty & provenance
This is SCREENING (anthropic-screening doctrine, cf. E2): every published world
documents that it was selected from N candidates by these filters. Log EVERYTHING
incl. rejects (funnel pass-rates are primary deliverables). No cherry-quoting:
yield curves = candidates/hour and interesting-per-100 by strategy
(uniform random vs jitter-around-reference-genomes vs evolver output).

## Compute plan
Stage 1 LOCAL: validate funnel + battery on ~200 candidates; measure stage costs.
Stage 2 FAN-OUT: controller provisions Prime CPU pods (prime CLI); workers run the
battery embarrassingly-parallel; merge archives. Do not provision pods yourself —
report when stage 1 is done and the controller handles rental.
