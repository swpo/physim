"""make_table -- the candidates table of DESIGN.md from results/screen_*.json (no simulation).

    python -B make_table.py            writes results/table.json and prints markdown rows

Per run: members without cells at T0; the screen gap (value +- SE over members) per view and program class;
the gap of an oracle of the comparison law that ignores the program; the target cell's mass shift truth - public
at h = 8 ticks in oracle replicate SDs with its z over members.
"""
import glob
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    rows = {}
    for f in sorted(glob.glob(os.path.join(HERE, "results", "screen_*.json"))):
        d = json.load(open(f))
        tag = os.path.basename(f)[len("screen_"):-len(".json")]
        st = d["state_at_T0"]
        r = {"file": "results/" + os.path.basename(f), "cand": d["cand"], "lam": d["lam"], "size": d["size"],
             "members": d["members"], "R": d["R"], "seed": d["seed"], "hidden_overrides": d.get("hidden_overrides"),
             "comparison": d.get("comparison_simulator", "public law from the projected state"),
             "members_without_cells_at_T0": int(sum(1 for c in st["cells_at_T0"] if c == 0)),
             "cells_at_T0_mean": sum(st["cells_at_T0"]) / len(st["cells_at_T0"]),
             "phi_area_at_T0_mean": (sum(st["phi_area_at_T0"]) / len(st["phi_area_at_T0"])) if "phi_area_at_T0" in st else None,
             "cpu_s": d.get("cpu_s_total"), "member_ticks": d.get("member_ticks")}
        for v, vv in d["screen"].items():
            r[v] = {c: [vv[c]["screen_gap"], vv[c]["se_members"]] for c in vv}
            r[v + "_ignore_program"] = {c: vv[c]["gap_if_program_ignored"] for c in ("blind", "feed", "starve")}
        tm = d["shift_truth_minus_public"]["target_mass"]
        r["target_mass_shift_h8_in_oracle_sd"] = {c: [tm[c]["shift_over_oracle_sd"][1], tm[c]["z_members"][1]] for c in tm}
        rows[tag] = r
    json.dump(rows, open(os.path.join(HERE, "results", "table.json"), "w"), indent=1)

    def g(x):
        return "n/a" if x is None or x[0] != x[0] else f"{x[0]:+.3f} ± {x[1]:.3f}"
    for view in ("pop", "raster", "focus"):
        print(f"\n### {view}\n| run | no cells | none | blind | feed | starve | inputs | ignore-program feed / starve |")
        print("|---|---|---|---|---|---|---|---|")
        for tag, r in rows.items():
            if view not in r:
                continue
            ip = r[view + "_ignore_program"]
            print(f"| {tag} | {r['members_without_cells_at_T0']}/{r['members']} | " +
                  " | ".join(g(r[view][c]) for c in ("none", "blind", "feed", "starve", "inputs")) +
                  f" | {ip['feed']:.3f} / {ip['starve']:.3f} |")
    print("\n### target-cell mass, truth - comparison law at h = 8, in oracle SDs (z over members)")
    for tag, r in rows.items():
        t = r["target_mass_shift_h8_in_oracle_sd"]
        print(f"| {tag} | " + " | ".join(f"{t[c][0]:+.1f} ({t[c][1]:+.1f})" for c in ("none", "blind", "feed", "starve")) + " |")


if __name__ == "__main__":
    main()
