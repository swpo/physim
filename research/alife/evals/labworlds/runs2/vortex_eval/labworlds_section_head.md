## Lab bundles and the fed-vortex evaluation candidate (31 Oct)

**`physim/labbundle.py`.** A lab bundle has the Blobkit bundle's shape (manifest with world, preparation
and suite identities, simulation/evaluation profiles, `suite.json`, `truth/*.npz`, `checks.json`) with the
world as files: `world/` (the world file verbatim, the labkit modules it imports, `observables.py` for the
observe-only channels), `labworld.json` (the declaration), `apparatus.json` (devices, observed-port
permutation, adjustment matrix, protocol) and `preparation.npz` (fields and `carry` keys only; the rest of
the module state is rebuilt by the world's `init`, nothing is unpickled). Schema `physim-lab-bundle-v1`; the
world identity binds every world file, the declaration and the implementation (source hashes of
`blobround6`, `labworld`, `devices`, `blobround6_eval`, `labbundle`; numpy and scipy versions).
`LabBundle(Bundle)` provides what `taskset` and `evaluation` use (`manifest`, `roster`, `limits`, `suite`,
`apparatus`, `protocol`, `verified_path`, `truth`, `references`, `check_runtime`, `make_oracle`);
`open_bundle` picks it when the manifest declares a lab world, and `taskset.required_bundle` now calls
`open_bundle`. Because `blobround6_eval.PublicRoster` has one port count, a lab bundle must declare as many
observed ports as actuators (refused otherwise); the fed vortices meet this with two observe-only channels.
Still Blobkit-only: `hub.fetch_bundle` and `cli.py` construct `Bundle` directly. A lab bundle runs its world
file in the grader's host process (trusted-code policy still open), and any edit of the hashed sources
invalidates it until its manifest is rewritten.
