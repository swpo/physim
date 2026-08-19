# transport searcher — WORKING NOTES (checkpoint, updated as I go)
(files: results.json = append-only run log; data/*.npz = tracks+final fields)

## Anchors (dx=0.5 continuum, imexfft, node convention = M3-faithful at dx=1)
- eps=0 controls at dx=1 reproduce M3 EXACTLY (A 169px, B 25px; cmp_m3.py).
- **HONEST NEGATIVE: M3 species A is NOT a continuum object.** At dx=0.5 (imexfft AND
  euler dt=0.0025) A grows 36->3200 px^2 into a labyrinth (T=3000). M3-A compactness
  is dx=1 lattice stabilization. Iso-line replacement found: **A' = d=0.65**
  (k1_1=-1.56391, k4_1=2.05, Du=0.65): stable 36.25 px^2 >=2000tu at dx=0.5,
  10ktu longrun pending. d=0.55 marginal (grows at ~1900tu), d=0.6/0.65/0.7 stable,
  d<=0.5 all grow. Du dial does NOT rescue big-A (0.8/0.95 grow, 1.1 dies).
- B unchanged (30.25 px^2 at dx=0.5 = M3's 25 at dx=1 within refinement).

## P1 gradient/drift (tri profile, b=eps*(x-24) on rising branch, couple=(1,1))
- B curve (x0=24): v=+2.75*eps for eps in [0.00125,0.0095], r2>0.999 per fit.
  eps=0.0025: v=0.00677 (seeds 1/2/3 with noise 2.5e-3: 0.006777/0.006764/0.006791).
  dx=0.25 spot check: 0.006695 (-1.1%) => unpinned. DOWNSTREAM(B) = UP-gradient (+b).
- **FLIP bifurcation:** eps>=0.01 B reverses (v=-0.047 at 0.01, -0.024/-0.056 seeded
  0.0125), shrinks to ~17px^2 fast state, parks near trough. eps_flip in (0.0095,0.010).
- A'(d=0.65) curve: v=+4.4/3.9/3.8/3.6/3.2/2.7 x1e-3*[eps/1.25e-3...] — i.e. slope
  ~3.9x at low eps, 40% faster than B, same sign. BUT A' has tiny headroom:
  destabilizes (area>2x) at k1_eff ~ -1.55..-1.53 (static window edge -1.55 OK/-1.53
  grows), i.e. after climbing b=+0.02-0.03. 3 seeds at 0.0025 noise: v=0.0095/0.0109/0.0113.
- Level limits (static, dx=0.5, T=1500): B stable at k1_2=-1.62, grows at -1.59;
  A' stable at -1.55, grows at -1.53. B blob survives DOWN to k1_eff=-1.856 (flip run,
  shrunk state) — down-side never killed it in-run.
- Background integrity: no-blob world stays quiescent to <1e-4 dev at eps<=0.0125 dx=0.5.

## P2 selectivity
- couple=(1,1): same sign, A' ~1.4x faster at low eps — QUANTITATIVE selectivity only.
- couple=(0,1) demo: B feels naked ramp (v=+0.0154 at eps=0.0025, 2.3x the (1,1) value:
  shared-w backreaction cancels part of the ramp when both couple); A' with c1=0 still
  drifts -x at -0.0067 via w-landscape (NOT independent — w couples everything).
- OPPOSITE-SIGN candidate: eps~0.0105 => B flips (-x) while A' still climbs (+x). Demo TBD.

## P3 obstacles (design settled, runs TBD)
- Self-assembled STATIC WALL: B blob parked at ridge GROWS INTO A RIDGE-ALIGNED STRIPE
  (park_B_ridge, conv_probe final fields: clean stationary stripe spanning domain).
  Wall = autonomous structure held by the field ridge. Use as blocking obstacle
  with B cargo at eps=0.0025 (cargo parks at w-standoff BEFORE its growth zone).
  Control WITHOUT wall exists already (parkridge_eps0.0025: cargo reaches ridge & grows).
- Rails for channeling: wall16 run (A' row, couple=(0,1), eps=0.005) self-organized into
  x-ALIGNED stripes at 16px y-spacing with a gap at the ridge — usable as channel rails.
- Engine needs init_from (load saved F as IC) — implementing now.

## P4 ratchet
- Noise ratchet: B pinned under flat+noise up to sigma=0.03 (net<0.08px/800tu) =>
  positional diffusion too small; Kramers hops over 24px spacing astronomically slow.
  HONEST NEGATIVE (quantify D_eff).
- Deterministic saw transport observed: conv_probe (frac=0.7, eps=0.005): +12.4px to
  apex then grew (apex level b=+0.042 in growth zone — level kill). conv_mirror
  (frac=0.3): -12.2px, mirror-symmetric ✓.
- **CIRCULATION design from measured pieces:** need slope<eps_flip on long branch AND
  cliff slope=frac/(1-frac)*eps>eps_flip AND apex level b=eps*P*frac/2 below growth.
  saw frac=0.8 n_teeth=4 (P=24): eps=0.0027 -> cliff 0.0108>flip, apex b=+0.026 stable.
  Predict: B climbs 19.2px slowly, flip-crosses cliff, repeats => net conveyor current.

## Budget
dx=0.5 L=96: ~5.5-6 tu/s single job (3-4 parallel). 900-1500tu candidates = 2.5-4.5min B7 OK.
dx=0.25 700tu = 19min (one-off checks only). 10ktu longruns ~30min (one-off anchors).
