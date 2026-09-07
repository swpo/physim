# p4g2_044 / seed 928: privileged physics reconnaissance

**Status: complete, bounded first pass. Private evaluator material.**
This is a per-world coverage map, not an agent syllabus and not a decision to retain L1–L4.
No simulations, new seeds, ensembles, model calls, or evaluations were run.

## Main findings

1. **OBSERVED — spots, stripes, and a nonmonotone long-lag source outcome.**
   A few bright `u0` spots coexist with box-wide `u1` stripes. In the existing
   matched source branches, amplitude 1 leaves one extra `u0` segment at lag
   250, but amplitude 2 leaves none. Amplitudes 3 and 4 leave two and three.
   Even amplitude 2 still rearranges `u1`. This is one anchor and noise path,
   not a universal dose law.
2. **OBSERVED — duplicated activators do not have duplicate morphologies.**
   `u2` and `u3` have high positive backgrounds and negative defects. Late in
   this cache, `u2` has a few small holes; `u3` has long branched dark filaments.
   `u2` is elevated where `u3` is negative. Their identical feedback rows and
   shared channel drives suggest a compensation mechanism, not independent
   species dynamics or a conserved population.
3. **OBSERVED — a localized thresholded channel can be almost invisible at
   both home probes.** `x7` has nonzero spot-associated halos in the full field
   while its two home readings are tiny at t=1700. It becomes readily visible
   at device A later. It is also the weak bridge from `u0` to the `u2/u3`
   subsystem. Small cross-group responses are useful coverage, not a reason
   to discard this subsystem.

**Labels.** OBSERVED means a listed figure was actually viewed or a stated
quantity was measured from the cache. HYPOTHESIS means a mechanistic reading
consistent with equations and measurements. NOT YET TESTED marks a proposed
experiment or a claim beyond these data. Equations alone are not empirical
proof of the hypotheses.

## 1. Evidence and access

### Data actually inspected

- Base cache: `probes/blobs/agentenv/cache/p4g2_044_s928.npz`.
  `frames` is `(501,12,256,256)`, float16, t=0…2500 at 5tu cadence.
  The box is periodic, L=128, dx=0.5. `snapF_1700` is float32.
- Existing branches: `p4g2_044_s928_branches.npz`.
  `control`, `calib1`, `calib2`, `announced`, and `calib4` each have
  `(51,12,256,256)` full-field frames. All start at t=1700. Sources act on
  `u0`, amplitudes 0/1/2/3/4, for 10tu at original device-A home.
  `adequacy.py:build_cache` restores the same state **and RNG** for each.
  Control and main-cache frames are exactly equal in stored float16 at the
  seven inspected lags: 0,5,10,25,50,100,250.
- `cache/round5/r5_p4g2_044_s928_truth.npz` was inspected for layout only.
  Its truths are sensor arrays and event counts, **not 2D fields**.
- Full base-field measurements here use t=0,250,750,1700,2500. Native blob
  records span all 501 frames. Branch measurements use the seven lags above.

The four figures below were loaded with `attach_image` and actually inspected:

| Figure | What it shows |
|---|---|
| [activators_time.png](activators_time.png) | Full 2D activators at five times, fixed color scale per row |
| [all_fields_t1700.png](all_fields_t1700.png) | All 12 fields, separate raw scale per panel, home probes overlaid |
| [native_segments.png](native_segments.png) | Native thresholded component counts and above-threshold areas |
| [paired_source_fields.png](paired_source_fields.png) | Full control/treatment fields and paired differences for amplitude 3 |

### Native sensor interface

`device.py` samples scalar fields by periodic bilinear interpolation. The
base devices have 13 and 19 slots. Agents receive anonymous ports and slots,
plus per-port global means and variances; they do not receive these field
names or coordinates. `blobcore.py` supplies the home geometry and fixes the
source at original device-A home for replica experiments. Passive sensor
motion must not be confused with motion of the emitter.

All indices here are zero-based. The privileged map for this realization is:

| Field | u0 | u1 | u2 | u3 | x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Port | 4 | 5 | 11 | 7 | 0 | 8 | 1 | 10 | 2 | 9 | 3 | 6 |

In this native interface, ports 7 and 11 are scalar activators, not angles.
This map is private and is not a proposed hint to the predictor.

## 2. Equations that constrain the explanations

From the world JSON and `sim_cpu.py:advance`, with `z_i = u_i-u0_i`:

```
∂t u_i = D_i ∇²u_i + λ_i u_i - u_i³ + k1_i - Σ_c K_ic x_c + noise_i
∂t x_c = D_c ∇²x_c + (drive_c - x_c)/τ_c
```

There are no bilinear terms in this genome. Reaction is explicit with old
activators in channel drives. Diffusion is spectral. The native step is
0.02tu; activator noise uses `0.002*sqrt(dt)` per grid/substep. These facts do
not establish chaos. Signed feedback channels are not conserved densities.
In particular, a negative channel value can **increase** an activator via
`-K*x`.

The architecture is unusually informative:

- `x0` is driven by `z0`; `x1` by `z0 + 0.5*z1`; `x2,x3` by `z1`.
  `u0` receives `x0 + 1.5*x1 + 0.012734*x7` as its subtracted feedback.
  `u1` receives `2.05*x1 + x2 + 0.147247*x3`.
- `x4,x5,x6` all receive **the same drive** `S=z2+z3`.
  The `u2` and `u3` feedback rows are exactly equal:
  `1.964060*x4 + 0.812359*x5 + 0.308166*x6 + 0.012734*x7`.
  Their local cubic parameters and diffusion differ. Subtracting their two
  equations cancels the channel-feedback term, but does not conserve their
  difference or force synchronization.
- `x7` has drive
  `0.105719 * Σ_{i in {0,2,3}} tanh(max(z_i-0.659104,0)/0.303073)`.
  **There is no u1 input.** Its feedback to `u0,u2,u3` is weak and identical
  in coefficient. This is the only route from `u0` into `u2/u3`.

Selected channel scales are below. `sqrt(D*τ)` is an equation-derived
steady filtering length, **not a measured propagation radius**.

| Channel | τ (tu) | D | sqrt(Dτ) | Role to test |
|---|---:|---:|---:|---|
| x1 | 0.7 | 20 | 3.74 | Fast shared feedback for u0/u1 |
| x3 | 28.464 | 0.03183 | 0.952 | Slow, spatially narrow u1 feedback |
| x4 | 78.885 | 11.9509 | 30.70 | Broad, slow common-drive field |
| x5 | 1.882 | 5.0901 | 3.10 | Faster, more local common-drive field |
| x6 | 6.085 | 8.6009 | 7.23 | Intermediate common-drive field |
| x7 | 52.283 | 0.42444 | 4.71 | Thresholded local-history candidate |

## 3. P1 — spots embedded in stripes; nonmonotone persistence

### OBSERVED

At t=1700 `u0` is mostly negative with four small positive segments. `u1`
forms a bright labyrinth across the box. Away from positive `u0` spots,
`u0` and `u1` pixel values have correlation **-0.7397**. The dark stripe
imprint in `u0` is visible; the measured sign agrees with shared feedback.
This is not a fitted traveling-wave or rotor model.

The matched branches reveal more than a dose-response magnitude:

| Source amp, dur=10 | u0 segments, lag 10 | lag 50 | lag 250 | max abs Δu0, lag 250 | max abs Δu1, lag 250 |
|---|---:|---:|---:|---:|---:|
| control | 4 | 4 | 5 | 0 | 0 |
| 1 | 5 | 5 | 6 | 1.8350 | 2.3037 |
| 2 | 5 | 4 | 5 | 0.1577 | 2.2402 |
| 3 | 5 | 6 | 7 | 1.9932 | 2.3594 |
| 4 | 5 | 6 | 8 | 1.9858 | 2.4199 |

Counts use the native positive-segment threshold `u0>0.2541601` with
periodic labeling. They are not organism identities. The positive spots
have peaks near 1.07 and a negative background; the extra peaks are not
small noise excursions around the count threshold.

The amplitude-3 image shows two additional bright spots and displaced
stripes at t=1950, **240tu after source shutoff**. They lie near `(y,x)` =
`(73.84,78.44)` and `(73.04,97.92)`, not at the original source center
`(71.14,107.63)`. We did not track their lineage or measure their speed.
Alternating positive/negative `u1` difference bands are consistent with
stripe displacement, not merely a change in stripe height.

The immediate max `|Δu0|` at lag 10 increases with dose: 2.067, 2.270,
2.420, 2.537. The long-lag localized-state outcome does not. Amplitude 2
is especially valuable: **no extra u0 segment is not no physical effect**.

### HYPOTHESIS

The cubic response plus spatial and delayed feedback can support distinct
localized outcomes. An intermediate pulse might lose its induced spot
through feedback charging or geometry, while a weaker pulse survives and
stronger pulses reorganize the local pattern. The equations and images
support investigating this explanation; they do not identify the mechanism.

### Compact experiment and private query

- Existing cached comparison: same anchor, control versus amplitudes 1,2,3.
  Read `u0,u1,x7` through both the pulse and the source-off tail. Keep a
  witness near the altered pattern, not only at device B.
- **NOT YET TESTED:** compare equal integrated sources with different
  duration, such as amplitude 1 for 20tu versus amplitude 2 for 10tu. A
  nearby-anchor comparison can test sensitivity to local stripe state.
  A matched shared-feedback preconditioning trial could separate feedback
  loading from a purely local amplitude explanation. No such trial was run.
- Private predictor coverage: complete source schedules from opaque `t0`
  and anonymous query IDs/times, with source timing and witness selection
  made privately. Include an immediate pulse, a no-extra-spot tail, and a
  persistent-extra-spot tail. Score coupled stripe and halo outputs from
  full returned arrays, not just a monotone source scale or a final count.

## 4. P2 — asymmetric negative defects and shared feedback

### OBSERVED

The time montage makes the polarity important: `u2/u3` have positive
backgrounds and dark negative defects, unlike the bright-on-low-background
`u0/u1` structures.

| Time | Fraction u2<0 | Fraction u3<0 | corr(u2,u3) |
|---|---:|---:|---:|
| 250 | 0.03067 | 0.07359 | -0.2941 |
| 750 | 0.03151 | 0.15971 | -0.2730 |
| 1700 | 0.00641 | 0.21118 | -0.3596 |
| 2500 | 0.00470 | 0.21706 | -0.3910 |

At t=1700, mean `u2` is **1.76253 where u3<0**, versus **1.54246 where
u3>1**. The full images show this elevated counterpart along the dark
`u3` filaments. The few `u2` holes and extended `u3` worms are not equivalent
phenotypes merely because they share feedback.

The common-drive channels also differ visibly. At t=1700 their spatial
standard deviations are `x4=0.01783`, `x5=0.49941`, `x6=0.18711`. `x4`
is broad and smooth; `x5` resolves the negative-domain geometry.
Their means are:

```
<S>  = -0.29446384
<x4> = -0.29256329
<x5> = -0.29441378
<x6> = -0.29433179
```

For a periodic box, their equations imply
`d<xc>/dt = (<S>-<xc>)/τc`. Diffusion contributes no spatial-mean change.
This is a useful sensor-accessible relation because global means are
available. These five snapshots are a consistency check, **not an empirical
fit or validation of all three relaxation times**.

### HYPOTHESIS

A negative excursion of one activator reduces the shared drive. Through
signed shared feedback, this can permit a higher background in its partner.
This matches the observed spatial compensation. Different local cubic
parameters and diffusion may account for the very different defect shapes.
Direct interventions or ablations are needed to establish either cause.

### Compact experiment and private query

- Use a sensor pose that straddles a negative-domain boundary. Read both
  activators and all three shared channels, plus their global means. Compare
  local compensation with the common global-drive relation.
- **NOT YET TESTED:** matched positive-source trials in `u2` and `u3`, with
  high/low starting states checked first. Test the partner's sign and delay,
  rather than assuming equal response from equal feedback rows.
- Private coverage: select boundary witnesses and source times privately.
  Calls still contain only complete schedules from `t0` and anonymous
  queries. Score the joint response of smooth `x4`, structured `x5`, and
  both activators from the returned arrays. The global-mean relation is
  exploration evidence, not a future driver-history input to the predictor.

**Important descriptor gap.** At t=1700 the native positive thresholds label
81.35% of the box in `u2` and 44.49% in `u3`, yielding only two positive
components each. These components often include a large background region.
They do not justify “two organisms,” global death, or population conservation.
Ports 7/11 should not be treated as angle variables just because they switch
between high and low scalar states.

## 5. P3 — thresholded local history and meaningful quiet regions

### OBSERVED

The gate's absolute opening levels are approximately `u0>-0.02073`,
`u2>2.05978`, `u3>2.02871`. At all four inspected late times, no grid cell
of `u2` or `u3` crosses its gate. At t=1700 about **1.048%** of `u0` cells
do. Initial dressed seeds do cross the `u2/u3` gates, so the late-state
statement is not an all-time architectural invariant. No claim is made
about uninspected intermediate frames.

At t=1700, `x7` has visible halos centered near the bright `u0` spots:

| Observable | x7 value |
|---|---:|
| full-field maximum | 0.0272217 |
| full-field mean | 0.0009655 |
| full-field standard deviation | 0.0028526 |
| largest device-A home reading | about 0.0000243 |
| largest device-B home reading | about 0.0000010 |

At t=2500 the largest A reading is **0.0204594**. Earlier quiet readings
were a spatial sampling limitation, not a dead channel.

The amplitude-3 branch gives a second view. At lag 250, full-field max
`|Δx7|=0.0283793`, and A sees up to 0.0157993 of paired halo change even
though A's maximum `|Δu0|` is only 0.09665. The extra `u0` spots now lie away from
the source center; the halo need not coincide with a current
positive `u0` reading at a particular slot.

Cross-group effects are small but not uniformly zero. For the same branch
and lag, max full-field `|Δu2|=0.0009766` (near one float16 field increment)
and max `|Δu3|=0.0126953`. A's `u2` samples are exactly equal in the stored
comparison, but that does not prove exact dynamical invariance. B misses
most of the small `u3` effect. The global and A measurements prevent the
incorrect conclusion that nothing happened anywhere.

### HYPOTHESIS

`x7` is a localized low-pass history of above-gate excursions, mainly `u0`
spots at these late states. The only `u0` path to `u2/u3` passes through
this weak gated channel, consistent with their small paired responses.
A persistent spot also continuously drives `x7`; a halo by itself does
**not** establish memory after its driver disappears. The measured decay
time and separation of persistent drive, diffusion, and memory remain open.

### Compact experiment and private query

- Passive, matched-state reads at a spot, its halo, and a remote patch can
  already use the cache. Record all ports and global moments. Check that
  moving the passive sensor changes local readings but not the global field.
- **NOT YET TESTED:** source-off records where the local driver falls below
  gate, with controls for a spot moving past rather than dying. A direct
  `x7` perturbation can test relaxation only if changes in gated drive are
  checked, not assumed absent.
- Private coverage: coupled `u0/x7` predictions for anonymous query
  IDs/times, privately chosen to sample quiet locations, halos, and source-off
  tails under the complete action schedule from `t0`. Retain nearly invariant
  `u2` targets beside nonzero changes in other fields. Do not select only
  targets with large response or supply witness geometry to the predictor.

## 6. What this recommends for R6, and what it does not

This first pass suggests three **coverage axes**: localized-state outcomes
within a stripe field; complementary negative-domain dynamics with shared
filters; and gated local history with spatial observability gaps. They are
not a mentor curriculum or a fixed contract menu.

**R6 interface alignment.** The predictor has a fixed opaque `t0` and the
entry point `predict(actions, queries, n_samples, seed)`. It receives the
complete action schedule from `t0` plus anonymous query IDs/times. It receives
**no history, anchor, field name, or geometry input**. Histories in the
experiments above are exploration evidence. Anchors and boundary locations
are private evaluator choices, not extra predictor arguments. Selected
fields/slots can be scored privately from the returned full arrays. The
existing t=1700 branches are reconnaissance cases, not automatically valid
R6 calls; root must map any retained case to a schedule reachable from its
chosen opaque `t0`.

For executable-predictor evaluation:

1. Hide target futures until the predictor is sealed. A forecast scored
   inside a readable cache can otherwise be interpolation, not learned
   dynamics. Existing branches are useful private sanity cases, not evidence
   of extrapolation if their outputs were available during exploration.
2. Use genuinely paired state/RNG control and source truths when evaluating
   a treatment response. Predicting treated absolute streams and subtracting
   a different undisturbed replay mixes effects with other error sources.
   **Root design gate:** the current R6 `policyA` runner keeps shams on the
   base RNG but reseeds at the first effective treatment. It does not supply
   the proposed matched-sham noise coupling. The common-RNG result above is
   about the legacy `adequacy.py` cache builder, not that current runner.
3. Include joint outputs that distinguish mechanisms: `u0` *and* stripes;
   duplicate activators *and* shared channels; spot values *and* halos.
   Local raw streams and global moments are accessible. Full-field topology,
   field names, source geometry, and gate-active masks are privileged here.
4. Include informative nulls and witness failures. A quiet remote probe,
   a no-extra-spot outcome, or a nearly invariant partner field can be a
   correct physical prediction. Check other locations/fields before calling
   an intervention globally null.

No universal source threshold, invariant species ranking, fitted rotor,
chaos claim, spot velocity, conserved population, or full mechanistic law
is established. The metadata describes a T=20000 run and uses “rotor” and
interest scores; this report does not use those labels as proof for the
0…2500 cache. No `h9 v0` ranking or threshold was used.

The E1 process/concurrency audit was read for cautions, not as field data.
No E1 agent observations entered these measurements. In particular, the
approximately 0.0021 passive-predictor L4 MAE is **not** used as an exact
paired intervention response. R5 sensor-only truth was not promoted to
full-field evidence.

## 7. Artifacts and reproduction

- [evidence.json](evidence.json): structured claims, maps, source hashes,
  selected raw/sensor measurements, branch counts/differences, and limits.
- [cache_layout.json](cache_layout.json): NPZ member shapes and dtypes.
- [first_look.json](first_look.json): raw selected snapshots' statistics,
  device samples, secrets, and metadata.
- [measurements.json](measurements.json): detailed paired branch measurements
  and morphology/gate diagnostics. Raw-field order is documented there.
- `cache_access.py`: read-only mmap for ZIP_STORED NPY members. No large
  cache extraction or full-array float32 conversion.
- `inspect_cache.py`, `first_look.py`, `measure_fields.py`: reproducible
  analysis/plotting scripts. They never call a stepper or simulator.

From repository root, if regeneration is wanted later:

```text
~/.venvs/bk3/bin/python probes/blobs/agentenv/round6/physics/p4g2_044/first_look.py
~/.venvs/bk3/bin/python probes/blobs/agentenv/round6/physics/p4g2_044/measure_fields.py
```

The analysis scripts set native thread limits to 1. Only individual frames
are promoted to float32 (about 3 MB each; the first montage keeps five).
Peak RSS was not measured. The final measurement/paired-plot pass completed
in about 1.45 seconds. The already completed first montage was not rerun.
All outputs are inside this owned directory; no shared files were edited
and no commits were made. Any new controlled simulation listed above needs
separate authorization.
