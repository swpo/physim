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


## UPDATE (post P3/P4 campaigns)

### P3 BLOCKING — PASS (curve + 3 seeds + out-of-grid)
Wall = self-assembled B-stripe on the ridge (parkridge final state; static, spans y).
Cargo B pushed into it (tri, couple=(1,1)):
  eps      standoff (wall_x - cargo_x_compact_end)
  0.00125  15.74      0.00175  14.74      0.0025   14.18 (s0; s1=14.34 s2=14.36 noise seeds;
  0.003    13.39      0.00375  12.90       block_x16 from x=16: 14.19 = same attractor)
  0.005    destabilizes cargo at standoff ~12.9 (t~1750) -> honest eps_max(blocking)~<0.005
Monotone standoff(eps): stronger push compresses the w-cushion. Control (no wall): passes
ridge & destabilizes there. Wall holds its position & area under all cargo impacts
(x=48+-0.2, wall intact at run end; wall alone static at eps=0.00125 for 1500tu).

### P3 CHANNELING — PASS (capture curve + 2 noise seeds)
Rails = two x-aligned A'-stripes (self-organized from A'-row at eps=0.005 couple=(0,1),
L=80, y=8 & 24). B cargo drifts +x between them:
  y0:     9      10     11     12     14     16    | ctrl(no rails) y0=12
  y_rms:  7.8*   1.49   1.21   1.02   0.72   0.00  | 4.0 (then stripe at own y)
  y_end:  8.1*   15.1   15.3   15.3   15.5   16.0  | 12.0 (never centers)
  (*captured BY the rail at 1px gap — rail attracts at contact; capture basin edge
   between y0=9 and 10.) Cargo centered to channel centerline y=16 from any y0>=10,
   3-seed stable (s1/s2 identical to 1e-2). net_x ~ +6.5px while compact (then hits
   ridge zone & fattens: channel POSITIONING works; long-range convey needs isod mode).

### P4 RATCHET
- Noise ratchet (saw f=0.7, eps=0.0025 apex-parked, sigma=0.02/0.03, 3000tu):
  net |dx|<0.21px, v ~ -7e-6 px/tu. NO transport. HONEST NEGATIVE: B's positional
  diffusion under noise is ~zero (soliton too stiff); Kramers hopping unmeasurable.
- Deterministic saw current (no noise): direction follows tooth asymmetry
  (f=0.7 -> +x, f=0.3 -> -x mirror; conveys ~12px to first apex). Apex is absorbing
  (level b at apex crosses growth threshold at eps*P*f/2 too big) -> single-shot
  conveyor, not circulation. f=0.9/n3 apex at b=+0.036: still absorbs (grows there).
  k1-mode saw cannot circulate: cliff needs slope>eps_flip~0.0095 while |b|<0.03
  everywhere AND rising slope <0.0095 -- possible in principle (eps=0.003, P=16,
  f=0.85: cliff 0.017, apex 0.020<0.03) but teeth width ~ blob width -> averaging
  kills the cliff. PARKED: revisit in isod mode where level-kill is absent.

### NEW PRIMITIVE: iso-displacement coupling (mode="isod") — the SAFE dial
b(x) moves BOTH k1_i and k4_i along the M3 iso-background line: d_i(x)=d_i+c_i*b(x).
Reaction perturbation = c_i*b*(UB_ISO - w) -> vanishes at quiescent background
(zero-footprint force field; only felt under a blob where w deviates!).
- B drifts DOWN-d: v = -0.90*eps (eps 0.0025-0.01 measured, r2>0.999, area stays 30-32!)
- eps=0.01 SAFE in isod (vs k1-mode flip+shrink at 0.0095): no destabilization seen.
- A' same sign, v=-0.0059 at eps=0.005 (vs B -0.0044): ratio 1.33.
- Direction: blobs slide toward SMALLER d (bigger/softer species end of the line).
  DOWNSTREAM(isod) = -grad(d). Physically: blob chases the parameter point where its
  species is 'bigger' (lower k4, higher k1).
