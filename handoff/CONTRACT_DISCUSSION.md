# Earlier contract discussion — corrected record

This conversation first examined absolute per-contract scoring and worked through
**R5 L1 only**. It then moved to world-specific physics and the R6 predictor
proposal. L2 through L4D were not explained one by one; do not assume that old
walkthrough is complete or that continuing it is the current approved task.

## Shared observable definitions

A port is one signed scalar simulation field under an opaque permutation, not
necessarily a positive chemical density. A device samples all ports at its slots
by periodic bilinear interpolation. The current device0 has13 slots; device1 has19.
Pose, orientation, field meaning and slot-to-node correspondence are hidden from
the investigator. Global mean and variance are spatial reductions of each field.
Geometry/rules in the developer's dossiers are not agent-visible inputs.

## L1: apparatus response

R5 draws an anchor in600…2300tu and1–3 commands in[-1,1]^3. Starting device0 at
its initial pose, each command shifts/dilates the array and takes5tu. The target
is its full reading after the final command: shape `(n_ports,13)`. The world
continues evolving but moving this passive sensor does not perturb it.

The private fixed actuator map is dx=1.5*u1, dy=1.5*u2, and spacing multiplied by
exp(u3), subject to dilation bounds. R5 truth applies sequential clipping, not
merely one clipping of the summed log gains. The truth builder uses the base
realization at `anchor+5*n_commands`, sampled at the final pose. L1 therefore has
one deterministic truth member under that specified base realization.

The submitted mean/sigma define a Gaussian per port/slot. The scorer averages
Gaussian CRPS across entries. Sigma=0 reduces to absolute error. A sigma in the
payload can reflect the investigator's uncertainty; it is not a measurement of
physical noise amplitude. The score does not separately test a recovered actuator
map, spatial layout, or a general dynamics law.

### The actual two completed draws

| Item | E1 #928 | E2 #942 |
|---|---:|---:|
| Anchor |1758.1|747.6|
| Commands |2|1|
| Reading time |1768.1|752.6|
| Net shift dx,dy (field units) |-0.4644,+0.2457|+0.55245,-0.11025|
| Initial spacing -> final, approximate |3.5 ->2.88|3.5 ->3.15|
| Raw L1 CRPS |0.072269|0.024033|

For provenance, E1's commands were `[0.197,0.4786,0.5426]` and
`[-0.5066,-0.3148,-0.7374]`; E2's was `[0.3683,-0.0735,-0.1045]`.
These exact draws are in the audited nested traces listed in LOCAL_ASSETS.json.
The raw scores are preserved in the absolute-scoring archive. Neither draw hits
a dilation bound. These illustrative cases differ in world, scene and command;
they are not matched measures of model quality.

### What the L1 reference actually does

Both rungs use device0's **home-pose pre-anchor history**, ignoring the requested
pose change. Climatology uses per-element historical mean and SD; persistence
uses the last pre-anchor home reading for its mean, with historical SD rather
than zero sigma. See `blobround5.ladders5` for the exact history slicing.

Those are meaningful comparators for some small moves but not proof that a test
measures important physics. Beating them on one draw does not alone establish
actuator discovery. Conversely, quiet local observations do not prove the whole
field is inactive. The actual experiment/process and spatial evidence matter.

The earlier proposed full-base-SD and LOO-floor normalizations were exploratory,
not accepted 0–1 scores. See the archive's corrections, including the erroneous
0.77 climatology claim and the misuse of prediction MAE as treatment effect.

## Why the project changed direction

The user pointed out that a generic point forecast can test an uninteresting
background because the interesting structure never visits it. A scientific task
should lead the investigator to find the structure and understand its behavior.
Our privileged view can identify and validate phenomena, then privately test
whether submitted prediction code covers them without requiring shared theory
terminology. That is the R6 direction, not a decision to merely strengthen the
six old contracts with generic baseline gates.

Sources: current `environments/physim/physim/blobcore.py`, `blobround5.py`,
`probes/blobs/agentenv/device.py`, both R5 process audits, the original raw-score
artifact, and the local exact trace IDs in LOCAL_ASSETS.json. This note is a
corrected summary of prior work; no score, simulation or model was rerun for it.
