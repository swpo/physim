#!/usr/bin/env python3
"""Build HARVEST2_DRAFT.md from audit.py output; no inputs are changed."""
import csv
import json
from pathlib import Path

D = Path(__file__).resolve().parent
T = json.loads((D / "audit_tables.json").read_text())
H = json.loads((D / "history_evidence.json").read_text())
M = json.loads((D / "source_manifest.json").read_text())
J = json.loads((D / "confirmation_join_anomalies.json").read_text())
F = json.loads((D / "film_selection_identity_checks.json").read_text())
with (D / "observations.csv").open() as f:
    OBS = list(csv.DictReader(f))
with (D / "image_shortlist.csv").open() as f:
    IMAGES = list(csv.DictReader(f))


def pick(rows, **conditions):
    matches = [r for r in rows if all(r.get(k) == v for k, v in conditions.items())]
    assert len(matches) == 1, conditions
    return matches[0]


def fmt(x, n=4):
    return "—" if x is None or x == "" else f"{float(x):.{n}f}"


def fraction(n, d):
    return f"{n}/{d} ({100*n/d:.1f}%)" if d else f"{n}/{d}"


def tab(headers, rows):
    def escape(v):
        return str(v).replace("|", "\\|")
    return "\n".join(["| " + " | ".join(map(escape, headers)) + " |",
                       "| " + " | ".join("---" for _ in headers) + " |"]
                      + ["| " + " | ".join(map(escape, r)) + " |" for r in rows])


def phase(cohort, phase="screen", mode="all", island="both"):
    return pick(T["phase_summary"], cohort=cohort, phase=phase, C9_mode=mode, island=island)


def op(cohort, operator="ALL", w=0.25):
    return pick(T["operator_rates"], cohort=cohort, op=operator, W9=w, island="both")


parts = []
parts.append("""# HARVEST2 — audited final v3 continuation (draft)

**Scope:** two islands, creative generations 1–12, with generation-12 seed2/seed3 settlement complete. This is a local read-only analysis of the settled small files. No simulations, model evaluations, remote jobs, full archive extraction, raw-data rewrites, or web-page edits were performed by the main audit. Supplemental history notes pin selected source-text members from the already-local final archives.

## Measured verdict

The changed-configuration continuation added qualifying MAP-Elites descriptor bins and raised the best observed **partial-C9** same-genome confirmation from **0.8504 to 0.8895**. It did not show uniform improvement across islands or across selected confirmations. Screen success improved descriptively, but the selected-confirmation distribution and candidate-level validation yields did not improve uniformly.

This is **not** proof of biological cells, heterogeneous compartments, or a new biological organization level. Full C9 was not measured during the continuation. h9 remains exploratory; this harvest does not validate it. The operator mix, retry limits, objective weight, and parent archive changed together. These data do not identify their separate causal effects. They also do not test an unrun same-configuration continuation. The earlier forecast that the C9 ceiling could not improve under that counterfactual lacked evidence.

## 1. Sources, identity, and exclusions

The audit rehashes all ten critical settled files and matches the existing independent final-archive verification records. It does not rehash the two large archives. Their recorded SHA256 values and every small input hash are in `source_manifest.json`. Both final states are generation 12. The 2,324 baseline rows are exactly preserved in the final results and are not counted twice.
""")
parts.append(tab(["Artifact owner", "Raw final rows", "Creative screens", "Selected confirmation rows", "C9fill raw / retained", "Atlas imports"], [
    [i, T["integrity"]["per_island_raw"][str(i)],
     sum(r["island"] == str(i) and r["bucket"] == "creative_screen" for r in OBS),
     sum(r["island"] == str(i) and r["bucket"] == "selected_confirmation" for r in OBS),
     f"{sum(r['island']==str(i) and r['phase']=='c9fill' for r in OBS)} / {sum(r['island']==str(i) and r['phase']=='c9fill' and r['primary_included']=='True' for r in OBS)}",
     3] for i in (1, 2)]))
parts.append("""
Identity is the actual row tuple **(island, cand, phase, seed)**. Candidate-name prefixes are not island evidence. The 3,606 raw rows contain 3,605 distinct keys. One key has contradictory model payloads. Both variants are quarantined from primary summaries, leaving **3,604 retained rows**: 2,099 creative screens, 1,331 selected assay rows, 168 C9 backfill imports, and six atlas imports.

The conflicting key is `(2, p1g2_008_c9, c9fill, 958)`. Its two rows have:

- ghash `a19e1629a9d1fb98`, 4 activators / 8 channels, C9 0.4215, raw I 54.57172838379547;
- ghash `6aef37d09adb821c`, 2 activators / 5 channels, C9 0.4855, raw I 59.5337117778859.

Both donor entries already share the name `p1g2_008`. The backfill generator iterates archive entries without an identity-safe output name. Both rows declare `p1g2_008_c9.npz`. A single candidate-based path is therefore ambiguous. Row timestamps do not establish which genome the surviving film contains or prove overwrite timing. See `dedup_conflicts.json` and `history_evidence.json:c9fill_duplicate`. Both raw variants remain in `observations.csv` with `primary_included=False`.

### Eleven baseline seed3 rows are not replications of the named screen genome

All 2,318 generation-1–7 job/result pairs agree on the actual genome, parent list, and operator. However, eleven seed3 **jobs themselves** use a donor genome with the same base name as a new v3 candidate. Their physical model fields differ from the screen/seed2 model. These are not id, tag, provenance, or float-format-only differences.

`g0import` keeps donor names. New screens reuse `p{island}g{gen}_{index}`. `archive_seedk` takes the first archive entry whose candidate name matches after suffix stripping. `cmd_ingest2` then builds seed3 from that entry's genome, not the seed2 result's genome. The selected donor model matches each anomalous seed3 row exactly. See `pod_lib.py:291–306`, `pod_gen.py:375–393`, and the pinned source excerpts in `history_evidence.json`.
""")
parts.append(tab(["Island", "seed3 row", "Screen ghash", "Actual seed3 ghash", "Physical fields that differ", "Named screen op → actual model op"], [
    [j["key"]["island"], j["key"]["cand"], j["screen_ghash"], j["confirmation_ghash"],
     ", ".join(j["physical_differences_from_named_screen"]["differing_core_fields"]),
     j["screen_operator"] + " → " + str(j["actual_origin_op"])] for j in J]))
parts.append("""
`confirmation_join_anomalies.json` records the exact keys, donor entries, job paths, model hashes, and sample numeric differences. These eleven runs remain valid observations of their actual models, but do not count as third-seed confirmations of the named v3 screens. Three meet the joint threshold at W9=.25; two meet it at W9=.40.

Strict physical-genome matching succeeds for **931/942 baseline selected assay rows** and **389/389 continuation selected assay rows**. This is a statement about these stored result/job identities, not a blanket validity claim for all runs. It does not establish same-initial-condition replication.

## 2. Common scores and metric modes

For each preserved row, compute only:

```text
I_w = (1-w) * interest_v2_preserved + 100*w*C9
w in {0.25, 0.40}
qualifying = status == "ok" AND C9 >= 0.4 AND I_w >= 60
```

The raw `interest` field is unchanged and retained in `observations.csv`. No old/new raw-interest difference is treated as like-for-like. The formula rescales stored measurements; it does not rerun the metric or the search. Partial C9 omits s9 and is not the same assay as full four-factor C9. Missing C9 is not assigned zero in metric means. Missing/failed screens still count in the screen-lane denominator.

There are 19 full-C9 rows: six atlas imports and 13 generation-1 creative screens. All continuation and C9fill measurements are partial. The following table separates full and partial observations. Mean scores are conditional on the shown measured rows; they are not means over all emitted lanes.
""")
cohort_names = {"baseline_g1_7":"g1–7", "transition_g8":"g8", "late_g9_12":"g9–12", "continuation_g8_12":"g8–12"}
metric_rows = []
for cohort in cohort_names:
    for mode in (("partial", "full") if cohort == "baseline_g1_7" else ("partial",)):
        r = phase(cohort, mode=mode)
        metric_rows.append([cohort_names[cohort], mode, r["n"], fmt(r["c9_mean"]), fmt(r["c9_median"]), fmt(r["c9_max"]),
                            fmt(r["common_I025_mean"], 2), fmt(r["common_I040_mean"], 2),
                            f"{r['qualifying_025_n']} / {r['qualifying_025_descriptor_bins']}",
                            f"{r['qualifying_040_n']} / {r['qualifying_040_descriptor_bins']}"])
parts.append(tab(["Creative cohort", "C9 mode", "Measured n", "Mean C9", "Median C9", "Max C9", "Mean I.25", "Mean I.40", "Q.25 / bins", "Q.40 / bins"], metric_rows))
parts.append("""
The retained backfill imports are separate from creative progress: 168 partial-C9 rows, mean 0.3188, median 0.3719, maximum 0.6393. They yield 64 qualifying rows / 34 bins at W9=.25, and 59 / 32 at W9=.40. These counts exclude the two ambiguous variants. Atlas imports yield no joint-threshold successes.

Selected confirmations are also separate. Their means are selection-biased and are not estimates of the complete screen population. This table uses only correctly linked physical genomes:
""")
parts.append(tab(["Cohort", "Selected assay n", "C9 measured n", "Mean / median C9", "Max C9", "Mean I.25 / I.40", "Q.25 / Q.40"], [
    [cohort_names[c], r["n"], r["c9_measured_n"], f"{fmt(r['c9_mean'])} / {fmt(r['c9_median'])}", fmt(r["c9_max"]),
     f"{fmt(r['common_I025_mean'],2)} / {fmt(r['common_I040_mean'],2)}", f"{r['qualifying_025_n']} / {r['qualifying_040_n']}"]
    for c in cohort_names for r in [phase(c, "verified_same_genome_confirmations")]]))
parts.append("""
The continuation's observed partial-C9 screen mean is higher than the baseline's, but its selected-confirmation mean is lower. The maximum and distribution tell different stories. Neither difference isolates an operator or configuration effect.

## 3. Screen-only generation tables and descriptor breadth

Below, `n` includes every emitted creative screen. C9 mean/median/max use only measured rows. `P/F` gives partial/full measurement counts. Generation 1's aggregate C9 statistic is mixed-mode; its full/partial split is above and in the CSV. Qualifying counts use the common score at each weight. Bins are exact **MAP-Elites descriptor bins**, not biological cells or heterogeneous compartments. Island-specific and mode-specific tables are in `screen_by_generation.csv`.
""")
parts.append(tab(["Gen", "n", "ok / no_blobs / fail_g0a", "P/F", "C9 mean / median / max", "Q.25 / bins", "Q.40 / bins"], [
    [r["gen"], r["n"], f"{r['status_ok']} / {r['status_no_blobs']} / {r['status_fail_g0a']}",
     f"{r['c9_partial_n']}/{r['c9_full_n']}", f"{fmt(r['c9_mean'])} / {fmt(r['c9_median'])} / {fmt(r['c9_max'])}",
     f"{r['qualifying_025_n']} / {r['qualifying_025_descriptor_bins']}",
     f"{r['qualifying_040_n']} / {r['qualifying_040_descriptor_bins']}"]
    for r in T["per_generation_screen"] if r["island"] == "both" and r["C9_mode"] == "all"]))
parts.append("""
Across screens only, baseline g1–7 has **59 / 51 qualifying bins** at common W9=.25/.40. Continuation g8–12 has **50 / 45**, including **12 / 14 bins** not seen qualifying in the baseline. The unions are **71 / 65**. In partial mode alone, the corresponding baseline counts are 55 / 48 and the unions are 67 / 62. These are observed-bin counts, not newly created archive entries.

The old **516 rows / 76 union bins** is reproducible at common W9=.25 when screens and selected assay rows are pooled. It is not 516 independent candidates or 76 verified archive incumbents. Excluding the three qualifying wrong-genome seed3 links leaves 513 correctly linked/screen qualifying observations, while the union remains 76 because those bins also have other observations. The corresponding correctly linked W9=.40 row count is 441, with 66 union bins. Screen-only baseline counts are 281 / 241 rows, not 516. Generation 1 alone has 102 pooled qualifying rows in 38 bins at W9=.25, not the full seven-generation 76-bin union.

## 4. Corrected candidate and operator rates

Definitions:

- **Screen success:** qualifying screen / all emitted creative screens.
- **Any-confirmed base:** at least one correctly linked same-genome seed2/seed3 assay qualifies. The screen need not qualify. Count each `(island, base candidate)` once.
- **Three-seed joint-threshold base:** screen, seed2, and seed3 all qualify, with matching physical genome and three distinct seeds. The CSV calls this `robust_three_seeds`; it is not a probability guarantee for new seeds.
- **Partial-only three-seed base:** the previous condition plus partial C9 on all three assays.

The all-base denominator measures observed validation yield. Unselected candidates have missing confirmation evidence, not proven failures. The selected and complete-pair denominators are shown separately. Selection is adaptive. Candidate names are distinct counting units, not independent random samples: the 2,099 creative candidates contain 1,929 distinct physical ghashes and share ancestry.
""")
rate_rows = []
for c in cohort_names:
    for w in (.25,.40):
        r=op(c,w=w)
        rate_rows.append([cohort_names[c], fmt(w,2), fraction(r["screen_success_n"],r["base_candidates_n"]),
                          f"{r['selected_valid_n']} / {r['complete_valid_pairs_n']}",
                          fraction(r["any_confirmed_n"],r["base_candidates_n"]),
                          fraction(r["any_confirmed_n"],r["selected_valid_n"]),
                          fraction(r["robust_three_seeds_n"],r["base_candidates_n"]),
                          fraction(r["robust_three_seeds_n"],r["complete_valid_pairs_n"]),
                          r["robust_partial_only_n"]])
parts.append(tab(["Cohort", "W9", "Screen / all", "Selected / valid pairs", "Any confirm / all", "Any confirm / selected", "Three-seed / all", "Three-seed / pairs", "Partial-only three-seed n"],rate_rows))
parts.append("""
### Why 0.82 was not an operator hit rate

The old `merge_spatial_ic` numerator 92 combined **52 qualifying screens + 40 qualifying selected confirmation rows**, then divided by 112 screen lanes. The corrected W9=.25 screen rate is **52/112 = 46.4%**. At candidate level, **23/112 = 20.5%** have at least one qualifying same-genome confirmation, and **12/112 = 10.7%** meet the three-assay threshold (11 are partial-only). Among the 49 selected bases, the any-confirmed fraction is 23/49; among 44 valid complete pairs, the three-assay fraction is 12/44. At W9=.40, the counts are 45 screen successes, 21 any-confirmed bases, and 12 three-assay bases.

**Initial-condition caveat:** SIC screens use a composed `ic_npz`. The seed2 and seed3 builders omit `ic_npz` and use ordinary genome reseeds. All 182 stored SIC screens have `ic_merge=True`; all 130 SIC-origin confirmation rows lack that flag. Thus these are same-genome assays under a different initial-state construction, **not replications of the spatially composed phenotype**. This design difference is separate from the eleven wrong-genome substitutions.

The corrected baseline operator table at common W9=.25 follows. All numerators are one-count-per-base, except the explicitly screen-only column. Both weights, both islands, and all continuation cohorts are in `operator_rates.csv`.
""")
parts.append(tab(["Origin operator", "Screen success / all bases", "Selected bases", "Any-confirmed / all bases", "Three-assay / all bases"], [
    [r["op"], fraction(r["screen_success_n"],r["base_candidates_n"]), r["selected_valid_n"],
     fraction(r["any_confirmed_n"],r["base_candidates_n"]), fraction(r["robust_three_seeds_n"],r["base_candidates_n"])]
    for r in T["operator_rates"] if r["island"]=="both" and r["cohort"]=="baseline_g1_7" and r["W9"]==.25 and r["op"]!="ALL"]))
parts.append("""
SIC has the largest observed baseline screen success fraction, but the experiment did not randomly assign common parents and initial states to operators. The result is not a controlled causal validation. Continuation SIC has 28/70 screen successes at W9=.25, six any-confirmed bases, and four three-assay bases. Genome reuse is especially common in SIC: 112 baseline SIC candidates contain 43 distinct ghashes; 70 continuation SIC candidates contain 34. Different composed screens can share a genotype, while ordinary confirmation reseeds can repeat the same genotype/seed outcome under different candidate names.

## 5. Actual generator/configuration history

Use jobs, code, and campaign history rather than stale config comments. Requested counts are per island per generation. See `history_notes.md` and `history_evidence.json` for exact source lines and hashes.
""")
parts.append(tab(["Setting", "g1–7", "g8 only", "g9–12"], [
    ["W9", ".25", ".40", ".40"],
    ["mutate",16,16,22], ["mint_bilin",12,16,18], ["delete_bilin",4,4,4], ["add_chan",8,8,8],
    ["dup_act",8,0,0], ["SIC target slots",8,24,12], ["SIC retries per target","pilot generator",60,12],
    ["immigrate",20,5,5], ["merge_mix cross / slow / share","12 / 8 / 4","14 / 6 / 0","14 / 6 / 0"],
    ["Actual classical merge target slots",24,20,20], ["Total requested creative slots",100,93,89]]))
parts.append("""
`mix.merge=20` is not the generator's classical-merge loop bound. `merge_mix` supplies the loop plan, so the old plan totals 24, not 20. A slow-tanh target can fall back to a cross-edge child, and retry failure can drop a target. Requested and emitted counts therefore differ. Gen8 emitted 81/82 creative jobs across the two islands. Gens9–12 emitted 72/70, 69/72, 70/68, and 72/67.

The SIC target changes from 24 to 12 **at generation 9**, with retry cap 12. The final generator differs from the launch generator only in SIC retry cap 60→12 at line 203. `campaign9.sh` and both campaign logs pin the resume to generation 9. The settled `_midcourse` text saying “gens10–12” is stale. The gen8→gen9 mutate/mint increases are **+6 and +2**, not “+6 each.” Relative to the original pilot, their values are 16→22 and 12→18, respectively.
""")
parts.append(tab(["Gen", "SIC emitted isl1", "SIC emitted isl2", "SIC target per island"], [
    [g,
     next(j["operators"].get("merge_spatial_ic",0) for j in H["generation_history"]["emitted_jobs"] if j["island"]==1 and j["gen"]==g),
     next(j["operators"].get("merge_spatial_ic",0) for j in H["generation_history"]["emitted_jobs"] if j["island"]==2 and j["gen"]==g),
     24 if g==8 else 12] for g in range(8,13)]))
parts.append("""
The continuation emitted 70 SIC screens in total: 45 in gen8 and 25 in gens9–12, not 24 lanes per island for all five generations. `operator_emitted_by_generation.csv` records all actual screen operators. Broader changes also include C9 backfill, reblended parent selection, and C9 field propagation into new archive entries. Their joint effect cannot be separated from objective weight or operator mix using this continuation alone.

## 6. Archive reblend limitations — identified, not repaired

The final archives have 343 and 327 entries. Each still includes 100 legacy six-axis keys; the remaining keys have seven axes. This is not a count of biological compartments. The stored union contains 435 descriptor keys, which must not replace the qualifying-observation bin counts above.

All 496 surviving `_reblended_w9=.4` entries reproduce the historical script's numeric score and C9 join. However, that script selects the highest **stored-interest** row after name-suffix splitting, then copies its new blend/C9 annotation into an existing entry. It does not require the same physical genome, descriptor key, or seed, and does not update the archive key, genome, horizon, summary, or existing confirmation fields.
""")
parts.append(tab(["Island", "Marked entries", "Different physical genome", "Different descriptor key", "Of these: seven-axis keys", "Different winning row if ranked at common .40"], [
    [r["island"],r["marked_reblended_n"],r["marked_model_mismatch_n"],r["marked_descriptor_mismatch_n"],
     r["marked_descriptor_mismatch_7axis_n"],r["marked_different_best_at_040_n"]] for r in T["archive_summary"]]))
parts.append("""
### Initial contamination versus surviving entries

The initial join can be reconstructed without later-generation rows: use each original 269-entry gen7 archive and the preserved baseline-plus-C9fill result prefix. All 538 initial targets join; none is retained for lack of C9. The initial and surviving scopes differ as follows:
""")
parts.append(tab(["Island", "Scope", "Entries", "Wrong physical model", "Different descriptor key", "Exact-model screen references", "Different seed from that screen"], [
    [r["island"],r["stage"],r["entries"],r["wrong_physical_model_n"],r["different_descriptor_key_n"],
     r["exact_model_screen_reference_n"],r["selected_seed_differs_from_screen_reference_n"]]
    for r in T["reblend_initial_vs_surviving"]]))
parts.append("""
The same 29 wrong-physical-model key/source pairs are present initially and survive at the end. The 42 replaced entries contain no wrong-model joins; their 13 descriptor mismatches explain the reduction from 365 to 352. This reconstruction supports the initial count rather than assuming the surviving count was the full initial impact.

**Seed limitation:** all 538 initial and all 670 final entries omit the target `seed` field. Therefore a universal wrong-target-seed count is not identifiable. The last two table columns compare the chosen source seed only to an exact name-and-physical-model matching historical screen, where one exists. Different source seeds are expected when intentionally choosing a best reseed; they are not automatically wrong seeds. Two island-2 cases also choose the wrong physical model. See `reblend_initial_vs_surviving.csv` for every initial and surviving target.

Of the 29 physical-genome mismatches, 27 are imported gen0 entries. Two are island-2 v3 entries (`p2g2_038`, `p2g7_039`) whose chosen seed3 model is a namesake donor. The 352 descriptor mismatches include all 200 legacy six-axis keys and 152 seven-axis keys. A different descriptor on a correctly matched reseed can be real behavioral variation; the problem is attaching that score to an unchanged archive key as if it measured the same bin/run.

The reblend ranking also mixes old stored weights with already-.40 backfill rows. For 27 surviving entries, selecting by common W9=.40 would choose a different row. This is a diagnostic only. It is not a silent archive repair. Numeric “single currency” does not establish model/run provenance.

The native seed3-ok counts are 103/99 in the final archives (74/73 in the baseline). Native `seed{k}_ok` means positive score ≥0.6× incumbent score, not the joint C9/interest threshold, and name-only matching is unsafe. These flags must not be presented as strict same-genome or same-IC confirmation counts. See `archive_reblend_diagnostics.csv` for every surviving entry and `history_evidence.json` for all 29 mismatched identities.

## 7. Confirmed maxima and image candidates

These maxima use explicit parents plus matching physical genomes. All are partial C9. “Confirmed” here means the row is a correctly linked selected reseed, not that every tested seed has the maximum or passes the joint threshold.
""")
parts.append(tab(["Island", "Cohort", "Maximum-C9 selected row", "C9", "Preserved I2", "Common I.25", "Common I.40", "Qualifies at .25/.40"], [
    [r["island"],cohort_names[r["cohort"]],r["cand"],fmt(r["C9"]),fmt(r["interest_v2"],3),fmt(r["common_I025"],3),fmt(r["common_I040"],3),
     f"{r['qualifies_025']}/{r['qualifies_040']}"]
    for r in T["maxima"] if r["island"] in (1,2) and r["cohort"] in ("baseline_g1_7","continuation_g8_12") and r["phase"]=="valid_selected_confirmations" and r["metric"]=="C9"]))
parts.append("""
Island 2's continuation maximum C9=0.7123 does **not** meet I≥60 at either common weight. Its full-run maximum remains the older 0.8048 row. The best continuation island-2 C9 row that does meet both thresholds is `p2g8_020_s2` (0.6824).

The final overall joint-score maximum is `p1g12_049_s2`: preserved I2=81.38231987330606, C9=.8854, common I.25=83.17173990497955 and I.40=84.24539192398363. The final overall C9 maximum is its seed3 row `.8895`, not the old `.8504`.

Recommended image subjects include the following distinct base candidates. The CSV contains exact raw inputs, seed rows, archive/member paths, and threshold flags. A path is a locator, not evidence that a film has been visually reviewed here.
""")
show_ids = {(1,"p1g12_049"),(1,"p1g12_007"),(1,"p1g12_037"),(1,"p1g11_043"),(2,"p2g8_020"),(2,"p2g10_023"),(2,"p2g6_032")}
parts.append(tab(["Base candidate", "Origin op", "C9 screen / seed2 / seed3", "Three-assay pass at .25/.40", "Image role"], [
    [r["cand"],r["op"],f"{fmt(r['screen_C9'])} / {fmt(r['seed2_C9'])} / {fmt(r['seed3_C9'])}",
     f"{r['robust_three_seeds_025']}/{r['robust_three_seeds_040']}",r["suggested_role"]]
    for r in IMAGES if (int(r["island"]),r["cand"]) in show_ids]))
parts.append("Current final film-selection manifests also resolve to the following exact row identities. All six row indices match, none is a known wrong-genome confirmation, and all five confirmation items match their screen genome. The screen item is not itself a confirmation. Three manifests embed legacy job payloads; those three match their actual row models. Missing embedded jobs are not counted as checked by this particular manifest audit. Replay output is outside this audit; see `film_selection_identity_checks.json`.")
parts.append(tab(["Island", "Selected row", "Phase", "Seed", "Actual origin op", "Embedded job model checked"], [
    [x["key"]["island"],x["key"]["cand"],x["key"]["phase"],x["key"]["seed"],x["actual_origin_op"],
     x["embedded_job_matches_actual_row_model"] if x["embedded_job_matches_actual_row_model"] is not None else "not embedded"] for x in F]))
parts.append("""
`p1g12_049` is an `add_chan` child of `p1g11_043`; `p1g12_007` is a `mutate` child of the same parent. `p1g11_043` is a `delete_bilin` child of `p1g10_048`. The middle candidate's screen C9=.8185 falls to zero in both ordinary reseeds, so it is a useful instability control. Its descendants' high observations are not evidence of monotonic robust lineage improvement.

The old HARVEST image examples (`p1g1_009_s3`, `p2g6_032_s2`, `p1g3_005_s3`, `p1g2_051_s3`, `p1g2_052_s3`, `p1g4_050_s3`, `p2g7_049_s3`) are outside the eleven wrong-genome set. Four anomalous seed3 origin labels do change, as listed in section 1. Films of any affected row must use that row's actual job genome/seed/phase, not a suffix-inferred parent. SIC film captions must also distinguish composed screen IC from soup reseeds.

## 8. Corrections needed in posts 10/12 and the old harvest notes

No web pages or old harvest documents were edited by this audit. These corrections refer to the exact reviewed versions pinned in `interpretation_source_pins.json`. Concurrent edits may already address some items. Validation detected that post12 changed after review; its original hash and quoted line excerpts are retained rather than silently repinned. `VALIDATION.json` records interpretation drift separately from immutable data/code input checks.

### Post 12: `docs/blobs/breeding-spatial-economies.html`

- Lines 40–46, 115–120: call 76 a union of qualifying observed **descriptor bins** over screens and selected assays, not 76 archived biological/economy cells or independent candidates. Use screen-only rates and separate native archive flags from strict confirmation.
- Lines 63–65: replace the displayed additive equation with `(1-W9)*interest_v2 +100*W9*C9`.
- Lines 126–141: replace or label the pooled-generation table. It is not a screen-only trial series. Supply full/partial and denominator distinctions.
- Lines 143–170 and the associated chart: replace 0.82 and the whole mixed-row “hit-rate” table. Use screen success and one-count-per-base confirmation rates. State SIC's changed-IC confirmation design.
- Lines 173–179 and 211–233: retain the limited observation that the initial global maximum appeared early. Remove a fixed-ceiling forecast and the claim that all 76 bins appeared in one generation. Changed-config continuation is not a same-config counterfactual test, nor a grammar-ceiling proof.
- Lines 220–227: describe sic24 for gen8 only, then sic12+retry12 for gens9–12; mutate22/mint18; actual `merge_mix` planning and emitted counts. Do not carry the stale midcourse note forward.
- Label the actual new maxima and full-vs-partial limits. Do not imply that a proxy or a film proves heterogeneous compartments.

### `HARVEST.md` and `POST12_FACTS.json`

Correct `operator_hit_rate`, pooled `per_gen` labels, `continuation`, and the counterfactual ceiling prose. Keep the historical 516/76 figures only with their proper pooled-observation definition. “Strict economy class = 6” means **six qualifying full-C9 rows at W9=.25**, not six total class-economy rows: there are 18 total, including atlas imports and nonqualifying screens. The corresponding qualifying count at W9=.40 is four. No partial-C9 continuation row can satisfy the full-s9 spatial-class rule.

Do not call the reblended archive fully provenance-consistent just because its scalar scores use one formula. Add the contradictory C9fill key, the eleven wrong-genome seed3 jobs, and the 29 surviving reblend identity mismatches. None should be silently rewritten.

### Post 10: `docs/blobs/evolving-at-scale.html`

This audit does **not** re-audit the original v2 campaign's 423-bin, 9,409-evaluation, lineage, or I=91.16 claims. Do not replace those numbers with v3 data. Clarify “cells” as MAP-Elites descriptor bins where needed. Keep original v2 scores distinct from normalized v3 scores; 91.16 v2 and 84.2454 v3 are not directly comparable. Cross-links and new captions must not assume a reused candidate name uniquely identifies a v2/v3 model. C9fill imports and v3 descendants are not newly discovered v2 archive worlds. Original v2 provenance claims need their own source-genome audit before any numerical correction.

## 9. Reproduction and source pins

From the project root, in its own environment:

```sh
.venv/bin/python probes/blobs/l0/deepsearch/v3_pilot/harvest2_audit/audit.py
.venv/bin/python probes/blobs/l0/deepsearch/v3_pilot/harvest2_audit/write_report.py
.venv/bin/python probes/blobs/l0/deepsearch/v3_pilot/harvest2_audit/validate_audit.py
```

`audit.py` reads only small settled/reference JSON, logs, configs, and baseline job JSON. It does not depend on the ongoing metadata/film extraction. The optional `history_evidence.json` is a pinned supplement with source excerpts; the report uses it for the history section. Source-history pins can be checked with a selective text-member read, without extracting the archive to disk. Main assertions check final counts, small-file certificates, baseline row identity, all baseline job/result identities, and the eleven strict-genome mismatches.

Primary outputs:

- `observations.csv`: preserved raw scores, common-weight scores, phase/mode, identity, and inclusion flags for every raw row.
- `screen_by_generation.csv`, `cohort_phase_summary.csv`, `operator_emitted_by_generation.csv`: denominators, modes, per-generation screens, common-weight comparisons, and actual emitted operators.
- `candidate_confirmations.csv`, `operator_rates.csv`, `confirmation_origins.csv`: candidate-unit evidence and strict physical-genome rates.
- `dedup_conflicts.json`, `confirmation_join_anomalies.json`, `archive_reblend_diagnostics.csv`, `reblend_initial_vs_surviving.csv`: explicit unresolved/invalid joins and initial-versus-final reconstruction; no repair.
- `confirmed_top_rows.csv`, `image_shortlist.csv`, `film_selection_identity_checks.json`: exact candidate/phase/seed, film member locators, and checked selection identities.
- `audit_tables.json`, `source_manifest.json`, `history_notes.md`, `history_evidence.json`, `interpretation_source_pins.json`: machine-readable summaries and exact reviewed source pins.
- `VALIDATION.json`: independent checks of row identity, raw-score preservation, common-score arithmetic, candidate denominators, initial/final joins, film selections, and every small input hash.

Critical result/archive SHA256 pins:
""")
pins = []
for i in (1,2):
    for fn in ("results.json","archive.json","state.json"):
        c=next(c for c in T["integrity"]["critical_small_files_match_verified_final_archives"] if c["island"]==i and c["path"].endswith("/"+fn))
        pins.append([f"island {i} settled {fn}",c["sha256"]])
    pins.append([f"isl{i}_final2.tgz (existing verified record)",T["integrity"]["archive_whole_sha256_from_existing_verified_records"][str(i)]])
parts.append(tab(["Source", "SHA256"],pins))
parts.append("""
The final deployed `pod_gen.py` SHA256 is `e1e52bac2847fcb8d0be99cc8f1d47cf7019de3914988e2e314959f7dd90dc3e`. The local launch generator is `1eb2277273338bd9fee441bcabc556eb2fc2ad8c5e0e7f55861311a55cbebdf7`. The final deployed `reblend_archive.py` is `8111730347b0fefcf0cb2d98b98a6420ea8cad26d8b41cffe3c4bed66ba3a160`. The final metric source is `2273a13f7de704234261c15f2886a57a1b68d017b196bf637e3c61db5fbd40c9`. Exact archive member names, config/log hashes, and source-line evidence are in `history_evidence.json` and `source_manifest.json`.
""")
report = "\n\n".join(p.strip() for p in parts) + "\n"
(D / "HARVEST2_DRAFT.md").write_text(report)
print(f"Wrote {D / 'HARVEST2_DRAFT.md'} ({len(report)} characters)")
