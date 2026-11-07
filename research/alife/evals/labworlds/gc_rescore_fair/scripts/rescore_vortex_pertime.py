"""vortex/review3/pertime.py with both estimators: long2's frozen groups restricted to one query time, ignore_actions,
wrong_probe_geometry and native_b against the independent native per case (quoted in the long2 cards' caveats).
Checks the plugin result against review3/pertime_scores.json. usage: rescore_vortex_pertime.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

L2 = C.GC / "vortex" / "long2"
TIMES = [0, 2, 5, 8, 10, 12, 15, 20, 22, 25, 30, 35, 40, 45, 50]
SCORE_TIMES = [2, 5, 8, 10, 12, 15, 20, 25, 30, 35, 40, 45, 50]


def main():
    s = C.jload(L2 / "suite.json")
    out = {e: {} for e in C.ESTS}
    for x in s["cases"]:
        truth = C.load_npz(L2 / x["truth"])[0]
        rost = C.roster_for(truth)
        preds = {}
        for name in ("independent_native", "ignore_actions", "wrong_probe_geometry", "native_b"):
            p = L2 / "controls" / ("ignore_actions.npz" if name == "ignore_actions" else f"{x['id']}/{name}.npz")
            if name == "native_b" and x["program"] == "sham":
                p = L2 / "controls" / "ignore_actions.npz"
            preds[name] = [a[:4] for a in C.load_npz(p)[0]]
        for e in C.ESTS:
            row = {}
            for tu in SCORE_TIMES:
                ti = TIMES.index(tu)
                groups = []
                for g in s["groups"]:
                    keep = [k for k, sel in enumerate(g["selectors"]) if sel["time_index"] == ti]
                    groups.append(dict(id=g["id"], selectors=[g["selectors"][k] for k in keep],
                                       scales=[g["scales"][k] for k in keep], unit="x"))
                sc = {n: C.score(x["request"], p, truth, groups, 4, 2, rost, e) for n, p in preds.items()}
                ref = sc["independent_native"]["joint_energy_equal_group_mean"]
                gref = {g["id"]: g["energy_score"] for g in sc["independent_native"]["joint_energy"]}
                row[tu] = {n: dict(agg=round(sc[n]["joint_energy_equal_group_mean"] / ref, 3),
                                   top=sorted(((g["id"], round(g["energy_score"] / gref[g["id"]], 2))
                                               for g in sc[n]["joint_energy"]), key=lambda kv: -kv[1])[:3])
                           for n in sc if n != "independent_native"}
            out[e][x["program"]] = row
    for e in C.ESTS:
        C.jdump(C.OUT_ROOT / "vortex" / "long2" / e / "pertime_scores.json", C.jload_str(out[e]))
    d = C.diff(C.jload(C.GC / "vortex" / "review3" / "pertime_scores.json"),
               C.jload(C.OUT_ROOT / "vortex" / "long2" / "plugin" / "pertime_scores.json"))
    print("plugin vs review3/pertime_scores.json differences:", len(d), d[:3])


if __name__ == "__main__":
    main()
