# SUCCESSION TOWER — round-2 summary (fire-forest, 2026-02-17)

## Verdict
**PASS G1–G5 with 4 stacked layers** — and one honest structural finding:
the L4 law is **bistable relaxation to a pinned savanna–forest mosaic**
(Staver–Levin alternative stable states with a 14× hysteresis window in the
tree growth price), NOT a biome oscillation. Both stacking targets from the
brief are demonstrated: (a) bistability + hysteresis, (b) slow biome
relaxation law; fire-return clock is locally biome-modulated (totally:
mature forest never burns).

## Model (sf_core.py; W7 backbone untouched)
- Grass B, fire F: exactly round-1 W7 (theta=.78, Lam=9, M=2, D=8, gsig=.35,
  rho=.03, g=2e-3), except grass regrows into `1 − B − cT·T` (canopy shading).
- Trees T (slow): `dT = gT·e^u·(rhoT + (T+<T>nn)/2)(1−T) − mu·T − kapT·F·trap(T)·T`,
  trap(T)=logistic(−(T−Tm)/wm) → **fire trap**: fire kills saplings (T<Tm),
  mature canopy is fire-immune.
- **Fire–biome coupling (choice, justified):** flammability = sig(B−theta) is
  carried by grass fine fuel ONLY. Canopy shading keeps B<theta under forest,
  so forest is a self-maintained fuel break (mesic Staver–Levin regime).
  Negative control: making canopy flammable (veg_flam=0.8) destroys
  bistability — forest burns like grass and cannot exist. veg_flam=0.4 still
  bistable (choice is robust, not knife-edge).

## Hierarchy (best candidate S1, mixed-mosaic init, L=64, 60k ticks)
| layer | variable | timescale | adjacent sep |
|---|---|---|---|
| L1 fire front | hot residence | tau1 ≈ 2.0 | — |
| L2 fire events | event duration/size | tau2 ≈ 90–100 | 46–53× |
| L3 grass fire-return clock | phi_grass (switch, r2 .87–.90) | tau3 ≈ 1570–1965 | 16–21× |
| L4 biome field | meanT relaxation (r2 .95–.97) | tau4 ≈ 14000–17000 | **8.6–10.6×** |
Total span tau4/tau1 ≈ **7300–8600×** (gate: ≥3000×). All four variables
measured from the same run.

S1 params: gT=1e-4 (R=0.05), mu=1.5e-5 (W=0.15), kapT=1.5, Tm=0.45, wm=0.08,
rhoT=0.03, cT=0.5, patch_frac=0.30, Tinit_patch=0.62 + W7 fire params.

## Gates
- **G1 PASS (4 layers):** seps 46–53× / 16–21× / 8.6–10.6×, span 7300–8600×,
  65–107 events/run. L3 clock survives the tower (r2 0.86–0.90 vs 0.85
  tree-free control at same params).
- **G2 PASS (on L4):** relaxation fit on meanT r2 = 0.949–0.974 across
  4 seeds + 3 jitter draws. Plus alternative-stable-state evidence:
  savanna init → fF=0, forest init → fF=1 at identical params (3 seeds +
  2 full-jitter draws, 5/5 bistable).
- **G3 PASS:** forest-branch equilibrium T* vs tree growth price gT
  (mu, fire params absolute-fixed; 6 values × 3 seeds): 0.762, 0.817, 0.877,
  0.918, 0.945, 0.963 — smooth, monotone, seed-spread < 0.001. Bistable
  window edges also move with gT: forest collapses below ≈2.5e-5, savanna
  tips to forest above ≈3.5e-4 (hysteresis loop plotted).
- **G4 PASS:** S1 mosaic 4/4 seeds + 3/3 ±10%-jitter (all 15 params);
  bistability 3/3 extra seeds + 2/2 jitter draws.
- **G5 PASS:** 8 s per 60k-tick L=64 candidate (cap 300 s).

## The L4 story (honest)
The biome mosaic **relaxes** (tau4 ≈ 15k ticks) to a configuration pinned by
the static site-quality map: 150k-tick run shows fracF drift of only 0.005
after settling. So L4 is a *relaxation + bistable switch* top, not an
oscillator: no biome turnover cycle at L=64 without external climate
forcing or senescence waves (absent by design). Hysteresis is real and wide
(14× in gT). Fires never enter mature forest — FRI contrast is infinite
(41339 grass FRI samples vs 0 forest; burn count 15.45/cell vs 0.00/cell);
"locally modulated fire-return clock" holds in the strongest form.

## Negative results (first-class)
1. Flammable canopy (veg_flam≥0.8) destroys the tower's 4th layer entirely.
2. W = mu/gT ≥ 0.3: L4 never settles (r2 0.63) — senescence must be weak
   vs growth inside the window; forest branch dies below gT≈2.5e-5.
3. No 5th layer for free: pinned mosaic ⇒ biome oscillation requires new
   physics (climate wave), a deliberate omission per no-scripted-macro rule.
4. R=0.08 with kapT=0.8 (id 306/307): if trees grow too fast relative to
   fire kill, savanna slowly forests up and L4 fit degrades — succession
   slowness R ≤ 0.065 keeps layers separable. This bounds the brief's
   "~10x slower" intuition: at L=64/60k budget, R≈0.05 is the sweet spot.

## Files
sf_core.py, sf_measure.py; sanity_succ.py, wave0.py, pilot.py, bist_map.py,
sweepS1.py, gateS1.py, g3_succ.py, hysteresis.py, extra_probes.py,
bist_seeds.py, strips_S1.py, plots_final.py.
results.json (25 candidates incl. failures + maps + certification),
strips/: S1_macro_layers (all 4 layers, one run), S1_L4_treecover (mosaic
coarsening), S1_biome_vs_burns (fires avoid forest), S1_hysteresis_G3.png,
sanity_*.png.

## Engine-integration sketch
Add one World field `tree` (T) next to `fuel`,`fire`. Per tick: 4-neighbor
mean of T, logistic trap gate, three-term update (all O(L²) numpy). New
params: gT, mu, kapT, Tm, wm, rhoT, cT. Macro observables: mean(T),
frac(T>0.5), phi_grass (mask B>theta on T<0.3), per-biome FRI via last-burn
map (already O(L²)). Runtime x1.35 vs round-1 world.
