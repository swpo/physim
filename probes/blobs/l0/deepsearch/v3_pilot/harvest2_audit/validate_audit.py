#!/usr/bin/env python3
"""Independent stdlib checks on generated audit tables; no simulation/imports."""
import csv
import hashlib
import json
import math
from pathlib import Path

D = Path(__file__).resolve().parent
T = json.loads((D / "audit_tables.json").read_text())
M = json.loads((D / "source_manifest.json").read_text())
W = Path.home() / "v3work"
raw = {n: json.loads((W / f"ops/recovery_20260905/v3cont-{n}/settled/results.json").read_text()) for n in (1,2)}
checks = []


def check(label, condition):
    assert condition, label
    checks.append(label)


def read_csv(name):
    with (D / name).open() as f:
        return list(csv.DictReader(f))


obs = read_csv("observations.csv")
check("raw_row_count", len(obs) == 3606)
check("unambiguous_row_count", sum(r["primary_included"] == "True" for r in obs) == 3604)
check("unique_identity_keys", len({(r["island"],r["cand"],r["phase"],r["seed"]) for r in obs}) == 3605)
for row in obs:
    actual = raw[int(row["source_island"])][int(row["source_row_index"])]
    assert all(str(actual[k]) == row[k] for k in ("island","cand","phase","seed"))
    for k, target in (("interest", "interest_raw"), ("interest_v2", "interest_v2_preserved"), ("C9","C9")):
        assert (float(row[target]) if row[target] else None) == actual.get(k)
    for label, w in (("025",.25),("040",.40)):
        if actual.get("C9") is None or actual.get("interest_v2") is None:
            assert row[f"common_I{label}"] == ""
        else:
            score = (1-w)*actual["interest_v2"]+100*w*actual["C9"]
            assert float(row[f"common_I{label}"]) == score
            qualifies = actual["status"]=="ok" and actual["C9"]>=.4 and score>=60
            assert row[f"qualifies_{label}"] == str(qualifies)
check("every_observation_raw_values_identity_and_common_scores", True)
cs = read_csv("candidate_confirmations.csv")
check("one_unit_per_named_base", len(cs)==2099 and len({(r["island"],r["cand"]) for r in cs})==2099)
check("invalid_confirmations_not_attributed", sum(int(r["invalid_confirmation_rows"]) for r in cs)==11)
for label in ("025","040"):
    for r in cs:
        if r[f"robust_three_seeds_{label}"] == "True":
            assert r["valid_pair"] == "True" and r[f"screen_qualifies_{label}"] == "True"
            assert int(r["unique_assayed_seeds"]) == 3
            assert r["seed2_cand"] and r["seed3_cand"]
check("three_assay_joint_threshold_requires_valid_pair_and_three_seeds", True)
gs = [r for r in T["per_generation_screen"] if r["island"]=="both" and r["C9_mode"]=="all"]
check("per_generation_screen_n_sum", sum(r["n"] for r in gs)==2099)
check("per_generation_status_n_sums", all(r["n"]==r["status_ok"]+r["status_no_blobs"]+r["status_fail_g0a"] for r in gs))
check("baseline_rows_preserved", all(r["all_identical"] for r in T["integrity"]["baseline_preservation"]))
check("initial_wrong_model_reconstruction", sum(r["wrong_physical_model_n"] for r in T["reblend_initial_vs_surviving"] if r["stage"]=="initial_gen7_archive")==29)
check("initial_descriptor_mismatches", sum(r["different_descriptor_key_n"] for r in T["reblend_initial_vs_surviving"] if r["stage"]=="initial_gen7_archive")==365)
check("final_descriptor_mismatches", sum(r["different_descriptor_key_n"] for r in T["reblend_initial_vs_surviving"] if r["stage"]=="surviving_marked_final")==352)
check("archive_target_seed_unknown", all(r["target_seed_recorded_n"]==0 for r in T["reblend_initial_vs_surviving"]))
for path, meta in M["inputs"].items():
    p=Path(path)
    assert hashlib.sha256(p.read_bytes()).hexdigest() == meta["sha256"], path
check("all_small_data_code_and_pin_input_hashes_still_match_manifest", True)
interpretation_changes = []
for meta in M.get("audited_interpretations", []):
    current = hashlib.sha256(Path(meta["path"]).read_bytes()).hexdigest()
    if current != meta["audited_sha256"]:
        interpretation_changes.append(dict(path=meta["path"], audited_sha256=meta["audited_sha256"],
                                           current_sha256=current,
                                           meaning="Interpretation changed after review; old pin retained. Not a change to simulation data."))
films = json.loads((D / "film_selection_identity_checks.json").read_text())
check("six_current_film_keys_resolve", len(films)==6 and all(r["row_index_matches_key"] for r in films))
check("film_selection_no_known_invalid_parent_joins", all(not r["known_invalid_genome_confirmation"] for r in films))
result=dict(ok=True, checks=checks, check_count=len(checks), interpretation_drift=interpretation_changes,
            scope="Pure local JSON/CSV/hash validation; no simulation, metric execution, or input modification")
(D / "VALIDATION.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
