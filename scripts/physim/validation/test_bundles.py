"""Bundle trust boundary and offline release workflow checks; no network/model calls."""

import hashlib
import io
import json
import os
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

import numpy as np
from physim import hub
from physim.bundles import (
    Bundle,
    BundleError,
    load_arrays,
    read_json,
    relative_path,
    safe_path,
    validate_manifest,
)


class DataBoundaryTests(unittest.TestCase):
    def test_paths_reject_traversal_absolute_and_noncanonical(self):
        for value in ("../data", "/tmp/data", "a/../b", "a//b", "./a", "a\\b", "C:data", "", "a/./b"):
            with self.subTest(value=value), self.assertRaises(BundleError):
                relative_path(value)

    def test_symlink_is_not_a_regular_bundle_input(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "file").write_text("{}")
            (root / "link").symlink_to(root / "file")
            with self.assertRaises(BundleError):
                safe_path(root, "link")
            with self.assertRaises(BundleError):
                read_json(root / "link")

    def test_json_rejects_duplicate_nonfinite_and_oversize(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / "data.json"
            for value in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}'):
                p.write_text(value)
                with self.assertRaises(BundleError):
                    read_json(p)
            p.write_text(" " * 100)
            with self.assertRaises(BundleError):
                read_json(p, maximum=99)

    def test_npz_rejects_objects_nonfinite_and_header_allocation(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / "data.npz"
            for value in (np.array([{}], dtype=object), np.array([np.nan]), np.array(["arbitrary"])):
                np.savez(p, fields=value)
                with self.assertRaises(BundleError):
                    load_arrays(p)
            stream = io.BytesIO()
            np.lib.format.write_array_header_1_0(stream, dict(descr="<f8", fortran_order=False, shape=(10**12,)))
            with zipfile.ZipFile(p, "w") as z:
                z.writestr("fields.npy", stream.getvalue())
            with self.assertRaises(BundleError):
                load_arrays(p)

    def test_npz_rejects_archive_paths_and_duplicate_arrays(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / "data.npz"
            with zipfile.ZipFile(p, "w") as z:
                z.writestr("../fields.npy", b"bad")
            with self.assertRaises(BundleError):
                load_arrays(p)

    def test_public_inputs_are_frozen_before_grading(self):
        from physim.artifact_store import read_artifact_files
        from physim.evaluation import _snapshot_inputs

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            source.mkdir()
            (source / "predictor.py").write_text("original")
            rows = _snapshot_inputs(source, root / "frozen")
            (source / "predictor.py").write_text("changed after freeze")
            frozen = dict(read_artifact_files(root / "frozen", rows))
            self.assertEqual(frozen["predictor.py"], b"original")
            self.assertEqual(rows[0]["sha256"], hashlib.sha256(b"original").hexdigest())
            (source / "link").symlink_to(source / "predictor.py")
            with self.assertRaises(RuntimeError):
                _snapshot_inputs(source, root / "rejected")

    def test_mutable_revision_fails_without_network(self):
        for revision in ("main", "v1", "abc1234", "A" * 40):
            with self.assertRaises(BundleError):
                hub.fetch_bundle(repo="owner/worlds", revision=revision, path="bundles/world/v1", offline=True)

    def test_offline_miss_never_downloads(self):
        with (
            tempfile.TemporaryDirectory() as cache,
            patch.object(hub, "_download", side_effect=AssertionError("network")),
        ):
            with self.assertRaisesRegex(BundleError, "offline cache"):
                hub.fetch_bundle(
                    repo="owner/worlds", revision="a" * 40, path="bundles/world/v1", cache=cache, offline=True
                )


@unittest.skipUnless(os.environ.get("PHYSIM_TEST_BUNDLE"), "set PHYSIM_TEST_BUNDLE for release integration checks")
class ReferenceBundleTests(unittest.TestCase):
    def setUp(self):
        self.fixture = Path(os.environ["PHYSIM_TEST_BUNDLE"]).resolve()
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "bundle"
        shutil.copytree(self.fixture, self.root)

    def test_all_truth_requests_and_sample_arrays_are_bound(self):
        b = Bundle(self.root)
        self.assertEqual(len(b.suite["cases"]), 15)
        for row in b.suite["cases"]:
            self.assertTrue(b.truth(row)["samples"])

    def test_manifest_identities_cannot_be_forged_independently(self):
        original = read_json(self.root / "manifest.json")
        for kind in ("world", "preparation", "suite"):
            m = json.loads(json.dumps(original))
            m["objects"][kind]["changed"] = True
            with self.assertRaises(BundleError):
                validate_manifest(m)
        m = json.loads(json.dumps(original))
        m["bundle_id"] = "changed"
        with self.assertRaises(BundleError):
            validate_manifest(m)
        m = json.loads(json.dumps(original))
        m["files"][-1]["sha256"] = "a" * 64
        with self.assertRaises(BundleError):
            validate_manifest(m)

    def test_corrupt_truth_is_rejected_before_scoring(self):
        p = next((self.root / "truth").glob("*.npz"))
        value = bytearray(p.read_bytes())
        value[-1] ^= 1
        p.write_bytes(value)
        with self.assertRaisesRegex(BundleError, "hash mismatch"):
            Bundle(self.root)

    def test_simulation_profile_has_no_truth_dependency(self):
        shutil.rmtree(self.root / "truth")
        (self.root / "suite.json").unlink()
        b = Bundle(self.root, profile="simulation")
        self.assertIsNone(b.suite)
        self.assertEqual(b.make_oracle()._template["F"].shape, (12, 256, 256))
        with self.assertRaises(BundleError):
            Bundle(self.root)

    def test_fetch_only_requested_profile_and_verify_offline(self):
        calls = []

        def download(repo, revision, name, destination, maximum, expected_bytes=None):
            self.assertEqual(revision, "a" * 40)
            calls.append(name)
            source = self.root / name.removeprefix("bundles/world/v1/")
            self.assertLessEqual(source.stat().st_size, maximum)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)

        kwargs = dict(
            repo="owner/worlds",
            revision="a" * 40,
            path="bundles/world/v1",
            profile="simulation",
            cache=Path(self.temp.name) / "cache",
        )
        with patch.object(hub, "_download", download):
            target = hub.fetch_bundle(**kwargs)
        self.assertFalse(any("/truth/" in name for name in calls))
        with patch.object(hub, "_download", side_effect=AssertionError("network")):
            self.assertEqual(hub.fetch_bundle(**kwargs, offline=True), target)
            (target / "world.json").write_text("{}")
            with self.assertRaises(BundleError):
                hub.fetch_bundle(**kwargs, offline=True)

    def test_failed_fetch_never_promotes_partial_cache(self):
        def download(repo, revision, name, destination, maximum, expected_bytes=None):
            destination.parent.mkdir(parents=True, exist_ok=True)
            if name.endswith("manifest.json"):
                shutil.copyfile(self.root / "manifest.json", destination)
            else:
                destination.write_bytes(b"corrupt")

        cache = Path(self.temp.name) / "cache"
        with patch.object(hub, "_download", download), self.assertRaises(BundleError):
            hub.fetch_bundle(repo="owner/worlds", revision="a" * 40, path="bundles/world/v1", cache=cache)
        self.assertFalse(list(cache.rglob("world.json")))

    def test_truth_arrays_open_only_after_all_forecasts_are_frozen(self):
        from physim import evaluation as E

        b = Bundle(self.root)
        seen = []
        original = b.truth
        output = Path(self.temp.name) / "run"

        def truth(row):
            manifest = read_json(output / "grading_predictions/manifest.json")
            self.assertEqual(len(manifest["completed"]), 15)
            self.assertFalse(manifest["grader_truth_loaded"])
            seen.append(row["request"]["id"])
            return original(row)

        with patch.object(b, "truth", truth):
            result = E.reference_demo(b, output)
        self.assertTrue(result["ok"])
        self.assertEqual(len(seen), 15)


if __name__ == "__main__":
    unittest.main()
