# GUILD ECONOMY — world-search summary (2026-02-17)

## Verdict
**CONDITIONAL PASS.** The world produces a real 3-layer hierarchy with an
emergent market-clearing top law (exp relaxation of the producer:recycler
guild ratio, r2 ~ 0.96-0.996 on every certified run) and a clean price->
equilibrium demand curve (G3). The one honest weakness: the G1 L2->L3 TIME
separation hovers at the 5x line (s23 = 4.3-6.0 across seeds; median 5.3;
>=5 on 5/8 seeds). By length scales the separation is unambiguous
(patch diam ~6 px vs domain 96 px: 13-19x). I report both; if the gate is
read strictly as time-only, this is a NEAR-PASS at 4/8 seeds instead of a
pass, and I say so plainly rather than shop for a friendlier estimator.

## Mechanism (all linear prices; no authored curves, no scripted events)
One gene axis a in [0,1] beyond E2 enzyme economics:
  income = kE*V*(cR*a*R + cW*(1-a)*W)        (a = allocation to eating raw R)
  R eaten -> waste W at yield yW; W decays at dW; both diffuse.
  rent = m*V + m2*V*(#active pathways)       (m2 = expression overhead —
         still a linear price; generalists pay 2 pathways, specialists 1)
  finite larder E<=cap*V; bankruptcy burns tissue V+=E/0.05; death V<0.05;
  senescence hazard 4.5e-4/tick (vacancy turnover -> selection keeps acting);
  colonization: copy dominant-energy neighbor's a + N(0,sig); child must
  clear viability gate at LOCAL prices: kE*(cR*a*R+cW*(1-a)*W) > 1.1*rent.

## Hierarchy (layer -> variable -> timescale, certified numbers, GE1 seed0)
  L1 fields (fast):   R,W impulse-decay tau        66-96 ticks
  L2 guilds (meso):   8x8-block recycler share ACF tau ~480-660 ticks;
                      bimodal a (share_lo 0.42-0.46, purity 0.97, bimod 1.0);
                      producer/recycler patch mosaics, diam_w ~5-7 px
  L3 market (slow):   global guild ratio fr(t) relaxes exponentially,
                      tau3 ~ 2400-3140 ticks, r2 0.96-0.994
  separations: s12 = 5.2-6.4x (time), s23 = 4.3-6.0x (time) / 13-19x (length)

## Best candidate GE1 (theory coords)
  rho=cW/cR=2.1, yW=0.7, leak=dW/(0.3*kE)=0.65, margin=cR*kE/m=7.0,
  over=m2/m=1.5, sig_mut=0.05, r0=0.006, hazard=4.5e-4, DW=0.02, L=96
  (raw: kE=0.02, m=0.0036, cR=1.26, cW=2.646, dW=0.0039, m2=0.0054)
  Emergent equilibrium: fr* = 0.455 +- 0.004 (8 seeds); Rm/Wm = 1.51
  (marginal-return equalization pins the FIELD ratio near rho — the market
  clears: measured R*/W* tracks the price ratio).

## Gates
  G1 HIERARCHY: PASS (3 layers; s12 >= 5.2x time; s23 13-19x by length,
     4.3-6.0x by time — flagged: time-only reading is marginal).
  G2 SIMPLE TOP: PASS. compact_top_fit=relaxation on every certified run,
     r2 0.9597-0.9963 (12/12 GE1-family runs >= 0.85, incl. jitters);
     return gap to control-twin equilibrium 0.000-0.008.
  G3 COMPUTED: PASS. Demand curve fr*(rho): 0.323/0.408/0.455/0.473/0.493/
     0.507/0.524 at rho=1.9..2.5 — smooth, monotone, 7 points. tau3(rho):
     4050/3578/2890/2217/2034/2246/2036 — monotone 1.9->2.3 then flat
     (tau saturates once recycler patches percolate). fr* is the top-law
     OBSERVABLE and it tracks the micro price over the whole window.
     Also passes on yW (+-10%: fr* 0.351/0.495) and leak (0.471/0.385) axes.
  G4 ROBUST: PASS with stated margins. Seeds: 8/8 have relaxation r2>=0.96
     + return; s23>=5 (time) on 5/8, length s23 always >= 15x. All-coord
     ±10% jitter (4 draws): 2 full pass, 1 pass-by-length (s23 5.01,
     drift 0.08 — settle not converged), 1 FAIL no_guilds (draw pushed
     effective waste income rho*yW down 12% + leak up 6% -> recyclers not
     viable). Axis jitters: yW,leak,hazard,sig,DW,margin+10% all keep
     guilds+top law; margin-10% kills guilds (R* window edge, documented).
     HONEST BOTTOM LINE: the world sits ~1.2x inside its viability boundary
     on the margin/yW*rho axes; a wider margin needs a bigger price basin.
  G5 BUDGET: PASS. Full cycle in 60k ticks (settle 45k + kick relax 15k)
     at L=96, 98-122 s/run single core. L=64 works at 40k+20k (~35-45 s)
     with the same laws (tau3 ~ 3.4k), used for the 150+-run search.

## Response curve (top-law parameter vs micro price)
  rho:   1.9    2.0    2.1    2.2    2.3    2.4    2.5
  fr*:   0.323  0.408  0.455  0.473  0.493  0.507  0.524
  tau3:  4050   3578   2890   2217   2034   2246   2036
  (rho=2.1 entries are 8-seed medians; others seed 0. Mean-field theory
  q/(1+q), q = yW*rho - dW*R*/(r0*(1-R*)) predicts the SHAPE (monotone,
  concave) but overestimates fr* by ~0.07 — spatial self-shading of
  recycler patches, honestly unresolved.)

## Scoring extras
  + Patch-size distribution at equilibrium: alpha=1.70, 3.0 decades,
    n=457 (KS 0.185 — broadband mosaic structure at L2, claimed as
    broadband, NOT as criticality: KS is too big for a clean power law).
  + Visual drama: mosaic of interleaved guilds; kick turns the map
    producer-yellow then blue recycler islands re-nucleate INSIDE producer
    territory and grow back to the same global ratio (strips GE1_kick_*).
  + Real-world analogue: microbial cross-feeding / syntrophy (producer-
    recycler consortia), and textbook market clearing by marginal-return
    equalization.

## Negative results (deliverables)
  1. over=0 (no expression overhead): NO guilds — generalist a~0.5 wins
     (blending in strategy space). Bimodality REQUIRES the linear pathway
     overhead (over >= ~0.6 at margin 7; over/margin viability couples).
  2. over>=1.0 at margin<=4.5: total extinction (rent exceeds income at
     R<=1) — survivable window is margin/(1+over) in ~[2.6, 3.3].
  3. leak >= 0.7 at rho <= 1.8: recyclers never establish (W* below
     viability); leak <= 0.25: recyclers overrun (share_lo > 0.6) and the
     kick relaxes in <1.3k ticks (s23 < 2) — the G1 window is leak 0.5-0.65.
  4. DW=0.01: guilds fail (waste too local -> recyclers must sit ON
     producers; interleaving becomes cell-scale and mutation blurs it).
  5. hazard <= 3e-4: settle exceeds 60k (budget fail); hazard >= 8e-4:
     tau3 crashes to ~1.2k and s23 < 3 (turnover IS the market clock —
     tau3 ~ 1/hazard is the mechanism, sweep-verified).
  6. sig_mut <= 0.02: purity high but guild INTERLEAVING freezes; share_lo
     ~0.1 (recyclers can't nucleate in producer seas) — mutation supplies
     the market's "entrepreneurs".
  7. Flip-kick vs kill-kick vs dilute-kick: same tau3 (~4.4-5.7k at the
     L=64 anchor) — the relaxation is a property of the WORLD, not the
     perturbation protocol. Price-STEP (rho 2.2->2.6 live) also relaxes
     with tau ~5.2-6.0k to the new fr* — the law answers G3 dynamically.
  8. E2 lesson replicated: without hazard turnover the market freezes once
     space saturates (density compensation) — bankruptcy alone is not
     enough selection flux at equilibrium.

## Engine-integration sketch
  Fields: R (exists), W (new waste field: diffuse DW, decay dW, source
  yW*uptake_R), V/E (exist in E2 form), gene a (one more per-cell scalar,
  copy+mutate like E0/E1 genes). Params: cR, cW, yW, dW, m2 (all linear
  prices), hazard. Ports: cull-guild kick or cW modulation = the natural
  perturbation contract; guild ratio + relaxation tau + demand curve =
  certifiable laws. Storm compatibility: untested (out of scope).

## Files
  guild_econ.py (core physics), probe.py / probe_cert.py (protocols),
  sweep_*.py scan*.py g3*.py g4*.py gf_battery.py (search + certification),
  results.json (224 logged evaluations incl. all failures),
  strips/ (settle sequence, kick sequence, top-law fit, response curve),
  logs/ (raw run logs).
