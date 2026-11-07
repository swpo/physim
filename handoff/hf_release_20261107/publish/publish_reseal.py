"""Publish the staged fair-scorer reseal of seanpohorence/physim-worlds in one commit.

Modeled on handoff/hf_release_20260914/publish.py and
handoff/registry_contribution_20260915/publish_hf_guide.py. Without --publish this is
a read-only dry run: it re-verifies the staged inventory and compares it with the
remote parent anonymously. With --publish it requires the seanpohorence login,
commits against the exact parent revision, and writes publication.json.

Run from the release worktree:
    cd /Users/spoho/physim-release/physim
    uv run --locked python /Users/spoho/physim-release/publish/publish_reseal.py            # dry run
    uv run --locked python /Users/spoho/physim-release/publish/publish_reseal.py --publish  # upload
"""

import argparse
import hashlib
import json
from pathlib import Path

from huggingface_hub import CommitOperationAdd, CommitOperationDelete, HfApi
from physim.bundles import digest, identified

HERE = Path(__file__).resolve().parent
ROOT = Path("/Users/spoho/physim-release/physim")
STAGE = Path("/Users/spoho/physim-release/dist/hf-worlds-next")
REPO = "seanpohorence/physim-worlds"
PARENT = "bd77a0da2f14eef352bd80c4a38dff426e5c1bed"
OWNER = "seanpohorence"

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--publish", action="store_true", help="upload; otherwise only verify and print the plan")
args = parser.parse_args()

changes = json.loads((HERE / "hf_changes.json").read_text())
release = json.loads((STAGE / "release.json").read_text())
assert release["dataset_repo"] == REPO and changes["parent"] == PARENT
assert release["id"] == changes["release_id"]
assert identified("dataset-release", {k: v for k, v in release.items() if k != "id"}) == release
expected = {row["path"] for row in release["files"]} | {"release.json"}
actual = {p.relative_to(STAGE).as_posix() for p in STAGE.rglob("*") if p.is_file()}
assert actual == expected, sorted(actual ^ expected)
for row in release["files"]:
    path = STAGE / row["path"]
    assert path.stat().st_size == row["bytes"] and digest(path) == row["sha256"], row["path"]
for name, checksum in release["code"]["exporter_sha256"].items():
    assert digest(ROOT / name) == checksum, name
assert release["code"]["code_packages"]["source_commit"] == "c36626cabbb2c35273d6ed2fd97d3a67db4682da"
assert not release["code"]["working_tree_dirty"]

api = HfApi() if args.publish else HfApi(token=False)
info = api.repo_info(REPO, repo_type="dataset", files_metadata=True)
assert info.sha == PARENT, f"Remote head moved: {info.sha}"
assert not info.private
remote = {s.rfilename: s for s in info.siblings}


def same(name):
    data = (STAGE / name).read_bytes()
    entry = remote[name]
    if entry.lfs:
        return hashlib.sha256(data).hexdigest() == entry.lfs.sha256
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest() == entry.blob_id


added = sorted(expected - remote.keys())
removed = sorted(remote.keys() - expected)
changed = sorted(name for name in expected & remote.keys() if not same(name))
unchanged = len(expected & remote.keys()) - len(changed)
assert added == changes["added"], "added files differ from hf_changes.json"
assert removed == changes["removed"], "removed files differ from hf_changes.json"
assert changed == changes["changed"], "changed files differ from hf_changes.json"
# Only superseded bundle folders and the superseded seals' registry records may go.
assert all(
    name.startswith(("bundles/", "registry/artifact/", "registry/recipe/", "registry/generation-run/",
                     "registry/world-record/"))
    for name in removed
)
plan = dict(repo=REPO, parent=PARENT, added=len(added), changed=changed, removed=len(removed), unchanged=unchanged,
            release_id=release["id"], evaluation_bundles=[e["bundle_path"] for e in release["evaluations"]])
print(json.dumps(plan, indent=2), flush=True)
if not args.publish:
    print("Dry run only; nothing uploaded.")
    raise SystemExit(0)

assert api.whoami()["name"] == OWNER
operations = [CommitOperationAdd(path_in_repo=name, path_or_fileobj=STAGE / name) for name in added + changed]
operations += [CommitOperationDelete(path_in_repo=name) for name in removed]
commit = api.create_commit(
    REPO,
    repo_type="dataset",
    parent_commit=PARENT,
    operations=operations,
    commit_message="Reseal the three centered preparations for the fair ensemble scorer",
    commit_description=(
        "Physim's scorer now uses the fair (unbiased) ensemble estimator for energy score and CRPS "
        "(residency c36626cabbb2c35273d6ed2fd97d3a67db4682da; scorer sha256 9deb1738). "
        "bf_trail_lab_centered_v2, xv_rotor_lab_centered_v2 and p4g2_044_centered_v2 are resealed with "
        "byte-identical worlds, preparations, apparatus, suites and truths; suite and bundle identities "
        "and checks.json control scores change. The superseded seals remain at " + PARENT + "."
    ),
)
result = dict(
    repo=REPO, revision=commit.oid, commit_url=commit.commit_url, parent_revision=PARENT,
    release_id=release["id"], release_sha256=digest(STAGE / "release.json"),
    files=len(expected), added=len(added), changed=changed, removed=len(removed),
    registry=release["registry_verification"],
    evaluation_bundles=[entry["bundle_path"] for entry in release["evaluations"]],
)
(HERE / "publication.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2), flush=True)
