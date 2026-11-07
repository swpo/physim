"""Add the independent checker's block (and two corrected ranking fields) to results/summary.json."""
import json
from pathlib import Path
R = Path("/home/user/evalwork/gc_suites/rescore_fair")
p = R / "results/summary.json"
d = json.loads(p.read_text())
O = R / "checker/out"
d2 = json.loads((O / "derived2.json").read_text())
d["ranking"]["weakest_mechanism_control_overall"] = dict(
    per_case=dict(suite="vortex/long2", case="c003", control="eps0", ratio_old=1.5300094537676328, ratio_new=1.706608624284365),
    aggregate=dict(suite="vortex/long2", control="eps0", ratio_old=d2["weakest_mechanism_aggregate"]["plugin"][0],
                   ratio_new=d2["weakest_mechanism_aggregate"]["fair"][0]),
    note="added by checker: the report text named rods/main_iter2 walloff (1.60 -> 1.79), which is the weakest in rods only")
d["ranking"]["ratio_to_native_change_factor"] = dict(
    per_case_non_native=[0.9751834845476929, 1.7781805082131485],
    per_case_persistence=[1.0623613756389738, 1.7781805082131485],
    aggregate_non_native=[d2["ratio_rise_factor_non_native_controls"][0][0], d2["ratio_rise_factor_non_native_controls"][1][0]],
    aggregate_native_like=[d2["ratio_rise_factor_native_like"][0][0], d2["ratio_rise_factor_native_like"][-1][0]],
    note="added by checker: fair ratio / plugin ratio to independent_native; extremes rods/formation c002 wrong_probe_geometry "
         "(0.975) and vortex/main c004 initial_persistence (1.778, native drops 43.8% there); native-like = band_native, "
         "native_b, numerical_null, and ignore_actions on no-action cases. The report's 'every ratio rises 1.06-1.48x' is wrong.")
d["checker"] = dict(
    what="Independent check (checker/ scripts, own forecast lookup from the suites' own scripts, own report/specificity "
         "formulas); about 0.5 CPU-minute, nice 10, one process.",
    verified=[
        "plugin reproduces all 715 stored suite scores bit for bit (full score_case reports incl. marginal CRPS for the 9 "
        "pm/cips/rods suites; agg + groups for vortex main/formation/long2): checker/out/plugin_check.json",
        "checker's plugin and fair scores equal out/<world>/<suite>/{plugin,fair} exactly for all 715: checker/out/compare_with_shadow.json",
        "control tables cips/main_iter2, cips/formation, phase_membrane/formation, vortex/formation: every ratio, ci90 and "
        "separated flag equals control_tables (rtol 1e-12): checker/out/derived.json, check3.json",
        "specificity: page cards probe_wide, sink_site, steer_p, keep_empty, vortex S_steer equal page.cards old/new; "
        "all 109 pm/cips/rods program rows reproduce the stored rows under plugin and equal summary.specificity under fair; "
        "vortex E_feed (first native 1.586->1.376, pooled 1.134->0.989), I_follow probe (1.57->1.54), cips B_s_bath (1.51->1.64)",
        "tag changes: page probe_wide 'at the probe'->'whole-world' and steer_p 'specific'->'at the probe'; off-page "
        "feed_B x2, hold_neck, E_feed (first native): exactly these, no others; phase_membrane Singled out 'S I BD'->'I BD'",
        "separation flags (cips iter2 null now separates; cips formation wrong_probe_geometry no longer), the only aggregate "
        "order change (cips formation null vs band_native), persistence min 2.26->2.74, 20 per-case flips, native drop "
        "19.5-22.3% per suite (cases 5.9-43.8%, groups 14-31%), rods band 0.976-1.108 and S_steer null 0.96, vortex "
        "formation null 0.94 [0.90, 1.01] / band 0.43-1.62 / 4 of 27 cells, pm formation null global groups 1.11-1.28 vs "
        "band 1.09, cips moat null 1.37 vs band 1.12, cips formation null 1.12 (1.14, 1.05), pm B_links_core ranges",
        "no file outside rescore_fair/ modified (mtimes)"],
    not_checked=["bundle-proof forecasts (2-member true simulator, 64-member persistence)", "cips formation diagnostics/",
                 "vortex long2 and main caveat numbers beyond those listed"],
    edits=[
        "added ranking.weakest_mechanism_control_overall (vortex/long2 eps0: per case c003 1.530->1.707, aggregate "
        "1.560->1.739); report text said 1.60->1.79 rods walloff",
        "added ranking.ratio_to_native_change_factor (per case 0.975-1.778, persistence 1.06-1.78; aggregate non-native "
        "0.975-1.32, native-like 0.93-1.08); report text said every ratio rises 1.06-1.48x",
        "no existing numeric field of summary.json was found wrong; nothing else changed (pre-edit copy: checker/summary.before_checker.json)"],
    report_text_corrections=[
        "weakest mechanism control is vortex long2 eps0 (1.53->1.71 per case), not rods walloff (1.60->1.79); still far above 1",
        "ratios to native do not all rise 1.06-1.48x: per case 0.975-1.78x (persistence up to 1.78x on vortex main c004); "
        "native-like ensembles' ratios fall or rise 0.93-1.08x",
        "per-case flips: 19 of 20 between native-equivalent ensembles; one (cips iter2 hold_neck, ignore_actions vs "
        "wrong_probe_geometry, 0.07% -> 0.97% apart) between two naive controls; gaps 0.02-13.8% before, not 1-12%",
        "cips S does not rest on keep_empty: steer_p stays 'at the probe' (12.1), which alone keeps S in Singled out; "
        "keep_empty (1.509) is only the last 'specific' S card"])
p.write_text(json.dumps(d, indent=1, allow_nan=False) + "\n")
print("ok", len(p.read_text()))
