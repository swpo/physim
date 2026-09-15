# Archived Physim implementation

These earlier engines and taskset sources were moved out of the active environment
when aligning with the residency repository. Their bytes were preserved and are
mapped in `handoff/residency_alignment/source_before.json`. This directory is not
an active workspace package and is not part of the environment distribution.

Migration/native-comparison tools explicitly add this source directory to the
current package search path through `generators/physim/_research.py`. New runtime
code must never enable that compatibility path. Original scientific records and
the source snapshots attached to old runs are unchanged.
