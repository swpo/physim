"""canalyze -- derived tables of the study `bias2` (local, numpy only): what each bias found in each world.

usage: python -B canalyze.py RESULTS_DIR [world ...]
Reads RESULTS_DIR/<world>/combined.json (written on the pod by ccombine.py) and writes
RESULTS_DIR/analysis.json and RESULTS_DIR/table_<world>.txt. Per world:
  hand        every c = 1 hand design: closure ceilings, persistence ceiling, effective dimension (participation
              ratio PR), predictable content, how much the box mean moves (0 = conserved), ranked by slowness
  configs     every learned config: ceilings, PR, content, and its identification by PER-BLOCK LOCAL READOUTS:
              best block design under the symmetric score min(R2(H | Z), R2(Z | H)) for loc1 / loc1q / loc9, the
              same feature's tent (8-px halo) version, the round-4 global-ridge score, agreement with the closed-form
              slow features, seed agreement, the linear window's field shares
  matched     each learned c = 1 latent against hand designs AT THE SAME EFFECTIVE DIMENSION: every hand feature
              is a family over windows (block, tents with a 4 / 8 / 16-px halo) whose PR falls with smoothing; a
              metric is interpolated linearly in PR inside each family that brackets the learned latent's PR; the
              comparison is with the best such family and with the family of the best-agreeing feature
"""
import json
import os
import sys

import numpy as np

R = sys.argv[1]
WORLDS = sys.argv[2:] or [w for w in ("gliders", "vortex", "membrane") if os.path.exists(os.path.join(R, w, "combined.json"))]
HZ = [1, 2, 4, 8, 16]
HI = {h: i for i, h in enumerate(HZ)}
f4 = lambda v: None if v is None else (np.round(np.asarray(v, float), 4).tolist() if np.ndim(v) else round(float(v), 4))   # noqa: E731


def nz(v):
    return float("nan") if v is None else v


def sym(a, mode):
    """min of the two directions of one readout mode (None if either is missing)."""
    x, y = a[mode]["H_from_Z"], a[mode]["Z_from_H"]
    return None if x is None or y is None else float(min(x, y))


def ident(agr, mode, suffix="_h0", top=3):
    """Hand designs with the given suffix ranked by the symmetric score of one readout mode."""
    rows = [(k[:-len(suffix)], sym(v, mode)) for k, v in agr.items() if k.endswith(suffix)]
    rows = sorted([r for r in rows if r[1] is not None], key=lambda r: -r[1])
    return rows[:top]


def hand_row(r):
    nt = r["nontriv"]
    return {"ceiling_G": f4(r["G"]["ceiling"]), "se": f4(r["G"]["se"]), "ceiling_GL": f4(r["GL"]["ceiling"]) if "GL" in r else None,
            "persistence_ceiling": f4(r["persistence_ceiling"]), "oracle_share_of_V0": f4(r["oracle_share_of_V0"]),
            "PR": f4(nt["participation_ratio"]), "r_dyn": f4(nt["r_dyn"]), "I_avail": f4(r["logdet"]["I_avail"]),
            "I_capt": f4(r["logdet"]["I_capt"]), "box_mean_var_share": f4(nt["box_mean_var_share"]),
            "box_mean_time_var_x64": f4(nt["box_mean_time_var_x64"]), "box_mean_drift_sd": f4(nt["box_mean_drift_sd"]),
            "block_autocorr": {h: f4(v) for h, v in nt["block_autocorr"].items()}, "q": r["q"]}


def families(C):
    """{feature: [(h, PR, row)]} for the c = 1 hand designs present at several windows."""
    fam = {}
    for k, r in C["hand"].items():
        if "_h" not in k or r["q"] != 64:
            continue
        f, h = k.rsplit("_h", 1)
        fam.setdefault(f, []).append((int(h), float(r["nontriv"]["participation_ratio"]), r))
    return {f: sorted(v) for f, v in fam.items()}


def metric_of(r, name):
    if name.startswith("ceil"):
        v = r["G"]["ceiling"][HI[int(name[4:])]] if "G" in r else r["ceiling_G"][HI[int(name[4:])]]
    else:
        key, h = name.split("@")
        v = (r["logdet"] if "logdet" in r else r)[key][HI[int(h)]]
    return None if v is None else float(v)


METRICS = ("ceil1", "ceil4", "ceil16", "I_avail@1", "I_capt@1", "I_capt@4")


def at_pr(fam_rows, pr, name):
    """Linear interpolation in PR of a metric along one hand family -> (value, clamped). Outside the family's PR
    range the nearest end is used (clamped = True: the family cannot be matched in effective dimension there)."""
    pts = sorted((p, metric_of(r, name)) for _, p, r in fam_rows)
    xs, ys = [p for p, _ in pts], [y for _, y in pts]
    if any(y is None for y in ys):
        return None
    return float(np.interp(pr, xs, ys)), bool(pr < xs[0] - 1e-9 or pr > xs[-1] + 1e-9)


def analyse(world):
    C = json.load(open(os.path.join(R, world, "combined.json")))
    out = {"world": world, "fields": C["fields"], "layout": C["layout"], "hand": {}, "configs": {}, "matched": {}}
    fam = families(C)
    for k, r in C["hand"].items():
        out["hand"][k] = hand_row(r)
        if k in ("sfa_c1", "sfax_c1") or k.endswith("_h0"):
            out["hand"][k]["ident_loc1"] = ident(r["agreement"], "loc1")
    slow = sorted([(k[:-3], out["hand"][k]["ceiling_G"][HI[16]], out["hand"][k]["block_autocorr"]["16"][0],
                    out["hand"][k]["box_mean_time_var_x64"][0]) for k in out["hand"] if k.endswith("_h0")], key=lambda r: -r[1])
    out["hand_block_designs_by_ceiling16"] = [{"feature": a, "ceiling16": b, "block_autocorr16": c, "box_mean_time_var_x64": d}
                                              for a, b, c, d in slow]
    out["families_PR"] = {f: [(h, round(p, 2)) for h, p, _ in v] for f, v in fam.items()}
    for nm, r in C["configs"].items():
        agr = r["agreement"]
        row = {k: r[k] for k in ("enc", "h", "obj", "c", "n_seeds")}
        row.update({"ceiling_G": f4(r["ceiling_G"]), "ceiling_G_se": f4(r["ceiling_G_se_mean"]),
                    "ceiling_G_seed_diff": f4(r.get("ceiling_G_seed_diff")), "ceiling_GL": f4(r.get("ceiling_GL")),
                    "persistence_ceiling": f4(r["persistence_ceiling"]), "PR": f4(r["nontriv"]["participation_ratio"]),
                    "r_dyn": f4(r["nontriv"]["r_dyn"]), "I_avail": f4(r["I_avail"]), "I_capt": f4(r["I_capt"]),
                    "box_mean_time_var_x64": f4(r["nontriv"]["box_mean_time_var_x64"]),
                    "box_mean_var_share": f4(r["nontriv"]["box_mean_var_share"]),
                    "seed_loc1": f4(r["seed_agreement"].get("loc1_mean")), "seed_glob": f4(r["seed_agreement"].get("glob_mean"))})
        if "train" in r:
            row["best_step"] = r["train"]["best_step"]
            row["val_best_over_init"] = f4(np.mean(np.asarray(r["train"]["val_best"], float) / np.asarray(r["train"]["val_init"], float))) \
                if r["train"]["steps"] else None
        if "field_shares" in r:
            row["field_shares"] = [{k: round(v, 3) for k, v in ch.items()} for ch in r["field_shares"]]
        idn = {}
        for mode in ("loc1", "loc1q", "loc9", "glob"):
            idn[mode] = [(a, round(b, 4)) for a, b in ident(agr, mode)]
        row["ident_block"] = idn
        if idn["loc1"]:
            f = idn["loc1"][0][0]
            row["best_feature"] = f
            row["best_feature_scores"] = {
                "block": {m: f4(sym(agr[f + "_h0"], m)) for m in ("loc1", "loc1q", "loc9", "glob")},
                "tent8": {m: f4(sym(agr[f + "_h8"], m)) for m in ("loc1", "loc1q", "loc9", "glob")},
                "block_directions_loc1": {d: f4(agr[f + "_h0"]["loc1"][d]) for d in ("H_from_Z", "Z_from_H")},
                "tent8_directions_loc1": {d: f4(agr[f + "_h8"]["loc1"][d]) for d in ("H_from_Z", "Z_from_H")}}
            row["best_tent_feature"] = [(a, round(b, 4)) for a, b in ident(agr, "loc1", "_h8", 1)]
        row["contains_loc1"] = {k[:-3]: f4(v["loc1"]["H_from_Z"]) for k, v in agr.items() if k.endswith("_h0")}   # R2(H | Z)
        row["contains_loc9"] = {k[:-3]: f4(v["loc9"]["H_from_Z"]) for k, v in agr.items() if k.endswith("_h0")}
        row["closed"] = {k: {m: f4(sym(agr[k], m)) for m in ("loc1", "glob")} for k in ("sfa_c1", "sfax_c1") if k in agr}
        row["multi"] = {k: {"loc1_H_from_Z": f4(v["loc1"]["H_from_Z"]), "loc1_Z_from_H": f4(v["loc1"]["Z_from_H"])}
                        for k, v in agr.items() if "_h" not in k and not k.startswith("sfa")}
        out["configs"][nm] = row
        if r["c"] == 1 and fam:
            pr = float(r["nontriv"]["participation_ratio"])
            m = {"PR": round(pr, 2), "metrics": {}}
            for name in METRICS:
                mine = metric_of(r, name)
                if mine is None:
                    continue
                allc = {f: at_pr(v, pr, name) for f, v in fam.items()}
                allc = {f: v for f, v in allc.items() if v is not None}
                cands = {f: v[0] for f, v in allc.items() if not v[1]}          # families that bracket the learned PR
                e = {"learned": round(mine, 4), "n_families_bracketing": len(cands)}
                if cands:
                    fb = max(cands, key=cands.get)
                    e.update({"best_hand_family": fb, "best_hand_at_PR": round(cands[fb], 4), "diff_vs_best_hand": round(mine - cands[fb], 4)})
                bf = row.get("best_feature")
                if bf in allc:
                    e.update({"own_family": bf, "own_family_at_PR": round(allc[bf][0], 4), "own_family_clamped": allc[bf][1],
                              "diff_vs_own_family": round(mine - allc[bf][0], 4)})
                m["metrics"][name] = e
            out["matched"][nm] = m
    return out


def table(a):
    L = [f"world {a['world']}  (fields {a['fields']}; layout {a['layout']})", "",
         "hand block designs (c = 1, 16-px block means), by closure ceiling at h = 16:",
         "feature | ceiling h=1,4,16 | persistence 1,4,16 | PR | I_avail@1 | I_capt@1 | box-mean time var x64"]
    for e in a["hand_block_designs_by_ceiling16"]:
        h = a["hand"][e["feature"] + "_h0"]
        L.append(f"{e['feature']:6s} | {h['ceiling_G'][0]:.3f} {h['ceiling_G'][2]:.3f} {h['ceiling_G'][4]:.3f} | "
                 f"{h['persistence_ceiling'][0]:.3f} {h['persistence_ceiling'][2]:.3f} {h['persistence_ceiling'][4]:.3f} | {h['PR']:.1f} | "
                 f"{nz(h['I_avail'][0]):.0f} | {nz(h['I_capt'][0]):.0f} | {h['box_mean_time_var_x64'][0]:.3g}")
    for k in ("sfa_c1", "sfax_c1", "pca_c1"):
        if k in a["hand"]:
            h = a["hand"][k]
            L.append(f"{k:6s} | {h['ceiling_G'][0]:.3f} {h['ceiling_G'][2]:.3f} {h['ceiling_G'][4]:.3f} | "
                     f"{h['persistence_ceiling'][0]:.3f} {h['persistence_ceiling'][2]:.3f} {h['persistence_ceiling'][4]:.3f} | {h['PR']:.1f} | "
                     f"{nz(h['I_avail'][0]):.0f} | {nz(h['I_capt'][0]):.0f} | {h['box_mean_time_var_x64'][0]:.3g}")
    L += ["", "learned configs: ceiling h=1,4,16 | PR | I_capt@1 | best block design (loc1 sym; its tent8; loc1q; loc9; glob) | sfa/sfax loc1 | seed loc1 | field shares"]
    for nm, r in a["configs"].items():
        bf = r.get("best_feature", "-")
        s = r.get("best_feature_scores", {})
        b, t = s.get("block", {}), s.get("tent8", {})
        fs = r.get("field_shares")
        cl = r.get("closed", {})
        L.append(f"{nm:15s} | {r['ceiling_G'][0]:.3f} {r['ceiling_G'][2]:.3f} {r['ceiling_G'][4]:.3f} | {r['PR']:.1f} | {nz(r['I_capt'][0]):.0f} | "
                 f"{bf} {b.get('loc1')} (tent {t.get('loc1')}; q {b.get('loc1q')}; 9 {b.get('loc9')}; glob {b.get('glob')}) | "
                 f"{cl.get('sfa_c1', {}).get('loc1')}/{cl.get('sfax_c1', {}).get('loc1')} | {r['seed_loc1']} | {fs[0] if fs else ''}")
    L += ["", "matched effective dimension (c = 1): learned minus the best hand family interpolated at the learned PR",
          "config | PR | ceil4: learned, best hand (family), diff; own = the best-agreeing feature's family (* = PR outside its range, nearest window used) | ceil16: ... | I_capt@1: ..."]
    for nm, m in a["matched"].items():
        def cell(k):
            e = m["metrics"].get(k)
            if e is None:
                return "n/a"
            own = (f"; own {e['own_family']} {e['own_family_at_PR']}{'*' if e['own_family_clamped'] else ''} {e['diff_vs_own_family']:+.3f}"
                   if "own_family" in e else "")
            if "best_hand_at_PR" not in e:
                return f"{e['learned']} (no family brackets{own})"
            return f"{e['learned']} vs {e['best_hand_at_PR']} ({e['best_hand_family']}) {e['diff_vs_best_hand']:+.3f}{own}"
        L.append(f"{nm:15s} | {m['PR']} | {cell('ceil4')} | {cell('ceil16')} | {cell('I_capt@1')}")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    A = {}
    for w in WORLDS:
        A[w] = analyse(w)
        with open(os.path.join(R, f"table_{w}.txt"), "w") as f:
            f.write(table(A[w]))
        print(table(A[w]))
    json.dump(A, open(os.path.join(R, "analysis.json"), "w"), indent=None, separators=(",", ":"))
