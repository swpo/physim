"""aggregate.py — collect soup_assay rows -> validation table + rank."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))

ORDER = ["m0", "m4", "xv", "bf", "pred", "coex", "mv3"]
LABEL = dict(m0="a_gas", m4="b_travelbond", xv="c_rotor", bf="d_bfield",
             pred="e_predation", coex="f_coexist3", mv3="g_machinev3")

def rows(metrics_name="metrics_dev"):
    data = json.load(open(os.path.join(HERE, "results.json")))
    out = {}
    for r in data:
        if r.get("kind") != "soup_assay" or r.get("metrics") != metrics_name:
            continue
        w = r["tag"].replace("gt_", "")
        out.setdefault(w, []).append(r)
    return out

def table(metrics_name="metrics_dev"):
    R = rows(metrics_name)
    lines = []
    hd = ["world", "seed", "int", "C1pop", "C2time", "C3mot", "C4grph",
          "C5mem", "C6eco", "n_end", "model", "phase", "mvfrac", "vcorr",
          "r_emerg", "turn", "spp"]
    lines.append(" | ".join(f"{h:>8}" for h in hd))
    ranks = []
    for w in ORDER:
        for r in R.get(w, []):
            b = r["battery"]; C = b["C"]; D = b["D"]
            row = [LABEL[w], r["seed"], round(b["interest"], 1),
                   *[round(C[k], 2) for k in ("C1_popdyn", "C2_timescale",
                     "C3_motion", "C4_graph", "C5_memory", "C6_ecology")],
                   round(D["d1"]["n_end"], 0), D["d1"]["model"],
                   D["d5"]["phase"], round(D["d4"]["moving_frac"], 2),
                   round(D["d4"]["v_corr"], 2),
                   round(D["d2"].get("r_emerg") or 0, 1),
                   round(D["d1"].get("turnover") or 0, 2),
                   f'{D["d1"].get("n_species_alive","?")}/{D["d1"].get("n_species_seeded","?")}']
            lines.append(" | ".join(f"{str(v):>8}" for v in row))
            ranks.append((w, r["seed"], b["interest"]))
    return "\n".join(lines), ranks

if __name__ == "__main__":
    mn = sys.argv[1] if len(sys.argv) > 1 else "metrics_dev"
    t, ranks = table(mn)
    print(t)
    print()
    ranks.sort(key=lambda z: -z[2])
    print("RANK:", " > ".join(f"{w}(s{s})={i:.1f}" for w, s, i in ranks))
