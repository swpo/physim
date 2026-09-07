# p6g8_033 / seed 942: first-pass physics coverage

**Private evaluator-side evidence. Not an agent prompt, syllabus, or fixed contract menu.**

This pass first inspected this world's equations and native full 2D fields. It then
checked a small set of existing paired branches. It did not run a simulation,
generate truth, fit a model, or evaluate an agent. All proposed experiments below
are **NOT YET TESTED** unless an existing cached observation is stated explicitly.

## 1. Scope and direct visual evidence

The native base cache contains **501 × 13 × 256 × 256 float16 values**, on a
128 × 128 periodic domain, at t=0,5,…,2500 tu. It also holds a float32 field and RNG
snapshot at t=1700. This is not the genome summary's 20,000-tu evaluation.
The genome's labels “growing rotor ecology”, “liquid”, and “42 organisms” are
archived descriptors, not findings independently established here.

All five linked figures were actually viewed with `attach_image`:

- [All activators, five times](initial_activators.png): positive u0 spots/ridges,
  dense curved u1 ridges, and negative u2 cores in a positive background.
- [Channels X0–X4](initial_channels_0_4.png): different spatial shadows of those structures.
- [Channels X5–X9](initial_channels_5_9.png): u2-linked cores, the X7 shadow, and a quiet X9.
- [Late polarity, broad halo, quiet control](late_polarity_and_quiet_control.png):
  late-only explicit scales expose the X4 halo and remove an initial-figure artifact.
- [Matched pulse field differences](matched_branch_fields.png): direct spatial
  evidence for the existing act0 pulse, including positive and negative responses.

**Plot caution:** the initial X9 row has a degenerate zero range. Matplotlib's
colorbar normalization makes its final zero panel a different color. This is not
physics. All five displayed X9 arrays are zero at stored float16 precision. The
late control figure uses an explicit nonzero plotting range and is the correct
visual reference for X9. Initial X4 panels also hide the weak late halo because
the fixed scale includes its much larger initialization pulse.

`initial_stats.json` and `offline_checks.json` retain the numerical observations.
`evidence.json` records claim status, source hashes, array headers, and exclusions.

## 2. Rules: three activators, ten filters, two gated drives

Here **u0,u1,u2 are field indices**, not anonymous port IDs. Let
`b=(-0.679836269,-0.867559241,1.400673798)` and `z_i=u_i-b_i`.
The following continuum-style notation summarizes the implemented reaction and
diffusion rules; the actual solver uses the discrete split update described below.
Coefficients are rounded here; the genome JSON is authoritative.

```text
du0/dt = 1.082673 ∇²u0 + 1.948010 u0 - u0³ + 1.010123
         - X0 - 1.5 X1 - 0.012734 X7 + noise0

du1/dt = 0.65 ∇²u1 + 2 u1 - u1³ + 1.082142
         - 2.05 X1 - X2 - 0.147247 X3 + 1.195591 X0 X6 + noise1

du2/dt = 0.441146 ∇²u2 + 2.852402 u2 - u2³ - 1.247321
         - 1.964060 X4 - 0.812359 X5 - 0.308166 X6
         - 0.012734 X7 - 0.069270 X8 + 0.684814 X9 + noise2

dXc/dt = Dc ∇²Xc + (qc - Xc)/tau_c
h(z;theta,s) = tanh(max(z-theta,0)/s)
```

| Channel | Drive q | tau (tu) | D |
|---|---|---:|---:|
| X0 | z0 | 3.4792 | 1 |
| X1 | z0 + 0.5 z1 | 0.7 | 20 |
| X2 | z1 | 3 | 1 |
| X3 | z1 | 28.4640 | 0.031828 |
| X4 | z2 | 78.8855 | 11.95086 |
| X5 | z2 | 1.88223 | 5.09013 |
| X6 | z2 | 6.08507 | 8.60088 |
| X7 | 0.105719[h(z0;0.659104,0.303073) + h(z2;0.659104,0.303073)] | 52.2826 | 0.424444 |
| X8 | z2 | 1.81195 | 1.45941 |
| X9 | h(z2;0.367424,0.208182) | 17.4916 | 7.02735 |

The positive bilinear term in du1/dt is intentional: the stored coefficient is
negative and the implementation subtracts it. X6 therefore changes the local
u0-channel-to-u1 coupling with location and sign. It is not a generic all-to-all
three-species competition model.

**Rule implications, not causal ablation results:**

- X1 is a fast shared inhibitory channel for u0/u1. X3 is a slower, very local
  u1-driven inhibitor. X7 is a weakly coupled, slower gated trace.
- X4 is a slow, broad u2-linked field. The isolated linear filter's screening
  length `sqrt(D*tau)` is about 30.7 world units, versus about 0.95 for X3.
  These are equation scales, not fitted propagation lengths.
- X9 has a positive feedback sign into u2, but its endogenous drive is gated.
  A passively quiet X9 need not be an ineffective actuator when directly injected.
- These are signed reaction fields. There is no asserted conserved population,
  positivity law, organism identity, or thermodynamic interpretation.

`sim_cpu.py:59–213`, `sim_v1.py:1–18,58–89`, and `device.py:242–293` specify
`dx=0.5`, `dt=0.02`, periodic exact Fourier diffusion, explicit reaction using old
activators for channel drives, and additive activator noise of amplitude
`0.002*sqrt(dt)` per step. Channels do not receive that direct noise. Injection
is a Gaussian source of sigma=2 world units, applied before each reaction step;
it is not a one-off state replacement.

## 3. Candidate phenomenon A — evolving ridges and delayed local state

### OBSERVED

At t=250,1000,1700,2500, u1 has curved extended high-value ridges whose layout
changes. u0 has strong positive spots and later long ridges, together with weaker
banded modulation. X0 resembles the u0 pattern; X1 contains broad bands and spot
shadows; X2/X3 carry u1-linked bands; X7 highlights the u0 active regions with a
smoother trace. These are full-field observations, not inferences from one sensor.

For example, spatial standard deviations of u0 are 0.229,0.241,0.355,0.469 at those
four times. For u1 they are 0.669,0.858,0.837,0.767. More u0 contrast is **not** a
measured population growth rate. Curved bands are **not** proof of a rotating
spiral, a winding number, or a wave speed.

### HYPOTHESIS

The shared X1 inhibition and slower X3 state could make u0/u1 ridge interactions
and recovery depend on recent local history. An instantaneous u1 value alone may
not tell whether a site is entering or recovering from an active episode. The
rules support this possibility; the montages do not isolate it causally. X7 may
also retain a useful delayed trace, but its small feedback coefficient does not
by itself prove it controls the observed reorganization.

### Sensor observability and compact discriminating test — NOT YET TESTED

At the existing home arrays, this is not a hidden-in-space phenomenon. Across
stored t=250…2500 and slots, port2=u1 ranges roughly -1.30…1.22 and port4=X3
roughly -0.36…1.38. Port7=u0 and port11=X7 are also variable.

A compact test can use a fixed patch and a short multi-port history. Compare a
small **port4/X3 pulse and sham from the same anchor, pose, and noise path**.
Observe port2/u1 and the faster linked port6/X2 during and after the pulse. Repeat
at a second local phase identified from pre-pulse sensor history. A delayed
suppression/recovery contrast that depends on phase would support a local
history effect. A response explained equally well by current readings alone is
a useful negative result. Do not choose the phase using future truth.

**Private held-out predictor queries:** supply the complete action schedule
from the fixed t0 and query times, using anonymous device/port IDs. Do not supply
sensor histories, an anchor state/time input, or sensor geometry. The investigator
may use histories during exploration; the private grader may use its own history
to select schedules that reach rising or falling local phases. Assess signed
recovery at privately selected slots of the returned **full device arrays**.
Keep native field labels and the causal interpretation private. This is a
coverage axis, not a required investigator method.

**Missing:** dense phase/feature tracking, controlled pathway tests, and evidence
that a learned history dependence transfers to unseen anchors. No rotation law,
refractory time, or complete effective dynamics has been measured.

## 4. Candidate phenomenon B — persistent negative cores and meaningful quiet channels

### OBSERVED

Using the explicit diagnostic mask **u2<0**, periodic connected components number
**four** at each of t=250,1000,1700,2500. Their combined area is
261.25,265.25,268.5,267.5 square world units, about **1.6% of the domain**. These
are negative cores within a positive background, not positive u2 blobs under an
unstated threshold. This mask is a morphology diagnostic, not an organism claim.

They are long-lived in the sampled views but **not pinned**. Matching the four
visually corresponding components gives t=250→2500 centroid displacements of
about 0.34,5.83,6.00,2.52 world units. Mask overlap with t=250 falls to 0.345 by
2500. Sparse views cannot prove there was no intermediate splitting or merging.

X4, X5, X6 and X8 show different-width shadows around the negative cores. The
late-only X4 figure reveals a broad nonuniform halo that the initial-scale plot
nearly hides. At t=1700, full-field u2 std is 0.36046. Yet the two home arrays see
u2 only around **1.405–1.409**, with pooled time/slot std about **0.00054 and
0.00048** over t=250…2500. A nearly flat port0 at home is therefore a sampling
fact, not evidence that u2 is globally inactive. The free global variance can
expose this discrepancy even without full-field access.

**A distinct quiet control:** X9/port3 has zero nonzero float16 cells at every
saved late time t=250…2500; its last nonzero stored frame is t=140. The t=1700
float32 snapshot retains about **6.2e-43**, so “exact physical zero” is too strong.
At all saved late times, `max(u2)<=1.556641`, below X9's positive-drive threshold
`b2+0.367424=1.768098`. That is consistent with a closed gate and decay. It does
not inspect the intervening 0.02-tu substeps or prove future gate closure.

### HYPOTHESIS

The u2 subsystem supports slowly drifting, opposite-polarity localized states
with spatially extended filter shadows. Its negative cores may modify local u1
behavior through X6 and the X0*X6 term. Neither the stability mechanism nor that
cross-subsystem influence has been isolated. X9's quiet late signal is consistent
with unforced relaxation below threshold, not loss of a species or an absent
coupling.

### Sensor observability and compact discriminating tests — NOT YET TESTED

- Compare a local cross-scan at a heterogeneous patch and a return scan at the
  same pose. Read port0=u2 with port12=X4 and the sharper port10=X8. Core, edge,
  and background measurements can distinguish a localized state and broad halo
  from a globally uniform field. A small background-only scan is a valid null,
  but it cannot settle the global question. Both present home arrays miss cores;
  finding or supplying a covered patch is a real acquisition requirement.
- For the gate, compare matched sham and two allowed-strength positive u2/port0
  pulses at one patch. Check whether **measured** u2 crosses the gate region and
  whether port3 develops a delayed response. If no tested dose crosses it, report
  “threshold not reached”; do not call the channel dead. A direct small port3
  pulse is a possible separate instrument/feedback positive control. No such
  threshold or direct-channel experiment was run here.

**Private held-out predictor queries:** choose complete t0 action schedules
whose anonymous adjustment commands place arrays in background-null or core/halo
regions. Provide those schedules and query times, not coordinates, geometry,
histories, or anchor inputs. The grader can privately select relevant slots from
the returned full device arrays. Include passive quiet port3 continuations and,
after a pilot establishes accessibility, subthreshold versus gate-opening pulse
conditions. Reward correct quiet predictions where quiet is the physics. Do not
require every port to be variable.

**Missing:** controlled stability/relaxation tests, an efficient sensor search
for the remote cores, substep evidence for gate closure, and pulse conditions
that actually cross the gate within apparatus limits. No multi-seed generality.

## 5. Candidate phenomenon C — a short pulse leaves a long spatial rearrangement

### OBSERVED: a genuine native matched contrast, but only one noise path

`p6g8_033_s942_branches.npz` contains control and amplitudes 1,2,3,4 of a
**u0/port7** source for 10 tu, from t=1700 at device A's home. All four initial
branch frames equal control. **All 51 control frames exactly equal the base
frames t=1700…1950 at stored float16 precision.** The build source restores the
same float32 snapshot and RNG for every branch. This is much stronger evidence
than pairing different E2 trace anchors or interpreting an agent's MAE.

The figure shows amplitude3. At lag10 the pulse gives a local positive u0 peak
and mainly negative u1 bands near A. At lag50, after the source has ended, the
perturbed u0 field has extra local peaks. By lag250, u0 and u1 differences have
both signs around displaced/rearranged ridges and spots, including the witness
region. These facts support a conditional pulse-induced pattern change. They do
not establish a nucleation threshold, feature lineage, chaos, or a propagation law.

| Amplitude3, lag (tu) | Full-field mean Δu0 | Full-field mean Δu1 | Full-field RMS Δu0 | Full-field RMS Δu1 | B-slot RMS Δu1 |
|---:|---:|---:|---:|---:|---:|
| 10 | 0.01258 | -0.01919 | 0.1474 | 0.1853 | 0.00122 |
| 50 | 0.00681 | -0.01033 | 0.1100 | 0.2223 | 0.06021 |
| 250 | -0.00097 | -0.00014 | 0.2825 | 0.3641 | 0.79032 |

Δ means **perturbed minus matched control**, not forecast error. At late time,
substantial signed local changes almost cancel in the global mean. A predictor
of global means alone could miss this physics. At B, u2 remains far less changed
(RMS about 8.5e-5 at lag250), and stored X9 stays unchanged. The small u2 contrast
is below a typical float16 step near its background value; it does not resolve
an exact small physical effect. These are useful within-experiment controls,
not worthless channels.

Amplitudes1/2/3/4 also differ: B-slot u1 RMS at lag250 is about
0.0285/0.7617/0.7903/0.8110. This is **one dose series at one phase, one emitter,
one duration, and one noise path**. It is not a fitted response law or a proven
threshold. A wave crest arriving at B can change this summary without a new
universal dynamical regime. The archived R5 exploration tools cap amplitude at1;
that fact does not establish the R6 exploration limit. The inspected R6 prototype
has a proposed evaluation range0…3 (`blobround6.py:25`), not a declaration that all
these doses are available during exploration. The native amplitude4 observation
is not automatically an R6 query case. Any exploration/query range mismatch must
be explicit in the root policy.

### HYPOTHESIS

A local u0 excitation can suppress nearby u1 through the shared X1 drive, then
change the coupled pattern's subsequent timing/shape. Early u1 suppression is
consistent with that pathway. Later mixed signs suggest pattern rearrangement,
not a permanent spatially uniform increase. Source equations and this matched
response motivate the hypothesis; they do not identify the sole mechanism.

### Sensor observability and compact discriminating test — NOT YET TESTED

A and B are about23.93 world units apart. Both local and remote streams can
observe the response, but the remote early change is tiny. Use a matched sham
and two **allowed** positive strengths at one anchor/pose, with the same noise
path within each pair. Record a short A/B multi-port series and a few later
witness times. Then use a second anchor selected from a different observed
pre-pulse local phase. Replicate pairs under independent noise paths only if
estimating a distribution rather than this one-path contrast.

This separates direct signed response, later rearrangement, phase dependence,
and noise variation. It does not require an agent to use a particular model.
Matched continuation noise is a **proposed scientific requirement**, not a current
R6 runner guarantee: policy A's no-op sham and treated case follow different noise
semantics. See the unresolved comparison gate in Section6. The controlled future
simulations need separate authorization; none were run.

**Private held-out predictor queries:** provide the complete declared action
schedule from the fixed t0, including any pulse or sham, plus query times.
Do not provide observed histories, anchor inputs, or sensor geometry. The private
grader can select schedules with different pre-pulse phases using its own
history. Vary in-range dose and score near/remote slots privately within the
returned full device arrays. Assess **signed sensor outputs**, not only an RMS
magnitude or global response. Include u2/X9 control outputs. Any dose outside the
actual exploration range belongs to an explicitly separate extrapolation question,
not an unmarked test of learnable in-range physics.

**Missing:** repeated noise paths, other emitters/anchors/durations, paired
small-dose data below1, and spatial feature tracking. The existing dose series
cannot establish a general propagation speed, bifurcation, or irreducible error.

## 6. Private coverage map and separation from the old evaluation

These are **three scientific coverage directions**, not six replacement L1–L4
contracts. The fixed-t0 executable predictor receives complete action schedules
and query times, with anonymous device/port IDs. It does **not** receive histories,
anchor states/times as separate inputs, or sensor geometry. The public investigator
need not receive these mechanisms, port meanings, prescribed experiments, or
private query selections. Histories can guide exploration and the private grader's
phase selection; they are not predictor inputs. The grader may score selected
slots of returned full device arrays without requesting a slot subset from the
predictor. A held-out query should not merely ask for a value already stored in
the investigator's record. Query generation, policy, scoring, and the public
interface belong to the root specification, not this reconnaissance.

**Current API and unresolved noise-comparison gate.** The inspected prototype is
`environments/physim/physim/blobround6.py`, SHA-256 prefix `f3ed537fe6287c77`;
its full hash is in `evidence.json`. Its submitted signature is
`Predictor.predict(actions, queries, n_samples=64, seed=0)`; the last two arguments
control predictive sampling, not access to a world history or anchor. Under its
current policy A, a no-effective-action sham stays on the base RNG path, while a
treated continuation is reseeded per member (`:355–395`). Thus the native cached
common-noise pulse/control checks above **do not establish common-noise sham/
treatment semantics for the R6 runner**. Every proposed same-noise experiment in
this report requires a controlled pairing mechanism or a resolved root comparison
policy. That gate is unresolved here. No runner policy was changed or tested.

For the current A0 sensor construction only:

```text
port:   0   1   2   3   4   5   6   7   8   9   10  11  12
field:  u2  X1  u1  X9  X3  X6  X2  u0  X0  X5  X8  X7  X4
```

This mapping comes from `device.world_secrets('p6g8_033|s942|A0',...)`, sampled
with the native bilinear device function. The 13-node A and 19-node B arrays are
passive; displacement changes what is sampled, not the field. The currently
inspected R6 prototype **reuses this A0 layout** through `B.world_key` and
`B.ROSTER` (`blobround6.py:431–438`). This is source/version-specific evidence for
the same world and hidden seed, not a claim about other versions or scenarios.
Coordinates and geometry remain private and are not predictor inputs.

The existing round5 truth file was inspected **only for headers and manifest**.
Its L4/L4D arrays are 16×6×13×19 and 16×3×13×19 sensor outputs, not 2D fields.
Their ports, anchors, doses, and durations differ. No effect size or field
phenomenon in this report is inferred by subtracting them. The E2 audit's trace
observations are provisional due to state-concurrency defects and did not supply
our physics measurements. Agent MAE, noise-spread growth, or Gaussian leave-one-out
CRPS do not establish a paired effect, chaos, or an exact irreducible floor.

## 7. Reproducibility and evidence bounds

- `recon.py` made the initial three figures and selected-time statistics.
- `offline_checks.py` made the two follow-up figures, native paired checks,
  negative-core diagnostics, sampled gate check, and native home-sensor summaries.
- Both ran with `~/.venvs/bk3/bin/python` and all of
  `OMP_NUM_THREADS/OPENBLAS_NUM_THREADS/MKL_NUM_THREADS=1`.
- Stored NPZ members were mapped read-only in place. No archive was extracted;
  no full float32 cache copy was made. The largest mapped payload is 0.854GB.
  The scripts use per-frame or selected-frame working arrays, not trajectory copies.
- No new seed/world/truth member, simulator step, model, evaluation, remote job,
  monitor, archive unpack, secret-bearing launcher read, or commit was performed.
- Source and cache SHA-256 values are in `evidence.json`. Current source hashes
  are not a recovered immutable build manifest of the old simulation job.

The handoff is deliberately incomplete: it establishes concrete morphology,
one conditional perturbation response, meaningful quiet controls, and specific
next tests. It does not claim a completed theory of p6g8_033.
