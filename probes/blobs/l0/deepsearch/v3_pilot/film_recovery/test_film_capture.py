"""Local-only tests: metadata, native recorder/driver, and a FAKE stepping seam.

No JAX import, GPU allocation, assay, dynamics integration, or scoring runs.
The fake GPU-like container checks our I/O/control logic, NOT GPU correctness.
A real --smoke remains required on the parent's free GPU.
"""
import contextlib
import copy
import io
import json
import os
import sys
import struct
from pathlib import Path
import tempfile
import time
from types import SimpleNamespace
import unittest
from unittest import mock

import numpy as np

import film_capture as FC
from blobkit.soup import sim_cpu as SC
from blobkit.soup import sim_gpu as SG_NATIVE
from blobkit.soup import driver as DRIVER
from blobkit.soup import asyncapply_proto as AA


G = {"id": "base", "acts": [{"lam": 2.0, "k1": 0.0, "Du": 0.5, "u0": -1.4142135623730951}],
     "chans": [{"tau": 2.0, "D": 1.0, "g": "id"}], "W": [[1.0]], "K": [[0.5]], "bilin": []}


class FakeArray:
    def __init__(self, a):
        self.a = np.asarray(a)

    @property
    def dtype(self):
        return self.a.dtype

    def __array__(self, dtype=None, copy=None):
        return np.asarray(self.a, dtype=dtype).copy() if copy else np.asarray(self.a, dtype=dtype)

    def __getitem__(self, index):
        return FakeArray(self.a[index])

    def devices(self):
        return [SimpleNamespace(platform="gpu")]


class FakeNative:
    """Real native recorder and driver; deterministic synthetic field changes."""
    def __init__(self, fault=None):
        self.fault = fault
        self.targets = []

    def init_soup_gpu_batch(self, jobs, *, L, dtype, noise, ics):
        g, seed = jobs[0]
        S = SC.init_soup(g, L=L, seed=seed, dtype=dtype, n_soup=1, noise=noise, workers=1)
        if ics[0] is not None:
            S["F"] = np.asarray(ics[0], dtype=S["F"].dtype).copy()
        master = {"worlds": [S], "_gpu": {"F": FakeArray(S["F"][None].copy())}}
        return master

    def advance_gpu_batch(self, master, target, overlap):
        self.targets.append(target)
        S, device = master["worlds"][0], master["_gpu"]
        if self.fault == "early_exit" and target > 0:
            S["status"] = "all_dead"
            return ["all_dead"]
        def step(t, n):
            a = np.asarray(device["F"]).copy()
            a[:, :S["na"]] += np.asarray(n * 0.0001, dtype=a.dtype)
            device["F"] = FakeArray(a)
        def pull(full):
            a = np.asarray(device["F"])[0].copy()
            if not full:
                a[S["na"]:] = 0
            return [a]
        DRIVER.run_chunks([S], int(round(target / S["dt"])), step_fn=step,
                          pull_fn=pull, record_fn=SG_NATIVE._record_host,
                          rec=S["rec"], crec=S["crec"], dt=S["dt"],
                          overlap=overlap, stop_when_dead=False)
        if self.fault == "missing_snap":
            S["snaps"].pop(target, None)
        if self.fault == "stale_snap" and target > 0:
            S["snaps"][target] = S["snaps"][0].copy()
        return [S["status"]]

    @staticmethod
    def snapshot_rec_gpu(S):
        return SC.snapshot_rec(S)


class TestFilmRecovery(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.island = self.root / "island"
        (self.island / "out/jobs").mkdir(parents=True)
        self.cfg = {"island": 1, "seed": 957, "batch_dtype": "f32",
                    "sim_backend": "gpu_batch", "record_mode": "device", "apply_mode": "async"}
        self.row = {"island": 1, "cand": "base_s3", "phase": "seed3", "seed": 959,
                    "kind": "ds2_eval", "status": "ok", "batched": True,
                    "sim_backend": "gpu_batch", "genome": copy.deepcopy(G), "ghash": FC.fleet_ghash(G),
                    "T_used": 1000.0, "horizon": {"T_used": 1000.0}, "interest": 42.5, "C9": 0.3,
                    "op": "merge_spatial_ic"}
        self.job = {"cand": "base_s3", "kind": "seed3", "seed": 959, "L": 8.0,
                    "genome": copy.deepcopy(G), "t0": 1000.0, "parents": ["base"]}
        self.item = {"name": "island1-base-s3", "island_dir": str(self.island),
                     "island": 1, "cand": "base_s3", "phase": "seed3", "seed": 959}
        self.flush_inputs()

    def tearDown(self):
        self.temp.cleanup()

    def flush_inputs(self):
        FC.write_json(self.island / "island_config.json", self.cfg)
        FC.write_json(self.island / "out/results.json", [self.row])
        FC.write_json(self.island / "out/jobs/s3g1_w0.json", [self.job])
        # Real batch manifests are lists of paths, not job dictionaries.
        FC.write_json(self.island / "out/jobs/batch_g1.json", ["out/jobs/s3g1_w0.json"])

    def plan(self, smoke=True):
        return FC.resolve_item(self.item, self.root, {}, smoke=smoke, record_mode="host", apply_mode="sync")

    def selection_file(self):
        path = self.root / "selection.json"
        FC.write_json(path, {"schema": FC.SCHEMA, "items": [self.item]})
        return path

    def make_spatial(self, missing=False):
        self.row.update(cand="base", phase="screen", seed=957, ic_merge=True)
        self.job.update(cand="base", kind="screen", ic_npz="out/jobs/ic_base.npz")
        self.job.pop("seed", None)  # Real screen jobs use cfg.seed.
        self.item.update(cand="base", phase="screen", seed=957)
        if not missing:
            np.savez_compressed(self.island / "out/jobs/ic_base.npz", ic=np.full((2, 16, 16), 0.2, np.float64))
        self.flush_inputs()

    def test_exact_confirmation_is_soup_despite_base_origin(self):
        p = self.plan()
        self.assertEqual(p["ic"]["kind"], "soup")
        self.assertEqual(p["original"]["seed"], 959)
        self.assertEqual(p["genome"]["id"], "base")
        self.assertEqual(p["original"]["dtype"], "f32")
        self.assertEqual(p["replay"]["snapshot_times"], [0.0, 25.0, 50.0])
        self.assertFalse(p["replay"]["exact_original_trace"])
        self.assertEqual(p["original"]["T_used"], 1000)
        self.assertNotEqual(p["original"]["T_used"], p["replay"]["T"])
        self.assertEqual(p["request_sha256"], FC.obj_hash({k:v for k,v in p.items() if k != "request_sha256"}))

    def test_spatial_source_f64_does_not_change_f32_simulation(self):
        self.make_spatial()
        p = self.plan()
        self.assertEqual(p["ic"]["kind"], "spatial")
        self.assertEqual(p["ic"]["source_dtype"], "float64")
        self.assertEqual(p["replay"]["dtype"], "f32")
        self.assertEqual(p["original"]["seed"], 957)
        self.assertEqual(p["ic"]["path"], str(self.island / "out/jobs/ic_base.npz"))

    def test_missing_spatial_ic_fails_closed(self):
        self.make_spatial(missing=True)
        with self.assertRaisesRegex(FC.MissingIC, "NOT soup"):
            self.plan()

    def test_no_base_ic_inheritance(self):
        self.item["ic_path"] = "out/jobs/ic_base.npz"
        with self.assertRaisesRegex(FC.CaptureError, "forbidden"):
            self.plan()

    def test_row_ic_marker_without_job_ic_is_error(self):
        self.row["ic_merge"] = True
        self.flush_inputs()
        with self.assertRaises(FC.MissingIC):
            self.plan()

    def test_relocated_ic_needs_matching_expected_hash(self):
        self.make_spatial()
        old = self.island / "out/jobs/ic_base.npz"
        new = self.root / "relocated.npz"
        old.rename(new)
        self.item["ic_path"] = str(new)
        with self.assertRaisesRegex(FC.CaptureError, "expected ic_sha256"):
            self.plan()
        self.item["ic_sha256"] = FC.file_hash(new)
        self.assertEqual(self.plan()["ic"]["path"], str(new))
        self.item["ic_sha256"] = "0" * 64
        with self.assertRaisesRegex(FC.CaptureError, "SHA256 mismatch"):
            self.plan()

    def test_invalid_ic_shape_and_nan_fail(self):
        self.make_spatial()
        np.savez(self.island / "out/jobs/ic_base.npz", ic=np.zeros((1, 16, 16), np.float32))
        with self.assertRaisesRegex(FC.CaptureError, "IC must"):
            self.plan()
        a = np.zeros((2, 16, 16), np.float32)
        a[0, 0, 0] = np.nan
        np.savez(self.island / "out/jobs/ic_base.npz", ic=a)
        with self.assertRaisesRegex(FC.CaptureError, "IC must"):
            self.plan()

    def test_cpu_fallback_overrides_reported_backend_and_needs_ack(self):
        self.row.update(ic_merge=True, batched=False)
        self.assertEqual(FC.resolve_backend(self.row, {})[0], "cpu")
        self.flush_inputs()
        with self.assertRaisesRegex(FC.CaptureError, "allow_backend_change"):
            self.plan()
        with self.assertRaisesRegex(FC.CaptureError, "contradicts"):
            FC.resolve_backend(self.row, {"backend": "gpu"})

    def test_config_for_other_island_rejected(self):
        self.cfg["island"] = 9
        self.flush_inputs()
        with self.assertRaisesRegex(FC.CaptureError, "another island"):
            self.plan()

    def test_dtype_conflict_or_missing_is_not_silent_f64(self):
        self.item["original"] = {"dtype": "f64"}
        with self.assertRaisesRegex(FC.CaptureError, "conflicting"):
            self.plan()
        self.cfg["batch_dtype"] = "f64"
        self.flush_inputs()
        self.assertEqual(self.plan()["replay"]["dtype"], "f64")
        self.cfg.pop("batch_dtype")
        self.item.pop("original")
        self.flush_inputs()
        with self.assertRaisesRegex(FC.CaptureError, "dtype missing"):
            self.plan()

    def test_horizon_is_not_capped_and_t0_is_not_start(self):
        self.row.update(T_used=40000.0, horizon={"T_used": 40000.0})
        self.flush_inputs()
        p = self.plan(smoke=False)
        self.assertEqual(p["replay"]["T"], 40000)
        self.assertEqual(p["replay"]["snapshot_times"][0], 0)
        self.assertEqual(len(p["replay"]["snapshot_times"]), 161)
        self.assertEqual(FC.snapshot_grid(275), [0.0, 250.0, 275.0])
        with self.assertRaisesRegex(FC.CaptureError, "no silent rounding"):
            FC.snapshot_grid(257)
        with self.assertRaisesRegex(FC.CaptureError, "no silent rounding"):
            FC.snapshot_grid(20000.00001)
        with self.assertRaises(FC.CaptureError):
            FC.snapshot_grid(float("nan"))

    def test_exact_job_and_result_ambiguity_fail(self):
        self.job["seed"] = 3
        self.flush_inputs()
        with self.assertRaisesRegex(FC.CaptureError, "exact job unavailable"):
            self.plan()
        self.job["seed"] = 959
        self.flush_inputs()
        FC.write_json(self.island / "out/results.json", [self.row, self.row])
        with self.assertRaisesRegex(FC.CaptureError, "found 2"):
            self.plan()
        self.item["row_index"] = 1
        self.assertEqual(self.plan()["row_source"]["index"], 1)

    @staticmethod
    def appledouble_fixture():
        # Same structural layout/length as the real 163-byte macOS sidecars in
        # state_isl*.tgz, without copying machine-specific extended attributes.
        return (struct.pack(">II16sH", 0x00051607, 0x00020000, b"Mac OS X        ", 2)
                + struct.pack(">III", 9, 50, 113)
                + struct.pack(">III", 2, 163, 0) + bytes(112) + b"0")

    def test_appledouble_sidecars_reproduce_decode_error_then_are_skipped(self):
        raw = self.appledouble_fixture()
        with self.assertRaisesRegex(UnicodeDecodeError, "utf-16-be"):
            json.loads(raw)
        sidecar = self.island / "out/jobs/._s3g1_w0.json"
        sidecar.write_bytes(raw)
        mac_dir = self.island / "out/jobs/__MACOSX"
        mac_dir.mkdir()
        nested = mac_dir / "._g1_w0.json"
        nested.write_bytes(raw)
        p = self.plan()
        self.assertEqual(p["job_source"]["path"], str(self.island / "out/jobs/s3g1_w0.json"))
        ignored = p["job_source"]["ignored_filesystem_metadata"]
        self.assertEqual({entry["path"] for entry in ignored}, {str(sidecar), str(nested)})
        self.assertTrue(all(entry["kind"] == "AppleDouble" and entry["bytes"] == 163 for entry in ignored))
        self.assertTrue(all(entry["sha256"] == FC.file_hash(sidecar) for entry in ignored))

    def test_metadata_style_filename_is_not_a_blanket_skip(self):
        bad = self.island / "out/jobs/._bad.json"
        bad.write_bytes(b"not JSON and not AppleDouble")
        with self.assertRaises(FC.CaptureError) as error:
            self.plan()
        self.assertIn(str(bad), str(error.exception))
        self.assertIn("JSONDecodeError", str(error.exception))
        self.assertIsNone(FC.appledouble_metadata(bad))
        # A valid JSON shard is still considered even if its name starts ._.
        FC.write_json(bad, [self.job])
        self.assertEqual(len(self.plan()["job_source"]["matching_copies"]), 2)

    def test_corrupt_real_shards_are_not_skipped_and_errors_name_path(self):
        bad = self.island / "out/jobs/g2_w0.json"
        for raw, expected_error in ((b'{"unfinished":', "JSONDecodeError"),
                                     (self.appledouble_fixture(), "UnicodeDecodeError")):
            with self.subTest(error=expected_error):
                bad.write_bytes(raw)
                self.assertIsNone(FC.appledouble_metadata(bad))  # No ._ filename.
                with self.assertRaises(FC.CaptureError) as error:
                    self.plan()
                self.assertIn(str(bad), str(error.exception))
                self.assertIn(expected_error, str(error.exception))

    def test_invalid_appledouble_header_or_entry_bounds_are_not_skipped(self):
        bad = self.island / "out/jobs/._invalid.json"
        original = self.appledouble_fixture()
        invalid = [original[:40], original[:4] + b"\x00\x03\x00\x00" + original[8:]]
        broken_bounds = bytearray(original)
        broken_bounds[30:34] = (1000).to_bytes(4, "big")
        invalid.append(bytes(broken_bounds))
        for raw in invalid:
            bad.write_bytes(raw)
            self.assertIsNone(FC.appledouble_metadata(bad))
            with self.assertRaises(FC.CaptureError) as error:
                self.plan()
            self.assertIn(str(bad), str(error.exception))

    def test_explicit_appledouble_job_path_is_an_error_not_silent_skip(self):
        sidecar = self.island / "out/jobs/._s3g1_w0.json"
        sidecar.write_bytes(self.appledouble_fixture())
        self.item["job_path"] = str(sidecar)
        with self.assertRaisesRegex(FC.CaptureError, "explicit job_path is AppleDouble") as error:
            self.plan()
        self.assertIn(str(sidecar), str(error.exception))

    def test_identical_job_copies_deduplicate_without_circular_metadata(self):
        FC.write_json(self.island / "out/jobs/copied.json", [self.job])
        p = self.plan()
        self.assertEqual(len(p["job_source"]["matching_copies"]), 2)
        FC.canonical(p)
        other = copy.deepcopy(self.job)
        other["t0"] = 2000.0
        FC.write_json(self.island / "out/jobs/copied.json", [other])
        with self.assertRaisesRegex(FC.CaptureError, "ambiguous exact jobs"):
            self.plan()

    def test_inline_row_job_preserve_different_ids_and_metadata_only_genome(self):
        self.item["row"] = self.row
        self.item["job"] = copy.deepcopy(self.job)
        self.item["job"]["genome"]["vtags"] = ["job_only_metadata"]
        self.assertEqual(self.plan()["genome"]["id"], "base")
        self.item["job"]["genome"]["K"] = [[0.75]]
        with self.assertRaisesRegex(FC.CaptureError, "different numerical genomes"):
            self.plan()

    def test_fake_native_capture_changing_frames_and_integrity(self):
        self.make_spatial()
        p = self.plan()
        path = self.root / "complete"
        fake = FakeNative()
        events = []
        m = FC.capture_one(p, path, fake, lambda: {"TEST_FAKE_NOT_GPU": True}, time.monotonic() + 60, events.append)
        self.assertEqual(fake.targets, [0, 25, 50])
        self.assertEqual(m["validation"]["changing_transitions"], 2)
        self.assertEqual(m["native_snapshot_device_checks"], 3)
        self.assertEqual(len(events), 3)
        _, check = FC.integrity_check(path, p)
        self.assertEqual(check["n_records"], 11)
        with np.load(path / "film.npz", allow_pickle=False) as z:
            for key in z.files:  # No object arrays needing pickle.
                _ = z[key]
            self.assertEqual(z["frames"].dtype, np.dtype("float32"))
            self.assertIn("not original trace", str(z["name"]))
            self.assertTrue(np.array_equal(z["frames"][0], np.full((1, 16, 16), .2, np.float32)))
        with (path / "film.npz").open("ab") as f:
            f.write(b"corruption")
        with self.assertRaisesRegex(FC.CaptureError, "artifact integrity failed"):
            FC.integrity_check(path, p)

    def test_stale_missing_and_early_stop_never_publish_success(self):
        for fault in ("missing_snap", "stale_snap", "early_exit"):
            with self.subTest(fault=fault):
                p = self.plan()
                path = self.root / fault
                with self.assertRaises(FC.CaptureError):
                    FC.capture_one(p, path, FakeNative(fault), lambda: {}, time.monotonic() + 60, lambda e: None)
                self.assertFalse((path / "manifest.json").exists())

    def test_manifest_tamper_and_request_change_fail_integrity(self):
        p = self.plan()
        path = self.root / "complete"
        FC.capture_one(p, path, FakeNative(), lambda: {}, time.monotonic() + 60, lambda e: None)
        other = copy.deepcopy(p)
        other["request_sha256"] = "0" * 64
        with self.assertRaisesRegex(FC.CaptureError, "different explicit request"):
            FC.integrity_check(path, other)
        m, _ = FC.read_json(path / "manifest.json")
        m["exact_original_trace"] = True
        FC.write_json(path / "manifest.json", m)
        with self.assertRaisesRegex(FC.CaptureError, "manifest content hash mismatch"):
            FC.integrity_check(path, p)

    def test_identical_frames_and_bad_record_counts_rejected(self):
        p = self.plan()
        path = self.root / "complete"
        FC.capture_one(p, path, FakeNative(), lambda: {}, time.monotonic() + 60, lambda e: None)
        with np.load(path / "film.npz", allow_pickle=False) as z:
            arrays = {k: z[k] for k in z.files}
        arrays["frames"][:] = arrays["frames"][0]
        with self.assertRaisesRegex(FC.CaptureError, "all frames are identical"):
            FC.validate_arrays(arrays, p)
        arrays["frames"][-1] += .1
        arrays["rec_ct"] = arrays["rec_ct"][:-1]
        with self.assertRaisesRegex(FC.CaptureError, "record stream"):
            FC.validate_arrays(arrays, p)

    def test_native_runtime_rejects_cpu_before_yield(self):
        import blobkit
        stub_jax = SimpleNamespace(default_backend=lambda: "cpu")
        # Isolate the GPU gate from the independent lock gate. The actual local
        # package currently has pre-existing 0.3.5 IC-hook lock-table drift.
        with mock.patch.object(blobkit, "verify_locks", return_value={"ok": True}):
            with mock.patch.dict(sys.modules, {"jax": stub_jax}):
                with self.assertRaisesRegex(FC.CaptureError, "no GPU backend"):
                    with FC.native_runtime("host", "sync"):
                        self.fail("must not yield on CPU")

    def test_native_runtime_checks_locks_even_when_import_check_skipped(self):
        import blobkit
        with mock.patch.dict(os.environ, {"BLOBKIT_SKIP_LOCK": "1"}):
            with mock.patch.object(blobkit, "verify_locks", side_effect=RuntimeError("LOCK DRIFT")) as gate:
                with self.assertRaisesRegex(RuntimeError, "LOCK DRIFT"):
                    with FC.native_runtime("host", "sync"):
                        self.fail("must not yield after lock drift")
                gate.assert_called_once_with(strict=True)

    def test_explicit_known_source_pins_match_local_035_bytes_and_preserve_drift(self):
        import blobkit
        pins = json.loads((Path(__file__).parent / "source_pins.blobkit-0.3.5.json").read_text())
        evidence = FC.source_lock_check(blobkit, pins)
        self.assertFalse(evidence["lock_check"]["ok"])
        self.assertFalse(evidence["new_locked_numerics_certification_claim"])
        self.assertEqual(set(evidence["lock_check"]["drift"]), {"assay_batch.py", "soup/sim_gpu.py"})
        self.assertEqual(len(evidence["expected_actual_sha256"]), 48)
        for entry in evidence["expected_actual_sha256"].values():
            self.assertEqual(entry["expected_source_sha256"], entry["actual_sha256"])

    def test_source_pins_reject_modified_manifest_or_unexpected_deployed_bytes(self):
        import blobkit
        pins = json.loads((Path(__file__).parent / "source_pins.blobkit-0.3.5.json").read_text())
        modified = copy.deepcopy(pins)
        modified["files"]["soup/sim_gpu.py"] = "0" * 64
        with self.assertRaisesRegex(FC.CaptureError, "not the exact reviewed"):
            FC.source_lock_check(blobkit, modified)
        actual_file_hash = FC.file_hash
        def drift(path):
            if str(path).endswith("soup/sim_gpu.py"):
                return "0" * 64
            return actual_file_hash(path)
        with mock.patch.object(FC, "file_hash", side_effect=drift):
            with self.assertRaisesRegex(FC.CaptureError, "unapproved source bytes"):
                FC.source_lock_check(blobkit, pins)
        with mock.patch.object(blobkit, "verify_locks", return_value={"ok": False, "drift": {"other.py": "drift"}}):
            with self.assertRaisesRegex(FC.CaptureError, "not exactly"):
                FC.source_lock_check(blobkit, pins)

    def test_capture_rejects_cpu_device_array_before_advance(self):
        fake = FakeNative()
        with mock.patch.object(FakeArray, "devices", return_value=[SimpleNamespace(platform="cpu")]):
            with self.assertRaisesRegex(FC.CaptureError, "not on GPU"):
                FC.capture_one(self.plan(), self.root / "cpu-array", fake, lambda: {},
                               time.monotonic() + 60, lambda e: None)
        self.assertEqual(fake.targets, [])

    def test_capture_rejects_silent_dtype_change_before_advance(self):
        class WrongDtype(FakeNative):
            def init_soup_gpu_batch(self, *args, **kwargs):
                ss = super().init_soup_gpu_batch(*args, **kwargs)
                ss["_gpu"]["F"] = FakeArray(np.asarray(ss["_gpu"]["F"], dtype=np.float64))
                return ss
        fake = WrongDtype()
        with self.assertRaisesRegex(FC.CaptureError, "state dtype"):
            FC.capture_one(self.plan(), self.root / "wrong-dtype", fake, lambda: {},
                           time.monotonic() + 60, lambda e: None)
        self.assertEqual(fake.targets, [])

    def test_budget_failure_precedes_native_initialization(self):
        fake = FakeNative()
        with self.assertRaises(FC.BudgetExceeded):
            FC.capture_one(self.plan(), self.root / "budget", fake, lambda: {}, time.monotonic() - 1, lambda e: None)
        self.assertEqual(fake.targets, [])

    def test_plan_only_and_empty_selection_exit_codes(self):
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            rc = FC.main([str(self.selection_file()), str(self.root / "output"), "--plan-only"])
        self.assertEqual(rc, 0, stream.getvalue())
        with mock.patch.object(FC, "native_runtime", side_effect=AssertionError("no GPU work allowed")):
            FC.write_json(self.root / "empty.json", {"schema": FC.SCHEMA, "items": []})
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                rc = FC.main([str(self.root / "empty.json"), str(self.root / "empty-output")])
        self.assertEqual(rc, 1)
        self.assertNotIn("FILM_SELECTION_COMPLETE", stream.getvalue())
        self.assertNotIn("FILMCAP_DONE", stream.getvalue())

    def test_missing_ic_report_nonzero_without_native_import(self):
        self.make_spatial(missing=True)
        output = self.root / "missing-output"
        with mock.patch.object(FC, "native_runtime", side_effect=AssertionError("must not initialize GPU")):
            with contextlib.redirect_stdout(io.StringIO()):
                rc = FC.main([str(self.selection_file()), str(output)])
        self.assertEqual(rc, 1)
        report = json.loads(next(output.glob("reports/*/report.json")).read_text())
        self.assertEqual(report["items"][0]["status"], "skipped_missing_ic")
        self.assertEqual(report["successful_items"], 0)

    def test_idempotent_skip_requires_full_integrity_and_does_not_reinit(self):
        fake = FakeNative()
        @contextlib.contextmanager
        def runtime(*args):
            yield fake, lambda: {"TEST_FAKE_NOT_GPU": True}
        output = self.root / "idempotent-output"
        args = [str(self.selection_file()), str(output), "--smoke"]
        with mock.patch.object(FC, "native_runtime", side_effect=runtime) as patched:
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(FC.main(args), 0)
                self.assertEqual(FC.main(args), 0)
            self.assertEqual(patched.call_count, 1)
            film = output / "smoke" / self.item["name"] / "film.npz"
            film.write_bytes(b"broken")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(FC.main(args), 1)
            self.assertEqual(patched.call_count, 1)

    def test_partial_success_is_failure_for_intended_selection(self):
        selection = self.selection_file()
        data = json.loads(selection.read_text())
        bad = copy.deepcopy(self.item)
        bad.update(name="missing-row", cand="does-not-exist")
        data["items"].append(bad)
        FC.write_json(selection, data)
        @contextlib.contextmanager
        def runtime(*args):
            yield FakeNative(), lambda: {"TEST_FAKE_NOT_GPU": True}
        # Production T=250 => two frames; this still uses synthetic fields only.
        self.row.update(T_used=250, horizon={"T_used": 250})
        self.flush_inputs()
        stream = io.StringIO()
        with mock.patch.object(FC, "native_runtime", side_effect=runtime):
            with contextlib.redirect_stdout(stream):
                rc = FC.main([str(selection), str(self.root / "partial-success")])
        self.assertEqual(rc, 1, stream.getvalue())
        self.assertIn("FILM_COMPLETE", stream.getvalue())
        self.assertNotIn("FILM_SELECTION_COMPLETE", stream.getvalue())

    def test_pure_native_async_extract_apply_snapshots_match_host_record(self):
        a = SC.init_soup(G, L=8, n_soup=1, dtype="f32", workers=1)
        b = copy.deepcopy(a)
        a["snap_t"] = b["snap_t"] = [0.0, 25.0, 50.0]
        # Do not share the mutable schedule between recorders.
        a["snap_t"] = list(a["snap_t"])
        for t in (0, 1250, 2500):
            F = np.full_like(a["F"], .2 + t / 10000.0)
            a["F"], b["F"] = F.copy(), F.copy()
            SC._record(a, t)
            ctx, acts, chans_mem, snap_due = AA.payload_of(b, t)
            delta = AA.extract_record(ctx, acts, chans_mem, t, snap_due)
            AA.apply_record(b, delta, t)
        self.assertEqual(a["ts"], b["ts"])
        self.assertEqual(sorted(a["snaps"]), [0, 25, 50])
        for key in a["snaps"]:
            np.testing.assert_array_equal(a["snaps"][key], b["snaps"][key])
        self.assertFalse(np.array_equal(a["snaps"][0], a["snaps"][50]))


if __name__ == "__main__":
    unittest.main()
