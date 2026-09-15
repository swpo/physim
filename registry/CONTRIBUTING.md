# Contributing worlds

Contribute to the [Physim world registry on Hugging Face](https://huggingface.co/datasets/seanpohorence/physim-worlds)
through a pull request. You need an HF account, but do not need write access to
the dataset's main branch. A maintainer reviews and merges submissions.

If you would like help packaging a world, start a discussion in the dataset's
[Community tab](https://huggingface.co/datasets/seanpohorence/physim-worlds/discussions)
with its definition, source, and available evidence. You can also use the steps
below to submit the registry files directly.

## What to contribute

A **preserved world** needs:

- A valid Blobkit genome defining its dynamics, and a descriptive name.
- Attribution and origin: who made it, where it came from, and source links or
  commits where available. State gaps in historical provenance explicitly.
- License information. This dataset publishes world data under CC-BY-4.0 and
  archived code under Apache-2.0. Include only material you can contribute under
  those terms, and retain third-party attribution and applicable license notices.
- A short description of what is known about the world. Include the simulator
  version, numerical settings, seeds, recipe, and observations where available;
  distinguish measured behavior from hypotheses.

Any world can be preserved, including simple controls and historical examples.
An evaluation suite, apparatus, exact saved starting state, or claim of interesting
physics is not required. Missing historical information should remain identified
as missing; do not reconstruct it by guessing.

An **eval-ready preparation** additionally needs an exact starting state and
numerical profile, measurement/control apparatus, a frozen evaluation suite,
reference trajectories, scoring configuration, and validation evidence. The
apparatus belongs to the preparation; it is not part of the world's intrinsic
dynamics. One world can have several preparations and suites.

## Package a preserved world

Use a fresh working directory containing your `genome.json`, `source.json`, and
`README.md`. The genome file should contain the genome itself, not the enclosing
registry record. For an existing registry entry, `Registry.load_genome(record_id)`
returns that definition.

Install the published Blobkit release and HF client in an isolated environment:

```sh
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python \
  'blobkit @ https://github.com/swpo/physim/releases/download/blobkit-v0.3.5/blobkit-0.3.5-py3-none-any.whl#sha256=6747e7ebe26e3909c05d91d050ebce93715d08992c51498cbf480b8206224331' \
  'huggingface_hub>=1,<2'
```

For `source.json`, adapt this example to your actual provenance. The keys are
descriptive metadata rather than a rigid schema. In `README.md`, describe the
behavior, any reproduction commands, numerical settings, and limitations.

```json
{
  "authors": ["Your name or HF handle"],
  "origin": "New world created for this submission",
  "data_license": "CC-BY-4.0",
  "code_license": "Apache-2.0",
  "simulator": "blobkit 0.3.5",
  "source_url": null,
  "missing_provenance": []
}
```

Save the following as `make_submission.py`. Change the name and extend the
explicit artifact list with any recipe inputs, reports, license notices, or
other files needed to reproduce your world.

```python
import json
from pathlib import Path

from blobkit.registry import Registry

registry = Registry("submission/registry")
artifacts = {"README.md": Path("README.md").read_bytes()}
for name in ("recipe.py", "requirements.txt", "initial_state.npz",
             "observations.npz", "report.md"):
    path = Path(name)
    if path.is_file():
        artifacts[name] = path.read_bytes()

world_id = registry.add_source_world(
    "my_world",
    json.loads(Path("genome.json").read_text()),
    source=json.loads(Path("source.json").read_text()),
    artifacts=artifacts,
)
print(world_id)
print(registry.verify())
```

```sh
.venv/bin/python make_submission.py
.venv/bin/blobkit registry verify submission/registry
```

Blobkit validates the genome and writes immutable records and exact artifact
bytes with content-based identifiers. Verification checks hashes and references;
it does not run a simulation or certify the scientific claims. Keep the printed
world ID for the PR description. Changing the inputs creates new records; use a
fresh submission directory when replacing an earlier draft to avoid proposing
unintended intermediate worlds.

If you used `blobkit generate`, retain its recipe, run, candidate, checkpoint,
and harvested-world records together with every referenced object. That preserves
the structured search history. The minimal example above archives supplied source
files, but does not invent a generation run or turn `recipe.py` into a structured
recipe record. `Registry.export_recipe` applies to those structured recipe records.

## Open the HF pull request

Log in with your own account using `.venv/bin/hf auth login`. Then save this as
`submit.py` and run `.venv/bin/python submit.py`:

```python
from huggingface_hub import HfApi

commit = HfApi().upload_folder(
    repo_id="seanpohorence/physim-worlds",
    repo_type="dataset",
    folder_path="submission/registry",
    path_in_repo="registry",
    create_pr=True,
    commit_message="Propose world: my_world",
    commit_description="World ID: paste the ID printed above.\n"
                       "Requested status: preserved.\n"
                       "Describe the origin, evidence, and known limitations.",
)
print(commit.pr_url)
```

Open the returned PR link, fill in the description, and mark it ready for review
when complete. Upload only the isolated registry directory. Do not hand-edit
hashes, overwrite existing records, or change the generated catalogs,
`registry/index.json`, `registry/availability.json`, or `release.json`.

To update an existing PR, replace `create_pr=True` with `revision="refs/pr/N"`,
using its actual PR number. Repeating `create_pr=True` opens another PR; after an
interrupted upload, check the Community tab before retrying. A corrected immutable
record gets a new ID; identify superseded records in the PR so they can be removed
from the proposed changes before merge.

These steps use HF's supported [upload API](https://huggingface.co/docs/huggingface_hub/guides/upload)
and [community PR workflow](https://huggingface.co/docs/hub/repositories-pull-requests-discussions).

## Preparing a world for evaluation

You can request eval-ready review in the same PR or build on a preserved world
later. Include the preparation and suite inputs, executable recipes and their
dependencies, saved arrays, and a report covering:

- Fresh simulations using the stated simulator and numerical settings, with
  observations supporting the behavior the suite is intended to measure.
- The exact prepared state and apparatus, action/query programs, score groups,
  scales, and reference-generation seeds. Freeze the suite before model testing.
- Native reference checks and mechanism/scoring controls, including known
  numerical or measurement limitations and reproduction commands.
- Any model pilots used as evidence, with model, harness, budget, stopping
  conditions, submissions, and failed attempts recorded. A high model score is
  not a condition for preserving a world.

Archive these files as named artifacts alongside the world record, or provide a
complete registry export with their references. Maintainers help assemble and
validate the runnable bundle before adding eval-ready availability. Existing
preparations and evidence can be explored through the dataset's `evaluations`
catalog and `registry/availability.json`. A new preparation or suite receives
new content identities; old results keep their original references.

## Maintainer review and publication

The current intake process uses manual review and existing validation tools;
opening a PR does not trigger an automatic scientific certification.

1. Check attribution, licenses, provenance gaps, and whether the submission is a
   new world, a new preparation, or a correction. Inspect archived code before
   explicitly running it; registry reads and verification do not execute it.
2. Verify the combined registry, including all referenced objects. Reproduce the
   submitted claims as appropriate; require the preparation, suite, and native
   validation checks before promoting a record to eval-ready.
3. Rebuild the registry index and both JSONL catalogs. Only validated preparations
   go in availability and the evaluation catalog. Stage bundles, documentation,
   and the release manifest together and verify their identities and file hashes.
4. Include those derived updates in the reviewed publication, merge, and record
   the resulting HF commit. The viewer may take time to refresh. Update evaluation
   configs separately when the new preparation should be used in a run.

Submission itself does not change default evaluation selection. Runtime configs
continue to pin explicit dataset revisions and preparations.
