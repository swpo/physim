# H9 prototype: read-only scientific review

## Disposition

**Retain v0 only as `h9_v0_fixed_grid_diag`: an exploratory fixed-grid
phenotype-label association diagnostic. It is NOT a ranker for the intended
compartment phenotype. Do not add it to C9 or set a biological cutoff.**

Do not run a full-harvest scan merely to hunt for h9 > .2. The streaming design
below is a conditional engineering proposal, not authorization for that scan.

No factor-of-two coordinate bug or valid-input range failure was found.
There are serious **semantic** failures: the claimed d7b species equivalence,
“motility ceiling,” and identification of regional multi-field compartments
are not supported. Batch input guards also need attention. Any later correction
must get a new version; do not silently replace historical h9 values.

Scope: source audit plus small synthetic arrays in the native `bk3` environment.
No simulations, GPU/SSH, archive extraction, production edits, or commits.
The five old examples were not rerun and do not establish archive-wide behavior.
Selected films are re-simulations, not the original measured trajectories.

## What was checked

Run from the repository root:

```sh
~/.venvs/bk3/bin/python -B probes/blobs/l0/complexity/h9_review/toy_checks.py
```

All assertions passed. `toy_results.json` contains numbers, source paths/hashes,
versions, constants, and invalid-input results. `toy_run.log` records the run.
Python 3.9.6 / NumPy 1.26.4 / SciPy 1.13.1 were used.
`h9_dev.py` hash starts `f791bd655791`; it imports the hard-coded
`~/v3work/v3bundle/lib/metrics_v3.py`, not a guaranteed repository-local module.
That file matched local `metrics_v3.py` at review time (hash `2273a13f7de7…`).
The bundle's v1/v2 shims resolved to the repository's blobkit package.

Actual constants: BURN=500 tu, REC=5 tu, CREC=25 tu; late window at least
1000 tu; minimum 8 records/track and 6 feature rows; k ceiling 24;
silhouette floor .25; **d7b cluster persistence minimum 500 tu**.
The fallback constants in h9 are not the values used in this environment.

## Units and species semantics

**Use L, not N, for recorded positions.** Blobkit
`soup/sim_v1.py:29–58` computes centers as circular angles times `N*dx`, and
areas as cell counts times `dx*dx`. `sim_cpu.py:126–163` records those centers
unchanged; the GPU recording paths reuse this contract. `metrics_v1.build_tracks`
unwraps them with physical L. `track_speeds`, v2 density maps, and
`metrics_v3.bond_frames` use those same length units. Comments saying “px” do
not turn stored centers into raw grid indices.

Toy: N=64, dx=.5, L=32, one active cell at grid index (8,48) produced center
(4.25,24.25), area .25, and the same track center. P=4 maps it to patch (0,3).
Dividing by N incorrectly maps it to (0,1). Bond frames also correctly link a
pair 0.5 physical units apart across the periodic seam. Memf indices
`position/L*nb` have the same correct dimensional form.

**h9 copies feature construction and k-means selection, not all d7b semantics.**
`h9_dev.py:24–84` returns raw labels immediately after its silhouette gate.
`metrics_v3.py:605–663` then does more: cluster time-coverage pruning, effective
species weighting, and a takeover discount. In d7b, persistence is the union
of covered record intervals times REC, not the sum over simultaneous tracks.
The h9 `k_species=max(label)+1` is a raw-label diagnostic, not d7b's retained
species count. The differing short/one-species fallbacks also matter.

Neither feature set directly identifies joint activator compartments.
Features include area, speed, bond statistics, act identity, and selected
memory fields. The memory sampler averages a **fixed wrapped-coordinate
median location from the track's first late observation through the end**,
including time after a short track dies. It is not a co-moving composition
sample; a linear median near the periodic seam can lie far from the track.
Spatially dependent features also mean label shuffling is not an independent
end-to-end null for the feature/clustering procedure.

## Toy evidence

Unless specified, these call the unmodified `h9_from_frames` with known labels,
P=4, B=60, seed=0. They isolate the estimator, not chemical dynamics. Most use
128 samples at REC=5 (640 tu of track-frame coverage). Persistence rows also
call actual tracking, `track_table`, and `d7b_species`, with a minimal v2 stub
that disables frozen-bond features. These are not evolved positive worlds.

| Control / counterexample | Result |
|---|---|
| Two stationary binary-label regions, 8 tracks each | h9=1; shuffle control=0 |
| Same rigid object translated along its separation axis for one wrap | h9=0; identities and separation never change |
| Same-speed rigid translation perpendicular to separation | h9=1 |
| Rigid rotation of separated groups for one cycle | h9=0 |
| Stationary separation in y, interleaved x ranks (not all-tied x) | **actual h9=1; positional control=0** |
| A={u1,u2}, B={u1,u3}, with equal counts within each region | h9=.3091, pers=1 |
| 16 identical {u1,u2} locales; each has a 2-unit internal offset across grid boundaries | **h9=1** |
| Identical locales above, globally shifted 2 units in x | **h9=0**; also 0 at P=2 |
| Identical locales with exactly coincident u1/u2 | h9=0 |
| Two 200-tu clusters | d7b retains 0 species; h9 reports 2 and scores 1 |
| Two 600-tu clusters | d7b retains 2; h9=1 |
| One 600-tu cluster plus a second region appearing only for the last 200 tu | d7b retains 1; **h9=1, pers=1** |

Thus repeated identical compositions are not *always* falsely rewarded, but
internal geometry plus grid boundaries can make them outscore the intended
A/B multi-field contrast. Track counts, not field mass or joint chemical
membership, determine the mixture. Empty space, compartment connectedness,
and boundaries are not tested.

### Exact constructions behind the main counterexamples

All coordinates below are `(y,x)` in L=128. Unless stated otherwise,
`k=0..127`, `t[k]=500+5*k`, P=4, B=60, seed=0. Labels are supplied to the
estimator; these point/track constructions are not physical simulations.

- Binary regions: label `s=0,1`, eight tracks `j=0..7` per label, fixed at
  `(16+.25*j, 16+64*s)`. Result: `(h9,UC,PERS)=(1,1,1)`, I=Hs=.6931,
  I0=.0384. Add `(0,k)` modulo L to every track: `(0,0,.5)`.
  Add `(k,0)` instead: `(1,1,1)`. Separation and labels stay unchanged.
- Rotation: for each `(s,j)`, use radius `40+.1*j` about `(64,64)` and angle
  `2*pi*(k+.5)/128+s*pi`, with `(y,x)=(64+r*sin(a),64+r*cos(a))`.
  Result: `(h9,UC,PERS)=(0,0,0)`.
- False ceiling: label `s` at `(16+64*s,10+j+.25*s)` for `j=0..7`.
  Actual h9=1, median-x relabel control=0.
- Distinct compositions: at each binary-region position above place one
  track of each label in `{0,1}` for A and `{0,2}` for B. There are 32 tracks.
  Result: I=.3466, Hs=1.0397, I0=.0364, h9=.3091, PERS=1.
- Identical locales: centers `(8+16*j,x0)`, `j=0..7`, `x0 in {32,96}`.
  Each has label 0 at `x0-1` and label 1 at `x0+1`, fixed for all k.
  Result: I=Hs=.6931, I0=.3292, h9=1. Translate **every** point by `(0,2)`:
  I=0, I0=.1383, h9=0. At P=2 without translation, I=0, h9=0.
- Persistence: four fixed blobs per act at the Cartesian product of
  `{10+96*s,22+96*s}` in y and x, area=4, peak=2, REC=5 starting at t=500.
  With 40 samples per act, d7b coverage is 200 tu each, n_species=0,
  but h9=1. With 120 samples for act 0 and only the last 40 for act 1,
  coverage is 600/200 tu, d7b n_species=1, but h9=UC=PERS=1.

`toy_checks.py` gives the complete executable constructors, including the
unequal-duration and degenerate cases; `toy_results.json` gives every output.

### Why the controls do not establish the claimed phenotype

- `controls()` only splits tracks at median **x**. It does not optimize label
  placement, preserve the real species count/entropy, or construct physical
  compartments. The y-separated counterexample disproves an upper bound.
  Wrapped medians add another origin dependence. Call this an axis-specific
  relabel diagnostic, not a “perfect” control or motility ceiling.
- Time pooling measures association with **fixed world patches**. Translation
  or rotation can erase it without erasing compartment identity. The two
  equal-speed translation results also disprove a general inference that
  motility or lack of confinement prevents regional composition.
- PERS compares only two aggregate mixes. Its split is the median of pooled
  **track-frame times**, not the clock midpoint. It tests neither continuous
  existence nor a minimum lifetime. A patch needs only five observations per
  half, potentially from several simultaneous tracks.
- Patches missing either half are **omitted**, and weights are renormalized
  over those remaining. The late-arriving-region toy consequently gets
  pers=1. Conversely, no eligible patch returns h9=0 with a reason code.
  Such a zero is not evidence of homogenization.
- One shuffled labeling and one stochastic replacement curve do not calibrate
  false positives. Replacement fractions .25/.5/.75 redraw random labels;
  they are not exact fractions of labels flipped. Monotonicity is not guaranteed.

## Null weighting and numerical behavior

For track i of length n_i, observed species weight is
`sum_i n_i * 1[label_i=s]`. The null preserves **numbers of tracks per label**,
not these frame-weighted species totals, unless durations are equal.
Track-label exchangeability is an explicit hypothesis about complete
trajectories, including duration; it must not be assumed for phenotypes with
label-dependent tracking/lifetimes. This is a weighting/interpretation issue,
not proof that every track-level permutation test is invalid.

Toy: label-0 tracks `i=0..11` sit at
`(16+32*(i//4),16+32*(i%4))`, with 80 times `500+5*k`.
Four label-1 tracks sit at `(112,112)`, with 20 times `650+5*k`.
Observed patch separation is perfect:
I=Hs=.2712. Across the 60 shuffles the second species has 140–320 frames instead
of 80, with mean shuffled Hs=.5612. **I0=.5318 > observed Hs, so UC=h9=0.**
The advertised “maximum” normalization is not a fixed-margin correction here.
Report this degeneracy and duration weights; do not interpret the zero as mixing.

For valid finite inputs and B>0, the algebra is bounded: `0 <= I <= Hs`.
If `I0 < Hs`, the corrected ratio cannot exceed 1; otherwise its clipped
numerator is zero. PERS is clamped to [0,1]. Unequal durations did not produce
an out-of-range value. One label and one occupied patch both returned 0;
relabeling species identities left the binary result unchanged. Too few frames
and no shared-half support returned the documented zero/reason gates.

Invalid inputs are not safely handled: empty tracks raise ValueError; an empty
record raises IndexError; B=0 yields NaN; L=0 emits warnings but returns 0.
Before any batch run, validate finite positive L, integer P>=1/B>=1, aligned
nonempty arrays, finite coordinates/times, ordered record times, label validity,
and recording cadence. Distinguish invalid/missing/unsupported from measured
zero. Preserve warning/error rows. The toy JSON encodes nonfinite results as
strings so the evidence file remains strict JSON.

## Supported versus unsupported historical claims

Supported: the frozen code can detect certain stationary label-patch
associations; its coordinate normalization matches the recording contract;
its d7b feature/k-means path is substantially copied. The old five-row table
is limited selected-example evidence, not an archive census or calibration.

**Unsupported:** “MEASURE VALIDATED”; “NOTHING evolved so far segregates”;
“sic fully homogenizes”; “genome-level merges are required”; and
“confinement/membranes are prerequisites.” The counterexamples refute the
claimed control guarantee and phenotype equivalence. They do **not** establish
that any harvested world actually has the desired phenotype. Low h9 cannot
distinguish homogenization, motion, sampling failure, track/silhouette gates,
null saturation, or coarse compositional resolution. A genome-merge requirement
is a causal/operator-expressivity hypothesis, not a consequence of these scores.
A single shared chemistry does **not** logically preclude several stable local
compositions: one reaction law can support multiple local states and spatial
patterns. This audit does not establish that any particular harvested genome
does so. Genome merging might help expressivity, but necessity and complete
homogenization remain unproven. Neither a .2 cutoff nor another biological
cutoff is justified.

## Bounded-memory archival plan — proposal only, owned by root

This is a feasibility design **only if a separate, predeclared diagnostic
question later warrants archival extraction**. It is not approval for a full
h9 ranking or a >.2 hunt. No extraction was run here. Any v0 output must be
named `h9_v0_fixed_grid_diag`, not "regional compartment diversity".

1. Freeze source/dependency hashes, import paths, constants, P/B/seeds and
   interpretation. Use original final-archive records, not fresh simulations.
   Keep original v3/C9 results unchanged. Join status, island, generation,
   candidate, seed and lineage using an on-disk manifest/SQLite table; do not
   assume metadata precedes records in tar order or basenames are unique.
2. Read each `~/v3work/islN_final2.tgz` **once** using
   `tarfile.open(..., mode="r|gz")`; disable/clear cached TarInfo lists if the
   native version retains them. Hash during streaming, not a second pass.
   Accept only expected regular members; do not extract arbitrary paths or
   links. Copy one selected `runs/*.npz` member in bounded chunks to one
   seekable temporary file, with compressed/uncompressed size caps and a
   content hash. NPZ needs seeking; `run` is a pickled object dictionary, so
   its fields cannot simply be lazy-streamed. Load trusted originals only.
3. Use one worker/record at a time, with a memory cap and explicit oversized,
   corrupt, missing, non-ok, and unsupported rows. Peak memory includes one
   decoded record, tracks, bond-pair workspace, and clustering workspace;
   it is **not constant in record size**. Delete each temporary file and end
   the worker before the next. Store metadata/results incrementally on disk.
   A cap breach must not silently truncate a trajectory or become h9=0.
4. Preserve original tracking order and all history required by the feature
   path. Do not trim to the late window before tracking, or replace the
   full-window d3 bond radius / d5 phase with late-only versions. Reuse saved
   inputs only after proving provenance/equivalence to the frozen call path.
5. For an exact later optimization, retain per-track counts `C[i,patch,half]`
   plus the pooled timestamp histogram needed for the exact median split.
   Each null table is a sum of these counts by permuted track label; there is
   no need for a full F/Fp copy for each shuffle. This preserves the current
   statistic, not a new metric. Check equality against the present toy suite
   and a small original-record sample before using it. Keep any compact
   per-record feature/position sidecars on disk, not in an archive-wide list.
6. Emit append-only rows with source/member hash, gates/errors, time window,
   raw labels versus d7b-retained species, cluster coverage, track-duration
   weights, eligible-patch coverage, I/Hs/I0/UC/PERS, and seeds. Reconcile all
   expected original records, duplicates and missing rows before any claim
   about the full archive. Predeclare case selection by scientific question,
   controls and lineage; do not turn diagnostic scores into biological ranks.

## Follow-up direction — no replacement implemented

Investigate **component/region composition**, rather than global track labels
versus fixed coordinates. First identify spatially coherent, possibly co-moving
regions from joint field support. Then describe their joint chemical composition
and compare **simultaneously coexisting, persistent regions**. Separate this
between-region comparison from internal morphology, motion, population size,
and confidence in region tracking. The target contrast is A={u1,u2} versus
B={u1,u3}; duplicating the same {u1,u2} locale must not create new composition
types. Region construction and chemical thresholds need independent validation;
this paragraph is a research direction, not a metric specification or C9 change.

### Minimum acceptance tests for any replacement

1. **Chemical contrast:** known persistent A/B compositions must differ from
   one composition repeated many times, even when internal geometry differs.
   The common u1 field must not obscure the differing u2/u3 membership.
2. **Coordinate/motion invariance:** global periodic shifts, axis exchange,
   consistent field renaming, and quarter-turn rotations must preserve the
   conclusion. Rigid translation/rotation and co-motion of unchanged regions
   must not destroy their compositional diversity. Set discretization tolerances
   from controls, not from desired archive ranks.
3. **Replication/tracking invariance:** more identical locales, artificial
   splitting of a track ID, and equivalent time resampling must not manufacture
   diversity. Uncertainty may change; the underlying composition must not.
4. **Actual persistence:** disappearance, late birth, swaps of composition,
   mergers and splits need explicit outcomes. Omitting unsupported regions
   must not report perfect persistence. Report insufficient observations as
   such, not as homogenization or zero diversity.
5. **Measurement/null checks:** test grid phase/resolution, support thresholds,
   shared backgrounds, unequal region lifetimes and sampling density. Define
   the time/region weighting before selecting a null; check its conserved
   quantities and replicate variability. Include empty/single-region cases,
   finite range checks, and known negative controls. No biological cutoff yet.

### Required records and fields

- Original, time-aligned **spatial fields for all relevant activators** across
  a sufficiently sampled late interval, not only centroids or final images.
  If memory/channel composition is part of the phenotype, include those fields
  too; selected coarse `memf` channels alone are not a complete field record.
- L, N/dx, boundary conditions, exact timestamps, field order/channel identities,
  baseline/support conventions (`thr`, `thr_lo` or a separately validated
  replacement), and the matching genome. Preserve source, candidate, seed,
  island/generation, status and saved-time provenance.
- Per-time region masks and region/lineage correspondences, derived from those
  fields with documented handling of overlap, merges and splits. Record
  chemical summaries inside each region and the time it was observable.

Existing blob lists and memf can support limited diagnostics, but cannot by
themselves recover arbitrary multi-activator co-presence. Inventory actual
original snapshot keys, channel coverage and times before promising this
analysis. `assay_v3` uses a separate full-field `fsnaps` buffer for scoring;
`save_run(rec)` does not itself guarantee that buffer was archived. If dense
original fields are missing, mark the phenotype unobserved at that resolution.
A new positive-control run or film is new evidence, **not** a recovered original
trajectory. Only after these controls succeed should a separately versioned
metric or a calibrated biological threshold be considered.
