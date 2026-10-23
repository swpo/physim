# P7: preparing a controlled recovery test

23 October 2026. This is a static intervention check using the P7 state saved on
11 October. P7 is the patterned island whose internal feature remained recognizable
through the [earlier saved trajectory](../evaluation/2026-10-23-p7-persistence.md).
No simulation time advanced in this study.

We have validated a way to disturb P7’s internal pattern and inspect the immediate result. Resetting the two activator fields inside a fixed interior region removes its curled stripe and adjacent band. Pulses in the surrounding band or a translated exterior region leave that interior feature visible at the same instant. The six other model fields remain unchanged in every case. This completes the preparation check for a recovery experiment; no time evolution was run, so we have not yet tested whether the feature returns or whether the surrounding region helps restore it.

The standing evaluator passed the fixed-view check. The comparison below shows
two activator fields—model quantities that help drive the pattern—in a fixed
interior region. Cyan shows A0; pale yellow shows A1. Gray is outside the region
being inspected. Each image keeps the same display mapping and saved pixels.

![Six immediate intervention cases: the interior feature is retained in S, B and C, and removed in D, DB and DC.](../../docs/assets/research/2026-10-23-p7-static-construction/interior-contact.png)

| Case | What changed immediately |
| --- | --- |
| S | Nothing; the unmodified comparison. |
| B | The two activators in the selected boundary-region band. |
| C | The same band shape at a fixed exterior location. |
| D | The two activators in the fixed interior region. |
| DB | The interior and boundary-region band together. |
| DC | The interior and exterior control together. |

The B and C regions have the same shape and area, but different initial field
values and intervention magnitudes. They are not equivalent-damage controls.
The six other fields remain intact, so retained model state could help a pattern
return in a later experiment.

The next consequential step is to implement and register the same fixed six-case
recovery comparison over 250 simulation-time units. It asks whether the named
surrounding-region intervention changes sustained recovery of the internal
feature. A positive result would remain compatible with restoration of a stable
pattern; it would not establish autonomy or a unique effect of boundary geometry.
Leaving the fixed view or becoming visually ambiguous would make the recovery
judgment inconclusive. No recovery execution is admitted by this static result.

[Read the standing evaluator’s assessment](../evaluation/2026-10-23-p7-static-construction.md)
· [View the earlier persistence evidence and movie](../evaluation/2026-10-23-p7-persistence.md)
· [Return to the research guide](../README.md)
