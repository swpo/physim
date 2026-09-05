#!/usr/bin/env python3
"""Safe, selection-driven v3 GPU film re-simulation. No ranking or scoring.

Run --plan-only first, then --smoke (50tu, first selected item). Real films
use the original row's T_used, 250tu snapshots, and an exact job/IC match.
Use an external hard timeout; --max-wall-seconds is a soft boundary budget.
See README.md / PLAN.md for the explicit selection format and limitations.
"""
from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import fcntl
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import platform
import re
import shutil
import sys
import time
import uuid

SCHEMA = "v3-film-replay-v1"
# Explicit, root-approved 0.3.5 IC-hook source identity; not a relock or certification.
APPROVED_SOURCE_PINS_SHA256 = "371f8ae1f7d2087827c5e490131782c0115c9cb0b9f3e101a76f41773e571b8e"
DT, DX, REC_TU, CREC_TU, FRAME_TU = 0.02, 0.5, 5.0, 25.0, 250.0
TRACE_LABEL = "GPU re-simulation / replay; NOT the exact original trace"
METRIC_KEYS = ("interest", "interest_v2", "C9", "C9_factors", "c9_partial",
               "cell", "spatial_class", "metrics", "flags", "summary", "horizon")


class CaptureError(RuntimeError):
    pass


class MissingIC(CaptureError):
    pass


class BudgetExceeded(CaptureError):
    pass


def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("utf-8")


def obj_hash(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def array_hash(array):
    import numpy as np
    a = np.ascontiguousarray(array)
    h = hashlib.sha256(canonical({"shape": list(a.shape), "dtype": a.dtype.str}))
    h.update(memoryview(a).cast("B"))
    return h.hexdigest()


def read_json(path):
    path = Path(path).resolve()
    try:
        raw = path.read_bytes()
        value = json.loads(raw)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise CaptureError(f"cannot read JSON {path}: {type(exc).__name__}: {exc}") from exc
    return value, {"path": str(path), "sha256": hashlib.sha256(raw).hexdigest()}


def appledouble_metadata(path):
    """Recognize a real AppleDouble ._* sidecar, not arbitrary hidden/bad JSON.

    Mac-created tar archives can contain these binary extended-attribute files.
    Require the filename convention, magic, supported version, and a complete
    in-bounds entry table. Anything else still goes through strict JSON parsing.
    """
    path = Path(path)
    if not path.name.startswith("._"):
        return None
    try:
        raw = path.read_bytes()
    except OSError:
        return None  # read_json will report the read failure with its full path.
    if len(raw) < 26 or raw[:4] != b"\x00\x05\x16\x07":
        return None
    version = int.from_bytes(raw[4:8], "big")
    if version not in (0x00010000, 0x00020000):
        return None
    count = int.from_bytes(raw[24:26], "big")
    table_end = 26 + 12 * count
    if table_end > len(raw):
        return None
    for i in range(count):
        entry = raw[26 + 12 * i:38 + 12 * i]
        offset = int.from_bytes(entry[4:8], "big")
        length = int.from_bytes(entry[8:12], "big")
        if offset < table_end or offset + length > len(raw):
            return None
    return {"kind": "AppleDouble", "path": str(path.resolve()),
            "version": f"0x{version:08x}", "entries": count, "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest()}


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp-" + uuid.uuid4().hex)
    try:
        with tmp.open("wb") as f:
            f.write(json.dumps(value, indent=2, sort_keys=True,
                               allow_nan=False).encode() + b"\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


def abs_path(value, base):
    p = Path(value).expanduser()
    return p.resolve() if p.is_absolute() else (Path(base) / p).resolve()


def positive_number(value, name):
    if isinstance(value, bool):
        raise CaptureError(f"{name} must be a finite positive number")
    try:
        value = float(value)
    except (TypeError, ValueError):
        raise CaptureError(f"{name} must be a finite positive number") from None
    if not math.isfinite(value) or value <= 0:
        raise CaptureError(f"{name} must be a finite positive number")
    return value


def integer(value, name):
    if isinstance(value, bool):
        raise CaptureError(f"{name} must be an integer")
    try:
        iv = int(value)
        if float(value) != iv:
            raise ValueError()
    except (TypeError, ValueError, OverflowError):
        raise CaptureError(f"{name} must be an integer") from None
    return iv


def genome_dict(value):
    if isinstance(value, str):
        value = json.loads(value)
    if not isinstance(value, dict) or not all(k in value for k in ("acts", "chans", "W", "K")):
        raise CaptureError("genome must contain acts/chans/W/K")
    canonical(value)  # Reject NaN/Infinity and non-JSON data.
    if not value["acts"] or not value["chans"]:
        raise CaptureError("empty activator/channel layout is not supported")
    return value


def fleet_ghash(g):
    # Verbatim pod_lib.ghash contract. No pod/scoring modules are imported.
    key = json.dumps([g["acts"], g["chans"], g["W"], g["K"],
                      sorted(map(list, g.get("bilin", [])))],
                     sort_keys=True, default=float)
    return hashlib.sha1(key.encode()).hexdigest()[:16]


def snapshot_grid(T, smoke=False):
    T = positive_number(T, "T")
    quantum = CREC_TU if smoke else FRAME_TU
    if T % CREC_TU != 0.0:
        raise CaptureError("T_used must be on the native 25tu CREC grid; no silent rounding")
    times = [float(i * quantum) for i in range(int(math.floor(T / quantum)) + 1)]
    if times[-1] != T:
        times.append(T)  # Preserve an off-250tu original endpoint, if CREC-aligned.
    return times


def _same_identity(row, item):
    return (str(row.get("island")) == str(item["island"])
            and row.get("cand") == item["cand"]
            and row.get("phase") == item["phase"]
            and integer(row.get("seed"), "row.seed") == integer(item["seed"], "seed"))


def select_row(item, root, cache):
    if "row" in item:
        row = item["row"]
        if not isinstance(row, dict):
            raise CaptureError("inline row must be an object")
        source = {"path": None, "kind": "explicit_selection_inline_row"}
        for key in ("cand", "phase", "seed", "island"):
            if key in item and str(item[key]) != str(row.get(key)):
                raise CaptureError(f"inline row disagrees with selection.{key}")
    else:
        for key in ("island", "cand", "phase", "seed"):
            if key not in item:
                raise CaptureError(f"selection identity missing {key}; no candidate-name heuristics")
        path = abs_path(item.get("results_path", "out/results.json"), root)
        if str(path) not in cache:
            cache[str(path)] = read_json(path)
        rows, src = cache[str(path)]
        if not isinstance(rows, list):
            raise CaptureError("results must be a JSON row list")
        if "row_index" in item:
            idx = integer(item["row_index"], "row_index")
            if not 0 <= idx < len(rows) or not _same_identity(rows[idx], item):
                raise CaptureError("row_index does not match exact island/cand/phase/seed")
            matches = [(idx, rows[idx])]
        else:
            matches = [(i, r) for i, r in enumerate(rows) if _same_identity(r, item)]
        if len(matches) != 1:
            raise CaptureError(f"need one exact result row; found {len(matches)} (use row_index)")
        idx, row = matches[0]
        source = dict(src, index=idx, kind="results_row")
    row_sha = obj_hash(row)
    if item.get("row_sha256") and item["row_sha256"] != row_sha:
        raise CaptureError("row SHA256 does not match the explicit selection")
    source["row_sha256"] = row_sha
    for key in ("cand", "phase", "seed", "island", "genome", "T_used"):
        if key not in row or row[key] is None:
            raise CaptureError(f"selected row missing {key}")
    if row.get("status") != "ok":
        raise CaptureError("only completed status=ok original rows are intended film inputs")
    return row, source


def select_job(item, row, root, cfg, cache):
    def matches(job):
        return (isinstance(job, dict) and job.get("cand") == row["cand"]
                and job.get("kind", "screen") == row["phase"]
                and integer(job.get("seed", cfg.get("seed")), "job.seed") == int(row["seed"]))
    if "job" in item:
        job = item["job"]
        if not matches(job):
            raise CaptureError("inline job does not match exact cand/phase/seed")
        return job, {"kind": "explicit_selection_inline_job", "path": None,
                     "job_sha256": obj_hash(job)}
    if item.get("job_path"):
        paths = [abs_path(item["job_path"], root)]
    else:
        jobs_dir = abs_path(item.get("jobs_dir", "out/jobs"), root)
        paths = sorted(jobs_dir.rglob("*.json")) if jobs_dir.is_dir() else []
    candidates, ignored_metadata = [], []
    for path in paths:
        metadata = appledouble_metadata(path)
        if metadata is not None:
            if item.get("job_path"):
                raise CaptureError(f"explicit job_path is AppleDouble metadata, not a job shard: {path}")
            ignored_metadata.append(metadata)
            continue
        if str(path) not in cache:
            cache[str(path)] = read_json(path)
        jobs, src = cache[str(path)]
        if not isinstance(jobs, list):
            raise CaptureError(f"job shard is not a JSON list: {path}")
        for i, job in enumerate(jobs):
            if item.get("job_path") and "job_index" in item and i != int(item["job_index"]):
                continue
            if matches(job):
                candidates.append((job, dict(src, index=i, job_sha256=obj_hash(job))))
    if not candidates:
        raise CaptureError("exact job unavailable; supply the original job/shard, not its base candidate")
    # Identical copies of a shard are harmless; differing jobs must be disambiguated.
    if len({src["job_sha256"] for _, src in candidates}) != 1:
        raise CaptureError("ambiguous exact jobs; provide job_path and job_index")
    job, source = candidates[0]
    source["matching_copies"] = [dict(src) for _, src in candidates]
    source["ignored_filesystem_metadata"] = ignored_metadata
    return job, source


def resolve_backend(row, supplied):
    reported = row.get("sim_backend")
    if row.get("ic_merge") is True and row.get("batched") is False:
        actual, evidence = "cpu", "v3 _eval_single_ic fallback: ic_merge=true, batched=false"
    elif row.get("batched") is True:
        actual, evidence = "gpu", "row.batched=true"
        if reported == "cpu":
            raise CaptureError("row says both batched=true and sim_backend=cpu")
    elif reported in ("cpu", "gpu", "gpu_batch"):
        actual = "cpu" if reported == "cpu" else "gpu"
        evidence = "row.sim_backend (not a CPU spatial-IC fallback)"
    elif supplied.get("backend") in ("cpu", "gpu"):
        actual, evidence = supplied["backend"], "selection.original.backend"
    else:
        raise CaptureError("original CPU/GPU backend is unknown; state it explicitly with evidence")
    if supplied.get("backend") and supplied["backend"] != actual:
        raise CaptureError(f"selection.original.backend contradicts actual original {actual}")
    return actual, evidence


def resolve_ic(item, row, job, root, g, L):
    import numpy as np
    ref = job.get("ic_npz")
    if row.get("ic_merge") is True and not ref:
        raise MissingIC("spatial original row has no exact-job ic_npz; do not substitute soup")
    if not ref:
        if item.get("ic_path") or item.get("ic_sha256"):
            raise CaptureError("this exact job is soup; attaching a base/parent IC is forbidden")
        return {"kind": "soup", "original_path": None, "path": None, "sha256": None,
                "basis": "exact matched job has no ic_npz; no suffix/parent inheritance"}
    if row.get("ic_merge") is False:
        raise CaptureError("job has spatial ic_npz but row explicitly says ic_merge=false")
    expected_path = abs_path(ref, root)
    path = abs_path(item["ic_path"], root) if item.get("ic_path") else expected_path
    if path != expected_path and not item.get("ic_sha256"):
        raise CaptureError("relocated IC requires explicit ic_path AND expected ic_sha256")
    if not path.is_file():
        raise MissingIC(f"exact spatial IC unavailable: {path}; skipped, NOT soup")
    sha = file_hash(path)
    if item.get("ic_sha256") and item["ic_sha256"] != sha:
        raise CaptureError("IC SHA256 mismatch")
    with np.load(path, allow_pickle=False) as z:
        if "ic" not in z:
            raise MissingIC(f"spatial IC file has no 'ic' array: {path}")
        ic = z["ic"]
    N, nf = int(round(L / DX)), len(g["acts"]) + len(g["chans"])
    if ic.shape != (nf, N, N) or ic.dtype.kind != "f" or not np.isfinite(ic).all():
        raise CaptureError(f"IC must be finite floating ({nf}, {N}, {N}); got {ic.shape}/{ic.dtype}")
    return {"kind": "spatial", "original_path": str(ref),
            "resolved_original_path": str(expected_path), "path": str(path),
            "sha256": sha, "array_sha256": array_hash(ic),
            "source_dtype": str(ic.dtype), "shape": list(ic.shape),
            "basis": "ic_npz on the exact matched cand/phase/seed job"}


def resolve_item(item, selection_base, cache, *, smoke, record_mode, apply_mode, source_pins=None):
    if not isinstance(item, dict):
        raise CaptureError("each selection item must be an object")
    if not item.get("island_dir"):
        raise CaptureError("each item needs island_dir (worker HERE; relative IC paths use this root)")
    root = abs_path(item["island_dir"], selection_base)
    cfg_path = abs_path(item.get("config_path", "island_config.json"), root)
    cfg, cfg_src = read_json(cfg_path) if cfg_path.is_file() else ({}, {"path": str(cfg_path), "missing": True})
    row, row_src = select_row(item, root, cache)
    if cfg.get("island") is not None and str(cfg["island"]) != str(row["island"]):
        raise CaptureError("island_config belongs to another island; supply the historical config_path")
    job, job_src = select_job(item, row, root, cfg, cache)
    g = genome_dict(row["genome"])
    if fleet_ghash(g) != fleet_ghash(genome_dict(job["genome"])):
        raise CaptureError("row and exact job have different numerical genomes")
    if row.get("ghash") and row["ghash"] != fleet_ghash(g):
        raise CaptureError("row.ghash does not match its genome")
    if item.get("genome_sha256") and item["genome_sha256"] != obj_hash(g):
        raise CaptureError("genome SHA256 mismatch")
    original = item.get("original") or {}
    backend, backend_basis = resolve_backend(row, original)
    if backend == "cpu" and item.get("allow_backend_change") is not True:
        raise CaptureError("CPU original -> GPU re-simulation requires allow_backend_change=true; RNG differs")
    dtype_sources = []
    if row.get("dtype"):
        dtype_sources.append((row["dtype"], "row.dtype"))
    if original.get("dtype"):
        dtype_sources.append((original["dtype"], "selection.original.dtype"))
    if backend == "gpu" and row.get("batched") is True and cfg.get("batch_dtype"):
        dtype_sources.append((cfg["batch_dtype"], "config.batch_dtype (snapshot; not proof of historical env)"))
    if not dtype_sources:
        if backend == "cpu" and row.get("ic_merge") is True and row.get("batched") is False:
            dtype_sources.append(("f32", "known _eval_single_ic -> assay_v3 -> init_soup default f32"))
        else:
            raise CaptureError("dtype missing; provide original.dtype=f32/f64 or the matching batch config")
    if len({v for v, _ in dtype_sources}) != 1 or dtype_sources[0][0] not in ("f32", "f64"):
        raise CaptureError(f"unknown/conflicting simulation dtype: {dtype_sources}")
    dtype = dtype_sources[0][0]
    fallback_cpu = backend == "cpu" and row.get("ic_merge") is True and row.get("batched") is False
    L = 128.0 if fallback_cpu else positive_number(job.get("L") or 128.0, "job.L")
    L_basis = ("known CPU fallback did not pass job.L; assay_v3 default 128" if fallback_cpu
               else "exact job.L or native fleet worker default 128")
    for key, supplied_L in (("row.L", row.get("L")), ("original.L", original.get("L"))):
        if supplied_L is not None and not math.isclose(float(supplied_L), L, rel_tol=0.0, abs_tol=1e-9):
            raise CaptureError(f"{key} contradicts original worker/job L={L}")
    if not math.isclose(L / DX, round(L / DX), rel_tol=0.0, abs_tol=1e-9):
        raise CaptureError("L must exactly match the native dx=0.5 grid")
    T_original = positive_number(row["T_used"], "row.T_used")
    for supplied_T in (original.get("T_used"), (row.get("horizon") or {}).get("T_used")):
        if supplied_T is not None and not math.isclose(float(supplied_T), T_original, rel_tol=0.0, abs_tol=1e-9):
            raise CaptureError("T_used provenance conflicts; no default or cap is permitted")
    # Fleet workers do not pass custom soup parameters. Require a different helper
    # if a nonstandard job needs them rather than silently accepting an override.
    for obj in (job, original):
        for key in ("noise", "n_soup", "kicks", "gpu_seed"):
            if key in obj:
                raise CaptureError(f"custom {key} is not supported by this fleet-only helper")
    ic = resolve_ic(item, row, job, root, g, L)
    name = item.get("name") or f"i{row['island']}_{row['cand']}_{row['phase']}_seed{row['seed']}"
    if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,159}", name):
        raise CaptureError("name must be a safe unique filename (letters/digits/._-, max160)")
    capture_T = 50.0 if smoke else T_original
    if smoke and T_original < capture_T:
        raise CaptureError("50tu smoke would exceed original T_used")
    schedule = snapshot_grid(capture_T, smoke)
    plan = {
        "schema": SCHEMA, "name": name, "island_dir": str(root),
        "row": row, "job": job, "row_source": row_src, "job_source": job_src,
        "genome": g, "genome_sha256": obj_hash(g), "fleet_ghash": fleet_ghash(g),
        "ic": ic, "config_snapshot": cfg, "config_source": cfg_src,
        "original": {"island": row["island"], "cand": row["cand"], "phase": row["phase"],
                     "seed": integer(row["seed"], "row.seed"), "T_used": T_original,
                     "L": L, "L_basis": L_basis, "backend": backend,
                     "reported_sim_backend": row.get("sim_backend"), "backend_basis": backend_basis,
                     "dtype": dtype, "dtype_evidence": dtype_sources,
                     "metrics": {k: row[k] for k in METRIC_KEYS if k in row},
                     "environment": original.get("environment") or {"historical_versions": "unknown"},
                     "record_mode_from_config_snapshot": cfg.get("record_mode", "unknown"),
                     "apply_mode_from_config_snapshot": cfg.get("apply_mode", "unknown")},
        "replay": {"label": TRACE_LABEL, "exact_original_trace": False,
                   "display_name": name + " [GPU re-simulation; not original trace]",
                   "mode": "smoke" if smoke else "capture", "backend": "gpu", "dtype": dtype,
                   "T": capture_T, "snapshot_times": schedule,
                   "frame_spacing_tu": CREC_TU if smoke else FRAME_TU,
                   "preserve_off_grid_endpoint": capture_T % FRAME_TU != 0,
                   "L": L, "dx": DX, "dt": DT, "noise": 0.002, "n_soup": 12,
                   "kicks": "native default 0.5px", "gpu_seed": int(row["seed"]),
                   "record_mode": record_mode, "apply_mode": apply_mode,
                   "overlap": False, "batch_lanes": 1,
                   "metrics_origin": "original_result_row; NOT recomputed for this replay",
                   "cpu_to_gpu_noise_stream_change": backend == "cpu",
                   "limitations": ["Replay is not an archived trace or a score reconfirmation.",
                                    "GPU threefry noise differs from CPU PCG64.",
                                    "Single-lane shape, backend versions and hardware can change trajectories.",
                                    "Historical environment may be only partly known; config is a snapshot.",
                                    "Soup IC is regenerated; actual starting fields are saved and hashed."]},
        "runtime_source_pins": source_pins,
        "helper_sha256": file_hash(__file__),
    }
    nframes, na, N = len(schedule), len(g["acts"]), int(round(L / DX))
    plan["estimate"] = {"frames": nframes, "steps": int(round(capture_T / DT)),
                        "raw_frame_bytes": nframes * na * N * N * (4 if dtype == "f32" else 8),
                        "wall_time": "unknown until GPU smoke; short smoke includes compilation"}
    plan["request_sha256"] = obj_hash(plan)
    return plan


def check_deadline(deadline):
    if time.monotonic() >= deadline:
        raise BudgetExceeded("soft wall budget reached at a frame boundary; no horizon truncation")


def validate_arrays(arrays, plan):
    import numpy as np
    required = ("frames", "ts", "rec_ts", "rec_ct", "na", "status", "T", "seed", "genome", "name")
    if any(k not in arrays for k in required):
        raise CaptureError("film is missing house-renderer fields")
    frames, ts = np.asarray(arrays["frames"]), np.asarray(arrays["ts"])
    rec_ts, rec_ct = np.asarray(arrays["rec_ts"]), np.asarray(arrays["rec_ct"])
    expected = np.asarray(plan["replay"]["snapshot_times"], dtype=np.float64)
    na, N = len(plan["genome"]["acts"]), int(round(plan["replay"]["L"] / DX))
    want_dtype = np.dtype("float32" if plan["replay"]["dtype"] == "f32" else "float64")
    if frames.shape != (len(expected), na, N, N) or frames.dtype != want_dtype:
        raise CaptureError(f"bad frames shape/dtype: {frames.shape}/{frames.dtype}")
    if not np.array_equal(ts, expected) or not np.isfinite(frames).all():
        raise CaptureError("missing/off-grid snapshots or nonfinite frames")
    if len(ts) < 2 or not np.all(np.diff(ts) > 0):
        raise CaptureError("film needs at least two increasing snapshot times")
    changes = [float(np.max(np.abs(frames[i].astype(np.float64) - frames[i-1])))
               for i in range(1, len(frames))]
    if not any(d > 0 for d in changes):
        raise CaptureError("all frames are identical; stale/empty capture is not success")
    expected_rec = np.arange(int(round(plan["replay"]["T"] / REC_TU)) + 1) * REC_TU
    if (not np.array_equal(rec_ts, expected_rec) or rec_ct.shape != rec_ts.shape
            or not np.isfinite(rec_ct).all() or np.any(rec_ct < 0)
            or np.any(rec_ct != np.round(rec_ct))):
        raise CaptureError("rec_ts/rec_ct do not cover the exact native 5tu record stream")
    for key, expected_scalar in (("status", "ok"), ("T", plan["replay"]["T"]),
                                 ("seed", plan["original"]["seed"]),
                                 ("name", plan["replay"]["display_name"]), ("na", na)):
        if np.asarray(arrays[key]).item() != expected_scalar:
            raise CaptureError(f"film scalar {key} does not match manifest request")
    if obj_hash(json.loads(np.asarray(arrays["genome"]).item())) != plan["genome_sha256"]:
        raise CaptureError("film genome does not match manifest request")
    return {"n_frames": len(ts), "n_records": len(rec_ts),
            "changing_transitions": sum(d > 0 for d in changes),
            "max_abs_frame_delta": max(changes), "per_transition_max_abs_delta": changes,
            "frames_dtype": str(frames.dtype), "finite": True,
            "snapshot_grid_exact": True, "record_grid_exact": True}


def integrity_check(directory, plan):
    import numpy as np
    directory = Path(directory)
    manifest, _ = read_json(directory / "manifest.json")
    expected_hash = manifest.pop("manifest_sha256", None)
    if not expected_hash or obj_hash(manifest) != expected_hash:
        raise CaptureError("manifest content hash mismatch")
    if (manifest.get("schema") != SCHEMA or manifest.get("status") != "complete"
            or manifest.get("request_sha256") != plan["request_sha256"]):
        raise CaptureError("manifest is incomplete or belongs to a different explicit request")
    stored_plan, _ = read_json(directory / "request.json")
    stored_request_hash = stored_plan.pop("request_sha256", None)
    if obj_hash(stored_plan) != stored_request_hash or stored_request_hash != plan["request_sha256"]:
        raise CaptureError("saved request integrity mismatch")
    artifacts = manifest.get("artifacts") or {}
    if not {"film.npz", "request.json", "genome.json", "initial_state.npz"}.issubset(artifacts):
        raise CaptureError("manifest lacks required artifact hashes")
    for name, entry in artifacts.items():
        if Path(name).name != name:
            raise CaptureError("invalid manifest artifact path")
        p = directory / name
        if not p.is_file() or p.stat().st_size != entry["bytes"] or file_hash(p) != entry["sha256"]:
            raise CaptureError(f"artifact integrity failed: {name}")
    with np.load(directory / "film.npz", allow_pickle=False) as z:
        validation = validate_arrays(z, plan)
        first_frame = z["frames"][0]
    with np.load(directory / "initial_state.npz", allow_pickle=False) as z:
        initial = z["ic"]
    if (array_hash(initial) != manifest["initial_state"]["array_sha256"]
            or not np.array_equal(first_frame, initial[:len(plan["genome"]["acts"])])):
        raise CaptureError("t=0 frame does not equal the saved, hashed starting IC")
    if manifest.get("native_snapshot_device_checks") != len(plan["replay"]["snapshot_times"]):
        raise CaptureError("native snapshot/device freshness checks are incomplete")
    manifest["manifest_sha256"] = expected_hash
    return manifest, validation


def validate_source_pins(pins):
    if not isinstance(pins, dict) or obj_hash(pins) != APPROVED_SOURCE_PINS_SHA256:
        raise CaptureError("source pins are not the exact reviewed 0.3.5 manifest; unknown drift is forbidden")
    return pins


def source_lock_check(blobkit, pins=None):
    if pins is None:
        return {"policy": "strict_legacy_locks", "lock_check": blobkit.verify_locks(strict=True)}
    validate_source_pins(pins)
    pkg = Path(blobkit.__file__).resolve().parent
    if blobkit.__version__ != pins["module_version"]:
        raise CaptureError("source-pin module version mismatch")
    lock_path = pkg / "_locks.json"
    actual_table_sha = file_hash(lock_path)
    if actual_table_sha != pins["upstream_lock_table_sha256"]:
        raise CaptureError("legacy lock table changed; source-pin exception is not applicable")
    table, _ = read_json(lock_path)
    expected_actual = {}
    for rel, expected in pins["files"].items():
        actual = file_hash(pkg / rel)
        expected_actual[rel] = {"expected_source_sha256": expected, "actual_sha256": actual,
                                "upstream_locked_sha256": table["files"].get(rel)}
        if actual != expected:
            raise CaptureError(f"unapproved source bytes {rel}: expected {expected}; actual {actual}")
    original_report = blobkit.verify_locks(quiet=True)
    if set(original_report["drift"]) != set(pins["allowed_lock_drift"]):
        raise CaptureError("legacy lock drift is not exactly the reviewed two-file IC-hook promotion")
    return {"policy": "explicit_known_0.3.5_source_pins_for_re_simulation_only",
            "new_locked_numerics_certification_claim": False,
            "pins_document_sha256": obj_hash(pins), "pins_document": pins,
            "lock_check": original_report, "expected_actual_sha256": expected_actual,
            "upstream_lock_table_expected_sha256": pins["upstream_lock_table_sha256"],
            "upstream_lock_table_actual_sha256": actual_table_sha}


def runtime_info(blobkit, jax, SG, source_pins=None):
    versions = {"blobkit": blobkit.__version__, "python": sys.version}
    for package in ("numpy", "scipy", "jax", "jaxlib"):
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = "unknown"
    pkg = Path(blobkit.__file__).resolve().parent
    sources = {}
    for rel in ("genome.py", "soup/sim_cpu.py", "soup/sim_gpu.py", "soup/sim_v1.py",
                "soup/driver.py", "soup/devrec_proto.py", "soup/asyncapply_proto.py", "_locks.json"):
        p = pkg / rel
        sources[rel] = {"path": str(p), "sha256": file_hash(p)} if p.is_file() else {"missing": True}
    source_verification = source_lock_check(blobkit, source_pins)
    return {"versions": versions, "platform": platform.platform(), "executable": sys.executable,
            "jax_default_backend": jax.default_backend(), "jax_enable_x64": bool(jax.config.jax_enable_x64),
            "devices": [{"id": d.id, "platform": d.platform, "kind": d.device_kind, "description": str(d)}
                        for d in jax.devices()], "source_files": sources,
            "environment_variables": {k: os.environ.get(k) for k in
                ("JAX_ENABLE_X64", "JAX_PLATFORM_NAME", "JAX_PLATFORMS", "XLA_FLAGS",
                 "XLA_PYTHON_CLIENT_PREALLOCATE", "XLA_PYTHON_CLIENT_MEM_FRACTION",
                 "CUDA_VISIBLE_DEVICES", "BLOBGPU_REC_THREADS", "OMP_NUM_THREADS",
                 "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "BLOBKIT_SKIP_LOCK")},
            "rng": "jax threefry folded on absolute step and activator index",
            "einsum_precision": "HIGHEST (native make_stepper)",
            "lock_check": source_verification["lock_check"], "source_verification": source_verification}


@contextlib.contextmanager
def native_runtime(record_mode, apply_mode, source_pins=None):
    # Lazy imports keep --plan-only and all metadata tests GPU-free.
    import blobkit
    source_lock_check(blobkit, source_pins)
    import jax
    from blobkit.soup import sim_gpu as SG
    if jax.default_backend() != "gpu":
        raise CaptureError("no GPU backend; refusing an accidental CPU simulation")
    DR = AA = None
    try:
        if record_mode == "device":
            from blobkit.soup import devrec_proto as DR
            DR.install(async_apply=(apply_mode == "async"))
        elif apply_mode == "async":
            from blobkit.soup import asyncapply_proto as AA
            AA.install()
        yield SG, lambda: runtime_info(blobkit, jax, SG, source_pins)
    finally:
        if DR is not None:
            DR.uninstall()
            if apply_mode == "async":
                from blobkit.soup import asyncapply_proto as AA
        if AA is not None:
            AA.uninstall()


def capture_one(plan, directory, SG, get_environment, deadline, progress):
    import numpy as np
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=False)
    write_json(directory / "request.json", plan)
    write_json(directory / "genome.json", plan["genome"])
    ic = None
    if plan["ic"]["kind"] == "spatial":
        source = Path(plan["ic"]["path"])
        if file_hash(source) != plan["ic"]["sha256"]:
            raise CaptureError("spatial IC changed after planning")
        shutil.copyfile(source, directory / "source_ic.npz")
        if file_hash(directory / "source_ic.npz") != plan["ic"]["sha256"]:
            raise CaptureError("spatial IC changed while copying")
        with np.load(directory / "source_ic.npz", allow_pickle=False) as z:
            ic = z["ic"]
        if array_hash(ic) != plan["ic"]["array_sha256"]:
            raise CaptureError("spatial IC array changed after planning")
    check_deadline(deadline)
    SS = SG.init_soup_gpu_batch([(plan["genome"], plan["original"]["seed"])],
                                L=plan["replay"]["L"], dtype=plan["replay"]["dtype"],
                                noise=plan["replay"]["noise"], ics=[ic])
    S = SS["worlds"][0]
    want_dtype = np.dtype("float32" if plan["replay"]["dtype"] == "f32" else "float64")
    if np.dtype(SS["_gpu"]["F"].dtype) != want_dtype or np.dtype(S["F"].dtype) != want_dtype:
        raise CaptureError("native state dtype does not equal explicitly resolved original dtype")
    if any(d.platform != "gpu" for d in SS["_gpu"]["F"].devices()):
        raise CaptureError("state is not on GPU")
    # One lane has no activator padding. Save the full actual starting fields.
    initial = np.asarray(SS["_gpu"]["F"])[0].copy()
    if ic is not None and not np.array_equal(initial, ic.astype(want_dtype)):
        raise CaptureError("native GPU initialization did not retain the exact spatial IC (after dtype cast)")
    np.savez_compressed(directory / "initial_state.npz", ic=initial)
    S["snap_t"] = list(plan["replay"]["snapshot_times"])
    n_checks = 0
    start = time.monotonic()
    for target in plan["replay"]["snapshot_times"]:
        check_deadline(deadline)
        statuses = SG.advance_gpu_batch(SS, target, overlap=False)
        rec = SG.snapshot_rec_gpu(S)
        if statuses != ["ok"] or rec["status"] != "ok" or not math.isclose(rec["T"], target, rel_tol=0.0, abs_tol=1e-9):
            raise CaptureError(f"native replay stopped early at {rec['T']}: {statuses}; intended T not captured")
        if target not in rec["snaps"]:
            raise CaptureError(f"native recorder missed exact snapshot {target}; no stale S['F'] fallback")
        frame = np.asarray(rec["snaps"][target], dtype=want_dtype)
        fresh_acts = np.asarray(SS["_gpu"]["F"][:, :S["na"]])[0]
        if not np.array_equal(frame, fresh_acts) or not np.isfinite(frame).all():
            raise CaptureError(f"snapshot {target} does not equal fresh native device activators")
        n_checks += 1
        progress({"name": plan["name"], "target": target, "intended_T": plan["replay"]["T"],
                  "native_snapshots_checked": n_checks, "wall_s": round(time.monotonic() - start, 3)})
    rec = SG.snapshot_rec_gpu(S)
    schedule = plan["replay"]["snapshot_times"]
    if sorted(rec["snaps"]) != schedule or S["snap_t"]:
        raise CaptureError("native snapshot schedule not exhausted exactly")
    rec_ts = np.asarray(rec["t"], dtype=np.float64)
    rec_ct = np.zeros(len(rec_ts), dtype=np.int64)
    for a in range(S["na"]):
        if len(rec["blobs"][a]) != len(rec_ts):
            raise CaptureError("native blob record length mismatch")
        rec_ct += np.asarray([len(bl) for bl in rec["blobs"][a]], dtype=np.int64)
    arrays = dict(frames=np.stack([rec["snaps"][t] for t in schedule]).astype(want_dtype),
                  ts=np.asarray(schedule, dtype=np.float64), rec_ts=rec_ts, rec_ct=rec_ct,
                  na=S["na"], status=rec["status"], T=plan["replay"]["T"],
                  seed=plan["original"]["seed"], genome=json.dumps(plan["genome"], sort_keys=True),
                  name=plan["replay"]["display_name"], capture_name=plan["name"],
                  cand=plan["original"]["cand"], island=str(plan["original"]["island"]),
                  L=plan["replay"]["L"], original_T_used=plan["original"]["T_used"],
                  original_backend=plan["original"]["backend"], replay_label=TRACE_LABEL,
                  metrics_origin="original_result_row; NOT recomputed", schema=SCHEMA,
                  interest=float(plan["row"]["interest"]) if plan["row"].get("interest") is not None else np.nan,
                  C9=float(plan["row"]["C9"]) if plan["row"].get("C9") is not None else np.nan)
    validation = validate_arrays(arrays, plan)
    check_deadline(deadline)
    np.savez_compressed(directory / "film.npz", **arrays)
    manifest = {"schema": SCHEMA, "status": "complete", "completed_utc": utc(),
                "request_sha256": plan["request_sha256"], "provenance": plan,
                "label": TRACE_LABEL, "exact_original_trace": False,
                "numerical_environment": get_environment(),
                "native_snapshot_device_checks": n_checks, "validation": validation,
                "initial_state": {"path": "initial_state.npz", "array_sha256": array_hash(initial),
                                  "shape": list(initial.shape), "dtype": str(initial.dtype),
                                  "origin": plan["ic"]["kind"],
                                  "is_original_trace_checkpoint": False},
                "wall_s": time.monotonic() - start,
                "artifacts": {p.name: {"sha256": file_hash(p), "bytes": p.stat().st_size}
                              for p in sorted(directory.iterdir()) if p.is_file()}}
    manifest["manifest_sha256"] = obj_hash(manifest)
    write_json(directory / "manifest.json", manifest)
    integrity_check(directory, plan)  # Read back from disk; no existence-only success.
    return manifest


def parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("selection", type=Path, help="explicit selection JSON; no automatic ranking")
    p.add_argument("output", type=Path, help="film/reports output root (do not use out/runs)")
    p.add_argument("--plan-only", action="store_true", help="validate selection, jobs and ICs; no JAX import or simulation")
    p.add_argument("--smoke", action="store_true", help="first selected item only, 50tu / three snapshots [0,25,50]")
    p.add_argument("--only", action="append", default=[], help="filter exact explicit selection name; repeatable")
    p.add_argument("--max-wall-seconds", type=float, default=900.0, help="soft budget at frame boundaries; external hard timeout REQUIRED")
    p.add_argument("--record-mode", choices=("host", "device"), default="host", help="default native host recorder (no prototype pools)")
    p.add_argument("--apply-mode", choices=("sync", "async"), default="sync", help="async opts into the existing native asyncapply prototype")
    p.add_argument("--source-pins", type=Path, help="EXPLICIT opt-in to exact reviewed 0.3.5 source hashes for replay only; default strict locks")
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    start = time.monotonic()
    output = args.output.expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    run_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S") + "-" + uuid.uuid4().hex[:8]
    report_dir = output / "reports" / run_id
    report_dir.mkdir(parents=True)
    report = {"schema": SCHEMA, "started_utc": utc(), "mode": "plan" if args.plan_only else "smoke" if args.smoke else "capture",
              "label": TRACE_LABEL, "selection_path": str(args.selection.expanduser().resolve()),
              "items": [], "status": "running", "exit_code": None}
    report_path = report_dir / "report.json"
    write_json(report_path, report)
    print(f"FILM_REPORT {report_path}", flush=True)
    failed = False
    try:
        budget = positive_number(args.max_wall_seconds, "max-wall-seconds")
        selection, selection_src = read_json(args.selection.expanduser().resolve())
        if not isinstance(selection, dict) or selection.get("schema") != SCHEMA:
            raise CaptureError(f"selection must be an object with schema={SCHEMA!r}")
        items = selection.get("items")
        if not isinstance(items, list) or not items:
            raise CaptureError("empty/missing items; no intended captures is NOT success")
        report["selection_source"] = selection_src
        write_json(report_dir / "selection.json", selection)
        source_pins = None
        if args.source_pins:
            source_pins, pin_source = read_json(args.source_pins.expanduser().resolve())
            validate_source_pins(source_pins)
            report["source_pins_file"] = pin_source
            write_json(report_dir / "source_pins.json", source_pins)
            # Read-only source verification, no JAX import. A pin mismatch fails
            # even in --plan-only, before any intended capture can start.
            import blobkit
            report["source_verification"] = source_lock_check(blobkit, source_pins)
        if args.only:
            found = {i.get("name") for i in items if isinstance(i, dict)}
            if not set(args.only).issubset(found):
                raise CaptureError("--only must name existing explicitly named selection items")
            items = [i for i in items if i.get("name") in args.only]
        if args.smoke:
            report["smoke_note"] = "Only the first explicit selected item is intended in smoke mode. This is NOT a full film."
            items = items[:1]
        ready, cache, names = [], {}, set()
        for index, item in enumerate(items):
            result = {"index": index, "name": item.get("name") if isinstance(item, dict) else None}
            report["items"].append(result)
            try:
                plan = resolve_item(item, args.selection.expanduser().resolve().parent, cache,
                                    smoke=args.smoke, record_mode=args.record_mode, apply_mode=args.apply_mode,
                                    source_pins=source_pins)
                result["name"] = plan["name"]
                if plan["name"] in names:
                    raise CaptureError("duplicate selection name; no output aliasing")
                names.add(plan["name"])
                result.update(status="planned", request_sha256=plan["request_sha256"], estimate=plan["estimate"])
                ready.append((plan, result))
            except Exception as exc:
                result.update(status="skipped_missing_ic" if isinstance(exc, MissingIC) else "failed_preflight",
                              error=f"{type(exc).__name__}: {exc}")
                failed = True
        write_json(report_dir / "plan.json", {"schema": SCHEMA, "selection_source": selection_src,
                                             "plans": [plan for plan, _ in ready]})
        write_json(report_path, report)
        if not args.plan_only:
            # One invocation per output root. flock auto-releases on timeout/kill.
            with (output / ".film_capture.lock").open("a") as lock:
                try:
                    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError:
                    raise CaptureError("another capture owns this output root") from None
                pending = []
                for plan, result in ready:
                    final = output / plan["replay"]["mode"] / plan["name"]
                    result["directory"] = str(final)
                    if final.exists():
                        try:
                            _, validation = integrity_check(final, plan)
                            result.update(status="verified_existing", validation=validation)
                            print(f"VERIFIED_EXISTING {final}", flush=True)
                        except Exception as exc:
                            result.update(status="failed_existing_integrity", error=f"{type(exc).__name__}: {exc}")
                            failed = True
                    else:
                        pending.append((plan, result, final))
                write_json(report_path, report)
                if pending:
                    check_deadline(start + budget)
                    with native_runtime(args.record_mode, args.apply_mode, source_pins) as (SG, get_env):
                        for plan, result, final in pending:
                            stage = final.parent / ("." + final.name + ".partial-" + uuid.uuid4().hex[:8])
                            result.update(status="running", partial_directory=str(stage))
                            write_json(report_path, report)
                            def progress(event):
                                result["progress"] = event
                                write_json(report_path, report)
                                print("FILM_PROGRESS " + json.dumps(event, sort_keys=True), flush=True)
                            try:
                                check_deadline(start + budget)
                                manifest = capture_one(plan, stage, SG, get_env, start + budget, progress)
                                # Completed artifact set is published by one atomic directory rename.
                                if final.exists():
                                    raise CaptureError("output appeared during capture; refusing replacement")
                                os.rename(stage, final)
                                result.update(status="complete", manifest_sha256=manifest["manifest_sha256"],
                                              validation=manifest["validation"], wall_s=manifest["wall_s"])
                                result.pop("partial_directory", None)
                                print(f"FILM_COMPLETE {final / 'film.npz'}", flush=True)
                            except Exception as exc:
                                failed = True
                                result.update(status="failed_budget" if isinstance(exc, BudgetExceeded) else "failed_capture",
                                              error=f"{type(exc).__name__}: {exc}")
                                if stage.is_dir():
                                    write_json(stage / "failure.json", result)
                            write_json(report_path, report)
        successful = sum(r.get("status") in (("planned",) if args.plan_only else ("complete", "verified_existing"))
                         for r in report["items"])
        if successful != len(items) or successful == 0:
            failed = True
        report["successful_items"] = successful
    except Exception as exc:
        report["error"] = f"{type(exc).__name__}: {exc}"
        for result in report["items"]:
            if result.get("status") in ("planned", "running"):
                result.update(status="not_captured", error=report["error"])
        failed = True
    report.update(status="failed" if failed else "complete", exit_code=1 if failed else 0,
                  finished_utc=utc(), wall_s=round(time.monotonic() - start, 3))
    write_json(report_path, report)
    print(("FILM_FAILED " if failed else "FILM_PLAN_VALID " if args.plan_only else "FILM_SELECTION_COMPLETE ")
          + str(report_path), flush=True)
    return report["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
