"""Static R6 first-pass handoff checks. No simulator or submitted code is run."""
from pathlib import Path
import hashlib
import json
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
SPEC = ROOT / "probes/blobs/l0/deepsearch/TRACKA_R6_PREDICTOR.md"

def strict_json(path):
    def invalid(value):
        raise ValueError(f"nonfinite JSON constant in {path}: {value}")
    return json.loads(path.read_text(), parse_constant=invalid)

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

checks = {}
json_paths = [p for p in HERE.rglob("*.json") if p.name != "first_pass_validation.json"]
parsed = {str(p.relative_to(ROOT)): strict_json(p) for p in json_paths}
checks["strict_json_all_finite"] = True

missing_links = []
markdown = sorted(HERE.rglob("*.md")) + [SPEC]
for path in markdown:
    text = path.read_text()
    for raw in re.findall(r"\]\(([^)]+)\)", text):
        raw = raw.split(' "', 1)[0]
        link = urlsplit(raw)
        if link.scheme or link.netloc or not link.path:
            continue
        target = (path.parent / unquote(link.path)).resolve()
        if not target.exists():
            missing_links.append([str(path.relative_to(ROOT)), raw])
checks["local_markdown_links_exist"] = not missing_links

hash_checks = []
large_sources_not_rehashed = []
for world in ("p4g2_044", "p6g8_033"):
    folder = HERE / "physics" / world
    evidence = strict_json(folder / "evidence.json")
    assert evidence["world"] == world
    sources = evidence.get("sources", evidence.get("provenance", []))
    for row in sources:
        p = ROOT / row["path"]
        assert p.exists(), p
        if p.stat().st_size > 10 * 1024 * 1024:
            large_sources_not_rehashed.append(str(p.relative_to(ROOT)))
            continue
        ok = p.stat().st_size == row["bytes"] and sha(p) == row["sha256"]
        hash_checks.append({"path": str(p.relative_to(ROOT)), "matches": ok})
    for row in evidence.get("artifacts", []):
        p = folder / row["path"]
        ok = p.exists() and p.stat().st_size == row["bytes"] and sha(p) == row["sha256"]
        hash_checks.append({"path": str(p.relative_to(ROOT)), "matches": ok})
checks["recorded_small_source_and_artifact_hashes_match"] = all(r["matches"] for r in hash_checks)

parent = strict_json(HERE / "parent_validation.json")
worker = strict_json(HERE / "runner/validation.json")
checks["worker_and_parent_31_tests_pass"] = all(
    d["status"] == "passed" and d["tests_run"] == 31 and not d["failures"]
    and not d["errors"] and not d["skipped"] for d in (parent, worker))
checks["native_scope_max_six_substeps"] = all(
    d["native"]["maximum_trajectory_substeps"] == 6
    and d["native"]["old_truth_parity"].startswith("not run") for d in (parent, worker))

text_paths = markdown + sorted(HERE.rglob("*.py")) + json_paths + [
    ROOT / "environments/physim/physim/blobround6.py",
    ROOT / "environments/physim/tools/test_blob_round6.py"]
credential_patterns = [r"sk-[A-Za-z0-9_-]{20,}", r"Bearer[ \t]+[A-Za-z0-9_.-]{20,}"]
credential_files = [str(p.relative_to(ROOT)) for p in text_paths
                    if any(re.search(pat, p.read_text()) for pat in credential_patterns)]
checks["no_credential_value_patterns"] = not credential_files
checks["no_legacy_truth_parity_promotion"] = "not a valid blanket" in SPEC.read_text()
checks["causal_pair_noise_gate_explicit"] = "Open causal-comparison gate" in SPEC.read_text()
checks["privileged_material_isolation_gate_explicit"] = "contamination" in SPEC.read_text()

report = {
    "status": "passed" if all(checks.values()) else "failed", "checks": checks,
    "json_files": len(json_paths), "markdown_files": len(markdown),
    "hash_checks": hash_checks, "missing_links": missing_links,
    "credential_files": credential_files,
    "large_sources_not_rehashed_by_parent": large_sources_not_rehashed,
    "limitations": [
        "Static consistency checks, not independent regeneration of all physics measurements.",
        "E1 full cache hashes were not supplied; E2 large cache hashes were not rehashed here.",
        "Evidence is finite, quantized, and largely single-realization; no universal law or noise floor is certified.",
        "No simulator, model, scorer, sandbox, or production integration is run by this validator."]}
(HERE / "first_pass_validation.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({"status": report["status"], "checks": checks,
                  "json_files": len(json_paths), "hashes_checked": len(hash_checks),
                  "missing_links": missing_links, "credential_files": credential_files}, indent=2))
raise SystemExit(0 if report["status"] == "passed" else 1)
