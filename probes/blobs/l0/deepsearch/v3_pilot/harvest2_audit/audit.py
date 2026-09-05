#!/usr/bin/env python3
"""Read-only, local audit of the settled v3 continuation. Stdlib only.

Run from the physim root:
  .venv/bin/python probes/blobs/l0/deepsearch/v3_pilot/harvest2_audit/audit.py

No network, simulation, archive extraction, input rewriting, or file deletion.
The baseline snapshots are references, not additional observations.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median

WEIGHTS = (("025", 0.25), ("040", 0.40))
CORE = ("acts", "chans", "W", "K", "bilin")
PHASES = ("screen", "seed2", "seed3", "c9fill")
COHORTS = {
    "baseline_g1_7": set(range(1, 8)),
    "transition_g8": {8},
    "late_g9_12": set(range(9, 13)),
    "continuation_g8_12": set(range(8, 13)),
    "all_g1_12": set(range(1, 13)),
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False)


def rowkey(row):
    return tuple(row[k] for k in ("island", "cand", "phase", "seed"))


def keydict(key):
    return dict(zip(("island", "cand", "phase", "seed"), key))


def core_model(genome):
    if not genome:
        return None
    return {k: genome.get(k, [] if k == "bilin" else None) for k in CORE}


def model_equal(a, b):
    return core_model(a.get("genome")) == core_model(b.get("genome"))


def physical_differences(a, b):
    """Exact physical-model differences, excluding id/provenance/tag metadata."""
    ga, gb = core_model(a.get("genome")), core_model(b.get("genome"))
    samples, n_diffs = [], 0

    def walk(x, y, path):
        nonlocal n_diffs
        if x == y:
            return
        if isinstance(x, dict) and isinstance(y, dict):
            for key in sorted(set(x) | set(y)):
                walk(x.get(key), y.get(key), f"{path}.{key}" if path else key)
        elif isinstance(x, list) and isinstance(y, list):
            for i in range(max(len(x), len(y))):
                walk(x[i] if i < len(x) else None, y[i] if i < len(y) else None, f"{path}[{i}]")
        else:
            n_diffs += 1
            if len(samples) < 5:
                samples.append(dict(path=path, screen_value=x, compared_value=y))
    walk(ga, gb, "")
    return dict(differing_core_fields=[k for k in CORE if ga.get(k) != gb.get(k)],
                differing_leaf_count=n_diffs, first_five_differences=samples,
                screen_core_sha256=hashlib.sha256(canonical(ga).encode()).hexdigest(),
                compared_core_sha256=hashlib.sha256(canonical(gb).encode()).hexdigest())


def mode(row):
    if row.get("C9") is None:
        return "missing"
    if row.get("c9_partial") is True:
        return "partial"
    if row.get("c9_partial") is False:
        return "full"
    return "unknown"


def common(row, weight):
    c9, iv2 = row.get("C9"), row.get("interest_v2")
    if c9 is None or iv2 is None:
        return None
    return (1.0 - weight) * iv2 + weight * 100.0 * c9


def qualifying(row, weight):
    score = common(row, weight)
    return bool(row.get("status") == "ok" and row.get("C9", -1) >= 0.4
                and score is not None and score >= 60.0)


def rate(n, d):
    return n / d if d else None


def safe_mean(values):
    return mean(values) if values else None


def safe_median(values):
    return median(values) if values else None


def safe_max(values):
    return max(values) if values else None


def bucket(row):
    if row["phase"] == "c9fill":
        return "c9_backfill_import"
    if row["phase"] == "screen" and row["gen"] == 0:
        return "atlas_gen0_import"
    if row["phase"] == "screen":
        return "creative_screen"
    if row["phase"] in ("seed2", "seed3"):
        return "selected_confirmation"
    return "other"


def stat_summary(rows):
    c9s = [r["C9"] for r in rows if r.get("C9") is not None]
    i2 = [r["interest_v2"] for r in rows if r.get("interest_v2") is not None]
    statuses = Counter(r["status"] for r in rows)
    modes = Counter(mode(r) for r in rows)
    result = dict(n=len(rows), status_ok=statuses["ok"],
                  status_no_blobs=statuses["no_blobs"], status_fail_g0a=statuses["fail_g0a"],
                  c9_measured_n=len(c9s), c9_partial_n=modes["partial"],
                  c9_full_n=modes["full"], c9_missing_n=modes["missing"],
                  c9_mean=safe_mean(c9s), c9_median=safe_median(c9s), c9_max=safe_max(c9s),
                  preserved_i2_mean=safe_mean(i2), preserved_i2_median=safe_median(i2),
                  descriptor_bins_observed=len({r["cell"] for r in rows if r.get("cell")}),
                  unique_ghashes=len({r["ghash"] for r in rows if r.get("ghash")}),
                  strict_economy_class_n=sum(r.get("spatial_class") == "economy" for r in rows))
    for label, w in WEIGHTS:
        scores = [common(r, w) for r in rows if common(r, w) is not None]
        qs = [r for r in rows if qualifying(r, w)]
        result.update({f"common_I{label}_mean": safe_mean(scores),
                       f"common_I{label}_median": safe_median(scores),
                       f"common_I{label}_max": safe_max(scores),
                       f"qualifying_{label}_n": len(qs),
                       f"qualifying_{label}_per_all_n": rate(len(qs), len(rows)),
                       f"qualifying_{label}_descriptor_bins": len({r["cell"] for r in qs if r.get("cell")}),
                       f"qualifying_{label}_strict_economy_class_n": sum(r.get("spatial_class") == "economy" for r in qs)})
    return result


def write_csv(path, rows):
    if not rows:
        path.write_text("")
        return
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: canonical(v) if isinstance(v, (list, dict, tuple)) else v
                             for k, v in row.items()})


def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, allow_nan=False) + "\n")


def historical_base(cand):
    # Reproduce the OLD archival bug ONLY in the diagnostic. Never use for dedup
    # or base-candidate confirmation attribution.
    return cand.split("_s2")[0].split("_s3")[0].split("_c9")[0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path, default=Path.home() / "v3work")
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    work, out = args.work.expanduser().resolve(), args.out.expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    repo = next(p for p in Path(__file__).resolve().parents if (p / "probes/blobs").is_dir())
    pilot = repo / "probes/blobs/l0/deepsearch/v3_pilot"
    inputs = {}

    def read_json(path):
        inputs[str(path)] = dict(bytes=path.stat().st_size, sha256=sha256(path))
        return json.loads(path.read_text())

    final, old, configs, states, archives, old_archives, donors, verified = {}, {}, {}, {}, {}, {}, {}, {}
    critical_checks, baseline_checks, config_note_checks = [], [], []
    job_index = defaultdict(list)
    job_stats = Counter()
    raw = []
    source_index = {}
    for island in (1, 2):
        settled = work / f"ops/recovery_20260905/v3cont-{island}/settled"
        snap = work / f"harvest/isl{island}_snap/out"
        final[island] = read_json(settled / "results.json")
        old[island] = read_json(snap / "results.json")
        configs[island] = read_json(settled / "island_config.json")
        states[island] = read_json(settled / "state.json")
        archives[island] = read_json(settled / "archive.json")
        old_archives[island] = read_json(snap / "archive.json")
        donors[island] = read_json(snap / "archive_seed.json")
        settled_marker = read_json(settled / "CONFIRM12_SETTLED.json")
        verified[island] = read_json(work / f"isl{island}_final2.tgz.verified.json")
        assert states[island]["gen"] == settled_marker["gen"] == 12
        assert len(final[island]) == settled_marker["rows"]
        for name in ("results.json", "archive.json", "state.json", "island_config.json", "driver.log"):
            path = settled / name
            digest = sha256(path)
            inputs[str(path)] = dict(bytes=path.stat().st_size, sha256=digest)
            member = f"isl{island}/" + (name if name == "island_config.json" else "out/" + name)
            expected = verified[island]["critical_sha256"][member]
            assert digest == expected, (path, digest, expected)
            critical_checks.append(dict(island=island, path=str(path), archive_member=member,
                                        sha256=digest, verified_record_sha256=expected, match=True))
        final_by_key = defaultdict(list)
        for index, row in enumerate(final[island]):
            assert row["island"] == island
            final_by_key[rowkey(row)].append(row)
            source_index[id(row)] = dict(source_island=island, source_row_index=index)
            raw.append(row)
        same = sum(any(r == x for x in final_by_key[rowkey(r)]) for r in old[island])
        baseline_checks.append(dict(island=island, baseline_rows=len(old[island]),
                                    identical_final_rows=same, all_identical=same == len(old[island])))
        assert same == len(old[island])
        for path in sorted((snap / "jobs").glob("*.json")):
            if not (path.name.startswith(("g", "s2g", "s3g")) and "_w" in path.name):
                continue
            for job in read_json(path):
                phase = job.get("kind", "screen")
                seed = job.get("seed", configs[island]["seed"])
                job_index[(island, job["cand"], phase, seed)].append((str(path), job))
        config_note_checks.append(dict(island=island, mix=configs[island]["mix"],
                                       merge_mix=configs[island]["merge_mix"],
                                       continuation_note=configs[island].get("_continuation"),
                                       midcourse_note=configs[island].get("_midcourse")))

    # Final observations only. Baseline rows are not appended again.
    grouped = defaultdict(list)
    for row in raw:
        grouped[rowkey(row)].append(row)
    primary, conflicts, duplicate_groups = [], [], []
    excluded_ids = set()
    for key, variants in grouped.items():
        payloads = {canonical(r) for r in variants}
        if len(payloads) == 1:
            primary.append(variants[0])
            if len(variants) > 1:
                duplicate_groups.append(dict(key=keydict(key), repeated_rows=len(variants)))
        else:
            excluded_ids.update(id(r) for r in variants)
            changed = sorted(k for k in set().union(*(r.keys() for r in variants))
                             if len({canonical(r.get(k)) for r in variants}) > 1)
            conflicts.append(dict(key=keydict(key), n_rows=len(variants), changed_fields=changed,
                                  physical_differences=physical_differences(variants[0], variants[1]),
                                  film_path_ambiguity="Both rows declare the same cand-based NPZ path. File content or overwrite timing is not inferred from row timestamps.",
                                  variants=[dict(**source_index[id(r)], ghash=r.get("ghash"),
                                                 core_model_sha256=hashlib.sha256(canonical(core_model(r.get("genome"))).encode()).hexdigest(),
                                                 na=r.get("na"), nc=r.get("nc"),
                                                 interest_raw=r.get("interest"), interest_v2=r.get("interest_v2"),
                                                 C9=r.get("C9"), cell=r.get("cell"), npz=r.get("npz"),
                                                 genome_provenance=(r.get("genome") or {}).get("provenance"),
                                                 timestamp=r.get("ts")) for r in variants]))
    primary.sort(key=lambda r: (r["island"], source_index[id(r)]["source_row_index"]))
    assert len(raw) == 3606 and len(primary) == 3604 and len(conflicts) == 1

    screen_index = defaultdict(list)
    for row in primary:
        if row["phase"] == "screen":
            screen_index[(row["island"], row["cand"])].append(row)
    assert all(len(v) == 1 for v in screen_index.values())
    creative = [r for r in primary if bucket(r) == "creative_screen"]
    confirms = [r for r in primary if bucket(r) == "selected_confirmation"]
    valid_confirms, declared_confirms = defaultdict(list), defaultdict(list)
    joins, join_anomalies, confirm_origins = {}, [], []
    for row in confirms:
        parents = row.get("parents") or []
        matches = screen_index.get((row["island"], parents[0]), []) if len(parents) == 1 else []
        if len(parents) == 1:
            declared_confirms[(row["island"], parents[0])].append(row)
        valid = len(matches) == 1 and row.get("ghash") == matches[0].get("ghash") and model_equal(row, matches[0])
        join = dict(key=keydict(rowkey(row)), declared_parents=parents, valid_same_genome_base=valid,
                    unique_screen_parent=len(matches) == 1)
        if matches:
            screen = matches[0]
            join.update(screen_key=keydict(rowkey(screen)), screen_ghash=screen.get("ghash"),
                        confirmation_ghash=row.get("ghash"), screen_operator=screen.get("op"),
                        model_fields_equal=model_equal(row, screen))
        jobs = job_index.get(rowkey(row), [])
        join["job_evidence"] = [p for p, j in jobs]
        if jobs:
            join["result_genome_equals_job"] = len(jobs) == 1 and jobs[0][1].get("genome") == row.get("genome")
        if valid:
            base_key = (row["island"], parents[0])
            valid_confirms[base_key].append(row)
            join["actual_origin_op"] = matches[0]["op"]
            join["origin_evidence"] = "explicit_single_parent_and_matching_ghash_and_model"
        else:
            donor_matches = [dict(descriptor_key=k, cand=c.get("cand"), ghash=c.get("ghash"),
                                  op=c.get("op")) for k, c in donors[row["island"]].items()
                             if c.get("ghash") == row.get("ghash") and model_equal(c, row)]
            join["matching_donor_archive_entries"] = donor_matches
            provenance = (row.get("genome") or {}).get("provenance", {})
            join["actual_origin_op"] = provenance.get("op")
            join["origin_evidence"] = "actual_job_genome_provenance_not_named_screen"
            join["genome_provenance"] = provenance
            join["physical_differences_from_named_screen"] = physical_differences(matches[0], row) if matches else None
            join_anomalies.append(join)
        joins[rowkey(row)] = join
        confirm_origins.append(dict(island=row["island"], cand=row["cand"], phase=row["phase"],
                                    seed=row["seed"], gen=row["gen"], declared_parent=parents[0] if len(parents) == 1 else None,
                                    actual_origin_op=join.get("actual_origin_op"),
                                    valid_same_genome_base=valid, evidence=join["origin_evidence"]))
    assert len(join_anomalies) == 11
    assert all(j.get("matching_donor_archive_entries") for j in join_anomalies)
    assert all(j.get("result_genome_equals_job") for j in join_anomalies)
    for row in primary:
        if row["gen"] not in range(1, 8):
            continue
        js = job_index.get(rowkey(row), [])
        if len(js) != 1:
            job_stats["no_unique_job"] += 1
        elif js[0][1].get("genome") != row.get("genome"):
            job_stats["model_disagrees"] += 1
        elif js[0][1].get("parents") != row.get("parents") or js[0][1].get("op") != row.get("op"):
            job_stats["parents_or_op_disagree"] += 1
        else:
            job_stats["job_result_genome_parents_op_equal"] += 1
    assert job_stats == {"job_result_genome_parents_op_equal": 2318}

    # Row-level compact table preserves the raw score. Even quarantined variants
    # remain visible, but primary_included=False keeps them out of main counts.
    observations = []
    retained_ids = {id(r) for r in primary}
    for row in raw:
        join = joins.get(rowkey(row), {})
        obs = dict(**source_index[id(row)], **keydict(rowkey(row)), gen=row["gen"],
                   bucket=bucket(row), op=row["op"], parents=row.get("parents"),
                   ghash=row.get("ghash"), status=row["status"],
                   primary_included=id(row) in retained_ids, C9_mode=mode(row),
                   C9=row.get("C9"), interest_raw=row.get("interest"),
                   interest_v2_preserved=row.get("interest_v2"),
                   common_I025=common(row, 0.25), common_I040=common(row, 0.40),
                   qualifies_025=qualifying(row, 0.25), qualifies_040=qualifying(row, 0.40),
                   descriptor_bin=row.get("cell"), spatial_class=row.get("spatial_class"),
                   valid_same_genome_confirmation=join.get("valid_same_genome_base"),
                   actual_origin_op=join.get("actual_origin_op", row.get("op")),
                   ic_merge=row.get("ic_merge", False), T_used=row.get("T_used"))
        observations.append(obs)
    write_csv(out / "observations.csv", observations)

    # Per-generation screens only, including unsuccessful lanes in denominators.
    per_gen = []
    for island in (1, 2, "both"):
        for gen in range(1, 13):
            rows = [r for r in creative if r["gen"] == gen and (island == "both" or r["island"] == island)]
            for metric_mode in ("all", "partial", "full", "missing"):
                rr = rows if metric_mode == "all" else [r for r in rows if mode(r) == metric_mode]
                per_gen.append(dict(island=island, gen=gen, C9_mode=metric_mode, **stat_summary(rr)))
    write_csv(out / "screen_by_generation.csv", per_gen)
    emitted = []
    for island in (1, 2, "both"):
        for gen in range(1, 13):
            rows = [r for r in creative if r["gen"] == gen and (island == "both" or r["island"] == island)]
            counts = Counter(r["op"] for r in rows)
            emitted.append(dict(island=island, gen=gen, n=len(rows), **{op: counts[op] for op in sorted({r["op"] for r in creative})}))
    write_csv(out / "operator_emitted_by_generation.csv", emitted)

    # Common-weight comparisons, with screen / confirmations / backfill separate.
    phase_summary = []
    for island in (1, 2, "both"):
        for cohort, generations in COHORTS.items():
            for phase in ("screen", "seed2", "seed3", "selected_confirmations_pooled", "verified_same_genome_confirmations"):
                rows = [r for r in primary if r["gen"] in generations
                        and (r["phase"] == phase
                             or (phase == "selected_confirmations_pooled" and r["phase"] in ("seed2", "seed3"))
                             or (phase == "verified_same_genome_confirmations" and r["phase"] in ("seed2", "seed3") and joins[rowkey(r)]["valid_same_genome_base"]))
                        and (island == "both" or r["island"] == island)]
                for metric_mode in ("all", "partial", "full"):
                    rr = rows if metric_mode == "all" else [r for r in rows if mode(r) == metric_mode]
                    phase_summary.append(dict(island=island, cohort=cohort, phase=phase,
                                              C9_mode=metric_mode, **stat_summary(rr)))
        for b in ("atlas_gen0_import", "c9_backfill_import"):
            rows = [r for r in primary if bucket(r) == b and (island == "both" or r["island"] == island)]
            for metric_mode in ("all", "partial", "full"):
                rr = rows if metric_mode == "all" else [r for r in rows if mode(r) == metric_mode]
                phase_summary.append(dict(island=island, cohort=b, phase="screen" if b == "atlas_gen0_import" else "c9fill",
                                          C9_mode=metric_mode, **stat_summary(rr)))
    write_csv(out / "cohort_phase_summary.csv", phase_summary)

    # Candidate-level rates: a base gets at most one success per definition.
    # "robust" here means all THREE assayed seeds qualify, not a statistical
    # claim about unseen seeds, and not same-IC reproduction for SIC operators.
    candidate_rows = []
    for screen in creative:
        key = (screen["island"], screen["cand"])
        linked = valid_confirms[key]
        declared = declared_confirms[key]
        byphase = {r["phase"]: r for r in linked}
        assert len(byphase) == len(linked)
        all_three = [screen] + linked
        complete = set(byphase) == {"seed2", "seed3"} and len({r["seed"] for r in all_three}) == 3
        cr = dict(island=screen["island"], cand=screen["cand"], gen=screen["gen"], op=screen["op"],
                  parents=screen.get("parents"), ghash=screen.get("ghash"),
                  screen_status=screen["status"], screen_C9_mode=mode(screen), screen_C9=screen.get("C9"),
                  screen_interest_raw=screen.get("interest"), screen_interest_v2=screen.get("interest_v2"),
                  screen_descriptor_bin=screen.get("cell"),
                  selected_declared=bool(declared), selected_valid=bool(linked),
                  declared_pair={r["phase"] for r in declared} == {"seed2", "seed3"},
                  valid_pair=complete, invalid_confirmation_rows=len(declared) - len(linked),
                  unique_assayed_seeds=len({r["seed"] for r in all_three}),
                  three_seed_C9_min=min(r.get("C9", -1) for r in all_three) if complete and all(r.get("C9") is not None for r in all_three) else None)
        for phase in ("seed2", "seed3"):
            row = byphase.get(phase, {})
            cr.update({f"{phase}_cand": row.get("cand"), f"{phase}_status": row.get("status"),
                       f"{phase}_C9": row.get("C9"), f"{phase}_interest_raw": row.get("interest"),
                       f"{phase}_interest_v2": row.get("interest_v2")})
        for label, w in WEIGHTS:
            sq = qualifying(screen, w)
            cq = any(qualifying(r, w) for r in linked)
            robust = complete and sq and all(qualifying(r, w) for r in linked)
            cr.update({f"screen_qualifies_{label}": sq,
                       f"screen_common_I{label}": common(screen, w),
                       f"any_seed_qualifies_{label}": sq or cq,
                       f"any_confirmed_{label}": cq,
                       f"screen_plus_any_confirmed_{label}": sq and cq,
                       f"robust_three_seeds_{label}": robust,
                       f"robust_partial_only_{label}": robust and all(mode(r) == "partial" for r in all_three),
                       f"three_seed_common_I{label}_min": min(common(r, w) for r in all_three) if complete and all(common(r, w) is not None for r in all_three) else None})
        candidate_rows.append(cr)
    write_csv(out / "candidate_confirmations.csv", candidate_rows)

    operator_rates = []
    for island in (1, 2, "both"):
        for cohort, generations in COHORTS.items():
            pool = [c for c in candidate_rows if c["gen"] in generations and (island == "both" or c["island"] == island)]
            for op in ["ALL"] + sorted({c["op"] for c in pool}):
                cs = pool if op == "ALL" else [c for c in pool if c["op"] == op]
                n, selected, paired = len(cs), sum(c["selected_valid"] for c in cs), sum(c["valid_pair"] for c in cs)
                for label, w in WEIGHTS:
                    sn = sum(c[f"screen_qualifies_{label}"] for c in cs)
                    an = sum(c[f"any_confirmed_{label}"] for c in cs)
                    rn = sum(c[f"robust_three_seeds_{label}"] for c in cs)
                    rp = sum(c[f"robust_partial_only_{label}"] for c in cs)
                    operator_rates.append(dict(island=island, cohort=cohort, op=op, W9=w,
                        base_candidates_n=n, unique_ghashes=len({c["ghash"] for c in cs}),
                        screen_status_ok_n=sum(c["screen_status"] == "ok" for c in cs),
                        screen_status_ok_rate=rate(sum(c["screen_status"] == "ok" for c in cs), n),
                        screen_partial_n=sum(c["screen_C9_mode"] == "partial" for c in cs),
                        screen_full_n=sum(c["screen_C9_mode"] == "full" for c in cs),
                        screen_missing_C9_n=sum(c["screen_C9_mode"] == "missing" for c in cs),
                        screen_success_n=sn, screen_success_rate=rate(sn, n),
                        screen_partial_success_n=sum(c[f"screen_qualifies_{label}"] and c["screen_C9_mode"] == "partial" for c in cs),
                        screen_full_success_n=sum(c[f"screen_qualifies_{label}"] and c["screen_C9_mode"] == "full" for c in cs),
                        selected_declared_n=sum(c["selected_declared"] for c in cs), selected_valid_n=selected,
                        complete_valid_pairs_n=paired, declared_pairs_n=sum(c["declared_pair"] for c in cs),
                        invalid_confirmation_rows=sum(c["invalid_confirmation_rows"] for c in cs),
                        any_seed_success_n=sum(c[f"any_seed_qualifies_{label}"] for c in cs),
                        any_confirmed_n=an, any_confirmed_per_all_bases=rate(an, n),
                        any_confirmed_per_selected=rate(an, selected),
                        screen_plus_any_confirmed_n=sum(c[f"screen_plus_any_confirmed_{label}"] for c in cs),
                        robust_three_seeds_n=rn, robust_per_all_bases=rate(rn, n),
                        robust_per_complete_valid_pairs=rate(rn, paired),
                        robust_partial_only_n=rp, robust_partial_per_all_bases=rate(rp, n)))
    write_csv(out / "operator_rates.csv", operator_rates)
    write_csv(out / "confirmation_origins.csv", confirm_origins)

    # Historical reproduction: rows and bins are not candidate hit probabilities.
    reproduction = []
    for label, w in WEIGHTS:
        for island in (1, 2, "both"):
            rr = [r for r in primary if r["gen"] in range(1, 8) and r["phase"] in ("screen", "seed2", "seed3")
                  and (island == "both" or r["island"] == island)]
            qs = [r for r in rr if qualifying(r, w)]
            reproduction.append(dict(island=island, W9=w, all_phase_qualifying_rows=len(qs),
                all_phase_qualifying_descriptor_bins=len({r["cell"] for r in qs}),
                qualifying_invalid_genome_confirm_rows=sum(r["phase"] in ("seed2", "seed3") and not joins[rowkey(r)]["valid_same_genome_base"] for r in qs),
                qualifying_strict_economy_class_rows=sum(r.get("spatial_class") == "economy" for r in qs)))

    # Distinct observed descriptor bins and newly observed bins. Archive occupancy
    # is deliberately not substituted for observation-level evidence.
    breadth = []
    for label, w in WEIGHTS:
        for metric_mode in ("all", "partial", "full"):
            for phases_name, phases in (("screen_only", {"screen"}),
                                        ("screen_plus_selected_assay_runs", {"screen", "seed2", "seed3"}),
                                        ("screen_plus_verified_same_genome_confirmations", {"screen", "seed2", "seed3"})):
                rr = [r for r in primary if r["gen"] in range(1, 13) and r["phase"] in phases
                      and (metric_mode == "all" or mode(r) == metric_mode) and qualifying(r, w)
                      and (phases_name != "screen_plus_verified_same_genome_confirmations" or r["phase"] == "screen" or joins[rowkey(r)]["valid_same_genome_base"])]
                old_bins = {r["cell"] for r in rr if r["gen"] <= 7}
                new_bins = {r["cell"] for r in rr if r["gen"] >= 8}
                breadth.append(dict(W9=w, C9_mode=metric_mode, scope=phases_name,
                                    baseline_descriptor_bins=len(old_bins), continuation_descriptor_bins=len(new_bins),
                                    union_descriptor_bins=len(old_bins | new_bins),
                                    newly_observed_continuation_descriptor_bins=len(new_bins - old_bins),
                                    new_bin_keys=sorted(new_bins - old_bins)))

    # Reproduce the historical reblend join (including raw conflicting imports)
    # for diagnosis, not as an endorsement or a rewrite of the archives.
    archive_diagnostics, archive_summary = [], []
    for island in (1, 2):
        history_rows = [r for r in final[island] if r["gen"] <= 7 or r["phase"] == "c9fill"]
        best, best40, bybase = {}, {}, defaultdict(list)
        for r in history_rows:
            if r.get("status") != "ok" or r.get("C9") is None:
                continue
            base = historical_base(r["cand"])
            bybase[base].append(r)
            if base not in best or (r.get("interest") or 0) > (best[base].get("interest") or 0):
                best[base] = r
            if base not in best40 or common(r, 0.4) > common(best40[base], 0.4):
                best40[base] = r
        ds = []
        for key, entry in archives[island].items():
            marked = entry.get("_reblended_w9") is not None
            selected = best.get(entry["cand"]) or best.get(str(entry["cand"]).split("_s2")[0].split("_s3")[0])
            normalized_best = best40.get(entry["cand"]) or best40.get(str(entry["cand"]).split("_s2")[0].split("_s3")[0])
            d = dict(archive_owner_island=island, descriptor_key=key, key_axes=len(key.split("|")),
                     archive_cand=entry.get("cand"), archive_gen=entry.get("gen"),
                     archive_recorded_origin_island=entry.get("island"), archive_ghash=entry.get("ghash"),
                     archive_interest_raw=entry.get("interest"), archive_C9=entry.get("C9"),
                     archive_C9_mode=mode(entry), reblend_marker=entry.get("_reblended_w9"),
                     native_seed2_ok=entry.get("seed2_ok"), native_seed3_ok=entry.get("seed3_ok"),
                     reblend_source_found=selected is not None)
            if marked and selected:
                d.update(selected_cand=selected["cand"], selected_phase=selected["phase"], selected_seed=selected["seed"],
                         selected_ghash=selected.get("ghash"), selected_descriptor=selected.get("cell"),
                         selected_interest_raw=selected.get("interest"), selected_C9=selected.get("C9"),
                         score_matches_historical_reblend=math.isclose(entry["interest"], common(selected, 0.4), abs_tol=1e-9),
                         C9_matches_historical_reblend=entry.get("C9") == selected.get("C9"),
                         same_ghash=entry.get("ghash") == selected.get("ghash"), same_model=model_equal(entry, selected),
                         same_descriptor=key == selected.get("cell"), same_T_used=entry.get("T_used") == selected.get("T_used"),
                         different_best_row_under_common_040=rowkey(selected) != rowkey(normalized_best),
                         common040_best_cand=normalized_best["cand"], common040_best_phase=normalized_best["phase"])
            ds.append(d)
        archive_diagnostics.extend(ds)
        marked_ds = [d for d in ds if d["reblend_marker"] is not None]
        archive_summary.append(dict(island=island, final_entries=len(ds), baseline_entries=len(old_archives[island]),
            key_axes_counts=dict(Counter(d["key_axes"] for d in ds)),
            C9_mode_counts=dict(Counter(d["archive_C9_mode"] for d in ds)),
            native_seed2_ok_n=sum(bool(d["native_seed2_ok"]) for d in ds), native_seed3_ok_n=sum(bool(d["native_seed3_ok"]) for d in ds),
            baseline_native_seed3_ok_n=sum(bool(c.get("seed3_ok")) for c in old_archives[island].values()),
            marked_reblended_n=len(marked_ds),
            reproduced_reblend_score_n=sum(d.get("score_matches_historical_reblend", False) for d in marked_ds),
            reproduced_reblend_C9_n=sum(d.get("C9_matches_historical_reblend", False) for d in marked_ds),
            marked_ghash_mismatch_n=sum(not d.get("same_ghash", False) for d in marked_ds),
            marked_model_mismatch_n=sum(not d.get("same_model", False) for d in marked_ds),
            marked_descriptor_mismatch_n=sum(not d.get("same_descriptor", False) for d in marked_ds),
            marked_descriptor_mismatch_7axis_n=sum(d["key_axes"] == 7 and not d.get("same_descriptor", False) for d in marked_ds),
            marked_different_best_at_040_n=sum(d.get("different_best_row_under_common_040", False) for d in marked_ds),
            marked_selected_phases=dict(Counter(d.get("selected_phase") for d in marked_ds))))
    write_csv(out / "archive_reblend_diagnostics.csv", archive_diagnostics)

    # Initial contamination versus surviving marked entries. The original gen7
    # archive is the pre-reblend target; only gen<=7 / c9fill rows are eligible.
    # Stored entries generally omit seed, so do not invent a target-seed match.
    reblend_stages, reblend_stage_summary = [], []
    for island in (1, 2):
        eligible = [r for r in final[island] if (r["gen"] <= 7 or r["phase"] == "c9fill")
                    and r.get("status") == "ok" and r.get("C9") is not None]
        best = {}
        for r in eligible:
            b = historical_base(r["cand"])
            if b not in best or (r.get("interest") or 0) > (best[b].get("interest") or 0):
                best[b] = r
        for stage, target in (("initial_gen7_archive", old_archives[island]),
                              ("surviving_marked_final", archives[island])):
            ss = []
            for key, entry in target.items():
                if stage == "surviving_marked_final" and entry.get("_reblended_w9") != 0.4:
                    continue
                r = best.get(entry["cand"]) or best.get(str(entry["cand"]).split("_s2")[0].split("_s3")[0])
                refs = [s for s in screen_index.get((island, entry["cand"]), [])
                        if s.get("ghash") == entry.get("ghash") and model_equal(s, entry)]
                ref = refs[0] if len(refs) == 1 else None
                d = dict(island=island, stage=stage, target_descriptor_key=key,
                         target_cand=entry.get("cand"), target_gen=entry.get("gen"),
                         target_ghash=entry.get("ghash"), target_seed_recorded=entry.get("seed"),
                         source_found=r is not None, same_model_screen_reference=ref is not None,
                         reference_screen_seed=ref.get("seed") if ref else None)
                if r:
                    d.update(selected_cand=r["cand"], selected_phase=r["phase"], selected_seed=r["seed"],
                             selected_ghash=r.get("ghash"), selected_descriptor_key=r.get("cell"),
                             selected_interest_raw=r.get("interest"), selected_C9=r.get("C9"),
                             reblended_I040=common(r, 0.4),
                             same_physical_model=model_equal(entry, r), same_ghash=entry.get("ghash") == r.get("ghash"),
                             same_descriptor_key=key == r.get("cell"),
                             seed_differs_from_recorded_target=(entry["seed"] != r["seed"]) if entry.get("seed") is not None else None,
                             selected_seed_differs_from_screen_reference=(ref["seed"] != r["seed"]) if ref else None)
                ss.append(d)
            reblend_stages.extend(ss)
            reblend_stage_summary.append(dict(island=island, stage=stage, entries=len(ss),
                source_found_n=sum(d["source_found"] for d in ss),
                wrong_physical_model_n=sum(d.get("same_physical_model") is False for d in ss),
                different_descriptor_key_n=sum(d.get("same_descriptor_key") is False for d in ss),
                target_seed_recorded_n=sum(d["target_seed_recorded"] is not None for d in ss),
                seed_differs_from_recorded_target_n=sum(d.get("seed_differs_from_recorded_target") is True for d in ss),
                exact_model_screen_reference_n=sum(d["same_model_screen_reference"] for d in ss),
                selected_seed_differs_from_screen_reference_n=sum(d.get("selected_seed_differs_from_screen_reference") is True for d in ss),
                selected_source_phases=dict(Counter(d.get("selected_phase") for d in ss))))
    write_csv(out / "reblend_initial_vs_surviving.csv", reblend_stages)

    # Actual maxima: valid linked selected confirmations only; screen maximum is
    # reported independently. The C9 maximum need not pass the joint threshold.
    maxima, ranked = [], []
    for island in (1, 2, "both"):
        for cohort, generations in COHORTS.items():
            for phase in ("screen", "valid_selected_confirmations"):
                rr = [r for r in primary if r["gen"] in generations and (island == "both" or r["island"] == island)
                      and ((phase == "screen" and r["phase"] == "screen")
                           or (phase == "valid_selected_confirmations" and r["phase"] in ("seed2", "seed3") and joins[rowkey(r)]["valid_same_genome_base"]))
                      and r.get("status") == "ok" and r.get("C9") is not None]
                for metric, fun in (("C9", lambda r: r["C9"]), ("common_I025", lambda r: common(r, 0.25)),
                                    ("common_I040", lambda r: common(r, 0.40))):
                    if not rr:
                        continue
                    ordered = sorted(rr, key=fun, reverse=True)
                    best = ordered[0]
                    maxima.append(dict(island=island, cohort=cohort, phase=phase, metric=metric,
                                       maximum=fun(best), cand=best["cand"], actual_island=best["island"],
                                       seed=best["seed"], C9=best["C9"], C9_mode=mode(best),
                                       interest_raw=best.get("interest"), interest_v2=best.get("interest_v2"),
                                       common_I025=common(best, 0.25), common_I040=common(best, 0.40),
                                       qualifies_025=qualifying(best, 0.25), qualifies_040=qualifying(best, 0.40)))
                    if island in (1, 2) and cohort in ("baseline_g1_7", "continuation_g8_12") and phase == "valid_selected_confirmations":
                        for rank, r in enumerate(ordered[:5], 1):
                            join = joins[rowkey(r)]
                            ranked.append(dict(ranking_scope=f"island{island}:{cohort}:{metric}", rank=rank,
                                island=r["island"], cand=r["cand"], phase=r["phase"], seed=r["seed"], gen=r["gen"],
                                base_cand=r["parents"][0], origin_op=join["actual_origin_op"], C9=r["C9"], C9_mode=mode(r),
                                interest_raw=r.get("interest"), interest_v2=r.get("interest_v2"),
                                common_I025=common(r, 0.25), common_I040=common(r, 0.40),
                                qualifies_025=qualifying(r, 0.25), qualifies_040=qualifying(r, 0.40),
                                descriptor_bin=r.get("cell"), ghash=r.get("ghash"),
                                final_archive_path=str(work / f"isl{island}_final2.tgz"),
                                film_archive_member=f"isl{island}/out/runs/{r['cand']}.npz",
                                filename_declared_in_row=r.get("npz")))
    write_csv(out / "confirmed_top_rows.csv", ranked)

    image_ids = set()
    for island in (1, 2):
        for generations in (set(range(1, 8)), set(range(8, 13))):
            rr = [r for r in confirms if r["island"] == island and r["gen"] in generations
                  and joins[rowkey(r)]["valid_same_genome_base"] and r.get("C9") is not None]
            seen = set()
            for r in sorted(rr, key=lambda r: r["C9"], reverse=True):
                base_key = (island, r["parents"][0])
                if base_key in seen:
                    continue
                seen.add(base_key)
                image_ids.add(base_key)
                if len(seen) == 5:
                    break
    # Explicit instability control: high screen C9, both confirmation C9=0.
    image_ids.add((1, "p1g11_043"))
    image_rows = []
    bycandidate = {(c["island"], c["cand"]): c for c in candidate_rows}
    for key in sorted(image_ids):
        c = bycandidate[key]
        row = dict(c)
        row["film_archive_path"] = str(work / f"isl{key[0]}_final2.tgz")
        row["screen_film_member"] = f"isl{key[0]}/out/runs/{key[1]}.npz"
        row["seed2_film_member"] = f"isl{key[0]}/out/runs/{key[1]}_s2.npz" if c["seed2_cand"] else None
        row["seed3_film_member"] = f"isl{key[0]}/out/runs/{key[1]}_s3.npz" if c["seed3_cand"] else None
        row["suggested_role"] = "unstable_high_screen_control" if key == (1, "p1g11_043") else "top_confirmed_C9_candidate"
        image_rows.append(row)
    write_csv(out / "image_shortlist.csv", image_rows)

    # Source code is inspected as evidence, not imported as an authoritative
    # metric recomputation. No input model/metric code is executed.
    code_paths = [Path(__file__).resolve(), out / "write_report.py", out / "validate_audit.py", pilot / "pod_lib.py", pilot / "reblend_archive.py",
                  pilot / "v3_postpass.py", pilot / "gen_c9backfill.py", pilot / "pod_worker_batch.py",
                  repo / "probes/blobs/l0/complexity/metrics_v3.py", work / "v3bundle/pod_gen.py",
                  work / "v3bundle/pod_lib.py", work / "v3bundle/pod_gen_batch.py",
                  work / "v3bundle/island_config_1.json", work / "v3bundle/island_config_2.json",
                  work / "v3bundle/island_config_cont_1.json", work / "v3bundle/island_config_cont_2.json"]
    for path in code_paths:
        if path.is_file():
            inputs[str(path)] = dict(bytes=path.stat().st_size, sha256=sha256(path))
    interpretation_pins = read_json(out / "interpretation_source_pins.json")
    history_path = out / "history_evidence.json"
    history_evidence = read_json(history_path) if history_path.is_file() else None
    film_selection_checks = []
    for island in (1, 2):
        selection_path = work / f"ops/recovery_20260905/film/selection.final.island{island}.json"
        if not selection_path.is_file():
            continue
        selection = read_json(selection_path)
        for item in selection["items"]:
            r = final[island][item["row_index"]]
            k = (item["island"], item["cand"], item["phase"], item["seed"])
            origin = r if r["phase"] == "screen" else screen_index[(r["island"], r["parents"][0])][0]
            film_selection_checks.append(dict(selection_file=str(selection_path), key=keydict(k),
                row_index=item["row_index"], row_index_matches_key=rowkey(r) == k,
                actual_origin_op=origin["op"], same_genome_screen_link=model_equal(r, origin),
                known_invalid_genome_confirmation=r["phase"] in ("seed2", "seed3") and not joins[rowkey(r)]["valid_same_genome_base"],
                embedded_job_matches_actual_row_model=model_equal(item["job"], r) if item.get("job") else None,
                scope="Identity and model audit only; replay output not reviewed or rerun"))
    write_json(out / "film_selection_identity_checks.json", film_selection_checks)
    residuals = []
    for period in ("baseline_or_atlas", "continuation_or_backfill"):
        for metric_mode in ("partial", "full"):
            rr = [r for r in primary if mode(r) == metric_mode
                  and ((r["gen"] <= 7 and r["phase"] != "c9fill") == (period == "baseline_or_atlas"))]
            w = 0.25 if period == "baseline_or_atlas" else 0.40
            residuals.append(dict(period=period, C9_mode=metric_mode, expected_raw_W9=w, n=len(rr),
                                  max_abs_raw_minus_preserved_blend=safe_max([abs(r["interest"] - common(r, w)) for r in rr])))
    definitions = {
        "identity": "Actual row (island,cand,phase,seed); candidate-name prefixes do not set island. Baselines are reference rows, never appended to final data.",
        "conflict_policy": "Identical-key different-payload variants are quarantined from all primary summaries; both are retained in observations.csv and dedup_conflicts.json. No suffix dedup, latest-row choice or silent genome merge.",
        "common_score": "I_w=(1-w)*interest_v2_preserved +100*w*C9, at w=.25 and .40. interest_raw is not rewritten. Full and partial C9 are not interchangeable assays.",
        "qualification": "status=ok AND C9>=.4 AND common I_w>=60; a descriptive joint threshold, not a biological-cell or heterogeneity test.",
        "C9_stats_denominator": "Only rows with preserved C9 contribute mean/median/max. n and screen-success denominator include all emitted screen jobs, including no_blobs/fail_g0a and missing C9.",
        "screen_success": "Qualifying screen row / all emitted creative screens in cohort/operator, one candidate-name unit per actual island.",
        "any_confirmed": "At least one valid explicit-parent+same-genome seed2/seed3 row qualifies, counted once per base; screen need not qualify. Both all-screen-base and selected-base denominators are shown.",
        "robust_three_seeds": "Screen AND both valid distinct-seed seed2/seed3 rows qualify; complete pair required. Not a confidence statement about unseen seeds. robust_partial_only further requires all three C9 modes partial.",
        "screen_plus_any_confirmed": "Screen qualifies and at least one valid same-genome confirmation qualifies.",
        "selection_bias": "Seed2/seed3 are selected adaptively. All-base confirmation rates are observed validation yields, not estimates that unselected candidates fail. Candidate labels/genotypes/ancestry are correlated; no IID claim.",
        "SIC_caveat": "merge_spatial_ic screen jobs use composed ICs; seed2/seed3 job construction omits ic_npz and uses ordinary reseeds. Same-genome confirmation is not replication of the composed initial state.",
        "descriptor_bins": "Exact preserved MAP-Elites cell strings, not biological cells or heterogeneous compartments. Screen-only observation bins differ from archive occupancy and from pooled-seed bins.",
        "archive_caveat": "Diagnostic reproduces the historical name-based reblend, including quarantined raw imports ONLY for reconstruction. Archive keys/genomes/seed flags are never changed.",
        "native_seed_ok": "Native archive seed{k}_ok is positive interest >=.6*incumbent interest, NOT C9>=.4 and I>=60 or valid same-genome matching.",
        "files": "CSV observations hold preserved scores and all variants. JSON holds compact summary tables. Image member paths identify expected stored runs, not extraction or visual validation."
    }
    integrity = dict(raw_final_rows=len(raw), per_island_raw={str(k): len(v) for k, v in final.items()},
        unique_identity_keys=len(grouped), unambiguous_primary_rows=len(primary),
        exact_duplicate_groups=duplicate_groups, conflicting_identity_keys=len(conflicts), quarantined_rows=len(excluded_ids),
        primary_bucket_counts=dict(Counter(bucket(r) for r in primary)),
        raw_phase_counts=dict(Counter(r["phase"] for r in raw)),
        primary_phase_counts=dict(Counter(r["phase"] for r in primary)),
        baseline_preservation=baseline_checks, baseline_job_result_checks=dict(job_stats),
        valid_confirmation_rows=sum(len(v) for v in valid_confirms.values()), invalid_named_genome_confirmation_rows=len(join_anomalies),
        final_state_gen={str(n): states[n]["gen"] for n in (1, 2)},
        critical_small_files_match_verified_final_archives=critical_checks,
        archive_whole_sha256_from_existing_verified_records={str(n): verified[n]["sha256"] for n in (1, 2)},
        archive_whole_hash_note="Archive SHA256 values are read from existing independent verification records, not rehashed by this audit. Each small critical input is rehashed and matched here.",
        c9_mode_counts=dict(Counter(mode(r) for r in primary)), raw_blend_residuals=residuals,
        unique_creative_ghashes=len({r["ghash"] for r in creative}), creative_base_candidates_n=len(creative))
    summary = dict(definitions=definitions, integrity=integrity, config_notes_to_audit=config_note_checks,
                   phase_summary=phase_summary, per_generation_screen=per_gen, operator_rates=operator_rates,
                   baseline_historical_reproduction=reproduction, descriptor_breadth=breadth,
                   archive_summary=archive_summary, reblend_initial_vs_surviving=reblend_stage_summary, maxima=maxima,
                   history_evidence_file=str(history_path) if history_evidence is not None else None)
    write_json(out / "audit_tables.json", summary)
    write_json(out / "dedup_conflicts.json", dict(policy=definitions["conflict_policy"], conflicts=conflicts))
    write_json(out / "confirmation_join_anomalies.json", join_anomalies)
    write_json(out / "source_manifest.json", dict(inputs=inputs,
               audited_interpretations=interpretation_pins["sources"],
               final_archive_sha256_from_verified_records=integrity["archive_whole_sha256_from_existing_verified_records"]))
    print(json.dumps(dict(output=str(out), integrity={k: integrity[k] for k in (
        "raw_final_rows", "unique_identity_keys", "unambiguous_primary_rows", "primary_bucket_counts",
        "valid_confirmation_rows", "invalid_named_genome_confirmation_rows")},
        archive_summary=archive_summary), indent=2))


if __name__ == "__main__":
    main()
