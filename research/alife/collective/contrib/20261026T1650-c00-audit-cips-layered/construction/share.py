"""Summarize the per-body source split of the rim s from world_tag.py's log.
usage: python share.py tag_sSEED.jsonl OUTPREFIX"""
import sys, json
import numpy as np
rows = [json.loads(l) for l in open(sys.argv[1])]
out = sys.argv[2]
tab = []
allb = []
for r in rows:
    b = r["bodies"]
    if not b:
        tab.append({"t": r["t"], "n": 0, "cat_share_body": r["cat_share_body"]}); continue
    rb = np.array([x["rim_body"] for x in b]); rn = np.array([x["rim_band"] for x in b]); rf = np.array([x["rim_far"] for x in b])
    cb = np.array([x["catch_body"] for x in b])
    rc = [x["rim_core"] for x in b if x["rim_core"] is not None]; ro = [x["rim_out"] for x in b if x["rim_out"] is not None]
    tab.append({"t": r["t"], "n": len(b), "cat_share_body": round(r["cat_share_body"], 3), "cat_share_band": round(r["cat_share_band"], 3),
                "rim_body_min": round(float(rb.min()), 3), "rim_body_med": round(float(np.median(rb)), 3),
                "rim_bodyband_min": round(float((rb + rn).min()), 3), "rim_far_max": round(float(rf.max()), 3),
                "catch_body_min": round(float(cb.min()), 3),
                "rim_core_min": round(min(rc), 2) if rc else None, "rim_out_min": round(min(ro), 2) if ro else None,
                "s_global_body_share": round(r["sb_total"] / r["s_total"], 3)})
    for x in b:
        allb.append((r["t"], x["area"], x["rim_body"], x["rim_body"] + x["rim_band"]))
A = np.array(allb)
summ = {"body_samples": int(len(A)),
        "rim_body_lt_0.5": int((A[:, 2] < 0.5).sum()), "rim_bodyband_lt_0.5": int((A[:, 3] < 0.5).sum()),
        "samples_lt_0.5_times": sorted(set(float(t) for t, a, x, y in allb if x < 0.5)),
        "rim_body_median_all": float(np.median(A[:, 2])), "rim_body_min_all": float(A[:, 2].min()),
        "rim_body_min_after_t500": float(A[A[:, 0] >= 500, 2].min()) if (A[:, 0] >= 500).any() else None,
        "rim_body_min_t_ge_1000": float(A[A[:, 0] >= 1000, 2].min()) if (A[:, 0] >= 1000).any() else None}
json.dump({"summary": summ, "table": tab}, open(out + ".json", "w"), indent=0)
for row in tab:
    print(row)
print(summ)
