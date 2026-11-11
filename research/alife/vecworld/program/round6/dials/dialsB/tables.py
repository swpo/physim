"""tables -- the README's tables as markdown, printed from results/job/analysis.json and ranges.json (no numpy).

    python -B tables.py [RESULTS_JOB_DIR]

Every number is read from the job's files (copied to results/job/ by make_summary.py); nothing is recomputed.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
D = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "results", "job")
A = json.load(open(os.path.join(D, "analysis.json")))
R = json.load(open(os.path.join(D, "ranges.json")))
seeds = [str(s) for s in A["seeds"]]
f2 = lambda v: "n/a" if v is None else f"{v:+.2f}"          # noqa: E731
f3 = lambda v: "n/a" if v is None else f"{v:.3f}"           # noqa: E731

print("### Conditions (focus view, pooled over the 8 seeds and 8, 16, 32 ticks)\n")
print("| condition | number | one-sided 90% bounds of the per-seed contrast (>= 0 means it holds) | at the point estimate | reading |")
print("|---|---|---|---|---|")
for k, c in A["conditions"].items():
    if "closed" in c:
        print(f"| {k} | closed {c['closed']:.3f} | mean {c['mean']:+.3f}, lower {c['lower90']:+.3f}, upper {c['upper90']:+.3f} | "
              f"{'holds' if c['holds_at_point'] else 'fails'} | {c['reading']} |")
    else:
        ct = A["arms"]["main"]["stand_in"]["mix_8_16_32"]["contrast_s_ge_0.10"]
        print(f"| {k} | share {c['share_s']:.3f} | mean {ct['mean']:+.3f}, lower {ct['lower90']:+.3f}, upper {ct['upper90']:+.3f} | "
              f"{'holds' if c['holds_at_point'] else 'fails'} | {c['reading']}; {c['status']} |")
print(f"\nVerdict: **{A['verdict']['three_way']}**; the plan's rule at the point estimates: **{A['verdict']['plan_rule_at_point_estimates']}**.\n")

for arm in A["arms"]:
    F = A["arms"][arm]["focus"]
    al, hl = F["all_start_states"]["pooled_8_16_32"], F["heaviest_left_out"]["pooled_8_16_32"]
    print(f"### Per seed, {arm} arm (focus view, share of the public-to-oracle gap closed over 8, 16, 32 ticks)\n")
    print("| seed | rho, D_X, a0 (pilot) | items | heaviest state's share of the gap | G* is | G2 | G3 | A_act | G* | G*, heaviest out | H | H, heaviest out |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for j, s in enumerate(seeds):
        t = A["truths_pilot"][s]
        hv = A["arms"][arm]["heaviest"][s]
        print(f"| {s} | {t['rho']:.4f}, {t['DX']:.3f}, {t['a0']:.4f} | {hv['items']} | {hv['share_of_gap']:.2f} | {F['Gstar_picks'][s]} | "
              + " | ".join(f2(al[p]["per_seed"][j]) for p in ("G2", "G3", "A_act", "Gstar")) + f" | {f2(hl['Gstar']['per_seed'][j])} | "
              f"{f2(al['H']['per_seed'][j])} | {f2(hl['H']['per_seed'][j])} |")
    print("| **pooled** | | | | | " + " | ".join(f"**{f2(al[p]['closed'])}**" for p in ("G2", "G3", "A_act", "Gstar"))
          + f" | **{f2(hl['Gstar']['closed'])}** | **{f2(al['H']['closed'])}** | **{f2(hl['H']['closed'])}** |")
    print("| median of seeds | | | | | " + " | ".join(f2(al[p]["median_seed"]) for p in ("G2", "G3", "A_act", "Gstar"))
          + f" | {f2(hl['Gstar']['median_seed'])} | {f2(al['H']['median_seed'])} | {f2(hl['H']['median_seed'])} |")
    rng = lambda x: f"{x[0]:+.2f} to {x[1]:+.2f}"          # noqa: E731
    print("| leave-one-seed-out range | | | | | " + " | ".join(rng(al[p]["leave_one_seed_out_range"]) for p in ("G2", "G3", "A_act", "Gstar"))
          + f" | {rng(hl['Gstar']['leave_one_seed_out_range'])} | {rng(al['H']['leave_one_seed_out_range'])} | {rng(hl['H']['leave_one_seed_out_range'])} |")
    print("| bootstrap over seeds, 5%-95% | | | | | " + " | ".join(rng(al[p]["bootstrap_seeds_5_95"]) for p in ("G2", "G3", "A_act", "Gstar"))
          + f" | {rng(hl['Gstar']['bootstrap_seeds_5_95'])} | {rng(al['H']['bootstrap_seeds_5_95'])} | {rng(hl['H']['bootstrap_seeds_5_95'])} |")
    print()
    print(f"### Per horizon, {arm} arm (pooled over seeds; share of the gap at that horizon closed)\n")
    print("| view | start states | policy | 4 ticks | 8 | 16 | 32 | pooled 8-32 |")
    print("|---|---|---|---|---|---|---|---|")
    for view, vname in (("focus", "focus"), ("cr", "cell-resolved list")):
        for sub, sname in (("all_start_states", "all"), ("heaviest_left_out", "heaviest out")):
            B = A["arms"][arm][view][sub]
            for p in ("G2", "G3", "A_act", "Gstar", "H", "G1", "G4", "pub0"):
                if view == "cr" and p in ("G1", "G4", "pub0"):
                    continue
                print(f"| {vname} | {sname} | {'G*' if p == 'Gstar' else p} | " + " | ".join(f2(B["by_horizon"][h][p]) for h in ("4", "8", "16", "32"))
                      + f" | {f2(B['pooled_8_16_32'][p]['closed'])} |")
    gs = A["arms"][arm]["focus"]["gap_share_by_horizon_8_16_32"]
    print(f"\nShare of the pooled gap at 8, 16, 32 ticks (focus view): {gs[0]:.2f}, {gs[1]:.2f}, {gs[2]:.2f}.\n")
    print(f"### Per seed and horizon, {arm} arm (focus view, all start states)\n")
    print("| seed | G* 8 | G* 16 | G* 32 | A_act 8 | A_act 16 | A_act 32 | H 8 | H 16 | H 32 |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    bh = A["arms"][arm]["focus"]["all_start_states"]["by_horizon_per_seed"]
    for j, s in enumerate(seeds):
        print(f"| {s} | " + " | ".join(f2(bh[h][p][j]) for p in ("Gstar", "A_act", "H") for h in ("8", "16", "32")) + " |")
    print()
    st = A["arms"][arm]["stand_in"]
    m = st["mix_8_16_32"]
    print(f"### The history-only stand-in, {arm} arm (focus view)\n")
    print("| items | share s = (L(P0s) - L(Cs)) / (L(K) - L(Cs)) | state-given gap | kept | skill of Cs, of the oracle's |")
    print("|---|---|---|---|---|")
    print(f"| declared mix, 8-32 ticks | {f3(m['share_s'])} | {f3(m['state_given_gap'])} | {f2(m['kept'])} | {f3(m['skill_Cs_of_oracle'])} |")
    for c in ("aimed", "blind", "none"):
        b = st["by_class_8_16_32"][c]
        print(f"| {c} only | {f3(b['share_s'])} | {f3(b['state_given_gap'])} | {f2(b['kept'])} | {f3(b['skill_Cs_of_oracle'])} |")
    for h in ("8", "16", "32"):
        b = st["by_horizon_mix"][h]
        print(f"| mix, {h} ticks | {f3(b['share_s'])} | {f3(b['state_given_gap'])} | {f2(b['kept'])} | {f3(b['skill_Cs_of_oracle'])} |")
    print(f"\ns per seed: " + ", ".join(f3(v) for v in m["share_s_per_seed"]) + f"; median {f3(m['share_s_median_seed'])}; leave-one-seed-out "
          f"{f3(m['share_s_leave_one_seed_out_range'][0])} to {f3(m['share_s_leave_one_seed_out_range'][1])}; bootstrap over seeds 5%-95% "
          f"{f3(m['share_s_bootstrap_seeds_5_95'][0])} to {f3(m['share_s_bootstrap_seeds_5_95'][1])}.\n")

print("### Scan C: the ranges of rho, D_X, a0 (screen gap, focus view, 8-32 ticks; 16 members)\n")
print("| parameter | value | gap without input | gap, blind input | gap, aimed input | states with a focus cell | admissible |")
print("|---|---|---|---|---|---|---|")
for k, v in R["carrier_ranges"].items():
    for r in v["rows"]:
        print(f"| {k} | {r['value']:g} | {f3(r['gap_none'])} | {f3(r['gap_blind'])} | {f3(r['gap_aimed'])} | {r['members_with_focus_cell']} | {'yes' if r['admissible'] else 'no'} |")
print("\nRanges: " + "; ".join(f"{k} {v['range'][0]:g} to {v['range'][1]:g}" + (" (scan failed: the centre alone)" if v["scan_failed"] else "") for k, v in R["carrier_ranges"].items()) + ".\n")
print("### Scan V: the hidden parameter set of the public law (8 members; headroom = state-given loss of the default-parameter law)\n")
print("| parameter | family | viable at 0.8, 0.9, 1.1, 1.2 x default | headroom at those | box (x default) | headroom (smaller edge) | eligible |")
print("|---|---|---|---|---|---|---|")
for p, r in R["scan_V"].items():
    via = ", ".join("yes" if r["viable"][f] else "no" for f in ("0.8", "0.9", "1.1", "1.2"))
    hd = ", ".join(f3(r["headroom_by_factor"][f]) for f in ("0.8", "0.9", "1.1", "1.2"))
    box = "none" if r["box_factors"] is None else f"{r['box_factors'][0]:g} to {r['box_factors'][1]:g}"
    print(f"| {p} | {r['family']} | {via} | {hd} | {box} | {f3(r['headroom'])} | {'yes' if r['eligible'] else 'no'} |")
fl = R["scan_V_default_floor"]
print(f"\nNoise floor (the default law against itself): {f3(fl['headroom'])} +- {f3(fl['se_members'])}. Hidden set: "
      + ", ".join(f"{h['param']} in {h['box'][0]:g} to {h['box'][1]:g} ({h['family']}, headroom {h['headroom']:.3f})" for h in R["hidden_set"]) + ".")
