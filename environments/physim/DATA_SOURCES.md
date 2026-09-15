# Code and data

Physim and blobkit code are Apache-2.0. The released reference data are CC-BY-4.0:
the genome, exact prepared fields, apparatus, case programs, score groups, and
retained native realizations. License choices are recorded in
`configs/physim/release.toml` and in each data-bundle manifest.

The [published dataset](https://huggingface.co/datasets/seanpohorence/physim-worlds/tree/dcd6abd5eae76a47f326c70518315d2d1e101d86) is `seanpohorence/physim-worlds`, verified at
`dcd6abd5eae76a47f326c70518315d2d1e101d86`. It includes 24 registry records
(19 distinct genomes), all available provenance, and three evaluation bundles.
Anonymous downloads, all file hashes, offline reuse, reference scores, and short
native simulations were verified. Fetch the selected bundle at this revision and
supply its local directory through `env.taskset.task.tools.bundle`; publication
does not introduce an implicit world selection.

These are disclosed reference/development preparations: the original p4g2_044
example, BF's trail laboratory, and XV's rotating-pair laboratory.
The host owns its fields, apparatus mapping, selected programs, and grader truths.
Those inputs are not included in the solver image or exposed through its harness.
Future held-out suites must use distinct preparations and explicit access controls.

Original source hashes, the initial-field hash, and all retained-truth hashes are
recorded in the bundle. The numerical source files remain byte-identical to the
validated reference. The original migration exporter retains its existing truth;
new preparation recipes freeze their suites before generating fresh truth. Third-party
Python dependencies retain their own licenses.
